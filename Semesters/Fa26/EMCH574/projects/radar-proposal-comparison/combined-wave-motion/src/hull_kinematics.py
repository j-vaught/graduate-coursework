"""Change surge, roll, and yaw assumptions one at a time in the strongest linear cell."""

import argparse
import csv
from functools import partial
from pathlib import Path

import numpy as np

import paired_experiment as model


def stressed_pose(
    t, f, a, p, damping, pitch_phase, *, pitch_response, surge_gain, roll_gain, yaw_deg
):
    origin, rotation, pitch, roll = model.pose(
        t, f, a, p, damping, pitch_phase, pitch_response=pitch_response
    )
    reference = origin - rotation @ model.LEVER
    reference[:, 0] *= surge_gain
    rotation = model.rotation(pitch, roll_gain * roll)
    yaw = np.deg2rad(yaw_deg) * np.sin(2 * np.pi * f[0] * t - p[0])
    cosine, sine = np.cos(yaw), np.sin(yaw)
    body_x, body_y = rotation[:, 0].copy(), rotation[:, 1].copy()
    rotation[:, 0] = cosine[:, None] * body_x - sine[:, None] * body_y
    rotation[:, 1] = sine[:, None] * body_x + cosine[:, None] * body_y
    return reference + rotation @ model.LEVER, rotation, pitch, roll_gain * roll


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = []
    for phase in range(32):
        baseline = model.run(0.3325, 0.432, phase, visits=192, samples=601)
        for name, surge, roll, yaw in [
            ("baseline", 1, 1, 0),
            ("half_surge", 0.5, 1, 0),
            ("zero_surge", 0, 1, 0),
            ("reversed_surge", -1, 1, 0),
            ("zero_roll", 1, 0, 0),
            ("yaw_0.5deg", 1, 1, 0.5),
            ("yaw_1deg", 1, 1, 1),
        ]:
            pose = partial(stressed_pose, surge_gain=surge, roll_gain=roll, yaw_deg=yaw)
            visit = model.run(0.3325, 0.432, phase, visits=192, samples=601, pose_model=pose)
            if name == "baseline":
                np.testing.assert_array_equal(visit["usable"], baseline["usable"])
            counts = visit["usable"].sum(axis=1)
            rows.append(
                {
                    "phase_id": phase,
                    "assumption": name,
                    "surge_gain": surge,
                    "roll_gain": roll,
                    "yaw_amplitude_deg": yaw,
                    "scheduled_count": len(visit["t"]),
                    "midpoint_usable": int(counts[0]),
                    "spoke_usable": int(counts[1]),
                    "level_usable": int(counts[2]),
                }
            )
    with args.output.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
