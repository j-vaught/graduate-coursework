"""Diagnostic script for four-bar linkage domain in DeepXube.

Investigates why training loss is stagnant (~230 -> ~226 over 53k iters)
and test solve rate is poor (16% at avg path cost 1.75).
"""

import sys
import os
import numpy as np
from collections import defaultdict
from scipy import stats

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

from deepxube.domains.four_bar_linkage import (
    FourBarLinkage, LinkState, LinkGoal, LinkAction,
    N_PARAMS, SENTINEL,
)

np.random.seed(42)

DOMAIN = FourBarLinkage(n_steps=64, n_waypoints=64, n_bins=64, ws_range=8.0)

SEPARATOR = "=" * 72


def print_header(title):
    print(f"\n{SEPARATOR}")
    print(f"  {title}")
    print(SEPARATOR)


# ------------------------------------------------------------------ helpers

def make_random_state():
    params = np.random.randint(0, DOMAIN.n_steps, size=N_PARAMS).astype(np.int8)
    return LinkState(params)


def scramble_from_state(state, n_steps):
    """Do a random walk of n_steps from state, return final state and path cost."""
    states_out, costs = DOMAIN.random_walk([state], [n_steps])
    return states_out[0], costs[0]


def curve_bins(state):
    return DOMAIN._state_to_curve_bins(state)


def count_valid_waypoints(bins_arr):
    return int(np.sum(bins_arr[::2] != SENTINEL))


def count_matching_waypoints(bins_a, bins_b):
    valid_a = bins_a[::2] != SENTINEL
    valid_b = bins_b[::2] != SENTINEL
    both_valid = valid_a & valid_b
    if not np.any(both_valid):
        return 0, 0
    idxs = np.where(both_valid)[0]
    match = np.sum(
        (bins_a[idxs * 2] == bins_b[idxs * 2]) &
        (bins_a[idxs * 2 + 1] == bins_b[idxs * 2 + 1])
    )
    return int(match), int(np.sum(both_valid))


def l1_param_dist(s1, s2):
    return int(np.sum(np.abs(s1.params.astype(int) - s2.params.astype(int))))


def l2_param_dist(s1, s2):
    return float(np.sqrt(np.sum((s1.params.astype(float) - s2.params.astype(float)) ** 2)))


def curve_l2_distance(s1, s2):
    """L2 distance between the raw (continuous) coupler curves, ignoring NaN waypoints."""
    c1 = DOMAIN._coupler_curve(s1.params)
    c2 = DOMAIN._coupler_curve(s2.params)
    valid = ~np.isnan(c1[:, 0]) & ~np.isnan(c2[:, 0])
    if not np.any(valid):
        return float('nan')
    diff = c1[valid] - c2[valid]
    return float(np.sqrt(np.sum(diff ** 2)))


def bin_vector_l1(s1, s2):
    """L1 distance between curve-bin vectors, only counting mutually valid waypoints."""
    b1 = curve_bins(s1)
    b2 = curve_bins(s2)
    valid = (b1[::2] != SENTINEL) & (b2[::2] != SENTINEL)
    if not np.any(valid):
        return float('nan')
    idxs = np.where(valid)[0]
    dx = np.abs(b1[idxs * 2].astype(int) - b2[idxs * 2].astype(int))
    dy = np.abs(b1[idxs * 2 + 1].astype(int) - b2[idxs * 2 + 1].astype(int))
    return float(np.sum(dx + dy))


# ================================================================== TEST 1
def test_cost_to_go_learnability(n_goals=200, n_samples_per_depth=50):
    print_header("TEST 1: Cost-to-go learnability")

    depths = [1, 2, 3, 5, 10, 20, 50, 100]
    records = []

    for goal_idx in range(n_goals):
        goal_state = make_random_state()
        goal_bins = curve_bins(goal_state)
        goal = LinkGoal(goal_bins)

        for depth in depths:
            scrambled, path_cost = scramble_from_state(goal_state, depth)
            param_l1 = l1_param_dist(scrambled, goal_state)
            param_l2 = l2_param_dist(scrambled, goal_state)
            match, total = count_matching_waypoints(
                curve_bins(scrambled), goal_bins)
            match_frac = match / total if total > 0 else float('nan')
            c_l2 = curve_l2_distance(scrambled, goal_state)
            bv_l1 = bin_vector_l1(scrambled, goal_state)

            records.append({
                'depth': depth,
                'path_cost': path_cost,
                'param_l1': param_l1,
                'param_l2': param_l2,
                'match_frac': match_frac,
                'curve_l2': c_l2,
                'bin_l1': bv_l1,
            })

    # Analyze correlations
    depths_arr = np.array([r['depth'] for r in records], dtype=float)
    costs_arr = np.array([r['path_cost'] for r in records], dtype=float)
    param_l1_arr = np.array([r['param_l1'] for r in records], dtype=float)
    param_l2_arr = np.array([r['param_l2'] for r in records], dtype=float)
    match_arr = np.array([r['match_frac'] for r in records], dtype=float)
    curve_l2_arr = np.array([r['curve_l2'] for r in records], dtype=float)
    bin_l1_arr = np.array([r['bin_l1'] for r in records], dtype=float)

    print("\n--- Path cost vs scramble depth ---")
    valid = ~np.isnan(costs_arr)
    r, p = stats.pearsonr(depths_arr[valid], costs_arr[valid])
    print(f"  Pearson r = {r:.4f}, p = {p:.2e}")
    print(f"  Mean path_cost by depth:")
    for d in sorted(set(int(x) for x in depths_arr)):
        mask = depths_arr == d
        print(f"    depth={d:3d}: mean_cost={costs_arr[mask].mean():.2f}, "
              f"std={costs_arr[mask].std():.2f}, "
              f"min={costs_arr[mask].min():.1f}, max={costs_arr[mask].max():.1f}")

    print("\n--- Feature correlations with path_cost ---")
    for name, arr in [('param_L1', param_l1_arr), ('param_L2', param_l2_arr),
                       ('match_frac', match_arr), ('curve_L2', curve_l2_arr),
                       ('bin_L1', bin_l1_arr)]:
        valid_mask = ~np.isnan(arr) & ~np.isnan(costs_arr)
        if np.sum(valid_mask) < 10:
            print(f"  {name}: too few valid samples")
            continue
        r, p = stats.pearsonr(arr[valid_mask], costs_arr[valid_mask])
        print(f"  {name}: r={r:.4f}, p={p:.2e}")

    print("\n--- Feature correlations with scramble_depth ---")
    for name, arr in [('param_L1', param_l1_arr), ('param_L2', param_l2_arr),
                       ('match_frac', match_arr), ('curve_L2', curve_l2_arr),
                       ('bin_L1', bin_l1_arr)]:
        valid_mask = ~np.isnan(arr)
        if np.sum(valid_mask) < 10:
            print(f"  {name}: too few valid samples")
            continue
        r, p = stats.pearsonr(depths_arr[valid_mask], arr[valid_mask])
        print(f"  {name}: r={r:.4f}, p={p:.2e}")

    # KEY: is path_cost == depth? (are random walks self-avoiding?)
    print("\n--- Random walk self-cancellation ---")
    print("  If path_cost << depth, the walk is canceling itself.")
    for d in sorted(set(int(x) for x in depths_arr)):
        mask = depths_arr == d
        ratio = costs_arr[mask].mean() / d if d > 0 else float('nan')
        actual_param_dist = param_l1_arr[mask].mean()
        print(f"    depth={d:3d}: mean_cost/depth={ratio:.3f}, "
              f"mean_param_L1={actual_param_dist:.1f}")


# ================================================================== TEST 2
def test_input_representation(n_samples=2000):
    print_header("TEST 2: Input representation quality")

    # Check fraction of SENTINEL waypoints
    sentinel_fracs = []
    for _ in range(n_samples):
        s = make_random_state()
        bins = curve_bins(s)
        n_valid = count_valid_waypoints(bins)
        sentinel_fracs.append(1.0 - n_valid / DOMAIN.n_waypoints)

    sentinel_arr = np.array(sentinel_fracs)
    print(f"\n--- SENTINEL (NaN) waypoint fraction ---")
    print(f"  Mean: {sentinel_arr.mean():.4f}")
    print(f"  Median: {np.median(sentinel_arr):.4f}")
    print(f"  Min: {sentinel_arr.min():.4f}, Max: {sentinel_arr.max():.4f}")
    print(f"  Fraction of states with >50% NaN: {np.mean(sentinel_arr > 0.5):.4f}")
    print(f"  Fraction of states with 100% NaN: {np.mean(sentinel_arr >= 1.0):.4f}")
    print(f"  Fraction of states with 0% NaN: {np.mean(sentinel_arr == 0.0):.4f}")

    # Check how SENTINEL is handled in to_np_flat_sg
    print(f"\n--- SENTINEL handling in to_np_flat_sg ---")
    print(f"  SENTINEL value = {SENTINEL} (int8)")
    print(f"  In to_np_flat_sg, goal curve is clipped: np.clip(g, 0, n_bins-1)")
    print(f"  So SENTINEL (-1) becomes 0 -- indistinguishable from bin 0!")

    # How big is the one-hot input?
    dims, depths = DOMAIN.get_input_info_flat_sg()
    total_input = sum(d * oh for d, oh in zip(dims, depths))
    print(f"\n--- One-hot encoding dimensions ---")
    print(f"  State: {dims[0]} params x {depths[0]} one-hot = {dims[0]*depths[0]} features")
    print(f"  Goal: {dims[1]} curve bins x {depths[1]} one-hot = {dims[1]*depths[1]} features")
    print(f"  Total input dim: {total_input}")
    print(f"  State is {dims[0]*depths[0]/total_input*100:.1f}% of input, "
          f"Goal is {dims[1]*depths[1]/total_input*100:.1f}%")

    # Check: do similar-cost states have similar representations?
    print(f"\n--- Representation similarity for same-cost states ---")
    goal_state = make_random_state()
    goal_bins = curve_bins(goal_state)
    goal = LinkGoal(goal_bins)

    for depth in [1, 5, 10, 50]:
        bin_dists = []
        for _ in range(100):
            s1, _ = scramble_from_state(goal_state, depth)
            s2, _ = scramble_from_state(goal_state, depth)
            b1 = curve_bins(s1)
            b2 = curve_bins(s2)
            valid = (b1[::2] != SENTINEL) & (b2[::2] != SENTINEL)
            if np.any(valid):
                idxs = np.where(valid)[0]
                d_total = np.sum(np.abs(b1[idxs*2].astype(int) - b2[idxs*2].astype(int)) +
                                 np.abs(b1[idxs*2+1].astype(int) - b2[idxs*2+1].astype(int)))
                bin_dists.append(d_total)
        if bin_dists:
            print(f"  depth={depth:3d}: mean bin-vector L1 between same-cost scrambles = "
                  f"{np.mean(bin_dists):.1f} (std={np.std(bin_dists):.1f})")


# ================================================================== TEST 3
def test_random_walk_quality(n_walks=500):
    print_header("TEST 3: Random walk quality")

    # Check parameter diversity after random walks
    print("\n--- Parameter diversity after random walks ---")
    for depth in [1, 5, 10, 20, 50, 100]:
        start = make_random_state()
        endpoints = []
        for _ in range(200):
            end, cost = scramble_from_state(start, depth)
            endpoints.append(end.params.astype(int))

        endpoints_arr = np.array(endpoints)
        unique_states = len(set(tuple(e) for e in endpoints_arr))

        print(f"\n  depth={depth:3d}: {unique_states}/200 unique endpoints")

        # Parameter-wise spread
        for p in range(N_PARAMS):
            vals = endpoints_arr[:, p]
            print(f"    param[{p}] ({['a','b','c','d','p','beta'][p]:4s}): "
                  f"start={int(start.params[p]):2d}, "
                  f"mean={vals.mean():.1f}, std={vals.std():.1f}, "
                  f"range=[{vals.min()}, {vals.max()}]")

    # Check boundary clamping: how often do walks hit boundaries?
    print("\n\n--- Boundary clamping analysis ---")
    n_at_boundary = defaultdict(int)
    n_total_samples = 0
    for _ in range(n_walks):
        start = make_random_state()
        end, _ = scramble_from_state(start, 50)
        n_total_samples += 1
        for p in range(N_PARAMS):
            val = int(end.params[p])
            if p == 5:  # beta wraps, no boundary
                continue
            if val == 0 or val == DOMAIN.n_steps - 1:
                n_at_boundary[p] += 1

    print(f"  After 50-step walks from random starts ({n_walks} samples):")
    for p in range(5):
        frac = n_at_boundary[p] / n_total_samples
        print(f"    param[{p}] ({['a','b','c','d','p'][p]:4s}): "
              f"{frac*100:.1f}% at boundary (0 or {DOMAIN.n_steps-1})")

    # Check: does the walk return to start? (self-cancellation)
    print("\n--- Walk self-cancellation (param L1 from start) ---")
    for depth in [1, 5, 10, 20, 50, 100]:
        distances = []
        for _ in range(200):
            start = make_random_state()
            end, cost = scramble_from_state(start, depth)
            distances.append(l1_param_dist(start, end))
        print(f"  depth={depth:3d}: mean_param_L1={np.mean(distances):.2f}, "
              f"std={np.std(distances):.2f}, "
              f"zero_dist_frac={np.mean(np.array(distances)==0):.3f}")


# ================================================================== TEST 4
def test_cost_distribution():
    print_header("TEST 4: Cost-to-go distribution in training data")

    # Simulate training data generation: uniform random depth from 1..step_max
    step_max_values = [50, 100, 200]
    for step_max in step_max_values:
        print(f"\n--- step_max = {step_max} ---")
        depths = np.random.randint(1, step_max + 1, size=2000)
        actual_costs = []
        for d in depths:
            start = make_random_state()
            _, cost = scramble_from_state(start, int(d))
            actual_costs.append(cost)
        actual_costs = np.array(actual_costs)

        print(f"  Requested depths: mean={depths.mean():.1f}, "
              f"std={depths.std():.1f}")
        print(f"  Actual path costs: mean={actual_costs.mean():.1f}, "
              f"std={actual_costs.std():.1f}")
        print(f"  Path cost percentiles: "
              f"10%={np.percentile(actual_costs,10):.0f}, "
              f"25%={np.percentile(actual_costs,25):.0f}, "
              f"50%={np.percentile(actual_costs,50):.0f}, "
              f"75%={np.percentile(actual_costs,75):.0f}, "
              f"90%={np.percentile(actual_costs,90):.0f}")

        # Cost IS the number of steps (each action costs 1.0) so cost == depth
        print(f"  Path cost == depth? "
              f"all_equal={np.all(actual_costs == depths)}")


# ================================================================== TEST 5
def test_goal_curve_overlap():
    print_header("TEST 5: Goal curve waypoint overlap after scrambling")

    print("\n--- Fraction of goal waypoints still matching after N steps ---")
    for depth in [1, 2, 3, 5, 10, 20, 50, 100]:
        match_fracs = []
        for _ in range(500):
            goal_state = make_random_state()
            goal_bins = curve_bins(goal_state)

            scrambled, _ = scramble_from_state(goal_state, depth)
            scrambled_bins = curve_bins(scrambled)

            match, total = count_matching_waypoints(scrambled_bins, goal_bins)
            if total > 0:
                match_fracs.append(match / total)

        if match_fracs:
            arr = np.array(match_fracs)
            print(f"  depth={depth:3d}: mean_match={arr.mean():.4f}, "
                  f"median={np.median(arr):.4f}, "
                  f"std={arr.std():.4f}, "
                  f"frac_100%_match={np.mean(arr>=1.0):.4f}, "
                  f"frac_0%_match={np.mean(arr==0):.4f}")

    # Check is_solved rate
    print("\n--- is_solved() check after N random steps ---")
    for depth in [1, 2, 3, 5, 10, 20]:
        solved_count = 0
        total = 500
        for _ in range(total):
            goal_state = make_random_state()
            goal_bins = curve_bins(goal_state)
            goal = LinkGoal(goal_bins)
            scrambled, _ = scramble_from_state(goal_state, depth)
            if DOMAIN.is_solved([scrambled], [goal])[0]:
                solved_count += 1
        print(f"  depth={depth:3d}: is_solved rate = {solved_count/total:.4f} "
              f"({solved_count}/{total})")


# ================================================================== TEST 6
def test_gradient_signal():
    print_header("TEST 6: Input difference analysis (gradient signal)")

    print("\n--- How different are inputs at cost=1 vs cost=10 vs cost=50? ---")
    n_trials = 300

    for depth in [1, 2, 5, 10, 20, 50]:
        param_diffs = []
        bin_diffs = []
        frac_bins_changed = []

        for _ in range(n_trials):
            goal_state = make_random_state()
            goal_bins = curve_bins(goal_state)

            scrambled, _ = scramble_from_state(goal_state, depth)
            scr_bins = curve_bins(scrambled)

            # Parameter difference
            pdiff = np.abs(scrambled.params.astype(int) - goal_state.params.astype(int))
            param_diffs.append(pdiff.sum())

            # Bin difference (only mutually valid)
            valid = (scr_bins[::2] != SENTINEL) & (goal_bins[::2] != SENTINEL)
            if np.any(valid):
                idxs = np.where(valid)[0]
                bx_diff = np.abs(scr_bins[idxs*2].astype(int) - goal_bins[idxs*2].astype(int))
                by_diff = np.abs(scr_bins[idxs*2+1].astype(int) - goal_bins[idxs*2+1].astype(int))
                bin_diffs.append((bx_diff.sum() + by_diff.sum()))
                frac_changed = np.mean((bx_diff > 0) | (by_diff > 0))
                frac_bins_changed.append(frac_changed)

        param_diffs = np.array(param_diffs)
        bin_diffs = np.array(bin_diffs) if bin_diffs else np.array([0.0])
        frac_bins_changed = np.array(frac_bins_changed) if frac_bins_changed else np.array([0.0])

        print(f"\n  depth={depth:3d}:")
        print(f"    param L1: mean={param_diffs.mean():.2f}, std={param_diffs.std():.2f}")
        print(f"    bin L1: mean={bin_diffs.mean():.1f}, std={bin_diffs.std():.1f}")
        print(f"    frac bins changed: mean={frac_bins_changed.mean():.4f}, "
              f"std={frac_bins_changed.std():.4f}")

    # Compare one-hot input difference magnitude
    print("\n\n--- One-hot Hamming distance analysis ---")
    print("  (How many one-hot bits differ between state and goal-state?)")

    for depth in [1, 5, 10, 50]:
        hamming_dists = []
        for _ in range(200):
            goal_state = make_random_state()
            goal_bins = curve_bins(goal_state)
            scrambled, _ = scramble_from_state(goal_state, depth)
            scr_bins = curve_bins(scrambled)

            # State one-hot: 6 params x 64 one-hot = 384 bits
            # Params that differ
            n_params_diff = np.sum(scrambled.params != goal_state.params)

            # Goal one-hot: 128 bins x 64 one-hot = 8192 bits
            # But SENTINEL (-1) is clipped to 0, so both valid and invalid
            # may look the same
            goal_clipped = np.clip(goal_bins.astype(np.int64), 0, DOMAIN.n_bins - 1)
            scr_clipped = np.clip(scr_bins.astype(np.int64), 0, DOMAIN.n_bins - 1)
            n_bins_diff = np.sum(goal_clipped != scr_clipped)

            # Total one-hot bits that differ = 2 * n_params_diff (one bit on, one bit off)
            # + 2 * n_bins_diff
            hamming_state = 2 * n_params_diff
            hamming_goal = 2 * n_bins_diff
            hamming_dists.append((hamming_state, hamming_goal, hamming_state + hamming_goal))

        h = np.array(hamming_dists)
        total_bits = 6 * 64 + 128 * 64
        print(f"  depth={depth:3d}: "
              f"state_OH_diff={h[:,0].mean():.1f}/{6*64}, "
              f"goal_OH_diff={h[:,1].mean():.1f}/{128*64}, "
              f"total_OH_diff={h[:,2].mean():.1f}/{total_bits} "
              f"({h[:,2].mean()/total_bits*100:.2f}%)")


# ================================================================== TEST 7
def test_action_effectiveness():
    print_header("TEST 7: Single-action curve sensitivity")

    print("\n--- How much does a single action change the curve? ---")
    n_trials = 500

    for param_idx in range(N_PARAMS):
        bin_changes = []
        frac_changes = []
        for _ in range(n_trials):
            state = make_random_state()
            s_bins = curve_bins(state)

            act = LinkAction(param_idx, +1)
            new_states, _ = DOMAIN.next_state([state], [act])
            new_state = new_states[0]
            n_bins = curve_bins(new_state)

            # Check if params actually changed (boundary clamping)
            if np.array_equal(state.params, new_state.params):
                continue

            valid = (s_bins[::2] != SENTINEL) & (n_bins[::2] != SENTINEL)
            if not np.any(valid):
                continue

            idxs = np.where(valid)[0]
            dx = np.abs(s_bins[idxs*2].astype(int) - n_bins[idxs*2].astype(int))
            dy = np.abs(s_bins[idxs*2+1].astype(int) - n_bins[idxs*2+1].astype(int))
            changed = (dx > 0) | (dy > 0)
            bin_changes.append(np.sum(dx + dy))
            frac_changes.append(np.mean(changed))

        if bin_changes:
            name = ['a','b','c','d','p','beta'][param_idx]
            print(f"  param[{param_idx}] ({name:4s}): "
                  f"mean_bin_L1_change={np.mean(bin_changes):.1f}, "
                  f"frac_waypts_changed={np.mean(frac_changes):.4f}, "
                  f"mean_frac_std={np.std(frac_changes):.4f}")


# ================================================================== TEST 8
def test_many_to_one_and_hash_collisions():
    print_header("TEST 8: Many-to-one mapping (different params -> same curve bins)")

    print("\n--- Do nearby parameters produce the same binned curve? ---")
    same_curve_count = 0
    total_checked = 0

    for _ in range(500):
        s1 = make_random_state()
        b1 = curve_bins(s1)

        # Try all 12 single-step neighbors
        for act in DOMAIN.all_actions:
            new_states, _ = DOMAIN.next_state([s1], [act])
            s2 = new_states[0]
            if np.array_equal(s1.params, s2.params):
                continue  # boundary, skip
            b2 = curve_bins(s2)
            total_checked += 1
            if np.array_equal(b1, b2):
                same_curve_count += 1

    print(f"  Single-step neighbors with IDENTICAL curve bins: "
          f"{same_curve_count}/{total_checked} = "
          f"{same_curve_count/total_checked*100:.2f}%")

    # Also check: is_solved can be True for states != goal_state
    print("\n--- False-positive solve rate (neighbor is_solved) ---")
    false_solved = 0
    total_checked2 = 0
    for _ in range(500):
        goal_state = make_random_state()
        goal_bins = curve_bins(goal_state)
        goal = LinkGoal(goal_bins)
        for act in DOMAIN.all_actions:
            new_states, _ = DOMAIN.next_state([goal_state], [act])
            s2 = new_states[0]
            if np.array_equal(goal_state.params, s2.params):
                continue
            total_checked2 += 1
            if DOMAIN.is_solved([s2], [goal])[0]:
                false_solved += 1

    print(f"  1-step neighbors that are is_solved=True for original goal: "
          f"{false_solved}/{total_checked2} = "
          f"{false_solved/total_checked2*100:.2f}%")


# ================================================================== TEST 9
def test_effective_vs_nominal_depth():
    print_header("TEST 9: Effective vs nominal scramble depth")

    print("\n--- After N random steps, what is the actual min-cost-to-go? ---")
    print("  (Estimated by checking if fewer steps could have reached the same state)")
    print("  Note: path_cost == depth since each action costs 1.0")

    # The REAL question: does a 50-step random walk end up at a state
    # that could be reached in far fewer steps?
    for depth in [5, 10, 20, 50]:
        param_l1s = []
        for _ in range(500):
            start = make_random_state()
            end, _ = scramble_from_state(start, depth)
            # In parameter space, L1 is a lower bound on true cost-to-go
            # because each action changes one param by 1
            # (except beta which wraps, so we need min(diff, 64-diff))
            diffs = np.abs(end.params.astype(int) - start.params.astype(int))
            # Beta wrapping
            beta_diff = int(diffs[5])
            beta_diff = min(beta_diff, DOMAIN.n_steps - beta_diff)
            diffs[5] = beta_diff
            lb = int(np.sum(diffs))
            param_l1s.append(lb)

        arr = np.array(param_l1s)
        print(f"  depth={depth:3d}: "
              f"mean_L1_lower_bound={arr.mean():.2f}, "
              f"std={arr.std():.2f}, "
              f"ratio_lb/depth={arr.mean()/depth:.3f}, "
              f"frac_lb==0={np.mean(arr==0):.4f}")


# ================================================================== MAIN
if __name__ == "__main__":
    print("Four-Bar Linkage Domain Diagnostic Report")
    print(f"Domain: {DOMAIN}")
    print(f"n_steps={DOMAIN.n_steps}, n_waypoints={DOMAIN.n_waypoints}, "
          f"n_bins={DOMAIN.n_bins}")
    print(f"Total actions: {len(DOMAIN.all_actions)}")

    dims, depths = DOMAIN.get_input_info_flat_sg()
    total_input = sum(d * oh for d, oh in zip(dims, depths))
    print(f"Input info: dims={dims}, one_hot_depths={depths}, total={total_input}")

    test_cost_to_go_learnability()
    test_input_representation()
    test_random_walk_quality()
    test_cost_distribution()
    test_goal_curve_overlap()
    test_gradient_signal()
    test_action_effectiveness()
    test_many_to_one_and_hash_collisions()
    test_effective_vs_nominal_depth()

    print(f"\n{SEPARATOR}")
    print("  DIAGNOSTIC COMPLETE")
    print(SEPARATOR)
