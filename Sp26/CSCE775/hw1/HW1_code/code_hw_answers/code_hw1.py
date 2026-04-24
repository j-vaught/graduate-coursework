from typing import List, Dict, Tuple
from environments.environment_abstract import Environment, State
from numpy.typing import NDArray
import numpy as np


def mrp(state_trans_probs: NDArray, state_rewards: NDArray, gamma: float) -> NDArray:
    """ Compute the value of every state in the Markov reward process (MRP)
    |S| represents the size of the state space
    :param state_trans_probs: a |S|x|S| matrix of state transition probabilities
    :param state_rewards: a |S|x1 matrix of expected rewards for every state
    :param gamma: discount factor
    :return: a |S|x1 matrix of state values

    Bellman equation for MRP: V = R + γPV
    Solving: V = (I - γP)^(-1) R
    """
    n = state_trans_probs.shape[0]
    I = np.eye(n)
    state_values = np.linalg.solve(I - gamma * state_trans_probs, state_rewards)
    return state_values


def dynamic_programming(env: Environment, states: List[State], state_values: Dict[State, float],
                        gamma: float) -> Tuple[Dict[State, float], Dict[State, List[float]]]:
    """ Perform tabular dynamic programming to exactly compute the optimal value function and obtain an optimal policy

    @param env: environment
    @param states: all states in the state space
    @param state_values: dictionary that maps states to values
    @param gamma: the discount factor

    @return: the state value function and policy found by value iteration
    """
    threshold = 1e-10

    while True:
        delta = 0
        for state in states:
            if env.is_terminal(state):
                continue

            old_value = state_values[state]
            actions = env.get_actions(state)

            action_values = []
            for action in actions:
                expected_reward, next_states, probs = env.state_action_dynamics(state, action)
                q_value = expected_reward
                for next_state, prob in zip(next_states, probs):
                    q_value += gamma * prob * state_values[next_state]
                action_values.append(q_value)

            state_values[state] = max(action_values)
            delta = max(delta, abs(old_value - state_values[state]))

        if delta < threshold:
            break

    policy: Dict[State, List[float]] = {}
    for state in states:
        actions = env.get_actions(state)
        num_actions = len(actions)

        if env.is_terminal(state):
            policy[state] = [1.0 / num_actions] * num_actions
            continue

        action_values = []
        for action in actions:
            expected_reward, next_states, probs = env.state_action_dynamics(state, action)
            q_value = expected_reward
            for next_state, prob in zip(next_states, probs):
                q_value += gamma * prob * state_values[next_state]
            action_values.append(q_value)

        best_value = max(action_values)
        best_actions = [i for i, v in enumerate(action_values) if abs(v - best_value) < 1e-9]

        policy[state] = [0.0] * num_actions
        for a in best_actions:
            policy[state][a] = 1.0 / len(best_actions)

    return state_values, policy


def model_free(env: Environment, action_values: Dict[State, List[float]], gamma: float) -> Dict[State, List[float]]:
    """ Perform model free tabular reinforcement learning to compute an action-value function
    @param env: environment
    @param action_values: dictionary that maps states to their action values (list of floats)
    @param gamma: the discount factor

    @return: the action value function

    Q-learning: Q(s,a) <- Q(s,a) + alpha * [r + gamma * max_a' Q(s',a') - Q(s,a)]
    """
    alpha = 0.1
    epsilon = 0.1
    num_episodes = 10000
    max_steps = 500

    for episode in range(num_episodes):
        state = env.sample_start_states(1)[0]

        for step in range(max_steps):
            if env.is_terminal(state):
                break

            actions = env.get_actions(state)

            if np.random.random() < epsilon:
                action = np.random.choice(actions)
            else:
                q_vals = action_values[state]
                max_q = max(q_vals)
                best_actions = [a for a in actions if q_vals[a] == max_q]
                action = np.random.choice(best_actions)

            next_state, reward = env.sample_transition(state, action)

            if env.is_terminal(next_state):
                max_next_q = 0.0
            else:
                max_next_q = max(action_values[next_state])

            td_target = reward + gamma * max_next_q
            td_error = td_target - action_values[state][action]
            action_values[state][action] += alpha * td_error

            state = next_state

    return action_values
