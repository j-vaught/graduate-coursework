"""
Random detection dropout for synthetic radar data.

This module randomly removes entire objects from frames to simulate
missed detections in radar tracking scenarios.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

import numpy as np


@dataclass
class DropoutConfig:
    """Configuration for detection dropout.

    Attributes:
        dropout_rate: Probability of dropping an object per frame (0-1).
        min_consecutive_frames: Minimum frames an object must appear before
            being eligible for dropout.
        seed: Random seed for reproducibility.
    """

    dropout_rate: float = 0.1
    min_consecutive_frames: int = 1
    seed: Optional[int] = None

    def __post_init__(self) -> None:
        """Validate configuration parameters."""
        if not 0 <= self.dropout_rate <= 1:
            raise ValueError("dropout_rate must be between 0 and 1")
        if self.min_consecutive_frames < 1:
            raise ValueError("min_consecutive_frames must be at least 1")


@dataclass
class DropoutRecord:
    """Record of dropout events for ground truth tracking.

    Attributes:
        frame_id: Frame index where dropout occurred.
        object_id: ID of the dropped object.
        original_points: Points that were removed.
    """

    frame_id: int
    object_id: int
    original_points: np.ndarray


@dataclass
class DropoutResult:
    """Result of applying dropout to frame data.

    Attributes:
        points: Remaining points after dropout.
        object_ids: Object IDs for remaining points.
        dropped_objects: Set of object IDs that were dropped.
        dropout_records: Detailed records of each dropout event.
    """

    points: np.ndarray
    object_ids: np.ndarray
    dropped_objects: Set[int]
    dropout_records: List[DropoutRecord] = field(default_factory=list)


class ObjectDropout:
    """Applies random detection dropout to radar objects.

    Randomly removes entire objects from frames to simulate missed detections.
    Tracks which objects were dropped for ground truth modification.
    """

    def __init__(self, config: DropoutConfig) -> None:
        """Initialize the dropout handler.

        Args:
            config: DropoutConfig specifying dropout parameters.
        """
        self.config = config
        self._rng = np.random.default_rng(config.seed)
        self._object_frame_counts: Dict[int, int] = {}
        self._all_dropout_records: List[DropoutRecord] = []

    def reset(self) -> None:
        """Reset internal state for a new sequence."""
        self._object_frame_counts.clear()
        self._all_dropout_records.clear()

    def apply_dropout(
        self,
        points: np.ndarray,
        object_ids: np.ndarray,
        frame_id: int,
    ) -> DropoutResult:
        """Apply random dropout to a single frame.

        Args:
            points: Array of point coordinates (N, 3) with (x, y, intensity)
                or (range, azimuth, intensity).
            object_ids: Array of object IDs for each point (N,).
            frame_id: Current frame index.

        Returns:
            DropoutResult containing remaining points and dropout information.
        """
        if len(points) == 0:
            return DropoutResult(
                points=points,
                object_ids=object_ids,
                dropped_objects=set(),
                dropout_records=[],
            )

        # Get unique objects in this frame
        unique_objects = np.unique(object_ids)

        # Update object frame counts
        for obj_id in unique_objects:
            self._object_frame_counts[obj_id] = (
                self._object_frame_counts.get(obj_id, 0) + 1
            )

        # Determine which objects are eligible for dropout
        eligible_objects = [
            obj_id
            for obj_id in unique_objects
            if self._object_frame_counts[obj_id] >= self.config.min_consecutive_frames
        ]

        # Randomly select objects to drop
        dropped_objects: Set[int] = set()
        dropout_records: List[DropoutRecord] = []

        for obj_id in eligible_objects:
            if self._rng.random() < self.config.dropout_rate:
                dropped_objects.add(obj_id)

                # Record the dropout
                obj_mask = object_ids == obj_id
                record = DropoutRecord(
                    frame_id=frame_id,
                    object_id=obj_id,
                    original_points=points[obj_mask].copy(),
                )
                dropout_records.append(record)
                self._all_dropout_records.append(record)

        # Filter out dropped objects
        if dropped_objects:
            keep_mask = ~np.isin(object_ids, list(dropped_objects))
            filtered_points = points[keep_mask]
            filtered_object_ids = object_ids[keep_mask]
        else:
            filtered_points = points.copy()
            filtered_object_ids = object_ids.copy()

        return DropoutResult(
            points=filtered_points,
            object_ids=filtered_object_ids,
            dropped_objects=dropped_objects,
            dropout_records=dropout_records,
        )

    def apply_dropout_sequence(
        self,
        frames: List[Tuple[np.ndarray, np.ndarray]],
    ) -> List[DropoutResult]:
        """Apply dropout to a sequence of frames.

        Args:
            frames: List of (points, object_ids) tuples for each frame.

        Returns:
            List of DropoutResult for each frame.
        """
        self.reset()
        results = []

        for frame_id, (points, object_ids) in enumerate(frames):
            result = self.apply_dropout(points, object_ids, frame_id)
            results.append(result)

        return results

    def get_all_dropout_records(self) -> List[DropoutRecord]:
        """Get all dropout records from the current sequence.

        Returns:
            List of all DropoutRecord events.
        """
        return self._all_dropout_records.copy()

    def get_dropout_summary(self) -> Dict:
        """Get summary statistics of dropout events.

        Returns:
            Dictionary with dropout statistics.
        """
        if not self._all_dropout_records:
            return {
                "total_dropouts": 0,
                "unique_objects_dropped": 0,
                "frames_with_dropouts": 0,
                "dropout_rate_actual": 0.0,
            }

        dropped_objects = set(r.object_id for r in self._all_dropout_records)
        frames_with_dropouts = len(
            set(r.frame_id for r in self._all_dropout_records)
        )

        return {
            "total_dropouts": len(self._all_dropout_records),
            "unique_objects_dropped": len(dropped_objects),
            "frames_with_dropouts": frames_with_dropouts,
            "objects_dropped": list(dropped_objects),
        }


class GroundTruthModifier:
    """Modifies ground truth data to reflect dropout events.

    Updates ground truth labels to mark dropped objects appropriately.
    """

    @staticmethod
    def update_ground_truth(
        ground_truth: Dict,
        dropout_records: List[DropoutRecord],
    ) -> Dict:
        """Update ground truth to reflect dropout events.

        Args:
            ground_truth: Original ground truth dictionary with object tracks.
            dropout_records: List of dropout events to apply.

        Returns:
            Modified ground truth with dropout annotations.
        """
        modified_gt = {
            "original": ground_truth.copy(),
            "dropouts": [],
            "tracks": {},
        }

        # Group dropouts by object
        dropouts_by_object: Dict[int, List[int]] = {}
        for record in dropout_records:
            if record.object_id not in dropouts_by_object:
                dropouts_by_object[record.object_id] = []
            dropouts_by_object[record.object_id].append(record.frame_id)

        # Record dropout information
        for obj_id, frame_ids in dropouts_by_object.items():
            modified_gt["dropouts"].append(
                {
                    "object_id": obj_id,
                    "dropped_frames": sorted(frame_ids),
                }
            )

        # Modify tracks if they exist in ground truth
        if "tracks" in ground_truth:
            for track_id, track_data in ground_truth["tracks"].items():
                modified_track = track_data.copy()
                obj_id = track_data.get("object_id", int(track_id))

                if obj_id in dropouts_by_object:
                    dropped_frames = set(dropouts_by_object[obj_id])
                    if "frames" in modified_track:
                        modified_track["frames"] = [
                            f for f in modified_track["frames"]
                            if f not in dropped_frames
                        ]
                    modified_track["dropped_frames"] = sorted(dropped_frames)

                modified_gt["tracks"][track_id] = modified_track

        return modified_gt


def create_dropout_handler(
    dropout_rate: float = 0.1,
    min_consecutive_frames: int = 1,
    seed: Optional[int] = None,
) -> ObjectDropout:
    """Factory function to create an ObjectDropout handler.

    Args:
        dropout_rate: Probability of dropping an object per frame (0-1).
        min_consecutive_frames: Minimum frames before eligible for dropout.
        seed: Random seed for reproducibility.

    Returns:
        Configured ObjectDropout instance.
    """
    config = DropoutConfig(
        dropout_rate=dropout_rate,
        min_consecutive_frames=min_consecutive_frames,
        seed=seed,
    )
    return ObjectDropout(config)
