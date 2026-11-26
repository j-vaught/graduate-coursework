"""Pair long-crested and directional waves with the same elevation spectrum."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model
from clock_policy import longest_update_gaps, p95

RATIOS = np.array([0.72, 0.83, 0.92, 1.0, 1.08, 1.18, 1.29])
WEIGHTS = np.array([0.07, 0.125, 0.19, 0.23, 0.19, 0.125, 0.07])
SPREAD = model.RAD * np.array([-40, 27, -15, 0, 15, -27, 40])
HEADINGS = {"long_crested": np.full(len(RATIOS), model.HEADING), "spread": model.HEADING + SPREAD}
CASES = {"reference": (0.3500, 0.150), "largest_linear_gain": (0.3325, 0.432)}
RECORDS = 64
TIMES = model.PERIOD * (np.arange(192) + 0.25)


class DirectionalSea:
    """Apply each component direction to wave geometry and modal forcing."""

    def __init__(self, headings):
        self.cos_heading = np.cos(headings)
        self.sin_heading = np.sin(headings)

    def wave(self, x, y, t, frequencies, amplitudes, phases):
        x, y, t = np.broadcast_arrays(x, y, t)
        omega = 2 * np.pi * frequencies
        k = omega**2 / model.G
        spatial_phase = (k * self.cos_heading)[:, None] * x.ravel()[None, :] + (
            k * self.sin_heading
        )[:, None] * y.ravel()[None, :]
        angle = spatial_phase - omega[:, None] * t.ravel()[None, :] + phases[:, None]
        return np.sum(amplitudes[:, None] * np.cos(angle), axis=0).reshape(x.shape)

    def rotational_amplitudes(self, frequencies, amplitudes, damping):
        k = (2 * np.pi * frequencies) ** 2 / model.G
        slope_response = (
            model.HULL_PITCH_GAIN
            * k
            * amplitudes
            * model.transfer(frequencies, model.NATURAL, damping)
        )
        pitch = 1j * self.cos_heading * slope_response
        roll = 0.6 * self.sin_heading * np.exp(1j * np.pi / 3) * slope_response
        return pitch, roll

    def pose(self, t, frequencies, amplitudes, phases, damping, pitch_phase=0.0, **_):
        phase = np.exp(1j * (2 * np.pi * frequencies[:, None] * t - phases[:, None]))
        pitch_amplitudes, roll_amplitudes = self.rotational_amplitudes(
            frequencies, amplitudes, damping
        )
        heave_amplitudes = amplitudes * model.transfer(frequencies, 0.8, 0.3)
        surge_amplitudes = 1j * self.cos_heading * amplitudes
        pitch = np.real((pitch_amplitudes * np.exp(1j * pitch_phase)) @ phase)
        roll = np.real(roll_amplitudes @ phase)
        heave = np.real(heave_amplitudes @ phase)
        surge = np.real(surge_amplitudes @ phase)
        rotation = model.rotation(pitch, roll)
        center = np.column_stack(
            (surge, np.zeros_like(t), model.RADAR_HEIGHT - model.LEVER[2] + heave)
        )
        origin = center + rotation @ model.LEVER
        return origin, rotation, pitch, roll


def run_case(name, carrier, nominal_amplitude, ray_samples):
    frequencies = carrier * RATIOS
    amplitudes = nominal_amplitude * np.sqrt(WEIGHTS)
    nominal_slope_bound = float((2 * np.pi * frequencies) ** 2 @ amplitudes / model.G)
    seas = {label: DirectionalSea(headings) for label, headings in HEADINGS.items()}
    nominal_angles = {
        label: tuple(
            float(np.sum(np.abs(values)) / model.RAD)
            for values in sea.rotational_amplitudes(frequencies, amplitudes, model.DAMPING)
        )
        for label, sea in seas.items()
    }
    scale = min(
        1.0,
        model.MAX_STEEPNESS / nominal_slope_bound,
        model.MAX_ANGLE_DEG / max(max(bounds) for bounds in nominal_angles.values()),
    )
    amplitudes *= scale
    rng = np.random.default_rng(model.SEED + 500_000)
    rows = []
    for record, phases in enumerate(rng.uniform(0, 2 * np.pi, (RECORDS, len(RATIOS)))):

        def components(*_, phases=phases):
            return frequencies, amplitudes, phases

        for label, sea in seas.items():
            result = model.run(
                carrier,
                nominal_amplitude,
                record,
                times=TIMES,
                samples=ray_samples,
                component_model=components,
                surface_model=sea.wave,
                pose_model=sea.pose,
            )
            usable = result["usable"]
            counts = usable.sum(axis=1)
            gaps = longest_update_gaps(TIMES, usable)
            rows.append(
                {
                    "case": name,
                    "sea": label,
                    "carrier_hz": carrier,
                    "nominal_regular_amplitude_m": nominal_amplitude,
                    "regular_equivalent_amplitude_m": nominal_amplitude * scale,
                    "surface_rms_m": nominal_amplitude * scale / np.sqrt(2),
                    "scale_to_limits": scale,
                    "nominal_slope_bound": nominal_slope_bound,
                    "slope_bound": scale * nominal_slope_bound,
                    "pitch_bound_deg": scale * nominal_angles[label][0],
                    "roll_bound_deg": scale * nominal_angles[label][1],
                    "record": record,
                    "visits": len(TIMES),
                    "midpoint_usable": counts[0],
                    "spoke_usable": counts[1],
                    "level_usable": counts[2],
                    "midpoint_longest_gap_s": gaps[0],
                    "spoke_longest_gap_s": gaps[1],
                    "level_longest_gap_s": gaps[2],
                }
            )
    return rows


def verify_long_crested():
    sea = DirectionalSea(HEADINGS["long_crested"])
    frequencies = CASES["reference"][0] * RATIOS
    amplitudes = CASES["reference"][1] * np.sqrt(WEIGHTS)
    phases = np.linspace(0, 2 * np.pi, len(RATIOS), endpoint=False)
    t = TIMES[:7]
    np.testing.assert_allclose(
        sea.wave(t, 0, t, frequencies, amplitudes, phases),
        model.wave(t, 0, t, frequencies, amplitudes, phases),
        atol=1e-14,
    )
    for reproduced, production in zip(
        sea.pose(t, frequencies, amplitudes, phases, model.DAMPING),
        model.pose(t, frequencies, amplitudes, phases, model.DAMPING),
        strict=True,
    ):
        np.testing.assert_allclose(reproduced, production, atol=1e-14)


def summarize(rows):
    for name in CASES:
        gains = {}
        for label in HEADINGS:
            subset = [row for row in rows if row["case"] == name and row["sea"] == label]
            counts = np.array(
                [[row[f"{key}_usable"] for key in ("midpoint", "spoke", "level")] for row in subset]
            )
            fractions = counts / len(TIMES)
            gains[label] = 100 * np.diff(fractions, axis=1)
            gaps = [
                p95([row[f"{key}_longest_gap_s"] for row in subset])
                for key in ("midpoint", "spoke", "level")
            ]
            print(
                f"{name} {label}: a_eq={subset[0]['regular_equivalent_amplitude_m']:.4f} m, "
                f"slope<={subset[0]['slope_bound']:.4f}, "
                f"pitch<={subset[0]['pitch_bound_deg']:.3f} deg, "
                f"roll<={subset[0]['roll_bound_deg']:.3f} deg, "
                f"usable (%)={100 * fractions.mean(axis=0)}, "
                f"registration/pointing gains (pp)={gains[label].mean(axis=0)}, "
                f"gaps (s)={gaps}"
            )
        paired = gains["spread"] - gains["long_crested"]
        print(
            f"{name}: paired gain changes (pp)={paired.mean(axis=0)} "
            f"+/- {1.96 * paired.std(axis=0, ddof=1) / np.sqrt(RECORDS)}"
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--ray-samples", type=int, default=601)
    args = parser.parse_args()
    verify_long_crested()
    rows = []
    for case, (frequency, amplitude) in CASES.items():
        rows.extend(run_case(case, frequency, amplitude, args.ray_samples))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summarize(rows)


if __name__ == "__main__":
    main()
