"""Warehouse Multi-Agent Path Finding (MAPF) domain for DeepXube.

K robots on an H x W grid warehouse floor must simultaneously navigate
to assigned shelf positions while avoiding other shelves and each other.
Goal cells are ON shelf obstacles; only the assigned robot may enter its
own goal shelf cell. All other shelf cells are impassable.

All robots move at each timestep; valid directions are UP, DOWN, LEFT,
RIGHT, WAIT. Joint actions are rejected on vertex conflicts (two robots
target the same cell) or edge conflicts (two robots swap positions).

The optimization objective is makespan: total timesteps until all
robots reach their goals (uniform cost 1.0 per transition).
"""

from typing import List, Tuple, Optional, Dict, Any, Set
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

_BRAND_COLORS = [GARNET, ATLANTIC, CONGAREE, HORSESHOE, ROSE,
                 HONEYCOMB, WARM_GREY, GRASS, BLACK_70, BLACK_50]


def _generate_robot_colors(k: int) -> List[str]:
    if k <= len(_BRAND_COLORS):
        return _BRAND_COLORS[:k]
    import colorsys
    colors = list(_BRAND_COLORS)
    for i in range(len(_BRAND_COLORS), k):
        hue = (i * 0.618033988749895) % 1.0
        r, g, b = colorsys.hsv_to_rgb(hue, 0.75, 0.70)
        colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
    return colors

UP, DOWN, LEFT, RIGHT, WAIT = 0, 1, 2, 3, 4
DIR_OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)]
DIR_NAMES = ["UP", "DOWN", "LEFT", "RIGHT", "WAIT"]

# -- Warehouse layouts --------------------------------------------------------

def _warehouse_8x8() -> NDArray[np.bool_]:
    obs = np.zeros((8, 8), dtype=np.bool_)
    for r in [1, 2, 4, 5]:
        for c in [1, 2, 4, 5]:
            obs[r, c] = True
    return obs


def _warehouse_20x20() -> NDArray[np.bool_]:
    obs = np.zeros((20, 20), dtype=np.bool_)
    shelf_rows = [2, 3, 4, 6, 7, 8, 11, 12, 13, 15, 16, 17]
    shelf_cols = [2, 3, 5, 6, 8, 9, 11, 12, 14, 15]
    for r in shelf_rows:
        for c in shelf_cols:
            obs[r, c] = True
    return obs


def _warehouse_28x28() -> NDArray[np.bool_]:
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
    __slots__ = ['positions', 'goal_positions', '_hash']

    def __init__(self, positions: NDArray[np.int8],
                 goal_positions: Optional[NDArray[np.int8]] = None):
        self.positions: NDArray[np.int8] = positions
        self.goal_positions: Optional[NDArray[np.int8]] = goal_positions
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

    def __init__(self, height: int = 20, width: int = 20, n_robots: int = 8,
                 max_joint_actions: int = 256,
                 exact_joint_action_limit: int = 5000):
        super().__init__()
        self.H = height
        self.W = width
        self.K = n_robots
        self.max_joint_actions = max(1, max_joint_actions)
        self.exact_joint_action_limit = max(1, exact_joint_action_limit)

        layout_fn = WAREHOUSE_LAYOUTS.get((height, width))
        if layout_fn is not None:
            self.obstacles: NDArray[np.bool_] = layout_fn()
        else:
            self.obstacles = np.zeros((height, width), dtype=np.bool_)

        self.free_cells: List[Tuple[int, int]] = []
        self.shelf_cells: List[Tuple[int, int]] = []
        for r in range(height):
            for c in range(width):
                if self.obstacles[r, c]:
                    self.shelf_cells.append((r, c))
                else:
                    self.free_cells.append((r, c))
        self.n_free = len(self.free_cells)
        self.n_obs = len(self.shelf_cells)
        self.robot_colors = _generate_robot_colors(n_robots)

        self._goal_cells: Dict[Tuple[int, int], int] = {}

    # ----------------------------------------------------------- state helpers

    def _get_pos(self, state: MAPFState, i: int) -> Tuple[int, int]:
        return int(state.positions[2 * i]), int(state.positions[2 * i + 1])

    def _get_goal_pos(self, goal: MAPFGoal, i: int) -> Tuple[int, int]:
        return int(goal.positions[2 * i]), int(goal.positions[2 * i + 1])

    def _set_pos(self, arr: NDArray[np.int8], i: int, r: int, c: int) -> None:
        arr[2 * i] = np.int8(r)
        arr[2 * i + 1] = np.int8(c)

    def _goal_cells_from_positions(
        self, positions: NDArray[np.int8]
    ) -> Dict[Tuple[int, int], int]:
        return {
            (int(positions[2 * i]), int(positions[2 * i + 1])): i
            for i in range(self.K)
        }

    def _goal_cells_from_goal(self, goal: MAPFGoal) -> Dict[Tuple[int, int], int]:
        return self._goal_cells_from_positions(goal.positions)

    def _goal_cells_from_state(
        self, state: MAPFState
    ) -> Dict[Tuple[int, int], int]:
        if state.goal_positions is None:
            return self._goal_cells
        return self._goal_cells_from_positions(state.goal_positions)

    def set_active_goal(self, goal: MAPFGoal) -> None:
        self._goal_cells = self._goal_cells_from_goal(goal)

    # --------------------------------------------------------- move validation

    def _target_cell(self, r: int, c: int, d: int) -> Tuple[int, int]:
        dr, dc = DIR_OFFSETS[d]
        return r + dr, c + dc

    def _in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.H and 0 <= c < self.W

    def _is_passable(self, r: int, c: int, robot_idx: int,
                     goal_cells: Optional[Dict[Tuple[int, int], int]] = None) -> bool:
        if not self._in_bounds(r, c):
            return False
        if not self.obstacles[r, c]:
            return True
        cells = self._goal_cells if goal_cells is None else goal_cells
        return cells.get((r, c)) == robot_idx

    def _compute_targets(self, state: MAPFState,
                         dirs: tuple,
                         goal_cells: Optional[Dict[Tuple[int, int], int]] = None
                         ) -> Optional[List[Tuple[int, int]]]:
        targets = []
        current_flat: List[int] = []
        target_flat: List[int] = []
        for i in range(self.K):
            r, c = self._get_pos(state, i)
            tr, tc = self._target_cell(r, c, dirs[i])
            if not self._is_passable(tr, tc, i, goal_cells):
                tr, tc = r, c
            targets.append((tr, tc))
            current_flat.append(r * self.W + c)
            target_flat.append(tr * self.W + tc)

        if len(set(target_flat)) != self.K:
            return None

        current_to_robot = {
            cell: idx for idx, cell in enumerate(current_flat)
        }
        for i, target_cell in enumerate(target_flat):
            other = current_to_robot.get(target_cell)
            if other is not None and other != i:
                if target_flat[other] == current_flat[i]:
                    return None
        return targets

    def _per_robot_dirs(
        self, state: MAPFState, goal_cells: Dict[Tuple[int, int], int]
    ) -> List[List[int]]:
        per_robot_dirs: List[List[int]] = []
        for i in range(self.K):
            r, c = self._get_pos(state, i)
            valid = []
            for d in range(5):
                tr, tc = self._target_cell(r, c, d)
                if self._is_passable(tr, tc, i, goal_cells) or d == WAIT:
                    valid.append(d)
            if WAIT not in valid:
                valid.append(WAIT)
            per_robot_dirs.append(valid)
        return per_robot_dirs

    def _sample_joint_action(
        self, state: MAPFState,
        goal_cells: Dict[Tuple[int, int], int],
        per_robot_dirs: List[List[int]],
        max_retries: int = 200,
    ) -> MAPFAction:
        for _ in range(max_retries):
            dirs = tuple(
                dirs_i[np.random.randint(len(dirs_i))]
                for dirs_i in per_robot_dirs
            )
            if self._compute_targets(state, dirs, goal_cells) is not None:
                return MAPFAction(dirs)
        return MAPFAction(tuple([WAIT] * self.K))

    def _goal_pos_for_robot(
        self,
        state: MAPFState,
        goal_cells: Dict[Tuple[int, int], int],
        robot_idx: int,
    ) -> Tuple[int, int]:
        if state.goal_positions is not None:
            return (
                int(state.goal_positions[2 * robot_idx]),
                int(state.goal_positions[2 * robot_idx + 1]),
            )
        for (r, c), idx in goal_cells.items():
            if idx == robot_idx:
                return r, c
        raise KeyError(f"missing goal position for robot {robot_idx}")

    def _ordered_dirs_to_goal(
        self,
        state: MAPFState,
        goal_cells: Dict[Tuple[int, int], int],
        per_robot_dirs: List[List[int]],
    ) -> List[List[int]]:
        ordered_dirs: List[List[int]] = []
        for i, valid_dirs in enumerate(per_robot_dirs):
            r, c = self._get_pos(state, i)
            gr, gc = self._goal_pos_for_robot(state, goal_cells, i)
            scored = []
            for d in valid_dirs:
                tr, tc = self._target_cell(r, c, d)
                dist = abs(tr - gr) + abs(tc - gc)
                wait_pen = 0.25 if d == WAIT and dist > 0 else 0.0
                stay_pen = 0.05 if d == WAIT else 0.0
                scored.append((dist, wait_pen, stay_pen, d))
            scored.sort(key=lambda item: item[:3])
            ordered_dirs.append([item[3] for item in scored])
        return ordered_dirs

    def _try_greedy_joint_action(
        self,
        state: MAPFState,
        goal_cells: Dict[Tuple[int, int], int],
        ordered_dirs: List[List[int]],
        robot_order: List[int],
        alt_shift: int = 0,
    ) -> Optional[MAPFAction]:
        assigned_dirs = [WAIT] * self.K
        current_flat = [0] * self.K
        for i in range(self.K):
            r, c = self._get_pos(state, i)
            current_flat[i] = r * self.W + c

        target_by_robot: Dict[int, int] = {}
        target_cells: Set[int] = set()

        for order_pos, i in enumerate(robot_order):
            dirs = ordered_dirs[i]
            if len(dirs) > 1:
                shift_span = min(3, len(dirs))
                shift = (alt_shift + order_pos) % shift_span
                dirs_try = dirs[shift:shift_span] + dirs[:shift] + dirs[shift_span:]
            else:
                dirs_try = dirs

            chosen_dir: Optional[int] = None
            chosen_target: Optional[int] = None
            for d in dirs_try:
                r, c = self._get_pos(state, i)
                tr, tc = self._target_cell(r, c, d)
                target_flat = tr * self.W + tc
                if target_flat in target_cells:
                    continue

                swap_conflict = False
                for j, other_target in target_by_robot.items():
                    if other_target == current_flat[i] and target_flat == current_flat[j]:
                        swap_conflict = True
                        break
                if swap_conflict:
                    continue

                chosen_dir = d
                chosen_target = target_flat
                break

            if chosen_dir is None or chosen_target is None:
                return None

            assigned_dirs[i] = chosen_dir
            target_by_robot[i] = chosen_target
            target_cells.add(chosen_target)

        dirs_tuple = tuple(assigned_dirs)
        if self._compute_targets(state, dirs_tuple, goal_cells) is None:
            return None
        return MAPFAction(dirs_tuple)

    def _guided_joint_actions(
        self,
        state: MAPFState,
        goal_cells: Dict[Tuple[int, int], int],
        per_robot_dirs: List[List[int]],
    ) -> List[MAPFAction]:
        ordered_dirs = self._ordered_dirs_to_goal(state, goal_cells, per_robot_dirs)
        dists = []
        for i in range(self.K):
            r, c = self._get_pos(state, i)
            gr, gc = self._goal_pos_for_robot(state, goal_cells, i)
            dists.append(abs(r - gr) + abs(c - gc))

        unsolved = [i for i, dist in enumerate(dists) if dist > 0]
        solved = [i for i, dist in enumerate(dists) if dist == 0]

        orders: List[List[int]] = []
        seen_orders: Set[tuple[int, ...]] = set()

        def add_order(order: List[int]) -> None:
            order_t = tuple(order)
            if order_t in seen_orders:
                return
            seen_orders.add(order_t)
            orders.append(order)

        add_order(unsolved + solved)
        add_order(sorted(range(self.K), key=lambda idx: (-dists[idx], idx)))
        add_order(sorted(range(self.K), key=lambda idx: (dists[idx], idx)))
        add_order(list(range(self.K)))
        add_order(list(reversed(range(self.K))))

        if unsolved:
            for _ in range(min(8, len(unsolved))):
                perm = unsolved.copy()
                np.random.shuffle(perm)
                add_order(perm + solved)

        actions: List[MAPFAction] = [MAPFAction(tuple([WAIT] * self.K))]
        seen_dirs: Set[tuple] = {actions[0].dirs}
        guided_cap = min(self.max_joint_actions, 32)

        for order in orders:
            for alt_shift in range(3):
                action = self._try_greedy_joint_action(
                    state, goal_cells, ordered_dirs, order, alt_shift=alt_shift)
                if action is None or action.dirs in seen_dirs:
                    continue
                actions.append(action)
                seen_dirs.add(action.dirs)
                if len(actions) >= guided_cap:
                    return actions

        return actions

    def _get_actions_for_state(self, state: MAPFState) -> List[MAPFAction]:
        goal_cells = self._goal_cells_from_state(state)
        per_robot_dirs = self._per_robot_dirs(state, goal_cells)
        num_joint = 1
        for dirs in per_robot_dirs:
            num_joint *= len(dirs)
            if num_joint > self.exact_joint_action_limit:
                break

        if num_joint <= self.exact_joint_action_limit:
            actions: List[MAPFAction] = []
            for combo in itertools.product(*per_robot_dirs):
                if self._compute_targets(state, combo, goal_cells) is not None:
                    actions.append(MAPFAction(combo))
            return actions or [MAPFAction(tuple([WAIT] * self.K))]

        actions = self._guided_joint_actions(state, goal_cells, per_robot_dirs)
        seen: Set[tuple] = {action.dirs for action in actions}
        attempts = 0
        max_attempts = max(self.max_joint_actions * 50, 1000)
        while len(actions) < self.max_joint_actions and attempts < max_attempts:
            attempts += 1
            action = self._sample_joint_action(
                state, goal_cells, per_robot_dirs, max_retries=1)
            if action.dirs in seen:
                continue
            actions.append(action)
            seen.add(action.dirs)
        return actions

    # ============================================================== ActsEnum

    def get_state_actions(self, states: List[MAPFState]) -> List[List[MAPFAction]]:
        return [self._get_actions_for_state(state) for state in states]

    # ============================================================== Domain

    def next_state(self, states: List[MAPFState],
                   actions: List[MAPFAction]) -> Tuple[List[MAPFState], List[float]]:
        new_states: List[MAPFState] = []
        for state, action in zip(states, actions):
            goal_cells = self._goal_cells_from_state(state)
            targets = self._compute_targets(state, action.dirs, goal_cells)
            if targets is None:
                new_states.append(state)
                continue
            new_pos = state.positions.copy()
            for i, (tr, tc) in enumerate(targets):
                self._set_pos(new_pos, i, tr, tc)
            goal_pos = None if state.goal_positions is None else state.goal_positions.copy()
            new_states.append(MAPFState(new_pos, goal_pos))
        return new_states, [1.0] * len(states)

    def is_solved(self, states: List[MAPFState],
                  goals: List[MAPFGoal]) -> List[bool]:
        result: List[bool] = []
        for state, goal in zip(states, goals):
            if state.goal_positions is None:
                state.goal_positions = goal.positions.copy()
            result.append(bool(np.array_equal(state.positions, goal.positions)))
        return result

    # ================================================ GoalStartRevWalkable

    def sample_goalstate_goal_pairs(
        self, num: int,
    ) -> Tuple[List[MAPFState], List[MAPFGoal]]:
        states: List[MAPFState] = []
        goals: List[MAPFGoal] = []
        if self.K > len(self.shelf_cells):
            raise ValueError(
                f"Cannot sample {self.K} MAPF goals from "
                f"{len(self.shelf_cells)} shelf cells")
        for _ in range(num):
            shelf_idxs = np.random.choice(
                len(self.shelf_cells), size=self.K, replace=False)
            pos = np.zeros(2 * self.K, dtype=np.int8)
            for i, idx in enumerate(shelf_idxs):
                r, c = self.shelf_cells[idx]
                self._set_pos(pos, i, r, c)
            goal_pos = pos.copy()
            states.append(MAPFState(pos, goal_pos.copy()))
            goals.append(MAPFGoal(goal_pos))
        return states, goals

    def _sample_random_action(self, state: MAPFState,
                              max_retries: int = 200) -> MAPFAction:
        goal_cells = self._goal_cells_from_state(state)
        return self._sample_joint_action(
            state, goal_cells, self._per_robot_dirs(state, goal_cells),
            max_retries=max_retries)

    _DR = np.array([-1, 1, 0, 0, 0], dtype=np.int16)
    _DC = np.array([0, 0, -1, 1, 0], dtype=np.int16)

    def random_walk(self, states: List[MAPFState],
                    num_steps_l: List[int]) -> Tuple[List[MAPFState], List[float]]:
        N = len(states)
        if N == 0:
            return [], []
        K = self.K
        H, W = self.H, self.W
        max_steps = max(num_steps_l)
        steps_arr = np.array(num_steps_l, dtype=np.int32)

        all_pos = np.stack(
            [s.positions for s in states], axis=0).astype(np.int16)
        goal_positions = [
            s.positions.copy() if s.goal_positions is None else s.goal_positions.copy()
            for s in states
        ]

        goal_rows = all_pos[:, 0::2].copy()
        goal_cols = all_pos[:, 1::2].copy()

        free_mask = ~self.obstacles

        for step in range(max_steps):
            active = steps_arr > step
            aidx = np.where(active)[0]
            B = len(aidx)
            if B == 0:
                break

            bp = all_pos[aidx]
            rows = bp[:, 0::2]
            cols = bp[:, 1::2]
            g_r = goal_rows[aidx]
            g_c = goal_cols[aidx]

            valid = np.ones((B, K, 5), dtype=np.bool_)
            for d in range(4):
                tr = rows + self._DR[d]
                tc = cols + self._DC[d]
                ib = (tr >= 0) & (tr < H) & (tc >= 0) & (tc < W)
                tr_c = np.clip(tr, 0, H - 1)
                tc_c = np.clip(tc, 0, W - 1)
                passable = ib & free_mask[tr_c, tc_c]
                is_obs = ib & ~free_mask[tr_c, tc_c]
                if np.any(is_obs):
                    passable |= is_obs & (tr_c == g_r) & (tc_c == g_c)
                valid[:, :, d] = passable

            resolved = np.zeros(B, dtype=np.bool_)
            new_r = rows.copy()
            new_c = cols.copy()
            _triu = np.triu(np.ones((K, K), dtype=np.bool_), k=1)

            for _retry in range(8):
                todo_idx = np.where(~resolved)[0]
                if len(todo_idx) == 0:
                    break

                Bt = len(todo_idx)
                v = valid[todo_idx]
                r_t = rows[todo_idx]
                c_t = cols[todo_idx]

                rand = np.random.random((Bt, K, 5))
                rand[~v] = -1.0
                dirs = np.argmax(rand, axis=2).astype(np.int16)

                tr = r_t + self._DR[dirs]
                tc = c_t + self._DC[dirs]

                tf = tr * W + tc
                cf = r_t * W + c_t

                sorted_tf = np.sort(tf, axis=1)
                has_vertex = np.any(
                    sorted_tf[:, 1:] == sorted_tf[:, :-1], axis=1)

                swap_fwd = tf[:, :, None] == cf[:, None, :]
                swap_rev = tf[:, None, :] == cf[:, :, None]
                moved = (dirs != WAIT)
                moved_pair = moved[:, :, None] & moved[:, None, :]
                has_swap = np.any(
                    swap_fwd & swap_rev & moved_pair & _triu[None], axis=(1, 2))

                ok = ~has_vertex & ~has_swap
                ok_orig = todo_idx[ok]
                new_r[ok_orig] = tr[ok]
                new_c[ok_orig] = tc[ok]
                resolved[ok_orig] = True

            new_bp = bp.copy()
            new_bp[:, 0::2] = new_r.astype(np.int16)
            new_bp[:, 1::2] = new_c.astype(np.int16)
            all_pos[aidx] = new_bp

        result = [
            MAPFState(all_pos[i].astype(np.int8), goal_positions[i])
            for i in range(N)
        ]
        return result, [float(s) for s in num_steps_l]

    def random_walk_rev(self, states: List[MAPFState],
                        num_steps_l: List[int]) -> List[MAPFState]:
        return self.random_walk(states, num_steps_l)[0]

    # ========================================================= HasFlatSGIn

    def get_input_info_flat_sg(self) -> Tuple[List[int], List[int]]:
        n_cells = self.H * self.W
        return [self.K, self.K], [n_cells, n_cells]

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
                             fig: Figure, frozen: Optional[List[bool]] = None) -> None:
        from matplotlib.colors import to_rgba
        CELL = 64
        img_w = self.W * CELL
        img_h = self.H * CELL
        robot_r = min(24, CELL // 3)
        label_size = max(7, min(14, 28 - self.K // 3))
        goal_inset = max(2, CELL // 16)
        goal_lw = max(1.5, min(3, 4 - self.K / 20))

        goal_set: Dict[Tuple[int, int], int] = {}
        for i in range(self.K):
            gr, gc = self._get_goal_pos(goal, i)
            goal_set[(gr, gc)] = i

        fig.set_facecolor("white")
        ax = fig.add_axes([0.03, 0.05, 0.94, 0.92])
        ax.set_xlim(0, img_w)
        ax.set_ylim(img_h, 0)
        ax.set_aspect('equal')
        ax.axis('off')

        for r in range(self.H):
            for c in range(self.W):
                x, y = c * CELL, r * CELL
                if (r, c) in goal_set:
                    rid = goal_set[(r, c)]
                    color = self.robot_colors[rid]
                    fill = to_rgba(color, alpha=0.30)
                    ax.add_patch(mpatches.Rectangle(
                        (x, y), CELL, CELL,
                        facecolor=fill, edgecolor=color,
                        linewidth=goal_lw, zorder=1))
                elif self.obstacles[r, c]:
                    ax.add_patch(mpatches.Rectangle(
                        (x, y), CELL, CELL,
                        facecolor='black', edgecolor='black', linewidth=1))
                else:
                    ax.add_patch(mpatches.Rectangle(
                        (x, y), CELL, CELL,
                        facecolor='white', edgecolor=BLACK_30, linewidth=0.5))

        for i in range(self.K):
            sr, sc = self._get_pos(state, i)
            cx, cy = sc * CELL + CELL / 2, sr * CELL + CELL / 2
            color = self.robot_colors[i]
            is_frozen = frozen[i] if frozen else False
            edge = "black"
            edge_w = 1.5 if not is_frozen else 2.5
            ax.add_patch(mpatches.Circle(
                (cx, cy), robot_r,
                facecolor=color, edgecolor=edge, linewidth=edge_w,
                zorder=10))

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
                f"free={self.n_free}, shelves={self.n_obs}, "
                f"max_joint_actions={self.max_joint_actions})")


@domain_factory.register_parser("mapf")
class MAPFParser(Parser):
    def parse(self, args_str: str) -> Dict[str, Any]:
        parts = args_str.split("_")
        if len(parts) == 1:
            return {"n_robots": int(parts[0])}
        if len(parts) in (3, 4):
            kwargs: Dict[str, Any] = {
                "height": int(parts[0]),
                "width": int(parts[1]),
                "n_robots": int(parts[2]),
            }
            if len(parts) == 4:
                kwargs["max_joint_actions"] = int(parts[3])
            return kwargs
        raise ValueError(
            f"Expected 'n_robots' or 'height_width_n_robots[_max_joint_actions]', got '{args_str}'"
        )

    def help(self) -> str:
        return ("n_robots or height_width_n_robots[_max_joint_actions]. "
                "E.g. 'mapf.4', 'mapf.8_8_4', or 'mapf.28_28_30_128'")
