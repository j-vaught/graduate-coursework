from typing import List, Tuple, Dict, Optional
from environments.environment_abstract import Environment, State
import torch
from torch import nn
import numpy as np
import heapq


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """
    Greedy Best-First Search using heuristic h(s) = -max_a Q(s,a), clamped >= 0.

    Uses a priority queue ordered only by h(s), tracking visited states to avoid cycles.
    Caps exploration at 200000 expansions.

    Args:
        env: Environment with get_actions, state_action_dynamics, is_terminal
        state_start: Starting state
        nnet: Neural network (DQN) that computes Q-values

    Returns:
        List of actions from start to terminal, or None if no solution found
    """

    if env.is_terminal(state_start):
        return []

    def compute_heuristic_batch(states):
        """Compute h(s) = -max_a Q(s,a), clamped >= 0 for a batch of states"""
        if not states:
            return []
        inp = env.states_to_nnet_input(states)
        with torch.no_grad():
            qvals = nnet(torch.tensor(inp, dtype=torch.float32))
        return (-qvals.max(dim=1).values).clamp(min=0).numpy()

    # Priority queue: (h_value, counter, state, action_path)
    counter = 0
    open_list = []
    h_start = float(compute_heuristic_batch([state_start])[0])
    heapq.heappush(open_list, (h_start, counter, state_start, []))
    counter += 1

    visited = set()
    expansions = 0
    max_expansions = 200000

    while open_list and expansions < max_expansions:
        _, _, current_state, action_path = heapq.heappop(open_list)

        if current_state in visited:
            continue

        visited.add(current_state)
        expansions += 1

        if env.is_terminal(current_state):
            return action_path

        # Expand and batch evaluate successors
        actions = env.get_actions(current_state)
        succs, s_actions = [], []
        for action in actions:
            _, next_states_list, _ = env.state_action_dynamics(current_state, action)
            ns = next_states_list[0]
            if ns not in visited:
                succs.append(ns)
                s_actions.append(action)

        if succs:
            hs = compute_heuristic_batch(succs)
            for ns, a, h in zip(succs, s_actions, hs):
                heapq.heappush(open_list, (float(h), counter, ns, action_path + [a]))
                counter += 1

    return None
