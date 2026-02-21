#!/usr/bin/env python3
"""Generate YAML scene configs for all ablation conditions.

Produces scene YAML files compatible with the radar-scene-augmentation
pipeline. Each ablation gets a directory of configs parameterized by
the variable under study.

Output structure:
    scenes/
        a1_trail_length/
            stationary_N0.yaml, stationary_N3.yaml, ...
            slow_N0.yaml, ...
            medium_N0.yaml, ...
            fast_N0.yaml, ...
        a2_decay/
            exponential.yaml, concave.yaml, linear.yaml, step.yaml
        a3_intensity/
            binary.yaml, proportional.yaml
        a4_color/
            mono.yaml, twotone.yaml, gradient.yaml, intensity.yaml
        a5_range/
            near_N0.yaml, near_N3.yaml, ..., mid_N0.yaml, ..., far_N0.yaml, ...
        a6_clutter/
            low.yaml, moderate.yaml, heavy.yaml
        a7_proximity/
            sep_10m.yaml, sep_20m.yaml, ..., sep_100m.yaml
        a8_crossing/
            angle_15.yaml, angle_30.yaml, ..., angle_90.yaml
"""

import os
import yaml
from pathlib import Path


FRAMES_PER_SCENE = 250
SEED_BASE = 42

# Speed classes in px/scan (approximate bin displacement per frame)
SPEED_CLASSES = {
    "stationary": 0,
    "slow": 2,
    "medium": 5,
    "fast": 15,
}

# Trail lengths for A1 and A5
TRAIL_LENGTHS = [0, 3, 6, 12, 24]

# Range bins: near (~200m), mid (~1nm ≈ 1852m), far (~3nm ≈ 5556m)
# With 868 bins over ~6nm max range, 1 bin ≈ 6.9m
RANGE_BINS = {
    "near": 80,    # ~200m from center
    "mid": 350,    # ~1nm
    "far": 750,    # ~3nm
}

# Proximity separations in meters (converted to bins: 1 bin ≈ 6.9m)
PROXIMITY_METERS = list(range(10, 110, 10))

# Crossing angles
CROSSING_ANGLES = [15, 30, 45, 60, 75, 90]


def make_object_group(name, count=1, size="medium", speed=0,
                      heading=135, intensity_base=1.0,
                      position=None, bin_idx=None,
                      flicker_enabled=False):
    """Build an object group dict for YAML serialization."""
    group = {
        "name": name,
        "count": count,
        "size": size,
        "intensity": {
            "base": intensity_base,
            "variability": 0.1,
            "profile": "constant",
        },
        "flicker": {
            "enabled": flicker_enabled,
            "rate": 0.3 if flicker_enabled else 0.0,
            "primary_frames": [15, 50],
            "flicker_frames": [2, 6],
            "intensity_drop": 0.4,
        },
    }

    if speed == 0:
        path = {"type": "fixed"}
        if position is not None:
            path["position"] = position
        elif bin_idx is not None:
            path["position"] = [360, bin_idx]
        else:
            path["position"] = "random"
        group["path"] = path
    else:
        path = {
            "type": "linear",
            "start": "random" if bin_idx is None else [360, bin_idx],
            "heading": heading,
            "speed": float(speed),
            "duration": [0.6, 0.9],
        }
        group["path"] = path

    group["placement"] = {"margin": 30}
    return group


def make_scene(seed, count, objects, class_map=None):
    """Build a complete scene config dict."""
    if class_map is None:
        class_map = {obj["name"]: 0 for obj in objects}
    return {
        "seed": seed,
        "count": count,
        "objects": objects,
        "labels": {
            "export": True,
            "class_map": class_map,
        },
    }


def write_yaml(path, data):
    """Write a YAML file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def generate_a1(base_dir):
    """A1: Trail length × speed class. 5 lengths × 4 speeds = 20 configs.

    Trail length is applied post-hoc by apply_trails.py, but we need
    separate scene configs per speed class (the speed determines the
    raw frame generation). Trail length variation happens at the
    apply_trails step, not here.
    """
    out = base_dir / "a1_trail_length"
    for speed_name, speed_val in SPEED_CLASSES.items():
        objects = [
            make_object_group(
                name="target",
                count=3,
                size="medium",
                speed=speed_val,
                heading=135,
                intensity_base=1.2,
            ),
        ]
        scene = make_scene(SEED_BASE, FRAMES_PER_SCENE, objects)
        write_yaml(str(out / f"{speed_name}.yaml"), scene)

    print(f"  A1: {len(SPEED_CLASSES)} scene configs (trail length varied at apply_trails)")


def generate_a2(base_dir):
    """A2: Decay function. 4 configs (same scene, decay varied at apply_trails)."""
    out = base_dir / "a2_decay"
    # Single scene config; decay function is an apply_trails parameter
    objects = [
        make_object_group("target", count=3, size="medium", speed=5,
                          heading=135, intensity_base=1.2),
    ]
    scene = make_scene(SEED_BASE, FRAMES_PER_SCENE, objects)
    write_yaml(str(out / "base.yaml"), scene)
    print("  A2: 1 scene config (decay function varied at apply_trails)")


def generate_a3(base_dir):
    """A3: Intensity mode. Uses same scene as A2."""
    out = base_dir / "a3_intensity"
    objects = [
        make_object_group("target", count=3, size="medium", speed=5,
                          heading=135, intensity_base=1.2),
        make_object_group("weak_target", count=2, size="small", speed=2,
                          heading=45, intensity_base=0.5),
    ]
    scene = make_scene(
        SEED_BASE, FRAMES_PER_SCENE, objects,
        class_map={"target": 0, "weak_target": 0},
    )
    write_yaml(str(out / "mixed_rcs.yaml"), scene)
    print("  A3: 1 scene config (intensity mode varied at apply_trails)")


def generate_a4(base_dir):
    """A4: Color mapping. Uses same scene as A3."""
    out = base_dir / "a4_color"
    objects = [
        make_object_group("target", count=3, size="medium", speed=5,
                          heading=135, intensity_base=1.2),
        make_object_group("weak_target", count=2, size="small", speed=2,
                          heading=45, intensity_base=0.5),
    ]
    scene = make_scene(
        SEED_BASE, FRAMES_PER_SCENE, objects,
        class_map={"target": 0, "weak_target": 0},
    )
    write_yaml(str(out / "mixed_rcs.yaml"), scene)
    print("  A4: 1 scene config (color mapping varied at apply_trails)")


def generate_a5(base_dir):
    """A5: Range dependence. 3 ranges × 5 trail lengths = 15 configs.

    Objects placed at specific range bins. Trail lengths varied at apply_trails.
    """
    out = base_dir / "a5_range"
    for range_name, range_bin in RANGE_BINS.items():
        objects = [
            make_object_group(
                "target", count=3, size="medium", speed=5,
                heading=135, intensity_base=1.2,
                bin_idx=range_bin,
            ),
        ]
        scene = make_scene(SEED_BASE, FRAMES_PER_SCENE, objects)
        write_yaml(str(out / f"{range_name}.yaml"), scene)

    print(f"  A5: {len(RANGE_BINS)} scene configs (trail length varied at apply_trails)")


def generate_a6(base_dir):
    """A6: Clutter level. 3 configs with different clutter intensities.

    Clutter level is controlled by sorting background frames by average
    intensity at the generate_scenes.py stage. Here we add different
    amounts of synthetic clutter objects.
    """
    out = base_dir / "a6_clutter"

    for level, (clutter_count, clutter_intensity) in {
        "low": (0, 0.0),
        "moderate": (5, 0.3),
        "heavy": (15, 0.5),
    }.items():
        objects = [
            make_object_group("target", count=3, size="medium", speed=5,
                              heading=135, intensity_base=1.2),
        ]
        if clutter_count > 0:
            objects.append(
                make_object_group(
                    "clutter", count=clutter_count, size=[5, 40],
                    speed=0, intensity_base=clutter_intensity,
                    flicker_enabled=True,
                )
            )
        class_map = {"target": 0}
        if clutter_count > 0:
            class_map["clutter"] = 0
        scene = make_scene(SEED_BASE, FRAMES_PER_SCENE, objects, class_map)
        write_yaml(str(out / f"{level}.yaml"), scene)

    print("  A6: 3 scene configs (low, moderate, heavy clutter)")


def generate_a7(base_dir):
    """A7: Target proximity. 10 separations (10m to 100m in 10m steps).

    Two fixed targets at controlled separations. Separation is in range bins
    (1 bin ≈ 6.9m), placed along the same azimuth.
    """
    out = base_dir / "a7_proximity"
    center_bin = 400  # mid-range

    for sep_m in PROXIMITY_METERS:
        sep_bins = max(1, round(sep_m / 6.9))
        bin_a = center_bin - sep_bins // 2
        bin_b = center_bin + sep_bins // 2

        objects = [
            make_object_group("target_a", count=1, size="medium", speed=0,
                              intensity_base=1.0, position=[360, bin_a]),
            make_object_group("target_b", count=1, size="medium", speed=0,
                              intensity_base=1.0, position=[360, bin_b]),
        ]
        scene = make_scene(
            SEED_BASE, FRAMES_PER_SCENE, objects,
            class_map={"target_a": 0, "target_b": 0},
        )
        write_yaml(str(out / f"sep_{sep_m}m.yaml"), scene)

    print(f"  A7: {len(PROXIMITY_METERS)} scene configs (10m–100m separations)")


def generate_a8(base_dir):
    """A8: Crossing trajectories. 6 crossing angles.

    Two linear-path targets that cross near the center of the scene.
    One moves at heading 0° (north), the other at the specified angle.
    """
    out = base_dir / "a8_crossing"

    for angle in CROSSING_ANGLES:
        objects = [
            make_object_group("target_a", count=1, size="medium", speed=5,
                              heading=0, intensity_base=1.2),
            make_object_group("target_b", count=1, size="medium", speed=5,
                              heading=float(angle), intensity_base=1.2),
        ]
        scene = make_scene(
            SEED_BASE, FRAMES_PER_SCENE, objects,
            class_map={"target_a": 0, "target_b": 0},
        )
        write_yaml(str(out / f"angle_{angle}.yaml"), scene)

    print(f"  A8: {len(CROSSING_ANGLES)} scene configs (crossing angles)")


def main():
    base_dir = Path(__file__).parent / "scenes"
    base_dir.mkdir(parents=True, exist_ok=True)

    print("Generating scene configs for ablation study...")
    generate_a1(base_dir)
    generate_a2(base_dir)
    generate_a3(base_dir)
    generate_a4(base_dir)
    generate_a5(base_dir)
    generate_a6(base_dir)
    generate_a7(base_dir)
    generate_a8(base_dir)

    total = sum(len(list(d.glob("*.yaml")))
                for d in base_dir.iterdir() if d.is_dir())
    print(f"\nTotal: {total} YAML configs generated in {base_dir}")


if __name__ == "__main__":
    main()
