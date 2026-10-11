#import "../style.typ": data-table, note
#import "../figures/experiments.typ": tape-and-paths, stage-offsets

= Experiments, Disturbances, and Validation

== Experiment design and comparisons

The comparison runner applies a common command record to configurations that share duration, scenario, operating point, amplitude, and initial state. The saved experiment lasts $12$ s, uses a $5$ ms integration step, and begins at $(x,y,psi,u,v,r)=(0,0,0,1,0,0)$ in SI units. Each configuration receives the same four-event pulse-and-turn input tape, and seed $792$ is used throughout.

- The tape starts at trim, raises both motor commands by $80$ microseconds at $t=2$ s, creates a differential command at $t=4$ s, and returns to trim at $t=6$ s.
  - Reusing the tape makes each run a controlled open-loop comparison under identical requested inputs.
  - Comparing internal motor force as well as position separates command interpretation and actuator response from hull and environmental effects.
- The cumulative mode enables successive groups of model features on top of each preceding stage.
  - The saved order is linear baseline, nonlinear hull, installed motor map, motor response, timing, sensors, disturbances, and parameter uncertainty.
  - A late-stage displacement therefore reflects the accumulated configuration; it cannot be attributed to that stage alone.
- Paired seeds preserve each named random stream across the compared configurations, while separate streams isolate gust, sensor, and timing draws.
  - This reduces avoidable randomness in the comparison, but a single seed does not characterize run-to-run variability.
  - Isolated mode adds each feature group to the same baseline, which is preferable when estimating that group's marginal effect.

#figure(tape-and-paths(), caption: [The common input tape and selected truth trajectories show how cumulative model stages change open-loop response.]) <exp-input-path>

The trajectory legend maps Linear hull to `00_linear`, Nonlinear hull to `01_hull`, With sensing to `05_sensors`, With disturbances to `06_disturbances`, and With uncertainty to `07_uncertainty`.

== Wind and prescribed waves

Environmental forcing enters the planar equations as body-frame surge force $X$, sway force $Y$, and yaw moment $N$. The configured steady wind vector is expressed in earth axes and can include two correlated gust components. With apparent wind enabled, the vessel's earth-frame velocity is subtracted before the relative wind is rotated into body axes.

For heading $psi$, earth-frame wind $(w_E,w_N)$, and body velocities $(u,v)$, the relative wind is $w^e_r=(w_E,w_N)-R(psi)(u,v)$, where $R(psi)$ rotates body components into earth axes. The model then rotates $w^e_r$ back into body axes as $(w_x,w_y)$. Its axis-wise projected-area drag is

$ (X_w,Y_w)=1/2 rho_a C_D (A_f w_x |w_x|, A_l w_y |w_y|), $

where $rho_a$ is air density, $C_D$ is the configured coefficient, and $A_f,A_l$ are frontal and lateral projected areas. If the force is applied at configured body offset $(x_c,y_c)$, its yaw moment is $N_w=x_c Y_w-y_c X_w$. The saved setting places the wind center $0.1$ m forward and on the centerline, so lateral wind force produces a yaw moment while surge force does not.

- Gusts follow a first-order update for two independently driven, temporally correlated components at the configured $0.1$ s interval.
  - For interval $Delta t$ and correlation time $tau_g$, $g_{k+1}=a g_k+sigma_g sqrt(1-a^2) eta_k$, with $a=exp(-Delta t/tau_g)$ and independent unit-normal two-axis draw $eta_k$.
  - Linear interpolation between update times makes the applied wind continuous in time; it does not make the gust process a measured atmospheric record.
- The wave option adds sinusoidal components $[X_q,Y_q,N_q]=[A_X,A_Y,A_N]sin(2 pi t/T_q)$ directly to the three generalized forces.
  - In the saved disturbance stage, the wave amplitudes are $0$ N surge, $1$ N sway, and $0.1$ N m yaw with a $4$ s period.
  - This prescribed planar forcing omits wave propagation, encounter frequency, heave, roll, pitch, and hydrodynamic radiation or diffraction, so it is a repeatable disturbance input rather than a sea-state simulation.

The feature set therefore supports repeatable sensitivity experiments. Its wind drag is an engineering approximation and its wave term is prescribed; neither establishes disturbance fidelity for a particular field condition.

== Reading the saved run

The input tape produces clear cumulative changes in the east-north truth paths. The baseline travels $13.28$ m east and $5.79$ m north by $12$ s. The nonlinear-hull stage ends at $(10.65,5.01)$ m, showing that the same PWM tape can produce a different path when the dynamics change. The sensor stage overlays the timing-stage truth, while prescribed disturbances move the endpoint to $(9.71,7.21)$ m and uncertainty moves it to $(8.86,6.46)$ m. Those endpoints describe the supplied experiment and are not evidence of improved tracking or a better controller.

#figure(stage-offsets(), caption: [Selected cumulative-stage separation from the linear baseline under the same open-loop trial.]) <exp-stage-offset>

The following values are read from the saved comparison record; the force integral is the time integral of the sum of squared port and starboard thrust, not mechanical work or energy.

#table(
  columns: (1.5fr, 0.8fr, 0.8fr, 0.75fr, 0.9fr, 0.9fr),
  inset: (x: 4pt, y: 3pt), stroke: 0.3pt + luma(75%),
  [Stage], [Final E (m)], [Final N (m)], [Peak (N)], [∫ |T|² dt (N² s)], [GNSS RMS (m)],
  [00 linear], [13.28], [5.79], [14.69], [2080], [0.000],
  [01 hull], [10.65], [5.01], [14.69], [2080], [0.000],
  [02 motor map], [10.82], [5.08], [15.46], [2219], [0.000],
  [03 motor response], [10.92], [4.92], [15.46], [2168], [0.000],
  [04 timing], [10.94], [4.89], [15.46], [2168], [0.000],
  [05 sensors], [10.94], [4.89], [15.46], [2168], [0.029],
  [06 disturbances], [9.71], [7.21], [15.46], [2168], [0.029],
  [07 uncertainty], [8.86], [6.46], [16.24], [2224], [0.029],
) <exp-metrics>

In this table, $T$ is the two-element vector of motor thrusts, and ∫ |T|² dt has units N² s. It is a command-effort proxy useful for comparing force histories; calling it energy would require multiplying force by velocity in a physically consistent power calculation. The sensor stage introduces a GNSS position RMS error of $0.029$ m while leaving truth nearly coincident with the timing-stage path. Sensor noise, bias, delay, dropout, and acquisition latency alter delivered observations and their scoring against truth; they do not feed back into the open-loop state integration when the applied command tape is fixed.

== Validation scope and next experiments

The existing tests check implementation behavior. They verify deterministic random streams, force and motor calculations, command timing, sensor causality, feature isolation, and the invariant that sensor errors do not change open-loop truth. These checks establish software properties for the implemented equations and scheduling logic. They do not measure agreement with a physical boat.

- The reported GNSS position error compares the delivered measurement's position with the truth at that measurement's acquisition time.
  - The truth point is the GNSS antenna location, including the configured lever arm, rather than the vessel reference origin.
  - Delivery latency determines when a controller could receive the record; it does not change the acquisition timestamp used for measurement error.
- A field-oriented identification study should collect synchronized PWM, GNSS, inertial, and motor or current records under documented loading and environmental conditions.
  - Estimate surge, sway, yaw, motor-map, lag, and rate parameters from selected maneuvers, then freeze those values before evaluation.
  - Hold out complete sessions, routes, and environmental conditions so adjacent samples from one maneuver do not leak across fit and test partitions.
- Future closed-loop controller comparisons should report tracking error, cross-track error, heading error, settling and overshoot, actuator saturation, force effort, and robustness across held-out seeds and conditions.
  - Score navigation against acquisition-time truth and separately report observation age and dropout so estimation error and communications delay remain distinguishable.
  - These are proposed validation measures; the saved runs do not compare controllers or demonstrate performance gains.

#note[The current evidence supports reproducible software tests and controlled model comparisons. Physical parameter identification and held-out boat trials are required to establish predictive accuracy.]
