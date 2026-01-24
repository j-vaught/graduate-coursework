"""
Gaussian position noise injection for synthetic radar data.

This module adds Gaussian noise to object positions in polar coordinates
while preserving intensity values.
"""

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np


@dataclass
class NoiseConfig:
    """Configuration for Gaussian noise injection.

    Attributes:
        sigma_range: Standard deviation for range noise (in range bins).
        sigma_azimuth: Standard deviation for azimuth noise (in azimuth ticks).
        seed: Random seed for reproducibility. None for random.
    """

    sigma_range: float = 1.0
    sigma_azimuth: float = 2.0
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if self.sigma_range < 0:
            raise ValueError("sigma_range must be non-negative")
        if self.sigma_azimuth < 0:
            raise ValueError("sigma_azimuth must be non-negative")


class NoiseInjector:
    """Injects Gaussian noise into radar point positions.

    Adds noise in polar coordinates (range, azimuth) while preserving
    the original intensity values.
    """

    def __init__(self, config: NoiseConfig) -> None:
        """Initialize the noise injector.

        Args:
            config: NoiseConfig specifying noise parameters.
        """
        self.config = config
        self._rng = np.random.default_rng(config.seed)

    def add_noise_polar(
        self,
        range_bins: np.ndarray,
        azimuth_ticks: np.ndarray,
        intensities: np.ndarray,
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Add Gaussian noise to polar coordinates.

        Args:
            range_bins: Array of range bin indices.
            azimuth_ticks: Array of azimuth tick values (0-8191 for full rotation).
            intensities: Array of intensity values (preserved unchanged).

        Returns:
            Tuple of (noisy_range_bins, noisy_azimuth_ticks, intensities).
            Range bins are clipped to non-negative values.
            Azimuth ticks are wrapped to [0, 8192) range.
        """
        n_points = len(range_bins)

        # Generate Gaussian noise
        range_noise = self._rng.normal(0, self.config.sigma_range, n_points)
        azimuth_noise = self._rng.normal(0, self.config.sigma_azimuth, n_points)

        # Apply noise
        noisy_range = range_bins.astype(np.float64) + range_noise
        noisy_azimuth = azimuth_ticks.astype(np.float64) + azimuth_noise

        # Clip range to non-negative (can't have negative range)
        noisy_range = np.maximum(noisy_range, 0)

        # Wrap azimuth to [0, 8192) range (full rotation = 8192 ticks)
        noisy_azimuth = np.mod(noisy_azimuth, 8192)

        return noisy_range, noisy_azimuth, intensities

    def add_noise_cartesian(
        self,
        x: np.ndarray,
        y: np.ndarray,
        intensities: np.ndarray,
        image_center: Tuple[float, float] = (867.5, 867.5),
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Add Gaussian noise to Cartesian coordinates via polar conversion.

        Converts to polar, adds noise, then converts back to Cartesian.

        Args:
            x: Array of x coordinates.
            y: Array of y coordinates.
            intensities: Array of intensity values (preserved unchanged).
            image_center: Center point (x, y) for polar conversion.

        Returns:
            Tuple of (noisy_x, noisy_y, intensities).
        """
        cx, cy = image_center

        # Convert to polar coordinates
        dx = x - cx
        dy = y - cy
        r = np.sqrt(dx**2 + dy**2)
        theta = np.arctan2(dy, dx)

        # Convert angle to azimuth ticks (full rotation = 8192 ticks)
        azimuth_ticks = (theta / (2 * np.pi)) * 8192
        azimuth_ticks = np.mod(azimuth_ticks, 8192)

        # Add noise in polar coordinates
        noisy_r, noisy_azimuth, _ = self.add_noise_polar(
            r, azimuth_ticks, intensities
        )

        # Convert back to Cartesian
        noisy_theta = (noisy_azimuth / 8192) * 2 * np.pi
        noisy_x = cx + noisy_r * np.cos(noisy_theta)
        noisy_y = cy + noisy_r * np.sin(noisy_theta)

        return noisy_x, noisy_y, intensities

    def add_noise_to_frame(
        self,
        frame_data: np.ndarray,
        coordinate_type: str = "polar",
        image_center: Optional[Tuple[float, float]] = None,
    ) -> np.ndarray:
        """Add noise to a complete frame of radar data.

        Args:
            frame_data: Array with columns depending on coordinate_type:
                - "polar": (range_bin, azimuth_tick, intensity)
                - "cartesian": (x, y, intensity)
            coordinate_type: Either "polar" or "cartesian".
            image_center: Required for cartesian coordinates.

        Returns:
            Noisy frame data with same shape as input.
        """
        if len(frame_data) == 0:
            return frame_data.copy()

        result = frame_data.copy()

        if coordinate_type == "polar":
            range_bins = frame_data[:, 0]
            azimuth_ticks = frame_data[:, 1]
            intensities = frame_data[:, 2]

            noisy_range, noisy_azimuth, _ = self.add_noise_polar(
                range_bins, azimuth_ticks, intensities
            )

            result[:, 0] = noisy_range
            result[:, 1] = noisy_azimuth

        elif coordinate_type == "cartesian":
            if image_center is None:
                image_center = (867.5, 867.5)

            x = frame_data[:, 0]
            y = frame_data[:, 1]
            intensities = frame_data[:, 2]

            noisy_x, noisy_y, _ = self.add_noise_cartesian(
                x, y, intensities, image_center
            )

            result[:, 0] = noisy_x
            result[:, 1] = noisy_y

        else:
            raise ValueError(f"Unknown coordinate_type: {coordinate_type}")

        return result


def create_noise_injector(
    sigma_range: float = 1.0,
    sigma_azimuth: float = 2.0,
    seed: Optional[int] = None,
) -> NoiseInjector:
    """Factory function to create a NoiseInjector.

    Args:
        sigma_range: Standard deviation for range noise (in range bins).
        sigma_azimuth: Standard deviation for azimuth noise (in azimuth ticks).
        seed: Random seed for reproducibility.

    Returns:
        Configured NoiseInjector instance.
    """
    config = NoiseConfig(
        sigma_range=sigma_range,
        sigma_azimuth=sigma_azimuth,
        seed=seed,
    )
    return NoiseInjector(config)
