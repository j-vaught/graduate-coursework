"""Visualize DeepXube puzzle domains: goal state and scrambled state."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from deepxube.factories.domain_factory import domain_factory
from deepxube.base.domain import StateGoalVizable, GoalSampleable
from deepxube.domains.grid import Grid, GridState, GridGoal

WHITE = "#FFFFFF"
SCRAMBLE_STEPS = 20

# --- Cube3 ---
print("Visualizing: cube3")
cube = domain_factory.build_class("cube3", {})
goal_states, goals = cube.sample_goalstate_goal_pairs(1)
scrambled, _ = cube.random_walk(goal_states, [SCRAMBLE_STEPS])

for suffix, state in [("goal", goal_states[0]), ("scrambled", scrambled[0])]:
    fig = plt.figure(figsize=(5, 5))
    fig.patch.set_facecolor(WHITE)
    cube.visualize_state_goal(state, goals[0], fig)
    fig.savefig(f"viz_cube3_{suffix}.png", dpi=150, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"  Saved viz_cube3_{suffix}.png")

# --- N-Puzzle ---
print("Visualizing: npuzzle")
npuzz = domain_factory.build_class("npuzzle", {})
goal_states, goals = npuzz.sample_goalstate_goal_pairs(1)
scrambled, _ = npuzz.random_walk(goal_states, [SCRAMBLE_STEPS])

for suffix, state in [("goal", goal_states[0]), ("scrambled", scrambled[0])]:
    fig = plt.figure(figsize=(5, 5))
    fig.patch.set_facecolor(WHITE)
    npuzz.visualize_state_goal(state, goals[0], fig)
    fig.savefig(f"viz_npuzzle_{suffix}.png", dpi=150, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"  Saved viz_npuzzle_{suffix}.png")

# --- Grid ---
print("Visualizing: grid")
grid = domain_factory.build_class("grid", {})
start = grid.sample_start_states(1)[0]
goal_obj = GridGoal(3, 3)  # fixed goal position

for suffix, state in [("start", start)]:
    fig = plt.figure(figsize=(5, 5))
    fig.patch.set_facecolor(WHITE)
    grid.visualize_state_goal(state, goal_obj, fig)
    fig.savefig(f"viz_grid_{suffix}.png", dpi=150, bbox_inches="tight", facecolor=WHITE)
    plt.close(fig)
    print(f"  Saved viz_grid_{suffix}.png")

print("\nDone!")
