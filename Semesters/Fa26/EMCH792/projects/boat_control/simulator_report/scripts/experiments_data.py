"""Rebuild the report's reduced experiment figure data from the saved run."""

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "configurable_simulator" / "comparison.json"
DESTINATION = ROOT / "simulator_report" / "data" / "experiments.json"


def main() -> None:
    runs: list[dict[str, Any]] = json.loads(SOURCE.read_text())
    baseline = runs[0]
    indices = {name: index for index, name in enumerate(baseline["columns"])}

    def values(run: dict[str, Any], field: str) -> list[float]:
        rows = run["history"]
        return [row[indices[field]] for row in rows]

    times = values(baseline, "time_s")
    output: dict[str, Any] = {
        "time_s": times[::10],
        "port_pwm_us": values(baseline, "port_pwm_us")[::10],
        "starboard_pwm_us": values(baseline, "starboard_pwm_us")[::10],
        "trajectory": {},
        "offsets": {},
        "metrics": [],
    }
    trajectory = output["trajectory"]
    offsets = output["offsets"]
    metrics = output["metrics"]
    base_x, base_y = values(baseline, "x_m"), values(baseline, "y_m")
    for run in runs:
        name = run["name"]
        x, y = values(run, "x_m"), values(run, "y_m")
        trajectory[name] = {"east_m": x[::10], "north_m": y[::10]}
        offsets[name] = {
            "time_s": times[::10],
            "distance_m": [
                ((x[i] - base_x[i]) ** 2 + (y[i] - base_y[i]) ** 2) ** 0.5
                for i in range(0, len(x), 10)
            ],
        }
        metric = run["metrics"]
        metrics.append(
            {
                "name": name,
                "east": metric["final_x_m"],
                "north": metric["final_y_m"],
                "heading_deg": metric["final_heading_rad"] * 180 / 3.141592653589793,
                "peak_force": metric["peak_force_N"],
                "force_sq_integral": metric["squared_force_integral_N2_s"],
                "gnss_rms": metric["gnss_position_rms_m"],
                "camera": metric["valid_delivered_camera_frames"],
            }
        )
    DESTINATION.write_text(json.dumps(output, indent=2) + "\n")


if __name__ == "__main__":
    main()
