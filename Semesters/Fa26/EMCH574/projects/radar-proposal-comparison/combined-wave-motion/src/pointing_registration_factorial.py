"""Cross antenna pointing and registration timing on the original paired visits."""

import argparse
import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

import paired_experiment as model
from crest_sensitivity import stokes_surface
from nonlinear_pitch import integrate_pitch

PHASE_COUNT = 32
VISIT_COUNT = 192
PATH_SUBDIVISIONS = 601
ARMS = ("body_midpoint", "body_spoke", "level_midpoint", "level_spoke")
CONTRASTS = {
    "register_body": (1, 0),
    "register_level": (3, 2),
    "level_midpoint": (2, 0),
    "level_spoke": (3, 1),
}


@dataclass(frozen=True)
class WaveCase:
    name: str
    frequency_hz: float
    amplitude_m: float
    options: dict = field(default_factory=dict)
    baseline: dict | None = None
    direct_ray: bool = False


def level_mapping_errors(run, phase, options):
    """A continuously level mount has the same axes at both timestamps."""
    rng = np.random.default_rng(model.SEED + 100000 + phase)
    bearing_noise = rng.normal(0, options.get("bearing_sigma_deg", 0.0) * model.RAD, VISIT_COUNT)
    range_noise = rng.normal(0, options.get("range_sigma_m", 0.0), VISIT_COUNT)
    height_noise = rng.normal(0, options.get("height_sigma_m", 0.0), VISIT_COUNT)
    target = run["target"]
    offset = target - run["origin"]
    azimuth = np.arctan2(offset[:, 1], offset[:, 0]) + bearing_noise
    measured_range = run["slant"] + range_noise
    height = target[:, 2] + height_noise
    direction = np.column_stack((np.cos(azimuth), np.sin(azimuth)))

    errors = []
    for origin in (run["midpoint"], run["origin"]):
        # With fixed horizontal axes, the reconstructed horizontal range is
        # the leg of a right triangle given slant range and height difference.
        squared_range = measured_range**2 - (height - origin[:, 2]) ** 2
        horizontal_range = np.sqrt(np.where(squared_range >= 0, squared_range, np.nan))
        position = origin[:, :2] + horizontal_range[:, None] * direction
        errors.append(np.linalg.norm(position - target[:, :2], axis=1))
    np.testing.assert_allclose(errors[1], run["errors"][2], atol=5e-13, rtol=0)
    return errors[0]


def paired_visits(case):
    acquisitions = []
    visits = []
    for phase in range(PHASE_COUNT):
        run = model.run(
            case.frequency_hz,
            case.amplitude_m,
            phase,
            visits=VISIT_COUNT,
            samples=PATH_SUBDIVISIONS,
            **case.options,
        )
        level_midpoint_error = level_mapping_errors(run, phase, case.options)
        errors = np.insert(run["errors"], 2, level_midpoint_error, axis=0)
        acquired = run["acquired"][[0, 1, 2, 2]]
        if case.direct_ray:
            beam_loss = (
                80
                * np.log10(2)
                * (np.array([run["body_angle"], run["level_angle"]]) / model.BETA) ** 2
            )
            acquired = (run["surface_clearance"] >= 0) & (beam_loss <= model.MARGIN)
            acquired = acquired[[0, 0, 1, 1]]
        usable = acquired & (errors <= case.options.get("tol", model.TOLERANCE))
        if not case.direct_ray:
            np.testing.assert_array_equal(usable[[0, 1, 3]], run["usable"])
        if case.baseline is not None:
            saved = case.baseline["realizations"][phase]
            assert saved["visits"] == VISIT_COUNT
            np.testing.assert_array_equal(acquired[[0, 1, 3]].sum(axis=1), saved["acquired_count"])
            np.testing.assert_array_equal(usable[[0, 1, 3]].sum(axis=1), saved["usable_count"])
        acquisitions.append(acquired)
        visits.append(usable)
    return np.array(acquisitions), np.array(visits)


def matched_changes(before, after):
    wins = int(np.count_nonzero(after & ~before))
    losses = int(np.count_nonzero(before & ~after))
    return wins, losses


def summarize(case):
    acquired, usable = paired_visits(case)
    scheduled = PHASE_COUNT * VISIT_COUNT
    acquired_counts = acquired.sum(axis=(0, 2))
    usable_counts = usable.sum(axis=(0, 2))
    pct = 100 / scheduled
    row = {
        "case": case.name,
        "frequency_hz": case.frequency_hz,
        "amplitude_m": case.amplitude_m,
        "scheduled": scheduled,
        "saved_three_arms_verified": case.baseline is not None,
    }
    for arm, acq, use in zip(ARMS, acquired_counts, usable_counts, strict=True):
        row[f"{arm}_acquired"] = int(acq)
        row[f"{arm}_usable"] = int(use)

    acquisition_wins, acquisition_losses = matched_changes(acquired[:, 0], acquired[:, 2])
    row.update(
        pointing_acquisition_wins=acquisition_wins, pointing_acquisition_losses=acquisition_losses
    )
    phase_counts = usable.sum(axis=2)
    gains = {}
    for name, (after, before) in CONTRASTS.items():
        wins, losses = matched_changes(usable[:, before], usable[:, after])
        gains[name] = wins - losses
        assert gains[name] == usable_counts[after] - usable_counts[before]
        row[f"{name}_wins"] = wins
        row[f"{name}_losses"] = losses
        row[f"{name}_pp"] = gains[name] * pct

        if name.startswith("level_"):
            acquired_wins = int(np.count_nonzero(usable[:, after] & ~acquired[:, before]))
            acquired_losses = int(np.count_nonzero(usable[:, before] & ~acquired[:, after]))
            row[f"{name}_wins_from_acquisition"] = acquired_wins
            row[f"{name}_losses_from_acquisition"] = acquired_losses
            row[f"{name}_wins_from_mapping"] = wins - acquired_wins
            row[f"{name}_losses_from_mapping"] = losses - acquired_losses

    row["registration_main_pp"] = (gains["register_body"] + gains["register_level"]) * pct / 2
    row["pointing_main_pp"] = (gains["level_midpoint"] + gains["level_spoke"]) * pct / 2
    interaction = phase_counts[:, 3] - phase_counts[:, 2] - phase_counts[:, 1] + phase_counts[:, 0]
    row["interaction_pp"] = int(interaction.sum()) * pct
    row["interaction_ci95_halfwidth_pp"] = (
        1.96 * float(np.std(interaction, ddof=1)) / np.sqrt(PHASE_COUNT) * 100 / VISIT_COUNT
    )
    # A zero gain indicates no reason to make a stand-alone change on this metric.
    row["standalone_choice"] = winning_intervention(gains["register_body"], gains["level_midpoint"])
    row["sequential_gain_choice"] = winning_intervention(
        gains["register_body"], gains["level_spoke"]
    )
    return row


def winning_intervention(register, level):
    if max(register, level) <= 0:
        return "neither"
    if register == level:
        return "tie"
    return "register" if register > level else "level"


def wave_cases(saved):
    for cell in saved["operating_map"]:
        yield WaveCase("grid", cell["frequency_hz"], cell["amplitude_m"], baseline=cell)

    reference_options = {
        "reference": {},
        "margin_5dB": {"margin": 5},
        "margin_15dB": {"margin": 15},
        "irregular": {"irregular": True},
        "measurement_noise_idealized": {"bearing_sigma_deg": 0.25, "range_sigma_m": 0.25},
    }
    for name, options in reference_options.items():
        baseline = next(cell for cell in saved["sensitivity"] if cell["name"] == name)
        yield WaveCase(name, 0.35, 0.15, options, baseline)

    yield WaveCase("reference_direct_ray", 0.35, 0.15, direct_ray=True)
    yield WaveCase("reference_stokes", 0.35, 0.15, {"surface_model": stokes_surface})
    yield WaveCase("neighbor_negative_pointing", 0.355, 0.155)
    for bearing_noise in (0.25, 1.0):
        yield WaveCase(
            f"maximum_registration_noise_{bearing_noise:g}deg",
            0.3325,
            0.432,
            {"bearing_sigma_deg": bearing_noise, "range_sigma_m": 0.25},
        )
    yield WaveCase("maximum_registration_direct_ray", 0.3325, 0.432, direct_ray=True)
    yield WaveCase("maximum_registration_stokes", 0.3325, 0.432, {"surface_model": stokes_surface})
    pitch, _ = integrate_pitch(0.3325, 0.432, 0.5, spinup=60, steps_per_period=128)
    yield WaveCase("maximum_registration_quadratic", 0.3325, 0.432, {"pitch_response": pitch})
    yield WaveCase("maximum_registration_broadside", 0.3325, 0.432, {"target_azimuth_deg": 90})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=Path("data/experiment-results.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    saved = json.loads(args.baseline.read_text())
    assert len(saved["operating_map"]) == 111
    rows = [summarize(case) for case in wave_cases(saved)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    grid = [row for row in rows if row["case"] == "grid"]
    changes = sum(row["standalone_choice"] != row["sequential_gain_choice"] for row in grid)
    print(f"Verified the original classifications for all {len(grid)} grid cells.")
    print(f"First-intervention choices changed in {changes} grid cells.")
    print(f"Wrote {len(rows)} cases to {args.output}.")


if __name__ == "__main__":
    main()
