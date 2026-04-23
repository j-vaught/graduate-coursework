"""Four-bar linkage mechanism design domain for DeepXube.

A planar four-bar linkage defined by six parameters: four link lengths
(a, b, c, d), one coupler extension length p, and one coupler extension
angle beta. The goal is to match a target coupler curve encoded as
discretized waypoints.

Forward kinematics couples all parameters nonlinearly: changing any single
parameter reshapes the entire coupler curve, making the problem
non-decomposable.

Actions: (param_idx, +/-1) -- increment or decrement one of the six
discretized parameters by one step. 12 total fixed actions.
"""

from typing import List, Tuple, Optional, Dict, Any
import numpy as np
from numpy.typing import NDArray
from matplotlib.figure import Figure

from deepxube.base.factory import Parser
from deepxube.base.domain import (
    State, Action, Goal,
    ActsEnumFixed, GoalStartRevWalkableActsRev,
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
BLACK_30 = "#C7C7C7"
BLACK_10 = "#ECECEC"

PARAM_NAMES = ["a", "b", "c", "d", "p", "beta"]
LINK_COLORS = [GARNET, ATLANTIC, HORSESHOE, CONGAREE]

N_PARAMS = 6


class LinkState(State):
    __slots__ = ['params', '_hash']

    def __init__(self, params: NDArray[np.int8]):
        self.params: NDArray[np.int8] = params
        self._hash: Optional[int] = None

    def __hash__(self) -> int:
        if self._hash is None:
            self._hash = hash(self.params.tobytes())
        return self._hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LinkState):
            return np.array_equal(self.params, other.params)
        return NotImplemented

    def __repr__(self) -> str:
        return f"Link[{','.join(str(p) for p in self.params)}]"


class LinkGoal(Goal):
    __slots__ = ['curve']

    def __init__(self, curve: NDArray[np.int8]):
        self.curve: NDArray[np.int8] = curve

    def __repr__(self) -> str:
        n_valid = np.sum(self.curve[::2] >= 0)
        return f"Goal[{n_valid} waypts]"


class LinkAction(Action):
    __slots__ = ['param', 'delta']

    def __init__(self, param: int, delta: int):
        self.param: int = param
        self.delta: int = delta

    def __hash__(self) -> int:
        return hash((self.param, self.delta))

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LinkAction):
            return self.param == other.param and self.delta == other.delta
        return NotImplemented

    def __repr__(self) -> str:
        sign = "+" if self.delta > 0 else "-"
        return f"{PARAM_NAMES[self.param]}{sign}"


PARAM_RANGES = [
    (0.5, 5.0),   # a: crank
    (0.5, 5.0),   # b: coupler
    (0.5, 5.0),   # c: follower
    (0.5, 5.0),   # d: ground
    (0.0, 3.0),   # p: coupler extension length
    (0.0, 2 * np.pi),  # beta: coupler extension angle
]

SENTINEL = np.int8(-1)


@domain_factory.register_class("linkage")
class FourBarLinkage(
    ActsEnumFixed[LinkState, LinkAction, LinkGoal],
    GoalStartRevWalkableActsRev[LinkState, LinkAction, LinkGoal],
    HasFlatSGIn[LinkState, LinkAction, LinkGoal],
    StateGoalVizable[LinkState, LinkAction, LinkGoal],
    StringToAct[LinkState, LinkAction, LinkGoal],
):

    def __init__(self, n_steps: int = 64, n_waypoints: int = 64,
                 n_bins: int = 64, ws_range: float = 8.0):
        super().__init__()
        self.n_steps = n_steps
        self.n_waypoints = n_waypoints
        self.n_bins = n_bins
        self.ws_min = -ws_range
        self.ws_max = ws_range
        self.bin_width = (self.ws_max - self.ws_min) / n_bins

        self.deltas = np.array(
            [(hi - lo) / n_steps for lo, hi in PARAM_RANGES])
        self.mins = np.array([lo for lo, _ in PARAM_RANGES])

        self.theta_samples = np.linspace(
            0, 2 * np.pi, n_waypoints, endpoint=False)

        self.all_actions: List[LinkAction] = []
        for p in range(N_PARAMS):
            self.all_actions.append(LinkAction(p, +1))
            self.all_actions.append(LinkAction(p, -1))

    def __repr__(self) -> str:
        return (f"FourBarLinkage(n_steps={self.n_steps}, "
                f"n_waypoints={self.n_waypoints}, n_bins={self.n_bins})")

    # -------------------------------------------------------- parameter conversion

    def _idx_to_continuous(self, params: NDArray[np.int8]) -> NDArray[np.float64]:
        return self.mins + (params.astype(np.float64) + 0.5) * self.deltas

    def _position_to_bin(self, x: float, y: float) -> Tuple[int, int]:
        bx = int(np.floor((x - self.ws_min) / self.bin_width))
        by = int(np.floor((y - self.ws_min) / self.bin_width))
        bx = max(0, min(self.n_bins - 1, bx))
        by = max(0, min(self.n_bins - 1, by))
        return bx, by

    # -------------------------------------------------------- forward kinematics

    def _coupler_curve(self, params: NDArray[np.int8]) -> NDArray[np.float64]:
        vals = self._idx_to_continuous(params)
        a, b, c, d, p, beta = vals

        curve = np.full((self.n_waypoints, 2), np.nan)

        cos_theta = np.cos(self.theta_samples)
        sin_theta = np.sin(self.theta_samples)

        ax_pts = a * cos_theta
        ay_pts = a * sin_theta

        f2 = a * a + d * d - 2 * a * d * cos_theta
        f = np.sqrt(np.maximum(f2, 1e-12))

        cos_gamma = (c * c + f2 - b * b) / (2 * c * f)

        valid = np.abs(cos_gamma) <= 1.0
        if not np.any(valid):
            return curve

        gamma = np.arccos(np.clip(cos_gamma[valid], -1, 1))
        alpha1 = np.arctan2(ay_pts[valid], ax_pts[valid] - d)

        phi = alpha1 + gamma

        bx = d + c * np.cos(phi)
        by = c * np.sin(phi)

        ab_angle = np.arctan2(by - ay_pts[valid], bx - ax_pts[valid])
        px = ax_pts[valid] + p * np.cos(ab_angle + beta)
        py = ay_pts[valid] + p * np.sin(ab_angle + beta)

        curve[valid, 0] = px
        curve[valid, 1] = py

        return curve

    def _curve_to_bins(self, curve: NDArray[np.float64]) -> NDArray[np.int8]:
        bins = np.full(self.n_waypoints * 2, SENTINEL, dtype=np.int8)
        for i in range(self.n_waypoints):
            if np.isnan(curve[i, 0]):
                continue
            bx, by = self._position_to_bin(curve[i, 0], curve[i, 1])
            bins[2 * i] = np.int8(bx)
            bins[2 * i + 1] = np.int8(by)
        return bins

    def _state_to_curve_bins(self, state: LinkState) -> NDArray[np.int8]:
        return self._curve_to_bins(self._coupler_curve(state.params))

    # ============================================================ ActsEnumFixed

    def get_actions_fixed(self) -> List[LinkAction]:
        return self.all_actions.copy()

    def expand(self, states: List[LinkState]
               ) -> Tuple[List[List[LinkState]], List[List[LinkAction]],
                           List[List[float]]]:
        n = len(states)
        states_exp: List[List[LinkState]] = [[] for _ in range(n)]
        actions_exp: List[List[LinkAction]] = [[] for _ in range(n)]
        costs_exp: List[List[float]] = [[] for _ in range(n)]

        for idx, state in enumerate(states):
            for act in self.all_actions:
                new_params = state.params.copy()
                val = int(new_params[act.param]) + act.delta
                if act.param == 5:  # beta wraps
                    val = val % self.n_steps
                else:
                    val = max(0, min(self.n_steps - 1, val))
                new_params[act.param] = np.int8(val)
                states_exp[idx].append(LinkState(new_params))
                actions_exp[idx].append(act)
                costs_exp[idx].append(1.0)

        return states_exp, actions_exp, costs_exp

    def rev_action(self, states: List[LinkState],
                   actions: List[LinkAction]) -> List[LinkAction]:
        return [LinkAction(a.param, -a.delta) for a in actions]

    # ============================================================= Domain

    def next_state(self, states: List[LinkState],
                   actions: List[LinkAction]
                   ) -> Tuple[List[LinkState], List[float]]:
        result: List[LinkState] = []
        for state, act in zip(states, actions):
            new_params = state.params.copy()
            val = int(new_params[act.param]) + act.delta
            if act.param == 5:
                val = val % self.n_steps
            else:
                val = max(0, min(self.n_steps - 1, val))
            new_params[act.param] = np.int8(val)
            result.append(LinkState(new_params))
        return result, [1.0] * len(states)

    def is_solved(self, states: List[LinkState],
                  goals: List[LinkGoal]) -> List[bool]:
        solved: List[bool] = []
        for state, goal in zip(states, goals):
            curve_bins = self._state_to_curve_bins(state)
            match = True
            for i in range(self.n_waypoints):
                gx, gy = goal.curve[2 * i], goal.curve[2 * i + 1]
                if gx == SENTINEL:
                    continue
                if curve_bins[2 * i] != gx or curve_bins[2 * i + 1] != gy:
                    match = False
                    break
            solved.append(match)
        return solved

    # ================================================ GoalStartRevWalkableActsRev

    def sample_goalstate_goal_pairs(
        self, num: int,
    ) -> Tuple[List[LinkState], List[LinkGoal]]:
        states: List[LinkState] = []
        goals: List[LinkGoal] = []
        for _ in range(num):
            params = np.random.randint(
                0, self.n_steps, size=N_PARAMS).astype(np.int8)
            curve_bins = self._curve_to_bins(self._coupler_curve(params))
            states.append(LinkState(params))
            goals.append(LinkGoal(curve_bins))
        return states, goals

    # ========================================================= HasFlatSGIn

    def get_input_info_flat_sg(self) -> Tuple[List[int], List[int]]:
        return (
            [N_PARAMS, self.n_waypoints * 2],
            [self.n_steps, self.n_bins],
        )

    def to_np_flat_sg(self, states: List[LinkState],
                      goals: List[LinkGoal]) -> List[NDArray]:
        s = np.stack([st.params for st in states], axis=0).astype(np.int64)
        g = np.stack([gl.curve for gl in goals], axis=0).astype(np.int64)
        g = np.clip(g, 0, self.n_bins - 1)
        return [s, g]

    # ======================================================= StringToAct

    def string_to_action_help(self) -> str:
        return "'<param><+/->' (a,b,c,d,p,beta) or '<idx> <delta>'"

    def string_to_action(self, act_str: str) -> Optional[LinkAction]:
        act_str = act_str.strip()
        for p_idx, name in enumerate(PARAM_NAMES):
            if act_str.startswith(name):
                rest = act_str[len(name):]
                if rest == "+":
                    return LinkAction(p_idx, +1)
                elif rest == "-":
                    return LinkAction(p_idx, -1)
        parts = act_str.split()
        if len(parts) == 2:
            try:
                p_idx = int(parts[0])
                delta = int(parts[1])
                if 0 <= p_idx < N_PARAMS and delta in (-1, +1):
                    return LinkAction(p_idx, delta)
            except ValueError:
                pass
        return None

    # ======================================================= Visualization

    def _compute_mechanism_positions(self, params: NDArray[np.int8],
                                     theta: float
                                     ) -> Optional[Dict[str, Tuple[float, float]]]:
        vals = self._idx_to_continuous(params)
        a, b, c, d, p, beta = vals

        ax_pt = a * np.cos(theta)
        ay_pt = a * np.sin(theta)

        f2 = a * a + d * d - 2 * a * d * np.cos(theta)
        f = np.sqrt(max(f2, 1e-12))

        cos_gamma = (c * c + f2 - b * b) / (2 * c * f)
        if abs(cos_gamma) > 1.0:
            return None

        gamma = np.arccos(np.clip(cos_gamma, -1, 1))
        alpha1 = np.arctan2(ay_pt, ax_pt - d)
        phi = alpha1 + gamma

        bx = d + c * np.cos(phi)
        by = c * np.sin(phi)

        ab_angle = np.arctan2(by - ay_pt, bx - ax_pt)
        px = ax_pt + p * np.cos(ab_angle + beta)
        py = ay_pt + p * np.sin(ab_angle + beta)

        return {
            'O1': (0.0, 0.0),
            'O2': (d, 0.0),
            'A': (ax_pt, ay_pt),
            'B': (bx, by),
            'P': (px, py),
        }

    def visualize_state_goal(self, state: LinkState, goal: LinkGoal,
                             fig: Figure) -> None:
        state_curve = self._coupler_curve(state.params)
        state_bins = self._curve_to_bins(state_curve)

        n_match = 0
        n_total = 0
        for i in range(self.n_waypoints):
            if goal.curve[2 * i] == SENTINEL:
                continue
            n_total += 1
            if (state_bins[2 * i] == goal.curve[2 * i] and
                    state_bins[2 * i + 1] == goal.curve[2 * i + 1]):
                n_match += 1

        solved = (n_match == n_total) and n_total > 0

        fig.set_facecolor(BLACK_10)

        ax_mech = fig.add_axes([0.02, 0.10, 0.46, 0.82])
        ax_curve = fig.add_axes([0.52, 0.10, 0.46, 0.82])

        vals = self._idx_to_continuous(state.params)
        d_val = vals[3]

        theta_mid = self.theta_samples[0]
        pts = self._compute_mechanism_positions(state.params, theta_mid)

        mech_range = max(6.0, d_val + 3.0)
        cx = d_val / 2.0
        ax_mech.set_xlim(cx - mech_range, cx + mech_range)
        ax_mech.set_ylim(-mech_range, mech_range)
        ax_mech.set_aspect('equal')
        ax_mech.set_facecolor('white')
        for spine in ax_mech.spines.values():
            spine.set_color(BLACK_30)
        ax_mech.tick_params(colors=BLACK_90, labelsize=7)
        ax_mech.set_title("Mechanism", fontsize=10, color=BLACK_90, pad=8)

        trail_x = state_curve[~np.isnan(state_curve[:, 0]), 0]
        trail_y = state_curve[~np.isnan(state_curve[:, 1]), 1]
        if len(trail_x) > 1:
            trail_x_closed = np.append(trail_x, trail_x[0])
            trail_y_closed = np.append(trail_y, trail_y[0])
            ax_mech.plot(trail_x_closed, trail_y_closed, '-',
                         color=ATLANTIC, alpha=0.35, linewidth=1.2, zorder=2)

        if pts is not None:
            o1, o2, a_pt, b_pt, p_pt = (
                pts['O1'], pts['O2'], pts['A'], pts['B'], pts['P'])

            ax_mech.plot([o1[0], a_pt[0]], [o1[1], a_pt[1]],
                         '-', color=GARNET, linewidth=3, zorder=4)
            ax_mech.plot([a_pt[0], b_pt[0]], [a_pt[1], b_pt[1]],
                         '-', color=ATLANTIC, linewidth=3, zorder=4)
            ax_mech.plot([o2[0], b_pt[0]], [o2[1], b_pt[1]],
                         '-', color=HORSESHOE, linewidth=3, zorder=4)
            ax_mech.plot([o1[0], o2[0]], [o1[1], o2[1]],
                         '-', color=CONGAREE, linewidth=4, zorder=3)

            for jx, jy in [o1, o2, a_pt, b_pt]:
                ax_mech.plot(jx, jy, 'o', color=BLACK_90,
                             markersize=5, zorder=6)

            ax_mech.plot(p_pt[0], p_pt[1], 'D', color=ATLANTIC,
                         markersize=7, zorder=7)

            ax_mech.plot([a_pt[0], p_pt[0]], [a_pt[1], p_pt[1]],
                         '--', color=ATLANTIC, alpha=0.5, linewidth=1, zorder=4)

        goal_curve_x = []
        goal_curve_y = []
        for i in range(self.n_waypoints):
            gx, gy = goal.curve[2 * i], goal.curve[2 * i + 1]
            if gx == SENTINEL:
                continue
            wx = self.ws_min + (float(gx) + 0.5) * self.bin_width
            wy = self.ws_min + (float(gy) + 0.5) * self.bin_width
            goal_curve_x.append(wx)
            goal_curve_y.append(wy)

        ws = self.ws_max
        ax_curve.set_xlim(-ws, ws)
        ax_curve.set_ylim(-ws, ws)
        ax_curve.set_aspect('equal')
        ax_curve.set_facecolor('white')
        for spine in ax_curve.spines.values():
            spine.set_color(BLACK_30)
        ax_curve.tick_params(colors=BLACK_90, labelsize=7)
        ax_curve.set_title("Curve Comparison", fontsize=10,
                           color=BLACK_90, pad=8)

        if goal_curve_x:
            gx_closed = goal_curve_x + [goal_curve_x[0]]
            gy_closed = goal_curve_y + [goal_curve_y[0]]
            ax_curve.plot(gx_closed, gy_closed, '--',
                          color=ROSE, linewidth=2.5, zorder=3,
                          label="Target")

        valid_state = ~np.isnan(state_curve[:, 0])
        if np.any(valid_state):
            sx = state_curve[valid_state, 0]
            sy = state_curve[valid_state, 1]
            sx_c = np.append(sx, sx[0])
            sy_c = np.append(sy, sy[0])
            ax_curve.plot(sx_c, sy_c, '-', color=ATLANTIC,
                          linewidth=1.8, zorder=4, label="Current")

        for i in range(self.n_waypoints):
            gx_val, gy_val = goal.curve[2 * i], goal.curve[2 * i + 1]
            if gx_val == SENTINEL:
                continue
            wx = self.ws_min + (float(gx_val) + 0.5) * self.bin_width
            wy = self.ws_min + (float(gy_val) + 0.5) * self.bin_width
            if (state_bins[2 * i] == gx_val and
                    state_bins[2 * i + 1] == gy_val):
                ax_curve.plot(wx, wy, 'o', color=HORSESHOE,
                              markersize=3, zorder=5)
            else:
                ax_curve.plot(wx, wy, 'x', color=ROSE,
                              markersize=3, zorder=5)

        ax_curve.legend(loc='upper right', fontsize=7,
                        framealpha=0.8, edgecolor=BLACK_30)

        status_color = HORSESHOE if solved else ROSE
        status_text = f"{n_match}/{n_total} waypoints matched"
        if solved:
            status_text += "  [SOLVED]"
        fig.text(0.5, 0.03, status_text, ha="center", va="bottom",
                 fontsize=11, color=status_color, fontweight="bold")


@domain_factory.register_parser("linkage")
class LinkageParser(Parser):
    def help(self) -> str:
        return "n_steps[_n_waypoints[_n_bins]]. E.g. 'linkage.64' or 'linkage.64_64_64'"

    def parse(self, args_str: str) -> Dict[str, Any]:
        kwargs: Dict[str, Any] = {}
        if args_str:
            parts = args_str.split("_")
            if len(parts) >= 1:
                kwargs["n_steps"] = int(parts[0])
            if len(parts) >= 2:
                kwargs["n_waypoints"] = int(parts[1])
            if len(parts) >= 3:
                kwargs["n_bins"] = int(parts[2])
        return kwargs
