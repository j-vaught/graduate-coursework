"""
Random clutter generation for synthetic radar data.

This module adds random high-intensity clutter points in water regions
using annotation.json to identify valid placement areas.
"""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np


@dataclass
class ClutterConfig:
    """Configuration for clutter generation.

    Attributes:
        clutter_density: Average number of clutter points per frame.
        intensity_min: Minimum clutter intensity (0-255).
        intensity_max: Maximum clutter intensity (0-255).
        cluster_probability: Probability of generating clustered clutter.
        cluster_size_range: Range of points per cluster (min, max).
        cluster_spread: Spatial spread of cluster points.
        seed: Random seed for reproducibility.
    """

    clutter_density: float = 5.0
    intensity_min: int = 180
    intensity_max: int = 255
    cluster_probability: float = 0.3
    cluster_size_range: Tuple[int, int] = (3, 8)
    cluster_spread: float = 10.0
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.clutter_density < 0:
            raise ValueError("clutter_density must be non-negative")
        if not 0 <= self.intensity_min <= 255:
            raise ValueError("intensity_min must be between 0 and 255")
        if not 0 <= self.intensity_max <= 255:
            raise ValueError("intensity_max must be between 0 and 255")
        if self.intensity_min > self.intensity_max:
            raise ValueError("intensity_min must be <= intensity_max")
        if not 0 <= self.cluster_probability <= 1:
            raise ValueError("cluster_probability must be between 0 and 1")


@dataclass
class WaterRegion:
    """Represents a water region from annotation data.

    Attributes:
        id: Unique region identifier.
        name: Human-readable name.
        polygon: List of (x, y) normalized coordinates for exterior boundary.
        holes: List of polygon holes (exclusion regions).
    """

    id: str
    name: str
    polygon: List[Tuple[float, float]]
    holes: List[List[Tuple[float, float]]]


class AnnotationLoader:
    """Loads and parses annotation.json files for water region data."""

    @staticmethod
    def load_annotations(annotation_path: Union[str, Path]) -> Dict:
        """Load annotation data from JSON file.

        Args:
            annotation_path: Path to annotation.json file.

        Returns:
            Parsed annotation dictionary.
        """
        path = Path(annotation_path)
        if not path.exists():
            raise FileNotFoundError(f"Annotation file not found: {path}")

        with open(path, "r") as f:
            return json.load(f)

    @staticmethod
    def extract_water_regions(annotations: Dict) -> List[WaterRegion]:
        """Extract water regions from annotation data.

        Args:
            annotations: Parsed annotation dictionary.

        Returns:
            List of WaterRegion objects.
        """
        water_regions = []

        regions = annotations.get("regions", [])
        for region in regions:
            if region.get("region_type") == "water":
                polygon_data = region.get("polygon", {})
                exterior = polygon_data.get("exterior", [])
                holes = polygon_data.get("holes", [])

                # Convert to (x, y) tuples
                exterior_coords = [(p["x"], p["y"]) for p in exterior]
                hole_coords = [
                    [(p["x"], p["y"]) for p in hole] for hole in holes
                ]

                water_region = WaterRegion(
                    id=region.get("id", ""),
                    name=region.get("name", ""),
                    polygon=exterior_coords,
                    holes=hole_coords,
                )
                water_regions.append(water_region)

        return water_regions


class PolygonUtils:
    """Utility functions for polygon operations."""

    @staticmethod
    def point_in_polygon(
        x: float, y: float, polygon: List[Tuple[float, float]]
    ) -> bool:
        """Check if a point is inside a polygon using ray casting.

        Args:
            x: X coordinate of point.
            y: Y coordinate of point.
            polygon: List of (x, y) polygon vertices.

        Returns:
            True if point is inside polygon.
        """
        n = len(polygon)
        if n < 3:
            return False

        inside = False
        j = n - 1

        for i in range(n):
            xi, yi = polygon[i]
            xj, yj = polygon[j]

            if ((yi > y) != (yj > y)) and (
                x < (xj - xi) * (y - yi) / (yj - yi) + xi
            ):
                inside = not inside

            j = i

        return inside

    @staticmethod
    def point_in_water_region(
        x: float, y: float, region: WaterRegion
    ) -> bool:
        """Check if a point is in a water region (exterior but not in holes).

        Args:
            x: X coordinate (normalized 0-1).
            y: Y coordinate (normalized 0-1).
            region: WaterRegion to check.

        Returns:
            True if point is in water region.
        """
        # Check if in exterior polygon
        if not PolygonUtils.point_in_polygon(x, y, region.polygon):
            return False

        # Check if in any hole
        for hole in region.holes:
            if PolygonUtils.point_in_polygon(x, y, hole):
                return False

        return True

    @staticmethod
    def get_polygon_bounds(
        polygon: List[Tuple[float, float]]
    ) -> Tuple[float, float, float, float]:
        """Get bounding box of a polygon.

        Args:
            polygon: List of (x, y) vertices.

        Returns:
            Tuple of (min_x, min_y, max_x, max_y).
        """
        if not polygon:
            return (0, 0, 1, 1)

        xs = [p[0] for p in polygon]
        ys = [p[1] for p in polygon]

        return (min(xs), min(ys), max(xs), max(ys))


class ClutterGenerator:
    """Generates random clutter points in water regions.

    Places high-intensity false positive points in designated water
    regions to simulate radar clutter.
    """

    def __init__(
        self,
        config: ClutterConfig,
        water_regions: Optional[List[WaterRegion]] = None,
    ) -> None:
        """Initialize the clutter generator.

        Args:
            config: ClutterConfig specifying generation parameters.
            water_regions: List of valid water regions for clutter placement.
        """
        self.config = config
        self.water_regions = water_regions or []
        self._rng = np.random.default_rng(config.seed)

    def load_regions_from_file(
        self, annotation_path: Union[str, Path]
    ) -> None:
        """Load water regions from annotation file.

        Args:
            annotation_path: Path to annotation.json file.
        """
        annotations = AnnotationLoader.load_annotations(annotation_path)
        self.water_regions = AnnotationLoader.extract_water_regions(annotations)

    def _sample_point_in_region(
        self, region: WaterRegion, max_attempts: int = 100
    ) -> Optional[Tuple[float, float]]:
        """Sample a random point within a water region.

        Uses rejection sampling within the bounding box.

        Args:
            region: WaterRegion to sample from.
            max_attempts: Maximum sampling attempts.

        Returns:
            (x, y) normalized coordinates or None if sampling fails.
        """
        bounds = PolygonUtils.get_polygon_bounds(region.polygon)
        min_x, min_y, max_x, max_y = bounds

        for _ in range(max_attempts):
            x = self._rng.uniform(min_x, max_x)
            y = self._rng.uniform(min_y, max_y)

            if PolygonUtils.point_in_water_region(x, y, region):
                return (x, y)

        return None

    def generate_clutter_frame(
        self,
        image_size: Tuple[int, int] = (1735, 1735),
    ) -> np.ndarray:
        """Generate clutter points for a single frame.

        Args:
            image_size: (width, height) of the image for coordinate scaling.

        Returns:
            Array of clutter points (N, 3) with (x, y, intensity).
        """
        if not self.water_regions:
            return np.array([]).reshape(0, 3)

        # Determine number of clutter points (Poisson distribution)
        n_points = self._rng.poisson(self.config.clutter_density)

        if n_points == 0:
            return np.array([]).reshape(0, 3)

        clutter_points = []
        width, height = image_size

        for _ in range(n_points):
            # Randomly select a water region
            region = self._rng.choice(self.water_regions)

            # Check if this is a cluster or single point
            if self._rng.random() < self.config.cluster_probability:
                # Generate a cluster
                cluster_size = self._rng.integers(
                    self.config.cluster_size_range[0],
                    self.config.cluster_size_range[1] + 1,
                )
                center = self._sample_point_in_region(region)

                if center is not None:
                    cx, cy = center
                    for _ in range(cluster_size):
                        # Add offset in normalized coordinates
                        offset_x = (
                            self._rng.normal(0, self.config.cluster_spread)
                            / width
                        )
                        offset_y = (
                            self._rng.normal(0, self.config.cluster_spread)
                            / height
                        )
                        px = cx + offset_x
                        py = cy + offset_y

                        # Only add if still in water region
                        if PolygonUtils.point_in_water_region(px, py, region):
                            intensity = self._rng.integers(
                                self.config.intensity_min,
                                self.config.intensity_max + 1,
                            )
                            # Convert to pixel coordinates
                            clutter_points.append(
                                [px * width, py * height, intensity]
                            )
            else:
                # Single point
                point = self._sample_point_in_region(region)
                if point is not None:
                    px, py = point
                    intensity = self._rng.integers(
                        self.config.intensity_min,
                        self.config.intensity_max + 1,
                    )
                    clutter_points.append([px * width, py * height, intensity])

        if not clutter_points:
            return np.array([]).reshape(0, 3)

        return np.array(clutter_points)

    def add_clutter_to_frame(
        self,
        frame_points: np.ndarray,
        image_size: Tuple[int, int] = (1735, 1735),
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Add clutter to existing frame points.

        Args:
            frame_points: Existing points (N, 3) with (x, y, intensity).
            image_size: Image dimensions for coordinate scaling.

        Returns:
            Tuple of (combined_points, clutter_mask) where clutter_mask
            indicates which points are clutter (True) vs original (False).
        """
        clutter = self.generate_clutter_frame(image_size)

        if len(clutter) == 0:
            mask = np.zeros(len(frame_points), dtype=bool)
            return frame_points.copy(), mask

        if len(frame_points) == 0:
            mask = np.ones(len(clutter), dtype=bool)
            return clutter, mask

        combined = np.vstack([frame_points, clutter])
        mask = np.concatenate([
            np.zeros(len(frame_points), dtype=bool),
            np.ones(len(clutter), dtype=bool),
        ])

        return combined, mask


def create_clutter_generator(
    clutter_density: float = 5.0,
    intensity_min: int = 180,
    intensity_max: int = 255,
    cluster_probability: float = 0.3,
    annotation_path: Optional[Union[str, Path]] = None,
    seed: Optional[int] = None,
) -> ClutterGenerator:
    """Factory function to create a ClutterGenerator.

    Args:
        clutter_density: Average clutter points per frame.
        intensity_min: Minimum clutter intensity.
        intensity_max: Maximum clutter intensity.
        cluster_probability: Probability of clustered clutter.
        annotation_path: Path to annotation.json with water regions.
        seed: Random seed for reproducibility.

    Returns:
        Configured ClutterGenerator instance.
    """
    config = ClutterConfig(
        clutter_density=clutter_density,
        intensity_min=intensity_min,
        intensity_max=intensity_max,
        cluster_probability=cluster_probability,
        seed=seed,
    )

    generator = ClutterGenerator(config)

    if annotation_path:
        generator.load_regions_from_file(annotation_path)

    return generator
