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
TRAIL_LENGTHS = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25]

# Radar geometry
NUM_RANGE_BINS = 868
MAX_RANGE_NM = 3.0
MAX_RANGE_M = MAX_RANGE_NM * 1852          # 5556 m
METERS_PER_BIN = MAX_RANGE_M / NUM_RANGE_BINS  # ≈ 6.40 m/bin

# Range bins: near (~200m), mid (~1nm ≈ 1852m), far (~3nm ≈ 5556m)
RANGE_BINS = {
    "near": 80,    # ~200m from center
    "mid": 350,    # ~1nm
    "far": 750,    # ~3nm
}

# Proximity separations in meters
PROXIMITY_METERS = list(range(10, 310, 10))

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

    import random as pyrandom

    def _build_objects(rng):
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
                    "heading": round(rng.uniform(0, 360), 1),
                    "speed": spec["speed"],
                    "duration": spec["duration"],
                }
            groups.append(g)
        return groups

    total = 0
    for scene_idx in range(1, NUM_SCENES + 1):
        seed = SEED_BASE + scene_idx * 7
        rng = pyrandom.Random(seed)
        for level_name, num_streaks in CLUTTER_LEVELS.items():
            scene = {
                "seed": seed,
                "count": A6_FRAMES,
                "objects": _build_objects(rng),
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
    """A7: Target proximity. 30 separations (10m to 300m in 10m steps) × 2 variants.

    Two fixed targets at controlled separations. Separation is in range bins,
    placed along the same azimuth. Each separation has a clutter and noclutter
    variant.
    """
    out = base_dir / "a7_proximity"
    center_bin = 400  # mid-range

    A7_FRAMES = 50
    total = 0

    for sep_m in PROXIMITY_METERS:
        sep_bins = max(1, round(sep_m / METERS_PER_BIN))
        bin_a = center_bin - sep_bins // 2
        bin_b = center_bin + sep_bins // 2

        objects = [
            make_object_group("target_a", count=1, size=[10, 300], speed=0,
                              intensity_base=1.0, position=[360, bin_a]),
            make_object_group("target_b", count=1, size=[10, 300], speed=0,
                              intensity_base=1.0, position=[360, bin_b]),
        ]
        class_map = {"target_a": 0, "target_b": 0}

        # With clutter
        scene = make_scene(SEED_BASE, A7_FRAMES, objects, class_map)
        scene["clutter"] = {
            "num_streaks": 100,
            "intensity_range": [200, 255],
            "per_frame": True,
        }
        write_yaml(str(out / f"sep_{sep_m}m.yaml"), scene)
        total += 1

        # Without clutter
        scene_nc = make_scene(SEED_BASE, A7_FRAMES, objects, class_map)
        write_yaml(str(out / f"sep_{sep_m}m_noclutter.yaml"), scene_nc)
        total += 1

    print(f"  A7: {total} scene configs ({len(PROXIMITY_METERS)} separations × 2 clutter variants)")


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
            class_map={"target_a": 1, "target_b": 1},
        )
        write_yaml(str(out / f"angle_{angle}.yaml"), scene)

    print(f"  A8: {len(CROSSING_ANGLES)} scene configs (crossing angles)")


def generate_gp(base_dir):
    """GP: General-purpose 2-class training data. 220 configs across 14 sets.

    Generates diverse scenes with varying object counts, stationary/moving
    ratios, and clutter levels. All use 2-class labels: stationary=0, moving=1.
    50 frames per scene.
    """
    import random as pyrandom

    out = base_dir / "gp_training"

    GP_FRAMES = 50

    # Speed tiers for moving objects (same as A5/A6)
    MOVING_SPEEDS = {
        "slow":   {"speed": 2.0,  "size": [80, 500], "duration": [0.6, 1.0]},
        "medium": {"speed": 5.0,  "size": [80, 500], "duration": [0.5, 1.0]},
        "fast":   {"speed": 12.0, "size": [80, 400], "duration": [0.4, 0.9]},
    }

    # ---------- Scene set definitions ----------
    # Each set: (prefix, num_configs, n_stationary_range, n_moving_range,
    #            clutter_streaks, description, placement_kwargs)
    GP_SETS = [
        # Sparse scenes
        ("gp_sparse_clean",         20, (2, 4),   (3, 4),   0,   {}),
        ("gp_sparse_clutter",       20, (2, 4),   (3, 4),   100, {}),
        # Moderate density
        ("gp_moderate_clean",       20, (8, 12),  (12, 18), 0,   {}),
        ("gp_moderate_low",         20, (8, 12),  (12, 18), 50,  {}),
        ("gp_moderate_heavy",       20, (8, 12),  (12, 18), 200, {}),
        # Dense scenes
        ("gp_dense_clean",          20, (20, 30), (40, 50), 0,   {}),
        ("gp_dense_clutter",        20, (20, 30), (40, 50), 100, {}),
        # Fast movers only
        ("gp_fast_only_clean",      10, (0, 0),   (15, 20), 0,   {}),
        ("gp_fast_only_clutter",    10, (0, 0),   (15, 20), 150, {}),
        # Stationary only
        ("gp_stationary_clean",     10, (15, 20), (0, 0),   0,   {}),
        ("gp_stationary_clutter",   10, (15, 20), (0, 0),   100, {}),
        # Range-focused
        ("gp_near_focus",           10, (10, 15), (15, 20), 75,  {"bin_range": (60, 200)}),
        ("gp_far_focus",            10, (10, 15), (15, 20), 75,  {"bin_range": (550, 800)}),
        # Mixed speed with varied clutter
        ("gp_mixed_speed",          20, (10, 10), (20, 30), -1,  {}),  # -1 = random 0-200
    ]

    def _build_gp_objects(rng, n_stat, n_mov, placement_kwargs):
        """Build object groups for a GP scene."""
        objects = []
        class_map = {}

        # Stationary targets
        if n_stat > 0:
            obj = {
                "name": "stationary",
                "count": n_stat,
                "size": [50, 300],
                "intensity": {"base": 1.0, "variability": 0.1, "profile": "constant"},
                "flicker": {"enabled": False},
                "placement": {"margin": 30},
            }
            if "bin_range" in placement_kwargs:
                lo, hi = placement_kwargs["bin_range"]
                obj["path"] = {"type": "fixed", "position": "random"}
                obj["placement"]["range_min"] = lo
                obj["placement"]["range_max"] = hi
            else:
                obj["path"] = {"type": "fixed", "position": "random"}
            objects.append(obj)
            class_map["stationary"] = 0

        # Moving targets — distribute across speed tiers
        if n_mov > 0:
            tier_names = list(MOVING_SPEEDS.keys())
            per_tier = max(1, n_mov // len(tier_names))
            remainder = n_mov - per_tier * len(tier_names)

            for i, tier_name in enumerate(tier_names):
                tier = MOVING_SPEEDS[tier_name]
                count = per_tier + (1 if i < remainder else 0)
                if count <= 0:
                    continue

                # Split between edge and interior starts
                n_edge = max(1, count * 2 // 3)
                n_int = count - n_edge

                if n_edge > 0:
                    edge_name = f"{tier_name}_edge"
                    edge_obj = {
                        "name": edge_name,
                        "count": n_edge,
                        "size": tier["size"],
                        "intensity": {"base": 1.0, "variability": 0.15, "profile": "constant"},
                        "flicker": {"enabled": False},
                        "path": {
                            "type": "linear",
                            "start": "edge",
                            "heading": round(rng.uniform(0, 360), 1),
                            "speed": tier["speed"],
                            "duration": tier["duration"],
                        },
                        "placement": {"margin": 30},
                    }
                    objects.append(edge_obj)
                    class_map[edge_name] = 1

                if n_int > 0:
                    int_name = f"{tier_name}_interior"
                    int_obj = {
                        "name": int_name,
                        "count": n_int,
                        "size": tier["size"],
                        "intensity": {"base": 1.0, "variability": 0.15, "profile": "constant"},
                        "flicker": {"enabled": False},
                        "path": {
                            "type": "linear",
                            "start": "random",
                            "heading": round(rng.uniform(0, 360), 1),
                            "speed": tier["speed"],
                            "duration": tier["duration"],
                        },
                        "placement": {"margin": 30},
                    }
                    objects.append(int_obj)
                    class_map[int_name] = 1

        return objects, class_map

    total = 0
    for (prefix, num_configs, stat_range, mov_range, clutter, pkwargs) in GP_SETS:
        for scene_idx in range(1, num_configs + 1):
            seed = SEED_BASE + scene_idx * 13 + hash(prefix) % 10000
            rng = pyrandom.Random(seed)

            n_stat = rng.randint(stat_range[0], stat_range[1]) if stat_range[1] > 0 else 0
            n_mov = rng.randint(mov_range[0], mov_range[1]) if mov_range[1] > 0 else 0

            objects, class_map = _build_gp_objects(rng, n_stat, n_mov, pkwargs)

            scene = {
                "seed": seed,
                "count": GP_FRAMES,
                "objects": objects,
                "labels": {
                    "export": True,
                    "class_map": class_map,
                },
            }

            # Clutter
            actual_clutter = clutter
            if clutter == -1:
                actual_clutter = rng.choice([0, 50, 100, 150, 200])
            if actual_clutter > 0:
                scene["clutter"] = {
                    "num_streaks": actual_clutter,
                    "intensity_range": [200, 255],
                    "per_frame": True,
                }

            fname = f"{prefix}_scene_{scene_idx:02d}.yaml"
            write_yaml(str(out / fname), scene)
            total += 1

    print(f"  GP: {total} scene configs (14 sets, diverse density/clutter/speed)")


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
    generate_gp(base_dir)

    total = sum(len(list(d.glob("*.yaml")))
                for d in base_dir.iterdir() if d.is_dir())
    print(f"\nTotal: {total} YAML configs generated in {base_dir}")


if __name__ == "__main__":
    main()
