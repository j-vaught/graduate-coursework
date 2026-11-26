"""Compare effective-edge and crest-based propagation on the same radar visits.

The Deygout construction follows NTIA TR-26-580, Section 3.3.3 and Appendix C.
The crest model represents each distinct regular-wave maximum by one edge.
"""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

import paired_experiment as model
from pointing_registration_factorial import level_mapping_errors

PHASE_COUNT = 32
VISITS = 192
PATH_SUBDIVISIONS = 601
METHODS = ("effective_single_edge", "crest_single_edge", "crest_deygout")
CASES = (("reference", 0.350, 0.150), ("largest_registration_gain", 0.3325, 0.432))
SPARSE_FREQUENCIES = (0.160, 0.275, 0.390, 0.505, 0.620)
SPARSE_AMPLITUDES = (0.040, 0.208, 0.376, 0.544)


def knife_loss(nu):
    if nu <= -0.78:
        return 0.0
    return max(0.0, float(6.9 + 20 * np.arcsinh(nu - 0.1) / np.log(10)))


def crest_edge_losses(distance, height, wavelength):
    """Return one-way losses for the primary and all recursive subpath edges."""

    def split(left, right):
        if right - left <= 1:
            return 0.0, 0.0
        inner = slice(left + 1, right)
        before = distance[inner] - distance[left]
        after = distance[right] - distance[inner]
        chord = height[left] + before / (before + after) * (height[right] - height[left])
        nu = (height[inner] - chord) * np.sqrt(2 / wavelength * (1 / before + 1 / after))
        primary = int(np.argmax(nu))
        loss = knife_loss(nu[primary])
        index = left + 1 + primary
        _, left_loss = split(left, index)
        _, right_loss = split(index, right)
        return loss, loss + left_loss + right_loss

    return split(0, len(distance) - 1)


def check_propagation():
    wavelength = 0.20
    straight = np.array([0.0, 100.0])
    assert crest_edge_losses(straight, np.zeros(2), wavelength) == (0.0, 0.0)
    single = np.array([0.0, 50.0, 100.0])
    expected = knife_loss(np.sqrt(2 / wavelength * (1 / 50 + 1 / 50)))
    np.testing.assert_allclose(crest_edge_losses(single, np.array([0, 1, 0]), wavelength), expected)

    # NTIA TR-26-580 Table 2 supplies a case with a secondary, a tertiary,
    # and a sufficiently clear sub-path edge whose contribution is zero.
    distance = np.array([0.0, 1200.0, 2800.0, 4400.0, 5800.0, 6600.0])
    height = np.array([0.0, 140.0, 260.0, 200.0, 220.0, 0.0])
    published_example = crest_edge_losses(distance, height, wavelength)
    np.testing.assert_allclose(published_example, (41.27, 99.87), atol=0.02, rtol=0)
    np.testing.assert_allclose(
        crest_edge_losses(distance[-1] - distance[::-1], height[::-1], wavelength),
        published_example,
        atol=1e-12,
        rtol=0,
    )


def regular_crest_fractions(start_phase, phase_advance):
    """Find the unique local maxima strictly inside the two ray endpoints."""
    assert phase_advance > 0
    start_cycle = start_phase / (2 * np.pi)
    end_cycle = (start_phase + phase_advance) / (2 * np.pi)
    crest_cycles = np.arange(np.floor(start_cycle) + 1, np.ceil(end_cycle))
    return (crest_cycles - start_cycle) * (2 * np.pi / phase_advance)


def regular_crest_losses(run, frequency, amplitude, phase):
    origin = run["origin"]
    target = run["target"]
    span = target - origin
    _, _, initial_phase = model.components(frequency, amplitude, phase)
    omega = 2 * np.pi * frequency
    wave_number = omega**2 / model.G
    heading = np.array([np.cos(model.HEADING), np.sin(model.HEADING)])
    start_phase = wave_number * (origin[:, :2] @ heading) - omega * run["t"] + initial_phase[0]
    phase_advance = wave_number * (span[:, :2] @ heading)
    losses = []
    for start, advance, distance, origin_z, target_z in zip(
        start_phase, phase_advance, run["slant"], origin[:, 2], target[:, 2], strict=True
    ):
        fractions = regular_crest_fractions(start, advance)
        assert np.all((fractions > 0) & (fractions < 1))
        np.testing.assert_allclose(np.cos(start + advance * fractions), 1.0, atol=1e-12)
        stations = distance * np.r_[0.0, fractions, 1.0]
        heights = np.r_[origin_z, np.full(len(fractions), amplitude), target_z]
        losses.append(crest_edge_losses(stations, heights, model.WAVELENGTH))
    return np.array(losses).T


def summarize(name, frequency, amplitude):
    acquired = []
    usable = []
    path_losses = []
    for phase in range(PHASE_COUNT):
        run = model.run(frequency, amplitude, phase, visits=VISITS, samples=PATH_SUBDIVISIONS)
        angle_loss = (
            80 * np.log10(2) * (np.array([run["body_angle"], run["level_angle"]]) / model.BETA) ** 2
        )
        baseline_path_loss = model.MARGIN - angle_loss[0] - run["margin_motion"]
        crest_paths = 2 * regular_crest_losses(run, frequency, amplitude, phase)
        assert np.all(crest_paths[1] >= crest_paths[0])
        two_way_path_loss = np.vstack((baseline_path_loss, crest_paths))
        receive_margin = model.MARGIN - angle_loss[None, :, :] - two_way_path_loss[:, None, :]
        detected = receive_margin[:, [0, 0, 1, 1], :] >= 0
        level_midpoint = level_mapping_errors(run, phase, {})
        errors = np.insert(run["errors"], 2, level_midpoint, axis=0)
        good = detected & (errors[None, :, :] <= model.TOLERANCE)
        np.testing.assert_array_equal(detected[0, [0, 1, 3]], run["acquired"])
        np.testing.assert_array_equal(good[0, [0, 1, 3]], run["usable"])
        acquired.append(detected)
        usable.append(good)
        path_losses.append(two_way_path_loss)

    acquisition = np.array(acquired)
    use = np.array(usable)
    losses = np.array(path_losses)
    results = []
    for index, method in enumerate(METHODS):
        detection = acquisition[:, index]
        positions = use[:, index]
        body = detection[:, 0]
        level = detection[:, 2]
        count = positions.sum(axis=(0, 2))
        total = PHASE_COUNT * VISITS
        results.append(
            {
                "case": name,
                "frequency_hz": frequency,
                "amplitude_m": amplitude,
                "propagation": method,
                "scheduled_visits": total,
                "body_acquired": int(body.sum()),
                "level_acquired": int(level.sum()),
                "midpoint_usable": int(count[0]),
                "spoke_usable": int(count[1]),
                "level_midpoint_usable": int(count[2]),
                "level_spoke_usable": int(count[3]),
                "registration_gain_pp": (count[1] - count[0]) * 100 / total,
                "level_gain_pp": (count[3] - count[1]) * 100 / total,
                "standalone_level_gain_pp": (count[2] - count[0]) * 100 / total,
                "registration_after_level_gain_pp": (count[3] - count[2]) * 100 / total,
                "level_acquisition_wins": int(np.count_nonzero(level & ~body)),
                "level_acquisition_losses": int(np.count_nonzero(body & ~level)),
                "body_classification_changes_vs_effective_edge": int(
                    np.count_nonzero(body != acquisition[:, 0, 0])
                ),
                "level_classification_changes_vs_effective_edge": int(
                    np.count_nonzero(level != acquisition[:, 0, 2])
                ),
                "path_loss_median_two_way_db": float(np.median(losses[:, index])),
                "max_added_secondary_loss_two_way_db": float(
                    np.max(losses[:, index] - losses[:, 1]) if index == 2 else 0.0
                ),
            }
        )
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=Path("data/experiment-results.json"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    check_propagation()
    # Test a regularly spaced subset without using the observed gains to select cells.
    eligible = json.loads(args.baseline.read_text())["operating_map"]
    sparse = [
        ("sparse_grid", cell["frequency_hz"], cell["amplitude_m"])
        for cell in eligible
        if np.any(np.isclose(cell["frequency_hz"], SPARSE_FREQUENCIES))
        and np.any(np.isclose(cell["amplitude_m"], SPARSE_AMPLITUDES))
    ]
    rows = [row for case in (*CASES, *sparse) for row in summarize(*case)]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Verified the NTIA four-edge example and scored {len(sparse)} sparse operating cells.")


if __name__ == "__main__":
    main()
