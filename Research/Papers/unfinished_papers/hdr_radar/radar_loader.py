"""
radar_loader.py
Simple loader for Furuno HDR radar CSV data.

Each CSV file is one complete antenna revolution (scan).
Columns: Status, Scale, Range, Gain, Angle, EchoValues...

Usage
-----
    from radar_loader import load_scan, load_run, load_runs

    # Single scan
    scan = load_scan("path/to/file.csv")
    scan.echoes       # (n_spokes, 868) uint8 array
    scan.gain         # int  (gain setting for this scan)
    scan.angles       # (n_spokes,) int array, degrees * 512/360 units
    scan.filename     # str

    # All scans in a directory, sorted by filename (= time order)
    run = load_run("path/to/Gain_Sweep_1/")
    run[0].gain, run[0].echoes.shape

    # Multiple directories at once
    runs = load_runs({
        "sweep1": "path/to/Gain_Sweep_1/",
        "sweep2": "path/to/Gain_Sweep_2/",
    })
    runs["sweep1"]   # list of RadarScan
"""

import csv
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np


# ---------------------------------------------------------------------------
# Data container
# ---------------------------------------------------------------------------

@dataclass
class RadarScan:
    """One complete antenna revolution."""
    filename: str
    gain: int              # gain setting (0-100)
    scale: int             # radar range scale setting
    echoes: np.ndarray     # shape (n_spokes, n_bins), dtype uint8
    angles: np.ndarray     # shape (n_spokes,), raw angle units (0-8188, step 4)
    status: np.ndarray     # shape (n_spokes,), status byte per spoke

    @property
    def n_spokes(self) -> int:
        return self.echoes.shape[0]

    @property
    def n_bins(self) -> int:
        return self.echoes.shape[1]

    @property
    def angles_deg(self) -> np.ndarray:
        """Angle in degrees (0-360)."""
        return self.angles * 360.0 / 8192.0


# ---------------------------------------------------------------------------
# Core loader
# ---------------------------------------------------------------------------

def load_scan(filepath: str | Path) -> RadarScan:
    """
    Load a single radar CSV file.

    Parameters
    ----------
    filepath : path to a .csv file

    Returns
    -------
    RadarScan
    """
    filepath = Path(filepath)

    statuses, scales, gains, angles, echo_rows = [], [], [], [], []

    with open(filepath, newline="") as f:
        reader = csv.reader(f)
        next(reader)  # skip header: Status,Scale,Range,Gain,Angle,EchoValues

        for row in reader:
            if len(row) < 6:
                continue
            statuses.append(int(row[0]))
            scales.append(int(row[1]))
            # row[2] is Range (range scale selection) — skipped
            gains.append(int(row[3]))
            angles.append(int(row[4]))
            echo_rows.append(row[5:])

    if not echo_rows:
        raise ValueError(f"No data rows found in {filepath}")

    # Pad echo rows to uniform length (first file in a run may be partial)
    n_bins = max(len(r) for r in echo_rows)
    echoes = np.zeros((len(echo_rows), n_bins), dtype=np.uint8)
    for i, row in enumerate(echo_rows):
        echoes[i, : len(row)] = [int(v) for v in row]

    # The gain is constant within a file; take the mode to handle edge cases
    gain_val = int(np.bincount(gains).argmax())

    return RadarScan(
        filename=filepath.name,
        gain=gain_val,
        scale=scales[0],
        echoes=echoes,
        angles=np.array(angles, dtype=np.int32),
        status=np.array(statuses, dtype=np.uint8),
    )


# ---------------------------------------------------------------------------
# Directory / run loaders
# ---------------------------------------------------------------------------

def load_run(
    directory: str | Path,
    verbose: bool = True,
) -> List[RadarScan]:
    """
    Load all CSV files in a directory as an ordered list of RadarScans.

    Files are sorted by filename (timestamps → chronological order).

    Parameters
    ----------
    directory : path to a data directory (e.g. Gain_Sweep_1/)
    verbose   : print progress

    Returns
    -------
    List of RadarScan, one per file, in time order
    """
    directory = Path(directory)
    files = sorted(directory.glob("*.csv"))

    if not files:
        raise FileNotFoundError(f"No CSV files found in {directory}")

    scans = []
    for i, fpath in enumerate(files):
        if verbose and (i % 20 == 0 or i == len(files) - 1):
            print(f"  Loading {directory.name}: {i+1}/{len(files)}", end="\r")
        scans.append(load_scan(fpath))

    if verbose:
        print(f"  Loaded {directory.name}: {len(scans)} scans, "
              f"gains {scans[0].gain}–{scans[-1].gain}, "
              f"{scans[0].n_spokes} spokes, {scans[0].n_bins} bins")

    return scans


def load_runs(
    directories: Dict[str, str | Path],
    verbose: bool = True,
) -> Dict[str, List[RadarScan]]:
    """
    Load multiple named runs.

    Parameters
    ----------
    directories : dict mapping label -> directory path
    verbose     : print progress

    Returns
    -------
    dict mapping label -> List[RadarScan]

    Example
    -------
    DATA = "/Volumes/MacShare/DATA/FURUNO_data/HDR_Paper_data"
    runs = load_runs({
        "sweep1": f"{DATA}/Gain_Sweep_1",
        "sweep2": f"{DATA}/Gain_Sweep_2",
        "sweep3": f"{DATA}/Gain_Sweep_3",
        "pw1":    f"{DATA}/Gain_PW_Sweep_1",
        "pw2":    f"{DATA}/Gain_PW_Sweep_2",
        "temporal": f"{DATA}/Baseline_G90",
        "baseline": f"{DATA}/Baseline_short_G10",
    })
    """
    return {label: load_run(path, verbose=verbose)
            for label, path in directories.items()}


# ---------------------------------------------------------------------------
# Quantization helpers
# ---------------------------------------------------------------------------

# The Furuno DRS4D-NXT encodes returns as uint8 (0-252), but a histogram of
# any single scan reveals only ~16 dominant spike values — the true 4-bit
# quantization levels, non-linearly (approximately logarithmically) mapped
# to the byte range.  Intermediate byte values appear rarely and are noise.
# These are the 16 canonical levels observed empirically:
CANONICAL_LEVELS = np.array(
    [0, 8, 20, 28, 36, 44, 56, 64, 76, 88, 104, 120, 140, 164, 188, 220, 252],
    dtype=np.uint8,
)


def quantize_to_levels(echoes: np.ndarray) -> np.ndarray:
    """
    Round each echo value to the nearest canonical 4-bit level.

    Returns an array of the same shape with dtype uint8, values drawn
    only from CANONICAL_LEVELS.
    """
    flat = echoes.ravel().astype(np.int16)
    diffs = np.abs(flat[:, None] - CANONICAL_LEVELS.astype(np.int16)[None, :])
    idx = diffs.argmin(axis=1)
    return CANONICAL_LEVELS[idx].reshape(echoes.shape)


def to_4bit(echoes: np.ndarray) -> np.ndarray:
    """
    Map echo values to 4-bit indices (0-16) based on nearest canonical level.

    Useful for analysis that needs integer level indices rather than
    raw byte values.
    """
    flat = echoes.ravel().astype(np.int16)
    diffs = np.abs(flat[:, None] - CANONICAL_LEVELS.astype(np.int16)[None, :])
    return diffs.argmin(axis=1).reshape(echoes.shape).astype(np.uint8)


# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------

def scans_to_gain_stack(scans: List[RadarScan]) -> tuple[np.ndarray, np.ndarray]:
    """
    Stack a gain-sweep run into a 3-D array indexed by [gain_step, spoke, bin].

    Only uses scans with complete spoke counts (skips partial first scan).

    Returns
    -------
    stack  : (n_scans, n_spokes, n_bins) uint8
    gains  : (n_scans,) int  — gain value for each scan
    """
    # Filter to complete scans
    max_spokes = max(s.n_spokes for s in scans)
    complete = [s for s in scans if s.n_spokes == max_spokes]

    n_bins = complete[0].n_bins
    stack = np.stack([s.echoes for s in complete], axis=0)
    gains = np.array([s.gain for s in complete], dtype=np.int32)
    return stack, gains


# ---------------------------------------------------------------------------
# Quick sanity-check when run directly
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    DATA = "/Volumes/MacShare/DATA/FURUNO_data/HDR_Paper_data"

    print("Loading Gain_Sweep_1...")
    sweep = load_run(f"{DATA}/Gain_Sweep_1")
    print(f"  {len(sweep)} scans")
    print(f"  Gains: {sweep[0].gain} -> {sweep[-1].gain}")
    print(f"  Shape: {sweep[0].echoes.shape}")
    print(f"  Echo range: {sweep[0].echoes.min()} – {sweep[-1].echoes.max()}")

    stack, gains = scans_to_gain_stack(sweep)
    print(f"  Gain stack shape: {stack.shape}")
    print(f"  Gains array: {gains[:5]} ... {gains[-5:]}")
    print()

    print("Loading Baseline_G90...")
    temporal = load_run(f"{DATA}/Baseline_G90")
    print(f"  {len(temporal)} scans, all at gain {temporal[0].gain}")
