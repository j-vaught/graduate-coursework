"""An open-loop command ignores feedback and cannot correct a displaced path."""

from __future__ import annotations

import unittest
from dataclasses import replace

import numpy as np

from blueboat_sim.controller_study import cases
from blueboat_sim.engine import Observation, run
from blueboat_sim.open_loop_study import FixedTrim, metrics
from blueboat_sim.physics import trim


class OpenLoopTests(unittest.TestCase):
    def test_command_ignores_observation(self) -> None:
        p = FixedTrim(1590)
        a = p(Observation(0, {}, None))
        b = p(Observation(20, {}, (100, -100, 3, 0, 0, 2)))
        self.assertEqual(a, b)

    def test_nominal_trim_holds_aligned_line(self) -> None:
        c = cases(2)["full_calm"]
        c = replace(
            c,
            initial_state=(0, 0, 0, 1, 0, 0),
            flags=replace(c.flags, motor_mismatch=False, missed_commands=False),
        )
        result = run(c, policy=FixedTrim(trim(c)[1]))
        h = np.array(result["history"])
        np.testing.assert_allclose(h[:, 1], h[:, 0], atol=1e-10)
        np.testing.assert_allclose(h[:, 2:4], 0, atol=1e-10)
        np.testing.assert_allclose(h[:, 4], 1, atol=1e-10)
        self.assertLess(metrics(result["history"])["cross_rms_m"], 1e-10)

    def test_equal_trim_does_not_correct_initial_offset_or_heading(self) -> None:
        c = cases(2)["full_calm"]
        c = replace(c, flags=replace(c.flags, motor_mismatch=False, missed_commands=False))
        result = run(c, policy=FixedTrim(trim(c)[1]))
        h = np.array(result["history"])
        self.assertGreater(h[-1, 2], 2)
        self.assertAlmostEqual(h[-1, 3], 0.12, places=10)


if __name__ == "__main__":
    unittest.main()
