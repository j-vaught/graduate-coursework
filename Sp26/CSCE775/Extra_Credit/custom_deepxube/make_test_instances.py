"""Generate deterministic test problem instances for the custom domains."""

from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np

import deepxube  # noqa: F401
from deepxube.utils.command_line_utils import get_domain_from_arg


OUT_DIR = Path("test_instances")

CASES = [
    ("hanoi.6.3", "hanoi_6_3.pkl", 30, 5, 35),
    ("pancake.10", "pancake_10.pkl", 30, 5, 35),
    ("linkage.64_64_64", "linkage_64.pkl", 40, 5, 50),
    ("mapf.28_28_30_64", "mapf_28x28_30.pkl", 30, 10, 80),
    ("arm.6_12_8", "arm_6_12_8.pkl", 40, 3, 25),
    ("retro.7", "retro_7.pkl", 40, 5, 30),
]


def main() -> None:
    np.random.seed(775)
    OUT_DIR.mkdir(exist_ok=True)

    for domain_str, file_name, num, step_min, step_max in CASES:
        domain, _ = get_domain_from_arg(domain_str)
        steps = np.random.randint(step_min, step_max + 1, size=num).tolist()
        states, goals = domain.sample_problem_instances(steps)
        out_file = OUT_DIR / file_name
        with out_file.open("wb") as f:
            pickle.dump(
                {
                    "domain": domain_str,
                    "steps": steps,
                    "states": states,
                    "goals": goals,
                },
                f,
                protocol=-1,
            )
        print(f"{domain_str}: wrote {num} instances to {out_file}")


if __name__ == "__main__":
    main()
