from typing import Dict, List, Optional, Tuple
from environments.environment_abstract import Environment, State
import heapq

import numpy as np
import torch
from torch import nn


_BATCH_SIZE = 4
_WEIGHT = 5.0
_MAX_HEURISTIC_CACHE_SIZE = 250_000
_MAX_TERMINAL_CACHE_SIZE = 250_000
_MAX_ACTION_CACHE_SIZE = 250_000
_MAX_DYNAMICS_CACHE_SIZE = 300_000


class _StateKey:
    __slots__ = ("state", "_hash")

    def __init__(self, state: State):
        self.state = state
        self._hash = hash(state)

    def __hash__(self) -> int:
        return self._hash

    def __eq__(self, other) -> bool:
        if not isinstance(other, _StateKey):
            return NotImplemented
        return self.state == other.state


_HEURISTIC_CACHE: Dict[Tuple[int, int], Dict[_StateKey, float]] = {}
_TERMINAL_CACHE: Dict[int, Dict[_StateKey, bool]] = {}
_ACTION_CACHE: Dict[int, Dict[_StateKey, Tuple[int, ...]]] = {}
_DYNAMICS_CACHE: Dict[int, Dict[Tuple[_StateKey, int], Tuple[float, Tuple[_StateKey, ...]]]] = {}


def _reconstruct_path(parent: Dict[_StateKey, Tuple[_StateKey, int]], state_key: _StateKey) -> List[int]:
    actions: List[int] = []
    while state_key in parent:
        state_key, action = parent[state_key]
        actions.append(action)
    actions.reverse()
    return actions


def _get_terminal_cached(state_key: _StateKey, is_terminal, terminal_cache: Dict[_StateKey, bool]) -> bool:
    cached = terminal_cache.get(state_key)
    if cached is not None:
        return cached

    solved = is_terminal(state_key.state)
    if len(terminal_cache) >= _MAX_TERMINAL_CACHE_SIZE:
        terminal_cache.clear()
    terminal_cache[state_key] = solved
    return solved


def _get_actions_cached(state_key: _StateKey, get_actions, action_cache: Dict[_StateKey, Tuple[int, ...]]) -> Tuple[int, ...]:
    cached = action_cache.get(state_key)
    if cached is not None:
        return cached

    actions = tuple(get_actions(state_key.state))
    if len(action_cache) >= _MAX_ACTION_CACHE_SIZE:
        action_cache.clear()
    action_cache[state_key] = actions
    return actions


def _get_dynamics_cached(
    state_key: _StateKey,
    action: int,
    state_action_dynamics,
    dynamics_cache: Dict[Tuple[_StateKey, int], Tuple[float, Tuple[_StateKey, ...]]],
) -> Tuple[float, Tuple[_StateKey, ...]]:
    cache_key = (state_key, action)
    cached = dynamics_cache.get(cache_key)
    if cached is not None:
        return cached

    reward, next_states, _ = state_action_dynamics(state_key.state, action)
    cached = (reward, tuple(_StateKey(next_state) for next_state in next_states))
    if len(dynamics_cache) >= _MAX_DYNAMICS_CACHE_SIZE:
        dynamics_cache.clear()
    dynamics_cache[cache_key] = cached
    return cached


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """Find a path from the start state to a goal using batched weighted A*."""

    is_terminal = env.is_terminal
    get_actions = env.get_actions
    state_action_dynamics = env.state_action_dynamics
    param = next(nnet.parameters(), None)
    device = param.device if param is not None else torch.device("cpu")
    inf = float("inf")
    heappush = heapq.heappush
    heappop = heapq.heappop

    heuristic_cache = _HEURISTIC_CACHE.setdefault((id(env), id(nnet)), {})
    terminal_cache = _TERMINAL_CACHE.setdefault(id(env), {})
    action_cache = _ACTION_CACHE.setdefault(id(env), {})
    dynamics_cache = _DYNAMICS_CACHE.setdefault(id(env), {})

    if len(heuristic_cache) >= _MAX_HEURISTIC_CACHE_SIZE:
        heuristic_cache.clear()
    if len(terminal_cache) >= _MAX_TERMINAL_CACHE_SIZE:
        terminal_cache.clear()
    if len(action_cache) >= _MAX_ACTION_CACHE_SIZE:
        action_cache.clear()
    if len(dynamics_cache) >= _MAX_DYNAMICS_CACHE_SIZE:
        dynamics_cache.clear()

    def heuristic(state_keys: List[_StateKey]) -> np.ndarray:
        values = np.empty(len(state_keys), dtype=np.float32)
        missing_indices: List[int] = []
        missing_keys: List[_StateKey] = []
        missing_states: List[State] = []

        for idx, state_key in enumerate(state_keys):
            cached = heuristic_cache.get(state_key)
            if cached is None:
                missing_indices.append(idx)
                missing_keys.append(state_key)
                missing_states.append(state_key.state)
            else:
                values[idx] = cached

        if missing_states:
            nnet_input = env.states_to_nnet_input(missing_states)
            tensor = torch.from_numpy(nnet_input)
            if device.type != "cpu":
                tensor = tensor.to(device)

            heuristics = torch.clamp(-nnet(tensor).amax(dim=1), min=0.0).cpu().numpy()

            if len(heuristic_cache) + len(missing_keys) >= _MAX_HEURISTIC_CACHE_SIZE:
                heuristic_cache.clear()

            for idx, state_key, h_val in zip(missing_indices, missing_keys, heuristics):
                heuristic_value = float(h_val)
                heuristic_cache[state_key] = heuristic_value
                values[idx] = heuristic_value

        return values

    start_key = _StateKey(state_start)
    if _get_terminal_cached(start_key, is_terminal, terminal_cache):
        return []

    parent: Dict[_StateKey, Tuple[_StateKey, int]] = {}
    best_g: Dict[_StateKey, float] = {start_key: 0.0}
    closed = set()

    with torch.inference_mode():
        start_h = float(heuristic([start_key])[0])
        heap = [(start_h, 0, start_key, 0.0)]
        counter = 1

        while heap:
            batch: List[Tuple[_StateKey, float]] = []
            while heap and len(batch) < _BATCH_SIZE:
                _, _, state_key, g = heappop(heap)

                if state_key in closed or g > best_g.get(state_key, inf):
                    continue

                if _get_terminal_cached(state_key, is_terminal, terminal_cache):
                    return _reconstruct_path(parent, state_key)

                batch.append((state_key, g))

            if not batch:
                continue

            pending_best_g: Dict[_StateKey, float] = {}
            for state_key, g in batch:
                if state_key in closed:
                    continue

                closed.add(state_key)

                for action in _get_actions_cached(state_key, get_actions, action_cache):
                    reward, next_state_keys = _get_dynamics_cached(
                        state_key, action, state_action_dynamics, dynamics_cache
                    )
                    if not next_state_keys:
                        continue

                    next_state_key = next_state_keys[0]
                    if next_state_key in closed:
                        continue

                    new_g = g - reward
                    if new_g >= best_g.get(next_state_key, inf):
                        continue

                    best_g[next_state_key] = new_g
                    parent[next_state_key] = (state_key, action)

                    if _get_terminal_cached(next_state_key, is_terminal, terminal_cache):
                        return _reconstruct_path(parent, next_state_key)

                    pending_g = pending_best_g.get(next_state_key)
                    if pending_g is None or new_g < pending_g:
                        pending_best_g[next_state_key] = new_g

            if not pending_best_g:
                continue

            pending_state_keys = list(pending_best_g)
            h_vals = heuristic(pending_state_keys)
            for next_state_key, h_val in zip(pending_state_keys, h_vals):
                next_g = pending_best_g[next_state_key]
                heappush(heap, (next_g + _WEIGHT * float(h_val), counter, next_state_key, next_g))
                counter += 1

    return None
