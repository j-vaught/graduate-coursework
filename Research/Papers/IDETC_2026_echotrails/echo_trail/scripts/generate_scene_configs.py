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
import sys
import yaml
from pathlib import Path

# Add radar-scene-augmentation to path for water mask validation
_SCENE_GEN_ROOT = Path("/Volumes/MacShare/Code/radar-scene-augmentation/scene-generator")
sys.path.insert(0, str(_SCENE_GEN_ROOT))

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


def load_water_mask():
    """Load the Charleston water mask in polar (pulse, bin) space."""
    from radar_core.annotations import AnnotationSet
    from radar_core.converter import RadarConverter, ConversionConfig
    from radar_core.mask import PolarMask, create_water_mask

    annotation_path = Path("/Volumes/MacShare/Code/radar-scene-augmentation/data/annotation_charleston.json")
    annotations = AnnotationSet.load(str(annotation_path))
    converter = RadarConverter(ConversionConfig())
    size = converter.image_size()
    cart_mask = create_water_mask(annotations, size, size)
    polar_mask = PolarMask.from_cartesian(cart_mask, converter)
    num_pulses = converter.num_pulses()
    return polar_mask, num_pulses


def find_water_position(rng, polar_mask, num_pulses, bin_lo, bin_hi, max_attempts=50):
    """Find a random (pulse, bin) position that falls on water.

    Returns (pulse, bin_idx) or None if no valid position found.
    """
    for _ in range(max_attempts):
        pulse = rng.randint(0, num_pulses - 1)
        bin_idx = rng.randint(bin_lo, bin_hi)
        if polar_mask.get(pulse, bin_idx):
            return pulse, bin_idx
    return None


def make_object_group(name, count=1, size=[10, 300], speed=0,
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
            "start": "edge" if bin_idx is None else [360, bin_idx],
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
                count=5,
                size=[10, 300],
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
        make_object_group("target", count=5, size=[10, 300], speed=5,
                          heading=135, intensity_base=1.2),
    ]
    scene = make_scene(SEED_BASE, FRAMES_PER_SCENE, objects)
    write_yaml(str(out / "base.yaml"), scene)
    print("  A2: 1 scene config (decay function varied at apply_trails)")


def generate_a3(base_dir):
    """A3: Intensity mode. Uses same scene as A2."""
    out = base_dir / "a3_intensity"
    objects = [
        make_object_group("target", count=5, size=[10, 300], speed=5,
                          heading=135, intensity_base=1.2),
        make_object_group("weak_target", count=2, size=[10, 100], speed=2,
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
        make_object_group("target", count=5, size=[10, 300], speed=5,
                          heading=135, intensity_base=1.2),
        make_object_group("weak_target", count=2, size=[10, 100], speed=2,
                          heading=45, intensity_base=0.5),
    ]
    scene = make_scene(
        SEED_BASE, FRAMES_PER_SCENE, objects,
        class_map={"target": 0, "weak_target": 0},
    )
    write_yaml(str(out / "mixed_rcs.yaml"), scene)
    print("  A4: 1 scene config (color mapping varied at apply_trails)")


def generate_a5(base_dir):
    """A5: Range dependence. 3 range bands × 10 scenes × 2 variants = 60 configs.

    Each scene has ~15 stationary + ~15 moving targets constrained to a
    specific range band. Moving targets include slow/medium/fast speed tiers.
    Objects are spread across many azimuths to avoid clustering on land.
    Two variants per scene: with clutter and without (noclutter).
    Uses 2-class labels: stationary=0, moving=1.
    """
    import random as pyrandom

    out = base_dir / "a5_range"

    A5_FRAMES = 50
    NUM_SCENES = 10

    # Load water mask for position validation
    polar_mask, NUM_PULSES = load_water_mask()

    # Range bands: (min_bin, max_bin)
    RANGE_BANDS = {
        "near": (60, 100),
        "mid":  (300, 400),
        "far":  (650, 800),
    }

    # Speed tiers for moving targets
    MOVING_TIERS = [
        {"name": "slow",   "speed": 2.0,  "count_edge": 3, "count_interior": 2,
         "size": [80, 500], "variability": 0.15, "duration": [0.6, 1.0]},
        {"name": "medium", "speed": 5.0,  "count_edge": 3, "count_interior": 2,
         "size": [80, 500], "variability": 0.15, "duration": [0.5, 1.0]},
        {"name": "fast",   "speed": 12.0, "count_edge": 3, "count_interior": 2,
         "size": [80, 400], "variability": 0.20, "duration": [0.4, 0.9]},
    ]

    total_configs = 0

    for range_name, (bin_lo, bin_hi) in RANGE_BANDS.items():
        for scene_idx in range(1, NUM_SCENES + 1):
            seed = SEED_BASE + scene_idx * 7 + hash(range_name) % 1000
            rng = pyrandom.Random(seed)

            # --- Build stationary objects with explicit positions on water ---
            stationary_objects = []
            for i in range(15):
                pos = find_water_position(rng, polar_mask, NUM_PULSES, bin_lo, bin_hi)
                if pos is None:
                    print(f"  Warning: could not find water position for stat_{i} "
                          f"in {range_name}_scene_{scene_idx:02d}")
                    continue
                pulse, bin_idx = pos
                stationary_objects.append({
                    "name": f"stat_{i}",
                    "count": 1,
                    "size": [50, 300],
                    "intensity": {
                        "base": 1.0,
                        "variability": 0.1,
                        "profile": "constant",
                    },
                    "flicker": {"enabled": False},
                    "path": {
                        "type": "fixed",
                        "position": [pulse, bin_idx],
                    },
                    "placement": {"margin": 30},
                })

            # --- Build moving objects with start positions on water ---
            moving_objects = []
            for tier in MOVING_TIERS:
                # Edge-start movers
                for i in range(tier["count_edge"]):
                    pos = find_water_position(rng, polar_mask, NUM_PULSES, bin_lo, bin_hi)
                    if pos is None:
                        print(f"  Warning: could not find water position for "
                              f"{tier['name']}_edge_{i} in {range_name}_scene_{scene_idx:02d}")
                        continue
                    pulse, bin_idx = pos
                    heading = rng.uniform(0, 360)
                    obj_name = f"{tier['name']}_edge_{i}"
                    moving_objects.append({
                        "name": obj_name,
                        "count": 1,
                        "size": tier["size"],
                        "intensity": {
                            "base": 1.0,
                            "variability": tier["variability"],
                            "profile": "constant",
                        },
                        "flicker": {"enabled": False},
                        "path": {
                            "type": "linear",
                            "start": [pulse, bin_idx],
                            "heading": round(heading, 1),
                            "speed": tier["speed"],
                            "duration": tier["duration"],
                        },
                        "placement": {"margin": 30},
                    })

                # Interior-start movers
                for i in range(tier["count_interior"]):
                    pos = find_water_position(rng, polar_mask, NUM_PULSES, bin_lo, bin_hi)
                    if pos is None:
                        print(f"  Warning: could not find water position for "
                              f"{tier['name']}_int_{i} in {range_name}_scene_{scene_idx:02d}")
                        continue
                    pulse, bin_idx = pos
                    heading = rng.uniform(0, 360)
                    obj_name = f"{tier['name']}_int_{i}"
                    moving_objects.append({
                        "name": obj_name,
                        "count": 1,
                        "size": tier["size"],
                        "intensity": {
                            "base": 1.0,
                            "variability": tier["variability"],
                            "profile": "constant",
                        },
                        "flicker": {"enabled": False},
                        "path": {
                            "type": "linear",
                            "start": [pulse, bin_idx],
                            "heading": round(heading, 1),
                            "speed": tier["speed"],
                            "duration": tier["duration"],
                        },
                        "placement": {"margin": 30},
                    })

            all_objects = stationary_objects + moving_objects

            # Build class map: stationary=0, moving=1
            class_map = {}
            for obj in stationary_objects:
                class_map[obj["name"]] = 0
            for obj in moving_objects:
                class_map[obj["name"]] = 1

            # --- Clutter variant ---
            scene_clutter = {
                "seed": seed,
                "count": A5_FRAMES,
                "objects": all_objects,
                "clutter": {
                    "num_streaks": 100,
                    "intensity_range": [200, 255],
                    "per_frame": True,
                },
                "labels": {
                    "export": True,
                    "class_map": class_map,
                },
            }
            fname_clutter = f"a5_{range_name}_scene_{scene_idx:02d}.yaml"
            write_yaml(str(out / fname_clutter), scene_clutter)
            total_configs += 1

            # --- No-clutter variant ---
            scene_noclutter = {
                "seed": seed,
                "count": A5_FRAMES,
                "objects": all_objects,
                "labels": {
                    "export": True,
                    "class_map": class_map,
                },
            }
            fname_noclutter = f"a5_{range_name}_scene_{scene_idx:02d}_noclutter.yaml"
            write_yaml(str(out / fname_noclutter), scene_noclutter)
            total_configs += 1

    print(f"  A5: {total_configs} scene configs (3 bands × 10 scenes × 2 variants)")


def generate_a6(base_dir):
    """A6: Clutter level. 10 scenes × 4 clutter levels = 40 configs.

    Reuses the A1 object template (stationary + slow/medium/fast movers,
    2-class labels) with varying clutter streak counts. The independent
    variable is num_streaks in the clutter block.
    """
    out = base_dir / "a6_clutter"

    A6_FRAMES = 50
    NUM_SCENES = 10

    CLUTTER_LEVELS = {
        "none":     0,
        "low":      50,
        "moderate": 100,
        "heavy":    200,
    }

    # Same object mix as A1 scene configs
    A6_OBJECTS = [
        {"name": "stationary",       "count": 15, "size": [50, 300], "speed": 0,
         "variability": 0.1,  "start": "random"},
        {"name": "slow_edge",        "count": 8,  "size": [80, 500], "speed": 2.0,
         "variability": 0.15, "start": "edge",   "duration": [0.6, 1.0]},
        {"name": "slow_interior",    "count": 4,  "size": [80, 500], "speed": 2.0,
         "variability": 0.15, "start": "random", "duration": [0.8, 1.0]},
        {"name": "medium_edge",      "count": 7,  "size": [80, 500], "speed": 5.0,
         "variability": 0.15, "start": "edge",   "duration": [0.5, 1.0]},
        {"name": "medium_interior",  "count": 4,  "size": [80, 500], "speed": 5.0,
         "variability": 0.15, "start": "random", "duration": [0.7, 1.0]},
        {"name": "fast_edge",        "count": 8,  "size": [80, 400], "speed": 12.0,
         "variability": 0.2,  "start": "edge",   "duration": [0.4, 0.9]},
        {"name": "fast_interior",    "count": 4,  "size": [80, 400], "speed": 12.0,
         "variability": 0.2,  "start": "random", "duration": [0.6, 0.9]},
    ]

    CLASS_MAP = {
        "stationary": 0,
        "slow_edge": 1, "slow_interior": 1,
        "medium_edge": 1, "medium_interior": 1,
        "fast_edge": 1, "fast_interior": 1,
    }

    def _build_objects():
        groups = []
        for spec in A6_OBJECTS:
            g = {
                "name": spec["name"],
                "count": spec["count"],
                "size": spec["size"],
                "intensity": {
                    "base": 1.0,
                    "variability": spec["variability"],
                    "profile": "constant",
                },
                "flicker": {"enabled": False},
                "placement": {"margin": 30},
            }
            if spec["speed"] == 0:
                g["path"] = {"type": "fixed", "position": "random"}
            else:
                g["path"] = {
                    "type": "linear",
                    "start": spec["start"],
                    "heading": "random",
                    "speed": spec["speed"],
                    "duration": spec["duration"],
                }
            groups.append(g)
        return groups

    total = 0
    for scene_idx in range(1, NUM_SCENES + 1):
        seed = SEED_BASE + scene_idx * 7
        for level_name, num_streaks in CLUTTER_LEVELS.items():
            scene = {
                "seed": seed,
                "count": A6_FRAMES,
                "objects": _build_objects(),
            }
            if num_streaks > 0:
                scene["clutter"] = {
                    "num_streaks": num_streaks,
                    "intensity_range": [200, 255],
                    "per_frame": True,
                }
            scene["labels"] = {
                "export": True,
                "class_map": dict(CLASS_MAP),
            }
            fname = f"a6_scene_{scene_idx:02d}_{level_name}.yaml"
            write_yaml(str(out / fname), scene)
            total += 1

    print(f"  A6: {total} scene configs ({NUM_SCENES} scenes × {len(CLUTTER_LEVELS)} clutter levels)")


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
            make_object_group("target_a", count=1, size=[10, 300], speed=0,
                              intensity_base=1.0, position=[360, bin_a]),
            make_object_group("target_b", count=1, size=[10, 300], speed=0,
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
            make_object_group("target_a", count=1, size=[10, 300], speed=5,
                              heading=0, intensity_base=1.2),
            make_object_group("target_b", count=1, size=[10, 300], speed=5,
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
