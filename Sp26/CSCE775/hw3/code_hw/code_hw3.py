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

    batch_size = 100
    ctr = 0
    h0 = float(heuristic([state_start])[0])
    heap = [(h0, ctr, state_start, 0.0, [])]
    ctr += 1
    best_g = {state_start: 0.0}

    while heap:
        # Pop a batch of nodes
        batch = []
        for _ in range(min(batch_size, len(heap))):
            batch.append(heapq.heappop(heap))

        # Expand all nodes in batch, collect all children
        all_children = []
        for f, _, state, g, actions in batch:
            if g > best_g.get(state, float('inf')):
                continue
            if env.is_terminal(state):
                return actions

            for a in env.get_actions(state):
                reward, next_states, _ = env.state_action_dynamics(state, a)
                ns = next_states[0]
                ng = g + (-reward)
                if ng < best_g.get(ns, float('inf')):
                    best_g[ns] = ng
                    all_children.append((ns, a, ng, actions + [a]))

        # Batch evaluate all children at once
        if all_children:
            states_batch = [c[0] for c in all_children]
            hs = heuristic(states_batch)
            for (ns, a, ng, path), h in zip(all_children, hs):
                heapq.heappush(heap, (ng + float(h), ctr, ns, ng, path))
                ctr += 1

    return None
