"""3D Robotic Arm domain for DeepXube.

A 3D articulated arm with n_joints revolute joints. Each joint angle is
discretized into n_angle_steps values spanning [0, 2pi). The goal is an
end-effector (EE) position discretized into spatial bins.

Forward kinematics couples all joints nonlinearly: every joint angle
affects the EE position. Spherical obstacles block certain configurations,
creating motion-planning dependencies on top of inverse kinematics.

Joints alternate between Z-axis and Y-axis rotation, producing a rich
3D workspace. Each rotation is followed by a fixed-length translation
along the local X-axis.

Actions: (joint_index, +/-1) -- increment or decrement one joint angle
by one discrete step (modular). Actions leading to obstacle collisions
are filtered out.
"""

from typing import List, Tuple, Optional, Dict, Any
import numpy as np
from numpy.typing import NDArray
from matplotlib.figure import Figure
import mpl_toolkits.mplot3d  # noqa: F401

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


class ArmState(State):
    __slots__ = ['joints', '_hash']

    def __init__(self, joints: NDArray[np.int8]):
        self.joints: NDArray[np.int8] = joints
        self._hash: Optional[int] = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.joints.tobytes())
        return self._hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ArmState):
            return np.array_equal(self.joints, other.joints)
        return NotImplemented

    def __repr__(self) -> str:
        return f"Arm[{','.join(str(j) for j in self.joints)}]"


class ArmGoal(Goal):
    def __init__(self, bins: NDArray[np.int8]):
        self.bins: NDArray[np.int8] = bins

    def __repr__(self) -> str:
        return f"Goal[{','.join(str(b) for b in self.bins)}]"


class ArmAction(Action):
    __slots__ = ['joint', 'delta']

    def __init__(self, joint: int, delta: int):
        self.joint: int = joint
        self.delta: int = delta

    def __hash__(self) -> int:
        return hash((self.joint, self.delta))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, ArmAction):
            return self.joint == other.joint and self.delta == other.delta
        return NotImplemented

    def __repr__(self) -> str:
        sign = "+" if self.delta > 0 else "-"
        return f"J{self.joint}{sign}"


def _rotation_z(theta: float) -> NDArray[np.float64]:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [c, -s, 0, 0],
        [s,  c, 0, 0],
        [0,  0, 1, 0],
        [0,  0, 0, 1],
    ])


def _rotation_y(theta: float) -> NDArray[np.float64]:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([
        [ c, 0, s, 0],
        [ 0, 1, 0, 0],
        [-s, 0, c, 0],
        [ 0, 0, 0, 1],
    ])


def _translation_x(d: float) -> NDArray[np.float64]:
    T = np.eye(4)
    T[0, 3] = d
    return T


@domain_factory.register_class("arm")
class RoboticArm(
    ActsEnum[ArmState, ArmAction, ArmGoal],
    GoalStartRevWalkable[ArmState, ArmAction, ArmGoal],
    HasFlatSGIn[ArmState, ArmAction, ArmGoal],
    StateGoalVizable[ArmState, ArmAction, ArmGoal],
    StringToAct[ArmState, ArmAction, ArmGoal],
):

    def __init__(self, n_joints: int = 6, n_angle_steps: int = 12,
                 n_pos_bins: int = 8, link_length: float = 0.5):
        super().__init__()
        self.n_joints = n_joints
        self.n_angle_steps = n_angle_steps
        self.n_pos_bins = n_pos_bins
        self.link_length = link_length
        self.reach = n_joints * link_length

        self.all_actions: List[ArmAction] = []
        for j in range(n_joints):
            self.all_actions.append(ArmAction(j, +1))
            self.all_actions.append(ArmAction(j, -1))

        self.obstacles: List[Tuple[NDArray[np.float64], float]] = [
            (np.array([0.33 * self.reach, 0.17 * self.reach, 0.17 * self.reach]),
             0.10 * self.reach),
            (np.array([-0.17 * self.reach, -0.10 * self.reach, 0.27 * self.reach]),
             0.08 * self.reach),
        ]

        self.ws_min = -self.reach
        self.ws_max = self.reach
        self.bin_width = (self.ws_max - self.ws_min) / n_pos_bins

        self._tx = _translation_x(link_length)
        angles = np.arange(n_angle_steps, dtype=np.float64) * (
            2.0 * np.pi / n_angle_steps
        )
        self._cos = np.cos(angles)
        self._sin = np.sin(angles)
        self._cache_limit = 200_000
        self._fk_cache: Dict[bytes, NDArray[np.float64]] = {}
        self._valid_cache: Dict[bytes, bool] = {}
        self._ee_bins_cache: Dict[bytes, NDArray[np.int8]] = {}

    # ------------------------------------------------------------------ FK

    @staticmethod
    def _state_key(joints: NDArray[np.int8]) -> bytes:
        return joints.tobytes()

    def _trim_cache_if_needed(self, cache: Dict[Any, Any]) -> None:
        if len(cache) >= self._cache_limit:
            cache.clear()

    def _fk(self, joints: NDArray[np.int8]) -> NDArray[np.float64]:
        key = self._state_key(joints)
        cached = self._fk_cache.get(key)
        if cached is not None:
            return cached

        positions = np.zeros((self.n_joints + 1, 3))
        pos = np.zeros(3)
        x_axis = np.array([1.0, 0.0, 0.0])
        y_axis = np.array([0.0, 1.0, 0.0])
        z_axis = np.array([0.0, 0.0, 1.0])

        for i in range(self.n_joints):
            idx = int(joints[i])
            c = self._cos[idx]
            s = self._sin[idx]

            x_old = x_axis
            y_old = y_axis
            z_old = z_axis
            if i % 2 == 0:
                x_axis = c * x_old + s * y_old
                y_axis = -s * x_old + c * y_old
                z_axis = z_old
            else:
                x_axis = c * x_old - s * z_old
                y_axis = y_old
                z_axis = s * x_old + c * z_old

            pos = pos + self.link_length * x_axis
            positions[i + 1] = pos

        self._trim_cache_if_needed(self._fk_cache)
        self._fk_cache[key] = positions
        return positions

    def _ee_position(self, joints: NDArray[np.int8]) -> NDArray[np.float64]:
        return self._fk(joints)[-1]

    # -------------------------------------------------------------- binning

    def _position_to_bins(self, pos: NDArray[np.float64]) -> NDArray[np.int8]:
        raw = np.floor((pos - self.ws_min) / self.bin_width).astype(np.int64)
        return np.clip(raw, 0, self.n_pos_bins - 1).astype(np.int8)

    def _bins_to_position(self, bins: NDArray[np.int8]) -> NDArray[np.float64]:
        return self.ws_min + (bins.astype(np.float64) + 0.5) * self.bin_width

    # ----------------------------------------------------------- collisions

    @staticmethod
    def _seg_sphere(p1: NDArray, p2: NDArray,
                    center: NDArray, radius: float) -> bool:
        d = p2 - p1
        a = float(np.dot(d, d))
        if a < 1e-12:
            diff = p1 - center
            return float(np.dot(diff, diff)) < radius * radius
        t = np.clip(-float(np.dot(p1 - center, d)) / a, 0.0, 1.0)
        closest = p1 + t * d
        diff = closest - center
        return float(np.dot(diff, diff)) < radius * radius

    def _is_collision(self, positions: NDArray[np.float64]) -> bool:
        for center, radius in self.obstacles:
            for i in range(len(positions) - 1):
                if self._seg_sphere(positions[i], positions[i + 1],
                                    center, radius):
                    return True
        return False

    def _is_valid_state(self, joints: NDArray[np.int8]) -> bool:
        key = self._state_key(joints)
        cached = self._valid_cache.get(key)
        if cached is not None:
            return cached

        valid = not self._is_collision(self._fk(joints))
        self._trim_cache_if_needed(self._valid_cache)
        self._valid_cache[key] = valid
        return valid

    def _ee_bins(self, joints: NDArray[np.int8]) -> NDArray[np.int8]:
        key = self._state_key(joints)
        cached = self._ee_bins_cache.get(key)
        if cached is not None:
            return cached

        bins = self._position_to_bins(self._ee_position(joints))
        self._trim_cache_if_needed(self._ee_bins_cache)
        self._ee_bins_cache[key] = bins
        return bins

    # -------------------------------------------------------- action helpers

    def _apply_action(self, joints: NDArray[np.int8],
                      action: ArmAction) -> NDArray[np.int8]:
        nj = joints.copy()
        nj[action.joint] = np.int8(
            (int(joints[action.joint]) + action.delta) % self.n_angle_steps
        )
        return nj

    # ============================================================ ActsEnum

    def get_state_actions(self, states: List[ArmState]) -> List[List[ArmAction]]:
        result: List[List[ArmAction]] = []
        for state in states:
            valid: List[ArmAction] = []
            for act in self.all_actions:
                if self._is_valid_state(self._apply_action(state.joints, act)):
                    valid.append(act)
            result.append(valid if valid else list(self.all_actions))
        return result

    # ============================================================= Domain

    def next_state(self, states: List[ArmState],
                   actions: List[ArmAction]) -> Tuple[List[ArmState], List[float]]:
        return (
            [ArmState(self._apply_action(s.joints, a))
             for s, a in zip(states, actions)],
            [1.0] * len(states),
        )

    def is_solved(self, states: List[ArmState],
                  goals: List[ArmGoal]) -> List[bool]:
        return [
            bool(np.array_equal(self._ee_bins(s.joints), g.bins))
            for s, g in zip(states, goals)
        ]

    # ================================================ GoalStartRevWalkable

    def sample_goalstate_goal_pairs(
        self, num: int,
    ) -> Tuple[List[ArmState], List[ArmGoal]]:
        states: List[ArmState] = []
        goals: List[ArmGoal] = []
        for _ in range(num):
            while True:
                joints = np.random.randint(
                    0, self.n_angle_steps, size=self.n_joints,
                ).astype(np.int8)
                if self._is_valid_state(joints):
                    break
            ee = self._ee_position(joints)
            states.append(ArmState(joints))
            goals.append(ArmGoal(self._position_to_bins(ee)))
        return states, goals

    def random_walk_rev(self, states: List[ArmState],
                        num_steps_l: List[int]) -> List[ArmState]:
        return self.random_walk(states, num_steps_l)[0]

    def random_walk(self, states: List[ArmState],
                    num_steps_l: List[int]) -> Tuple[List[ArmState], List[float]]:
        if not states:
            return [], []

        joints_np = np.stack([s.joints for s in states], axis=0).copy()
        steps = np.array(num_steps_l, dtype=np.int32)
        path_costs = np.zeros(len(states), dtype=np.float64)
        n_actions = len(self.all_actions)

        for step in range(int(np.max(steps))):
            active_idxs = np.where(steps > step)[0]
            if len(active_idxs) == 0:
                break

            for idx in active_idxs:
                current = joints_np[idx]
                moved = False
                for action_idx in np.random.permutation(n_actions):
                    candidate = self._apply_action(
                        current, self.all_actions[int(action_idx)])
                    if self._is_valid_state(candidate):
                        joints_np[idx] = candidate
                        moved = True
                        break
                if moved:
                    path_costs[idx] += 1.0

        walked = [ArmState(joints_np[i].copy()) for i in range(len(states))]
        return walked, path_costs.tolist()

    # ========================================================= HasFlatSGIn

    def get_input_info_flat_sg(self) -> Tuple[List[int], List[int]]:
        return ([self.n_joints, 3], [self.n_angle_steps, self.n_pos_bins])

    def to_np_flat_sg(self, states: List[ArmState],
                      goals: List[ArmGoal]) -> List[NDArray]:
        s = np.stack([st.joints for st in states], axis=0).astype(np.int64)
        g = np.stack([gl.bins for gl in goals], axis=0).astype(np.int64)
        return [s, g]

    # ======================================================= Visualization

    def _draw_arm(self, ax, positions: NDArray, ee_pos: NDArray,
                  target_pos: NDArray, solved: bool,
                  elev: float = 25, azim: float = 45,
                  show_labels: bool = True) -> None:
        ax.set_facecolor("white")

        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2],
                '-', color=GARNET, linewidth=3.5, solid_capstyle='round',
                zorder=5)

        ax.scatter(positions[1:-1, 0], positions[1:-1, 1], positions[1:-1, 2],
                   color=ATLANTIC, s=50, zorder=6, depthshade=False)

        ax.scatter([0], [0], [0], color=BLACK_90, s=80, marker='s',
                   zorder=7, depthshade=False)

        ax.scatter(*ee_pos, color=CONGAREE, s=90, marker='D',
                   zorder=8, depthshade=False)

        ax.scatter(*target_pos, color=HORSESHOE, s=160, marker='*',
                   zorder=9, depthshade=False)

        u = np.linspace(0, 2 * np.pi, 20)
        v = np.linspace(0, np.pi, 15)
        for center, radius in self.obstacles:
            xs = center[0] + radius * np.outer(np.cos(u), np.sin(v))
            ys = center[1] + radius * np.outer(np.sin(u), np.sin(v))
            zs = center[2] + radius * np.outer(np.ones_like(u), np.cos(v))
            ax.plot_surface(xs, ys, zs, color=ROSE, alpha=0.20, linewidth=0)

        lim = self.reach * 0.75
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-lim, lim)
        if show_labels:
            ax.set_xlabel('X', fontsize=8, color=BLACK_70)
            ax.set_ylabel('Y', fontsize=8, color=BLACK_70)
            ax.set_zlabel('Z', fontsize=8, color=BLACK_70)
        ax.tick_params(labelsize=6, colors=BLACK_50)
        ax.view_init(elev=elev, azim=azim)

    def visualize_state_goal(self, state: ArmState, goal: ArmGoal,
                             fig: Figure) -> None:
        fig.set_facecolor(BLACK_10)
        ax = fig.add_subplot(111, projection='3d')
        positions = self._fk(state.joints)
        ee_pos = positions[-1]
        target_pos = self._bins_to_position(goal.bins)
        solved = bool(np.array_equal(
            self._position_to_bins(ee_pos), goal.bins))

        self._draw_arm(ax, positions, ee_pos, target_pos, solved)

        ee_str = f"EE: ({ee_pos[0]:+.2f}, {ee_pos[1]:+.2f}, {ee_pos[2]:+.2f})"
        tgt_str = f"Target: ({target_pos[0]:+.2f}, {target_pos[1]:+.2f}, {target_pos[2]:+.2f})"
        status = "SOLVED" if solved else "unsolved"
        status_color = HORSESHOE if solved else ROSE
        fig.text(0.50, 0.02,
                 f"{ee_str}   {tgt_str}   {status}",
                 ha='center', va='bottom', fontsize=9,
                 color=status_color, fontweight='bold')

    def visualize_multi_view(self, state: ArmState, goal: ArmGoal,
                             fig: Figure) -> None:
        fig.set_facecolor(BLACK_10)
        positions = self._fk(state.joints)
        ee_pos = positions[-1]
        target_pos = self._bins_to_position(goal.bins)
        solved = bool(np.array_equal(
            self._position_to_bins(ee_pos), goal.bins))

        views = [
            (25, 45, "Perspective"),
            (90, -90, "Top (XY)"),
            (0, 0, "Front (XZ)"),
        ]
        for idx, (elev, azim, label) in enumerate(views):
            ax = fig.add_subplot(1, 3, idx + 1, projection='3d')
            self._draw_arm(ax, positions, ee_pos, target_pos, solved,
                           elev=elev, azim=azim, show_labels=True)
            ax.set_title(label, fontsize=9, color=BLACK_90, pad=2)

        ee_str = f"EE: ({ee_pos[0]:+.2f}, {ee_pos[1]:+.2f}, {ee_pos[2]:+.2f})"
        tgt_str = f"Target: ({target_pos[0]:+.2f}, {target_pos[1]:+.2f}, {target_pos[2]:+.2f})"
        status = "SOLVED" if solved else "unsolved"
        status_color = HORSESHOE if solved else ROSE
        fig.text(0.50, 0.02,
                 f"{ee_str}   {tgt_str}   {status}",
                 ha='center', va='bottom', fontsize=10,
                 color=status_color, fontweight='bold')

    # ========================================================== StringToAct

    def string_to_action(self, act_str: str) -> Optional[ArmAction]:
        try:
            s = act_str.strip().upper()
            if s.startswith('J'):
                s = s[1:]
            if s.endswith('+'):
                return ArmAction(int(s[:-1]), 1)
            if s.endswith('-'):
                return ArmAction(int(s[:-1]), -1)
            parts = s.split()
            joint, delta = int(parts[0]), int(parts[1])
            if 0 <= joint < self.n_joints and delta in (-1, 1):
                return ArmAction(joint, delta)
            return None
        except (ValueError, IndexError):
            return None

    def string_to_action_help(self) -> str:
        return f"'J<n><+/->' or '<joint> <delta>' (joints 0..{self.n_joints - 1})"

    def __repr__(self) -> str:
        return (f"RoboticArm(n_joints={self.n_joints}, "
                f"steps={self.n_angle_steps}, bins={self.n_pos_bins})")


@domain_factory.register_parser("arm")
class ArmParser(Parser):
    def parse(self, args_str: str) -> Dict[str, Any]:
        parts = args_str.split("_")
        if len(parts) != 3:
            raise ValueError(
                f"Expected 'n_joints_n_angle_steps_n_pos_bins', got '{args_str}'"
            )
        return {
            "n_joints": int(parts[0]),
            "n_angle_steps": int(parts[1]),
            "n_pos_bins": int(parts[2]),
        }

    def help(self) -> str:
        return "n_joints_n_angle_steps_n_pos_bins. E.g. 'arm.6_12_8'"
