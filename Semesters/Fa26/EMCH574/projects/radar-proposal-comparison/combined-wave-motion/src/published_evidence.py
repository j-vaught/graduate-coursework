"""Compute a published visibility model and analyze one measured IPIX record.

J.C. Vaught. Numerical outputs only. Typst/CeTZ authors every figure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

import numpy as np
from numpy.typing import NDArray
from scipy.io import netcdf_file
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/19931107_135603_starea.cdf"
SOURCE = "https://soma.ece.mcmaster.ca/ipix/dartmouth/data/19931107_135603_starea.cdf"
EXPECTED_SHA256 = "0476ddbba6953b2a95e1ca341ed1bfaf0da827114d7520fbffbdebfd9021e0a8"
FLOAT = NDArray[np.float64]


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def harmonic_visibility(height_ratio: float, phases: int, step: float) -> tuple[FLOAT, FLOAT]:
    """Wijaya 2016 Eqs. 3.4 and 3.7 on the normalized harmonic surface.

    A surface point is visible iff its slope from the radar exceeds the
    maximum slope to every nearer surface point. The endpoint is not tested
    against itself. Normalization uses h = H_r/A, not H_r/H_s for this case.
    """
    rho = np.arange(1, round(20 / step) + 1, dtype=np.float64) * step
    sample_rho = np.linspace(4, 20, 161)
    indices = np.rint(sample_rho / step).astype(int) - 1
    assert np.allclose(rho[indices], sample_rho, rtol=0, atol=1e-12)
    count = np.zeros(sample_rho.size, dtype=np.float64)
    for start in range(0, phases, 70):
        phi = (2 * np.pi / phases) * np.arange(start, min(start + 70, phases))
        surface = np.cos(2 * np.pi * rho[None, :] + phi[:, None])
        slope = (surface - height_ratio) / rho[None, :]
        horizon = np.maximum.accumulate(slope, axis=1)
        previous = horizon[:, indices - 1]
        count += np.sum(slope[:, indices] >= previous, axis=0)
    return sample_rho, count / phases


def published_model() -> dict:
    """Reproduce the harmonic visibility experiment preceding the joint model."""
    period = 9.0
    depth = 50.0
    gravity = 9.81
    omega = 2 * np.pi / period
    wavenumber = brentq(lambda k: gravity * k * np.tanh(k * depth) - omega**2, 1e-8, 1)
    wavelength = 2 * np.pi / wavenumber
    rho, h5 = harmonic_visibility(5, 1400, 0.0025)
    _, h10 = harmonic_visibility(10, 1400, 0.0025)
    _, h5_refined = harmonic_visibility(5, 2800, 0.00125)
    _, h10_refined = harmonic_visibility(10, 2800, 0.00125)
    difference = max(np.max(abs(h5 - h5_refined)), np.max(abs(h10 - h10_refined)))
    assert difference < 0.003
    assert np.all(h10 >= h5 - 0.002)
    assert np.isfinite(h5).all() and np.isfinite(h10).all()
    # Lund 2018 acquisition-time horizontal georeferencing, evaluated in its
    # constant-heading/constant-speed limit. Speed comes from the paper's
    # 11 kn example. This calculation is not a reproduction of field errors.
    rotation_period = 1.25
    speed_m_s = 11 * 1852 / 3600
    scan_phase = np.linspace(0, 1, 101)
    held_pose_error = speed_m_s * rotation_period * abs(scan_phase - 0.5)
    return {
        "source": "Wijaya2016Shadowing",
        "equations": "Dissertation chapter 3 Eqs. 3.4 and 3.7; Fig. 3.4 parameter case.",
        "kind": "Calculation from published equations. Not measured data or digitized curves.",
        "parameters": {
            "period_s": period,
            "depth_m": depth,
            "gravity_m_s2": gravity,
            "amplitude_m": 1,
            "radar_height_m": [5, 10],
            "wavelength_m": wavelength,
            "phase_samples": 1400,
            "radial_step_wavelengths": 0.0025,
            "phase_rule": "Uniform complete period, endpoint excluded.",
        },
        "rho": rho.tolist(),
        "range_m": (rho * wavelength).tolist(),
        "visibility_h5": h5.tolist(),
        "visibility_h10": h10.tolist(),
        "lund": {
            "source": "Lund2018SeaIceDrift",
            "kind": "Constant-motion limit of published ray-time mapping. Computed errors.",
            "rotation_period_s": rotation_period,
            "speed_kn": 11,
            "speed_m_s": speed_m_s,
            "range_grid_m": 7.5,
            "scan_fraction": scan_phase.tolist(),
            "midpoint_error_m": held_pose_error.tolist(),
            "per_ray_ideal_error_m": np.zeros(scan_phase.size).tolist(),
            "maximum_midpoint_error_m": float(np.max(held_pose_error)),
        },
        "checks": {
            "joint_phase_and_path_refinement_max_abs_change": float(difference),
            "h5_visibility_at_4_10_20": h5[[0, 60, 160]].tolist(),
            "h10_visibility_at_4_10_20": h10[[0, 60, 160]].tolist(),
            "normalization_invariance": "The skyline depends only on H_r/A and r/lambda.",
        },
    }


def scalar(variables: dict, name: str) -> float:
    return float(np.asarray(variables[name].data).item())


def measured_record() -> dict:
    """Fixed power gate after one common clutter-trained I/Q correction.

    Avoid per-bin normalization, seconds conversion, and visibility labels.
    No samples after the development boundary train the receiver correction,
    reference power, or threshold. Target bins 8 through 11 are excluded.
    """
    digest = hashlib.sha256(RAW.read_bytes()).hexdigest()
    assert digest == EXPECTED_SHA256, "Measured input does not match the source manifest."
    with netcdf_file(RAW, "r", mmap=False) as record:
        variables = record.variables
        adc = variables["adc_data"]
        assert adc.dimensions == ("nsweep", "ntxpol", "nrange", "nadc")
        assert adc.data.shape == (131072, 2, 14, 4)
        assert record.TX_polarization == b"A"
        assert not {"_FillValue", "missing_value"}.intersection(adc._attributes)
        # Match the official loader's unsigned(..., 1), preserving all 8 bits.
        unsigned = adc.data.view(np.uint8)
        i_channel = int(scalar(variables, "adc_like_I"))
        q_channel = int(scalar(variables, "adc_like_Q"))
        in_phase = unsigned[:, 0, :, i_channel].astype(np.float64)
        quadrature = unsigned[:, 0, :, q_channel].astype(np.float64)
        ranges = np.asarray(variables["range"].data, dtype=np.float64).tolist()
        source_metadata = {
            "collection_date_utc": record.Data_collection_date.decode(),
            "rf_ghz": scalar(variables, "RF_frequency"),
            "prf_hz": scalar(variables, "PRF"),
            "prf_description": variables["PRF"].long_name.decode(),
            "unambiguous_velocity_m_s": scalar(variables, "Unambig_velocity"),
            "antenna_height_m": scalar(variables, "radar_elev"),
            "beamwidth_deg": scalar(variables, "antenna_beamwidth"),
            "range_bin_near_edges_m": ranges,
        }

    development_sweeps = 32768
    window_sweeps = 64
    target_index = 8
    clutter_indices = np.array([0, 1, 2, 3, 4, 5, 6, 11, 12, 13])
    dev_i = in_phase[:development_sweeps, clutter_indices].reshape(-1)
    dev_q = quadrature[:development_sweeps, clutter_indices].reshape(-1)
    mean_i, mean_q = float(dev_i.mean()), float(dev_q.mean())
    std_i, std_q = float(dev_i.std()), float(dev_q.std())
    normalized_i = (in_phase - mean_i) / std_i
    normalized_q = (quadrature - mean_q) / std_q
    sin_beta = float(
        np.mean(
            normalized_i[:development_sweeps, clutter_indices]
            * normalized_q[:development_sweeps, clutter_indices]
        )
    )
    corrected_i = (normalized_i - normalized_q * sin_beta) / np.sqrt(1 - sin_beta**2)
    power = corrected_i**2 + normalized_q**2
    assert np.isfinite(power).all()
    integrated = power.reshape(-1, window_sweeps, 14).mean(axis=1)
    ndev = development_sweeps // window_sweeps
    dev_clutter = integrated[:ndev, clutter_indices].reshape(-1)
    baseline = float(dev_clutter.mean())
    threshold = float(np.quantile(dev_clutter, 0.99, method="higher"))
    db = 10 * np.log10(integrated / baseline)
    threshold_db = float(10 * np.log10(threshold / baseline))
    target_test = integrated[ndev:, target_index]
    clutter_test = integrated[ndev:, clutter_indices].reshape(-1)
    decision = target_test > threshold
    # First complete test window follows the boundary. Plot all held-out data.
    sweep_centers = np.arange(ndev, integrated.shape[0]) * window_sweeps + (window_sweeps - 1) / 2
    edges = np.linspace(-15, 15, 241)
    target_db = db[ndev:, target_index]
    clutter_db = db[ndev:, clutter_indices].reshape(-1)
    primary_ccdf = np.array([(target_db > edge).mean() for edge in edges])
    clutter_ccdf = np.array([(clutter_db > edge).mean() for edge in edges])
    padded = np.pad(~decision, (1, 1), constant_values=False)
    boundaries = np.flatnonzero(np.diff(padded.astype(int)))
    run_windows = boundaries[1::2] - boundaries[::2]
    # Threshold crossings are a primary-bin proxy, not truth-labeled detection.
    gate_sensitivity = {
        f"bin_{index + 1}_below_gate_fraction": float(
            (integrated[ndev:, index] <= threshold).mean()
        )
        for index in range(7, 11)
    }
    missing = int(np.count_nonzero(~np.isfinite(in_phase) | ~np.isfinite(quadrature)))
    assert missing == 0
    assert dev_clutter.size == 5120 and clutter_test.size == 15360
    assert decision.size == 1536
    assert float((dev_clutter > threshold).mean()) <= 0.01
    return {
        "kind": "Measured IPIX acquisition with stated processing. No wave-visibility truth.",
        "source_url": SOURCE,
        "sha256": digest,
        "source_bytes": RAW.stat().st_size,
        "metadata": source_metadata,
        "processing": {
            "polarization": "HH",
            "unsigned_byte_reinterpretation": True,
            "development_sweeps": [0, development_sweeps - 1],
            "test_sweeps": [development_sweeps, 131071],
            "window_sweeps": window_sweeps,
            "target_bin_1based": 9,
            "clutter_bins_1based": (clutter_indices + 1).tolist(),
            "secondary_target_bins_excluded": [8, 9, 10, 11],
            "common_i_mean_counts": mean_i,
            "common_q_mean_counts": mean_q,
            "common_i_std_counts": std_i,
            "common_q_std_counts": std_q,
            "common_phase_imbalance_sine": sin_beta,
            "reference_power": baseline,
            "threshold_reference_db": threshold_db,
            "quantile_rule": "Development clutter 0.99 quantile, higher interpolation.",
            "sample_clock": "Sweep index retained. File and tutorial PRF conventions conflict.",
            "missing_or_nonfinite_samples": missing,
            "fill_metadata": "No _FillValue or missing_value declared in this record.",
            "adc_boundary_fraction": float(
                np.mean(
                    (in_phase == 0) | (in_phase == 255) | (quadrature == 0) | (quadrature == 255)
                )
            ),
        },
        "sweep_index_thousands": (sweep_centers / 1000).tolist(),
        "primary_power_db": target_db.tolist(),
        "clutter_bin4_power_db": db[ndev:, 3].tolist(),
        "power_axis_db": edges.tolist(),
        "primary_ccdf": primary_ccdf.tolist(),
        "clutter_ccdf": clutter_ccdf.tolist(),
        "summary": {
            "development_clutter_decisions": int(dev_clutter.size),
            "test_clutter_decisions": int(clutter_test.size),
            "test_primary_decisions": int(decision.size),
            "development_above_gate_fraction": float((dev_clutter > threshold).mean()),
            "test_clutter_above_gate_fraction": float((clutter_test > threshold).mean()),
            "test_primary_below_gate_fraction": float((~decision).mean()),
            "test_primary_mean_power_db": float(10 * np.log10(target_test.mean() / baseline)),
            "test_clutter_mean_power_db": float(10 * np.log10(clutter_test.mean() / baseline)),
            "max_primary_below_gate_run_sweeps": int(np.max(run_windows, axis=0)) * window_sweeps,
            "primary_below_gate_run_count": int(run_windows.size),
            "target_bin_sensitivity": gate_sensitivity,
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="Download the source if absent.")
    args = parser.parse_args()
    if not RAW.exists():
        if not args.download:
            raise SystemExit(
                "Measured record absent. Run with --download to obtain the official file."
            )
        RAW.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(SOURCE, timeout=45) as response:
            RAW.write_bytes(response.read())
    published = published_model()
    measured = measured_record()
    write_json(ROOT / "data/published-model.json", published)
    write_json(ROOT / "data/measured-ipix.json", measured)
    print(json.dumps({"published_checks": published["checks"], "measured": measured["summary"]}))


if __name__ == "__main__":
    main()
