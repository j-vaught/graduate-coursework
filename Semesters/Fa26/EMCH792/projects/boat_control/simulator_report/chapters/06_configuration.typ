#import "../style.typ": *
= Configuration and reproducible operation <cfg-chapter>

The preceding chapters define the implemented physics and observations. Configuration selects which of those mechanisms participates in a run and supplies its numerical parameters. Flags choose a mechanism; parameters determine its strength, timing, and geometry.

== Configuration hierarchy

- `Experiment` supplies the run name, duration, seed, operating point, initial state, and command scenario.
  - The default run lasts 12 s, starts at 1 m/s, and uses a 5 ms maximum integration step with 20 ms logging.
    - Sensor and command events split integration intervals at their actual times. The maximum step does not quantize a 35 ms command delay into an approximate event.
- Five nested groups describe the model.
  - `flags` contains 31 Boolean switches. `hull`, `actuator`, `environment`, and `sensors` contain numerical settings.
    - Disabled effects retain their parameter values so a paired experiment can enable them without silently changing another assumption.
- Full JSON templates define every preset.
  - `00_linear` through `07_uncertainty` contain resolved settings rather than hidden inheritance.
    - The configuration saved with a result is the final version after command-line overrides. Use that record to reproduce a run.

#note[
A true flag can produce no numerical effect when its magnitude is zero. For example, enabled sensor dropout with probability zero retains all samples. Always inspect the resolved flag and its associated magnitude together.
]

== Preset ladder

The presets collect related effects into a cumulative ladder. Each row adds the named mechanisms to the preceding configuration. Custom JSON files can select other valid combinations, and isolated comparison mode adds one group to the linear baseline with its required dependencies.

#data-table((1.35in, 1fr),
  [Preset], [Additional effects],
  [`00_linear`], [Local hull and actuator linearizations; ideal command execution and enabled sensors. Perfect-state access is available.],
  [`01_hull`], [Actual heading rotation, nonlinear velocity coupling, and quadratic hull drag.],
  [`02_m200`], [Signed installed M200 lookup, saturation, neutral deadband, and reverse asymmetry.],
  [`03_motor`], [Motor force lag and force slew limits.],
  [`04_timing`], [Command sampling and compute, transport, and actuation delay.],
  [`05_sensors`], [Measurement noise, bias, latency, GNSS lever arm, and camera occlusion. Perfect-state access is disabled.],
  [`06_disturbances`], [Wind, correlated gusts, apparent wind, wind moment, and prescribed planar wave forcing.],
  [`07_uncertainty`], [Added inertia, motor mismatch, timing jitter, missed commands, watchdog, and random sensor loss.],
)

- A cumulative comparison reveals the response of an increasingly detailed model.
  - Its last row contains every preceding effect, so the final trajectory difference is not a single-feature result.
    - An isolated comparison is the appropriate first check when asking which mechanism caused a change.
- Independent flags enable more focused studies than the preset ladder.
  - For example, retain the nonlinear M200 lookup while disabling only motor lag, or increase GNSS noise while retaining fixed latency.
    - The numerical values and command tape must remain matched to interpret the resulting difference.

== Complete Boolean flag reference

The tables below specify the enabled behavior. Baseline means `00_linear`; only the three sensor-enable flags and perfect-state feedback are true in that baseline.

#text(size: 9pt)[
#data-table((1.95in, 1fr),
  [Hull switch], [Enabled behavior],
  [`nonlinear_kinematics`], [Use the actual heading rotation instead of its local first-order approximation.],
  [`nonlinear_coupling`], [Retain velocity-product coupling instead of its tangent at the operating speed.],
  [`nonlinear_drag`], [Retain quadratic surge drag and any configured quadratic sway/yaw damping.],
  [`added_mass`], [Add separately scaled surge, sway, and yaw inertia and their consistent coupling.],
)
]

#text(size: 9pt)[
#data-table((1.95in, 1fr),
  [Propulsion switch], [Enabled behavior],
  [`nonlinear_thrust`], [Use the bounded, signed installed-scaled M200 lookup. Requires saturation.],
  [`thrust_saturation`], [Clip PWM to 1100-1900 µs and force to the selected forward/reverse bounds.],
  [`neutral_deadband`], [Set requested force to zero for PWM from 1475 through 1525 µs.],
  [`reverse_asymmetry`], [Use the weaker reverse branch. With a linear actuator, scale negative force by the reverse/forward limit ratio.],
  [`motor_lag`], [Apply first-order force response using the configured time constant.],
  [`motor_rate_limit`], [Limit force change per second; combine with lag when both are enabled.],
  [`motor_mismatch`], [Apply separate motor gains and retain force limits when saturation is enabled.],
)
]

#text(size: 9pt)[
#data-table((1.95in, 1fr),
  [Timing switch], [Enabled behavior],
  [`command_sampling`], [Read the input program or call a policy on periodic command ticks.],
  [`command_delay`], [Queue computation, transport, and actuation dead time before applying the command.],
  [`timing_jitter`], [Add bounded nonnegative delay. Requires command sampling and delay.],
  [`missed_commands`], [Drop individual command updates with the selected probability. Requires sampling.],
  [`command_watchdog`], [Request neutral after no command has been applied for the timeout. Requires sampling.],
)
]

#text(size: 9pt)[
#data-table((1.95in, 1fr),
  [Environmental switch], [Enabled behavior],
  [`wind`], [Apply projected-area aerodynamic force from the configured world-frame wind.],
  [`gusts`], [Add a seeded correlated wind-velocity process. Requires wind.],
  [`apparent_wind`], [Subtract boat translational velocity before evaluating aerodynamic loading. Requires wind.],
  [`wind_yaw_moment`], [Apply wind force at an offset to obtain yaw moment. Requires wind.],
  [`wave_forcing`], [Add prescribed sinusoidal planar force/moment. Independent of wind.],
)
]

#text(size: 9pt)[
#data-table((1.95in, 1fr),
  [Sensor / observation switch], [Enabled behavior],
  [`sensor_noise`], [Add separate GNSS, inertial, pixel-center, and disparity noise streams.],
  [`sensor_bias`], [Add configured GNSS position offsets and gyro bias.],
  [`sensor_delay`], [Queue measurements until their sensor availability times.],
  [`sensor_dropout`], [Invalidate randomly selected samples using separate probabilities per sensor.],
  [`antenna_lever_arm`], [Include the GNSS antenna offset in its position and velocity.],
  [`camera_occlusion`], [Invalidate target observations during the configured time interval.],
  [`gnss_enabled`], [Schedule GNSS acquisition and delivery. True in the baseline.],
  [`imu_enabled`], [Schedule inertial acquisition and delivery. True in the baseline.],
  [`camera_enabled`], [Schedule camera acquisition and delivery. True in the baseline.],
  [`perfect_state_feedback`], [Expose a separate exact state tuple to a policy. True in the baseline; false from the sensor preset onward.],
)
]

== Useful numerical controls

With the enable switches defined, numerical overrides allow sensitivity studies without editing the implementation. The values below are default test settings; they are not a component acceptance specification.

#data-table((1.55in, 1fr, 1.0in),
  [Group], [Principal controls], [Default],
  [Run], [Duration / integration step / log interval.], [12 s / 5 ms / 20 ms.],
  [Operating point], [Forward speed / heading.], [1 m/s / 0 rad.],
  [Hull], [Mass, inertia, and each drag scale.], [1.0 each.],
  [Added inertia], [Surge / sway / yaw fractions.], [0.10 / 0.50 / 0.20.],
  [Geometry], [Motor separation / GNSS forward offset.], [0.75 m / -0.50 m.],
  [Motor], [Force time constant / force slew limit.], [0.20 s / 80 N/s.],
  [Command], [Period / compute / transport / dead time.], [20 / 5 / 10 / 20 ms.],
  [Command failure], [Maximum jitter / watchdog timeout.], [3 ms / 100 ms.],
  [Wind], [Speed / direction / gust standard deviation.], [5 m/s / 90° / 0.5 m/s.],
  [Gust], [Correlation time / process sample period.], [1 s / 0.1 s.],
  [Wave forcing], [Surge / sway / yaw amplitude, period.], [0 N / 1 N / 0.1 N m, 4 s.],
)

- Hull controls include separate linear and quadratic surge scales, linear sway and yaw scales, optional quadratic sway/yaw damping, and added-inertia fractions.
  - Changing an inertia fraction does not change hull mass or nominal drag.
    - Changing mass scale also changes the geometric yaw-inertia proxy. Change inertia scale independently to study mass-distribution error.
- Actuator controls include individual motor gains, all timing intervals, and missed-command probability.
  - The uncertainty preset uses gains 0.95 and 1.05 and missed-command probability 0.02.
    - Other presets retain gains and probabilities but leave their corresponding effects disabled.
- Sensor controls include periods, latency, each noise magnitude, bias, dropout probability, geometry, and occlusion interval.
  - The uncertainty preset uses GNSS dropout probability 0.05 and camera dropout probability 0.10. Inertial dropout remains zero.
    - A camera target is a fixed world point with configurable east/north position. It is not a generated competition scene.

== Reproduce a run and change one assumption

Run the commands from `EMCH792/projects/boat_control`. The first example repeats the report demonstration; the second makes a controlled sensor change.

```sh
uv sync
uv run python -m blueboat_sim compare \
  --set command_amplitude_us=80 \
  --output build/configurable-simulator

uv run python -m blueboat_sim run --preset 05_sensors \
  --set sensors.gnss_position_sigma_m=0.10 \
  --set flags.sensor_dropout=true \
  --set sensors.gnss_dropout_probability=0.05 \
  --set seed=100 --output build/noisy-run
```

- Use `--set group.field=value` for a numerical or Boolean override.
  - Boolean values use JSON `true` or `false`; a textual string is rejected as a flag.
    - Unknown keys, invalid probabilities, nonfinite values, reversed occlusion intervals, and inconsistent flag dependencies are rejected before integration.
- Use a custom JSON file when several related settings change together.
  - `--config configs/simulator/05_sensors.json` supplies a complete template.
    - Repeated `--config` arguments compare custom templates in their supplied order. Duration, scenario, operating point, command amplitude, and initial state must match.
- Use a command tape when the input must be exactly specified.
  - `configs/simulator/commands/reversal.json` requests neutral, full forward, full reverse, and neutral at 0, 2, 4, and 6 s.
    - Commands start at zero, use finite port/starboard PWM, and have strictly increasing times within the run.

== Outputs, auditing, and numerical limits

The command tape defines the requested excitation. Logs then expose the sequence between that request and the observed motion, so a run can be inspected rather than judged only by its final plot.

#data-table((1.55in, 1fr),
  [Saved file], [Use],
  [`resolved_config.json`], [Reproduce all final settings after overrides.],
  [`input_tape.json`], [Inspect the common requested PWM changes.],
  [`truth.csv`], [Plot time, six hull states, two actual motor forces, applied PWM, and target force.],
  [`metrics.json`], [Compare scalar summaries under the declared experiment.],
  [`result.json`], [Audit physical parameters, source hash, trim, raw sensor records, command application, watchdog trips, and policy decision timestamps.],
  [`comparison.json`], [Store matched histories and GNSS records for downstream plots; each record marks whether it was delivered.],
  [`summary.json`], [Locate run directories and their metrics.],
)

- Each output directory is named from the run name and seed.
  - Reusing the same directory replaces that run's files.
    - Use a new output root to retain an earlier experiment. Seeds support repeatability within the numerical environment; archive software versions for long-term reproduction.
- Hull states use fourth-order Runge-Kutta integration between exact event boundaries.
  - Motor force uses the analytic held-target lag/ramp solution at each stage.
    - Event times and integration step serve different purposes. Reduce the maximum step for numerical convergence while retaining the physical sensor and command periods.
- The validator caps a run at two million nominal integration steps and two million estimated scheduled events.
  - Nonfinite integrated states raise an error.
    - A successful run is still inspected for bounds, equilibrium behavior, and step-size convergence. Completion alone does not establish accuracy.
