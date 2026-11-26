"""Refine the ray grid at the two reported negative leveling-gain cases."""

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model

PATH_SUBDIVISIONS = (601, 1201, 2401, 4801)
PHASES = 32
VISITS = 192


def summarize_case(frequency, amplitude):
    grids = {}
    for subdivisions in PATH_SUBDIVISIONS:
        runs = [
            model.run(frequency, amplitude, phase, visits=VISITS, samples=subdivisions)
            for phase in range(PHASES)
        ]
        body_margin = np.stack([run["margin_motion"] for run in runs])
        level_margin = np.stack([run["margin_level"] for run in runs])
        body_angle = np.stack([run["body_angle"] for run in runs])
        body_beam_loss = 80 * np.log10(2) * (body_angle / model.BETA) ** 2
        diffraction = model.MARGIN - body_beam_loss - body_margin
        acquired = np.stack([run["acquired"] for run in runs], axis=1)
        usable = np.stack([run["usable"] for run in runs], axis=1)
        grids[subdivisions] = body_margin, level_margin, diffraction, acquired, usable

    finest = PATH_SUBDIVISIONS[-1]
    _, _, reference_loss, reference_acquired, reference_usable = grids[finest]
    rows = []
    for subdivisions, (body_margin, level_margin, loss, acquired, usable) in grids.items():
        lost = acquired[1] & ~acquired[2]
        gained = acquired[2] & ~acquired[1]
        gain_by_phase = (usable[2].mean(axis=1) - usable[1].mean(axis=1)) * 100
        loss_p50, loss_p95, loss_p99 = np.percentile(loss, (50, 95, 99))
        margin_delta = np.abs(loss - reference_loss)
        delta_p50, delta_p95, delta_p99 = np.percentile(margin_delta, (50, 95, 99))
        rows.append(
            {
                "frequency_hz": frequency,
                "amplitude_m": amplitude,
                "phases": PHASES,
                "visits_per_phase": VISITS,
                "path_subdivisions": subdivisions,
                "reference_path_subdivisions": finest,
                "body_acquired": np.count_nonzero(acquired[1]),
                "level_acquired": np.count_nonzero(acquired[2]),
                "body_usable": np.count_nonzero(usable[1]),
                "level_usable": np.count_nonzero(usable[2]),
                "visits_lost_by_leveling": np.count_nonzero(lost),
                "visits_gained_by_leveling": np.count_nonzero(gained),
                "level_usable_gain_pp": gain_by_phase.mean(),
                "level_usable_gain_ci95_halfwidth_pp": 1.96
                * gain_by_phase.std(ddof=1)
                / np.sqrt(PHASES),
                "body_acquisition_flips_vs_finest": np.count_nonzero(
                    acquired[1] != reference_acquired[1]
                ),
                "level_acquisition_flips_vs_finest": np.count_nonzero(
                    acquired[2] != reference_acquired[2]
                ),
                "midpoint_usable_flips_vs_finest": np.count_nonzero(
                    usable[0] != reference_usable[0]
                ),
                "body_usable_flips_vs_finest": np.count_nonzero(usable[1] != reference_usable[1]),
                "level_usable_flips_vs_finest": np.count_nonzero(usable[2] != reference_usable[2]),
                "two_way_diffraction_loss_p50_db": loss_p50,
                "two_way_diffraction_loss_p95_db": loss_p95,
                "two_way_diffraction_loss_p99_db": loss_p99,
                "abs_power_margin_change_vs_finest_p50_db": delta_p50,
                "abs_power_margin_change_vs_finest_p95_db": delta_p95,
                "abs_power_margin_change_vs_finest_p99_db": delta_p99,
                "abs_power_margin_change_vs_finest_max_db": margin_delta.max(),
                "lost_visit_body_margin_min_db": np.min(body_margin[lost], initial=np.inf),
                "lost_visit_body_margin_max_db": np.max(body_margin[lost], initial=-np.inf),
                "lost_visit_level_margin_min_db": np.min(level_margin[lost], initial=np.inf),
                "lost_visit_level_margin_max_db": np.max(level_margin[lost], initial=-np.inf),
            }
        )
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = summarize_case(0.4475, 0.152) + summarize_case(0.355, 0.155)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} case-resolution comparisons to {args.output}")


if __name__ == "__main__":
    main()
