"""Compare propagation assumptions and elevation policies on matched scheduled visits."""

import argparse
import csv
from pathlib import Path

import numpy as np
from scipy.special import ndtr

import paired_experiment as model


def evaluate(frequency, amplitude, phase):
    visit = model.run(frequency, amplitude, phase, visits=192, samples=601)
    scale = 80 * np.log10(2) / model.BETA**2
    diffraction_margin = visit["margin_level"] + scale * visit["level_angle"] ** 2
    clear = visit["surface_clearance"] >= 0
    nominal_elevation = np.arctan2(
        model.TARGET_HEIGHT - model.RADAR_HEIGHT, model.RANGE - model.LEVER[0]
    )
    angles = {
        "body": visit["body_angle"],
        "level": visit["level_angle"],
        "nominal_depression": visit["level_angle"] - nominal_elevation,
        "zero_pointing_loss": np.zeros_like(clear, dtype=float),
    }
    rows = []
    for law, headroom in [
        ("diffraction", diffraction_margin),
        ("geometric_visibility", np.where(clear, model.MARGIN, -np.inf)),
        ("unattenuated", np.full_like(diffraction_margin, model.MARGIN)),
    ]:
        for policy, elevation in angles.items():
            margin = headroom - scale * elevation**2
            acquired = margin >= 0
            if law == "diffraction" and policy in ("body", "level"):
                np.testing.assert_array_equal(
                    acquired, visit["acquired"][0 if policy == "body" else 2]
                )
            rows.append(
                {
                    "frequency_hz": frequency,
                    "amplitude_m": amplitude,
                    "phase_id": phase,
                    "path_law": law,
                    "elevation_policy": policy,
                    "acquired": int(acquired.sum()),
                    "scheduled": len(acquired),
                    "mean_probability_1db": float(ndtr(margin).mean()),
                    "mean_probability_3db": float(ndtr(margin / 3).mean()),
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
            rows.extend(evaluate(frequency, amplitude, phase))
    with args.output.open("w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
