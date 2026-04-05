from typing import List, Tuple, Dict, Optional
from environments.environment_abstract import Environment, State
import torch
from torch import nn
import numpy as np


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """ Find paths from start state to goal using trained DQN

    :param env: environment
    :param state_start: starting state
    :param nnet: trained DQN

    :return: a list of integers representing the actions that should be taken to reach the goal or None if no solution
    """
    import heapq

    if env.is_terminal(state_start):
        return []

    def heuristic(states):
        inp = env.states_to_nnet_input(states)
        with torch.no_grad():
            qvals = nnet(torch.tensor(inp, dtype=torch.float32))
        return (-qvals.max(dim=1).values).clamp(min=0).numpy()

    ctr = 0
    h0 = float(heuristic([state_start])[0])
    heap = [(h0, ctr, state_start, 0.0, [])]
    ctr += 1
    best_g = {state_start: 0.0}

    while heap:
        f, _, state, g, actions = heapq.heappop(heap)

        if g > best_g.get(state, float('inf')):
            continue

        if env.is_terminal(state):
            return actions

        succs, s_actions, s_gs = [], [], []
        for a in env.get_actions(state):
            reward, next_states, _ = env.state_action_dynamics(state, a)
            ns = next_states[0]
            ng = g + (-reward)
            if ng < best_g.get(ns, float('inf')):
                best_g[ns] = ng
                succs.append(ns)
                s_actions.append(a)
                s_gs.append(ng)

        if succs:
            hs = heuristic(succs)
            for ns, a, ng, h in zip(succs, s_actions, s_gs, hs):
                heapq.heappush(heap, (ng + float(h), ctr, ns, ng, actions + [a]))
                ctr += 1

    return None
