"""Independent checks of the paired experiment implementation.

Run after paired_experiment.py is finalized on a designated compute server.
"""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

import paired_experiment as model


def as_dict(results):
    return {
        "acquired_fraction": results["acquired"].mean(axis=1).tolist(),
        "usable_fraction": results["usable"].mean(axis=1).tolist(),
        "below_fraction": results["below"].tolist(),
        "outside_fraction": results["outside"].tolist(),
        "max_exact_pose_error_m": float(np.nanmax(results["errors"][1:])),
        "paired_acquisitions_identical": bool(
            np.array_equal(results["acquired"][0], results["acquired"][1])
        ),
    }


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", required=True)
    args = parser.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    cases = [
        (0.25, 0.25, 0, False),
        (0.35, 0.15, 0, False),
        (0.45, 0.20, 7, False),
        (0.55, 0.10, 5, False),
        (0.35, 0.15, 3, True),
    ]
    convergence = []
    paired_error_max = 0.0
    for f, amp, phase, irregular in cases:
        options = {
            "freq": f,
            "amplitude": amp,
            "phase": phase,
            "visits": 192,
            "irregular": irregular,
        }
        reference = model.run(**options, samples=2401)
        for n in (151, 301, 601, 1201):
            result = model.run(**options, samples=n)
            paired_error_max = max(paired_error_max, np.nanmax(result["errors"][1:]))
            convergence.append(
                {
                    "frequency_hz": f,
                    "amplitude_m": amp,
                    "phase": phase,
                    "irregular": irregular,
                    "path_samples": n,
                    "reference_path_samples": 2401,
                    "max_motion_margin_error_db": float(
                        np.max(abs(result["margin_motion"] - reference["margin_motion"]))
                    ),
                    "max_level_margin_error_db": float(
                        np.max(abs(result["margin_level"] - reference["margin_level"]))
                    ),
                    "changed_acquisitions": int(
                        np.sum(result["acquired"] != reference["acquired"])
                    ),
                    "changed_usable": int(np.sum(result["usable"] != reference["usable"])),
                    "scheduled_visits": 192,
                }
            )
            assert np.array_equal(result["acquired"][0], result["acquired"][1])
    with (out / "verification_paired_convergence.csv").open("w", newline="") as fp:
        writer = csv.DictWriter(fp, fieldnames=convergence[0].keys())
        writer.writeheader()
        writer.writerows(convergence)
    # Independently compare the exact motion response with the complex
    # sinusoidal transfer and the geometric slope sign at several frequencies.
    response = []
    for f in (0.20, 0.35, 0.50):
        frequencies = np.array([f])
        amplitude = np.array([0.15])
        phase = np.array([0.7])
        time = np.linspace(0, 5 / f, 10001)
        _, _, pitch, _ = model.pose(time, frequencies, amplitude, phase, 0.15)
        omega = 2 * np.pi * f
        k = omega**2 / model.G
        ratio = f / model.NATURAL
        gain = 1 / np.hypot(1 - ratio**2, 2 * 0.15 * ratio)
        lag = np.arctan2(2 * 0.15 * ratio, 1 - ratio**2)
        expected = (
            -model.HULL_PITCH_GAIN
            * k
            * 0.15
            * np.cos(model.HEADING)
            * gain
            * np.sin(omega * time - 0.7 - lag)
        )
        response.append(
            {
                "frequency_hz": f,
                "expected_peak_deg": float(
                    np.rad2deg(model.HULL_PITCH_GAIN * k * 0.15 * np.cos(model.HEADING) * gain)
                ),
                "maximum_pitch_error_rad": float(max(abs(expected - pitch))),
            }
        )
    # A fixed 40-second interval is sampled more densely; each count includes
    # scheduled midpoint-pose, line-of-sight, and threshold classifications.
    temporal = []
    for n in (256, 512, 1024, 2048):
        times = np.linspace(2.5, 42.5, n, endpoint=False)
        result = model.run(0.35, 0.15, 0, samples=601, times=times)
        temporal.append(dict(time_samples=n, **as_dict(result)))
    checks = {
        "cases": len(cases),
        "pitch_response": response,
        "temporal_sampling": temporal,
        "maximum_exact_pose_error_m": float(paired_error_max),
        "caveat": "Temporal check samples acquisition phase densely over 40 s. Production visits remain discrete rotation schedules; this is not a sampling-error estimate for finite wave records.",
    }
    (out / "verification_paired_checks.json").write_text(json.dumps(checks, indent=2) + "\n")
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    run()
