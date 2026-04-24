from typing import List, Tuple, Optional, Dict, Any

from deepxube.base.factory import Parser
from deepxube.base.domain import State, Action, Goal, ActsEnumFixed, GoalStartRevWalkableActsRev, GoalFixed, StateGoalVizable, StringToAct
from deepxube.factories.domain_factory import domain_factory
from deepxube.base.nnet_input import HasFlatSGIn
import numpy as np
import matplotlib.patches as patches
from matplotlib.figure import Figure

from numpy.typing import NDArray


class PancakeState(State):
    __slots__ = ['perm', 'hash']

    def __init__(self, perm: NDArray[np.uint8]):
        self.perm: NDArray[np.uint8] = perm
        self.hash: Optional[int] = None

    def __hash__(self) -> int:
        if self.hash is None:
            self.hash = hash(self.perm.tobytes())
        return self.hash

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PancakeState):
            return np.array_equal(self.perm, other.perm)
        return NotImplemented


class PancakeGoal(Goal):
    def __init__(self, perm: NDArray[np.uint8]):
        self.perm: NDArray[np.uint8] = perm


class PancakeAction(Action):
    def __init__(self, flip_idx: int):
        self.flip_idx = flip_idx

    def __hash__(self) -> int:
        return self.flip_idx

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PancakeAction):
            return self.flip_idx == other.flip_idx
        return NotImplemented

    def __repr__(self) -> str:
        return f"flip top {self.flip_idx + 1}"


@domain_factory.register_class("pancake")
class Pancake(ActsEnumFixed[PancakeState, PancakeAction, PancakeGoal],
              GoalStartRevWalkableActsRev[PancakeState, PancakeAction, PancakeGoal],
              GoalFixed[PancakeState, PancakeAction, PancakeGoal],
              HasFlatSGIn[PancakeState, PancakeAction, PancakeGoal],
              StateGoalVizable[PancakeState, PancakeAction, PancakeGoal],
              StringToAct[PancakeState, PancakeAction, PancakeGoal]):

    def __init__(self, num_pancakes: int = 8):
        super().__init__()
        self.num_pancakes: int = num_pancakes

        # Actions: flip top k for k in 2..num_pancakes (flip_idx = k-1, so 1..num_pancakes-1)
        self.actions_fixed: List[PancakeAction] = [PancakeAction(i) for i in range(1, num_pancakes)]

        # Goal: sorted order [0, 1, 2, ..., N-1]
        self.goal_perm: NDArray[np.uint8] = np.arange(num_pancakes, dtype=np.uint8)

    def sample_goalstate_goal_pairs(self, num: int) -> Tuple[List[PancakeState], List[PancakeGoal]]:
        states = [PancakeState(self.goal_perm.copy()) for _ in range(num)]
        goals = [PancakeGoal(self.goal_perm.copy()) for _ in range(num)]
        return states, goals

    def get_goal(self) -> PancakeGoal:
        return PancakeGoal(self.goal_perm.copy())

    def get_actions_fixed(self) -> List[PancakeAction]:
        return self.actions_fixed.copy()

    def rev_action(self, states: List[PancakeState], actions: List[PancakeAction]) -> List[PancakeAction]:
        return list(actions)

    def next_state(self, states: List[PancakeState], actions: List[PancakeAction]) -> Tuple[List[PancakeState], List[float]]:
        states_np = np.stack([s.perm for s in states], axis=0).copy()

        for action in set(actions):
            k = action.flip_idx + 1  # flip top k elements (indices 0..k-1)
            act_idxs = np.array([i for i, a in enumerate(actions) if a == action])
            states_np[np.ix_(act_idxs, range(k))] = states_np[np.ix_(act_idxs, range(k))][:, ::-1]

        return [PancakeState(states_np[i]) for i in range(len(states))], [1.0] * len(states)

    def is_solved(self, states: List[PancakeState], goals: List[PancakeGoal]) -> List[bool]:
        states_np = np.stack([s.perm for s in states], axis=0)
        goals_np = np.stack([g.perm for g in goals], axis=0)
        return list(np.all(states_np == goals_np, axis=1))

    def get_input_info_flat_sg(self) -> Tuple[List[int], List[int]]:
        return [self.num_pancakes], [self.num_pancakes]

    def to_np_flat_sg(self, states: List[PancakeState], goals: List[PancakeGoal]) -> List[NDArray]:
        return [np.stack([s.perm for s in states], axis=0).astype(np.uint8)]

    def visualize_state_goal(self, state: PancakeState, goal: PancakeGoal, fig: Figure) -> None:
        ax = fig.add_subplot(111)

        n = self.num_pancakes
        pancake_h = min(0.08, 0.80 / n)
        gap = 0.01
        base_y = 0.08
        max_w = 0.70
        cx = 0.5

        cmap = __import__('matplotlib').colormaps['tab10']

        # draw pancakes bottom-up: index 0 = top of stack, index N-1 = bottom
        for i in range(n):
            val = int(state.perm[i])
            # position: index 0 at top, index N-1 at bottom
            y = base_y + (n - 1 - i) * (pancake_h + gap)
            w = max_w * (val + 1) / n
            color = cmap(val % 10)
            in_place = (state.perm[i] == goal.perm[i])

            ax.add_patch(patches.Rectangle(
                (cx - w / 2, y), w, pancake_h,
                facecolor=color, edgecolor='limegreen' if in_place else 'k',
                linewidth=2.0 if in_place else 0.8,
            ))
            ax.text(cx, y + pancake_h / 2, str(val),
                    ha='center', va='center', fontsize=8, color='white', fontweight='bold')

        # flip markers on left side
        for i in range(1, n):
            y = base_y + (n - 1 - i) * (pancake_h + gap) + pancake_h
            ax.plot([0.08, 0.12], [y + gap / 2, y + gap / 2], color='gray', linewidth=0.5)
            ax.text(0.06, y + gap / 2, str(i + 1), ha='center', va='center', fontsize=5, color='gray')

        ax.text(cx, base_y + n * (pancake_h + gap) + 0.02, f'Goal: {[int(x) for x in goal.perm]}',
                ha='center', va='center', fontsize=7, color='dimgray')

        ax.set_xlim(0.0, 1.0)
        ax.set_ylim(0.0, 1.0)
        ax.axis('off')
        fig.canvas.draw()

    def string_to_action(self, act_str: str) -> Optional[PancakeAction]:
        try:
            k = int(act_str.strip())
            if 2 <= k <= self.num_pancakes:
                return PancakeAction(k - 1)
            return None
        except ValueError:
            return None

    def string_to_action_help(self) -> str:
        return f"flip top K pancakes: enter K (2-{self.num_pancakes})"

    def __repr__(self) -> str:
        return f"Pancake(num_pancakes={self.num_pancakes})"


@domain_factory.register_parser("pancake")
class PancakeParser(Parser):
    def parse(self, args_str: str) -> Dict[str, Any]:
        return {"num_pancakes": int(args_str)}

    def help(self) -> str:
        return "Number of pancakes. E.g. 'pancake.8'"
