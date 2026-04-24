"""Verify linkage fixes: SENTINEL handling and L1 cost labels."""
import sys
sys.path.insert(0, "/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Extra_Credit/deepxube")

import numpy as np
from deepxube.domains.four_bar_linkage import FourBarLinkage, LinkState, LinkGoal, SENTINEL

env = FourBarLinkage(n_steps=64, n_waypoints=64, n_bins=64)

# Test 1: SENTINEL no longer maps to bin 0
print("=== Test 1: SENTINEL handling ===")
states, goals = env.sample_goalstate_goal_pairs(100)
flat = env.to_np_flat_sg(states, goals)
g_flat = flat[1]  # (100, 128) goal array

# Check that SENTINEL values map to n_bins (64), not 0
n_sentinel = 0
n_at_64 = 0
for i in range(100):
    for j in range(128):
        if goals[i].curve[j] == SENTINEL:
            n_sentinel += 1
            assert g_flat[i, j] == 64, f"SENTINEL mapped to {g_flat[i, j]}, expected 64"
            n_at_64 += 1

print(f"  {n_sentinel} SENTINEL values correctly mapped to bin 64")
print(f"  Input info: {env.get_input_info_flat_sg()}")
print("  PASS")

# Test 2: L1 cost labels
print("\n=== Test 2: L1 parameter distance as cost ===")
np.random.seed(42)
states, goals = env.sample_goalstate_goal_pairs(50)
steps = [20] * 50
walked, costs = env.random_walk(states, steps)

for i in range(50):
    diff = np.abs(walked[i].params.astype(int) - states[i].params.astype(int))
    diff[5] = min(diff[5], 64 - diff[5])
    expected = float(np.sum(diff))
    assert costs[i] == expected, f"Cost mismatch at {i}: {costs[i]} vs {expected}"
    assert costs[i] <= 20, f"L1 cost {costs[i]} > walk length 20"

avg_cost = np.mean(costs)
avg_steps = 20
print(f"  Walk length: {avg_steps}, Avg L1 cost: {avg_cost:.1f} (ratio: {avg_cost/avg_steps:.2f})")
print("  PASS")

# Test 3: Cost distribution at various depths
print("\n=== Test 3: Cost vs depth ===")
np.random.seed(0)
for depth in [5, 10, 20, 50]:
    states, goals = env.sample_goalstate_goal_pairs(500)
    walked, costs = env.random_walk(states, [depth] * 500)
    print(f"  Depth {depth:2d}: L1 cost mean={np.mean(costs):.1f}, "
          f"std={np.std(costs):.1f}, ratio={np.mean(costs)/depth:.2f}")

print("\nAll tests passed!")
