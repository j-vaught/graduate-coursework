"""
Evaluation metrics for radar tracking.

This module computes Purity, Continuity, MOTA, and MOTP metrics
for evaluating clustering and tracking performance.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

import numpy as np


@dataclass
class ClusteringMetrics:
    """Metrics for clustering evaluation.

    Attributes:
        purity: Cluster purity score (0-1).
        num_clusters: Number of predicted clusters.
        num_ground_truth: Number of ground truth objects.
        cluster_sizes: Distribution of cluster sizes.
        dominant_class_distribution: Distribution of dominant class sizes.
    """

    purity: float
    num_clusters: int
    num_ground_truth: int
    cluster_sizes: Dict[int, int]
    dominant_class_distribution: Dict[int, int]


@dataclass
class TrackingMetrics:
    """Metrics for tracking evaluation.

    Attributes:
        continuity: Track continuity score (0-1).
        mota: Multiple Object Tracking Accuracy.
        motp: Multiple Object Tracking Precision.
        num_tracks: Number of predicted tracks.
        num_ground_truth_tracks: Number of ground truth tracks.
        num_id_switches: Number of ID switches.
        num_fragmentations: Number of track fragmentations.
        mostly_tracked: Number of mostly tracked objects (>80% tracked).
        mostly_lost: Number of mostly lost objects (<20% tracked).
    """

    continuity: float
    mota: Optional[float] = None
    motp: Optional[float] = None
    num_tracks: int = 0
    num_ground_truth_tracks: int = 0
    num_id_switches: int = 0
    num_fragmentations: int = 0
    mostly_tracked: int = 0
    mostly_lost: int = 0


class PurityCalculator:
    """Computes cluster purity metric.

    Purity measures how well clusters correspond to ground truth classes.
    A cluster is pure if all its members belong to the same ground truth class.
    """

    @staticmethod
    def compute_purity(
        cluster_labels: np.ndarray,
        ground_truth_labels: np.ndarray,
    ) -> ClusteringMetrics:
        """Compute cluster purity.

        Purity = (1/N) * sum(max_j |cluster_i AND class_j|)

        Args:
            cluster_labels: Predicted cluster label for each point.
            ground_truth_labels: Ground truth class label for each point.

        Returns:
            ClusteringMetrics with purity score and related statistics.
        """
        if len(cluster_labels) != len(ground_truth_labels):
            raise ValueError(
                "cluster_labels and ground_truth_labels must have same length"
            )

        n_points = len(cluster_labels)
        if n_points == 0:
            return ClusteringMetrics(
                purity=0.0,
                num_clusters=0,
                num_ground_truth=0,
                cluster_sizes={},
                dominant_class_distribution={},
            )

        unique_clusters = np.unique(cluster_labels)
        unique_gt = np.unique(ground_truth_labels)

        # Skip noise label (-1) if present
        unique_clusters = unique_clusters[unique_clusters >= 0]

        total_correct = 0
        cluster_sizes = {}
        dominant_class_dist = {}

        for cluster_id in unique_clusters:
            # Get points in this cluster
            cluster_mask = cluster_labels == cluster_id
            cluster_gt_labels = ground_truth_labels[cluster_mask]

            # Count occurrences of each ground truth class
            class_counts = Counter(cluster_gt_labels)
            dominant_count = max(class_counts.values())

            total_correct += dominant_count
            cluster_size = len(cluster_gt_labels)
            cluster_sizes[int(cluster_id)] = cluster_size
            dominant_class_dist[int(cluster_id)] = dominant_count

        purity = total_correct / n_points if n_points > 0 else 0.0

        return ClusteringMetrics(
            purity=purity,
            num_clusters=len(unique_clusters),
            num_ground_truth=len(unique_gt),
            cluster_sizes=cluster_sizes,
            dominant_class_distribution=dominant_class_dist,
        )

    @staticmethod
    def compute_inverse_purity(
        cluster_labels: np.ndarray,
        ground_truth_labels: np.ndarray,
    ) -> float:
        """Compute inverse purity (completeness).

        Measures how well ground truth classes are contained within clusters.

        Args:
            cluster_labels: Predicted cluster label for each point.
            ground_truth_labels: Ground truth class label for each point.

        Returns:
            Inverse purity score (0-1).
        """
        if len(cluster_labels) != len(ground_truth_labels):
            raise ValueError("Arrays must have same length")

        n_points = len(cluster_labels)
        if n_points == 0:
            return 0.0

        unique_gt = np.unique(ground_truth_labels)
        total_correct = 0

        for gt_id in unique_gt:
            gt_mask = ground_truth_labels == gt_id
            gt_cluster_labels = cluster_labels[gt_mask]

            # Find dominant cluster for this ground truth
            cluster_counts = Counter(gt_cluster_labels)
            dominant_count = max(cluster_counts.values())
            total_correct += dominant_count

        return total_correct / n_points


class ContinuityCalculator:
    """Computes track continuity metric.

    Continuity measures how consistently a tracker maintains object identity
    over time without ID switches.
    """

    @staticmethod
    def compute_continuity(
        track_assignments: Dict[int, List[Tuple[int, int]]],
        ground_truth_tracks: Dict[int, List[int]],
    ) -> TrackingMetrics:
        """Compute track continuity.

        Args:
            track_assignments: Dict mapping frame_id to list of
                (track_id, gt_object_id) assignments.
            ground_truth_tracks: Dict mapping gt_object_id to list
                of frame_ids where object appears.

        Returns:
            TrackingMetrics with continuity and related statistics.
        """
        if not track_assignments or not ground_truth_tracks:
            return TrackingMetrics(
                continuity=0.0,
                num_tracks=0,
                num_ground_truth_tracks=len(ground_truth_tracks) if ground_truth_tracks else 0,
            )

        # Build track-to-gt mapping over time
        track_gt_history: Dict[int, List[int]] = defaultdict(list)
        gt_track_history: Dict[int, List[int]] = defaultdict(list)

        for frame_id, assignments in track_assignments.items():
            for track_id, gt_id in assignments:
                track_gt_history[track_id].append(gt_id)
                gt_track_history[gt_id].append(track_id)

        # Count ID switches
        id_switches = 0
        for gt_id, track_ids in gt_track_history.items():
            if len(track_ids) > 1:
                for i in range(1, len(track_ids)):
                    if track_ids[i] != track_ids[i - 1]:
                        id_switches += 1

        # Count fragmentations (track breaks and restarts)
        fragmentations = 0
        for track_id, gt_ids in track_gt_history.items():
            if len(gt_ids) > 1:
                unique_gt = set(gt_ids)
                # If track covers multiple GT objects, it's fragmenting
                fragmentations += len(unique_gt) - 1

        # Compute continuity as proportion of consistent assignments
        total_assignments = sum(len(v) for v in gt_track_history.values())
        if total_assignments == 0:
            continuity = 0.0
        else:
            # Penalize ID switches
            continuity = max(0.0, 1.0 - (id_switches / total_assignments))

        # Compute mostly tracked / mostly lost
        mostly_tracked = 0
        mostly_lost = 0

        for gt_id, gt_frames in ground_truth_tracks.items():
            if gt_id not in gt_track_history:
                mostly_lost += 1
                continue

            tracked_frames = len(gt_track_history[gt_id])
            total_frames = len(gt_frames)

            if total_frames > 0:
                track_ratio = tracked_frames / total_frames
                if track_ratio >= 0.8:
                    mostly_tracked += 1
                elif track_ratio <= 0.2:
                    mostly_lost += 1

        return TrackingMetrics(
            continuity=continuity,
            num_tracks=len(track_gt_history),
            num_ground_truth_tracks=len(ground_truth_tracks),
            num_id_switches=id_switches,
            num_fragmentations=fragmentations,
            mostly_tracked=mostly_tracked,
            mostly_lost=mostly_lost,
        )


class MOTACalculator:
    """Computes Multiple Object Tracking Accuracy (MOTA).

    MOTA = 1 - (FN + FP + IDSW) / GT

    Where:
        FN = False Negatives (missed detections)
        FP = False Positives
        IDSW = ID Switches
        GT = Ground truth detections
    """

    @staticmethod
    def compute_mota(
        predicted_detections: Dict[int, List[Tuple[float, float, int]]],
        ground_truth_detections: Dict[int, List[Tuple[float, float, int]]],
        distance_threshold: float = 50.0,
    ) -> Tuple[float, Dict[str, int]]:
        """Compute MOTA metric.

        Args:
            predicted_detections: Dict mapping frame_id to list of
                (x, y, track_id) predictions.
            ground_truth_detections: Dict mapping frame_id to list of
                (x, y, object_id) ground truth.
            distance_threshold: Maximum distance for matching.

        Returns:
            Tuple of (MOTA score, statistics dictionary).
        """
        total_gt = 0
        total_fp = 0
        total_fn = 0
        total_idsw = 0

        # Track previous frame matches for ID switch detection
        prev_matches: Dict[int, int] = {}  # gt_id -> track_id

        all_frames = set(predicted_detections.keys()) | set(
            ground_truth_detections.keys()
        )

        for frame_id in sorted(all_frames):
            preds = predicted_detections.get(frame_id, [])
            gts = ground_truth_detections.get(frame_id, [])

            total_gt += len(gts)

            if not gts:
                total_fp += len(preds)
                continue

            if not preds:
                total_fn += len(gts)
                continue

            # Compute distance matrix
            n_preds = len(preds)
            n_gts = len(gts)
            distances = np.zeros((n_preds, n_gts))

            for i, (px, py, _) in enumerate(preds):
                for j, (gx, gy, _) in enumerate(gts):
                    distances[i, j] = np.sqrt((px - gx) ** 2 + (py - gy) ** 2)

            # Greedy matching
            matched_preds: Set[int] = set()
            matched_gts: Set[int] = set()
            current_matches: Dict[int, int] = {}

            while True:
                # Find minimum unmatched distance
                min_dist = float("inf")
                min_i, min_j = -1, -1

                for i in range(n_preds):
                    if i in matched_preds:
                        continue
                    for j in range(n_gts):
                        if j in matched_gts:
                            continue
                        if distances[i, j] < min_dist:
                            min_dist = distances[i, j]
                            min_i, min_j = i, j

                if min_dist > distance_threshold or min_i < 0:
                    break

                matched_preds.add(min_i)
                matched_gts.add(min_j)

                gt_id = gts[min_j][2]
                track_id = preds[min_i][2]
                current_matches[gt_id] = track_id

                # Check for ID switch
                if gt_id in prev_matches and prev_matches[gt_id] != track_id:
                    total_idsw += 1

            # Count FP and FN
            total_fp += n_preds - len(matched_preds)
            total_fn += n_gts - len(matched_gts)

            prev_matches = current_matches

        # Compute MOTA
        if total_gt == 0:
            mota = 0.0
        else:
            mota = 1.0 - (total_fn + total_fp + total_idsw) / total_gt

        stats = {
            "total_gt": total_gt,
            "total_fp": total_fp,
            "total_fn": total_fn,
            "total_idsw": total_idsw,
        }

        return mota, stats


class MOTPCalculator:
    """Computes Multiple Object Tracking Precision (MOTP).

    MOTP = sum(distances for matched pairs) / num_matches

    Measures the average localization error for matched detections.
    """

    @staticmethod
    def compute_motp(
        predicted_detections: Dict[int, List[Tuple[float, float, int]]],
        ground_truth_detections: Dict[int, List[Tuple[float, float, int]]],
        distance_threshold: float = 50.0,
    ) -> Tuple[float, int]:
        """Compute MOTP metric.

        Args:
            predicted_detections: Dict mapping frame_id to list of
                (x, y, track_id) predictions.
            ground_truth_detections: Dict mapping frame_id to list of
                (x, y, object_id) ground truth.
            distance_threshold: Maximum distance for matching.

        Returns:
            Tuple of (MOTP score, number of matches).
        """
        total_distance = 0.0
        total_matches = 0

        all_frames = set(predicted_detections.keys()) | set(
            ground_truth_detections.keys()
        )

        for frame_id in all_frames:
            preds = predicted_detections.get(frame_id, [])
            gts = ground_truth_detections.get(frame_id, [])

            if not preds or not gts:
                continue

            # Compute distance matrix
            n_preds = len(preds)
            n_gts = len(gts)
            distances = np.zeros((n_preds, n_gts))

            for i, (px, py, _) in enumerate(preds):
                for j, (gx, gy, _) in enumerate(gts):
                    distances[i, j] = np.sqrt((px - gx) ** 2 + (py - gy) ** 2)

            # Greedy matching
            matched_preds: Set[int] = set()
            matched_gts: Set[int] = set()

            while True:
                min_dist = float("inf")
                min_i, min_j = -1, -1

                for i in range(n_preds):
                    if i in matched_preds:
                        continue
                    for j in range(n_gts):
                        if j in matched_gts:
                            continue
                        if distances[i, j] < min_dist:
                            min_dist = distances[i, j]
                            min_i, min_j = i, j

                if min_dist > distance_threshold or min_i < 0:
                    break

                matched_preds.add(min_i)
                matched_gts.add(min_j)
                total_distance += min_dist
                total_matches += 1

        if total_matches == 0:
            return 0.0, 0

        motp = total_distance / total_matches
        return motp, total_matches


class MetricsEvaluator:
    """High-level interface for computing all metrics."""

    def __init__(self, distance_threshold: float = 50.0) -> None:
        """Initialize the evaluator.

        Args:
            distance_threshold: Distance threshold for matching.
        """
        self.distance_threshold = distance_threshold

    def evaluate_clustering(
        self,
        cluster_labels: np.ndarray,
        ground_truth_labels: np.ndarray,
    ) -> ClusteringMetrics:
        """Evaluate clustering performance.

        Args:
            cluster_labels: Predicted cluster labels.
            ground_truth_labels: Ground truth labels.

        Returns:
            ClusteringMetrics with purity and related statistics.
        """
        return PurityCalculator.compute_purity(cluster_labels, ground_truth_labels)

    def evaluate_tracking(
        self,
        track_assignments: Dict[int, List[Tuple[int, int]]],
        ground_truth_tracks: Dict[int, List[int]],
        predicted_detections: Optional[
            Dict[int, List[Tuple[float, float, int]]]
        ] = None,
        ground_truth_detections: Optional[
            Dict[int, List[Tuple[float, float, int]]]
        ] = None,
    ) -> TrackingMetrics:
        """Evaluate tracking performance.

        Args:
            track_assignments: Track-to-GT assignments per frame.
            ground_truth_tracks: GT object frame appearances.
            predicted_detections: Predicted detection positions (for MOTA/MOTP).
            ground_truth_detections: GT detection positions (for MOTA/MOTP).

        Returns:
            TrackingMetrics with continuity, MOTA, MOTP.
        """
        metrics = ContinuityCalculator.compute_continuity(
            track_assignments, ground_truth_tracks
        )

        if predicted_detections and ground_truth_detections:
            mota, _ = MOTACalculator.compute_mota(
                predicted_detections,
                ground_truth_detections,
                self.distance_threshold,
            )
            motp, _ = MOTPCalculator.compute_motp(
                predicted_detections,
                ground_truth_detections,
                self.distance_threshold,
            )
            metrics.mota = mota
            metrics.motp = motp

        return metrics

    def summary(
        self,
        clustering_metrics: Optional[ClusteringMetrics] = None,
        tracking_metrics: Optional[TrackingMetrics] = None,
    ) -> Dict:
        """Generate summary dictionary of all metrics.

        Args:
            clustering_metrics: Clustering evaluation results.
            tracking_metrics: Tracking evaluation results.

        Returns:
            Dictionary with all metric values.
        """
        summary = {}

        if clustering_metrics:
            summary["clustering"] = {
                "purity": clustering_metrics.purity,
                "num_clusters": clustering_metrics.num_clusters,
                "num_ground_truth": clustering_metrics.num_ground_truth,
            }

        if tracking_metrics:
            summary["tracking"] = {
                "continuity": tracking_metrics.continuity,
                "mota": tracking_metrics.mota,
                "motp": tracking_metrics.motp,
                "num_tracks": tracking_metrics.num_tracks,
                "num_ground_truth_tracks": tracking_metrics.num_ground_truth_tracks,
                "num_id_switches": tracking_metrics.num_id_switches,
                "num_fragmentations": tracking_metrics.num_fragmentations,
                "mostly_tracked": tracking_metrics.mostly_tracked,
                "mostly_lost": tracking_metrics.mostly_lost,
            }

        return summary


def compute_purity(
    cluster_labels: np.ndarray,
    ground_truth_labels: np.ndarray,
) -> float:
    """Convenience function to compute purity.

    Args:
        cluster_labels: Predicted cluster labels.
        ground_truth_labels: Ground truth labels.

    Returns:
        Purity score (0-1).
    """
    metrics = PurityCalculator.compute_purity(cluster_labels, ground_truth_labels)
    return metrics.purity


def compute_continuity(
    track_assignments: Dict[int, List[Tuple[int, int]]],
    ground_truth_tracks: Dict[int, List[int]],
) -> float:
    """Convenience function to compute continuity.

    Args:
        track_assignments: Track-to-GT assignments per frame.
        ground_truth_tracks: GT object frame appearances.

    Returns:
        Continuity score (0-1).
    """
    metrics = ContinuityCalculator.compute_continuity(
        track_assignments, ground_truth_tracks
    )
    return metrics.continuity
