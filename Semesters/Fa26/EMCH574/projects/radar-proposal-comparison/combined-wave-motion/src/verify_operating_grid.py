"""Check production-grid knife-edge resolution at several representative cells."""

import argparse
import csv
import json
from pathlib import Path

import numpy as np

import paired_experiment as m


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--outdir", required=True)
    args = p.parse_args()
    rows = []
    for f, amplitude in [(0.3325, 0.432), (0.35, 0.36), (0.35, 0.15)]:
        for seed in range(32):
            reference = m.run(f, amplitude, seed, visits=192, samples=2401)
            for samples in (301, 601, 1201):
                r = m.run(f, amplitude, seed, visits=192, samples=samples)
                rows.append(
                    {
                        "frequency_hz": f,
                        "amplitude_m": amplitude,
                        "seed": seed,
                        "path_samples": samples,
                        "reference_path_samples": 2401,
                        "visits": 192,
                        "changed_acquisitions": int(
                            np.count_nonzero(r["acquired"] != reference["acquired"])
                        ),
                        "changed_usable": int(np.count_nonzero(r["usable"] != reference["usable"])),
                        "max_margin_difference_db": float(
                            np.max(np.abs(r["margin_motion"] - reference["margin_motion"]))
                        ),
                    }
                )
    output = Path(args.outdir)
    output.mkdir(parents=True, exist_ok=True)
    with (output / "verification_grid_convergence.csv").open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0])
        writer.writeheader()
        writer.writerows(rows)
    summary = {}
    for n in (301, 601, 1201):
        group = [x for x in rows if x["path_samples"] == n]
        summary[str(n)] = {
            "changed_acquisitions": sum(x["changed_acquisitions"] for x in group),
            "changed_usable": sum(x["changed_usable"] for x in group),
            "max_margin_difference_db": max(x["max_margin_difference_db"] for x in group),
            "cases": len(group),
            "visits_per_case": 192,
        }
    (output / "verification_grid_convergence.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
