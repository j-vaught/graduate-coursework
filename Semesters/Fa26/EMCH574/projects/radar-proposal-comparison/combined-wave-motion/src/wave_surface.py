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
    # Object geometry is chosen for this snapshot; ray contact uses the exact
    # continuous Fourier surface, not a hand-selected drawing intersection.
    radar_x, radar_height, object_x, object_height = 25.0, 0.8, 375.0, 0.5

    def elevation(position: float) -> float:
        return float(np.cos(wavenumber * position + phase) @ amplitude)

    object_base = elevation(object_x)
    object_top = object_base + object_height

    def contact(endpoint_x: float, endpoint_height: float) -> tuple[float, float]:
        ray_slope = (endpoint_height - radar_height) / (endpoint_x - radar_x)
        clearance = np.asarray(snapshots[0]["elevation_m"]) - (
            radar_height + ray_slope * (x - radar_x)
        )
        hits = np.flatnonzero((x > radar_x) & (x < endpoint_x) & (clearance >= 0))
        assert hits.size > 0
        j = int(hits[0])
        hit_x = brentq(
            lambda position: (
                elevation(position) - (radar_height + ray_slope * (position - radar_x))
            ),
            float(x[j - 1]),
            float(x[j]),
        )
        hit_y = radar_height + ray_slope * (hit_x - radar_x)
        assert abs(elevation(hit_x) - hit_y) < 1e-10
        return hit_x, hit_y

    direct_contact = contact(object_x, object_top)
    lower_boundary_contact = contact(475.0, -0.1)
    direct_height = radar_height + (object_top - radar_height) * (x - radar_x) / (
        object_x - radar_x
    )
    intrusion = np.asarray(snapshots[0]["elevation_m"]) - direct_height
    mask = (x > radar_x) & (x < object_x)
    max_intrusion = float(np.max(intrusion[mask]))
    assert max_intrusion > 0.2
    obstruction = {
        "radar_x_m": radar_x,
        "radar_height_m": radar_height,
        "object_x_m": object_x,
        "object_base_m": object_base,
        "object_top_m": object_top,
        "object_height_m": object_height,
        "object_width_m": 8.0,
        "direct_contact_m": list(direct_contact),
        "lower_schematic_boundary_contact_m": list(lower_boundary_contact),
        "maximum_direct_path_intrusion_m": max_intrusion,
    }
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
        "obstruction_example": obstruction,
    }
    output = ROOT / "data/wave-surface.json"
    output.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    with (ROOT / "data/wave-components.csv").open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["frequency_hz", "wavenumber_per_m", "amplitude_m", "phase_rad"])
        writer.writerows(zip(frequency, wavenumber, amplitude, phase, strict=True))
    print(json.dumps({"wave_checks": checks, "obstruction": obstruction}, indent=2))


if __name__ == "__main__":
    main()
