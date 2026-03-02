"""Consolidated radar utilities for path visualization.

Contains only the code paths exercised by visualize_paths.py, extracted from:
  radar_core/csv_handler.py, annotations.py, converter.py, mask.py,
  scene.py, expressions.py, motion.py, and pipeline/data_loader.py.
"""

import json
import math
import uuid
import warnings
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import yaml


# ---------------------------------------------------------------------------
# Constants (from csv_handler.py)
# ---------------------------------------------------------------------------

NUM_RANGE_BINS: int = 868


# ---------------------------------------------------------------------------
# Annotations (from annotations.py)
# ---------------------------------------------------------------------------

SCHEMA_VERSION = "1.0.0"


@dataclass
class Point:
    x: float
    y: float

    def to_pixels(self, width: int, height: int) -> Tuple[int, int]:
        return (int(self.x * width), int(self.y * height))


@dataclass
class Polygon:
    exterior: List[Point]
    holes: List[List[Point]] = field(default_factory=list)

    def contains(self, point: Point) -> bool:
        if not _point_in_polygon(point, self.exterior):
            return False
        for hole in self.holes:
            if _point_in_polygon(point, hole):
                return False
        return True

    def bounding_box(self) -> Tuple[Point, Point]:
        if not self.exterior:
            return (Point(0.0, 0.0), Point(0.0, 0.0))
        min_x = min(p.x for p in self.exterior)
        min_y = min(p.y for p in self.exterior)
        max_x = max(p.x for p in self.exterior)
        max_y = max(p.y for p in self.exterior)
        return (Point(min_x, min_y), Point(max_x, max_y))


def _point_in_polygon(point: Point, polygon: List[Point]) -> bool:
    if len(polygon) < 3:
        return False
    inside = False
    n = len(polygon)
    j = n - 1
    for i in range(n):
        pi = polygon[i]
        pj = polygon[j]
        if ((pi.y > point.y) != (pj.y > point.y)) and \
           (point.x < (pj.x - pi.x) * (point.y - pi.y) / (pj.y - pi.y) + pi.x):
            inside = not inside
        j = i
    return inside


class RegionType(str, Enum):
    WATER = "water"
    LAND = "land"
    EXCLUDE = "exclude"


@dataclass
class Region:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: Optional[str] = None
    region_type: RegionType = RegionType.WATER
    polygon: Polygon = field(default_factory=lambda: Polygon([]))
    z_order: int = 0
    color: Optional[str] = None
    visible: bool = True
    locked: bool = False
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def contains(self, point: Point) -> bool:
        return self.polygon.contains(point)


@dataclass
class ImageDimensions:
    width: int
    height: int


@dataclass
class SourceInfo:
    path: str
    checksum: Optional[str] = None
    image_dimensions: Optional[ImageDimensions] = None


@dataclass
class Metadata:
    created_at: Optional[str] = None
    modified_at: Optional[str] = None
    author: Optional[str] = None
    notes: Optional[str] = None
    tool_version: Optional[str] = None


class CoordinateSystem(str, Enum):
    NORMALIZED = "normalized"
    PIXEL = "pixel"


@dataclass
class AnnotationSet:
    version: str = SCHEMA_VERSION
    source: SourceInfo = field(default_factory=lambda: SourceInfo(path=""))
    metadata: Metadata = field(default_factory=Metadata)
    coordinate_system: CoordinateSystem = CoordinateSystem.NORMALIZED
    regions: List[Region] = field(default_factory=list)

    def regions_by_type(self, region_type: RegionType) -> List[Region]:
        return [r for r in self.regions if r.region_type == region_type]

    @staticmethod
    def load(path: str) -> "AnnotationSet":
        with open(path, "r") as f:
            data = json.load(f)
        return _annotation_set_from_dict(data)


def _point_from_dict(d: dict) -> Point:
    return Point(x=d["x"], y=d["y"])


def _polygon_from_dict(d: dict) -> Polygon:
    exterior = [_point_from_dict(pt) for pt in d.get("exterior", [])]
    holes = [[_point_from_dict(pt) for pt in hole] for hole in d.get("holes", [])]
    return Polygon(exterior=exterior, holes=holes)


def _region_from_dict(d: dict) -> Region:
    return Region(
        id=d.get("id", str(uuid.uuid4())),
        name=d.get("name"),
        region_type=RegionType(d.get("region_type", "water")),
        polygon=_polygon_from_dict(d.get("polygon", {})),
        z_order=d.get("z_order", 0),
        color=d.get("color"),
        visible=d.get("visible", True),
        locked=d.get("locked", False),
        notes=d.get("notes"),
        tags=d.get("tags", []),
    )


def _annotation_set_from_dict(d: dict) -> AnnotationSet:
    src = d.get("source", {})
    source = SourceInfo(path=src.get("path", ""))
    source.checksum = src.get("checksum")
    if "image_dimensions" in src:
        source.image_dimensions = ImageDimensions(
            width=src["image_dimensions"]["width"],
            height=src["image_dimensions"]["height"],
        )

    meta_d = d.get("metadata", {})
    metadata = Metadata(
        created_at=meta_d.get("created_at"),
        modified_at=meta_d.get("modified_at"),
        author=meta_d.get("author"),
        notes=meta_d.get("notes"),
        tool_version=meta_d.get("tool_version"),
    )

    cs_val = d.get("coordinate_system", "normalized")
    try:
        cs = CoordinateSystem(cs_val)
    except ValueError:
        cs = CoordinateSystem.NORMALIZED

    regions = [_region_from_dict(r) for r in d.get("regions", [])]

    return AnnotationSet(
        version=d.get("version", SCHEMA_VERSION),
        source=source,
        metadata=metadata,
        coordinate_system=cs,
        regions=regions,
    )


# ---------------------------------------------------------------------------
# Converter (from converter.py)
# ---------------------------------------------------------------------------

@dataclass
class ConversionConfig:
    image_size: int = 1735
    num_pulses: int = 720
    max_gap_degrees: float = 1.0


class RadarConverter:
    def __init__(self, config: ConversionConfig = None):
        if config is None:
            config = ConversionConfig()
        self.config = config
        self._pulse_idx_lut: np.ndarray = None
        self._bin_idx_lut: np.ndarray = None
        self._valid_lut: np.ndarray = None
        self._build_lut()

    def _build_lut(self):
        size = self.config.image_size
        num_pulses = self.config.num_pulses
        center = size / 2.0
        max_radius = center

        ys = np.arange(size, dtype=np.float64)
        xs = np.arange(size, dtype=np.float64)
        yy, xx = np.meshgrid(ys, xs, indexing='ij')

        dx = xx - center
        dy = center - yy

        r = np.sqrt(dx * dx + dy * dy)
        r_norm = r / max_radius

        valid = r_norm <= 1.0

        theta = np.arctan2(dx, dy)
        theta_norm = np.where(theta < 0, theta + 2.0 * math.pi, theta)

        pulse_idx = ((theta_norm / (2.0 * math.pi)) * num_pulses).astype(np.int32) % num_pulses
        bin_idx = (r_norm * NUM_RANGE_BINS).astype(np.int32)
        bin_idx = np.minimum(bin_idx, NUM_RANGE_BINS - 1)

        self._pulse_idx_lut = pulse_idx.ravel()
        self._bin_idx_lut = bin_idx.ravel()
        self._valid_lut = valid.ravel()

    def polar_to_cartesian_point(self, angle_rad: float, range_bin: int):
        size = self.config.image_size
        center = size / 2.0
        max_radius = center

        r_norm = range_bin / NUM_RANGE_BINS
        r = r_norm * max_radius

        x = center + r * math.sin(angle_rad)
        y = center - r * math.cos(angle_rad)
        return (x, y)

    def cartesian_mask_to_polar(self, mask_flat: np.ndarray) -> np.ndarray:
        size = self.config.image_size
        num_pulses = self.config.num_pulses

        assert mask_flat.size == size * size, "Mask size must match image size"

        polar_mask = np.zeros((num_pulses, NUM_RANGE_BINS), dtype=bool)
        valid = self._valid_lut
        valid_mask = mask_flat[valid] if mask_flat.dtype == bool else mask_flat.astype(bool)[valid]
        p_idx = self._pulse_idx_lut[valid]
        b_idx = self._bin_idx_lut[valid]

        true_indices = valid_mask
        polar_mask[p_idx[true_indices], b_idx[true_indices]] = True

        return polar_mask

    def polar_mask_to_cartesian(self, polar_mask: np.ndarray) -> np.ndarray:
        size = self.config.image_size
        mask = np.zeros(size * size, dtype=bool)
        valid = self._valid_lut
        mask[valid] = polar_mask[self._pulse_idx_lut[valid], self._bin_idx_lut[valid]]
        return mask

    def image_size(self) -> int:
        return self.config.image_size

    def num_pulses(self) -> int:
        return self.config.num_pulses


# ---------------------------------------------------------------------------
# Mask (from mask.py)
# ---------------------------------------------------------------------------

class BinaryMask:
    def __init__(self, width: int, height: int, fill: bool = False):
        self.width = width
        self.height = height
        self.data = np.full((height, width), fill, dtype=bool)

    @classmethod
    def empty(cls, width: int, height: int) -> "BinaryMask":
        return cls(width, height, False)

    def fill_polygon(self, polygon, value: bool = True):
        """Fill a polygon region. Uses point-in-polygon test matching the Rust version."""
        min_pt, max_pt = polygon.bounding_box()
        min_x = int(math.floor(min_pt.x * self.width))
        min_y = int(math.floor(min_pt.y * self.height))
        max_x = int(math.ceil(max_pt.x * self.width))
        max_y = int(math.ceil(max_pt.y * self.height))

        for y in range(max(min_y, 0), min(max_y, self.height)):
            for x in range(max(min_x, 0), min(max_x, self.width)):
                norm_x = x / self.width
                norm_y = y / self.height
                point = Point(norm_x, norm_y)
                if polygon.contains(point):
                    self.data[y, x] = value

    def fill_region(self, region, value: bool = True):
        self.fill_polygon(region.polygon, value)

    def subtract(self, other: "BinaryMask"):
        self.data = np.logical_and(self.data, np.logical_not(other.data))

    @property
    def flat_data(self) -> np.ndarray:
        """Return flat bool array in row-major order (y*width+x) for converter compatibility."""
        return self.data.ravel()


def create_water_mask(annotations: AnnotationSet, width: int, height: int) -> BinaryMask:
    mask = BinaryMask.empty(width, height)
    water_regions = sorted(annotations.regions_by_type(RegionType.WATER), key=lambda r: r.z_order)
    for region in water_regions:
        mask.fill_region(region, True)

    land_regions = sorted(annotations.regions_by_type(RegionType.LAND), key=lambda r: r.z_order)
    for land_region in land_regions:
        land_mask = BinaryMask.empty(width, height)
        land_mask.fill_region(land_region, True)
        mask.subtract(land_mask)

    return mask


class PolarMask:
    def __init__(self, num_pulses: int, fill: bool = False):
        self.num_pulses = num_pulses
        self.num_bins = NUM_RANGE_BINS
        self.data = np.full((num_pulses, NUM_RANGE_BINS), fill, dtype=bool)

    @classmethod
    def from_cartesian(cls, cartesian: BinaryMask, converter: RadarConverter) -> "PolarMask":
        polar_data = converter.cartesian_mask_to_polar(cartesian.flat_data)
        mask = cls(polar_data.shape[0], False)
        mask.data = polar_data
        return mask

    def get(self, pulse_idx: int, bin_idx: int) -> bool:
        if 0 <= pulse_idx < self.num_pulses and 0 <= bin_idx < self.num_bins:
            return bool(self.data[pulse_idx, bin_idx])
        return False


# ---------------------------------------------------------------------------
# Scene (from scene.py — kept in full)
# ---------------------------------------------------------------------------

@dataclass
class FlickerConfig:
    enabled: bool = False
    rate: float = 0.3
    primary_frames: List[int] = field(default_factory=lambda: [15, 50])
    flicker_frames: List[int] = field(default_factory=lambda: [2, 6])
    intensity_drop: float = 0.4


@dataclass
class IntensityConfig:
    base: float = 1.0
    variability: float = 0.1
    profile: str = "constant"
    period: int = 30
    amplitude: float = 0.3
    ramp_start: float = 0.2
    ramp_end: float = 1.5
    expression: str = ""


@dataclass
class PathConfig:
    type: str = "fixed"
    position: Any = "random"           # [p, b] or "random"
    start: Any = "edge"                # [p, b], "edge", or "random"
    end: Any = "edge"                  # [p, b], "edge", or "random"
    heading: Any = 0.0                 # degrees, or "random"
    speed: Any = 1.0                   # number or expression string
    curvature: float = 0.4
    points: List[List[int]] = field(default_factory=list)
    smoothing: str = "cubic"           # cubic | linear | none
    loop: bool = False
    pulse_expr: str = ""               # equation type
    bin_expr: str = ""                 # equation type
    duration: List[float] = field(default_factory=lambda: [0.4, 0.9])
    allow_land: bool = False           # if True, snap to water; if False, truncate path


@dataclass
class PlacementConfig:
    margin: int = 50
    prefer_edge: bool = False


@dataclass
class ObjectGroupConfig:
    name: str = ""
    count: int = 1
    size: Any = "medium"               # "small"|"medium"|"large"|[min, max]
    intensity: IntensityConfig = field(default_factory=IntensityConfig)
    flicker: FlickerConfig = field(default_factory=FlickerConfig)
    path: PathConfig = field(default_factory=PathConfig)
    placement: PlacementConfig = field(default_factory=PlacementConfig)


@dataclass
class ClutterConfig:
    num_streaks: int = 30
    intensity_range: Tuple[int, int] = (40, 180)
    per_frame: bool = True


@dataclass
class LabelConfig:
    export: bool = True
    class_map: Dict[str, int] = field(default_factory=dict)


@dataclass
class SceneConfig:
    seed: Optional[int] = None
    count: int = 200
    objects: List[ObjectGroupConfig] = field(default_factory=list)
    labels: LabelConfig = field(default_factory=LabelConfig)
    clutter: Optional[ClutterConfig] = None


def _parse_flicker(d: Optional[Dict]) -> FlickerConfig:
    if d is None:
        return FlickerConfig()
    return FlickerConfig(
        enabled=d.get("enabled", False),
        rate=float(d.get("rate", 0.3)),
        primary_frames=list(d.get("primary_frames", [15, 50])),
        flicker_frames=list(d.get("flicker_frames", [2, 6])),
        intensity_drop=float(d.get("intensity_drop", 0.4)),
    )


def _parse_intensity(d: Optional[Dict]) -> IntensityConfig:
    if d is None:
        return IntensityConfig()
    return IntensityConfig(
        base=float(d.get("base", 1.0)),
        variability=float(d.get("variability", 0.1)),
        profile=str(d.get("profile", "constant")),
        period=int(d.get("period", 30)),
        amplitude=float(d.get("amplitude", 0.3)),
        ramp_start=float(d.get("ramp_start", 0.2)),
        ramp_end=float(d.get("ramp_end", 1.5)),
        expression=str(d.get("expression", "")),
    )


def _parse_path(d: Optional[Dict]) -> PathConfig:
    if d is None:
        return PathConfig()
    cfg = PathConfig(
        type=str(d.get("type", "fixed")),
        position=d.get("position", "random"),
        start=d.get("start", "edge"),
        end=d.get("end", "edge"),
        heading=d.get("heading", 0.0) if d.get("heading") == "random" else float(d.get("heading", 0.0)),
        speed=d.get("speed", 1.0),
        curvature=float(d.get("curvature", 0.4)),
        points=[list(p) for p in d.get("points", [])],
        smoothing=str(d.get("smoothing", "cubic")),
        loop=bool(d.get("loop", False)),
        pulse_expr=str(d.get("pulse", "")),
        bin_expr=str(d.get("bin", "")),
        duration=list(d.get("duration", [0.4, 0.9])),
        allow_land=bool(d.get("allow_land", False)),
    )
    return cfg


def _parse_placement(d: Optional[Dict]) -> PlacementConfig:
    if d is None:
        return PlacementConfig()
    return PlacementConfig(
        margin=int(d.get("margin", 50)),
        prefer_edge=bool(d.get("prefer_edge", False)),
    )


def _parse_object_group(d: Dict) -> ObjectGroupConfig:
    return ObjectGroupConfig(
        name=str(d.get("name", "")),
        count=int(d.get("count", 1)),
        size=d.get("size", "medium"),
        intensity=_parse_intensity(d.get("intensity")),
        flicker=_parse_flicker(d.get("flicker")),
        path=_parse_path(d.get("path")),
        placement=_parse_placement(d.get("placement")),
    )


def _parse_clutter(d: Optional[Dict]) -> Optional[ClutterConfig]:
    if d is None:
        return None
    intensity = d.get("intensity_range", [40, 180])
    return ClutterConfig(
        num_streaks=int(d.get("num_streaks", 30)),
        intensity_range=(int(intensity[0]), int(intensity[1])),
        per_frame=bool(d.get("per_frame", True)),
    )


def _parse_labels(d: Optional[Dict]) -> LabelConfig:
    if d is None:
        return LabelConfig()
    return LabelConfig(
        export=bool(d.get("export", True)),
        class_map=dict(d.get("class_map", {})),
    )


def load_scene(path: str) -> SceneConfig:
    """Load a scene profile from a YAML file."""
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    if raw is None:
        raw = {}

    objects = [_parse_object_group(o) for o in raw.get("objects", [])]

    return SceneConfig(
        seed=raw.get("seed"),
        count=int(raw.get("count", 200)),
        objects=objects,
        labels=_parse_labels(raw.get("labels")),
        clutter=_parse_clutter(raw.get("clutter")),
    )


# ---------------------------------------------------------------------------
# Expressions (from expressions.py — kept in full)
# ---------------------------------------------------------------------------

SAFE_MATH = {
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "sqrt": math.sqrt,
    "abs": abs,
    "pi": math.pi,
    "min": min,
    "max": max,
    "log": math.log,
    "exp": math.exp,
}


def safe_eval(expression: str, variables: dict) -> float:
    """Evaluate a math expression with whitelisted functions and variables."""
    ns = dict(SAFE_MATH)
    ns.update(variables)
    try:
        return float(eval(expression, {"__builtins__": {}}, ns))
    except Exception as e:
        raise ValueError(f"Failed to evaluate expression '{expression}': {e}")


# ---------------------------------------------------------------------------
# Motion (from motion.py — kept in full)
# ---------------------------------------------------------------------------

def eval_speed(speed_spec: Any, t: int) -> float:
    """Evaluate speed -- either a constant number or an expression string."""
    if isinstance(speed_spec, (int, float)):
        return float(speed_spec)
    return safe_eval(str(speed_spec), {"t": t})


def resolve_position(spec, valid_positions, edge_positions, rng) -> Tuple[int, int]:
    """Resolve a position specification to (pulse, bin).

    spec: "random", "edge", or [pulse, bin]
    """
    if isinstance(spec, str):
        if spec == "random":
            return tuple(rng.choice(valid_positions))
        elif spec == "edge":
            if edge_positions:
                return tuple(rng.choice(edge_positions))
            return tuple(rng.choice(valid_positions))
        else:
            raise ValueError(f"Unknown position spec: {spec}")
    elif isinstance(spec, (list, tuple)) and len(spec) == 2:
        return (int(spec[0]), int(spec[1]))
    raise ValueError(f"Invalid position spec: {spec}")


def validate_edge_start(position: Tuple[int, int], edge_positions: List[Tuple[int, int]],
                        water_mask, num_pulses: int, tolerance: int = 10) -> bool:
    """Check if position is at an edge (water/land boundary or radar coverage boundary)."""
    p, b = position
    if b < 60 or b > NUM_RANGE_BINS - 60:
        return True
    for ep, eb in edge_positions:
        dp = min(abs(p - ep), num_pulses - abs(p - ep))
        db = abs(b - eb)
        if dp <= tolerance and db <= tolerance:
            return True
    return False


def snap_to_water(pulse: int, bin_idx: int, water_mask, num_pulses: int,
                  max_radius: int = 20) -> Optional[Tuple[int, int]]:
    """Find nearest valid water pixel via expanding search."""
    for r in range(0, max_radius + 1):
        for dp in range(-r, r + 1):
            for db in range(-r, r + 1):
                if abs(dp) != r and abs(db) != r:
                    continue
                p = (pulse + dp) % num_pulses
                b = bin_idx + db
                if 0 <= b < NUM_RANGE_BINS and water_mask.get(p, b):
                    return (p, b)
    return None


def _validate_point(pulse: int, bin_idx: int, water_mask, num_pulses: int,
                    allow_land: bool = False) -> Optional[Tuple[int, int]]:
    """Validate a point against water mask."""
    pulse = pulse % num_pulses
    bin_idx = max(0, min(bin_idx, NUM_RANGE_BINS - 1))
    if water_mask.get(pulse, bin_idx):
        return (pulse, bin_idx)
    if allow_land:
        result = snap_to_water(pulse, bin_idx, water_mask, num_pulses)
        if result:
            warnings.warn(f"Position ({pulse}, {bin_idx}) is on land, snapped to {result}")
            return result
        warnings.warn(f"Position ({pulse}, {bin_idx}) is on land, no nearby water found")
        return (pulse, bin_idx)
    return None


def generate_path(path_config: PathConfig, total_frames: int,
                  valid_positions: List[Tuple[int, int]],
                  edge_positions: List[Tuple[int, int]],
                  water_mask, num_pulses: int, rng,
                  allow_land: bool = False) -> Tuple[List[Tuple[int, int]], int, int]:
    """Generate a path according to config.

    Returns: (positions, start_frame, end_frame)
    positions has one entry per active frame.
    """
    path_type = path_config.type
    effective_allow_land = path_config.allow_land or allow_land

    if path_type == "fixed":
        return _path_fixed(path_config, total_frames, valid_positions, edge_positions,
                           water_mask, num_pulses, rng, effective_allow_land)
    elif path_type == "linear":
        return _path_linear(path_config, total_frames, valid_positions, edge_positions,
                            water_mask, num_pulses, rng, effective_allow_land)
    elif path_type == "bezier":
        return _path_bezier(path_config, total_frames, valid_positions, edge_positions,
                            water_mask, num_pulses, rng, effective_allow_land)
    elif path_type == "waypoints":
        return _path_waypoints(path_config, total_frames, valid_positions, edge_positions,
                               water_mask, num_pulses, rng, effective_allow_land)
    elif path_type == "equation":
        return _path_equation(path_config, total_frames, valid_positions, edge_positions,
                              water_mask, num_pulses, rng, effective_allow_land)
    else:
        raise ValueError(f"Unknown path type: {path_type}")


def _compute_duration_frames(duration: List[float], total_frames: int, rng) -> Tuple[int, int]:
    """Compute start_frame, end_frame from duration fraction spec."""
    frac = rng.uniform(duration[0], duration[1]) if len(duration) == 2 else duration[0]
    active_frames = max(1, int(total_frames * frac))
    max_start = total_frames - active_frames
    start_frame = rng.randint(0, max(0, max_start))
    end_frame = min(start_frame + active_frames, total_frames)
    return start_frame, end_frame


def _path_fixed(config, total_frames, valid_positions, edge_positions,
                water_mask, num_pulses, rng, allow_land=False):
    pos = resolve_position(config.position, valid_positions, edge_positions, rng)
    validated = _validate_point(pos[0], pos[1], water_mask, num_pulses, allow_land=True)
    positions = [validated] * total_frames
    return positions, 0, total_frames


def _is_radar_edge(bin_idx: int, threshold: int = 60) -> bool:
    """Check if a bin index is at the radar coverage boundary."""
    return bin_idx < threshold or bin_idx > NUM_RANGE_BINS - threshold


def _filter_land_edges(edge_positions: List[Tuple[int, int]],
                       threshold: int = 60) -> List[Tuple[int, int]]:
    """Return only land/water boundary edges, excluding radar coverage edges."""
    land_edges = [(p, b) for p, b in edge_positions if not _is_radar_edge(b, threshold)]
    return land_edges if land_edges else edge_positions


def _path_linear(config, total_frames, valid_positions, edge_positions,
                 water_mask, num_pulses, rng, allow_land=False):
    max_attempts = 20
    min_useful_frames = max(5, int(total_frames * 0.1))

    land_edges = _filter_land_edges(edge_positions)

    positions = []
    start_frame = 0

    for attempt in range(max_attempts):
        start = resolve_position(config.start, valid_positions, land_edges, rng)

        if config.start != "random" and not validate_edge_start(start, edge_positions, water_mask, num_pulses):
            continue

        start_frame, end_frame = _compute_duration_frames(config.duration, total_frames, rng)
        active_frames = end_frame - start_frame

        heading_deg = rng.uniform(0, 360) if config.heading == "random" else float(config.heading)
        heading_rad = math.radians(heading_deg)
        dp_per_unit = math.sin(heading_rad)
        db_per_unit = -math.cos(heading_rad)

        positions = []
        cumulative_p = float(start[0])
        cumulative_b = float(start[1])

        for t in range(active_frames):
            spd = eval_speed(config.speed, t)
            if t > 0:
                cumulative_p += dp_per_unit * spd
                cumulative_b += db_per_unit * spd

            pulse = int(cumulative_p) % num_pulses
            bin_idx = max(0, min(int(cumulative_b), NUM_RANGE_BINS - 1))
            validated = _validate_point(pulse, bin_idx, water_mask, num_pulses, allow_land)
            if validated is None:
                break
            positions.append(validated)

        ends_at_radar = positions and _is_radar_edge(positions[-1][1])
        if len(positions) >= min_useful_frames and not ends_at_radar:
            actual_end = start_frame + len(positions)
            return positions, start_frame, actual_end

    actual_end = start_frame + len(positions)
    return positions, start_frame, actual_end


def _path_bezier(config, total_frames, valid_positions, edge_positions,
                 water_mask, num_pulses, rng, allow_land=False):
    start = resolve_position(config.start, valid_positions, edge_positions, rng)
    end = resolve_position(config.end, valid_positions, edge_positions, rng)

    if not validate_edge_start(start, edge_positions, water_mask, num_pulses):
        raise ValueError(f"Bezier start {start} is not at an edge.")

    start_frame, end_frame = _compute_duration_frames(config.duration, total_frames, rng)
    active_frames = end_frame - start_frame

    mid_p = (start[0] + end[0]) / 2.0
    mid_b = (start[1] + end[1]) / 2.0
    dx = float(end[0] - start[0])
    dy = float(end[1] - start[1])
    length = max(math.sqrt(dx * dx + dy * dy), 1.0)
    perp_x = -dy / length
    perp_y = dx / length
    curve_sign = 1.0 if rng.random() < 0.5 else -1.0
    offset = config.curvature * length * 0.5 * curve_sign
    ctrl_p = mid_p + perp_x * offset
    ctrl_b = mid_b + perp_y * offset

    num_samples = max(active_frames * 4, 200)
    raw_points = []
    for i in range(num_samples + 1):
        u = i / num_samples
        u1 = 1.0 - u
        p = u1 * u1 * start[0] + 2.0 * u1 * u * ctrl_p + u * u * end[0]
        b = u1 * u1 * start[1] + 2.0 * u1 * u * ctrl_b + u * u * end[1]
        raw_points.append((p, b))

    arc_lengths = [0.0]
    for i in range(1, len(raw_points)):
        dp = raw_points[i][0] - raw_points[i - 1][0]
        db = raw_points[i][1] - raw_points[i - 1][1]
        arc_lengths.append(arc_lengths[-1] + math.sqrt(dp * dp + db * db))
    total_arc = arc_lengths[-1]

    positions = []
    dist = 0.0
    for t in range(active_frames):
        spd = eval_speed(config.speed, t)
        if t > 0:
            dist += spd
        if dist > total_arc:
            dist = total_arc

        idx = 0
        for j in range(1, len(arc_lengths)):
            if arc_lengths[j] >= dist:
                idx = j - 1
                break
        else:
            idx = len(arc_lengths) - 2

        seg_len = arc_lengths[idx + 1] - arc_lengths[idx]
        frac = (dist - arc_lengths[idx]) / seg_len if seg_len > 0 else 0.0
        p = raw_points[idx][0] + frac * (raw_points[idx + 1][0] - raw_points[idx][0])
        b = raw_points[idx][1] + frac * (raw_points[idx + 1][1] - raw_points[idx][1])

        pulse = int(p) % num_pulses
        bin_idx = max(0, min(int(b), NUM_RANGE_BINS - 1))
        validated = _validate_point(pulse, bin_idx, water_mask, num_pulses, allow_land)
        if validated is None:
            break
        positions.append(validated)

    actual_end = start_frame + len(positions)
    return positions, start_frame, actual_end


def _path_waypoints(config, total_frames, valid_positions, edge_positions,
                    water_mask, num_pulses, rng, allow_land=False):
    points = config.points
    if len(points) < 2:
        raise ValueError("Waypoints path requires at least 2 points")

    for pt in points:
        p, b = int(pt[0]), int(pt[1])
        if not water_mask.get(p % num_pulses, max(0, min(b, NUM_RANGE_BINS - 1))):
            raise ValueError(f"Waypoint ({p}, {b}) is on land. Fix the YAML.")

    first = (int(points[0][0]), int(points[0][1]))
    if not validate_edge_start(first, edge_positions, water_mask, num_pulses):
        raise ValueError(f"Waypoints start {first} is not at an edge.")

    start_frame, end_frame = _compute_duration_frames(config.duration, total_frames, rng)
    active_frames = end_frame - start_frame

    pts_p = [float(pt[0]) for pt in points]
    pts_b = [float(pt[1]) for pt in points]

    if config.loop:
        pts_p.append(pts_p[0])
        pts_b.append(pts_b[0])

    n = len(pts_p)

    if config.smoothing == "cubic" and n >= 4:
        raw_points = _cubic_spline_sample(pts_p, pts_b, max(active_frames * 4, 200))
    elif config.smoothing == "linear" or n < 4:
        raw_points = _linear_interp_sample(pts_p, pts_b, max(active_frames * 4, 200))
    else:
        raw_points = _linear_interp_sample(pts_p, pts_b, max(active_frames * 4, 200))

    arc_lengths = [0.0]
    for i in range(1, len(raw_points)):
        dp = raw_points[i][0] - raw_points[i - 1][0]
        db = raw_points[i][1] - raw_points[i - 1][1]
        arc_lengths.append(arc_lengths[-1] + math.sqrt(dp * dp + db * db))
    total_arc = arc_lengths[-1]

    positions = []
    dist = 0.0
    for t in range(active_frames):
        spd = eval_speed(config.speed, t)
        if t > 0:
            dist += spd
        if config.loop and dist > total_arc:
            dist = dist % total_arc if total_arc > 0 else 0.0
        elif dist > total_arc:
            dist = total_arc

        idx = 0
        for j in range(1, len(arc_lengths)):
            if arc_lengths[j] >= dist:
                idx = j - 1
                break
        else:
            idx = len(arc_lengths) - 2

        seg_len = arc_lengths[idx + 1] - arc_lengths[idx]
        frac = (dist - arc_lengths[idx]) / seg_len if seg_len > 0 else 0.0
        p = raw_points[idx][0] + frac * (raw_points[idx + 1][0] - raw_points[idx][0])
        b = raw_points[idx][1] + frac * (raw_points[idx + 1][1] - raw_points[idx][1])

        pulse = int(p) % num_pulses
        bin_idx = max(0, min(int(b), NUM_RANGE_BINS - 1))
        validated = _validate_point(pulse, bin_idx, water_mask, num_pulses, allow_land)
        if validated is None:
            break
        positions.append(validated)

    actual_end = start_frame + len(positions)
    return positions, start_frame, actual_end


def _linear_interp_sample(pts_p, pts_b, num_samples):
    """Linearly interpolate between waypoints."""
    n = len(pts_p)
    result = []
    for i in range(num_samples + 1):
        t = i / num_samples * (n - 1)
        idx = min(int(t), n - 2)
        frac = t - idx
        p = pts_p[idx] + frac * (pts_p[idx + 1] - pts_p[idx])
        b = pts_b[idx] + frac * (pts_b[idx + 1] - pts_b[idx])
        result.append((p, b))
    return result


def _cubic_spline_sample(pts_p, pts_b, num_samples):
    """Cubic spline interpolation through waypoints using numpy."""
    n = len(pts_p)
    result = []
    ts = list(range(n))
    t_interp = [i / num_samples * (n - 1) for i in range(num_samples + 1)]

    p_interp = _natural_cubic_spline(ts, pts_p, t_interp)
    b_interp = _natural_cubic_spline(ts, pts_b, t_interp)

    for p, b in zip(p_interp, b_interp):
        result.append((p, b))
    return result


def _natural_cubic_spline(xs, ys, xs_interp):
    """Simple natural cubic spline implementation."""
    n = len(xs)
    if n < 2:
        return [ys[0]] * len(xs_interp)
    if n == 2:
        return [ys[0] + (ys[1] - ys[0]) * (x - xs[0]) / (xs[1] - xs[0]) for x in xs_interp]
    if n == 3:
        return _linear_interp_vals(xs, ys, xs_interp)

    h = [xs[i + 1] - xs[i] for i in range(n - 1)]
    alpha = [0.0] * n
    for i in range(1, n - 1):
        alpha[i] = (3.0 / h[i] * (ys[i + 1] - ys[i]) - 3.0 / h[i - 1] * (ys[i] - ys[i - 1]))

    l = [1.0] * n
    mu = [0.0] * n
    z = [0.0] * n
    for i in range(1, n - 1):
        l[i] = 2.0 * (xs[i + 1] - xs[i - 1]) - h[i - 1] * mu[i - 1]
        mu[i] = h[i] / l[i]
        z[i] = (alpha[i] - h[i - 1] * z[i - 1]) / l[i]

    c = [0.0] * n
    b_coef = [0.0] * n
    d = [0.0] * n
    for j in range(n - 2, -1, -1):
        c[j] = z[j] - mu[j] * c[j + 1]
        b_coef[j] = (ys[j + 1] - ys[j]) / h[j] - h[j] * (c[j + 1] + 2.0 * c[j]) / 3.0
        d[j] = (c[j + 1] - c[j]) / (3.0 * h[j])

    result = []
    for x in xs_interp:
        idx = min(max(0, int(x)), n - 2)
        for k in range(n - 2, -1, -1):
            if xs[k] <= x:
                idx = k
                break
        dx = x - xs[idx]
        val = ys[idx] + b_coef[idx] * dx + c[idx] * dx * dx + d[idx] * dx * dx * dx
        result.append(val)
    return result


def _linear_interp_vals(xs, ys, xs_interp):
    n = len(xs)
    result = []
    for x in xs_interp:
        idx = min(max(0, int(x)), n - 2)
        for k in range(n - 2, -1, -1):
            if xs[k] <= x:
                idx = k
                break
        frac = (x - xs[idx]) / (xs[idx + 1] - xs[idx]) if xs[idx + 1] != xs[idx] else 0.0
        result.append(ys[idx] + frac * (ys[idx + 1] - ys[idx]))
    return result


def _path_equation(config, total_frames, valid_positions, edge_positions,
                   water_mask, num_pulses, rng, allow_land=False):
    if not config.pulse_expr or not config.bin_expr:
        raise ValueError("Equation path requires 'pulse' and 'bin' expressions")

    start_frame, end_frame = _compute_duration_frames(config.duration, total_frames, rng)
    active_frames = end_frame - start_frame

    center_pulse = num_pulses // 2
    center_bin = NUM_RANGE_BINS // 2
    variables_base = {
        "center_pulse": center_pulse,
        "center_bin": center_bin,
        "num_pulses": num_pulses,
        "num_bins": NUM_RANGE_BINS,
    }

    positions = []
    for t in range(active_frames):
        variables = dict(variables_base)
        variables["t"] = t
        p = safe_eval(config.pulse_expr, variables)
        b = safe_eval(config.bin_expr, variables)
        pulse = int(p) % num_pulses
        bin_idx = max(0, min(int(b), NUM_RANGE_BINS - 1))
        validated = _validate_point(pulse, bin_idx, water_mask, num_pulses, allow_land)
        if validated is None:
            break
        positions.append(validated)

    actual_end = start_frame + len(positions)
    return positions, start_frame, actual_end


# ---------------------------------------------------------------------------
# Position helpers (from data_loader.py)
# ---------------------------------------------------------------------------

def compute_valid_positions(water_mask, num_pulses, margin):
    """Find polar positions that are safely within the water mask."""
    positions = []
    min_land_distance = margin
    min_land_distance_sq = min_land_distance * min_land_distance
    bin_start = min(margin, NUM_RANGE_BINS - 1)
    bin_end = NUM_RANGE_BINS - margin

    for pulse_idx in range(0, num_pulses, 5):
        for bin_idx in range(bin_start, bin_end, 10):
            if not water_mask.get(pulse_idx, bin_idx):
                continue

            is_far_from_land = True
            for dp in range(-min_land_distance, min_land_distance + 1):
                if not is_far_from_land:
                    break
                for db in range(-min_land_distance, min_land_distance + 1):
                    if dp * dp + db * db > min_land_distance_sq:
                        continue
                    b = bin_idx + db
                    if b < 0 or b >= NUM_RANGE_BINS:
                        is_far_from_land = False
                        break
                    p = (pulse_idx + dp) % num_pulses
                    if not water_mask.get(p, b):
                        is_far_from_land = False
                        break

            if is_far_from_land:
                positions.append((pulse_idx, bin_idx))

    return positions


def find_water_edge_positions(water_mask, num_pulses):
    """Find positions at the boundary between water and land/coverage edge."""
    edge_positions = []

    for pulse_idx in range(0, num_pulses, 2):
        for bin_idx in range(10, NUM_RANGE_BINS - 10):
            if not water_mask.get(pulse_idx, bin_idx):
                continue

            is_edge = False

            if bin_idx < 60 or bin_idx > NUM_RANGE_BINS - 60:
                is_edge = True

            if not is_edge:
                for dp in (-2, -1, 0, 1, 2):
                    for db in (-2, -1, 0, 1, 2):
                        if dp == 0 and db == 0:
                            continue
                        p = (pulse_idx + dp) % num_pulses
                        b = max(0, min(bin_idx + db, NUM_RANGE_BINS - 1))
                        if not water_mask.get(p, b):
                            is_edge = True
                            break
                    if is_edge:
                        break

            if is_edge:
                edge_positions.append((pulse_idx, bin_idx))

    return edge_positions
