"""
Format conversion utilities for radar data.

This module handles conversion between CSV (FURUNO format), point cloud,
polar, and Cartesian coordinate systems.
"""

import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple, Union

import numpy as np


@dataclass
class RadarPulse:
    """Single radar pulse data.

    Attributes:
        angle_ticks: Azimuth angle in ticks (0-8191 for full rotation).
        echoes: List of intensity values for each range bin.
        status: Radar status code.
        scale: Range scale setting.
        range_setting: Range in meters.
        gain: Radar gain setting.
    """

    angle_ticks: int
    echoes: List[int]
    status: int = 0
    scale: int = 0
    range_setting: int = 0
    gain: int = 0


@dataclass
class PointCloud:
    """Point cloud representation of radar data.

    Attributes:
        x: X coordinates (Cartesian).
        y: Y coordinates (Cartesian).
        intensity: Intensity values.
        frame_id: Frame index for each point.
        range_bins: Original range bin indices (optional).
        azimuth_ticks: Original azimuth tick values (optional).
    """

    x: np.ndarray
    y: np.ndarray
    intensity: np.ndarray
    frame_id: np.ndarray
    range_bins: Optional[np.ndarray] = None
    azimuth_ticks: Optional[np.ndarray] = None


class CSVLoader:
    """Loads radar data from FURUNO CSV format."""

    @staticmethod
    def load_csv(csv_path: Union[str, Path]) -> List[RadarPulse]:
        """Load radar pulses from a CSV file.

        CSV format: Status, Scale, Range, Gain, Angle, EchoValues, echo1, echo2, ...

        Args:
            csv_path: Path to CSV file.

        Returns:
            List of RadarPulse objects.
        """
        pulses = []

        with open(csv_path, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) < 6:
                    continue

                try:
                    status = int(row[0]) if row[0].isdigit() else 0
                    scale = int(row[1]) if row[1].isdigit() else 0
                    range_setting = int(row[2]) if row[2].isdigit() else 0
                    gain = int(row[3]) if row[3].isdigit() else 0
                    angle_ticks = int(row[4])

                    # Echo values start at column 5 (skip "EchoValues" header)
                    echoes = []
                    for val in row[5:]:
                        try:
                            echoes.append(int(val))
                        except ValueError:
                            continue

                    pulse = RadarPulse(
                        angle_ticks=angle_ticks,
                        echoes=echoes,
                        status=status,
                        scale=scale,
                        range_setting=range_setting,
                        gain=gain,
                    )
                    pulses.append(pulse)

                except (ValueError, IndexError):
                    continue

        return pulses

    @staticmethod
    def load_csv_directory(
        directory: Union[str, Path],
        pattern: str = "*.csv",
        max_frames: Optional[int] = None,
    ) -> Iterator[Tuple[int, List[RadarPulse]]]:
        """Load multiple CSV files from a directory.

        Args:
            directory: Directory containing CSV files.
            pattern: Glob pattern for CSV files.
            max_frames: Maximum number of frames to load.

        Yields:
            Tuple of (frame_index, pulses) for each file.
        """
        dir_path = Path(directory)
        files = sorted(dir_path.glob(pattern))

        if max_frames is not None:
            files = files[:max_frames]

        for idx, file_path in enumerate(files):
            pulses = CSVLoader.load_csv(file_path)
            yield idx, pulses


class CoordinateConverter:
    """Converts between polar and Cartesian coordinate systems."""

    def __init__(
        self,
        image_size: int = 1736,
        ticks_per_rotation: int = 8192,
    ) -> None:
        """Initialize the coordinate converter.

        Args:
            image_size: Size of the output image (assumes square).
            ticks_per_rotation: Number of azimuth ticks per full rotation.
        """
        self.image_size = image_size
        self.center = image_size // 2
        self.max_radius = self.center
        self.ticks_per_rotation = ticks_per_rotation

    def polar_to_cartesian(
        self,
        range_bin: float,
        azimuth_tick: float,
        num_bins: int,
    ) -> Tuple[float, float]:
        """Convert polar coordinates to Cartesian.

        Args:
            range_bin: Range bin index.
            azimuth_tick: Azimuth in ticks.
            num_bins: Total number of range bins.

        Returns:
            Tuple of (x, y) Cartesian coordinates.
        """
        # Normalize range to [0, 1]
        r_norm = range_bin / num_bins
        r = r_norm * self.max_radius

        # Convert ticks to radians
        angle_rad = (azimuth_tick / self.ticks_per_rotation) * 2 * np.pi

        # Convert to Cartesian (radar convention: 0 is North, clockwise)
        x = self.center + r * np.sin(angle_rad)
        y = self.center - r * np.cos(angle_rad)

        return x, y

    def cartesian_to_polar(
        self,
        x: float,
        y: float,
        num_bins: int,
    ) -> Tuple[float, float]:
        """Convert Cartesian coordinates to polar.

        Args:
            x: X coordinate.
            y: Y coordinate.
            num_bins: Total number of range bins.

        Returns:
            Tuple of (range_bin, azimuth_tick).
        """
        dx = x - self.center
        dy = self.center - y  # Flip Y for radar convention

        r = np.sqrt(dx**2 + dy**2)
        r_norm = r / self.max_radius
        range_bin = r_norm * num_bins

        # Compute angle (radar convention)
        angle_rad = np.arctan2(dx, dy)
        if angle_rad < 0:
            angle_rad += 2 * np.pi

        azimuth_tick = (angle_rad / (2 * np.pi)) * self.ticks_per_rotation

        return range_bin, azimuth_tick

    def pulses_to_point_cloud(
        self,
        pulses: List[RadarPulse],
        intensity_threshold: int = 0,
        frame_id: int = 0,
    ) -> PointCloud:
        """Convert radar pulses to point cloud.

        Args:
            pulses: List of RadarPulse objects.
            intensity_threshold: Minimum intensity to include.
            frame_id: Frame index for all points.

        Returns:
            PointCloud with Cartesian coordinates.
        """
        points_x = []
        points_y = []
        intensities = []
        range_bins = []
        azimuth_ticks = []

        for pulse in pulses:
            num_bins = len(pulse.echoes)
            if num_bins == 0:
                continue

            for bin_idx, intensity in enumerate(pulse.echoes):
                if intensity <= intensity_threshold:
                    continue

                x, y = self.polar_to_cartesian(
                    bin_idx, pulse.angle_ticks, num_bins
                )

                points_x.append(x)
                points_y.append(y)
                intensities.append(intensity)
                range_bins.append(bin_idx)
                azimuth_ticks.append(pulse.angle_ticks)

        return PointCloud(
            x=np.array(points_x),
            y=np.array(points_y),
            intensity=np.array(intensities),
            frame_id=np.full(len(points_x), frame_id),
            range_bins=np.array(range_bins),
            azimuth_ticks=np.array(azimuth_ticks),
        )


class PointCloudExporter:
    """Exports point cloud data to various formats."""

    @staticmethod
    def to_numpy(point_cloud: PointCloud) -> np.ndarray:
        """Export point cloud to NumPy array.

        Args:
            point_cloud: PointCloud to export.

        Returns:
            Array of shape (N, 4) with (x, y, intensity, frame_id).
        """
        return np.column_stack([
            point_cloud.x,
            point_cloud.y,
            point_cloud.intensity,
            point_cloud.frame_id,
        ])

    @staticmethod
    def save_npy(
        point_cloud: PointCloud,
        output_path: Union[str, Path],
        include_polar: bool = False,
    ) -> None:
        """Save point cloud to .npy file.

        Args:
            point_cloud: PointCloud to save.
            output_path: Output file path.
            include_polar: Include polar coordinates in output.
        """
        if include_polar and point_cloud.range_bins is not None:
            data = np.column_stack([
                point_cloud.x,
                point_cloud.y,
                point_cloud.intensity,
                point_cloud.frame_id,
                point_cloud.range_bins,
                point_cloud.azimuth_ticks,
            ])
        else:
            data = PointCloudExporter.to_numpy(point_cloud)

        np.save(output_path, data)

    @staticmethod
    def to_json(point_cloud: PointCloud) -> Dict:
        """Export point cloud to JSON-serializable dictionary.

        Args:
            point_cloud: PointCloud to export.

        Returns:
            Dictionary representation of point cloud.
        """
        result = {
            "num_points": len(point_cloud.x),
            "points": [
                {
                    "x": float(point_cloud.x[i]),
                    "y": float(point_cloud.y[i]),
                    "intensity": int(point_cloud.intensity[i]),
                    "frame_id": int(point_cloud.frame_id[i]),
                }
                for i in range(len(point_cloud.x))
            ],
        }

        if point_cloud.range_bins is not None:
            for i, pt in enumerate(result["points"]):
                pt["range_bin"] = float(point_cloud.range_bins[i])
                pt["azimuth_tick"] = float(point_cloud.azimuth_ticks[i])

        return result

    @staticmethod
    def save_json(
        point_cloud: PointCloud,
        output_path: Union[str, Path],
    ) -> None:
        """Save point cloud to JSON file.

        Args:
            point_cloud: PointCloud to save.
            output_path: Output file path.
        """
        data = PointCloudExporter.to_json(point_cloud)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)


class FormatConverter:
    """High-level format conversion interface."""

    def __init__(
        self,
        image_size: int = 1736,
        intensity_threshold: int = 0,
    ) -> None:
        """Initialize the format converter.

        Args:
            image_size: Size for coordinate conversion.
            intensity_threshold: Minimum intensity to include.
        """
        self.coord_converter = CoordinateConverter(image_size)
        self.intensity_threshold = intensity_threshold

    def csv_to_point_cloud(
        self,
        csv_path: Union[str, Path],
        frame_id: int = 0,
    ) -> PointCloud:
        """Convert a single CSV file to point cloud.

        Args:
            csv_path: Path to CSV file.
            frame_id: Frame index.

        Returns:
            PointCloud representation.
        """
        pulses = CSVLoader.load_csv(csv_path)
        return self.coord_converter.pulses_to_point_cloud(
            pulses, self.intensity_threshold, frame_id
        )

    def csv_directory_to_point_cloud(
        self,
        directory: Union[str, Path],
        pattern: str = "*.csv",
        max_frames: Optional[int] = None,
    ) -> PointCloud:
        """Convert directory of CSV files to combined point cloud.

        Args:
            directory: Directory containing CSV files.
            pattern: Glob pattern for CSV files.
            max_frames: Maximum frames to process.

        Returns:
            Combined PointCloud for all frames.
        """
        all_x = []
        all_y = []
        all_intensity = []
        all_frame_id = []
        all_range = []
        all_azimuth = []

        for frame_id, pulses in CSVLoader.load_csv_directory(
            directory, pattern, max_frames
        ):
            pc = self.coord_converter.pulses_to_point_cloud(
                pulses, self.intensity_threshold, frame_id
            )

            all_x.extend(pc.x)
            all_y.extend(pc.y)
            all_intensity.extend(pc.intensity)
            all_frame_id.extend(pc.frame_id)

            if pc.range_bins is not None:
                all_range.extend(pc.range_bins)
                all_azimuth.extend(pc.azimuth_ticks)

        return PointCloud(
            x=np.array(all_x),
            y=np.array(all_y),
            intensity=np.array(all_intensity),
            frame_id=np.array(all_frame_id),
            range_bins=np.array(all_range) if all_range else None,
            azimuth_ticks=np.array(all_azimuth) if all_azimuth else None,
        )

    def convert_and_save(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        output_format: str = "npy",
        include_polar: bool = False,
    ) -> None:
        """Convert CSV input and save to specified format.

        Args:
            input_path: Input CSV file or directory.
            output_path: Output file path.
            output_format: Output format ("npy" or "json").
            include_polar: Include polar coordinates in output.
        """
        input_path = Path(input_path)

        if input_path.is_dir():
            point_cloud = self.csv_directory_to_point_cloud(input_path)
        else:
            point_cloud = self.csv_to_point_cloud(input_path)

        if output_format == "npy":
            PointCloudExporter.save_npy(point_cloud, output_path, include_polar)
        elif output_format == "json":
            PointCloudExporter.save_json(point_cloud, output_path)
        else:
            raise ValueError(f"Unknown output format: {output_format}")


def create_converter(
    image_size: int = 1736,
    intensity_threshold: int = 0,
) -> FormatConverter:
    """Factory function to create a FormatConverter.

    Args:
        image_size: Size for coordinate conversion.
        intensity_threshold: Minimum intensity to include.

    Returns:
        Configured FormatConverter instance.
    """
    return FormatConverter(image_size, intensity_threshold)
