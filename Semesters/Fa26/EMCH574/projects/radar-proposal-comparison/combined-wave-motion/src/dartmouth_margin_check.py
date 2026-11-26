"""Bound possible threshold recovery across the official Dartmouth target records."""

import argparse
import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from shutil import copyfileobj
from urllib.request import urlopen

import numpy as np
from scipy.io import netcdf_file

CATALOG = "https://soma.ece.mcmaster.ca/ipix/dartmouth/datasets.html"
DATA_URL = "https://soma.ece.mcmaster.ca/ipix/dartmouth/data/"
WINDOW_SWEEPS = 64
BOOST_DB = 0.81
REFERENCE_HASH = "0476ddbba6953b2a95e1ca341ed1bfaf0da827114d7520fbffbdebfd9021e0a8"


@dataclass(frozen=True)
class Recording:
    identifier: int
    filename: str
    primary: int
    possible_target_bins: tuple[int, int]


# One-based range-bin labels and filenames are from the official catalog.
RECORDINGS = (
    Recording(17, "19931107_135603_starea.cdf", 9, (8, 11)),
    Recording(18, "19931107_141630_starea.cdf", 9, (8, 11)),
    Recording(19, "19931107_145028_starea.cdf", 8, (7, 9)),
    Recording(25, "19931108_213827_starea.cdf", 7, (6, 8)),
    Recording(26, "19931108_220902_starea.cdf", 7, (6, 8)),
    Recording(30, "19931109_191449_starea.cdf", 7, (6, 8)),
    Recording(31, "19931109_202217_starea.cdf", 7, (6, 9)),
    Recording(40, "19931110_001635_starea.cdf", 7, (5, 8)),
    Recording(54, "19931111_163625_starea.cdf", 8, (7, 10)),
    Recording(280, "19931118_023604_stareC0000.cdf", 8, (7, 10)),
    Recording(283, "19931118_035737_stareC0000.cdf", 10, (8, 12)),
    Recording(310, "19931118_162155_stareC0000.cdf", 7, (6, 9)),
    Recording(311, "19931118_162658_stareC0000.cdf", 7, (6, 9)),
    Recording(320, "19931118_174259_stareC0000.cdf", 7, (6, 9)),
)


def fetch(record, directory, download):
    path = directory / record.filename
    if path.is_file():
        return path
    if not download:
        raise FileNotFoundError(f"{path} is missing. Pass --download to retrieve official files.")
    directory.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(".part")
    with urlopen(DATA_URL + record.filename, timeout=90) as response, partial.open("wb") as target:
        copyfileobj(response, target)
    partial.replace(path)
    return path


def process(record, path):
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if record.identifier == 17:
        assert digest == REFERENCE_HASH
    with netcdf_file(path, "r", mmap=False) as source:
        variables = source.variables
        adc = variables["adc_data"]
        assert adc.data.dtype.itemsize == 1
        assert not {"_FillValue", "missing_value"}.intersection(adc._attributes)
        unsigned = adc.data.view(np.uint8)
        if source.TX_polarization == b"A":
            assert adc.dimensions == ("nsweep", "ntxpol", "nrange", "nadc")
            unsigned = unsigned[:, 0, :, :]
        else:
            assert source.TX_polarization == b"H"
            assert adc.dimensions == ("nsweep", "nrange", "nadc")
        i_channel = int(variables["adc_like_I"].data.item())
        q_channel = int(variables["adc_like_Q"].data.item())
        iq = unsigned[:, :, [i_channel, q_channel]].astype(np.float64)
        near_edges = np.asarray(variables["range"].data)
        metadata = {
            "record_id": record.identifier,
            "catalog": CATALOG,
            "official_file": DATA_URL + record.filename,
            "bytes": path.stat().st_size,
            "sha256": digest,
            "collection_time": source.Data_collection_date.decode(),
            "rf_ghz": float(variables["RF_frequency"].data.item()),
            "antenna_height_m": float(variables["radar_elev"].data.item()),
            "primary_bin_1based": record.primary,
            "primary_range_near_edge_m": float(near_edges[record.primary - 1]),
        }

    sweeps, bins, _ = iq.shape
    first, last = record.possible_target_bins
    assert 1 <= first <= record.primary <= last <= bins
    clutter = np.array([index - 1 for index in range(1, bins + 1) if not first <= index <= last])
    dev_windows = sweeps // (4 * WINDOW_SWEEPS)
    split = dev_windows * WINDOW_SWEEPS
    usable_sweeps = (sweeps // WINDOW_SWEEPS) * WINDOW_SWEEPS
    dev_iq = iq[:split, clutter].reshape(-1, 2)
    scaled = (iq - dev_iq.mean(axis=0)) / dev_iq.std(axis=0)
    in_phase, quadrature = scaled[:, :, 0], scaled[:, :, 1]
    imbalance = np.mean(in_phase[:split, clutter] * quadrature[:split, clutter])
    corrected_i = (in_phase - imbalance * quadrature) / np.sqrt(1 - imbalance**2)
    power = corrected_i**2 + quadrature**2
    integrated = power[:usable_sweeps].reshape(-1, WINDOW_SWEEPS, bins).mean(axis=1)
    dev_clutter = integrated[:dev_windows, clutter].ravel()
    db = 10 * np.log10(integrated / np.mean(dev_clutter))
    assert np.isfinite(db).all()
    metadata.update(
        catalog_possible_target_bins_1based=f"{first}:{last}",
        clutter_bins_1based=" ".join(str(index + 1) for index in clutter),
        window_sweeps=WINDOW_SWEEPS,
        development_sweep_start=0,
        development_sweep_stop_exclusive=split,
        heldout_sweep_start=split,
        heldout_sweep_stop_exclusive=usable_sweeps,
        trailing_sweeps_discarded=sweeps - usable_sweeps,
    )
    return (
        metadata,
        db[:dev_windows, clutter].ravel(),
        db[dev_windows:, clutter].ravel(),
        db[dev_windows:, record.primary - 1],
    )


def score(dev, clutter, target):
    threshold = float(np.quantile(dev, 0.99, method="higher"))
    target_margin = target - threshold
    recoverable = (-BOOST_DB <= target_margin) & (target_margin < 0)
    return {
        "threshold_db_relative_to_local_dev_mean": threshold,
        "heldout_clutter_crossings": int(np.count_nonzero(clutter >= threshold)),
        "heldout_clutter_crossing_pct": float(np.mean(clutter >= threshold) * 100),
        "heldout_primary_misses": int(np.count_nonzero(target_margin < 0)),
        "heldout_primary_miss_pct": float(np.mean(target_margin < 0) * 100),
        "recoverable_0p81db_windows": int(recoverable.sum()),
        "recovery_upper_bound_pp": float(recoverable.mean() * 100),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    records = [process(record, fetch(record, args.raw_dir, args.download)) for record in RECORDINGS]

    rows = []
    for index, (metadata, dev, clutter, target) in enumerate(records):
        other_development = np.concatenate(
            [item[1] for i, item in enumerate(records) if i != index]
        )
        row = dict(
            **metadata,
            local_dev_clutter_windows=len(dev),
            other_dev_clutter_windows=len(other_development),
            heldout_clutter_windows=len(clutter),
            heldout_primary_windows=len(target),
        )
        for label, development in (("local", dev), ("other_records", other_development)):
            result = score(development, clutter, target)
            row.update({f"{label}_{name}": value for name, value in result.items()})
        rows.append(row)

    reference = rows[0]
    assert reference["local_heldout_primary_misses"] == 1023
    assert reference["local_recoverable_0p81db_windows"] == 38
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"Reproduced the #17 result and scored {len(rows)} records in {args.output}.")


if __name__ == "__main__":
    main()
