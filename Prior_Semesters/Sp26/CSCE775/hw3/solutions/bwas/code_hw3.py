from typing import List, Tuple, Dict, Optional
from environments.environment_abstract import Environment, State
import torch
from torch import nn
import numpy as np
import heapq


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """
    Batch Weighted A* Search (BWAS) algorithm.

    Pops N nodes at a time from the open list, expands them all, batches all their
    children together for a single neural network evaluation, then pushes them all back.

    Args:
        env: Environment instance
        state_start: Starting state
        nnet: Neural network (DQN) for heuristic evaluation

    Returns:
        List of actions leading to terminal state, or None if no solution found
    """
    batch_size = 100
    weight = 1.0
    max_expansions = 200000

    # Handle terminal start state
    if env.is_terminal(state_start):
        return []

    # Initialize open list (priority queue)
    # Format: (f_value, counter, state, path)
    counter = 0
    open_list = []

    # Initialize with start state
    # Heuristic: h(s) = -max_a Q(s,a), clamped >= 0
    h_start = _compute_heuristic(env, [state_start], nnet)[0]
    f_start = 0.0 + weight * h_start
    heapq.heappush(open_list, (f_start, counter, state_start, []))
    counter += 1

    # Track best g values seen
    best_g = {state_start: 0.0}

    # Expansion counter
    num_expansions = 0

    while open_list and num_expansions < max_expansions:
        # Pop a batch of up to batch_size nodes
        batch_nodes = []
        for _ in range(min(batch_size, len(open_list))):
            if open_list:
                f_val, cnt, state, path = heapq.heappop(open_list)
                batch_nodes.append((state, path))

        # Expand all nodes in batch
        all_children = []
        for state, path in batch_nodes:
            num_expansions += 1

            # Check if terminal on expansion
            if env.is_terminal(state):
                return path

            # Get available actions
            actions = env.get_actions(state)

            # Expand all children
            for action in actions:
                expected_reward, next_states, probs = env.state_action_dynamics(state, action)

                # For deterministic environments, next_states has one element
                for next_state, prob in zip(next_states, probs):
                    new_g = -expected_reward + best_g[state]
                    new_path = path + [action]

                    # Track this child for batch evaluation
                    all_children.append((next_state, new_g, new_path))

        if not all_children:
            continue

        # Extract unique states and their best g values for heuristic evaluation
        states_to_eval = []
        state_to_children = {}

        for next_state, new_g, new_path in all_children:
            if next_state not in best_g or new_g < best_g[next_state]:
                if next_state not in state_to_children:
                    states_to_eval.append(next_state)
                    state_to_children[next_state] = []
                state_to_children[next_state].append((new_g, new_path))

        # Batch evaluate heuristics for all unique children
        if states_to_eval:
            heuristics = _compute_heuristic(env, states_to_eval, nnet)

            # Push all children back to open list
            for idx, next_state in enumerate(states_to_eval):
                h_val = heuristics[idx]

                for new_g, new_path in state_to_children[next_state]:
                    # Update best_g if this is better
                    if next_state not in best_g or new_g < best_g[next_state]:
                        best_g[next_state] = new_g
                        f_val = new_g + weight * h_val
                        heapq.heappush(open_list, (f_val, counter, next_state, new_path))
                        counter += 1

    # No solution found
    return None


def _compute_heuristic(env: Environment, states: List[State], nnet: nn.Module) -> List[float]:
    """
    Compute heuristics for a batch of states.
    h(s) = -max_a Q(s,a), clamped >= 0

    Args:
        env: Environment instance
        states: List of states to evaluate
        nnet: Neural network for Q-value evaluation

    Returns:
        List of heuristic values
    """
    if not states:
        return []

    # Convert states to network input
    nnet_input = env.states_to_nnet_input(states)

    # Convert to tensor
    nnet_input_tensor = torch.tensor(nnet_input, dtype=torch.float32)

    # Forward pass
    with torch.no_grad():
        q_values = nnet(nnet_input_tensor)  # Shape: (batch_size, num_actions)

    # Compute heuristics: h = -max_a Q(s,a), clamped >= 0
    max_q_values = torch.max(q_values, dim=1)[0].cpu().numpy()
    heuristics = np.maximum(-max_q_values, 0.0)

    return heuristics.tolist()
