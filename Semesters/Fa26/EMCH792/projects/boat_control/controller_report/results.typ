#import "../simulator_report/style.typ": *
#import "context.typ": *
= Comparison protocol
The controller designs now meet the same simulator boundary, so the experiment varies plant assumptions while retaining the gains and reference. Full-model wind sweeps measure disturbance rejection. The cumulative flag ladder shows what happens as model features are added, and ablations show what happens when a feature group is removed from the full plant.

- Every run lasts 40 s and uses a 5 ms maximum integration step, 20 ms logging, and a 20 ms controller tick.
  - The initial condition is $(E,N,psi,u,v,r) = (0,2,0.12,0.8,0,0)$ in SI units.
    - Seeds 792, 793, and 794 supply paired gust, measurement, dropout, missed-command, and jitter streams. The policies produce their own commands; commands are not forced to match across controllers.
- All gains, limits, estimator constants, and nominal motor-proxy parameters remain fixed.
  - The primary study uses installed M200 inverse-map compensation for every case.
    - In the linear-thrust ladder stages and ablation, the same physical inverse map feeds a tangent actuator approximation. That deliberate model mismatch is part of the comparison, not a retuning of the controller.
- The full plant is preset `07_uncertainty`.
  - Its 5 m/s crosswind points north. Gust standard deviation is 0.5 m/s; sway wave force is 1 N and yaw wave moment is 0.1 N m with a 4 s period.
    - At zero heading, steady lateral projected-area wind force is approximately 4.59 N at 5 m/s, 11.76 N at 8 m/s, and 18.38 N at 10 m/s. Actual apparent-wind forcing changes with vessel motion and heading.

== Cases and simulator flags
The following table records the changed fields. Every omitted field keeps its full-model value. The heavy-drag case adds parameter uncertainty and nonzero quadratic lateral/yaw damping rather than removing flags.
#data-table((1.35in, 1fr), [Case], [Difference from the full model],
  [`full_calm`], [Disable wind, gusts, apparent wind, wind yaw moment, and waves.],
  [`full_wind5`], [Full model at the nominal 5 m/s wind.],
  [`full_wind8`, `full_wind10`], [Change only mean wind speed to 8 or 10 m/s.],
  [`linear_hull`], [Disable nonlinear kinematics, coupling, and drag. Keep added inertia.],
  [`linear_thrust`], [Disable nonlinear thrust, deadband, and reverse asymmetry. Keep saturation and fixed inverse-map compensation.],
  [`ideal_motor`], [Disable motor lag, force slew limit, and gain mismatch.],
  [`ideal_timing`], [Disable command delay, jitter, missed commands, and watchdog. Retain 50 Hz decisions.],
  [`oracle_feedback`], [Enable perfect-state feedback. The motor proxy and gains stay fixed.],
  [`no_added_mass`], [Disable added inertia.],
  [`heavy_drag`], [Mass ×1.15, additional inertia scale ×1.1, all four drag scales ×1.2; add sway quadratic damping 10 N s²/m² and yaw quadratic damping 3 N m s².])

- The separate ladder begins with the original `00_linear` through `07_uncertainty` presets.
  - Command sampling is forced on in all eight stages because a feedback policy requires explicit decision ticks.
    - All later flags keep their original cumulative meaning. No controller is redesigned for a ladder stage.
- Ablation differences are conditional on the full model.
  - They isolate the selected group under the remaining enabled effects, rather than proving an additive contribution.
    - For example, removing motor lag also changes how sensor noise reaches the hull. Smaller error in one ablation does not establish a more accurate physical model.

== Metrics
The main score is cross-track root-mean-square (RMS) error computed from internal hull truth. Sensor errors affect feedback but do not define the ground-truth score. Speed error is measured against surge speed, which is the declared controller reference rather than ground speed along east.
$ "RMS"_y = sqrt(1/n sum_(k=1)^n (N_k-N_d)^2). $
$ "RMS"_u = sqrt(1/n sum_(k=1)^n (u_k-U)^2). $
$ "Effort" = 1/T integral_0^T (F_p^2 + F_s^2) dif t. $

- Whole-run RMS includes the initial 2 m recovery.
  - Final-ten-second RMS isolates sustained tracking after the transient.
    - The score uses all 20 ms truth samples; report plots retain every fifth sample for readability.
- Settling time is the first logged time after which $|e_y| <= 0.25$ m and $|delta u| <= 0.1$ m/s remain true through the end.
  - A run can have low RMS but no settling time if gusts cause a late threshold crossing.
    - Aggregated settling values use only settled runs. The settled count is shown explicitly.
- Allocation-limited fraction counts controller ticks whose raw candidate forces exceed the nominal signed bounds, including startup ticks whose final command is overridden to neutral.
  - Mean squared thrust uses actual simulated motor force.
    - It is an effort proxy, not electrical energy. Voltage, current, battery state, and propeller inflow are not simulated.

= Full-model results
The full-model tests show how the controllers behave when the boat retains its nonlinearities and the navigation feedback includes realistic delivery imperfections. The figures use seed 792; the tables include all three seeds so that one favorable gust sequence cannot determine the comparison.

#figure({
  import "figures/tracking.typ" as f
  f.cross
}, caption: [Cross-track recovery in the full model, seed 792.])

#data-table((0.9in, 1.15in, 0.85in, 0.85in, 0.85in, 0.9in), [Wind], [Controller], [Whole-run RMS (m)], [Tail RMS (m)], [Tail speed RMS (m/s)], [Effort (N²)],
  ..("full_calm", "full_wind5", "full_wind8", "full_wind10").map(c => methods.enumerate().map(pair => (
    [#(if c == "full_calm" { "Calm" } else { c.replace("full_wind", "")+" m/s" })],
    [#names.at(pair.first())],
    [#pretty(aggregate(c,pair.last(),"cross_rms_m").mean)],
    [#pretty(aggregate(c,pair.last(),"tail_cross_rms_m").mean)],
    [#pretty(aggregate(c,pair.last(),"tail_speed_rms_m_s").mean)],
    [#pretty(aggregate(c,pair.last(),"mean_squared_thrust_N2").mean, digits: 1)]
  )).flatten()).flatten())

At 5 m/s wind, the mean tail line errors are #pretty(aggregate("full_wind5","pid","tail_cross_rms_m").mean) m for PID, #pretty(aggregate("full_wind5","lqr","tail_cross_rms_m").mean) m for LQR, and #pretty(aggregate("full_wind5","pole_placement","tail_cross_rms_m").mean) m for pole placement. At 10 m/s wind, LQR reduces PID's tail error by #pretty(100*(1 - aggregate("full_wind10","lqr","tail_cross_rms_m").mean/aggregate("full_wind10","pid","tail_cross_rms_m").mean), digits: 1)% while increasing mean squared thrust by #pretty(100*(aggregate("full_wind10","lqr","mean_squared_thrust_N2").mean/aggregate("full_wind10","pid","mean_squared_thrust_N2").mean - 1), digits: 1)%.

The fixed PID has greater residual line error than either state-feedback design in this envelope. LQR and pole placement produce very similar tail errors, so their small numerical differences should be judged together with transient recovery and thrust effort.

#figure({
  import "figures/tracking.typ" as f
  f.motion
}, caption: [Speed regulation and crab heading, seed 792.])

- The vessel points into the crosswind while holding the east-going line.
  - This heading is expected because the thrusters cannot push directly sideways.
    - Integral action and the coupling-aware feedback create the required yaw bias. PID additionally applies explicit sideslip compensation in its guidance loop.
- The small speed transient includes sensor startup and actuator delay.
  - Subsequent speed errors reflect gusts, wave forcing, allocation, and the controller's surge gains.
    - The local linearization includes surge drag slope and motor lag but not nonlinear sway/yaw energy exchange away from trim.

#figure({
  import "figures/comparison.typ" as f
  f.wind
}, caption: [Mean tail line error across three paired seeds.])

The calm point disables waves and gusts along with wind. The 5, 8, and 10 m/s points retain gusts and waves, so the jump from calm to 5 m/s includes all environmental forcing. The 5-to-10 m/s comparison changes only mean wind speed.

#data-table((1.0in, 1.2in, 1.1in, 0.8in, 0.95in), [Wind], [Controller], [Tail RMS range (m)], [Settled runs], [Mean settling (s)],
  ..("full_wind5", "full_wind8", "full_wind10").map(c => methods.enumerate().map(pair => {
    let m = pair.last()
    let e = aggregate(c,m,"tail_cross_rms_m")
    let t = aggregate(c,m,"settling_s")
    ([#c.replace("full_wind", "") m/s], [#names.at(pair.first())],
     [#pretty(e.min)-#pretty(e.max)], [#t.n / #summary.seeds.len()], [#pretty(t.mean, digits: 1)])
  }).flatten()).flatten())

== Effort and actuator demand
The controller can improve line error by using more differential thrust. The effort and allocation records therefore accompany the tracking results. These records also identify whether an apparent response advantage depends on sustained clipping.

#figure({
  import "figures/tracking.typ" as f
  f.force
}, caption: [Actual M200 forces at 10 m/s wind, seed 792.])

#data-table((1.6in, 1fr, 1fr), [Controller at 10 m/s], [Mean allocation-limited ticks (%)], [Maximum actual force (N)],
  ..methods.enumerate().map(pair => (
    [#names.at(pair.first())],
    [#pretty(100*aggregate("full_wind10",pair.last(),"allocation_limited_fraction").mean, digits: 2)],
    [#pretty(aggregate("full_wind10",pair.last(),"peak_force_N").max, digits: 2)]
  )).flatten())

= Progressive realism and ablations
The preceding wind results establish performance on the full model. The flag comparisons now explain which simplifications affect that performance, while preserving the same controller gains and M200 compensation.

#figure({
  import "figures/comparison.typ" as f
  f.ladder
}, caption: [Whole-run line error as cumulative features are added.])

#data-table((0.45in, 1.2in, 1fr), [Index], [Preset], [New feature group],
  [0], [`00_linear`], [Local hull and tangent actuator; perfect hull state.],
  [1], [`01_hull`], [Nonlinear hull rotation, coupling, and surge drag.],
  [2], [`02_m200`], [Bounded signed M200 lookup, neutral deadband, reverse asymmetry.],
  [3], [`03_motor`], [Motor lag and force slew limit.],
  [4], [`04_timing`], [35 ms command delay.],
  [5], [`05_sensors`], [Noise, bias, delay, antenna offset, camera occlusion; remove perfect-state feedback.],
  [6], [`06_disturbances`], [Wind, gusts, apparent wind, wind moment, prescribed waves.],
  [7], [`07_uncertainty`], [Added inertia, motor mismatch, jitter, missed commands, watchdog, sensor dropout.])

The ladder does not imply that increasing fidelity must increase error. A controller can accidentally perform better on a more detailed plant because of changed damping, gain, or phase. The following full-model ablations make that dependence explicit.

#data-table((1.6in, 1fr, 1fr, 1fr), [Case], [PID tail RMS (m)], [LQR tail RMS (m)], [Pole-placement tail RMS (m)],
  ..("full_wind5", "linear_hull", "linear_thrust", "ideal_motor", "ideal_timing", "oracle_feedback", "no_added_mass", "heavy_drag").map(c => (
    [#raw(c)], ..methods.map(m => [#pretty(aggregate(c,m,"tail_cross_rms_m").mean)])
  )).flatten())

- Small hull and thrust-ablation differences indicate that this line-tracking maneuver stays fairly close to the design envelope.
  - The inverse M200 lookup already compensates the static propulsion map in the full plant.
    - A reversal, aggressive speed transition, tight turn, or large saturation event can expose much larger nonlinear differences and should be a subsequent maneuver test.
- The oracle feedback case shows the incremental effect of the shared estimator under the configured sensor errors.
  - A small oracle advantage means wind rejection or gain structure is dominating this particular score.
    - It does not establish that sensor bias, RTK degradation, or longer outages are harmless. Those faults need dedicated sweeps.
- Added inertia and drag change both disturbance acceleration and the response to feedback.
  - Their effect need not be monotonic. Higher damping can suppress a gust response while increasing required thrust.
    - The heavier-drag test therefore reports effort as well as tracking error in the saved metrics.

= Verification, reproduction, and next design decision
The simulation evidence supports a controller choice for this operating envelope. Mathematical checks support the local design, while causal and numerical checks support the implementation. Those checks have different purposes and should remain separate when the controller moves onto a physical boat.

- Mathematical verification checks both augmented controllability ranks, the Riccati residual, all local closed-loop eigenvalues, and agreement of the nonlinear hull Jacobian with the design matrices.
  - Controller tests also check heading wrapping, lever-arm and latency correction, invalid-packet retention, neutral output without navigation feedback, force limits, anti-windup, and calm recovery.
    - The complete project test suite contains 21 tests. Code formatting, linting, and static typing accompany those tests. Halving the maximum integration step from 5 ms to 2.5 ms in the full 5 m/s case changes the sampled hull states by less than $7 times 10^(-9)$ in SI units for all three controllers.
- Comparison evidence uses paired seeds and frozen tuning.
  - Mean, minimum, maximum, and individual-seed metrics are retained, rather than only a winning example.
    - Three seeds describe this small sweep; they do not establish a broad probability of mission success.
- LQR with integral action is the candidate to take forward.
  - It gives comparable rejection to pole placement while making the effort-versus-error tradeoff explicit through $Q$ and $R$.
    - Keep pole placement as a close benchmark and PID as the simpler fallback. This recommendation applies to the saved gains and moving-line task, not to every design in each controller family.

== Run and inspect
Run the saved comparison from the project directory. The CLI accepts existing simulator overrides, so controller studies use the same configuration flags as open-loop simulation.
```sh
uv sync
uv run python -m blueboat_sim.controller_study
uv run python -m blueboat_sim.controller_study \
  --case full_wind5 --case full_wind10 --seeds 792,793,794 \
  --set flags.sensor_dropout=false \
  --data build/no-dropout/data --output build/no-dropout
uv run python -m blueboat_sim.controller_study \
  --case full_wind5 --linear-pwm \
  --data build/tangent-pwm/data --output build/tangent-pwm
typst compile controller_report.typ controller_report.pdf
```

- `controller_report/data/design.json` stores matrices, weights, gains, poles, and nominal parameters.
  - `summary.json` stores every resolved case, seed, metric, aggregate, and source hash; `traces.json` stores the representative plotting samples.
    - Per-run truth CSV, policy estimates, requested force, integral states, resolved configuration, and decision-delivery audits are saved under `build/controllers/`.
- Keep optional experiments in a separate `--data` directory.
  - The report compiles from the retained main-study JSON files.
    - Changing the default data directory replaces the report's input data and therefore requires a fresh report review.

== Tests still needed before boat trials
The present controllers track a fixed east-going line at 1 m/s. They do not implement waypoint transitions, turning guidance, obstacle avoidance, station keeping, stereo-based navigation, or a full mission controller.

- Extend the reference tests to speed changes, reversals, curved paths, and large initial heading errors.
  - Test deliberate navigation outages, biased GNSS, longer command latency, and motor degradation.
    - Those cases should expose where fixed gains or the current minimal observer need replacement.
- Identify motor lag, installed thrust, mass/inertia, damping, and wind area from physical measurements.
  - Benchmark actual sensor and AGX Orin delivery timing.
    - The hardware controller should use measured uncertainty bounds and receive actuator acknowledgments where available.
