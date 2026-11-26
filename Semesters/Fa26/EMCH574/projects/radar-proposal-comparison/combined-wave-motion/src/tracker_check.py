"""Score held radar positions against a fixed or wave-following scatterer."""

import argparse
import csv
from pathlib import Path

import numpy as np

import paired_experiment as model

CASES = {"reference": (0.35, 0.15), "strongest_registration": (0.3325, 0.432)}
PHASE_COUNT = 32
VISITS_PER_PHASE = 192
REGISTRATIONS = ("midpoint", "spoke_time")


def score_holding(
    t: np.ndarray, truth: np.ndarray, fixes: np.ndarray, acquired: np.ndarray
) -> dict[str, int | float]:
    """Hold the most recent finite fix until the next acquired finite fix."""
    available = acquired & np.all(np.isfinite(fixes), axis=1)
    index = np.arange(len(t))
    last_update = np.maximum.accumulate(np.where(available, index, -1))
    held = ~available & (last_update >= 0)
    uninitialized = last_update < 0
    last_or_first = np.maximum(last_update, 0)
    error = np.linalg.norm(fixes[last_or_first] - truth, axis=1)
    within_tolerance = error <= model.TOLERANCE
    fresh_usable = np.count_nonzero(available & within_tolerance)
    held_usable = np.count_nonzero(held & within_tolerance)
    held_bad = np.count_nonzero(held & ~within_tolerance)
    stale_age = t[held] - t[last_update[held]]
    return {
        "acquired": int(np.count_nonzero(acquired)),
        "fresh_fixes": int(np.count_nonzero(available)),
        "fresh_usable": int(fresh_usable),
        "held_usable": int(held_usable),
        "held_outside_tolerance": int(held_bad),
        "uninitialized": int(np.count_nonzero(uninitialized)),
        "max_held_age_s": float(np.max(stale_age, initial=0.0)),
    }


def run() -> list[dict[str, str | int | float]]:
    rows: list[dict[str, str | int | float]] = []
    for name, (frequency, amplitude) in CASES.items():
        for orbital in (False, True):
            for sigma in (0.0, 0.25):
                for phase in range(PHASE_COUNT):
                    result = model.run(
                        frequency,
                        amplitude,
                        phase,
                        visits=VISITS_PER_PHASE,
                        samples=601,
                        range_sigma_m=sigma,
                        bearing_sigma_deg=sigma,
                        horizontal_orbit=orbital,
                    )
                    truth = result["target"][:, :2]
                    motion_m = np.linalg.norm(truth - np.array([model.RANGE, 0.0]), axis=1)
                    assert np.max(motion_m) <= (amplitude if orbital else 0.0) + 1e-12
                    for i, registration in enumerate(REGISTRATIONS):
                        scores = score_holding(
                            result["t"],
                            truth,
                            result["positions"][i, :, :2],
                            result["acquired"][i],
                        )
                        assert scores["fresh_usable"] == np.count_nonzero(result["usable"][i])
                        assert (
                            scores["fresh_fixes"]
                            + scores["held_usable"]
                            + scores["held_outside_tolerance"]
                            + scores["uninitialized"]
                            == VISITS_PER_PHASE
                        )
                        rows.append(
                            {
                                "case": name,
                                "frequency_hz": frequency,
                                "amplitude_m": amplitude,
                                "horizontal_motion": "orbital" if orbital else "fixed",
                                "bearing_noise_std_deg": sigma,
                                "range_noise_std_m": sigma,
                                "phase": phase,
                                "registration": registration,
                                "visits": VISITS_PER_PHASE,
                                **scores,
                            }
                        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    options = parser.parse_args()
    rows = run()
    with options.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
