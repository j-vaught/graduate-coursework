"""Phase-grid quadrature and finite-horizon checks for the paired experiment."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

import paired_experiment as m


def evaluate(freq, amplitude, count, visits, scan, samples, phase_method):
    results = []
    for phase in range(count):
        phase_origin = None
        if phase_method == "uniform":
            phase_origin = 2 * np.pi * (phase + 0.5) / count
        results.append(
            m.run(
                freq,
                amplitude,
                phase,
                scan=scan,
                visits=visits,
                samples=samples,
                phase_origin=phase_origin,
            )
        )
    summary = m.summarize(results)
    return {
        "frequency_hz": freq,
        "amplitude_m": amplitude,
        "phase_method": phase_method,
        "phase_count": count,
        "visits_per_phase": visits,
        "scan_period_s": scan,
        "usable_mid": summary["fraction"][0],
        "usable_spoke": summary["fraction"][1],
        "usable_level": summary["fraction"][2],
        "gain_pp": 100 * summary["correction_gain"],
        "level_gain_pp": 100 * summary["stabilization_gain"],
        "mean_max_consecutive_miss": summary["maxrun_mean"][0],
        "p95_max_consecutive_miss": summary["maxrun_p95"][0],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", required=True)
    out = Path(ap.parse_args().outdir)
    out.mkdir(exist_ok=True, parents=True)
    rows = []
    cases = [("reference", 0.35, 0.15)]
    for f in (0.20, 0.28, 0.35, 0.42):
        k = (2 * np.pi * f) ** 2 / m.G
        a = (3 * m.RAD) / (
            m.HULL_PITCH_GAIN
            * k
            * np.cos(m.HEADING)
            * abs(m.transfer(np.array([f]), m.NATURAL, m.DAMPING)[0])
        )
        if k * a <= m.MAX_STEEPNESS:
            cases.append(("matched_3deg", f, float(a)))
    for name, f, a in cases:
        for method in ("uniform", "random"):
            for count in (32, 64, 128, 256):
                row = evaluate(f, a, count, 192, 2.5, 301, method)
                row["case"] = name
                rows.append(row)
        # Test the long-run average and the finite observation horizon. Uniform
        # grid stays identical so the change comes from observation duration.
        for visits in (48, 96, 384, 768):
            row = evaluate(f, a, 64, visits, 2.5, 301, "uniform")
            row["case"] = name
            rows.append(row)
    # Matched-pitch scan-rate sensitivity on the same phase grid.
    for name, f, a in cases:
        if name != "matched_3deg":
            continue
        for scan in (1.25, 3.75):
            for count in (32, 128, 256):
                row = evaluate(f, a, count, 192, scan, 301, "uniform")
                row["case"] = name
                rows.append(row)
    path = out / "verification_phase_convergence.csv"
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    summary = []
    for name, f, a in cases:
        select = [
            r
            for r in rows
            if r["case"] == name and r["frequency_hz"] == f and r["scan_period_s"] == 2.5
        ]
        ref = next(
            r
            for r in select
            if r["phase_method"] == "uniform"
            and r["phase_count"] == 256
            and r["visits_per_phase"] == 192
        )
        comp = next(
            r
            for r in select
            if r["phase_method"] == "uniform"
            and r["phase_count"] == 32
            and r["visits_per_phase"] == 192
        )
        mc = next(
            r
            for r in select
            if r["phase_method"] == "random"
            and r["phase_count"] == 32
            and r["visits_per_phase"] == 192
        )
        summary.append(
            {
                "case": name,
                "frequency_hz": f,
                "amplitude_m": a,
                "uniform_32_vs_256_pp": max(
                    abs(100 * (comp[k] - ref[k]))
                    for k in ("usable_mid", "usable_spoke", "usable_level")
                ),
                "random_32_vs_uniform_256_pp": max(
                    abs(100 * (mc[k] - ref[k]))
                    for k in ("usable_mid", "usable_spoke", "usable_level")
                ),
                "maxrun_mean_uniform_256": ref["mean_max_consecutive_miss"],
                "maxrun_p95_uniform_256": ref["p95_max_consecutive_miss"],
            }
        )
    (out / "verification_phase_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
