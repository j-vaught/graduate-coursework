# Configurable BlueBoat simulator

The simulator separates physical motion, motor response, command timing, and sensor delivery. Start with a local linear model and enable one feature group at a time. The platform remains the BlueBoat configuration in `platform.json`. The existing report experiments remain reproducible through their original entry points.

The component assumptions follow the report's M200 propulsion, AGX Orin computer, one ZED X stereo camera, VN-110 inertial sensor, and mosaic-H dual-antenna RTK receiver. The IMU supplies planar raw gyro and acceleration measurements. GNSS heading uses the dual antennas. The camera supplies a range and bearing observation of a configured target; computer behavior uses configurable timing rather than a processor emulator.

- Use cumulative comparisons to increase model detail.
  - Every preset receives the same absolute motor-percentage command tape and the same initial state.
  - Independent random streams keep wind, timing, and sensor trials paired across configurations.
    - Enabling a camera does not change the GNSS noise sequence. Sensor errors change observations, while open-loop commands continue to follow the same tape.
- Use isolated comparisons to identify the effect of a feature group.
  - Each group is enabled on the linear baseline, with required dependencies included.
  - Numerical parameters can be changed independently of their enable flags.
    - A zero dropout probability or zero wave amplitude intentionally produces no disturbance, even when its feature is enabled.
- Establish improvement against evidence.
  - The comparison figure shows model differences and sensor errors. Added complexity alone does not establish better prediction.
  - Recorded boat trajectories and timestamps will supply held-out validation data; controller tracking metrics are documented in the companion controller study.

## Motor command convention

- `Command(port_percent=25, starboard_percent=25)` requests +25% on each motor.
  - Commands span -100% full reverse, 0% neutral, and +100% full forward.
    - This is percent drive request, not measured thrust, motor speed, or electrical power. The nonlinear M200 map converts the request to force in newtons.
  - The device adapter uses `pwm_us = 1500 + 4 * percent` internally.
    - The enabled neutral deadband spans -6.25% through +6.25%. Reverse thrust remains weaker than forward thrust.
  - At the 1 m/s nominal trim, +22.475% requests 7 N per motor.
    - +50% requests 18.854 N and +100% requests 40.207 N before mismatch. -100% requests -20.068 N.
- Tapes use `time_s`, `port_percent`, and `starboard_percent`.
  - Percent commands are validated at construction. Nonfinite and out-of-range requests are rejected.
    - `command_amplitude_percent=20` adds 20 percentage points to trim, not 20% of the trim value.
  - Legacy pulse-width tapes remain readable with their explicit `_pwm_us` keys; Python callers use `Command.from_pwm(...)`.
    - New exports use percentage fields. Truth and command logs retain pulse widths for device audits and add percentage fields. Result schema version 2 preserves the original truth-column positions and appends `port_percent` and `starboard_percent`.

## Feature ladder

| Preset | Additional effects |
| --- | --- |
| `00_linear` | Local hull and actuator linearizations, ideal execution and measurements. |
| `01_hull` | Full planar kinematics, nonlinear motion coupling, quadratic drag. |
| `02_m200` | Signed M200 lookup, installed thrust limits, neutral deadband, reverse asymmetry. |
| `03_motor` | First-order force lag and force slew limits. |
| `04_timing` | Command sampling and compute/transport/actuation delay. |
| `05_sensors` | Noise, bias, delivery latency, antenna lever arm, stereo occlusion; perfect-state feedback disabled. |
| `06_disturbances` | Wind, repeatable correlated gusts, apparent wind, wind moment, prescribed planar wave forces. |
| `07_uncertainty` | Added mass, motor mismatch, jitter, missed commands, watchdog, and random sensor loss. |

The editable preset files are in `configs/simulator/`. Each file contains the complete resolved configuration rather than inheriting hidden settings from another preset. The definitions in `blueboat_sim/config.py` generate those templates.

## Flags and associated parameters

| Flag | Enabled behavior and adjustable parameters |
| --- | --- |
| `nonlinear_kinematics` | Rotate body velocities using actual heading. Otherwise use first-order kinematics at the operating heading and speed. |
| `nonlinear_coupling` | Retain velocity products. Otherwise retain their local linearization, including the forward-speed/yaw coupling. |
| `nonlinear_drag` | Use signed quadratic surge drag and configurable quadratic sway/yaw damping. Otherwise use their local tangent at the operating speed. |
| `added_mass` | Add separate surge, sway, and yaw inertia fractions and consistent Coriolis terms. |
| `nonlinear_thrust` | Use the signed installed-scaled M200 curve. Otherwise use its local tangent at the operating motor percentage. |
| `thrust_saturation` | Clip force to the selected signed limits. Input commands always remain within -100% to +100%. Required by the bounded M200 lookup. |
| `neutral_deadband` | Apply zero demand from -6.25% through +6.25%. |
| `reverse_asymmetry` | Use the weaker reverse branch. Disabling it creates a symmetric ideal comparison. |
| `motor_lag` | Apply `actuator.lag_s` to held force demands. |
| `motor_rate_limit` | Limit force change using `actuator.rate_limit_N_s`. The ramp-plus-lag response is integrated analytically. |
| `motor_mismatch` | Apply separate port/starboard gains, then preserve enabled force limits. |
| `command_sampling` | Read commands or call a policy on `actuator.command_period_s` ticks. |
| `command_delay` | Queue commands through compute, transport, and actuator dead time. |
| `timing_jitter` | Add a bounded nonnegative delivery delay; requires sampling and delay. |
| `missed_commands` | Randomly lose command updates using the specified probability; requires sampling. |
| `command_watchdog` | Request 0% motor command and zero demand after no command has been applied for the configured timeout. Motor lag still governs force decay. |
| `wind` | Apply projected-area aerodynamic loading from wind speed and world-frame direction. |
| `gusts` | Add a seeded correlated wind-velocity process with selectable amplitude and correlation time. |
| `apparent_wind` | Subtract boat translation from world wind before calculating aerodynamic load. |
| `wind_yaw_moment` | Apply the wind force at the configured offset from the hull reference. |
| `wave_forcing` | Add selectable sinusoidal planar force/moment amplitudes and period. This is prescribed disturbance forcing, not a wave hydrodynamics model. |
| `sensor_noise` | Add independently seeded GNSS, IMU, pixel-center, and disparity noise. |
| `sensor_bias` | Add selectable GNSS position offsets and gyro bias. |
| `sensor_delay` | Deliver measurements after their configured sensor latency. |
| `sensor_dropout` | Suppress randomly selected measurements separately for each sensor. |
| `antenna_lever_arm` | Account for the GNSS antenna's offset and rotational velocity. |
| `camera_occlusion` | Withhold stereo observations during the selected interval. |
| `gnss_enabled`, `imu_enabled`, `camera_enabled` | Enable or disable each sensor's acquisitions and delivery. |
| `perfect_state_feedback` | Explicitly expose simulator state to the policy for ideal tests. When disabled, the policy receives delivered measurements only. |

Unknown fields, non-boolean flags, invalid timing/probabilities, and inconsistent flag dependencies are rejected. For example, enabling gusts with wind disabled raises an error. The simulator does not silently accept a feature that has no implementation.

## Run and compare

List or regenerate the templates.

```sh
uv run python -m blueboat_sim presets
uv run python -m blueboat_sim presets --output configs/simulator
```

Run a preset, then change selected flags and parameters without editing code.

```sh
uv run python -m blueboat_sim run --preset 05_sensors --output build/my-run
uv run python -m blueboat_sim run --config configs/simulator/05_sensors.json \
  --set sensors.gnss_position_sigma_m=0.10 \
  --set flags.sensor_dropout=true \
  --set sensors.gnss_dropout_probability=0.05 \
  --set seed=100 --output build/noisy-run
```

Run the cumulative ladder, isolate groups, or perform paired trials across several seeds.

```sh
uv run python -m blueboat_sim compare --output build/ladder
uv run python -m blueboat_sim compare --mode isolated --output build/isolated
uv run python -m blueboat_sim compare --seeds 792,793,794 --output build/paired-trials
```

Compare custom configurations by repeating `--config`. Duration, scenario, operating point, command amplitude, and initial state must match. A comparison always freezes one common absolute motor-percentage tape. Custom command files use a list of `time_s`, `port_percent`, and `starboard_percent` objects; times begin at zero and increase strictly. A reversing example is in `configs/simulator/commands/reversal.json`.

```sh
uv run python -m blueboat_sim run --preset 03_motor \
  --commands configs/simulator/commands/reversal.json \
  --set duration_s=8 --output build/reversal
```

Run outputs include `resolved_config.json`, `input_tape.json`, `result.json`, `truth.csv`, and `metrics.json`. The result records physical parameters, source provenance, sensor acquisition/availability times, pending deliveries, actual force, queued commands, watchdog events, and decision audits. The comparison exports `summary.json` and `comparison.json`. Reusing an output directory updates files for the same name and seed; choose a new directory to retain earlier trials.

## Controller boundary

`run(experiment, commands=...)` replays an open-loop program. `run(experiment, policy=...)` accepts a callback on configured command ticks. Its input is an immutable `Observation`; its output is a `Command` containing signed port/starboard percentages or `None` to hold the current command. PID, LQR, and pole-placement implementations use this interface; see `controller_report/README.md`.

- A policy sees only delivered measurements.
  - Each measurement includes acquisition time, availability time, validity, and measured values.
  - Invalid measurements contain missing values, and future deliveries remain unavailable.
    - The simulator stores acquisition-time truth separately for scoring. That truth is not in the policy's measurement objects.
- Full-state feedback is an explicit idealization.
  - `perfect_state_feedback=true` adds a separate state tuple for ideal state-feedback experiments.
  - Disabling it requires an estimator to construct states from delivered GNSS/IMU observations.
- Force allocation remains a controller integration task.
  - The current boundary accepts motor percentages. A controller can command surge force/yaw moment through a tested allocator and force-to-percentage adapter.
  - The stock ArduRover control loops and software are not simulated by this motor-command boundary.

## Physical scope and verification

The nonlinear rigid-body mode reproduces the report's equations. The added-mass extension uses diagonal planar inertia and consistent coupling from the [marine-craft formulation](https://www.fossen.biz/html/marineCraftModel.html). The linear mode uses the first-order tangent at the chosen operating point, including its nominal drag and command offsets. Initial motor force is the steady trim force; specify an appropriate initial velocity or a zero-speed operating point for launch tests.

The simulator retains the report's provisional loaded mass, drag, inertia, spacing, and installed thrust scaling. Added-mass fractions, slew limits, mismatch, gusts, wave amplitudes, dropouts, and latency distributions are engineering test assumptions. Battery discharge, voltage-dependent thrust, propeller inflow, water-current dynamics, roll/pitch/heave, camera images, learned perception, and GNSS float/single-point transitions need dedicated extensions.

Metrics include final position/heading, peak force, integrated squared force, delivered GNSS error, valid camera observations, missed commands, and watchdog trips. Integrated squared force is a control-effort proxy, not electrical energy. The companion controller study reports tracking and recovery against a straight-line reference.

```sh
uv run python -m unittest discover -s tests -v
uv run ruff check .
uv run ty check .
```

The acceptance tests cover report-model equivalence, local linearization, added-mass energy balance, analytic motor transients and slew limits, physical bounds, causal policy observations, delayed command boundaries, watchdog neutralization, reproducible independent random streams, sensor isolation, dropout/occlusion, and integration refinement.

The saved demonstration data, input tape, and resolved run metadata are in `data/configurable_simulator/`. They use seed 792 and a 20 percentage-point excitation to exercise the M200 curve beyond one local segment. Reproduce the demonstration with `uv run python -m blueboat_sim compare --set command_amplitude_percent=20 --output build/configurable-simulator`. The default 2.5 percentage-point excitation is a local small-signal experiment.

The comparison figure is authored in Typst/Lilaq and rebuilds with

```sh
typst compile simulator_comparison.typ figures/simulator-comparison.pdf
```
