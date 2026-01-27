"""
Radar Post-Processing Module

A comprehensive Python module for post-processing synthetic radar data,
including noise injection, detection dropout, clutter generation,
format conversion, and evaluation metrics.

Modules:
    noise: Gaussian position noise injection
    dropout: Random detection dropouts with ground truth tracking
    clutter: Random clutter generation in water regions
    convert: Format conversion (CSV, point cloud, NumPy, JSON)
    processor: Main processing pipeline
    metrics: Evaluation metrics (Purity, Continuity, MOTA, MOTP)
    cli: Command-line interface

Example usage:
    from radar_postprocessing import create_processor, create_converter
    from radar_postprocessing.metrics import compute_purity, compute_continuity

    # Process radar data
    processor = create_processor(config_path="config.toml")
    processor.process_csv_directory("./input", "./output")

    # Convert data formats
    converter = create_converter()
    converter.convert_and_save("./raw.csv", "./points.npy")
"""

from .clutter import (
    ClutterConfig,
    ClutterGenerator,
    WaterRegion,
    create_clutter_generator,
)
from .convert import (
    CoordinateConverter,
    CSVLoader,
    FormatConverter,
    PointCloud,
    PointCloudExporter,
    RadarPulse,
    create_converter,
)
from .dropout import (
    DropoutConfig,
    DropoutRecord,
    DropoutResult,
    GroundTruthModifier,
    ObjectDropout,
    create_dropout_handler,
)
from .metrics import (
    ClusteringMetrics,
    ContinuityCalculator,
    MetricsEvaluator,
    MOTACalculator,
    MOTPCalculator,
    PurityCalculator,
    TrackingMetrics,
    compute_continuity,
    compute_purity,
)
from .noise import NoiseConfig, NoiseInjector, create_noise_injector
from .processor import (
    ProcessingResult,
    RadarPostProcessor,
    ScenarioConfig,
    create_processor,
)

__version__ = "0.1.0"
__author__ = "University of South Carolina Radar Research"

__all__ = [
    # Noise module
    "NoiseConfig",
    "NoiseInjector",
    "create_noise_injector",
    # Dropout module
    "DropoutConfig",
    "DropoutRecord",
    "DropoutResult",
    "ObjectDropout",
    "GroundTruthModifier",
    "create_dropout_handler",
    # Clutter module
    "ClutterConfig",
    "ClutterGenerator",
    "WaterRegion",
    "create_clutter_generator",
    # Convert module
    "RadarPulse",
    "PointCloud",
    "CSVLoader",
    "CoordinateConverter",
    "PointCloudExporter",
    "FormatConverter",
    "create_converter",
    # Processor module
    "ScenarioConfig",
    "ProcessingResult",
    "RadarPostProcessor",
    "create_processor",
    # Metrics module
    "ClusteringMetrics",
    "TrackingMetrics",
    "PurityCalculator",
    "ContinuityCalculator",
    "MOTACalculator",
    "MOTPCalculator",
    "MetricsEvaluator",
    "compute_purity",
    "compute_continuity",
]
