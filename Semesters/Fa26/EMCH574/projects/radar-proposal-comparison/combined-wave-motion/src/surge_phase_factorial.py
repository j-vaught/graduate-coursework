"""Evaluate the four retrofit arms under both prescribed signs of longitudinal surge."""

import csv
from functools import partial
from pathlib import Path

from hull_kinematics import stressed_pose
from pointing_registration_factorial import WaveCase, summarize


def main():
    rows = []
    for frequency, amplitude in [(0.35, 0.15), (0.3325, 0.432), (0.36125, 0.376)]:
        for surge in [1, 0, -1]:
            pose = partial(stressed_pose, surge_gain=surge, roll_gain=1, yaw_deg=0)
            case = WaveCase(f"surge_{surge}", frequency, amplitude, {"pose_model": pose})
            rows.append(summarize(case))
    with Path("data/surge_phase_factorial.csv").open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
