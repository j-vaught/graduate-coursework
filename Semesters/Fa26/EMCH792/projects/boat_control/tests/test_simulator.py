"""Physical, causal, reproducibility, and feature-isolation acceptance checks."""

from __future__ import annotations

import json
import math
import unittest
from dataclasses import replace
from typing import cast

import numpy as np

from blueboat_sim.config import Experiment, from_dict, presets
from blueboat_sim.engine import (
    Command,
    CommandChange,
    Measurement,
    Observation,
    default_commands,
    run,
)
from blueboat_sim.physics import Physics, mapped_force, motor_after, physical, trim
from propulsion import FORCE, static_force
from simulate import P, rhs


class SimulatorTests(unittest.TestCase):
    def small(self, stage: str = "04_timing") -> Experiment:
        return replace(presets()[stage], duration_s=0.3, integration_step_s=0.005)

    def test_config_roundtrip_and_rejects_unknown_flags(self) -> None:
        for c in presets().values():
            self.assertEqual(from_dict(c.resolved()), c)
        for data in (
            {"flags": {"typo": True}},
            {"flags": {"wind": "false"}},
            {"duration_s": 0},
            {"seed": -1},
            {"seed": "bad"},
            {"flags": {"nonlinear_thrust": True}},
            {"sensors": {"imu_period_s": 0}},
            {"initial_state": [0, 0]},
            {"flags": {"gusts": True}},
            {"name": "../outside"},
            {"flags": {"timing_jitter": True}},
            {"flags": {"command_watchdog": True}},
            {"sensors": {"imu_period_s": 1e-9}},
            {"initial_state": [0, 0, 0, True, 0, 0]},
        ):
            with self.subTest(data=data), self.assertRaises((ValueError, TypeError)):
                from_dict(data)
        c = replace(self.small(), environment=replace(Experiment().environment, gust_period_s=1e-9))
        self.assertEqual(len(Physics(c).gust_times), 1)

    def test_nonlinear_physics_matches_report(self) -> None:
        c = presets()["01_hull"]
        p = physical(c)
        self.assertEqual(p.mass, P.mass_kg)
        self.assertEqual(p.inertia, P.yaw_inertia_kg_m2)
        model = Physics(c)
        for state in ([1, 2, 0.3, 0.8, -0.2, 0.1], [0, 0, -1, -0.3, 0.1, -0.2]):
            z = np.asarray(state, dtype=float)
            np.testing.assert_allclose(
                model.rhs(0, z, np.array([10, 15])), rhs(z, 10, 15, (0, 0)), atol=1e-12
            )

    def test_local_linearization_matches_nonlinear_jacobian(self) -> None:
        linear = Physics(presets()["00_linear"])
        nonlinear = Physics(presets()["01_hull"])
        z = np.array([0, 0, 0, 1, 0, 0], dtype=float)
        force = np.array([7, 7], dtype=float)
        h = 1e-5
        for column in range(6):
            d = np.eye(6)[column] * h
            a = (linear.rhs(0, z + d, force) - linear.rhs(0, z - d, force)) / (2 * h)
            b = (nonlinear.rhs(0, z + d, force) - nonlinear.rhs(0, z - d, force)) / (2 * h)
            np.testing.assert_allclose(a, b, atol=1e-9)
        f, pulse, slope = trim(presets()["00_linear"])
        self.assertAlmostEqual(f, 7)
        self.assertAlmostEqual(mapped_force(pulse, presets()["00_linear"]), 7)
        self.assertGreater(slope, 0)

    def test_added_mass_energy_balance(self) -> None:
        c = presets()["07_uncertainty"]
        c = replace(
            c,
            flags=replace(
                c.flags,
                wind=False,
                gusts=False,
                apparent_wind=False,
                wind_yaw_moment=False,
                wave_forcing=False,
            ),
        )
        model = Physics(c)
        z = np.array([0, 0, 0.3, 0.8, -0.2, 0.15])
        derivative = model.rhs(0, z, np.zeros(2))
        p = physical(c)
        measured = np.dot(np.array([p.mx, p.my, p.iz]) * z[3:], derivative[3:])
        expected = -p.d1 * z[3] ** 2 - p.d2 * abs(z[3]) ** 3 - p.dv * z[4] ** 2 - p.dr * z[5] ** 2
        self.assertAlmostEqual(float(measured), expected, places=12)

    def test_signed_map_deadband_and_saturation(self) -> None:
        c = presets()["02_m200"]
        for pwm in (1000, 1100, 1450, 1475, 1500, 1525, 1700, 1900, 2000):
            self.assertAlmostEqual(mapped_force(pwm, c), static_force(pwm))
        symmetric = replace(c, flags=replace(c.flags, reverse_asymmetry=False))
        self.assertAlmostEqual(mapped_force(1100, symmetric), -float(FORCE.max()))

    def test_motor_analytic_response_and_rate_bound(self) -> None:
        c = presets()["03_motor"]
        c = replace(c, flags=replace(c.flags, motor_rate_limit=False))
        initial, target = np.zeros(2), np.array([30, -15])
        np.testing.assert_allclose(
            motor_after(initial, target, 0.2, c), target * (1 - math.exp(-1)), atol=1e-12
        )
        c = replace(c, flags=replace(c.flags, motor_rate_limit=True))
        values = np.array([motor_after(initial, target, t, c) for t in np.arange(0, 1.001, 0.001)])
        self.assertLessEqual(
            float(np.max(np.abs(np.diff(values, axis=0))) / 0.001), c.actuator.rate_limit_N_s + 1e-9
        )
        self.assertTrue(np.all(values[:, 0] <= target[0]))
        self.assertTrue(np.all(values[:, 1] >= target[1]))

    def test_noisy_sensors_do_not_change_open_loop_truth(self) -> None:
        c = self.small("04_timing")
        sensor = replace(
            c,
            flags=replace(
                c.flags,
                sensor_noise=True,
                sensor_bias=True,
                sensor_delay=True,
                perfect_state_feedback=False,
            ),
        )
        tape = default_commands(c)
        a, b = run(c, tape), run(sensor, tape)
        np.testing.assert_allclose(a["history"], b["history"], atol=1e-8, rtol=0)
        self.assertGreater(b["metrics"]["gnss_position_rms_m"], 0)
        self.assertEqual(a["metrics"]["gnss_position_rms_m"], 0)

    def test_reproducible_random_streams(self) -> None:
        c = self.small("07_uncertainty")
        a, b = run(c), run(c)
        self.assertEqual(a, b)
        changed = run(replace(c, seed=793))
        self.assertNotEqual(a["measurements"]["gnss"], changed["measurements"]["gnss"])
        no_camera = run(replace(c, flags=replace(c.flags, camera_enabled=False)))
        a_error = (
            a["measurements"]["gnss"][1]["values"]["x_m"]
            - a["measurements"]["gnss"][1]["truth"]["x_m"]
        )
        b_error = (
            no_camera["measurements"]["gnss"][1]["values"]["x_m"]
            - no_camera["measurements"]["gnss"][1]["truth"]["x_m"]
        )
        self.assertAlmostEqual(a_error, b_error, places=12)

    def test_policy_only_sees_delivered_measurements(self) -> None:
        c = self.small("05_sensors")
        observations: list[Observation] = []

        def policy(observation: Observation) -> Command:
            observations.append(observation)
            self.assertIsNone(observation.perfect_state)
            for measurement in observation.measurements.values():
                self.assertLessEqual(measurement.available_time_s, observation.time_s + 1e-12)
                self.assertLessEqual(measurement.sample_time_s, measurement.available_time_s)
                self.assertNotIn("truth", measurement.values)
            return Command(1600, 1600)

        result = run(c, policy=policy)
        self.assertEqual(dict(observations[0].measurements), {})
        self.assertTrue(result["decision_audit"])
        self.assertTrue(any("gnss" in o.measurements for o in observations))
        with self.assertRaises(TypeError):
            cast(dict[str, Measurement], observations[-1].measurements)["injected"] = observations[
                -1
            ].measurements["gnss"]

    def test_sampling_and_delay_hold_exact_command_boundary(self) -> None:
        c = self.small("04_timing")
        tape = [CommandChange(0, Command(1500, 1500)), CommandChange(0.023, Command(1600, 1600))]
        result = run(c, tape)
        applied = next(v["time_s"] for v in result["actuation_events"] if v["target_port_N"] > 0)
        self.assertAlmostEqual(applied, 0.075, places=12)
        self.assertTrue(all(row[11] == 0 for row in result["history"] if 0.035 <= row[0] < 0.075))

    def test_dropout_occlusion_and_pending_delivery(self) -> None:
        c = self.small("05_sensors")
        c = replace(
            c,
            flags=replace(c.flags, sensor_dropout=True),
            sensors=replace(
                c.sensors, gnss_dropout_probability=1, occlusion_start_s=0, occlusion_end_s=1
            ),
        )
        result = run(c)
        self.assertTrue(all(not m["valid"] for m in result["measurements"]["gnss"]))
        self.assertTrue(all(m["values"]["x_m"] is None for m in result["measurements"]["gnss"]))
        self.assertTrue(all(not m["valid"] for m in result["measurements"]["camera"]))
        self.assertFalse(result["measurements"]["gnss"][-1]["delivered"])

    def test_out_of_view_camera_results_serialize(self) -> None:
        c = self.small("05_sensors")
        c = replace(c, sensors=replace(c.sensors, target_e_m=-15))
        result = run(c)
        self.assertTrue(all(not m["valid"] for m in result["measurements"]["camera"]))
        json.dumps(result, allow_nan=False)

    def test_watchdog_neutral_after_all_commands_lost(self) -> None:
        c = self.small("07_uncertainty")
        c = replace(
            c,
            flags=replace(c.flags, motor_lag=False, motor_rate_limit=False),
            actuator=replace(c.actuator, missed_command_probability=1),
        )
        result = run(c)
        self.assertEqual(result["watchdog_events_s"], [0.1])
        self.assertTrue(
            all(row[7] == 0 and row[8] == 0 for row in result["history"] if row[0] >= 0.1)
        )

    def test_integration_refinement_and_trim(self) -> None:
        c = replace(self.small("01_hull"), duration_s=1, scenario="pulse")
        result = run(c)
        self.assertAlmostEqual(result["history"][-1][1], 1, places=10)
        self.assertAlmostEqual(result["history"][-1][4], 1, places=10)
        tape = [CommandChange(0, Command(1600, 1700))]
        c = replace(
            c,
            flags=replace(
                c.flags, nonlinear_thrust=True, thrust_saturation=True, reverse_asymmetry=True
            ),
        )
        a, b = run(c, tape), run(replace(c, integration_step_s=0.0025), tape)
        np.testing.assert_allclose(a["history"], b["history"], atol=1e-7, rtol=0)


if __name__ == "__main__":
    unittest.main()
