"""Warehouse Multi-Agent Path Finding (MAPF) domain for DeepXube.

K robots on an H x W grid warehouse floor must simultaneously navigate
to assigned goal positions while avoiding static shelf obstacles and
each other. All robots move at each timestep; valid directions are
UP, DOWN, LEFT, RIGHT, WAIT. Joint actions are rejected on vertex
conflicts (two robots target the same cell) or edge conflicts (two
robots swap positions). Boundary/obstacle violations clamp individual
robots in place.

The optimization objective is makespan: total timesteps until all
robots reach their goals (uniform cost 1.0 per transition).
"""

from typing import List, Tuple, Optional, Dict, Any
import itertools
import numpy as np
from numpy.typing import NDArray
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from deepxube.base.factory import Parser
from deepxube.base.domain import (
    State, Action, Goal,
    ActsEnum, GoalStartRevWalkable,
    StateGoalVizable, StringToAct,
)
from deepxube.base.nnet_input import HasFlatSGIn
from deepxube.factories.domain_factory import domain_factory

GARNET = "#73000A"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
ROSE = "#CC2E40"
HONEYCOMB = "#A49137"
BLACK_90 = "#363636"
BLACK_70 = "#5C5C5C"
BLACK_50 = "#A2A2A2"
BLACK_30 = "#C7C7C7"
BLACK_10 = "#ECECEC"

WARM_GREY = "#676156"
GRASS = "#CED318"

ROBOT_COLORS = [GARNET, ATLANTIC, CONGAREE, HORSESHOE, ROSE,
                HONEYCOMB, WARM_GREY, GRASS, BLACK_70, BLACK_50]

UP, DOWN, LEFT, RIGHT, WAIT = 0, 1, 2, 3, 4
DIR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
DIR_NAMES = ["UP", "DOWN", "LEFT", "RIGHT", "WAIT"]

# -- Warehouse layouts --------------------------------------------------------

def _warehouse_8x8() -> NDArray[np.bool_]:
    """8x8 debug warehouse: 2 shelf blocks, 16 obstacles, 48 free."""
    obs = np.zeros((8, 8), dtype=np.bool_)
    for r in [1, 2, 4, 5]:
        for c in [1, 2, 4, 5]:
            obs[r, c] = True
    return obs


def _warehouse_20x20() -> NDArray[np.bool_]:
    """20x20 Amazon-style fulfillment center.

    Dense parallel shelf aisles with cross-aisles every 3 rows.
    Perimeter staging lanes on all sides. ~30% obstacle density.

        cols:  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19
    row  0:    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    row  1:    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    row  2:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row  3:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row  4:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row  5:    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    row  6:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row  7:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row  8:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row  9:    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    row 10:    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    row 11:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row 12:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row 13:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row 14:    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    row 15:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row 16:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row 17:    .  .  #  #  .  #  #  .  #  #  .  #  #  .  #  #  .  .  .  .
    row 18:    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    row 19:    .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .  .
    """
    obs = np.zeros((20, 20), dtype=np.bool_)
    shelf_rows = [2, 3, 4, 6, 7, 8, 11, 12, 13, 15, 16, 17]
    shelf_cols = [2, 3, 5, 6, 8, 9, 11, 12, 14, 15]
    for r in shelf_rows:
        for c in shelf_cols:
            obs[r, c] = True
    return obs


def _warehouse_28x28() -> NDArray[np.bool_]:
    """28x28 large fulfillment center. 6 shelf blocks, ~30% density."""
    obs = np.zeros((28, 28), dtype=np.bool_)
    shelf_cols = [2, 3, 5, 6, 8, 9, 11, 12, 14, 15, 17, 18, 20, 21, 23, 24]
    shelf_rows = [2, 3, 4, 6, 7, 8, 10, 11, 12,
                  15, 16, 17, 19, 20, 21, 23, 24, 25]
    for r in shelf_rows:
        for c in shelf_cols:
            obs[r, c] = True
    return obs


WAREHOUSE_LAYOUTS = {
    (8, 8): _warehouse_8x8,
    (20, 20): _warehouse_20x20,
    (28, 28): _warehouse_28x28,
}


class MAPFState(State):
    __slots__ = ['positions', '_hash']

    def __init__(self, positions: NDArray[np.int8]):
        self.positions: NDArray[np.int8] = positions
        self._hash: Optional[int] = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.positions.tobytes())
        return self._hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MAPFState):
            return np.array_equal(self.positions, other.positions)
        return NotImplemented

    def __repr__(self) -> str:
        pairs = [f"({self.positions[2*i]},{self.positions[2*i+1]})"
                 for i in range(len(self.positions) // 2)]
        return f"MAPF[{' '.join(pairs)}]"


class MAPFGoal(Goal):
    def __init__(self, positions: NDArray[np.int8]):
        self.positions: NDArray[np.int8] = positions

    def __repr__(self) -> str:
        pairs = [f"({self.positions[2*i]},{self.positions[2*i+1]})"
                 for i in range(len(self.positions) // 2)]
        return f"Goal[{' '.join(pairs)}]"


class MAPFAction(Action):
    __slots__ = ['dirs', '_hash']

    def __init__(self, dirs: tuple):
        self.dirs: tuple = dirs
        self._hash: Optional[int] = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.dirs)
        return self._hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, MAPFAction):
            return self.dirs == other.dirs
        return NotImplemented

    def __repr__(self) -> str:
        return "(" + ",".join(DIR_NAMES[d] for d in self.dirs) + ")"


@domain_factory.register_class("mapf")
class WarehouseMAPF(
    ActsEnum[MAPFState, MAPFAction, MAPFGoal],
    GoalStartRevWalkable[MAPFState, MAPFAction, MAPFGoal],
    HasFlatSGIn[MAPFState, MAPFAction, MAPFGoal],
    StateGoalVizable[MAPFState, MAPFAction, MAPFGoal],
    StringToAct[MAPFState, MAPFAction, MAPFGoal],
):

    def __init__(self, height: int = 20, width: int = 20, n_robots: int = 8):
        super().__init__()
        self.H = height
        self.W = width
        self.K = n_robots
        assert self.K <= 10

        layout_fn = WAREHOUSE_LAYOUTS.get((height, width))
        if layout_fn is not None:
            self.obstacles: NDArray[np.bool_] = layout_fn()
        else:
            self.obstacles = np.zeros((height, width), dtype=np.bool_)

        self.free_cells: List[Tuple[int, int]] = []
        for r in range(height):
            for c in range(width):
                if not self.obstacles[r, c]:
                    self.free_cells.append((r, c))
        self.n_free = len(self.free_cells)
        self.n_obs = int(self.obstacles.sum())

    # ----------------------------------------------------------- state helpers

    def _get_pos(self, state: MAPFState, i: int) -> Tuple[int, int]:
        return int(state.positions[2 * i]), int(state.positions[2 * i + 1])

    def _get_goal_pos(self, goal: MAPFGoal, i: int) -> Tuple[int, int]:
        return int(goal.positions[2 * i]), int(goal.positions[2 * i + 1])

    def _set_pos(self, arr: NDArray[np.int8], i: int, r: int, c: int) -> None:
        arr[2 * i] = np.int8(r)
        arr[2 * i + 1] = np.int8(c)

    # --------------------------------------------------------- move validation

    def _target_cell(self, r: int, c: int, d: int) -> Tuple[int, int]:
        dr, dc = DIR_OFFSETS[d]
        return r + dr, c + dc

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.H and 0 <= c < self.W

    def _is_free(self, r: int, c: int) -> bool:
        return self._in_bounds(r, c) and not self.obstacles[r, c]

    def _compute_targets(self, state: MAPFState,
                         dirs: tuple) -> Optional[List[Tuple[int, int]]]:
        targets = []
        for i in range(self.K):
            r, c = self._get_pos(state, i)
            tr, tc = self._target_cell(r, c, dirs[i])
            if not self._is_free(tr, tc):
                tr, tc = r, c
            targets.append((tr, tc))

        for i in range(self.K):
            for j in range(i + 1, self.K):
                if targets[i] == targets[j]:
                    return None
                ri, ci = self._get_pos(state, i)
                rj, cj = self._get_pos(state, j)
                if targets[i] == (rj, cj) and targets[j] == (ri, ci):
                    return None
        return targets

    # ============================================================== ActsEnum

    def get_state_actions(self, states: List[MAPFState]) -> List[List[MAPFAction]]:
        result: List[List[MAPFAction]] = []
        for state in states:
            per_robot_dirs: List[List[int]] = []
            for i in range(self.K):
                r, c = self._get_pos(state, i)
                valid = []
                for d in range(5):
                    tr, tc = self._target_cell(r, c, d)
                    if self._is_free(tr, tc) or d == WAIT:
                        valid.append(d)
                if WAIT not in valid:
                    valid.append(WAIT)
                per_robot_dirs.append(valid)

            valid_actions: List[MAPFAction] = []
            for combo in itertools.product(*per_robot_dirs):
                if self._compute_targets(state, combo) is not None:
                    valid_actions.append(MAPFAction(combo))

            if not valid_actions:
                valid_actions.append(MAPFAction(tuple([WAIT] * self.K)))
            result.append(valid_actions)
        return result

    # ============================================================== Domain

    def next_state(self, states: List[MAPFState],
                   actions: List[MAPFAction]) -> Tuple[List[MAPFState], List[float]]:
        new_states: List[MAPFState] = []
        for state, action in zip(states, actions):
            targets = self._compute_targets(state, action.dirs)
            if targets is None:
                new_states.append(state)
                continue
            new_pos = state.positions.copy()
            for i, (tr, tc) in enumerate(targets):
                self._set_pos(new_pos, i, tr, tc)
            new_states.append(MAPFState(new_pos))
        return new_states, [1.0] * len(states)

    def is_solved(self, states: List[MAPFState],
                  goals: List[MAPFGoal]) -> List[bool]:
        return [
            bool(np.array_equal(s.positions, g.positions))
            for s, g in zip(states, goals)
        ]

    # ================================================ GoalStartRevWalkable

    def sample_goalstate_goal_pairs(
        self, num: int,
    ) -> Tuple[List[MAPFState], List[MAPFGoal]]:
        states: List[MAPFState] = []
        goals: List[MAPFGoal] = []
        for _ in range(num):
            idxs = np.random.choice(self.n_free, size=self.K, replace=False)
            pos = np.zeros(2 * self.K, dtype=np.int8)
            for i, idx in enumerate(idxs):
                r, c = self.free_cells[idx]
                self._set_pos(pos, i, r, c)
            states.append(MAPFState(pos))
            goals.append(MAPFGoal(pos.copy()))
        return states, goals

    def _sample_random_action(self, state: MAPFState,
                              max_retries: int = 200) -> MAPFAction:
        per_robot: List[List[int]] = []
        for i in range(self.K):
            r, c = self._get_pos(state, i)
            valid = []
            for d in range(5):
                tr, tc = self._target_cell(r, c, d)
                if self._is_free(tr, tc) or d == WAIT:
                    valid.append(d)
            if not valid:
                valid = [WAIT]
            per_robot.append(valid)

        for _ in range(max_retries):
            dirs = tuple(
                per_robot[i][np.random.randint(len(per_robot[i]))]
                for i in range(self.K)
            )
            if self._compute_targets(state, dirs) is not None:
                return MAPFAction(dirs)
        return MAPFAction(tuple([WAIT] * self.K))

    def random_walk(self, states: List[MAPFState],
                    num_steps_l: List[int]) -> Tuple[List[MAPFState], List[List[MAPFAction]]]:
        result_states: List[MAPFState] = []
        result_actions: List[List[MAPFAction]] = []
        for state, n_steps in zip(states, num_steps_l):
            cur = state
            actions: List[MAPFAction] = []
            for _ in range(n_steps):
                act = self._sample_random_action(cur)
                nxt, _ = self.next_state([cur], [act])
                cur = nxt[0]
                actions.append(act)
            result_states.append(cur)
            result_actions.append(actions)
        return result_states, result_actions

    def random_walk_rev(self, states: List[MAPFState],
                        num_steps_l: List[int]) -> List[MAPFState]:
        return self.random_walk(states, num_steps_l)[0]

    # ========================================================= HasFlatSGIn

    def get_input_info_flat_sg(self) -> Tuple[List[int], List[int]]:
        n_cells = self.H * self.W
        return ([self.K], [n_cells]), ([self.K], [n_cells])

    def to_np_flat_sg(self, states: List[MAPFState],
                      goals: List[MAPFGoal]) -> List[NDArray]:
        s_flat = np.zeros((len(states), self.K), dtype=np.int64)
        g_flat = np.zeros((len(goals), self.K), dtype=np.int64)
        for b, (state, goal) in enumerate(zip(states, goals)):
            for i in range(self.K):
                sr, sc = self._get_pos(state, i)
                s_flat[b, i] = sr * self.W + sc
                gr, gc = self._get_goal_pos(goal, i)
                g_flat[b, i] = gr * self.W + gc
        return [s_flat, g_flat]

    # ======================================================= Visualization

    def visualize_state_goal(self, state: MAPFState, goal: MAPFGoal,
                             fig: Figure) -> None:
        CELL = 64
        img_w = self.W * CELL
        img_h = self.H * CELL

        fig.set_facecolor(BLACK_10)
        ax = fig.add_axes([0.05, 0.05, 0.9, 0.88])
        ax.set_xlim(0, img_w)
        ax.set_ylim(img_h, 0)
        ax.set_aspect('equal')
        ax.axis('off')

        for r in range(self.H):
            for c in range(self.W):
                x, y = c * CELL, r * CELL
                if self.obstacles[r, c]:
                    ax.add_patch(mpatches.Rectangle(
                        (x, y), CELL, CELL,
                        facecolor='black', edgecolor=BLACK_90, linewidth=1))
                else:
                    ax.add_patch(mpatches.Rectangle(
                        (x, y), CELL, CELL,
                        facecolor=BLACK_10, edgecolor=BLACK_30, linewidth=0.5))

        for i in range(self.K):
            gr, gc = self._get_goal_pos(goal, i)
            gx, gy = gc * CELL, gr * CELL
            color = ROBOT_COLORS[i]
            from matplotlib.colors import to_rgba
            fill = to_rgba(color, alpha=0.15)
            ax.add_patch(mpatches.Rectangle(
                (gx + 4, gy + 4), CELL - 8, CELL - 8,
                facecolor=fill, edgecolor=color, linewidth=3,
                linestyle='-', fill=True))

        for i in range(self.K):
            sr, sc = self._get_pos(state, i)
            cx, cy = sc * CELL + CELL / 2, sr * CELL + CELL / 2
            color = ROBOT_COLORS[i]
            ax.add_patch(mpatches.Circle(
                (cx, cy), 24,
                facecolor=color, edgecolor='white', linewidth=1.5,
                zorder=10))
            ax.text(cx, cy, str(i + 1),
                    ha='center', va='center',
                    fontsize=14, fontweight='bold', color='white',
                    zorder=11)

        solved = bool(np.array_equal(state.positions, goal.positions))
        status = "SOLVED" if solved else "unsolved"
        status_color = HORSESHOE if solved else ROSE
        fig.text(0.5, 0.01, status,
                 ha='center', va='bottom', fontsize=11,
                 color=status_color, fontweight='bold')

    # ========================================================== StringToAct

    def string_to_action(self, act_str: str) -> Optional[MAPFAction]:
        try:
            parts = act_str.strip().upper().split()
            if len(parts) != self.K:
                parts = act_str.strip().upper().split(",")
            if len(parts) != self.K:
                return None
            name_map = {"U": UP, "UP": UP, "D": DOWN, "DOWN": DOWN,
                        "L": LEFT, "LEFT": LEFT, "R": RIGHT, "RIGHT": RIGHT,
                        "W": WAIT, "WAIT": WAIT}
            dirs = []
            for p in parts:
                p = p.strip()
                if p not in name_map:
                    return None
                dirs.append(name_map[p])
            return MAPFAction(tuple(dirs))
        except (ValueError, IndexError):
            return None

    def string_to_action_help(self) -> str:
        return (f"'{self.K}' directions separated by spaces or commas. "
                f"Each: U/D/L/R/W (up/down/left/right/wait)")

    def __repr__(self) -> str:
        return (f"WarehouseMAPF(H={self.H}, W={self.W}, K={self.K}, "
                f"free={self.n_free}, obs={self.n_obs})")


@domain_factory.register_parser("mapf")
class MAPFParser(Parser):
    def parse(self, args_str: str) -> Dict[str, Any]:
        parts = args_str.split("_")
        if len(parts) == 1:
            return {"n_robots": int(parts[0])}
        if len(parts) == 3:
            return {
                "height": int(parts[0]),
                "width": int(parts[1]),
                "n_robots": int(parts[2]),
            }
        raise ValueError(
            f"Expected 'n_robots' or 'height_width_n_robots', got '{args_str}'"
        )

    def help(self) -> str:
        return "n_robots or height_width_n_robots. E.g. 'mapf.4' or 'mapf.8_8_4'"
