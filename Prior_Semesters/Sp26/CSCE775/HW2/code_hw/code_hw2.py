from environments.environment_abstract import Environment, State
from torch import nn
import torch
import torch.optim as optim
import numpy as np
import copy


class ValueNetwork(nn.Module):
    def __init__(self, input_dim=81, hidden_dim=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x):
        return self.net(x)


def greedy_action(env: Environment, state: State, nnet: nn.Module) -> int:
    actions = env.get_actions(state)
    num_samples = 8

    # Sample multiple transitions per action to reduce variance
    all_next_states = []
    all_rewards = np.zeros((len(actions), num_samples), dtype=np.float32)
    all_terminal = np.zeros((len(actions), num_samples), dtype=bool)

    for i, action in enumerate(actions):
        for k in range(num_samples):
            s_next, r = env.sample_transition(state, action)
            all_next_states.append(s_next)
            all_rewards[i, k] = r
            all_terminal[i, k] = env.is_terminal(s_next)

    nnet_input = env.states_to_nnet_input(all_next_states)
    nnet_input_t = torch.from_numpy(nnet_input)
    with torch.no_grad():
        values = nnet(nnet_input_t).squeeze(-1).numpy()

    values = values.reshape(len(actions), num_samples)
    values[all_terminal] = 0.0

    # Average Q-value across samples for each action
    q_values = np.mean(all_rewards + values, axis=1)

    return actions[np.argmax(q_values)]


def deep_rl(env: Environment) -> nn.Module:
    nnet = ValueNetwork(input_dim=81, hidden_dim=256)
    target_nnet = copy.deepcopy(nnet)
    optimizer = optim.Adam(nnet.parameters(), lr=0.001)
    loss_fn = nn.MSELoss()

    num_actions = 4
    gamma = 1.0
    num_samples = 3

    for iteration in range(100):
        states = env.sample_start_states(5000)
        np.random.shuffle(states)

        batch_size = 256
        nnet.train()
        target_nnet.eval()

        for batch_start in range(0, len(states), batch_size):
            batch_states = states[batch_start:batch_start + batch_size]
            actual_batch = len(batch_states)

            all_next_states = []
            all_rewards = np.zeros((actual_batch, num_actions, num_samples), dtype=np.float32)
            all_terminal = np.zeros((actual_batch, num_actions, num_samples), dtype=bool)

            for a in range(num_actions):
                for k in range(num_samples):
                    for i, s in enumerate(batch_states):
                        s_next, r = env.sample_transition(s, a)
                        all_next_states.append(s_next)
                        all_rewards[i, a, k] = r
                        all_terminal[i, a, k] = env.is_terminal(s_next)

            nnet_input = env.states_to_nnet_input(all_next_states)
            nnet_input_t = torch.from_numpy(nnet_input)

            with torch.no_grad():
                next_values = target_nnet(nnet_input_t).squeeze(-1).numpy()

            next_values = next_values.reshape(num_actions, num_samples, actual_batch).transpose(2, 0, 1)
            next_values[all_terminal] = 0.0

            # Average over samples, then max over actions
            q_values = np.mean(all_rewards + gamma * next_values, axis=2)
            targets = np.max(q_values, axis=1)

            state_input = env.states_to_nnet_input(batch_states)
            state_input_t = torch.from_numpy(state_input)
            targets_t = torch.from_numpy(targets)

            predictions = nnet(state_input_t).squeeze(-1)
            loss = loss_fn(predictions, targets_t)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (iteration + 1) % 5 == 0:
            target_nnet.load_state_dict(nnet.state_dict())

        if (iteration + 1) % 25 == 0:
            print(f"Iteration {iteration + 1}/100, loss: {loss.item():.4f}")

    return nnet
