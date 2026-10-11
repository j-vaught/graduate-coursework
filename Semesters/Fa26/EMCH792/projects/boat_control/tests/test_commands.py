"""Signed motor percentage preserves the actuator curve and causal plant response."""

from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

from blueboat_sim.__main__ import command_file
from blueboat_sim.commands import percent_to_pwm, pwm_to_percent
from blueboat_sim.config import from_dict, presets
from blueboat_sim.engine import Command, CommandChange, run
from blueboat_sim.physics import mapped_force


class PercentageCommandTests(unittest.TestCase):
    def test_endpoints_neutral_and_invalid_requests(self) -> None:
        for percent, pulse in ((-100, 1100), (0, 1500), (25, 1600), (100, 1900)):
            self.assertEqual(percent_to_pwm(percent), pulse)
            self.assertEqual(pwm_to_percent(pulse), percent)
        for value in (-101, 101, float("nan"), float("inf"), True):
            with self.assertRaises(ValueError):
                Command(value, 0)
        self.assertEqual(Command.from_pwm(1600, 1700), Command(25, 50))

    def test_deadband_nonlinearity_and_reverse_asymmetry(self) -> None:
        c = presets()["02_m200"]
        for percent in (-6.25, 0, 6.25):
            self.assertEqual(mapped_force(percent_to_pwm(percent), c), 0)
        self.assertGreater(mapped_force(percent_to_pwm(6.3), c), 0)
        maximum = mapped_force(percent_to_pwm(100), c)
        half_request = mapped_force(percent_to_pwm(50), c)
        self.assertGreater(abs(half_request - maximum / 2), 1)
        reverse = abs(mapped_force(percent_to_pwm(-100), c))
        self.assertLess(reverse, maximum * 0.6)

    def test_legacy_and_percentage_tapes_match_full_model(self) -> None:
        c = replace(presets()["07_uncertainty"], duration_s=1)
        old = [
            CommandChange(0, Command.from_pwm(1700, 1600)),
            CommandChange(0.4, Command.from_pwm(1300, 1500)),
        ]
        new = [CommandChange(0, Command(50, 25)), CommandChange(0.4, Command(-50, 0))]
        a, b = run(c, commands=old), run(c, commands=new)
        np.testing.assert_array_equal(a["history"], b["history"])
        self.assertEqual(a["commands"], b["commands"])
        self.assertEqual(a["input_tape"][0]["port_percent"], 50)
        self.assertEqual(a["columns"][-2:], ["port_percent", "starboard_percent"])
        h = np.asarray(a["history"])
        np.testing.assert_allclose(h[:, 13:15], (h[:, 9:11] - 1500) / 4)

    def test_tape_units_are_explicit_and_round_trip(self) -> None:
        for fields in (
            {"port_percent": 25, "starboard_percent": -50},
            {"port_pwm_us": 1600, "starboard_pwm_us": 1300},
        ):
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "commands.json"
                path.write_text(json.dumps([{"time_s": 0, **fields}]))
                tape = command_file(path)
                assert tape is not None
                self.assertEqual(tape[0].command, Command(25, -50))
        self.assertEqual(from_dict({"command_amplitude_us": 80}).command_amplitude_percent, 20)
        with self.assertRaises(ValueError):
            from_dict({"command_amplitude_us": 80, "command_amplitude_percent": 20})


if __name__ == "__main__":
    unittest.main()
