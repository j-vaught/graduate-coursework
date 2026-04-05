from typing import List, Tuple, Dict, Optional
from environments.environment_abstract import Environment, State
import torch
from torch import nn
import numpy as np
import sys


sys.setrecursionlimit(10000)


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """
    IDA* search using DQN heuristic.

    Args:
        env: The environment
        state_start: The starting state
        nnet: Neural network for computing heuristic values

    Returns:
        List of actions to reach goal, empty list if start is terminal, None if no solution found
    """

    if env.is_terminal(state_start):
        return []

    def compute_heuristic(state: State) -> float:
        """Compute h(s) = -max_a Q(s,a), clamped >= 0"""
        with torch.no_grad():
            state_input = env.states_to_nnet_input([state])
            state_tensor = torch.FloatTensor(state_input)
            q_values = nnet(state_tensor).numpy()
            h = -np.max(q_values)
            return max(0.0, h)

    def dfs(state: State, g: float, threshold: float, path_actions: List[int],
            visited: set) -> Tuple[Optional[List[int]], float]:
        """
        Depth-first search with threshold pruning.

        Args:
            state: Current state
            g: Cost so far
            threshold: Current f-cost threshold
            path_actions: Actions taken to reach this state
            visited: Set of visited states on current path

        Returns:
            (solution_actions or None, next_threshold to try)
        """

        h = compute_heuristic(state)
        f = g + h

        if f > threshold:
            return (None, f)

        if state in visited:
            return (None, float('inf'))

        visited.add(state)

        min_exceeded = float('inf')

        for action in env.get_actions(state):
            expected_reward, next_states, probs = env.state_action_dynamics(state, action)
            next_state = next_states[0]

            new_g = g + (-expected_reward)

            if env.is_terminal(next_state):
                visited.remove(state)
                return (path_actions + [action], threshold)

            solution, next_thresh = dfs(next_state, new_g, threshold,
                                       path_actions + [action], visited)

            if solution is not None:
                visited.remove(state)
                return (solution, threshold)

            min_exceeded = min(min_exceeded, next_thresh)

        visited.remove(state)
        return (None, min_exceeded)

    threshold = compute_heuristic(state_start)

    for iteration in range(50):
        visited_set = set()
        solution, next_threshold = dfs(state_start, 0.0, threshold, [], visited_set)

        if solution is not None:
            return solution

        if next_threshold == float('inf'):
            return None

        threshold = next_threshold

    return None
