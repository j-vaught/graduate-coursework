from typing import Dict, List, Optional
from environments.environment_abstract import Environment, State
import torch
from torch import nn
import numpy as np
import heapq


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """Find a path from the start state to the goal with weighted A* guided by the DQN."""

    is_terminal = env.is_terminal
    if is_terminal(state_start):
        return []

    get_actions = env.get_actions
    state_action_dynamics = env.state_action_dynamics
    device = next(nnet.parameters()).device
    weight = 3.0
    inf = float('inf')
    heappush = heapq.heappush
    heappop = heapq.heappop

    def heuristic(states: List[State]) -> np.ndarray:
        inp = env.states_to_nnet_input(states)
        tensor = torch.from_numpy(inp).to(device)
        qvals = nnet(tensor).cpu().numpy()
        return np.maximum(-qvals.max(axis=1), 0.0)

    parent: Dict[State, tuple[State, int]] = {}

    def reconstruct(state: State) -> List[int]:
        actions: List[int] = []
        while state in parent:
            prev_state, action = parent[state]
            actions.append(action)
            state = prev_state
        actions.reverse()
        return actions

    with torch.inference_mode():
        ctr = 0
        heap = [(float(heuristic([state_start])[0]), ctr, state_start, 0.0)]
        ctr += 1
        best_g = {state_start: 0.0}
        closed = set()

        while heap:
            _, _, state, g = heappop(heap)

            if state in closed or g > best_g.get(state, inf):
                continue

            if is_terminal(state):
                return reconstruct(state)

            closed.add(state)

            children_states = []
            children_gs = []
            for action in get_actions(state):
                reward, next_states, _ = state_action_dynamics(state, action)
                ns = next_states[0]
                if ns in closed:
                    continue
                ng = g - reward
                if ng < best_g.get(ns, inf):
                    best_g[ns] = ng
                    parent[ns] = (state, action)
                    if is_terminal(ns):
                        return reconstruct(ns)
                    children_states.append(ns)
                    children_gs.append(ng)

            if not children_states:
                continue

            h_vals = heuristic(children_states)
            for ns, ng, h in zip(children_states, children_gs, h_vals):
                heappush(heap, (ng + weight * float(h), ctr, ns, ng))
                ctr += 1

    return None
