"""Design mathematics, causal feedback, bounds, and closed-loop recovery."""

from __future__ import annotations

import math
import unittest
from dataclasses import replace
from types import MappingProxyType

import numpy as np

from blueboat_sim.config import presets
from blueboat_sim.controllers import Controller, SensorEstimate, Settings, design
from blueboat_sim.engine import Measurement, Observation, run
from blueboat_sim.physics import Physics, trim


class ControllerTests(unittest.TestCase):
    def test_design_controllability_riccati_and_requested_poles(self) -> None:
        for system in design()["systems"].values():
            a, b = np.array(system["A"]), np.array(system["B"])
            self.assertEqual(system["controllability_rank"], len(a))
            self.assertLess(system["riccati_residual"], 1e-7)
            for method, gain in system["gains"].items():
                eigen = np.linalg.eigvals(a - b @ np.array([gain]))
                self.assertTrue(np.all(eigen.real < 0))
                if method == "pole_placement":
                    np.testing.assert_allclose(
                        np.sort(eigen.real), np.sort(system["requested_poles"]), atol=1e-7
                    )

    def test_full_hull_jacobian_matches_design(self) -> None:
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
        force, _, _ = trim(c)
        physics = Physics(c)
        state = np.array([0, 0, 0, 1, 0, 0, force, force])
        jacobian = np.empty((6, 6))
        for i in range(6):
            plus, minus = state.copy(), state.copy()
            plus[i] += 1e-6
            minus[i] -= 1e-6
            jacobian[:, i] = (
                physics.rhs(0, plus, plus[6:]) - physics.rhs(0, minus, minus[6:])
            ) / 2e-6
        d = design()["systems"]
        indices = [1, 2, 4, 5]
        np.testing.assert_allclose(
            jacobian[np.ix_(indices, indices)], np.array(d["lateral"]["A"])[:4, :4], atol=1e-8
        )
        self.assertAlmostEqual(jacobian[3, 3], d["surge"]["A"][0][0], places=7)

    def test_lever_arm_delay_and_invalid_packets(self) -> None:
        estimator = SensorEstimate(-0.5, Settings())
        # A 1 m/s east-going boat; antenna sits half a metre behind the origin.
        values = {
            "x_m": 9.5,
            "y_m": 2.0,
            "heading_rad": 0.0,
            "velocity_e_m_s": 1.0,
            "velocity_n_m_s": 0.0,
        }
        gnss = Measurement("gnss", 1, 1.08, MappingProxyType(values), True)
        imu = Measurement("imu", 1.075, 1.08, MappingProxyType({"yaw_rate_rad_s": 0.0}), True)
        z, ready = estimator.update(Observation(1.08, {"gnss": gnss, "imu": imu}, None))
        self.assertTrue(ready)
        np.testing.assert_allclose(z, [10.08, 2, 0, 1, 0, 0], atol=1e-12)
        invalid = Measurement("gnss", 1.1, 1.18, MappingProxyType({}), False)
        z, ready = estimator.update(Observation(1.18, {"gnss": invalid, "imu": imu}, None))
        self.assertFalse(ready)  # The IMU is stale; invalid GNSS cannot replace a valid fix.
        self.assertAlmostEqual(z[0], 10.18)
        self.assertIs(estimator.gnss, gnss)

    def test_no_sensor_feedback_commands_neutral(self) -> None:
        c = presets()["07_uncertainty"]
        c = replace(c, duration_s=0.2, flags=replace(c.flags, gnss_enabled=False))
        for method in ("pid", "lqr", "pole_placement"):
            policy = Controller(method)
            result = run(c, policy=policy)
            self.assertTrue(
                all(
                    row["port_pwm_us"] == 1500 and row["starboard_pwm_us"] == 1500
                    for row in result["commands"]
                )
            )
            self.assertTrue(all(not row["ready"] for row in policy.logs))

    def test_saturation_antiwindup(self) -> None:
        for method in ("pid", "lqr", "pole_placement"):
            policy = Controller(method)
            for t in np.arange(0, 1, 0.02):
                cmd = policy(Observation(float(t), {}, (0, 100, 1, 0, 0, 0)))
                self.assertGreaterEqual(min(cmd.port_pwm_us, cmd.starboard_pwm_us), 1100)
                self.assertLessEqual(max(cmd.port_pwm_us, cmd.starboard_pwm_us), 1900)
            self.assertTrue(all(row["limited"] for row in policy.logs))
            np.testing.assert_allclose(policy.integrals, 0)

    def test_calm_full_model_recovers_from_small_offset(self) -> None:
        c = presets()["07_uncertainty"]
        c = replace(
            c,
            duration_s=30,
            initial_state=(0, 0.5, 0.05, 0.9, 0, 0),
            flags=replace(
                c.flags,
                wind=False,
                gusts=False,
                apparent_wind=False,
                wind_yaw_moment=False,
                wave_forcing=False,
                perfect_state_feedback=True,
                missed_commands=False,
            ),
        )
        for method in ("pid", "lqr", "pole_placement"):
            policy = Controller(method)
            h = np.array(run(c, policy=policy)["history"])
            tail = h[:, 0] >= 25
            self.assertLess(float(np.max(np.abs(h[tail, 2]))), 0.15, method)
            self.assertLess(float(np.max(np.abs(h[tail, 4] - 1))), 0.1, method)
            self.assertTrue(np.isfinite(h).all())

    def test_heading_wrap(self) -> None:
        from blueboat_sim.controllers import wrap

        self.assertAlmostEqual(wrap(2 * math.pi + 0.1), 0.1)


if __name__ == "__main__":
    unittest.main()
