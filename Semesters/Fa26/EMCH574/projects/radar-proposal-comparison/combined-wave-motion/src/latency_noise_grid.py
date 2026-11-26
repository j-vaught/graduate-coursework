"""Compare latency corrections on identical noisy echoes throughout the screened grid."""

import csv
import json
from pathlib import Path

import numpy as np

import paired_experiment as model


def cell_results(frequency, amplitude):
    delays = (0.0, 0.05, 0.1, 0.2, 0.625)
    phase_counts = []
    level_phase_counts = []
    visits = 192
    for seed in range(32):
        run = model.run(
            frequency,
            amplitude,
            seed,
            visits=visits,
            samples=601,
            range_sigma_m=0.25,
            bearing_sigma_deg=0.25,
        )
        f, a, phases = model.components(frequency, amplitude, seed)
        t = run["t"]
        _, attitude, _, _ = model.pose(t, f, a, phases, model.DAMPING)
        target_vector = run["target"] - run["origin"]
        ray = np.einsum("nji,nj->ni", attitude, target_vector)
        rng = np.random.default_rng(model.SEED + 100000 + seed)
        bearing_noise = rng.normal(0, 0.25 * model.RAD, visits)
        bearing = np.arctan2(ray[:, 1], ray[:, 0]) + bearing_noise
        level_bearing = np.arctan2(target_vector[:, 1], target_vector[:, 0]) + bearing_noise
        level_rotation = np.broadcast_to(np.eye(3), attitude.shape)
        slant = run["slant"] + rng.normal(0, 0.25, visits)
        counts = []
        level_counts = []
        for delay in delays:
            origin, rotation, _, _ = model.pose(t - delay, f, a, phases, model.DAMPING)
            xyz = model.inverse_plane(slant, bearing, origin, rotation, run["target"][:, 2])
            error = np.linalg.norm(xyz[:, :2] - run["target"][:, :2], axis=1)
            usable = run["acquired"][0] & (error <= model.TOLERANCE)
            if delay in (0.0, 0.625):
                assert np.array_equal(usable, run["usable"][int(delay == 0.0)])
            counts.append(usable.sum())
            level_xyz = model.inverse_plane(
                slant, level_bearing, origin, level_rotation, run["target"][:, 2]
            )
            level_error = np.linalg.norm(level_xyz[:, :2] - run["target"][:, :2], axis=1)
            level_usable = run["acquired"][2] & (level_error <= model.TOLERANCE)
            if delay == 0:
                assert np.array_equal(level_usable, run["usable"][2])
            level_counts.append(level_usable.sum())
        level_phase_counts.append(level_counts)
        phase_counts.append(counts)
    counts = np.asarray(phase_counts)
    level_counts = np.asarray(level_phase_counts)
    for column, delay in enumerate(delays):
        gain = 100 * (counts[:, 0] - counts[:, column]) / visits
        hardware_first = 100 * (level_counts[:, column] - counts[:, column]) / visits
        hardware_second = 100 * (level_counts[:, 0] - counts[:, 0]) / visits
        interaction = hardware_second - hardware_first
        yield {
            "frequency_hz": frequency,
            "amplitude_m": amplitude,
            "pose_age_s": delay,
            "scheduled_count": counts.shape[0] * visits,
            "usable_count": int(counts[:, column].sum()),
            "exact_pose_gain_pp": gain.mean(),
            "level_usable_count": int(level_counts[:, column].sum()),
            "hardware_first_gain_pp": hardware_first.mean(),
            "hardware_after_timing_gain_pp": hardware_second.mean(),
            "interaction_pp": interaction.mean(),
            "interaction_phase_interval_halfwidth_pp": (
                1.96 * interaction.std(ddof=1) / np.sqrt(len(interaction))
            ),
            "phase_interval_halfwidth_pp": 1.96 * gain.std(ddof=1) / np.sqrt(len(gain)),
        }


def main():
    archive = json.loads(Path("data/experiment-results.json").read_text())
    rows = [
        row
        for cell in archive["operating_map"]
        for row in cell_results(cell["frequency_hz"], cell["amplitude_m"])
    ]
    with Path("data/latency_noise_grid.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
