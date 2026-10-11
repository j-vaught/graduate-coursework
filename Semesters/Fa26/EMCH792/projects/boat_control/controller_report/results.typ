#import "../simulator_report/style.typ": *
#import "context.typ": *
#import "figures/visual_story.typ" as visual
#let open = json("data/open_loop.json")
#let om(case, metric) = open.aggregate.find(r=>r.case==case).metrics.at(metric).mean

#pagebreak()
= First watch the boat without feedback
The simplest starting point is a constant motor command. Choose the nominal thrust that balances forward drag at 1 m/s, apply it to both motors, and leave it unchanged. The boat then responds to its initial heading, hydrodynamics, motor differences, and wind; no sensor reading changes the command.

- Each motor uses a signed command from -100% through +100%.
  - 0% is neutral, +100% is full forward, and -100% is full reverse.
    - Percentage describes the drive request. Actual thrust follows the M200 curve; 50% command gives 18.85 N, compared with 40.21 N at 100%.
- The open-loop command is approximately +#pretty(open.runs.first().percent_each, digits: 1)% motor command to each motor.
  - The nominal installed M200 map converts this to 7 N per motor, or 14 N total.
    - This balances the model's nominal forward drag at 1 m/s. It does not request a north position, a heading correction, or a turn toward the line.
- The computer retransmits that fixed command at 50 Hz.
  - Sensors still operate and command delay, motor response, and other enabled simulator effects still apply.
    - The open-loop policy ignores every observation. It is a deliberate fixed-trim baseline; an open-loop program could also contain predetermined turns.

== Why a perfect start can be misleading
Begin with calm water, matched motors, and no lost commands. This illustration retains the nonlinear hull and M200 models. Change only the initial state to see why a boat that looks correct in one open-loop run may fail the actual recovery task.

#figure(visual.nominal, caption: [The same fixed command succeeds from an aligned start and misses the displaced-start objective.])

- Aligned start. The boat begins on the line, points east, and already travels at 1 m/s.
  - It reaches approximately 40 m east while staying on the line over 40 s.
    - No correction is needed, so this case does not demonstrate that the command can correct an error.
- Displaced start. The boat begins 2 m north, points 6.9° north of east, and travels initially at 0.8 m/s.
  - Forward speed rises toward 1 m/s, but the heading stays wrong and north position reaches #pretty(om("nominal_offset","final_n_m"), digits: 2) m.
    - The boat has regulated its speed through passive drag balance while failing the route objective. Equal fixed thrust supplies no instruction to return to the line.

#note[Speed and route following are different goals. A boat can move at the desired speed while traveling along the wrong path.]

#pagebreak()
= Now add the full boat model and feedback
The preceding illustration isolated the initial-condition problem. Return next to the complete model, including 5% port/starboard motor mismatch, added inertia, timing errors, measurement imperfections, and environmental forcing. The following comparison keeps the same initial condition and wind seed for open loop and all three feedback controllers.

#figure(visual.full_paths, caption: [Actual paths in 5 m/s northward wind, seed 792. East and north use the same metre scale.])

- Read the map as a top-down view.
  - East is right and north is up. The dashed horizontal line is the desired route; every boat begins at $(0,2)$ m.
    - The fixed-command boat finishes far south of the line. The feedback boats turn toward the line and then continue close to it. Their paths overlap because their errors are small on this map scale.
- All feedback controllers receive the same type of delivered GNSS and IMU data.
  - PID uses speed, heading, and cross-track loops. LQR and pole placement use estimated state and integral feedback.
    - Each changes port and starboard commands when the estimated boat state differs from the objective. The detailed gains and equations follow in the appendix.
- Equal motor percentages does not ensure equal actual thrust in the full model.
  - The model multiplies nominal port thrust by 0.95 and starboard thrust by 1.05.
    - In calm water this bias bends the fixed-command path north. At 40 s, its north position is #pretty(om("full_calm","final_n_m"), digits: 2) m on average across the three seeds.

== Why a northward wind can produce a southward path
The wind acts on sway and yaw as well as on forward motion. In this model, positive sway also changes yaw through the added-inertia coupling term $(m_x-m_y)u v$. Because $m_y > m_x$, positive sway contributes a clockwise yaw moment. That contribution competes with the direct wind yaw moment and motor bias.

- The resulting open-loop bow turns south of east in the saved wind runs.
  - Its forward velocity then has a southward world component, which can outweigh its northward body-frame sway velocity.
    - This is why the boat's final displacement is not obtained by simply adding a northward drift to a straight east-going track.
- The controllers correct the resulting route error rather than assuming which way the wind will move the boat.
  - These curves are predictions of the configured model, including its assumed added inertia and wind coefficients.
    - Wind direction alone is insufficient to predict the boat's path without considering heading and coupled dynamics.

#pagebreak()
= Check the two parts of the objective separately
The map shows where the boat goes. The plots below show when the objective is met. Positive line error means north of the route; negative error means south. Speed error is measured along the boat's own forward axis.

#figure(visual.errors, caption: [Route error and forward-speed error in the same 5 m/s run.])

- The upper plot answers whether the boat returns to the route.
  - Zero is the desired line. The initial value is 2 m for every policy.
    - Feedback brings the error close to zero. Fixed equal thrust cannot correct the changing path.
- The lower plot answers whether forward speed approaches 1 m/s.
  - Zero means the speed target is met; this does not imply that the boat is on the desired route.
    - A small speed error can coexist with a large line error, as the open-loop example demonstrates.

The table scores the final ten seconds, after the initial recovery. Values are root-mean-square (RMS) line distances averaged across seeds 792, 793, and 794. A value of 0.05 m means a 5 cm RMS route error over that window, rather than a constant 5 cm offset.

#data-table((1.1in, 1fr, 1fr, 1fr, 1fr), [Environment], [Open loop (m)], [PID (m)], [LQR (m)], [Pole placement (m)],
  ..("full_calm","full_wind5","full_wind10").map(c=>(
    [#(if c=="full_calm" {[Calm]} else {[#c.replace("full_wind", "") m/s wind]})],
    [#pretty(om(c,"tail_cross_rms_m"))],
    ..methods.map(m=>[#pretty(aggregate(c,m,"tail_cross_rms_m").mean)])
  )).flatten())

LQR and pole placement remain close in this moving-line benchmark. PID has a slower recovery and greater residual line error with its saved tuning. The open-loop comparison establishes why feedback is useful before comparing which feedback design performs best.

#pagebreak()
= What the controller changes and what the sensors measure
The error plots explain the outcome. The motor commands explain the action that produces it. Open loop sends the same motor percentage to both motors; feedback changes their sum to regulate forward motion and their difference to steer.

#figure(visual.commands, caption: [Signed motor commands in 5 m/s wind, seed 792. Zero is neutral.])

- Increasing both motor commands increases nominal forward thrust.
  - Increasing starboard thrust relative to port gives a counterclockwise yaw moment.
    - A corrective turn may require one motor to reduce thrust or reverse briefly. Actual force still follows the nonlinear lookup, lag, and slew limit.
- The line coordinate and desired speed come from the reference, not from a sensor.
  - GNSS measures antenna position, world velocity, and heading. The IMU measures yaw rate; the shared estimator corrects the antenna offset and extrapolates delayed data.
    - The controller computes line and speed errors from that estimate. Stereo camera observations remain simulated but are unused in this route-following benchmark.

== Bow direction and travel direction are different
The following snapshot uses the LQR boat at 20 s in 10 m/s wind. The bow points into the wind while motion remains nearly along the east-going route. The hull drawing is enlarged for clarity; arrow directions come from the simulated state.

#figure(visual.crab, caption: [A crab heading can hold the route while the boat moves east.])

- Heading $psi$ says where the bow points.
  - Direction of travel follows world velocity, measured by GNSS.
    - With forward velocity $u$ and sideways velocity $v$, the world components are $V_E = u cos psi - v sin psi$ and $V_N = u sin psi + v cos psi$.
- A successful wind-compensating boat does not always point exactly east.
  - The controller can hold a southward heading so that forward motion cancels the northward sideways component.
    - For this task, score line error and forward speed rather than treating a nonzero heading as failure.

#pagebreak()
= Use the flags to explain the difference
Once the path and objective are clear, the simulator flags become experiments rather than a list of implementation details. Every stage below uses the same initial condition, reference, fixed open-loop command, and frozen feedback gains. Command sampling is enabled in every stage so that all policies share a 50 Hz decision clock.

#figure(visual.ladder, caption: [Open-loop and feedback line error as model features are added.])

#data-table((0.45in,1.1in,1fr), [Stage], [Preset], [Added behavior],
  [0], [`00_linear`], [Local hull and tangent thrust; perfect hull feedback.],
  [1], [`01_hull`], [Nonlinear hull rotation, coupling, and drag.],
  [2], [`02_m200`], [Nonlinear signed thrust, saturation, deadband, reverse asymmetry.],
  [3], [`03_motor`], [Motor lag and force slew limit.],
  [4], [`04_timing`], [Command delay.],
  [5], [`05_sensors`], [Measured feedback with noise, bias, delay, and antenna offset.],
  [6], [`06_disturbances`], [Wind, gusts, apparent wind, wind moment, waves.],
  [7], [`07_uncertainty`], [Added inertia, motor mismatch, jitter, command loss, watchdog, sensor loss.])

- The line error already exists at the simplest stage.
  - The open-loop boat starts displaced and never receives a correction to that objective.
    - Added features change its path; they do not supply missing feedback.
- The three feedback methods retain much smaller route errors across the ladder.
  - The primary study uses the same inverse M200 map for all policies that request force.
    - Early tangent-thrust stages therefore include a mismatch with that physical map compensation. No controller gain is retuned between stages.
- The curve need not rise monotonically as features are added.
  - Added damping, inertia, and yaw coupling can change both the disturbance response and the direction of travel.
    - A more detailed simulation is a different model, not automatically a more accurate boat prediction.

== Reproduce the comparison
The study contains 171 feedback runs and #open.runs.len() fixed-command runs, including the nominal illustrations, matched full-model environments, and the same eight-stage ladder. Report maps use seed 792; summary values include all three seeds.

```sh
uv run python -m blueboat_sim.controller_study
uv run python -m blueboat_sim.open_loop_study
typst compile controller_report.typ controller_report.pdf
```

- `data/open_loop.json` retains commands, configurations, scores, paths, and source hashes.
  - Full truth CSVs and command records are under `build/open-loop/`.
    - Regenerate the feedback data with `uv run python -m blueboat_sim.controller_study`.
- All 28 project tests pass, including fixed-command independence from observations, nominal straight-line trim, and failure to correct an initial heading/line error.
  - Replaying all 210 runs preserves their physical results exactly.
