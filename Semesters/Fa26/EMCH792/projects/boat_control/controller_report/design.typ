#import "../simulator_report/style.typ": *
#import "context.typ": *
= Implementation and mathematical reference
The preceding maps establish the objective and observed behavior. This appendix gives the sensor processing, limits, model, and gains used to produce those results.

== Causal state estimate
The controllers need body-frame velocities and a current hull position. GNSS measures a displaced antenna and arrives late, so the shared estimator first corrects its lever arm and then extrapolates the corrected measurement to the decision time. It retains the most recent valid record through random dropouts.

The antenna offset is $ell = -0.5$ m along the forward axis. At measurement heading $psi_g$ and yaw rate estimate $hat(r)$, the hull origin and world velocity satisfy the following expressions.
$ hat(E_g) = E_a - ell cos psi_g, quad hat(N_g) = N_a - ell sin psi_g. $
$ hat(V_E) = V_(E,a) + ell hat(r) sin psi_g. $
$ hat(V_N) = V_(N,a) - ell hat(r) cos psi_g. $

For measurement age $Delta = t - t_g$, constant world velocity and yaw rate give the decision-time estimate.
$ hat(E) = hat(E_g) + Delta hat(V_E), quad hat(N) = hat(N_g) + Delta hat(V_N). $
$ hat(psi) = "wrap" (psi_g + Delta hat(r)). $
$ hat(u) = hat(V_E) cos hat(psi) + hat(V_N) sin hat(psi). $
$ hat(v) = -hat(V_E) sin hat(psi) + hat(V_N) cos hat(psi). $

- Between valid GNSS records, the estimate propagates position using held body velocities and propagates heading with IMU yaw rate.
  - The estimator reads only delivered records and timestamps supplied by the policy interface.
    - It does not read simulation truth, environmental forces, actual thrust, motor mismatch, or future packets. It does not subtract the configured gyro bias.
- Valid GNSS acquisition age must stay within 0.5 s and valid IMU acquisition age within 0.1 s.
  - Until both records exist, or after either becomes stale, the policy commands 0% motor command and clears its integrators.
    - This startup behavior explains the small initial speed dip in sensor-based runs.
- This observer is timestamp extrapolation rather than an extended Kalman filter.
  - It does not model acceleration during GNSS latency or estimate sensor bias.
    - The oracle case removes this shared estimation limitation and separates it from the controller law.

== Common motor proxy and limits
The public input is signed motor command $a_i in [-100,100]$ percent for port and starboard. The device adapter produces pulse-width modulation (PWM) at the actuator boundary.
$ p_i = (1500 + 4 a_i) "µs", quad F_(i,"nom") = F_"M200"(p_i). $
Zero is neutral. The enabled deadband covers $-6.25 <= a_i <= 6.25$. At trim, $a_i = 22.475$ gives 7 N; full forward gives 40.207 N and full reverse gives -20.068 N. Percentage denotes normalized drive command, not thrust, electrical power, or motor speed. The feedback laws retain forces in newtons and moments in newton metres, preserving their physical gains.

State feedback uses estimates of total thrust and yaw moment as motor states. A common internal motor proxy follows the requested motor percentages after a nominal 35 ms delay and a 0.2 s first-order lag. The proxy uses the nominal signed M200 map and does not receive acknowledgments for missed commands.
$ dot(hat(F_i)) = (F_(i,"nom") - hat(F_i)) / tau, quad tau = 0.2 " s". $

- Requested force is clipped between approximately $-20.068$ N and $40.207$ N per thruster.
  - The default controller converts bounded force to motor percentage using the inverse installed M200 lookup.
    - This feedforward conversion is identical for all three controllers. Motor mismatch, lag, slew limits, dropout, and timing remain in the plant.
- Conditional anti-windup freezes all stored integrators when either force request clips.
  - Speed, cross-track, and PID heading integrals are also bounded by $2$ m, $12$ m s, and $2$ rad s, respectively.
    - The current integration candidate contributes to the command, but is stored only when feedback is ready and neither thruster clips.
- `--linear-command` replaces the inverse lookup with the nominal trim tangent.
  - This is an independent compensation experiment, not a change in feedback gains.
    - Keep the simulator nonlinear-thrust flag enabled when evaluating compensation on the full boat model.

== Linear design model
The full nonlinear plant supplies the local design model. Linearization occurs at $u = U$, $v = r = psi = 0$, zero environmental forcing, and $F_p = F_s = 7$ N. Wind remains an external disturbance because the feedback gains should not require its true value. The underlying marine equations and coupling follow the simulator's Fossen-style model @Fossen2026MarineModel.

- Added inertia is included in the design.
  - Nominal loaded mass is 21.9 kg; effective surge and sway masses are 24.09 kg and 32.85 kg, and effective yaw inertia is approximately 5.048 kg m².
    - The longitudinal drag derivative is $d_u = d_1 + 2 d_2 U = 24$ N s/m. Lateral and yaw damping are $d_v = 35$ N s/m and $d_r = 12$ N m s.
- The equilibrium total force is $S_0 = d_1 U + d_2 U |U| = 14$ N.
  - Motor sum and moment dynamics have the same time constant $tau$.
    - Saturation, deadband, variable map slope, waves, noise, and timing errors are evaluated in simulation rather than inserted into the linear design matrices.

=== Surge subsystem
Define the augmented surge state $z_s = (delta u, delta S, I_u)^T$, where $delta S = F_p + F_s - S_0$ and $dot(I_u) = delta u$. Its control input is $delta S_c = S_c - S_0$.
$ dot(z_s) = A_s z_s + B_s delta S_c. $
$ A_s = mat(-d_u/m_x, 1/m_x, 0; 0, -1/tau, 0; 1, 0, 0), quad B_s = mat(0; 1/tau; 0). $

=== Sway-yaw subsystem
The lateral augmented state is $z_l = (e_y, psi, v, r, M, I_y)^T$, where $M = b(F_s-F_p)/2$ and $dot(I_y) = e_y$. The input is desired yaw moment $M_c$.
$ dot(z_l) = A_l z_l + B_l M_c. $
$ A_l = mat(0, U, 1, 0, 0, 0;
  0, 0, 0, 1, 0, 0;
  0, 0, -d_v/m_y, -m_x U/m_y, 0, 0;
  0, 0, (m_x-m_y)U/I_z, -d_r/I_z, 1/I_z, 0;
  0, 0, 0, 0, -1/tau, 0;
  1, 0, 0, 0, 0, 0). $
$ B_l = mat(0; 0; 0; 0; 1/tau; 0). $

- The surge and lateral controllability ranks are 3 and 6, matching their state counts.
  - The implemented matrix coefficients are checked against central finite differences of the full nonlinear hull.
    - Separating the local subsystems does not remove nonlinear surge/sway/yaw coupling from the simulator.

== Three controller designs
The common model and interfaces allow three different feedback choices. PID organizes feedback into familiar loops. LQR chooses gains from a quadratic cost, while pole placement chooses the local response rates explicitly. Both state-feedback controllers use the same states and integral definitions, so their different results arise from their gain choices.

=== Cascaded PID
The proportional-integral-derivative (PID) controller regulates surge speed and heading. An outer cross-track proportional-integral loop converts line error into desired heading, and the measured sideslip estimate compensates the difference between hull heading and direction of travel.
$ beta = "atan2" (hat(v), max(hat(u), 0.2)). $
$ psi_d = "clip" (-k_y e_y - k_(I y) I_y - beta, -35 degree, 35 degree). $
$ e_psi = "wrap" (hat(psi) - psi_d). $
$ S_c = S_0 - k_(P u) delta u - k_(I u) I_u - k_(D u) q. $
$ M_c = -k_(P psi) e_psi - k_(I psi) I_psi - k_(D psi) hat(r). $

- The speed derivative is filtered with time constant 0.1 s.
  - With tick interval $h$, the filter coefficient is $alpha = h/(0.1 + h)$.
    - Update $q_k = q_(k-1) + alpha ((delta u_k - delta u_(k-1))/h - q_(k-1))$. Heading derivative action uses measured yaw rate and therefore avoids a derivative kick from a heading-reference step.
- The cross-track loop is slower than the heading loop.
  - Its heading clamp prevents large line errors from requesting a near-sideways course.
    - The design requires forward motion. The denominator floor regularizes the sideslip computation; it does not establish zero-speed controllability.
- PID tuning used an initial engineering choice and a heading-damping adjustment after an exploratory full-model run.
  - The final gains below were frozen for all cases and seeds.
    - No claim is made that these gains are globally optimal or that all three methods had equal optimization effort.

#data-table((1.6in, 1fr, 1fr), [Loop], [Gains], [Interpretation],
  [Surge PID], [#d.settings.speed_kp, #d.settings.speed_ki, #d.settings.speed_kd], [Force per speed, integrated speed, and speed derivative.],
  [Heading PID], [#d.settings.heading_kp, #d.settings.heading_ki, #d.settings.heading_kd], [Moment per heading, integrated heading, and yaw rate.],
  [Cross-track PI], [#d.settings.cross_kp, #d.settings.cross_ki], [Heading per cross-track error and integrated cross-track error.])

=== LQR with integral action
The linear quadratic regulator (LQR) minimizes an infinite-horizon quadratic cost for each augmented subsystem. The state integral therefore enters the cost along with the physical states. SciPy solves the continuous algebraic Riccati equation @SciPy2026CARE.
$ J = integral_0^infinity (z^T Q z + a^T R a) dif t. $
$ A^T P + P A - P B R^(-1) B^T P + Q = 0. $
$ K = R^(-1) B^T P, quad a = -K z. $

- The surge weights are $Q_s = "diag"(25, 0.0025, 4)$ and $R_s = 0.01$.
  - The lateral weights are $Q_l = "diag"(4, 25, 11.111111, 25, 0.04, 0.111111)$ and $R_l = 0.0625$.
    - These engineering weights normalize speed, line error, angular motion, motor effort, and integral accumulation; they do not come from a measured optimum.
- Commands satisfy $S_c = S_0 - K_s z_s$ and $M_c = -K_l z_l$.
  - The integral coordinates create constant force and heading biases needed to reject steady disturbances.
    - The resulting stability statement applies locally to the unconstrained continuous linear model. The implemented sampled nonlinear system is checked by simulation.

=== Pole placement with integral action
Pole placement uses the same augmented models but requests eigenvalues directly. SciPy calculates $K$ so that the eigenvalues of $A - B K$ match the specified poles @SciPy2026PlacePoles.

- Surge poles are $(-0.5, -1.3, -5.5)$ s⁻¹.
  - Lateral poles are $(-0.25, -0.4, -0.7, -1.2, -3.0, -5.5)$ s⁻¹.
    - The slower lateral modes allow line and integral recovery; faster modes govern yaw and motor response. Distinct poles avoid repeated-pole restrictions on each single-input subsystem.
- Commands use the same $S_c = S_0 - K_s z_s$ and $M_c = -K_l z_l$ form.
  - The test checks the achieved eigenvalues numerically.
    - Pole placement controls local response rates but does not itself minimize effort or guarantee robustness to latency, saturation, or model error.

=== Numerical gains and local poles
The following gains are loaded directly from the saved design. Their units follow the state coordinates and force or moment output; gains across different coordinates should not be compared as dimensionless numbers.
#for subsystem in ("surge", "lateral") {
  let s = d.systems.at(subsystem)
  heading(level: 4, if subsystem == "surge" { [Surge gains] } else { [Lateral gains] })
  data-table((1.45in, 1fr), [Method], [Gain row in the declared state order],
    [LQR + integral], [#s.gains.lqr.map(x => pretty(x)).join(", ")],
    [Pole placement], [#s.gains.pole_placement.map(x => pretty(x)).join(", ")])
  for method in ("lqr", "pole_placement") {
    let label = if method == "lqr" { "LQR" } else { "Pole placement" }
    let poles = s.poles.at(method).map(z => {
      let re = pretty(z.at(0))
      let im = calc.abs(z.at(1))
      if im < 0.00001 { re } else { re + (if z.at(1) < 0 { " - " } else { " + " }) + pretty(im) + "i" }
    })
    [#label closed-loop poles in s⁻¹. #poles.join(", ").]
    parbreak()
  }
}
