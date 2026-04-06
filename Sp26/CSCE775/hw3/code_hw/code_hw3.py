from typing import Dict, List, Optional
from environments.environment_abstract import Environment, State
import torch
from torch import nn
import numpy as np
import heapq


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """Find a path from the start state to the goal with weighted A* guided by the DQN."""

    if env.is_terminal(state_start):
        return []

    device = next(nnet.parameters()).device
    weight = 3.0

    def heuristic(states: List[State]) -> np.ndarray:
        inp = env.states_to_nnet_input(states)
        tensor = torch.from_numpy(inp).to(device)
        with torch.inference_mode():
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

    ctr = 0
    h0 = float(heuristic([state_start])[0])
    heap = [(h0, ctr, state_start, 0.0)]
    ctr += 1
    best_g = {state_start: 0.0}
    closed = set()

    while heap:
        _, _, state, g = heapq.heappop(heap)

        if state in closed:
            continue
        if g > best_g.get(state, float('inf')):
            continue

        if env.is_terminal(state):
            return reconstruct(state)

        closed.add(state)

        children_states = []
        children_gs = []
        for a in env.get_actions(state):
            reward, next_states, _ = env.state_action_dynamics(state, a)
            ns = next_states[0]
            if ns in closed:
                continue
            ng = g - reward
            if ng < best_g.get(ns, float('inf')):
                best_g[ns] = ng
                parent[ns] = (state, a)
                if env.is_terminal(ns):
                    return reconstruct(ns)
                children_states.append(ns)
                children_gs.append(ng)

        if not children_states:
            continue

        h_vals = heuristic(children_states)
        for ns, ng, h in zip(children_states, children_gs, h_vals):
            heapq.heappush(heap, (ng + weight * float(h), ctr, ns, ng))
            ctr += 1

    return None
