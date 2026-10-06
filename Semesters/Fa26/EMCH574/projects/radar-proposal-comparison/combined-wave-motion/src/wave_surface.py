"""Reproducible linear random sea for the wave-obstruction figure.

J.C. Vaught. Numerical data only; Typst/Lilaq draws the figure.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    """Synthesize a long-crested, finite-depth Airy wave field."""
    gravity, depth, hs, tp = 9.81, 50.0, 1.0, 9.0
    fmin, fmax, components, seed = 0.04, 0.50, 1024, 2026
    df = (fmax - fmin) / components
    frequency = fmin + (np.arange(components) + 0.5) * df
    fp = 1 / tp
    spectrum = (5 / 16) * hs**2 * fp**4 * frequency**-5
    spectrum *= np.exp(-(5 / 4) * (fp / frequency) ** 4)
    target_variance = hs**2 / 16
    # Preserve specified spectral Hs after finite-band midpoint quadrature.
    quadrature_variance = float(np.sum(spectrum) * df)
    spectrum *= target_variance / quadrature_variance
    amplitude = np.sqrt(2 * spectrum * df)
    omega = 2 * np.pi * frequency
    wavenumber = np.array(
        [brentq(lambda k, w=w: gravity * k * np.tanh(k * depth) - w**2, 1e-10, 10) for w in omega]
    )
    phase = np.random.default_rng(seed).uniform(0, 2 * np.pi, components)
    x = np.linspace(0, 500, 2001)
    spatial_phase = x[:, None] * wavenumber + phase
    snapshots = [
        {
            "time_s": t,
            "elevation_m": (np.cos(spatial_phase - omega * t) @ amplitude).tolist(),
        }
        for t in (0.0, 2.0, 4.0)
    ]
    slope = -np.sin(spatial_phase) @ (amplitude * wavenumber)
    spectral_variance = float(np.sum(amplitude**2) / 2)
    dispersion_error = float(
        np.max(np.abs(gravity * wavenumber * np.tanh(wavenumber * depth) - omega**2) / omega**2)
    )
    kp = brentq(lambda k: gravity * k * np.tanh(k * depth) - (2 * np.pi * fp) ** 2, 1e-10, 10)
    checks = {
        "spectral_significant_height_m": 4 * np.sqrt(spectral_variance),
        "finite_band_variance_fraction": quadrature_variance / target_variance,
        "maximum_relative_dispersion_residual": dispersion_error,
        "maximum_absolute_surface_slope_at_t0": float(np.max(np.abs(slope))),
        "points_per_shortest_wavelength": float(2 * np.pi / wavenumber.max() / (x[1] - x[0])),
        "peak_wavelength_m": 2 * np.pi / kp,
    }
    assert np.isfinite(np.array(snapshots[0]["elevation_m"])).all()
    assert abs(checks["spectral_significant_height_m"] - hs) < 1e-12
    assert dispersion_error < 1e-9
    assert checks["points_per_shortest_wavelength"] > 20
    assert checks["maximum_absolute_surface_slope_at_t0"] < 0.2
    data = {
        "model": "Long-crested linear Airy superposition with ISSC/Bretschneider spectrum",
        "parameters": {
            "gravity_m_s2": gravity,
            "depth_m": depth,
            "significant_height_m": hs,
            "peak_period_s": tp,
            "seed": seed,
            "components": components,
            "frequency_band_hz": [fmin, fmax],
        },
        "equations": {
            "surface": "eta(x,t) = sum_j a_j cos(k_j x - omega_j t + phi_j)",
            "dispersion": "omega_j^2 = g k_j tanh(k_j h)",
            "amplitude": "a_j = sqrt(2 S(f_j) Delta_f)",
            "spectrum": "S(f) = (5/16) Hs^2 fp^4 f^-5 exp[-(5/4)(fp/f)^4]",
        },
        "x_m": x.tolist(),
        "snapshots": snapshots,
        "checks": checks,
    }
    output = ROOT / "data/wave-surface.json"
    output.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    with (ROOT / "data/wave-components.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["frequency_hz", "wavenumber_per_m", "amplitude_m", "phase_rad"])
        writer.writerows(zip(frequency, wavenumber, amplitude, phase, strict=True))
    print(json.dumps(checks, indent=2))


if __name__ == "__main__":
    main()
