"""Paired scan-offset and measurement-error sensitivity at the largest map gain."""

import argparse
import csv
from pathlib import Path

import paired_experiment as model


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    rows = []
    for phase in range(32):
        for offset in (-0.49, -0.25, 0.0, 0.25, 0.49):
            for bearing, distance in [(0.0, 0.0), (0.25, 0.25), (1.0, 0.25)]:
                visit = model.run(
                    0.3325,
                    0.432,
                    phase,
                    visits=192,
                    samples=601,
                    scan_offset=offset,
                    bearing_sigma_deg=bearing,
                    range_sigma_m=distance,
                )
                usable = visit["usable"].sum(axis=1)
                if offset == 0:
                    assert usable[0] == usable[1]
                rows.append(
                    {
                        "phase_id": phase,
                        "scan_offset_rotations": offset,
                        "bearing_sigma_deg": bearing,
                        "range_sigma_m": distance,
                        "scheduled_count": len(visit["t"]),
                        "body_acquired_count": int(visit["acquired"][0].sum()),
                        "midpoint_usable": int(usable[0]),
                        "spoke_usable": int(usable[1]),
                        "level_usable": int(usable[2]),
                    }
                )
    with args.output.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
