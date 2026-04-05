"""Test all search algorithm variants and compare results."""
import sys
import os
import importlib
import time
import pickle
import numpy as np
import torch
from torch import nn
from typing import List, Optional, Tuple
from environments.environment_abstract import Environment, State
from environments import env_utils


class FullyConnectedModel(nn.Module):
    def __init__(self, input_dim, layer_dims, layer_acts, batch_norms):
        super().__init__()
        self.layers = nn.ModuleList()
        self.flatten_nn = nn.Flatten()
        for layer_dim, act, batch_norm in zip(layer_dims, layer_acts, batch_norms):
            module_list = nn.ModuleList()
            module_list.append(nn.Linear(input_dim, layer_dim))
            if batch_norm:
                module_list.append(nn.BatchNorm1d(layer_dim))
            if act.upper() == "RELU":
                module_list.append(nn.ReLU())
            elif act.upper() != "LINEAR":
                raise ValueError(f"Unknown activation function {act}")
            self.layers.append(module_list)
            input_dim = layer_dim

    def forward(self, x):
        for module_list in self.layers:
            for module in module_list:
                x = module(x)
        return x


def check_soln(env, state_start, actions):
    state = state_start
    path_cost = np.inf
    if actions is not None:
        path_cost = 0.0
        for action in actions:
            state, reward = env.sample_transition(state, action)
            path_cost += -reward
    is_solved = env.is_terminal(state)
    return path_cost, is_solved


def test_variant(name, search_fn, env, states_start, path_costs_gt, dqn):
    is_optimal_l = []
    is_solved_l = []
    optimal_diffs = []
    start_time_tot = time.time()

    for idx, state_start in enumerate(states_start):
        gt = path_costs_gt[idx]
        try:
            actions = search_fn(env, state_start, dqn)
        except Exception as e:
            print(f"  [{name}] State {idx+1}: EXCEPTION - {e}")
            is_solved_l.append(False)
            is_optimal_l.append(False)
            optimal_diffs.append(float('inf'))
            continue

        path_cost, is_solved = check_soln(env, state_start, actions)
        is_solved_l.append(is_solved)
        is_optimal_l.append(path_cost == gt)
        optimal_diffs.append(path_cost - gt)

    total_time = time.time() - start_time_tot
    pct_solved = 100 * np.mean(is_solved_l)
    pct_optimal = 100 * np.mean(is_optimal_l)
    avg_diff = np.mean([d for d in optimal_diffs if d != float('inf')])

    return {
        'name': name,
        'pct_solved': pct_solved,
        'pct_optimal': pct_optimal,
        'avg_diff': avg_diff,
        'total_time': total_time,
    }


def main():
    env = env_utils.get_environment("puzzle8")[0]
    dqn = FullyConnectedModel(81, [200, 100, 4], ["relu", "relu", "linear"], [False, False, False])
    dqn.load_state_dict(torch.load("data/puzzle8/nnet.pt"))
    dqn.eval()

    data = pickle.load(open("data/puzzle8/puzzle8_states.pkl", "rb"), encoding="latin1")
    states_all = data['states']
    costs_all = np.array(data['optimal_path_cost'])

    # Build balanced test set (same as run_hw3.py)
    np.random.seed(42)  # fixed seed for fair comparison
    states_start = []
    path_costs_gt = []
    for pc in range(max(costs_all) + 1):
        idxs = np.where(costs_all == pc)[0]
        chosen = np.random.choice(idxs, size=min(5, len(idxs)))
        states_start.extend(states_all[i] for i in chosen)
        path_costs_gt.extend(costs_all[i] for i in chosen)

    print(f"Testing {len(states_start)} states\n")

    variants = [
        ('A*', 'solutions.astar.code_hw3'),
        ('BWAS', 'solutions.bwas.code_hw3'),
        ('GBFS', 'solutions.gbfs.code_hw3'),
        ('IDA*', 'solutions.ida_star.code_hw3'),
        ('Beam Search', 'solutions.beam_search.code_hw3'),
    ]

    results = []
    for name, module_path in variants:
        print(f"--- Testing {name} ---")
        try:
            mod = importlib.import_module(module_path)
            res = test_variant(name, mod.search, env, states_start, path_costs_gt, dqn)
            results.append(res)
            print(f"  Solved: {res['pct_solved']:.1f}%  Optimal: {res['pct_optimal']:.1f}%  "
                  f"Avg diff: {res['avg_diff']:.3f}  Time: {res['total_time']:.2f}s\n")
        except Exception as e:
            print(f"  FAILED TO LOAD: {e}\n")
            results.append({'name': name, 'pct_solved': 0, 'pct_optimal': 0, 'avg_diff': float('inf'), 'total_time': 0})

    # Summary table
    print("=" * 80)
    print(f"{'Algorithm':<15} {'Solved%':>8} {'Optimal%':>9} {'Avg Diff':>9} {'Time (s)':>9} {'Pass?':>6}")
    print("-" * 80)
    for r in sorted(results, key=lambda x: (-x['pct_solved'], -x['pct_optimal'], x['total_time'])):
        passed = r['pct_solved'] == 100 and r['pct_optimal'] >= 50 and r['total_time'] < 30
        print(f"{r['name']:<15} {r['pct_solved']:>7.1f}% {r['pct_optimal']:>8.1f}% "
              f"{r['avg_diff']:>9.3f} {r['total_time']:>9.2f} {'YES' if passed else 'NO':>6}")
    print("=" * 80)


if __name__ == "__main__":
    main()
