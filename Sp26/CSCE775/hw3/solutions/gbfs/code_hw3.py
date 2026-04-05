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

    def compute_heuristic(state: State) -> float:
        """Compute h(s) = -max_a Q(s,a), clamped >= 0"""
        states_input = env.states_to_nnet_input([state])
        q_values = nnet(torch.tensor(states_input, dtype=torch.float32))
        max_q = torch.max(q_values[0]).item()
        h_value = -max_q
        return max(0.0, h_value)

    # Priority queue: (h_value, counter, state, action_path)
    counter = 0
    open_list = []
    h_start = compute_heuristic(state_start)
    heapq.heappush(open_list, (h_start, counter, state_start, []))
    counter += 1

    visited = set()
    expansions = 0
    max_expansions = 200000

    while open_list and expansions < max_expansions:
        h_current, _, current_state, action_path = heapq.heappop(open_list)

        # Skip if already visited
        if current_state in visited:
            continue

        visited.add(current_state)
        expansions += 1

        # Check if terminal
        if env.is_terminal(current_state):
            return action_path

        # Expand successors
        actions = env.get_actions(current_state)
        for action in actions:
            expected_reward, next_states_list, probs_list = env.state_action_dynamics(
                current_state, action
            )

            # Use expected next state (weighted by probabilities)
            if next_states_list:
                next_state = next_states_list[0]  # Take first successor

                if next_state not in visited:
                    new_action_path = action_path + [action]
                    h_next = compute_heuristic(next_state)
                    heapq.heappush(open_list, (h_next, counter, next_state, new_action_path))
                    counter += 1

    return None
