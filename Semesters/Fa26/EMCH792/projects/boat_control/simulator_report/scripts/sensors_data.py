"""Generate the stereo range-uncertainty curve from simulator defaults."""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from blueboat_sim.config import Experiment


def main() -> None:
    sensors = Experiment().sensors
    distances = [float(distance) for distance in range(1, 21)]
    data = {
        "source": "blueboat_sim.config.Sensors default values",
        "fx_px": sensors.camera_fx_px,
        "baseline_m": sensors.camera_baseline_m,
        "disparity_sigma_px": sensors.camera_disparity_sigma_px,
        "max_range_m": sensors.camera_max_range_m,
        "distance_m": distances,
        "disparity_px": [
            sensors.camera_fx_px * sensors.camera_baseline_m / distance for distance in distances
        ],
        "range_sigma_m": [
            distance**2
            * sensors.camera_disparity_sigma_px
            / (sensors.camera_fx_px * sensors.camera_baseline_m)
            for distance in distances
        ],
        "streams": [
            {"name": "GNSS", "period_s": sensors.gnss_period_s, "latency_s": sensors.gnss_delay_s},
            {"name": "IMU", "period_s": sensors.imu_period_s, "latency_s": sensors.imu_delay_s},
            {
                "name": "Stereo",
                "period_s": sensors.camera_period_s,
                "latency_s": sensors.camera_delay_s,
            },
        ],
    }
    destination = Path(__file__).resolve().parents[1] / "data" / "sensors.json"
    destination.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
