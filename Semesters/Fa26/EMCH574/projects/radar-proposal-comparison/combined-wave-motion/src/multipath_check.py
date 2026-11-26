"""Test sensitivity to a bounded complex reflection on the same radar visits.

The one-way direct and specular fields sum at an isotropic scatterer. A
reciprocal monostatic channel squares this field for the received voltage,
so received power follows the fourth power of the one-way field magnitude.
See Galati et al., doi:10.3390/s20020463, Eq. (4) and Appendix A.
"""

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model
from pointing_registration_factorial import ARMS, level_mapping_errors, matched_changes

CASES = (("reference", 0.350, 0.150), ("largest_interaction", 0.36125, 0.376))
PHASES = 32
VISITS = 192
MAGNITUDE_STEPS = 20
PHASE_STEP_DEG = 5


def elevation(vector):
    return np.arctan2(vector[:, 2], np.hypot(vector[:, 0], vector[:, 1]))


def antenna_field(angle):
    """Square root of the one-way normalized Gaussian antenna power."""
    return np.exp2(-2 * (angle / model.BETA) ** 2)


def power(direct, reflected, reflection):
    """Monostatic received power relative to the direct boresight return."""
    return np.abs(direct + reflection * reflected) ** 4


def flat_paths(run):
    origin = run["origin"]
    buoy = run["target"]
    sea_plane = buoy[:, 2] - model.TARGET_HEIGHT
    antenna_height = origin[:, 2] - sea_plane
    assert np.all(antenna_height > 0) and model.TARGET_HEIGHT > 0
    image = buoy.copy()
    image[:, 2] = 2 * sea_plane - buoy[:, 2]
    reflected_vector = image - origin
    reflected_range = np.linalg.norm(reflected_vector, axis=1)
    direct_range = run["slant"]
    path_difference = reflected_range - direct_range
    assert np.all(path_difference > 0)

    # Confirm the image ray hits the reference plane and reproduces its
    # specular path length via a second calculation of the two legs.
    fraction = antenna_height / (antenna_height + model.TARGET_HEIGHT)
    specular_point = origin + fraction[:, None] * reflected_vector
    np.testing.assert_allclose(specular_point[:, 2], sea_plane, atol=1e-13, rtol=0)
    two_legs = np.linalg.norm(specular_point - origin, axis=1)
    two_legs += np.linalg.norm(buoy - specular_point, axis=1)
    np.testing.assert_allclose(two_legs, reflected_range, atol=5e-13, rtol=0)

    body_rotation = model.rotation(run["pitch"], run["roll"])
    reflected_body = np.einsum("nji,nj->ni", body_rotation, reflected_vector)
    direct_angles = np.array([run["body_angle"], run["level_angle"]])
    reflected_angles = np.array([elevation(reflected_body), elevation(reflected_vector)])
    propagation = (
        direct_range / reflected_range * np.exp(-2j * np.pi * path_difference / model.WAVELENGTH)
    )
    direct = antenna_field(direct_angles)
    reflected = antenna_field(reflected_angles) * propagation
    direct_only_margin = model.MARGIN - 80.0 * np.log10(2) * (direct_angles / model.BETA) ** 2
    np.testing.assert_allclose(
        model.MARGIN + 10 * np.log10(power(direct, reflected, 0)),
        direct_only_margin,
        atol=1e-12,
        rtol=0,
    )
    return direct, reflected, reflected_angles, path_difference, direct_only_margin >= 0


def fields(frequency, amplitude):
    direct_fields, reflected_fields, mapping_passes, direct_gates = [], [], [], []
    reflected_angles, differences = [], []
    for phase in range(PHASES):
        result = model.run(frequency, amplitude, phase, visits=VISITS, samples=601)
        direct, reflected, angles, difference, direct_gate = flat_paths(result)
        level_midpoint = level_mapping_errors(result, phase, {})
        errors = np.insert(result["errors"], 2, level_midpoint, axis=0)
        direct_fields.append(direct)
        reflected_fields.append(reflected)
        mapping_passes.append(errors <= model.TOLERANCE)
        direct_gates.append(direct_gate)
        reflected_angles.append(angles)
        differences.append(difference)

    return (
        np.concatenate(direct_fields, axis=1),
        np.concatenate(reflected_fields, axis=1),
        np.concatenate(mapping_passes, axis=1),
        np.concatenate(direct_gates, axis=1),
        np.concatenate(reflected_angles, axis=1),
        np.concatenate(differences),
    )


def reflection_grid():
    yield 0.0, 0
    for magnitude in np.linspace(0, 1, MAGNITUDE_STEPS + 1)[1:]:
        for phase in range(0, 360, PHASE_STEP_DEG):
            yield float(magnitude), phase


def evaluate(name, frequency, amplitude):
    direct, reflected, position_pass, direct_gate, angles, path_delta = fields(frequency, amplitude)
    threshold = 10 ** (-model.MARGIN / 10)
    scheduled = PHASES * VISITS
    for magnitude, phase in reflection_grid():
        reflection = magnitude * np.exp(1j * phase * model.RAD)
        acquired = power(direct, reflected, reflection) >= threshold
        if magnitude == 0:
            np.testing.assert_array_equal(acquired, direct_gate)
        acquired = acquired[[0, 0, 1, 1]]
        usable = acquired & position_pass
        count = usable.sum(axis=1)
        row = {
            "case": name,
            "wave_hz": frequency,
            "wave_amplitude_m": amplitude,
            "reflection_magnitude": magnitude,
            "reflection_phase_deg": phase,
            "scheduled_visits": scheduled,
            "min_one_way_path_difference_m": float(np.min(path_delta)),
            "max_one_way_path_difference_m": float(np.max(path_delta)),
            "min_reflected_departure_body_deg": float(np.min(angles[0]) / model.RAD),
            "max_reflected_departure_body_deg": float(np.max(angles[0]) / model.RAD),
            "min_reflected_departure_level_deg": float(np.min(angles[1]) / model.RAD),
            "max_reflected_departure_level_deg": float(np.max(angles[1]) / model.RAD),
        }
        for name_arm, acquired_count, usable_count in zip(
            ARMS, acquired.sum(axis=1), count, strict=True
        ):
            row[f"{name_arm}_acquired"] = int(acquired_count)
            row[f"{name_arm}_usable"] = int(usable_count)
        for contrast, after, before in (
            ("registration_body", 1, 0),
            ("registration_level", 3, 2),
            ("level_midpoint", 2, 0),
            ("level_spoke", 3, 1),
        ):
            wins, losses = matched_changes(usable[before], usable[after])
            row[f"{contrast}_wins"] = wins
            row[f"{contrast}_losses"] = losses
            row[f"{contrast}_pp"] = (wins - losses) * 100 / scheduled
        row["interaction_pp"] = (count[3] - count[2] - count[1] + count[0]) * 100 / scheduled
        yield row


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    np.testing.assert_allclose(power(1, 1, np.array([0, 1, -1, 1j])), [1, 16, 0, 4])
    rows = [row for case in CASES for row in evaluate(*case)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(
        f"Verified direct-only limits and wrote {len(rows)} reflection settings to {args.output}."
    )


if __name__ == "__main__":
    main()
