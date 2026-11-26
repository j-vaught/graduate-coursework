"""Separate timestamp errors in antenna position and attitude on identical acquired echoes."""

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model


def bearing_plane_solution(ranges, bearing, origin, rotation, height):
    """Intersect the horizontal range circle with the plane of measured bearing."""
    up = np.zeros_like(bearing)
    normal = np.column_stack((-np.sin(bearing), np.cos(bearing), up))
    world_normal = np.einsum("nij,nj->ni", rotation, normal)
    horizontal_norm = np.linalg.norm(world_normal[:, :2], axis=1)
    axis = world_normal[:, :2] / horizontal_norm[:, None]
    perpendicular = np.column_stack((axis[:, 1], -axis[:, 0]))
    dz = height - origin[:, 2]
    along = -world_normal[:, 2] * dz / horizontal_norm
    across = np.sqrt(ranges**2 - dz**2 - along**2)
    # With an upward antenna vertical and a near-horizontal forward ray, the
    # positive root selects the measured azimuth (the other is behind the antenna).
    return origin[:, :2] + along[:, None] * axis + across[:, None] * perpendicular


def compare(frequency, amplitude, phase):
    f, a, p = model.components(frequency, amplitude, phase)
    visit = model.run(frequency, amplitude, phase, visits=192, samples=601)
    t = visit["t"]
    spoke_origin, spoke_rotation, _, _ = model.pose(t, f, a, p, model.DAMPING)
    mid_origin, mid_rotation, _, _ = model.pose(t - model.PERIOD / 4, f, a, p, model.DAMPING)
    direction = np.einsum("nji,nj->ni", spoke_rotation, visit["target"] - spoke_origin)
    bearing = np.arctan2(direction[:, 1], direction[:, 0])
    rows = []
    for origin_name, origin in [("midpoint", mid_origin), ("spoke", spoke_origin)]:
        for rotation_name, rotation in [("midpoint", mid_rotation), ("spoke", spoke_rotation)]:
            mapped = model.inverse_plane(
                visit["slant"], bearing, origin, rotation, visit["target"][:, 2]
            )
            alternate = bearing_plane_solution(
                visit["slant"], bearing, origin, rotation, visit["target"][:, 2]
            )
            discrepancy = np.linalg.norm(mapped[:, :2] - alternate, axis=1)
            assert discrepancy.max() < 1e-10
            error = np.linalg.norm(mapped[:, :2] - visit["target"][:, :2], axis=1)
            usable = visit["acquired"][0] & (error <= model.TOLERANCE)
            if origin_name == rotation_name:
                np.testing.assert_array_equal(usable, visit["usable"][int(origin_name == "spoke")])
            rows.append(
                {
                    "frequency_hz": frequency,
                    "amplitude_m": amplitude,
                    "phase_id": phase,
                    "origin_time": origin_name,
                    "attitude_time": rotation_name,
                    "scheduled_count": len(t),
                    "acquired_count": int(visit["acquired"][0].sum()),
                    "usable_count": int(usable.sum()),
                    "max_solver_discrepancy_m": float(discrepancy.max()),
                }
            )
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for frequency, amplitude in [(0.35, 0.15), (0.3325, 0.432), (0.35, 0.36)]:
        for phase in range(32):
            rows.extend(compare(frequency, amplitude, phase))
    with args.output.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
