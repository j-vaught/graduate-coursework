"""Test and benchmark the batch-vectorized random_walk."""
import sys
sys.path.insert(0, "/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Extra_Credit/deepxube")

import time
import numpy as np
from deepxube.domains.warehouse_mapf import WarehouseMAPF, MAPFState

def test_correctness_8x8():
    """Basic correctness: walks produce valid states."""
    np.random.seed(42)
    env = WarehouseMAPF(8, 8, 4)
    states, goals = env.sample_goalstate_goal_pairs(50)

    # set_active_goal is needed for passability
    env.set_active_goal(goals[0])

    steps = [np.random.randint(1, 20) for _ in range(50)]
    result_states, costs = env.random_walk(states, steps)

    assert len(result_states) == 50, f"Expected 50 states, got {len(result_states)}"
    assert len(costs) == 50, f"Expected 50 costs, got {len(costs)}"

    for i, (rs, c, ns) in enumerate(zip(result_states, costs, steps)):
        assert c == float(ns), f"Cost mismatch at {i}: {c} != {ns}"
        assert rs.positions.shape == (8,), f"Shape mismatch at {i}"
        # Check all robots are in bounds
        for k in range(4):
            r, col = int(rs.positions[2*k]), int(rs.positions[2*k+1])
            assert 0 <= r < 8, f"Robot {k} row {r} out of bounds"
            assert 0 <= col < 8, f"Robot {k} col {col} out of bounds"

    # Check no two robots occupy the same cell
    for i, rs in enumerate(result_states):
        positions = set()
        for k in range(4):
            pos = (int(rs.positions[2*k]), int(rs.positions[2*k+1]))
            assert pos not in positions, f"Collision at state {i}, pos {pos}"
            positions.add(pos)

    print("  8x8 correctness: PASS")

def test_correctness_28x28():
    """Correctness with 28x28 grid and 30 robots."""
    np.random.seed(42)
    env = WarehouseMAPF(28, 28, 30)
    states, goals = env.sample_goalstate_goal_pairs(20)

    env.set_active_goal(goals[0])

    steps = [np.random.randint(5, 50) for _ in range(20)]
    result_states, costs = env.random_walk(states, steps)

    assert len(result_states) == 20
    for i, rs in enumerate(result_states):
        positions = set()
        for k in range(30):
            r, col = int(rs.positions[2*k]), int(rs.positions[2*k+1])
            assert 0 <= r < 28, f"Robot {k} row {r} out of bounds"
            assert 0 <= col < 28, f"Robot {k} col {col} out of bounds"
            pos = (r, col)
            assert pos not in positions, f"Collision at state {i}, pos {pos}"
            positions.add(pos)

    print("  28x28 correctness: PASS")

def test_solved_states_stay():
    """States with 0 steps should be unchanged."""
    np.random.seed(42)
    env = WarehouseMAPF(8, 8, 4)
    states, goals = env.sample_goalstate_goal_pairs(10)
    env.set_active_goal(goals[0])

    steps = [0] * 10
    # 0-step walks should return original states
    # But max_steps = 0 means the loop doesn't run at all
    result_states, costs = env.random_walk(states, steps)
    for i, (orig, res) in enumerate(zip(states, result_states)):
        assert np.array_equal(orig.positions, res.positions), \
            f"State {i} changed with 0 steps"
    print("  0-step invariance: PASS")

def test_no_obstacle_violations():
    """Verify robots don't sit on non-goal obstacles after walking."""
    np.random.seed(123)
    env = WarehouseMAPF(28, 28, 30)
    states, goals = env.sample_goalstate_goal_pairs(200)
    env.set_active_goal(goals[0])

    steps = [np.random.randint(10, 80) for _ in range(200)]
    result_states, _ = env.random_walk(states, steps)

    for b, (rs, orig) in enumerate(zip(result_states, states)):
        goal_set = set()
        for k in range(30):
            gr, gc = int(orig.positions[2*k]), int(orig.positions[2*k+1])
            goal_set.add((gr, gc, k))
        for k in range(30):
            r, c = int(rs.positions[2*k]), int(rs.positions[2*k+1])
            if env.obstacles[r, c]:
                assert (r, c, k) in goal_set, \
                    f"State {b}, robot {k} at obstacle ({r},{c}) which is not its goal"

    print("  Obstacle violation check: PASS")

def benchmark_28x28():
    """Benchmark: 1000 walks on 28x28 with 30 robots, ~25 steps each."""
    np.random.seed(42)
    env = WarehouseMAPF(28, 28, 30)
    states, goals = env.sample_goalstate_goal_pairs(1000)
    env.set_active_goal(goals[0])

    steps = list(np.random.randint(10, 50, size=1000))

    # Warmup
    env.random_walk(states[:10], steps[:10])

    t0 = time.time()
    result_states, costs = env.random_walk(states, steps)
    elapsed = time.time() - t0

    avg_steps = np.mean(steps)
    print(f"  1000 walks, 30 robots, 28x28, avg {avg_steps:.0f} steps")
    print(f"  Total: {elapsed:.2f}s, Per walk: {elapsed/1000*1000:.2f}ms")
    return elapsed

def benchmark_100k_28x28():
    """Benchmark: 100k walks (the training batch size) on 28x28 with 30 robots."""
    np.random.seed(42)
    env = WarehouseMAPF(28, 28, 30)
    # Training generates 100k states per iteration, but random_walk
    # is called per-state with varying step counts
    N = 100000
    states, goals = env.sample_goalstate_goal_pairs(N)
    env.set_active_goal(goals[0])

    steps = list(np.random.randint(1, 50, size=N))

    t0 = time.time()
    result_states, costs = env.random_walk(states, steps)
    elapsed = time.time() - t0

    avg_steps = np.mean(steps)
    print(f"  100k walks, 30 robots, 28x28, avg {avg_steps:.0f} steps")
    print(f"  Total: {elapsed:.1f}s, Per walk: {elapsed/N*1000:.3f}ms")
    return elapsed


if __name__ == "__main__":
    print("=== Correctness Tests ===")
    test_correctness_8x8()
    test_correctness_28x28()
    test_solved_states_stay()
    test_no_obstacle_violations()

    print("\n=== Benchmarks ===")
    benchmark_28x28()
    print()
    benchmark_100k_28x28()
