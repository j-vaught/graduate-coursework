from typing import List, Tuple, Dict, Optional
from environments.environment_abstract import Environment, State
import torch
from torch import nn
import numpy as np


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """
    Beam search using DQN heuristic.

    Keeps top-K candidates at each depth level. Expands all states in beam,
    evaluates children with DQN, and keeps only top-K by lowest h(s) value.

    h(s) = -max_a Q(s,a), clamped >= 0

    Args:
        env: Environment with state_action_dynamics, get_actions, is_terminal
        state_start: Initial state
        nnet: Neural network module returning Q-values

    Returns:
        List of actions to reach terminal state, or None if no solution found
    """
    # Check if start is terminal
    if env.is_terminal(state_start):
        return []

    beam_width_initial = 1000
    beam_width_retry = 5000
    max_depth = 100

    def beam_search_with_width(beam_width: int) -> Optional[List[int]]:
        """Execute beam search with given beam width."""
        # Beam contains (state, action_history)
        beam = [(state_start, [])]
        visited = {state_start}

        for depth in range(max_depth):
            # If beam is empty, no solution found
            if not beam:
                return None

            # Expand all states in current beam
            all_children = []  # List of (child_state, action, parent_action_history, reward)

            for state, action_history in beam:
                actions = env.get_actions(state)

                for action in actions:
                    expected_reward, next_states, probs = env.state_action_dynamics(state, action)

                    # Handle deterministic case (single next state with prob 1)
                    # or stochastic case (multiple next states with probabilities)
                    if next_states:
                        # Take first state (most likely or deterministic)
                        next_state = next_states[0]

                        # Check if terminal
                        if env.is_terminal(next_state):
                            return action_history + [action]

                        # Add to children (avoiding revisits)
                        if next_state not in visited:
                            all_children.append((next_state, action, action_history, expected_reward))
                            visited.add(next_state)

            # If no children generated, beam search fails
            if not all_children:
                return None

            # Batch evaluate all children through DQN
            child_states = [child[0] for child in all_children]
            nnet_input = env.states_to_nnet_input(child_states)
            nnet_input_tensor = torch.tensor(nnet_input, dtype=torch.float32)

            # Get Q-values from network
            with torch.no_grad():
                q_values = nnet(nnet_input_tensor)  # Shape: (num_children, num_actions)

            # Compute heuristic h(s) = -max_a Q(s,a), clamped >= 0
            max_q_per_state = torch.max(q_values, dim=1)[0]  # (num_children,)
            h_values = (-max_q_per_state).clamp(min=0.0)  # clamp to >= 0

            # Rank children by h-value (lowest is best)
            h_values_np = h_values.cpu().numpy()
            ranked_indices = np.argsort(h_values_np)

            # Keep only top-K children
            k = min(beam_width, len(all_children))
            top_k_indices = ranked_indices[:k]

            # Build new beam from top-K children
            beam = []
            for idx in top_k_indices:
                next_state, action, parent_history, _ = all_children[idx]
                new_history = parent_history + [action]
                beam.append((next_state, new_history))

        # Max depth reached without finding solution
        return None

    # Try with initial beam width
    result = beam_search_with_width(beam_width_initial)
    if result is not None:
        return result

    # If failed, retry with larger beam width
    result = beam_search_with_width(beam_width_retry)
    return result
