"""Simplified Retrosynthesis domain for DeepXube.

Molecules are linear carbon chains where each position carries a functional
group. Most reactions are SITE-SELECTIVE: they act on the position with the
highest reactivity among eligible groups, not a player-chosen position.
This creates tight coupling between positions -- changing a group anywhere
can redirect where the next reaction acts.

Global reagent incompatibilities (e.g. oxidation blocked by bromides present
anywhere) and protecting group mechanics add further planning dependencies.
The result is a genuinely non-decomposable puzzle where the optimal reaction
sequence depends on the entire molecular state.

Functional groups (8):
  H(0), OH(1), C=O(2), NH2(3), COOH(4), Br(5), OPG(6), NPG(7)

Reactions (12 site-selective + 3*N position-specific):
  Site-selective reactions target the eligible position with the highest
  reactivity score. Ties broken by lowest index. Each has a global
  precondition (certain groups must be absent everywhere).

  Position-specific: radical bromination, protect, deprotect.
"""

from typing import List, Tuple, Optional, Dict, Any, FrozenSet
import numpy as np
from numpy.typing import NDArray
import matplotlib.patches as patches
from matplotlib.figure import Figure
import random as stdlib_random

from deepxube.base.factory import Parser
from deepxube.base.domain import (
    State, Action, Goal,
    ActsEnum, GoalStartRevWalkable,
    StateGoalVizable, StringToAct,
)
from deepxube.base.nnet_input import HasFlatSGIn
from deepxube.factories.domain_factory import domain_factory

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from rdkit.Chem.Draw.rdMolDraw2D import MolDraw2DCairo
    from PIL import Image as PILImage
    import io as _io
    _HAS_RDKIT = True
except ImportError:
    _HAS_RDKIT = False

GARNET = "#73000A"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
ROSE = "#CC2E40"
BLACK_90 = "#363636"
BLACK_50 = "#A2A2A2"
BLACK_30 = "#C7C7C7"
BLACK_10 = "#ECECEC"
GRASS = "#CED318"
SANDSTORM = "#FFF2E3"

H = 0
OH = 1
KETONE = 2
NH2 = 3
COOH = 4
BR = 5
OPG = 6
NPG = 7
NUM_GROUPS = 8
NUM_REAL_GROUPS = 6

GROUP_LABELS = ["H", "OH", "C=O", "NH₂", "COOH", "Br", "OPG", "NPG"]
GROUP_ASCII = ["H", "OH", "C=O", "NH2", "COOH", "Br", "OPG", "NPG"]

REACTIVITY = np.array([0, 3, 5, 4, 2, 6, 0, 0], dtype=np.int8)

GROUP_COLORS = [
    BLACK_30,    # H
    ATLANTIC,    # OH
    ROSE,        # C=O
    CONGAREE,    # NH2
    GARNET,      # COOH
    HORSESHOE,   # Br
    HONEYCOMB,   # OPG
    HONEYCOMB,   # NPG
]

_S = frozenset
SELECTIVE_RXNS: List[Tuple[str, FrozenSet[int], Dict[int, int], FrozenSet[int]]] = [
    ("mild_oxidation",      _S({OH}),           {OH: KETONE},               _S({BR})),
    ("strong_oxidation",    _S({OH, KETONE}),   {OH: COOH, KETONE: COOH},   _S({NH2})),
    ("mild_reduction",      _S({KETONE}),       {KETONE: OH},               _S({COOH})),
    ("strong_reduction",    _S({KETONE, COOH}), {KETONE: OH, COOH: OH},     _S({BR})),
    ("amination",           _S({BR}),           {BR: NH2},                  _S({KETONE})),
    ("hydroxylation",       _S({BR}),           {BR: OH},                   _S()),
    ("bromination",         _S({OH, NH2}),      {OH: BR, NH2: BR},          _S()),
    ("reductive_amination", _S({KETONE}),       {KETONE: NH2},              _S({NH2})),
    ("ketone_from_acid",    _S({COOH}),         {COOH: KETONE},             _S({OH, NH2})),
    ("carboxylation",       _S({BR}),           {BR: COOH},                 _S({KETONE})),
    ("hydrogenolysis",      _S({BR}),           {BR: H},                    _S({KETONE})),
    ("defunctionalize",     _S({OH, NH2, COOH}), {OH: H, NH2: H, COOH: H}, _S()),
]
NUM_SELECTIVE = len(SELECTIVE_RXNS)
RXN_RADICAL_BR = NUM_SELECTIVE
RXN_PROTECT = NUM_SELECTIVE + 1
RXN_DEPROTECT = NUM_SELECTIVE + 2
RXN_NAMES = [r[0] for r in SELECTIVE_RXNS] + ["radical_br", "protect", "deprotect"]
OH_NH2_SET = _S({OH, NH2})
BR_SET = _S({BR})


def _select_site(mol: NDArray[np.int8], eligible: FrozenSet[int], n: int) -> int:
    best_idx = -1
    best_react = -1
    for i in range(n):
        g = int(mol[i])
        if g in eligible and REACTIVITY[g] > best_react:
            best_react = REACTIVITY[g]
            best_idx = i
    return best_idx


def _has_any(mol: NDArray[np.int8], groups: FrozenSet[int], n: int) -> bool:
    for i in range(n):
        if int(mol[i]) in groups:
            return True
    return False


def _mol_to_string(mol: NDArray[np.int8]) -> str:
    return "-".join(GROUP_ASCII[g] for g in mol)


_RDK_GREEN = (0.396, 0.471, 0.043, 1.0)
_RDK_RED = (0.800, 0.180, 0.251, 1.0)
_RDK_BG = (0.922, 0.922, 0.922, 1.0)


def _state_to_rdkit_mol(
    mol_array: NDArray[np.int8], chain_len: int,
    goal_array: Optional[NDArray[np.int8]] = None,
) -> Tuple[Any, list, dict]:
    rwmol = Chem.RWMol()
    pos_atoms: Dict[int, list] = {}
    backbone: list = []

    for i in range(chain_len):
        idx = rwmol.AddAtom(Chem.Atom(6))
        backbone.append(idx)
        pos_atoms[i] = [idx]

    for i in range(chain_len - 1):
        rwmol.AddBond(backbone[i], backbone[i + 1], Chem.BondType.SINGLE)

    pg_atoms: list = []

    for i in range(chain_len):
        g = int(mol_array[i])
        c_idx = backbone[i]

        if g == H:
            pass
        elif g == OH:
            o = rwmol.AddAtom(Chem.Atom(8))
            rwmol.AddBond(c_idx, o, Chem.BondType.SINGLE)
            pos_atoms[i].append(o)
        elif g == KETONE:
            o = rwmol.AddAtom(Chem.Atom(8))
            rwmol.AddBond(c_idx, o, Chem.BondType.DOUBLE)
            pos_atoms[i].append(o)
        elif g == NH2:
            n = rwmol.AddAtom(Chem.Atom(7))
            rwmol.AddBond(c_idx, n, Chem.BondType.SINGLE)
            pos_atoms[i].append(n)
        elif g == COOH:
            c2 = rwmol.AddAtom(Chem.Atom(6))
            rwmol.AddBond(c_idx, c2, Chem.BondType.SINGLE)
            o1 = rwmol.AddAtom(Chem.Atom(8))
            rwmol.AddBond(c2, o1, Chem.BondType.DOUBLE)
            o2 = rwmol.AddAtom(Chem.Atom(8))
            rwmol.AddBond(c2, o2, Chem.BondType.SINGLE)
            pos_atoms[i].extend([c2, o1, o2])
        elif g == BR:
            br = rwmol.AddAtom(Chem.Atom(35))
            rwmol.AddBond(c_idx, br, Chem.BondType.SINGLE)
            pos_atoms[i].append(br)
        elif g == OPG:
            o = rwmol.AddAtom(Chem.Atom(8))
            rwmol.AddBond(c_idx, o, Chem.BondType.SINGLE)
            pos_atoms[i].append(o)
            pg_atoms.append(o)
        elif g == NPG:
            n = rwmol.AddAtom(Chem.Atom(7))
            rwmol.AddBond(c_idx, n, Chem.BondType.SINGLE)
            pos_atoms[i].append(n)
            pg_atoms.append(n)

    mol = rwmol.GetMol()
    for atom_idx in pg_atoms:
        mol.GetAtomWithIdx(atom_idx).SetProp("atomNote", "PG")

    AllChem.Compute2DCoords(mol)

    ha: list = []
    hc: dict = {}
    for i in range(chain_len):
        match = goal_array is None or mol_array[i] == goal_array[i]
        color = _RDK_GREEN if match else _RDK_RED
        for atom_idx in pos_atoms[i]:
            ha.append(atom_idx)
            hc[atom_idx] = color

    return mol, ha, hc


def _render_mol_image(
    mol: Any, ha: list, hc: dict, width: int = 1000, height: int = 300,
) -> "PILImage.Image":
    drawer = MolDraw2DCairo(width, height)
    opts = drawer.drawOptions()
    opts.bondLineWidth = 2.5
    opts.setBackgroundColour(_RDK_BG)
    opts.useBWAtomPalette()
    opts.minFontSize = 14
    opts.annotationFontScale = 0.75
    drawer.DrawMolecule(mol, highlightAtoms=ha, highlightAtomColors=hc)
    drawer.FinishDrawing()
    png = drawer.GetDrawingText()
    return PILImage.open(_io.BytesIO(png)).copy()


class RetroState(State):
    __slots__ = ["mol", "_hash"]

    def __init__(self, mol: NDArray[np.int8]):
        self.mol: NDArray[np.int8] = mol
        self._hash: Optional[int] = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.mol.tobytes())
        return self._hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RetroState):
            return np.array_equal(self.mol, other.mol)
        return NotImplemented

    def __repr__(self) -> str:
        return _mol_to_string(self.mol)


class RetroGoal(Goal):
    def __init__(self, mol: NDArray[np.int8]):
        self.mol: NDArray[np.int8] = mol


class RetroAction(Action):
    __slots__ = ["rxn_id", "position", "_hash"]

    def __init__(self, rxn_id: int, position: int = -1):
        self.rxn_id: int = rxn_id
        self.position: int = position
        self._hash: Optional[int] = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash((self.rxn_id, self.position))
        return self._hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, RetroAction):
            return self.rxn_id == other.rxn_id and self.position == other.position
        return NotImplemented

    def __repr__(self) -> str:
        name = RXN_NAMES[self.rxn_id]
        if self.position >= 0:
            return f"{name}@{self.position}"
        return name


@domain_factory.register_class("retro")
class Retrosynthesis(
    ActsEnum[RetroState, RetroAction, RetroGoal],
    GoalStartRevWalkable[RetroState, RetroAction, RetroGoal],
    HasFlatSGIn[RetroState, RetroAction, RetroGoal],
    StateGoalVizable[RetroState, RetroAction, RetroGoal],
    StringToAct[RetroState, RetroAction, RetroGoal],
):

    def __init__(self, chain_len: int = 5):
        super().__init__()
        self.chain_len: int = chain_len
        self._selective_actions = [RetroAction(i) for i in range(NUM_SELECTIVE)]
        self._radical_actions = [
            RetroAction(RXN_RADICAL_BR, pos) for pos in range(chain_len)
        ]
        self._protect_actions = [
            RetroAction(RXN_PROTECT, pos) for pos in range(chain_len)
        ]
        self._deprotect_actions = [
            RetroAction(RXN_DEPROTECT, pos) for pos in range(chain_len)
        ]
        self._fallback_action = RetroAction(5)

    def _actions_for_mol(self, mol: NDArray[np.int8]) -> List[RetroAction]:
        n = self.chain_len
        actions: List[RetroAction] = []

        for rxn_id in range(NUM_SELECTIVE):
            _, eligible, _, forbidden = SELECTIVE_RXNS[rxn_id]
            if forbidden and _has_any(mol, forbidden, n):
                continue
            if _select_site(mol, eligible, n) >= 0:
                actions.append(self._selective_actions[rxn_id])

        if not _has_any(mol, OH_NH2_SET, n):
            for pos in range(n):
                if mol[pos] == H:
                    actions.append(self._radical_actions[pos])

        for pos in range(n):
            if mol[pos] == OH or mol[pos] == NH2:
                actions.append(self._protect_actions[pos])

        if not _has_any(mol, BR_SET, n):
            for pos in range(n):
                if mol[pos] == OPG or mol[pos] == NPG:
                    actions.append(self._deprotect_actions[pos])

        return actions if actions else [self._fallback_action]

    def get_state_actions(
        self, states: List[RetroState]
    ) -> List[List[RetroAction]]:
        return [self._actions_for_mol(state.mol) for state in states]

    def sample_state_action(
        self, states: List[RetroState]
    ) -> List[RetroAction]:
        actions_l = self.get_state_actions(states)
        return [stdlib_random.choice(acts) for acts in actions_l]

    def _apply_action_to_mol(
        self, mol_in: NDArray[np.int8], act: RetroAction
    ) -> NDArray[np.int8]:
        n = self.chain_len
        mol = mol_in.copy()

        if act.rxn_id < NUM_SELECTIVE:
            _, eligible, effects, forbidden = SELECTIVE_RXNS[act.rxn_id]
            if not (forbidden and _has_any(mol, forbidden, n)):
                target = _select_site(mol, eligible, n)
                if target >= 0:
                    mol[target] = effects[int(mol[target])]
        elif act.rxn_id == RXN_RADICAL_BR:
            p = act.position
            if 0 <= p < n and mol[p] == H and not _has_any(mol, OH_NH2_SET, n):
                mol[p] = BR
        elif act.rxn_id == RXN_PROTECT:
            p = act.position
            if 0 <= p < n:
                if mol[p] == OH:
                    mol[p] = OPG
                elif mol[p] == NH2:
                    mol[p] = NPG
        elif act.rxn_id == RXN_DEPROTECT:
            p = act.position
            if 0 <= p < n and not _has_any(mol, BR_SET, n):
                if mol[p] == OPG:
                    mol[p] = OH
                elif mol[p] == NPG:
                    mol[p] = NH2

        return mol

    def next_state(
        self, states: List[RetroState], actions: List[RetroAction]
    ) -> Tuple[List[RetroState], List[float]]:
        new_states: List[RetroState] = []
        for state, act in zip(states, actions):
            new_states.append(RetroState(self._apply_action_to_mol(state.mol, act)))
        return new_states, [1.0] * len(states)

    def is_solved(
        self, states: List[RetroState], goals: List[RetroGoal]
    ) -> List[bool]:
        return [np.array_equal(s.mol, g.mol) for s, g in zip(states, goals)]

    def sample_goalstate_goal_pairs(
        self, num: int
    ) -> Tuple[List[RetroState], List[RetroGoal]]:
        states: List[RetroState] = []
        goals: List[RetroGoal] = []
        for _ in range(num):
            mol = np.random.randint(0, NUM_REAL_GROUPS, size=self.chain_len, dtype=np.int8)
            states.append(RetroState(mol.copy()))
            goals.append(RetroGoal(mol.copy()))
        return states, goals

    def random_walk_rev(
        self, states: List[RetroState], num_steps_l: List[int]
    ) -> List[RetroState]:
        return self.random_walk(states, num_steps_l)[0]

    def _add_reverse_pred(
        self,
        mol: NDArray[np.int8],
        preds: List[NDArray[np.int8]],
        seen: set,
        pos: int,
        pred_group: int,
        action: RetroAction,
    ) -> None:
        pred = mol.copy()
        pred[pos] = np.int8(pred_group)
        pred_key = pred.tobytes()
        if pred_key in seen:
            return
        if action not in self._actions_for_mol(pred):
            return
        if not np.array_equal(self._apply_action_to_mol(pred, action), mol):
            return
        preds.append(pred)
        seen.add(pred_key)

    def _reverse_predecessors(self, mol: NDArray[np.int8]) -> List[NDArray[np.int8]]:
        preds: List[NDArray[np.int8]] = []
        seen = set()

        for pos in range(self.chain_len):
            curr_group = int(mol[pos])

            for rxn_id, (_, _, effects, _) in enumerate(SELECTIVE_RXNS):
                action = self._selective_actions[rxn_id]
                for pred_group, next_group in effects.items():
                    if curr_group == next_group:
                        self._add_reverse_pred(
                            mol, preds, seen, pos, pred_group, action,
                        )

            if curr_group == BR:
                self._add_reverse_pred(
                    mol, preds, seen, pos, H, self._radical_actions[pos],
                )

            if curr_group == OPG:
                self._add_reverse_pred(
                    mol, preds, seen, pos, OH, self._protect_actions[pos],
                )
            elif curr_group == NPG:
                self._add_reverse_pred(
                    mol, preds, seen, pos, NH2, self._protect_actions[pos],
                )

            if curr_group == OH:
                self._add_reverse_pred(
                    mol, preds, seen, pos, OPG, self._deprotect_actions[pos],
                )
            elif curr_group == NH2:
                self._add_reverse_pred(
                    mol, preds, seen, pos, NPG, self._deprotect_actions[pos],
                )

        return preds

    def random_walk(
        self, states: List[RetroState], num_steps_l: List[int]
    ) -> Tuple[List[RetroState], List[float]]:
        if not states:
            return [], []

        mols = np.stack([state.mol for state in states], axis=0).copy()
        steps = np.array(num_steps_l, dtype=np.int32)
        path_costs = np.zeros(len(states), dtype=np.float64)

        for step in range(int(np.max(steps))):
            active_idxs = np.where(steps > step)[0]
            if len(active_idxs) == 0:
                break

            for idx in active_idxs:
                preds = self._reverse_predecessors(mols[idx])
                if preds:
                    pred_idx = int(np.random.randint(len(preds)))
                    mols[idx] = preds[pred_idx]
                    path_costs[idx] += 1.0

        walked = [RetroState(mols[i].copy()) for i in range(len(states))]
        return walked, path_costs.tolist()

    def get_input_info_flat_sg(self) -> Tuple[List[int], List[int]]:
        return (
            [self.chain_len, self.chain_len],
            [NUM_GROUPS, NUM_GROUPS],
        )

    def to_np_flat_sg(
        self, states: List[RetroState], goals: List[RetroGoal]
    ) -> List[NDArray]:
        s = np.stack([st.mol for st in states], axis=0).astype(np.int64)
        g = np.stack([gl.mol for gl in goals], axis=0).astype(np.int64)
        return [s, g]

    def visualize_state_goal(
        self, state: RetroState, goal: RetroGoal, fig: Figure
    ) -> None:
        if _HAS_RDKIT:
            self._visualize_rdkit(state, goal, fig)
        else:
            self._visualize_matplotlib(state, goal, fig)

    def _visualize_rdkit(
        self, state: RetroState, goal: RetroGoal, fig: Figure
    ) -> None:
        cur_mol, cur_ha, cur_hc = _state_to_rdkit_mol(
            state.mol, self.chain_len, goal.mol,
        )
        cur_img = _render_mol_image(cur_mol, cur_ha, cur_hc)

        tgt_mol, tgt_ha, tgt_hc = _state_to_rdkit_mol(
            goal.mol, self.chain_len, goal.mol,
        )
        tgt_img = _render_mol_image(tgt_mol, tgt_ha, tgt_hc)

        ax1 = fig.add_subplot(211)
        ax1.imshow(cur_img)
        ax1.axis("off")
        ax1.set_title(
            "Current Molecule", fontsize=13, fontweight="bold",
            color=BLACK_90, pad=4,
        )
        ax1.text(
            0.5, -0.04, _mol_to_string(state.mol),
            ha="center", va="top", fontsize=10, color=BLACK_50,
            style="italic", transform=ax1.transAxes,
        )

        ax2 = fig.add_subplot(212)
        ax2.imshow(tgt_img)
        ax2.axis("off")
        ax2.set_title(
            "Target Molecule", fontsize=13, fontweight="bold",
            color=BLACK_90, pad=4,
        )
        ax2.text(
            0.5, -0.04, _mol_to_string(goal.mol),
            ha="center", va="top", fontsize=10, color=BLACK_50,
            style="italic", transform=ax2.transAxes,
        )

        solved = np.array_equal(state.mol, goal.mol)
        diff = int(np.sum(state.mol != goal.mol))
        if solved:
            status = "SOLVED"
            scolor = HORSESHOE
        else:
            status = f"{diff} position{'s' if diff != 1 else ''} differ"
            scolor = GARNET
        fig.text(
            0.5, 0.01, status,
            ha="center", va="center", fontsize=11,
            fontweight="bold", color=scolor,
        )
        fig.set_facecolor(BLACK_10)
        fig.subplots_adjust(hspace=0.35, top=0.93, bottom=0.06)

    def _visualize_matplotlib(
        self, state: RetroState, goal: RetroGoal, fig: Figure
    ) -> None:
        ax = fig.add_subplot(111)
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")
        ax.set_facecolor(BLACK_10)

        self._draw_molecule(ax, state.mol, goal.mol, y_center=0.72, label="Current Molecule")
        self._draw_molecule(ax, goal.mol, goal.mol, y_center=0.28, label="Target Molecule")

        solved = np.array_equal(state.mol, goal.mol)
        diff = int(np.sum(state.mol != goal.mol))
        if solved:
            status = "SOLVED"
            color = GRASS
        else:
            status = f"UNSOLVED ({diff} position{'s' if diff != 1 else ''} differ)"
            color = GARNET
        ax.text(
            0.5, 0.03, status,
            ha="center", va="center", fontsize=12, fontweight="bold", color=color,
        )

    def _draw_molecule(
        self, ax, mol: NDArray[np.int8], goal_mol: NDArray[np.int8],
        y_center: float, label: str,
    ) -> None:
        n = self.chain_len
        ax.text(
            0.5, y_center + 0.17, label,
            ha="center", va="center", fontsize=13, fontweight="bold", color=BLACK_90,
        )

        margin = 0.10
        spacing = (1.0 - 2 * margin) / max(n - 1, 1)
        r = 0.028

        for i in range(n - 1):
            x1 = margin + i * spacing + r + 0.005
            x2 = margin + (i + 1) * spacing - r - 0.005
            ax.plot(
                [x1, x2], [y_center, y_center],
                color=BLACK_30, linewidth=2.0, zorder=1, solid_capstyle="butt",
            )

        for i in range(n):
            x = margin + i * spacing
            g = int(mol[i])
            match = mol[i] == goal_mol[i]
            circle_color = HORSESHOE if match else GARNET

            is_protected = g in (OPG, NPG)
            edge_style = dict(
                edgecolor=HONEYCOMB if is_protected else BLACK_90,
                linewidth=2.0 if is_protected else 1.2,
                linestyle="--" if is_protected else "-",
            )

            circle = patches.Circle(
                (x, y_center), r,
                facecolor=circle_color, zorder=3, **edge_style,
            )
            ax.add_patch(circle)
            ax.text(
                x, y_center, "C",
                ha="center", va="center", fontsize=8, fontweight="bold",
                color="white", zorder=4,
            )

            fg_label = GROUP_LABELS[g]
            fg_color = GROUP_COLORS[g]
            if g == H:
                ax.text(
                    x, y_center + 0.055, "H",
                    ha="center", va="center", fontsize=8, color=BLACK_30, zorder=5,
                )
            else:
                ax.text(
                    x, y_center + 0.065, fg_label,
                    ha="center", va="center", fontsize=9, fontweight="bold",
                    color=fg_color,
                    bbox=dict(
                        boxstyle="square,pad=0.15", facecolor="white",
                        edgecolor=fg_color, linewidth=0.8,
                    ),
                    zorder=5,
                )

        ax.text(
            0.5, y_center - 0.10, _mol_to_string(mol),
            ha="center", va="center", fontsize=9, color=BLACK_50, style="italic",
        )

    def string_to_action(self, act_str: str) -> Optional[RetroAction]:
        try:
            s = act_str.strip().lower()
            if "@" in s:
                name, pos_str = s.rsplit("@", 1)
                pos = int(pos_str)
            else:
                parts = s.split()
                if len(parts) == 2:
                    name, pos = parts[0], int(parts[1])
                else:
                    name, pos = s, -1

            for rxn_id, rxn_name in enumerate(RXN_NAMES):
                if rxn_name == name:
                    if rxn_id < NUM_SELECTIVE:
                        return RetroAction(rxn_id)
                    elif 0 <= pos < self.chain_len:
                        return RetroAction(rxn_id, pos)
            return None
        except (ValueError, IndexError):
            return None

    def string_to_action_help(self) -> str:
        sel = ", ".join(RXN_NAMES[:NUM_SELECTIVE])
        pos = ", ".join(RXN_NAMES[NUM_SELECTIVE:])
        return (
            f"Site-selective (no position): {sel}\n"
            f"Position-specific: {pos} (e.g. 'radical_br@2', 'protect 0')"
        )

    def __repr__(self) -> str:
        return f"Retrosynthesis(chain_len={self.chain_len})"


@domain_factory.register_parser("retro")
class RetroParser(Parser):
    def parse(self, args_str: str) -> Dict[str, Any]:
        return {"chain_len": int(args_str)}

    def help(self) -> str:
        return "Chain length. E.g. 'retro.5'"
