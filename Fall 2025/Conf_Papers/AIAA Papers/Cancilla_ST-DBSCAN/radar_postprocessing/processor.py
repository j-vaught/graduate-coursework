"""
Main processing pipeline for synthetic radar data.

This module orchestrates the application of noise, dropout, and clutter
effects to radar data, managing configuration and ground truth updates.
"""

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from .clutter import ClutterConfig, ClutterGenerator, create_clutter_generator
from .convert import (
    CoordinateConverter,
    CSVLoader,
    FormatConverter,
    PointCloud,
    PointCloudExporter,
)
from .dropout import (
    DropoutConfig,
    DropoutRecord,
    GroundTruthModifier,
    ObjectDropout,
    create_dropout_handler,
)
from .noise import NoiseConfig, NoiseInjector, create_noise_injector


@dataclass
class ScenarioConfig:
    """Configuration for a complete processing scenario.

    Attributes:
        name: Scenario name.
        description: Scenario description.
        noise: Noise configuration parameters.
        dropout: Dropout configuration parameters.
        clutter: Clutter configuration parameters.
        conversion: Format conversion parameters.
        seed: Global random seed.
    """

    name: str = "default"
    description: str = ""
    noise: Optional[Dict[str, Any]] = None
    dropout: Optional[Dict[str, Any]] = None
    clutter: Optional[Dict[str, Any]] = None
    conversion: Optional[Dict[str, Any]] = None
    seed: Optional[int] = None

    @classmethod
    def from_toml(cls, toml_path: Union[str, Path]) -> "ScenarioConfig":
        """Load configuration from TOML file.

        Args:
            toml_path: Path to TOML configuration file.

        Returns:
            ScenarioConfig instance.
        """
        path = Path(toml_path)
        with open(path, "rb") as f:
            data = tomllib.load(f)

        return cls(
            name=data.get("name", "default"),
            description=data.get("description", ""),
            noise=data.get("noise"),
            dropout=data.get("dropout"),
            clutter=data.get("clutter"),
            conversion=data.get("conversion"),
            seed=data.get("seed"),
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScenarioConfig":
        """Load configuration from dictionary.

        Args:
            data: Configuration dictionary.

        Returns:
            ScenarioConfig instance.
        """
        return cls(
            name=data.get("name", "default"),
            description=data.get("description", ""),
            noise=data.get("noise"),
            dropout=data.get("dropout"),
            clutter=data.get("clutter"),
            conversion=data.get("conversion"),
            seed=data.get("seed"),
        )


@dataclass
class ProcessingResult:
    """Result of processing a single frame or sequence.

    Attributes:
        point_cloud: Processed point cloud data.
        ground_truth: Modified ground truth.
        dropout_records: Records of dropped objects.
        clutter_mask: Mask indicating clutter points.
        metadata: Additional processing metadata.
    """

    point_cloud: PointCloud
    ground_truth: Optional[Dict] = None
    dropout_records: List[DropoutRecord] = field(default_factory=list)
    clutter_mask: Optional[np.ndarray] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class RadarPostProcessor:
    """Main processing pipeline for radar data.

    Applies noise, dropout, and clutter effects in sequence,
    managing ground truth updates throughout.
    """

    def __init__(
        self,
        config: ScenarioConfig,
        annotation_path: Optional[Union[str, Path]] = None,
    ) -> None:
        """Initialize the post-processor.

        Args:
            config: ScenarioConfig specifying processing parameters.
            annotation_path: Path to annotation.json for clutter regions.
        """
        self.config = config
        self.annotation_path = annotation_path

        # Initialize processing components
        self._init_components()

    def _init_components(self) -> None:
        """Initialize processing components based on configuration."""
        # Use global seed if specific seeds not provided
        base_seed = self.config.seed

        # Noise injector
        if self.config.noise:
            noise_seed = self.config.noise.get("seed", base_seed)
            self.noise_injector = create_noise_injector(
                sigma_range=self.config.noise.get("sigma_range", 1.0),
                sigma_azimuth=self.config.noise.get("sigma_azimuth", 2.0),
                seed=noise_seed,
            )
        else:
            self.noise_injector = None

        # Dropout handler
        if self.config.dropout:
            dropout_seed = self.config.dropout.get("seed", base_seed)
            if dropout_seed == base_seed and base_seed is not None:
                dropout_seed = base_seed + 1  # Ensure different seeds
            self.dropout_handler = create_dropout_handler(
                dropout_rate=self.config.dropout.get("dropout_rate", 0.1),
                min_consecutive_frames=self.config.dropout.get(
                    "min_consecutive_frames", 1
                ),
                seed=dropout_seed,
            )
        else:
            self.dropout_handler = None

        # Clutter generator
        if self.config.clutter:
            clutter_seed = self.config.clutter.get("seed", base_seed)
            if clutter_seed == base_seed and base_seed is not None:
                clutter_seed = base_seed + 2
            self.clutter_generator = create_clutter_generator(
                clutter_density=self.config.clutter.get("clutter_density", 5.0),
                intensity_min=self.config.clutter.get("intensity_min", 180),
                intensity_max=self.config.clutter.get("intensity_max", 255),
                cluster_probability=self.config.clutter.get(
                    "cluster_probability", 0.3
                ),
                annotation_path=self.annotation_path,
                seed=clutter_seed,
            )
        else:
            self.clutter_generator = None

        # Format converter
        conv_config = self.config.conversion or {}
        self.converter = FormatConverter(
            image_size=conv_config.get("image_size", 1736),
            intensity_threshold=conv_config.get("intensity_threshold", 0),
        )

    def process_frame(
        self,
        points: np.ndarray,
        object_ids: Optional[np.ndarray] = None,
        frame_id: int = 0,
        coordinate_type: str = "cartesian",
    ) -> ProcessingResult:
        """Process a single frame of radar data.

        Applies noise, dropout, and clutter in sequence.

        Args:
            points: Point data (N, 3) with (x/range, y/azimuth, intensity).
            object_ids: Object IDs for each point (required for dropout).
            frame_id: Frame index.
            coordinate_type: "cartesian" or "polar".

        Returns:
            ProcessingResult with processed data.
        """
        if len(points) == 0:
            return ProcessingResult(
                point_cloud=PointCloud(
                    x=np.array([]),
                    y=np.array([]),
                    intensity=np.array([]),
                    frame_id=np.array([]),
                ),
                metadata={"frame_id": frame_id, "num_points_in": 0},
            )

        processed_points = points.copy()
        dropout_records = []
        remaining_object_ids = object_ids

        # Step 1: Apply noise
        if self.noise_injector is not None:
            processed_points = self.noise_injector.add_noise_to_frame(
                processed_points, coordinate_type
            )

        # Step 2: Apply dropout (if object IDs provided)
        if self.dropout_handler is not None and object_ids is not None:
            result = self.dropout_handler.apply_dropout(
                processed_points, object_ids, frame_id
            )
            processed_points = result.points
            remaining_object_ids = result.object_ids
            dropout_records = result.dropout_records

        # Step 3: Add clutter
        clutter_mask = None
        if self.clutter_generator is not None:
            conv_config = self.config.conversion or {}
            image_size = conv_config.get("image_size", 1736)

            if coordinate_type == "polar":
                # Convert clutter to polar coordinates
                clutter = self.clutter_generator.generate_clutter_frame(
                    (image_size, image_size)
                )
                if len(clutter) > 0:
                    # Convert clutter from Cartesian to polar
                    cx, cy = image_size / 2, image_size / 2
                    clutter_polar = np.zeros_like(clutter)
                    for i, pt in enumerate(clutter):
                        dx = pt[0] - cx
                        dy = pt[1] - cy
                        r = np.sqrt(dx**2 + dy**2)
                        theta = np.arctan2(dy, dx)
                        azimuth = (theta / (2 * np.pi)) * 8192
                        clutter_polar[i] = [r, azimuth % 8192, pt[2]]

                    n_original = len(processed_points)
                    processed_points = np.vstack([processed_points, clutter_polar])
                    clutter_mask = np.concatenate([
                        np.zeros(n_original, dtype=bool),
                        np.ones(len(clutter), dtype=bool),
                    ])
            else:
                processed_points, clutter_mask = (
                    self.clutter_generator.add_clutter_to_frame(
                        processed_points, (image_size, image_size)
                    )
                )

        # Build point cloud result
        if coordinate_type == "polar":
            coord_conv = CoordinateConverter(
                image_size=self.config.conversion.get("image_size", 1736)
                if self.config.conversion
                else 1736
            )
            x = []
            y = []
            for pt in processed_points:
                px, py = coord_conv.polar_to_cartesian(
                    pt[0], pt[1], 868  # Approximate num_bins
                )
                x.append(px)
                y.append(py)
            x = np.array(x)
            y = np.array(y)
            range_bins = processed_points[:, 0]
            azimuth_ticks = processed_points[:, 1]
        else:
            x = processed_points[:, 0]
            y = processed_points[:, 1]
            range_bins = None
            azimuth_ticks = None

        point_cloud = PointCloud(
            x=x,
            y=y,
            intensity=processed_points[:, 2],
            frame_id=np.full(len(processed_points), frame_id),
            range_bins=range_bins,
            azimuth_ticks=azimuth_ticks,
        )

        return ProcessingResult(
            point_cloud=point_cloud,
            dropout_records=dropout_records,
            clutter_mask=clutter_mask,
            metadata={
                "frame_id": frame_id,
                "num_points_in": len(points),
                "num_points_out": len(processed_points),
                "num_dropped": len(points) - len(processed_points)
                + (len(clutter_mask) - np.sum(~clutter_mask) if clutter_mask is not None else 0),
            },
        )

    def process_csv_directory(
        self,
        input_dir: Union[str, Path],
        output_dir: Union[str, Path],
        ground_truth_path: Optional[Union[str, Path]] = None,
        max_frames: Optional[int] = None,
        output_format: str = "npy",
    ) -> Dict[str, Any]:
        """Process a directory of CSV files.

        Args:
            input_dir: Input directory containing CSV files.
            output_dir: Output directory for processed data.
            ground_truth_path: Path to ground truth JSON (optional).
            max_frames: Maximum frames to process.
            output_format: Output format ("npy" or "json").

        Returns:
            Dictionary with processing summary.
        """
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Load ground truth if provided
        original_ground_truth = None
        if ground_truth_path:
            gt_path = Path(ground_truth_path)
            if gt_path.exists():
                with open(gt_path, "r") as f:
                    original_ground_truth = json.load(f)

        # Reset dropout handler for new sequence
        if self.dropout_handler:
            self.dropout_handler.reset()

        all_points = []
        all_dropout_records = []
        all_clutter_masks = []
        frame_metadata = []

        # Process each frame
        for frame_id, pulses in CSVLoader.load_csv_directory(
            input_path, max_frames=max_frames
        ):
            # Convert to point cloud
            pc = self.converter.coord_converter.pulses_to_point_cloud(
                pulses, self.converter.intensity_threshold, frame_id
            )

            if len(pc.x) == 0:
                continue

            # Create points array
            points = np.column_stack([pc.x, pc.y, pc.intensity])

            # For now, treat each point as its own object for dropout
            # In practice, you'd have object labels from detection
            object_ids = np.arange(len(points))

            # Process frame
            result = self.process_frame(
                points, object_ids, frame_id, "cartesian"
            )

            all_points.append(result.point_cloud)
            all_dropout_records.extend(result.dropout_records)
            if result.clutter_mask is not None:
                all_clutter_masks.append(
                    (frame_id, result.clutter_mask)
                )
            frame_metadata.append(result.metadata)

        # Combine all point clouds
        if all_points:
            combined_pc = PointCloud(
                x=np.concatenate([pc.x for pc in all_points]),
                y=np.concatenate([pc.y for pc in all_points]),
                intensity=np.concatenate([pc.intensity for pc in all_points]),
                frame_id=np.concatenate([pc.frame_id for pc in all_points]),
                range_bins=(
                    np.concatenate([pc.range_bins for pc in all_points])
                    if all_points[0].range_bins is not None
                    else None
                ),
                azimuth_ticks=(
                    np.concatenate([pc.azimuth_ticks for pc in all_points])
                    if all_points[0].azimuth_ticks is not None
                    else None
                ),
            )
        else:
            combined_pc = PointCloud(
                x=np.array([]),
                y=np.array([]),
                intensity=np.array([]),
                frame_id=np.array([]),
            )

        # Save processed point cloud
        if output_format == "npy":
            PointCloudExporter.save_npy(
                combined_pc,
                output_path / "processed_points.npy",
                include_polar=True,
            )
        else:
            PointCloudExporter.save_json(
                combined_pc,
                output_path / "processed_points.json",
            )

        # Update and save ground truth
        modified_gt = None
        if original_ground_truth:
            modified_gt = GroundTruthModifier.update_ground_truth(
                original_ground_truth, all_dropout_records
            )
            with open(output_path / "ground_truth_modified.json", "w") as f:
                json.dump(modified_gt, f, indent=2)

        # Save processing metadata
        summary = {
            "config": {
                "name": self.config.name,
                "description": self.config.description,
                "noise": self.config.noise,
                "dropout": self.config.dropout,
                "clutter": self.config.clutter,
            },
            "num_frames": len(frame_metadata),
            "total_points": len(combined_pc.x),
            "dropout_summary": (
                self.dropout_handler.get_dropout_summary()
                if self.dropout_handler
                else None
            ),
            "frame_metadata": frame_metadata,
        }

        with open(output_path / "processing_summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        return summary


def create_processor(
    config_path: Optional[Union[str, Path]] = None,
    config_dict: Optional[Dict[str, Any]] = None,
    annotation_path: Optional[Union[str, Path]] = None,
) -> RadarPostProcessor:
    """Factory function to create a RadarPostProcessor.

    Args:
        config_path: Path to TOML configuration file.
        config_dict: Configuration dictionary (alternative to file).
        annotation_path: Path to annotation.json for clutter regions.

    Returns:
        Configured RadarPostProcessor instance.
    """
    if config_path:
        config = ScenarioConfig.from_toml(config_path)
    elif config_dict:
        config = ScenarioConfig.from_dict(config_dict)
    else:
        config = ScenarioConfig()

    return RadarPostProcessor(config, annotation_path)
