"""Reconstruct zero-speed AutoNaut pitch amplitudes from Mounet et al. Table 4."""

import argparse
import csv
import math
from pathlib import Path

GRAVITY = 9.81
PROPAGATION_AZIMUTH_DEG = 25.0
CASES = (("reference", 0.35, 0.15), ("largest_registration_gain", 0.3325, 0.432))
# Mounet et al. (2024), Table 4. Section 2.2 sets the block coefficient to one.
AUTO_NAUT_MODELS = (
    ("weighted_average", 4.360, 1.180, 0.265),
    ("simple_mean", 3.760, 1.083, 0.249),
    ("geometry_defaults", 5.000, 0.800, 0.300),
)


def evaluate(case, frequency, amplitude, fit, length, breadth, draught):
    k = math.tau**2 * frequency**2 / GRAVITY
    k_longitudinal = k * abs(math.cos(math.radians(PROPAGATION_AZIMUTH_DEG)))
    # Jensen et al. (2004), Eqs. (2.5), (2.7)–(2.9), (2.12)–(2.13), at U = 0.
    sectional_damping = 2 * math.sin(k * breadth / 2) * math.exp(-k * draught)
    dynamic_damping = sectional_damping**2 / (k * breadth)
    load_factor = math.hypot(1 - k * draught, dynamic_damping)
    response_factor = 1 / math.hypot(1 - 2 * k * draught, dynamic_damping)
    half_phase_span = k_longitudinal * length / 2
    moment_factor = (
        6
        * (math.sin(half_phase_span) - half_phase_span * math.cos(half_phase_span))
        / (length * half_phase_span**2)
    )
    uncorrected_rao = abs(moment_factor) * load_factor * response_factor
    # NetSSE pitchCF uses k in the Smith correction. Jensen Eq. (2.10) prints k_e.
    autonaut_rao = uncorrected_rao * math.exp(-k * draught)
    jensen_rao = uncorrected_rao * math.exp(-k_longitudinal * draught)

    frequency_ratio = frequency / 0.35
    prescribed_dynamic_factor = math.hypot(
        1 - frequency_ratio**2, 2 * 0.15 * frequency_ratio
    )
    prescribed_rao = 0.25 * k_longitudinal / prescribed_dynamic_factor
    return {
        "case": case,
        "wave_frequency_hz": frequency,
        "wave_amplitude_m": amplitude,
        "propagation_azimuth_deg": PROPAGATION_AZIMUTH_DEG,
        "vessel_speed_m_s": 0.0,
        "autonaut_parameter_set": fit,
        "fitted_length_m": length,
        "fitted_breadth_m": breadth,
        "fitted_draught_m": draught,
        "autonaut_rao_rad_m": autonaut_rao,
        "autonaut_peak_pitch_deg": math.degrees(amplitude * autonaut_rao),
        "jensen_smith_rao_rad_m": jensen_rao,
        "prescribed_rao_rad_m": prescribed_rao,
        "prescribed_peak_pitch_deg": math.degrees(amplitude * prescribed_rao),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    rows = [evaluate(*case, *model) for case in CASES for model in AUTO_NAUT_MODELS]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
