"""Reproduce the three-by-three neighborhood around the nominal reference.

Run on a COMECH or COCESR host with NumPy installed.
"""

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    rows = []
    for frequency in (0.345, 0.350, 0.355):
        for amplitude in (0.145, 0.150, 0.155):
            wave_number = (2 * np.pi * frequency) ** 2 / model.G
            pitch_amplitude = (
                model.HULL_PITCH_GAIN
                * wave_number
                * amplitude
                * np.cos(model.HEADING)
                * abs(model.transfer(np.array([frequency]), model.NATURAL, model.DAMPING)[0])
            )
            assert wave_number * amplitude <= model.MAX_STEEPNESS
            assert pitch_amplitude / model.RAD <= model.MAX_ANGLE_DEG

            realizations = [
                model.run(frequency, amplitude, phase, visits=192, samples=601)
                for phase in range(32)
            ]
            result = model.summarize(realizations)
            rows.append(
                {
                    "frequency_hz": frequency,
                    "amplitude_m": amplitude,
                    "wave_steepness": float(wave_number * amplitude),
                    "peak_pitch_deg": float(pitch_amplitude / model.RAD),
                    "midpoint_fraction": result["fraction"][0],
                    "spoke_fraction": result["fraction"][1],
                    "stabilized_fraction": result["fraction"][2],
                    "correction_gain": result["correction_gain"],
                    "correction_ci95_halfwidth": result["correction_ci95_halfwidth"],
                    "stabilization_gain": result["stabilization_gain"],
                    "stabilization_ci95_halfwidth": result["stabilization_ci95_halfwidth"],
                    "phases": 32,
                    "visits_per_phase": 192,
                    "path_samples": 601,
                }
            )

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} cases to {output}")


if __name__ == "__main__":
    main()
