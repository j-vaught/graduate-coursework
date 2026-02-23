#!/usr/bin/env python3
"""Re-clean land frames by zeroing out any water-region returns.

The existing land frames have ~3% leakage in water regions (real boats/buoys
that weren't properly masked). This script applies the water mask from the
annotation file to zero out all water-region returns.

Usage:
    python clean_land_frames.py
"""

import math
import os
import sys

sys.path.insert(0, "/Volumes/MacShare/Code/radar-scene-augmentation/scene-generator")

from pipeline.data_loader import load_data
from radar_core.csv_handler import RadarCSVHandler


def main():
    annot = "/Volumes/MacShare/Code/radar-scene-augmentation/data/annotation_charleston.json"
    land_dir = "/Volumes/MacShare/Code/Generative_Radar/Composite_tier/data/land_frames_charleston"
    lib_dir = "/Volumes/MacShare/Code/Generative_Radar/Composite_tier/data/object_library_charleston"
    output_dir = "/Volumes/MacShare/Code/radar-scene-augmentation/data/land_frames_charleston"

    os.makedirs(output_dir, exist_ok=True)

    print("Loading data...")
    data = load_data(
        annotation_path=annot,
        land_frames_dir=land_dir,
        library_path=lib_dir,
        margin=30,
        min_intensity=20,
    )

    handler = RadarCSVHandler()
    files = sorted(data.land_files)
    print(f"Processing {len(files)} land frames...")

    total_zeroed = 0
    for i, fpath in enumerate(files):
        frame = handler.read_csv(fpath)
        zeroed = 0

        for pulse in frame.pulses:
            p_idx = int((pulse.angle_rad / (2 * math.pi)) * data.water_mask.num_pulses) % data.water_mask.num_pulses
            for b_idx in range(len(pulse.echoes)):
                if data.water_mask.get(p_idx, b_idx) and pulse.echoes[b_idx] > 0:
                    pulse.echoes[b_idx] = 0
                    zeroed += 1

        total_zeroed += zeroed

        # Save cleaned frame
        out_name = os.path.basename(fpath)
        handler.write_csv(frame, os.path.join(output_dir, out_name))

        if (i + 1) % 20 == 0 or (i + 1) == len(files):
            print(f"  {i+1}/{len(files)} frames cleaned ({zeroed} water pixels zeroed)")

    print(f"\nDone! Cleaned frames saved to: {output_dir}")
    print(f"Total water-region pixels zeroed: {total_zeroed}")


if __name__ == "__main__":
    main()
