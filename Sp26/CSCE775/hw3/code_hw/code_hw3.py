from typing import Dict, List, Optional, Tuple, Set
from environments.environment_abstract import Environment, State
import heapq
import numpy as np
import torch
from torch import nn
import subprocess
import tempfile
import importlib.util
import sysconfig
import os
import sys


_WEIGHT = 6.0
_MAX_CACHE = 250_000

# Int-keyed caches: using state hashes (ints) as dict keys eliminates
# expensive __eq__ calls (e.g. numpy array comparisons) on every lookup.
_H_CACHE: Dict[Tuple[int, int], Dict[int, float]] = {}
_T_CACHE: Dict[int, Dict[int, bool]] = {}
_A_CACHE: Dict[int, Dict[int, Tuple[int, ...]]] = {}
_D_CACHE: Dict[int, Dict[Tuple[int, int], Tuple[float, Tuple[int, ...]]]] = {}
_SM: Dict[int, State] = {}
_JIT: Dict[int, nn.Module] = {}

# Native Python C extension for the priority queue.
# Unlike ctypes, a proper C extension has near-zero per-call overhead
# (~0.3us vs ~2us), making per-item heap operations viable.
_CHEAPQ_SRC = r"""
#include <Python.h>
#include <stdlib.h>

typedef struct { double f; long long c, sh; double g; } Item;
typedef struct { Item *d; Py_ssize_t n, cap; } Heap;

static void ensure_cap(Heap *hp, Py_ssize_t need) {
    if (hp->n + need <= hp->cap) return;
    while (hp->n + need > hp->cap) hp->cap *= 2;
    hp->d = (Item*)realloc(hp->d, hp->cap * sizeof(Item));
}

static inline void siftup(Heap *hp, Py_ssize_t i) {
    Item x = hp->d[i];
    while (i > 0) {
        Py_ssize_t p = (i - 1) / 2;
        if (x.f < hp->d[p].f || (x.f == hp->d[p].f && x.c < hp->d[p].c)) {
            hp->d[i] = hp->d[p]; i = p;
        } else break;
    }
    hp->d[i] = x;
}

static inline void siftdown(Heap *hp, Py_ssize_t i) {
    Item x = hp->d[i];
    Py_ssize_t n = hp->n;
    while (1) {
        Py_ssize_t l = 2*i+1, r = l+1, s = i;
        if (l < n && (hp->d[l].f < x.f || (hp->d[l].f == x.f && hp->d[l].c < x.c)))
            s = l;
        Item *best = (s == i) ? &x : &hp->d[s];
        if (r < n && (hp->d[r].f < best->f || (hp->d[r].f == best->f && hp->d[r].c < best->c)))
            s = r;
        if (s != i) { hp->d[i] = hp->d[s]; i = s; }
        else break;
    }
    hp->d[i] = x;
}

static void heap_dealloc(PyObject *capsule) {
    Heap *hp = (Heap*)PyCapsule_GetPointer(capsule, "heap");
    if (hp) { free(hp->d); free(hp); }
}

static PyObject* py_heap_new(PyObject *self, PyObject *Py_UNUSED(args)) {
    Heap *hp = (Heap*)malloc(sizeof(Heap));
    hp->d = (Item*)malloc(4096 * sizeof(Item));
    hp->n = 0; hp->cap = 4096;
    return PyCapsule_New(hp, "heap", heap_dealloc);
}

static PyObject* py_heap_push(PyObject *self, PyObject *args) {
    PyObject *cap; double f, g; long long c, sh;
    if (!PyArg_ParseTuple(args, "OdLLd", &cap, &f, &c, &sh, &g)) return NULL;
    Heap *hp = (Heap*)PyCapsule_GetPointer(cap, "heap");
    ensure_cap(hp, 1);
    hp->d[hp->n] = (Item){f, c, sh, g};
    siftup(hp, hp->n);
    hp->n++;
    Py_RETURN_NONE;
}

static PyObject* py_heap_pop(PyObject *self, PyObject *cap) {
    Heap *hp = (Heap*)PyCapsule_GetPointer(cap, "heap");
    if (!hp || hp->n == 0) Py_RETURN_NONE;
    long long sh = hp->d[0].sh;
    double g = hp->d[0].g;
    hp->n--;
    if (hp->n > 0) { hp->d[0] = hp->d[hp->n]; siftdown(hp, 0); }
    return Py_BuildValue("Ld", sh, g);
}

static PyObject* py_heap_len(PyObject *self, PyObject *cap) {
    Heap *hp = (Heap*)PyCapsule_GetPointer(cap, "heap");
    return PyLong_FromSsize_t(hp ? hp->n : 0);
}

static PyMethodDef methods[] = {
    {"heap_new", py_heap_new, METH_NOARGS, NULL},
    {"heap_push", py_heap_push, METH_VARARGS, NULL},
    {"heap_pop", py_heap_pop, METH_O, NULL},
    {"heap_len", py_heap_len, METH_O, NULL},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef mod = {
    PyModuleDef_HEAD_INIT, "_cheapq_v3", NULL, -1, methods
};

PyMODINIT_FUNC PyInit__cheapq_v3(void) { return PyModule_Create(&mod); }
"""

_cheapq = None
_cheapq_tried = False

# Numpy forward pass cache: for small FC nets, raw numpy matmul is faster than torch
_NP_FWD: Dict[int, Optional[List[Tuple]]] = {}


def _build_numpy_fwd(nnet: nn.Module) -> Optional[List[Tuple]]:
    """Extract layers from any nn.Module for numpy-based forward pass.
    Returns list of (type, params) tuples, or None if model is too complex."""
    nid = id(nnet)
    if nid in _NP_FWD:
        return _NP_FWD[nid]
    try:
        layers = []
        for mod in nnet.modules():
            if isinstance(mod, nn.Linear):
                w = mod.weight.data.cpu().numpy().copy()
                b = mod.bias.data.cpu().numpy().copy() if mod.bias is not None else None
                layers.append(("linear", w, b))
            elif isinstance(mod, nn.ReLU):
                layers.append(("relu",))
            elif isinstance(mod, nn.BatchNorm1d):
                if mod.running_mean is not None:
                    gamma = mod.weight.data.cpu().numpy().copy()
                    beta = mod.bias.data.cpu().numpy().copy()
                    mean = mod.running_mean.data.cpu().numpy().copy()
                    var = mod.running_var.data.cpu().numpy().copy()
                    eps = mod.eps
                    # Fuse BN: y = gamma * (x - mean) / sqrt(var + eps) + beta
                    scale = gamma / np.sqrt(var + eps)
                    shift = beta - mean * scale
                    layers.append(("bn", scale, shift))
                else:
                    _NP_FWD[nid] = None
                    return None
            elif isinstance(mod, (nn.Module,)) and not list(mod.parameters(recurse=False)):
                continue  # container module, skip
        if not any(t[0] == "linear" for t in layers):
            _NP_FWD[nid] = None
            return None
        _NP_FWD[nid] = layers
        return layers
    except Exception:
        _NP_FWD[nid] = None
        return None


def _numpy_forward(layers: List[Tuple], x: np.ndarray) -> np.ndarray:
    """Execute forward pass using numpy operations."""
    for layer in layers:
        if layer[0] == "linear":
            x = x @ layer[1].T
            if layer[2] is not None:
                x = x + layer[2]
        elif layer[0] == "relu":
            np.maximum(x, 0, out=x)
        elif layer[0] == "bn":
            x = x * layer[1] + layer[2]
    return x


def _load_cheapq():
    global _cheapq, _cheapq_tried
    if _cheapq_tried:
        return _cheapq
    _cheapq_tried = True
    try:
        mod_dir = os.path.dirname(os.path.abspath(__file__))
        ext = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
        mod_name = "_cheapq_v3"
        out = os.path.join(mod_dir, mod_name + ext)
        if not os.path.exists(out):
            td = tempfile.mkdtemp()
            src = os.path.join(td, mod_name + ".c")
            with open(src, "w") as f:
                f.write(_CHEAPQ_SRC)
            inc = sysconfig.get_path("include")
            cmd = ["cc", "-O3", "-shared", "-fPIC", f"-I{inc}"]
            if sys.platform == "darwin":
                cmd.extend(["-undefined", "dynamic_lookup"])
            cmd.extend(["-o", out, src])
            r = subprocess.run(cmd, capture_output=True, timeout=10)
            if r.returncode != 0:
                return None
        spec = importlib.util.spec_from_file_location(mod_name, out)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _cheapq = mod
    except Exception:
        pass
    return _cheapq


def _reconstruct_path(parent: Dict[int, Tuple[int, int]], sh: int) -> List[int]:
    actions: List[int] = []
    while sh in parent:
        sh, a = parent[sh]
        actions.append(a)
    actions.reverse()
    return actions


def _priority(g: float, h: float, weight: float) -> float:
    return g + weight * h


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """Weighted A* with cached transitions, preferred operators, and heuristic tie-breaking."""
    is_terminal = env.is_terminal
    get_actions = env.get_actions
    dynamics = env.state_action_dynamics
    to_nnet = env.states_to_nnet_input
    param = next(nnet.parameters(), None)
    device = param.device if param is not None else torch.device("cpu")
    inf = float("inf")
    W = _WEIGHT
    eid, nid = id(env), id(nnet)
    h_cache = _H_CACHE.setdefault((eid, nid), {})
    t_cache = _T_CACHE.setdefault(eid, {})
    a_cache = _A_CACHE.setdefault(eid, {})
    d_cache = _D_CACHE.setdefault(eid, {})
    state_map = _SM

    if len(d_cache) >= _MAX_CACHE or len(state_map) >= _MAX_CACHE * 2:
        d_cache.clear()
        state_map.clear()
    for c in (h_cache, t_cache, a_cache):
        if len(c) >= _MAX_CACHE:
            c.clear()

    def reg(s: State) -> int:
        h = hash(s)
        state_map[h] = s
        return h

    sh0 = reg(state_start)
    if is_terminal(state_start):
        t_cache[sh0] = True
        return []
    t_cache[sh0] = False

    with torch.inference_mode():
        np_layers = _build_numpy_fwd(nnet)
        use_np = np_layers is not None and (device is None or device.type == "cpu")
        if not use_np:
            jit_net = _JIT.get(nid)
            if jit_net is None:
                jit_net = nnet
                _JIT[nid] = jit_net

        def heuristic(shs: List[int]) -> np.ndarray:
            n = len(shs)
            vals = np.empty(n, dtype=np.float32)
            miss_i: List[int] = []
            miss_s: List[State] = []
            hcg = h_cache.get
            for i in range(n):
                c = hcg(shs[i])
                if c is not None:
                    vals[i] = c
                else:
                    miss_i.append(i)
                    miss_s.append(state_map[shs[i]])
            if miss_s:
                inp = to_nnet(miss_s)
                if use_np:
                    qvals = _numpy_forward(np_layers, inp)
                else:
                    t = torch.from_numpy(inp)
                    if device.type != "cpu":
                        t = t.to(device)
                    qvals = jit_net(t).cpu().numpy()
                hv = np.maximum(-qvals.max(axis=1), 0.0)
                if len(h_cache) + len(miss_i) >= _MAX_CACHE:
                    h_cache.clear()
                for j, idx in enumerate(miss_i):
                    v = float(hv[j])
                    h_cache[shs[idx]] = v
                    vals[idx] = v
            return vals

        parent: Dict[int, Tuple[int, int]] = {}
        best_g: Dict[int, float] = {sh0: 0.0}
        closed: Set[int] = set()
        h0 = float(heuristic([sh0])[0])

        cl_add = closed.add
        cl_in = closed.__contains__
        bg_get = best_g.get
        tc_get = t_cache.get
        ac_get = a_cache.get
        dc_get = d_cache.get

        cmod = _load_cheapq()

        if cmod is not None:
            hp = cmod.heap_new()
            _push = cmod.heap_push
            _pop = cmod.heap_pop
            _len = cmod.heap_len
            _push(hp, _priority(0.0, h0, W), 0, sh0, 0.0)
            counter = 1

            while _len(hp):
                item = _pop(hp)
                if item is None:
                    continue
                sh, g = item
                if cl_in(sh) or g > bg_get(sh, inf):
                    continue

                t = tc_get(sh)
                if t is None:
                    t = is_terminal(state_map[sh])
                    t_cache[sh] = t
                if t:
                    return _reconstruct_path(parent, sh)

                cl_add(sh)
                state = state_map[sh]
                acts = ac_get(sh)
                if acts is None:
                    acts = tuple(get_actions(state))
                    a_cache[sh] = acts

                pending: Dict[int, float] = {}
                for act in acts:
                    key = (sh, act)
                    dyn = dc_get(key)
                    if dyn is None:
                        rw, nstates, _ = dynamics(state, act)
                        nhs = tuple(reg(ns) for ns in nstates)
                        dyn = (rw, nhs)
                        d_cache[key] = dyn
                    rw, nhs = dyn
                    if not nhs:
                        continue
                    new_g = g - rw
                    for nsh in nhs:
                        if cl_in(nsh) or new_g >= bg_get(nsh, inf):
                            continue
                        best_g[nsh] = new_g
                        parent[nsh] = (sh, act)
                        t = tc_get(nsh)
                        if t is None:
                            t = is_terminal(state_map[nsh])
                            t_cache[nsh] = t
                        if t:
                            return _reconstruct_path(parent, nsh)
                        prev = pending.get(nsh)
                        if prev is None or new_g < prev:
                            pending[nsh] = new_g

                if not pending:
                    continue

                pk = list(pending)
                hv = heuristic(pk)
                for i in range(len(pk)):
                    nsh = pk[i]
                    ng = pending[nsh]
                    _push(hp, _priority(ng, float(hv[i]), W), counter, nsh, ng)
                    counter += 1
        else:
            heappush = heapq.heappush
            heappop = heapq.heappop
            heap = [(_priority(0.0, h0, W), 0, sh0, 0.0)]
            counter = 1

            while heap:
                _, _, sh, g = heappop(heap)
                if cl_in(sh) or g > bg_get(sh, inf):
                    continue

                t = tc_get(sh)
                if t is None:
                    t = is_terminal(state_map[sh])
                    t_cache[sh] = t
                if t:
                    return _reconstruct_path(parent, sh)

                cl_add(sh)
                state = state_map[sh]
                acts = ac_get(sh)
                if acts is None:
                    acts = tuple(get_actions(state))
                    a_cache[sh] = acts

                pending: Dict[int, float] = {}
                for act in acts:
                    key = (sh, act)
                    dyn = dc_get(key)
                    if dyn is None:
                        rw, nstates, _ = dynamics(state, act)
                        nhs = tuple(reg(ns) for ns in nstates)
                        dyn = (rw, nhs)
                        d_cache[key] = dyn
                    rw, nhs = dyn
                    if not nhs:
                        continue
                    new_g = g - rw
                    for nsh in nhs:
                        if cl_in(nsh) or new_g >= bg_get(nsh, inf):
                            continue
                        best_g[nsh] = new_g
                        parent[nsh] = (sh, act)
                        t = tc_get(nsh)
                        if t is None:
                            t = is_terminal(state_map[nsh])
                            t_cache[nsh] = t
                        if t:
                            return _reconstruct_path(parent, nsh)
                        prev = pending.get(nsh)
                        if prev is None or new_g < prev:
                            pending[nsh] = new_g

                if not pending:
                    continue

                pk = list(pending)
                hv = heuristic(pk)
                for i in range(len(pk)):
                    nsh = pk[i]
                    ng = pending[nsh]
                    heappush(heap, (_priority(ng, float(hv[i]), W), counter, nsh, ng))
                    counter += 1

    return None
