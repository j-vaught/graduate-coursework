#import "figures.typ" as f
#import "hardware_figures.typ" as hw
#let cv = json("data/component_validation.json")
#let p = json("data/parameters.json")
#let schedule = json("data/schedule.json")
#set list(indent: 0.9em, body-indent: 0.55em, spacing: 4pt)
#let validation = json("data/validation.json")
#let metrics = validation.metrics
#let fmt = f.fmt
#set document(title: "BlueBoat Dynamics and Control Feasibility", author: "J.C. Vaught", date: datetime(year: 2026, month: 10, day: 8))
#set page(paper: "us-letter", margin: (x: 0.85in, top: 0.8in, bottom: 0.8in),
  header: [#text(size: 9pt)[J.C. Vaught] #h(1fr) #text(size: 9pt)[EMCH 792 · Boat control]],
  footer: context align(center, text(size: 9pt, counter(page).display("1"))))
#set text(font: ("Times New Roman", "New Computer Modern"), size: 11pt, lang: "en")
#set par(justify: true, leading: 0.57em, spacing: 0.75em)
#set heading(numbering: "1.")
#show heading: set text(size: 12pt, weight: "bold")
#show heading: set block(above: 12pt, below: 7pt)
#show figure.caption: set text(size: 9pt)
#set figure(gap: 7pt)
#set math.equation(numbering: "(1)")
#show table: set text(size: 9.5pt, hyphenate: false)
#let tbl(columns, ..cells) = table(columns: columns, inset: (x: 6pt, y: 5pt), stroke: none,
  table.hline(stroke: 0.8pt), ..cells, table.hline(stroke: 0.8pt))
#let section(title) = heading(title)

#align(center)[
  #text(size: 21pt)[BlueBoat Dynamics]
  #v(3pt)
  #text(size: 18pt)[and Control Feasibility]
  #v(9pt)
  J.C. Vaught #linebreak()
  EMCH 792 · Dr. Yi Wang #linebreak()
  October 8, 2026
]
#v(5pt)
#line(length: 100%, stroke: 1pt + f.garnet)

= Project objective
An autonomous surface vessel (ASV) must reach a target while wind changes its motion. BlueBoat uses two M200 motors with weedless propellers to generate forward force and yaw moment. This report evaluates that platform using its published dimensions, a selected loaded configuration, and explicit motion-model assumptions @BlueRobotics2025BlueBoat @BlueRobotics2026BlueBoatProduct.

- Every motion experiment uses the same BlueBoat model.
  - Equal thrust reaches #fmt(metrics.surge_terminal_m_s, digits: 3) m/s. A modeled 5 m/s crosswind causes #fmt(metrics.drift_60s_m) m of unpowered drift in 60 s.
  - The selected sensors observe this same motion; the delayed-motor tests use the same mass, inertia, drag, and spacing.
- The report establishes the plant for subsequent controller design.
  - These open-loop results quantify disturbance sensitivity. They do not claim measured hull performance or closed-loop recovery.

#figure(f.hull(), caption: [BlueBoat layout with hull origin $O$ and thrust-line separation $B$.]) <hull>

#tbl((1.05fr, 1.2fr, 1.45fr),
  table.header([Quantity], [Simulation value], [Basis]), table.hline(stroke: 0.5pt),
  [Length / beam], [1.20 m / 0.93 m], [Published BlueBoat geometry],
  [Loaded mass], [#fmt(p.mass_kg, digits: 1) kg], [Bare hull + batteries + equipment allowance],
  [Yaw inertia / spacing], [#fmt(p.yaw_inertia_kg_m2, digits: 3) kg m² / 0.75 m], [Geometric proxy / mounting estimate],
  [Propulsion], [Two M200 motors at 16 V], [Installed forward envelope 80.41 N],
)

#pagebreak()
= Physical configuration and parameter basis
The layout fixes the platform; its loading and propulsion determine the simulated response. Published values and selected configuration choices are recorded separately from coefficients that require on-water identification. All experiment files import the same configuration.

#tbl((1.35fr, 0.85fr, 1.55fr),
  table.header([Parameter], [Value], [Basis]), table.hline(stroke: 0.5pt),
  [Deployed length / beam / height], [1.20 / 0.93 / 0.46 m], [Manufacturer @BlueRobotics2025BlueBoat],
  [Bare mass], [14.5 kg], [Manufacturer],
  [Batteries], [Two; 2.4 kg total], [Standard-battery selection @BlueRobotics2026BlueBoatProduct],
  [Equipment and mounts], [5.0 kg], [Payload allowance; weigh installed equipment],
  [Loaded mass, $m$], [#fmt(p.mass_kg, digits: 1) kg], [Sum of hull, batteries, and allowance],
  [Batteries + payload capacity], [15.0 kg], [Selected load 7.4 kg],
  [Thrust-line separation, $B$], [0.75 m], [Estimated motor center spacing; survey hull],
  [Yaw inertia, $I_z$], [#fmt(p.yaw_inertia_kg_m2, digits: 3) kg m²], [Uniform planar-envelope proxy],
  [M200 weedless-propeller diameter], [112 mm], [Manufacturer @BlueRobotics2026Weedless],
  [Battery / static-map voltage], [14.8 V nominal / 16 V test], [4S battery; 16 V curve snapshot],
  [Installed forward force, each], [#fmt(p.thrust_max_N) N], [Half of published 8.2 kgf boat total],
  [Installed reverse force, each], [#fmt(p.thrust_min_N) N], [Same scaling applied to signed component curve],
)

The yaw-inertia proxy is $I_z=m(L^2+W^2)/12$. It treats the load as a uniform planar envelope; the actual twin-hull mass distribution and centrally mounted equipment require a measured replacement. The 0.75 m motor spacing is smaller than the 0.93 m beam and is not inferred as an exact manufacturer dimension.

#tbl((1.35fr, 0.85fr, 1.55fr),
  table.header([Motion coefficient], [Nominal value], [Basis]), table.hline(stroke: 0.5pt),
  [Surge linear drag, $d_1$], [4 N s/m], [Engineering assumption],
  [Surge quadratic drag, $d_2$], [10 N s²/m²], [Engineering assumption],
  [Sway linear drag, $d_v$], [35 N s/m], [Engineering assumption],
  [Yaw linear drag, $d_r$], [12 N m s], [Engineering assumption],
)

- Hydrodynamic coefficients are provisional.
  - They are not transferred from the presentation or fitted from BlueBoat trials. The later sensitivity tests vary mass and surge drag.
  - Added mass, propeller inflow, roll, pitch, and wave excitation are omitted from this initial planar model.
- The voltage snapshot is explicit @BlueRobotics2026OperatorGuide.
  - A standard 4S battery is nominally 14.8 V and fully charged at 16.8 V. The available M200 lookup describes 16 V static testing.
  - Battery discharge and inflow require additional measured thrust maps; no voltage law is inferred from this single curve.

#pagebreak()
= Planar model and simulation method
The physical configuration supplies the coefficients of a three-degree-of-freedom model. The inertial pose is $bold(eta)=(x,y,psi)^T$, and body velocity is $bold(nu)=(u,v,r)^T$. Position uses east and north coordinates; heading and yaw are counterclockwise from east. Surge points forward and sway points left. The equations retain planar rigid-body coupling and damping @Fossen2026MarineModel.

Heading rotates body velocity into the inertial frame, giving
$ dot(x)=u cos psi-v sin psi, quad dot(y)=u sin psi+v cos psi, quad dot(psi)=r. $ <kinematics>
The two parallel thrust lines generate the force and moment
$ tau_u=T_L+T_R, quad tau_v=0, quad tau_r=B/2 (T_R-T_L). $ <allocation>
With body-frame wind forces $F_u$ and $F_v$, the dynamic equations are
$ m dot(u)=m v r+T_L+T_R-d_1 u-d_2 u abs(u)+F_u, $ <surge>
$ m dot(v)=-m u r-d_v v+F_v, $ <sway>
$ I_z dot(r)=B/2 (T_R-T_L)-d_r r. $ <yaw>

A nominal wind speed of 5 m/s is converted to force through $F= rho_a C_D A V^2/2$. The assumed air density is 1.225 kg/m³, drag coefficient is 1, frontal area is 0.18 m², and lateral area is 0.30 m². Thus, the selected headwind force is #fmt(p.headwind_force_N, digits: 3) N and crosswind force is #fmt(p.wind_force_N, digits: 3) N. These areas include an allowance for exposed equipment and must be measured with the final mounts.

For a constant world-frame wind force $(F_x,F_y)$, the body forces are $F_u=F_x cos psi+F_y sin psi$ and $F_v=-F_x sin psi+F_y cos psi$. The tests hold this force fixed rather than recomputing apparent wind from boat velocity. Wind acts through the reference center with zero yaw moment. This provides a controlled disturbance test; off-center wind loading is a subsequent extension.

- The first experiments isolate hull response with ideal force application.
  - Every force command passes through the bounded, signed installed-M200 lookup. Force onset is instantaneous in these reference tests.
  - The later component chain applies sampling, execution delay, deadband, saturation, and thrust lag to the same hull model.
- Integration preserves input changes.
  - Relative and absolute tolerances are $10^(-10)$ and $10^(-12)$; the maximum step is 0.05 s. Each constant-input interval is integrated separately.
  - Histories are exported to data files and drawn as vector figures. Numerical refinement tests check each experiment.

#pagebreak()
= Steady and differential thrust
The first experiment isolates surge motion. Both M200 motors step to 15 N at $t=1$ s from rest. Drag rises until it balances the 30 N total force. Setting $dot(u)=0$ in @surge gives
$ d_2 u_infinity^2+d_1 u_infinity=30, quad u_infinity=(-d_1+sqrt(d_1^2+120 d_2))/(2 d_2)=#fmt(metrics.surge_terminal_m_s, digits: 4) "m/s". $
#figure(f.equal-step(), caption: [Equal-M200-thrust surge response.]) <equal>

The second experiment applies $T_L=10$ N and $T_R=15$ N at $t=1$ s. The 5 N difference generates #fmt(metrics.differential_yaw_moment_N_m, digits: 3) N m of yaw moment, giving $r_infinity=tau_r/d_r=#fmt(metrics.differential_terminal_r_rad_s, digits: 4)$ rad/s. Rotation induces negative sway through $-u r$, which feeds back into surge through $v r$.

#figure(f.differential(), caption: [Differential-M200-thrust translation and yaw.]) <differential>

#grid(columns: (1fr, 1fr), column-gutter: 20pt,
  align(center, f.turning-path()),
  [
    #v(12pt)
    The coupled terminal speeds are $u=#fmt(metrics.differential_terminal_u_m_s, digits: 4)$ m/s and $v=#fmt(metrics.differential_terminal_v_m_s, digits: 4)$ m/s. From @sway, $v_infinity=-m u_infinity r_infinity/d_v$, so lateral speed persists during the turn.

    At 60 s, the boat is at $(#fmt(metrics.differential_endpoint_m.first()),#fmt(metrics.differential_endpoint_m.last()))$ m. Equal scaling of both axes preserves the path geometry.

    The asymptotic turning radius is $sqrt(u_infinity^2+v_infinity^2)/abs(r_infinity)=#fmt(metrics.turning_radius_m)$ m. A constant thrust difference therefore creates sustained turning rather than convergence to a target.
  ],
)

#pagebreak()
= Pulse response and free decay
The sustained turn establishes coupling between motion components. A short asymmetric pulse then shows how that coupling persists after thrust is removed. The boat receives $T_L=30$ N and $T_R=-15$ N over $1 <= t < 2$ s and coasts for the remainder of the 30 s test. Both commands lie within the provisional installed-M200 envelope.

#figure(f.pulse(), caption: [Sway and yaw responses to a one-second M200 pulse.]) <pulse>

The pulse supplies 15 N of forward force and −16.875 N m of yaw moment. The yaw minimum is #fmt(metrics.pulse_min_r_rad_s, digits: 4) rad/s, while sway reaches #fmt(metrics.pulse_peak_v_m_s, digits: 4) m/s. Positive sway follows from $-u r$ when surge is positive and yaw is negative. Sway peaks after the pulse because turning and lateral damping act on different time scales.

The unforced test starts at $(u,v,r)=(1,0.5,0.5)$ and applies zero thrust for 30 s. Velocity approaches zero, but final position and heading depend on the integrated transient.

#figure(f.decay(), caption: [Unforced BlueBoat translation and yaw decay.]) <decay>

This behavior follows from kinetic energy. Defining $E=m(u^2+v^2)/2+I_z r^2/2$, substitution of @surge, @sway, and @yaw gives
$ dot(E)=-d_1 u^2-d_2 abs(u)^3-d_v v^2-d_r r^2 <= 0. $
The coupling terms cancel because they transfer energy between surge and sway. Damping removes energy, while position has no restoring term. Consequently, the boat can stop moving without reaching the desired location.

#pagebreak()
= Phase-plane behavior and wind drift
Free decay motivates a closer view of the sway–yaw subsystem. Holding surge at $U$ gives $dot(v)=-d_v v/m-U r$ and $dot(r)=-d_r r/I_z$. The phase portraits use 25 initial pairs spanning $v_0 in [-1,1]$ m/s and $r_0 in [-0.5,0.5]$ rad/s. Surge is frozen for this diagnostic rather than integrated as a third state.

#figure(f.phase-pair(), caption: [BlueBoat sway–yaw phase portraits at 0 and 1 m/s surge.]) <phase>

The decay rates are $-d_v/m=-#fmt(p.sway_linear_N_s_m/p.mass_kg, digits: 3)$ s⁻¹ and $-d_r/I_z=-#fmt(p.yaw_linear_N_m_s/p.yaw_inertia_kg_m2, digits: 3)$ s⁻¹. Both remain negative as $U$ changes, so surge modifies the transient geometry without changing these eigenvalues. The nominal time constants are #fmt(metrics.wind_time_constant_s, digits: 3) s for sway and #fmt(metrics.yaw_time_constant_s, digits: 3) s for yaw.

Wind shifts the velocity equilibrium. With zero thrust, zero initial motion, and #fmt(p.wind_force_N, digits: 3) N of crosswind force, @sway has the solution
$ v(t)=F_y/d_v (1-e^(-t/tau_v)), quad y(t)=F_y/d_v [t-tau_v(1-e^(-t/tau_v))], quad tau_v=m/d_v. $

#figure(f.wind(), caption: [Unpowered BlueBoat drift under modeled crosswind.]) <wind>

The lateral equilibrium is $v_infinity=F_y/d_v=#fmt(metrics.drift_terminal_m_s, digits: 4)$ m/s. Its integrated displacement is #fmt(metrics.drift_60s_m, digits: 4) m at 60 s. Position continues to drift after the velocity transient has decayed. This persistent offset is the disturbance the subsequent guidance controller must reject.

#pagebreak()
= Open-loop target approach
The drift result predicts failure of an input schedule calibrated only for calm water. The boat starts from rest at the origin and aims at $(20,0)$ m. Both M200 motors apply 15 N until $t=#fmt(schedule.chosen_cutoff_s, digits: 4)$ s, then switch to zero. The cutoff is computed from the BlueBoat model rather than fitted to a presentation curve.

#figure(f.schedule(), caption: [BlueBoat equal-thrust schedule and cutoff detail.]) <schedule>

The calm-water coast distance from cutoff speed $u_s$ is $m/d_2 ln(1+d_2 u_s/d_1)$. Adding it to the powered distance sets the asymptotic calm endpoint to 20 m. The headwind and crosswind cases use the same schedule without recalibration.

#figure(f.blind(), caption: [BlueBoat target approach under calm and wind conditions. Path axes use different scales.]) <blind>

#tbl((1.2fr, 1fr, 1fr, 1fr),
  table.header([Environment], [$x(90)$ (m)], [$y(90)$ (m)], [Target error (m)]), table.hline(stroke: 0.5pt),
  ..("calm", "crosswind", "headwind").map(name => {
    let row = metrics.blind_90s_states.at(name)
    ([#name], [#fmt(row.x, digits: 4)], [#fmt(row.y, digits: 4)], [#fmt(row.distance, digits: 4)])
  }).flatten(),
)

Crosswind preserves forward progress in this model because heading remains zero, but lateral displacement reaches #fmt(metrics.blind_90s_errors_m.crosswind) m at 90 s. Headwind reduces powered progress and then drives the unpowered boat backward; its final surge speed is #fmt(metrics.blind_90s_states.headwind.u, digits: 4) m/s. Thus, an open-loop schedule cannot regulate target distance under sustained wind.

#pagebreak()
= Numerical verification and parameter sensitivity
The preceding results depend on the BlueBoat configuration and provisional motion coefficients. Independent analytic checks first establish that the numerical integration follows those equations. The sensitivity tests then show how uncertainty in the coefficients changes the response.

#tbl((1.65fr, 1fr, 1.25fr),
  table.header([Verification], [Result], [Interpretation]), table.hline(stroke: 0.5pt),
  [Surge analytic agreement], [$#calc.round(validation.checks.surge_exact_max_error_m_s*1e11,digits:2) times 10^(-11)$ m/s], [Constant equal-thrust solution],
  [Yaw analytic agreement], [$#calc.round(validation.checks.yaw_exact_max_error_rad_s*1e12,digits:2) times 10^(-12)$ rad/s], [Constant differential moment],
  [Wind analytic agreement], [$#calc.round(validation.checks.wind_exact_max_error_m*1e12,digits:2) times 10^(-12)$ m], [Lateral drift solution],
  [Step refinement], [$#calc.round(validation.checks.step_refinement_max_state_difference*1e10,digits:2) times 10^(-10)$], [Maximum state difference; each state's units],
  [Energy / thrust / loading], [Pass], [Dissipative decay and physical bounds],
  [Controllability at rest / 1 m/s], [4 / 6], [Local linear-model ranks],
)

#figure(f.overlays(), caption: [BlueBoat mass and assumed surge-drag sensitivity.]) <overlays>

- Loading changes acceleration.
  - Compare 16.9 kg with two batteries and no added equipment, the nominal 21.9 kg configuration, and the 29.5 kg maximum loaded mass.
  - Drag is held fixed in this isolated test; mass changes the transient without changing the modeled steady speed.
- Drag changes both the transient and steady speed.
  - Scale the linear and quadratic surge terms together by 0.5, 1, and 2, holding thrust and mass fixed.
  - The resulting spread is model uncertainty, not a measured confidence interval.
- Verification and physical validation serve different purposes.
  - Analytic agreement checks the equations and solver. On-water logs must establish the actual inertia, drag, added mass, and installed thrust.
  - Every active result uses BlueBoat. The original presentation remains a historical source; its larger-boat traces are not validation data for this hull.

#pagebreak()
= Selected hardware and mission architecture
The BlueBoat wind tests show why feedback is required. Real-time kinematic (RTK) positioning supplies the global navigation satellite system (GNSS) reference. The deployment architecture assigns image processing and guidance to AGX Orin while retaining the BlueBoat Pi 4, Navigator, and ArduRover for low-level control. This assignment keeps the motor loops independent of the image-processing workload @BlueRobotics2025BlueBoat.

#tbl((0.8fr, 1.55fr, 1.5fr),
  table.header([Function], [Selection], [Reason / interface]), table.hline(stroke: 0.5pt),
  [Companion], [AGX Orin, 64 GB configuration @Nvidia2026Orin], [Perception, fusion, guidance; Ethernet],
  [Stereo vision], [One ZED X, 2 mm wide lens], [Global shutter; GMSL2 / ZED Link Duo capture],
  [Inertial sensing], [VectorNav VN-110 rugged], [Gyroscope, acceleration, attitude; RS-422],
  [Position / heading], [Septentrio mosaic-H], [RTK position; dual-antenna heading],
  [Antennas], [Two PolaNt-xMF @Septentrio2026Polant], [Fore–aft mounting, ≈1 m baseline],
  [Propulsion], [Existing M200 pair and ESCs], [Navigator pulse-width modulation],
)

#figure(f.feedback(), caption: [Proposed mission, sensing, guidance, and propulsion architecture.]) <feedback>

- One ZED X is the initial camera configuration @Stereolabs2026ZEDX.
  - It already contains two synchronized imagers and a 120 mm stereo baseline.
  - A second ZED X adds rear or side coverage. It is justified when a measured blind area limits a task, rather than to obtain the first stereo depth estimate.
    - Use the ZED Link Duo capture card supported on AGX Orin @Stereolabs2026Capture. Reserve a second mounting point and validate synchronization, extrinsics, and execution load before enabling it.
- RTK uses a local correction source @Septentrio2026MosaicH.
  - Mount a reference receiver at a surveyed point in the operating tent and relay Radio Technical Commission for Maritime Services (RTCM) corrections over the permitted local link.
  - Dual antennas give heading while stationary; the receiver reports solution status and correction age with the position.

#pagebreak()
= Signal ownership and measured outputs
The high-level blocks in @feedback separate responsibility. The detailed interfaces below make each command and measurement explicit, so guidance inputs are not confused with motor inputs.

#figure(hw.lowlevel(), caption: [Guidance on Orin and motor control in ArduRover.]) <lowlevel>

#tbl((1.05fr, 1.55fr, 1.4fr),
  table.header([Boundary], [Input], [Output]), table.hline(stroke: 0.5pt),
  [Mission → autonomy], [Waypoints, target class, task state], [Selected target / route],
  [Perception], [Stereo images, calibration, timestamps], [Class, bearing, depth, validity],
  [State estimator], [GNSS, gyro, acceleration, attitude], [$hat(x),hat(y),hat(psi),hat(u),hat(v),hat(r)$ and covariance],
  [Guidance], [Route, target geometry, estimated state], [$u_d$ in m/s; $r_d$ in rad/s],
  [Autopilot], [References; its navigation feedback], [Left / right PWM in µs],
  [Physical plant], [Actual $T_L,T_R$; wind / waves], [Pose and body velocity],
)

- The physical plant is actuated by force, not by sensor data.
  - An electronic speed controller (ESC) turns a pulse-width modulation (PWM) command into motor drive. The propeller converts rotation into thrust.
  - Actual thrust is a modeled internal quantity, inferred from the installed map. This sensor suite does not directly measure thrust, torque, or motor revolutions per minute.
- The navigation outputs are observations of boat motion.
  - GNSS measures antenna position, inertial velocity, and dual-antenna heading. Orin and the autopilot both consume the receiver stream; Navigator’s IMU supplies autopilot propagation. The VN-110 supplies Orin’s independent motion observations.
  - The inertial measurement unit (IMU) measures angular velocity and specific force. Its attitude and heading reference system (AHRS) provides an orientation estimate.
    - Use dual-GNSS heading as the main absolute heading reference. Motor magnetic fields can contaminate magnetic heading.
- The camera measures the scene relative to its optical frame.
  - Images are the raw outputs; detection class, bearing, disparity, and depth are processed outputs. Global position requires the estimated boat pose and camera extrinsics.

#pagebreak()
= Navigation sensing and reference conventions
The measured outputs become useful to control only after their coordinate frames and timestamps agree. Configure the autopilot’s Septentrio Binary Format dual-antenna backend and GNSS yaw source, then verify received rates and antenna offsets @ArduPilot2026Septentrio. Mount the VN-110 close to the center of gravity, survey both antenna lever arms, and calibrate the camera-to-hull transform. Use the GNSS pulse-per-second signal to discipline timestamps and record acquisition and delivery times separately.

- The mosaic-H supplies the high-accuracy global reference @Septentrio2026MosaicH.
  - The manufacturer specifies horizontal RTK accuracy of 0.6 cm plus 0.5 parts per million of baseline distance and heading accuracy of 0.15° with 1 m antenna separation.
  - The component test assumes RTK fixed, 20 Hz updates, 2 cm position noise, and 80 ms delivery latency. It uses 0.03 m/s velocity noise and 0.15° heading noise.
    - Inflate the estimator covariance when RTK becomes float or single-point. Stop using a stale correction status as evidence of centimeter positioning.
- The VN-110 supplies rapid motion measurements @VectorNav2026VN110.
  - Configure 200 Hz raw IMU output. The simulation uses 5 ms delivery latency, 0.002 rad/s gyro noise, a 0.001 rad/s residual bias, and 0.02 m/s² acceleration noise.
    - These are integration stress assumptions. They are not derived from the manufacturer’s noise-density specification.
  - Magnetic AHRS heading is simulated at 2° standard deviation, matching the scale of the manufacturer’s 2° RMS heading specification under calibrated magnetic conditions.

For a primary antenna located at body offset $bold(ell)=(-0.5,0)^T$ m, the observation model accounts for both position and rotational velocity.
$ bold(p)_a = bold(p) + R(psi) bold(ell), quad bold(V)_a = R(psi) [bold(v)_b + r J bold(ell)], quad J = mat(0,-1;1,0). $
Here $bold(p)=(x,y)^T$, $bold(v)_b=(u,v)^T$, and $R(psi)$ is the planar rotation matrix. A gyro measures $r+b_g+n_g$. At the center of gravity, the planar accelerometer model after gravity compensation is
$ a_x = dot(u)-v r+n_x, quad a_y = dot(v)+u r+n_y. $
This rotating-frame correction avoids treating a body velocity derivative as the accelerometer output. Roll, pitch, gravity, and off-center acceleration terms must be restored for the three-dimensional deployment.

The report uses east–north coordinates with leftward sway and counterclockwise yaw. ArduRover accepts body-forward velocity and yaw rate through the MAVLink message #text(font: "Menlo", size: 8pt)[SET_POSITION_TARGET_LOCAL_NED] in Guided mode @ArduPilot2026RoverGuided. Use the velocity-plus-yaw-rate mask 1511 and body frame 9. For this convention, set $v_x=u_d$, $v_y=0$, and $"yaw_rate"=-r_d$. If sending absolute heading, convert with $psi_"NED"=pi/2-psi$. The adapter sends the 50 Hz references and verifies the sign conversion in a low-speed left-turn test.

#pagebreak()
= Computer execution and response budget
The command interface defines what must meet a deadline. Run state propagation and guidance at 50 Hz, process images at 30 Hz, and deliver the latest valid reference through a bounded queue. Camera processing uses a separate worker so a late image cannot hold the guidance loop.

#figure(hw.timing(), caption: [Assumed command-to-thrust-onset timing budget.]) <timing>

#tbl((1.3fr, 0.85fr, 1.3fr),
  table.header([Stage], [Budget], [Meaning]), table.hline(stroke: 0.5pt),
  [Guidance sampling], [0–20 ms], [Wait until the next 50 Hz tick],
  [Estimator / guidance compute], [5 ms], [Execution allowance per tick],
  [Command transport / acceptance], [10 ms], [Orin to low-level controller],
  [Actuator dead time], [20 ms], [PWM update and drive response],
  [Motor time constant, $tau_T$], [0.2 s], [Sensitivity tests at 0.1 and 0.4 s],
)

For a newly changed command, the onset delay is bounded by the sample wait plus the fixed delays. The nominal bound is
$ L_"onset" <= 20+5+10+20 = 55 "ms". $
A first-order motor reaches 90% of its final force after $tau_T ln 10=0.4605$ s from onset. The simulated command changes at 1.023 s, is sampled at 1.040 s, and starts changing thrust at 1.075 s. The sampled 90% crossing occurs 0.517 s after demand, including motor lag.

- AGX Orin performance is established by execution measurements.
  - The 5 ms guidance budget and 20 ms vision budget are targets. Processor throughput does not establish either latency.
  - Log acquisition, dequeue, compute start/end, command send/receive, and PWM application timestamps using a common clock.
    - Record median, 95th and 99th percentile, maximum latency, missed deadlines, power mode, temperature, and image resolution under sustained load.
- Freshness is part of the response model.
  - The assumed worst measurement ages are 130 ms for GNSS, 10 ms for IMU, and 63.3 ms for the camera processing stream.
    - These bounds add one sample period to delivery latency. Propagate the state to command time and reject stale perception updates.
  - Implement a reference watchdog with an initial 100 ms timeout. Validate neutral-command delivery and the independent kill path; ArduRover’s documented velocity-command timeout is 3 s @ArduPilot2026RoverGuided.

#pagebreak()
= Motor and propeller response
The execution budget delays a command before the propulsion system responds. The propulsion model then maps each pulse width $p_i$ to a static thrust $T_{s,i}$ and applies a dynamic lag. The manufacturer’s M200 weedless-propeller curve at 16 V supplies the signed static lookup @BlueRobotics2026M200Reference @BlueRobotics2026MotorGuide.

#figure(hw.motor(), caption: [M200 static curve, installed-map assumption, and delayed reversal.]) <motor>

The static map interpolates the retained data after clipping $p_i$ to 1100–1900 µs. Commands from 1475 through 1525 µs produce zero demand, with 1500 µs neutral. The manufacturer component limits at 16 V are −27.56 N reverse and 55.21 N forward. The boat simulations use the uniformly scaled installed envelope, #fmt(p.thrust_min_N) N reverse and #fmt(p.thrust_max_N) N forward per motor. The dynamic model is
$ tau_T dot(T_i)+T_i=T_{s,i}(p_i(t-L_i),16"V"), quad i in {L,R}. $
For a constant demand after onset $t_0$, the force response is $T_i(t)=T_s+(T_i(t_0)-T_s)e^(-(t-t_0)/tau_T)$. The simulation changes the pulse demand at 1.023, 3.023, and 5.023 s; it integrates exactly between delayed changes. Its first forward step agrees with this analytic response to $1.31 times 10^(-9)$ N.

- Component thrust and installed-boat thrust require separate calibration.
  - The curve describes the manufacturer’s M200-and-propeller component test. BlueBoat’s published total static thrust is 8.2 kgf, approximately 80.4 N @BlueRobotics2026BlueBoatProduct.
  - The component maxima sum to 110.4 N. A factor of #fmt(p.installation_scale, digits: 4) scales the entire signed curve so the forward total matches the published 80.41 N boat envelope.
    - This is a provisional installation model. The reverse limit and intermediate curve are inferred by uniform scaling; they are not installed-boat measurements.
    - Mounting, guards, hull interaction, voltage, and inflow change the installed map. Use a load cell to measure each side and both sides together with the final guards installed.
- The dynamic model has identifiable limits.
  - Fit separate acceleration, reversal, and coast constants from synchronized force and PWM logs; test several pulse amplitudes and battery voltages.
    - Add rate limits or a second-order rotor model when the measured response requires them. The 0.2 s lag is a starting assumption, not a manufacturer response specification.

#pagebreak()
= Boat response and parameter identification
The motor tests establish a force history for the same BlueBoat plant used earlier. Equal thrust uses 15 N per side; the turning test uses 8 N left and 10 N right until 6.023 s, followed by neutral. These commands remain below the scaled M200 limits.

#figure(hw.boat-response(), caption: [M200 lag sensitivity and BlueBoat turning response.]) <boat-response>

At 2 s, ideal equal thrust gives #fmt(cv.summary.ideal_surge_at_2s_m_s, digits: 4) m/s while the delayed $tau_T=0.2$ s chain gives #fmt(cv.summary.delayed_surge_at_2s_m_s, digits: 4) m/s. Instantaneous thrust therefore overstates early speed by #fmt(cv.summary.ideal_surge_at_2s_m_s - cv.summary.delayed_surge_at_2s_m_s, digits: 4) m/s for this input. Yaw also persists after neutral while propeller force decays.

- Replace the provisional loading and geometry with measurements.
  - Weigh batteries, computer, sensors, guards, mounts, and cables separately, then weigh the assembled boat.
  - Survey thrust-line spacing and loaded center of gravity. Estimate yaw inertia from the measured mass distribution or a dedicated inertia test.
    - A narrowed competition configuration changes both spacing and inertia and requires a separate configuration.
- Identify the planar force response.
  - Equal-pulse steps establish surge acceleration; coast-down helps identify linear and quadratic drag.
  - Unequal and opposing thrust establish yaw response, while turning runs expose sway coupling and damping.
    - Repeat in both directions and record voltage, wind, current, payload, RTK status, and temperature. Hold out complete runs for prediction checks.
- Extend the identified model when the residuals require it.
  - Use $(M_"RB"+M_A)dot(bold(nu))+C(bold(nu))bold(nu)+D(bold(nu))bold(nu)=bold(tau)+bold(tau)_d$ to retain added mass @Fossen2026MarineModel.
  - Fit installed thrust and motor lag using force and PWM logs before attributing response error to hull damping.
    - Add roll, pitch, waves, and off-center wind moments when they materially affect actuation or sensing.

These measurements update the shared configuration rather than creating separate parameter sets for different figures. The report already uses BlueBoat geometry and propulsion throughout; identification replaces its remaining engineering assumptions.

#pagebreak()
= Sensor response under changing motion
The force chain produces motion that each sensor samples at its own rate. The following test uses the same unequal-thrust maneuver as the preceding section, a fixed random seed, and acquisition-time truth. Measurements are plotted at delivery time, exposing delay rather than hiding it with an ideal continuous observation.

#figure(hw.sensor-response(), caption: [Simulated GNSS position and IMU yaw-rate observations with noise and latency.]) <sensor-response>

#figure(hw.camera-response(), caption: [Simulated stereo range with a 5–6 s occlusion and distance-dependent depth uncertainty.]) <camera-response>

The stereo test observes a target at $(15,3)$ m in the world frame and occludes frames from 5 to 6 s. For a rectified stereo pair, disparity $d=p_L-p_R$ gives forward optical depth $Z=f b/d$. A target at planar bearing $beta$ has horizontal image coordinate $p_L=c_x-f tan beta$ and range $rho=Z/cos beta$. The first-order depth uncertainty is
$ sigma_Z approx Z^2/(f b) sigma_d. $
For $f=700$ pixels, $b=0.12$ m, and $sigma_d=0.5$ pixel, depth uncertainty is 0.60 m at 10 m and 2.38 m at 20 m. The camera model therefore reports range validity rather than promising centimeter accuracy from stereo.

- Camera latency includes capture and perception.
  - The test processes 30 frames/s with 10 ms acquisition/transfer and 20 ms vision compute. It assumes a rectified 1920-pixel image with $f=700$ pixels; deployed intrinsics replace that approximation.
  - Invalid, behind-camera, out-of-view, occluded, and beyond-20 m observations are withheld. The run returns #cv.summary.camera_valid_frames of #cv.summary.camera_total_frames frames.
    - Water glare, low texture, and object occlusion require measured validity thresholds. This geometric test does not reproduce the detector or the stereo software’s full error distribution.

#pagebreak()
= Control feasibility and competition integration
The shared BlueBoat component chain supports controller development, but it does not supply closed-loop performance results. The presentation’s proposed linear-quadratic regulator (LQR) minimizes state error and control effort around a local operating point @MathWorks2026LQR. Its feasibility depends on whether thrust can influence each relevant motion mode.

- The boat is laterally underactuated.
  - At rest, $dot(y)=v$ and $dot(v)=-d_v v/m$ have no direct thrust input. The six-state controllability matrix has rank four; the uncontrolled lateral-position integrator has eigenvalue zero.
  - At a straight-running reference of $U=1$ m/s, yaw and lateral motion couple and the rank becomes six. The nominal trim requires 14 N total thrust, within the scaled installed-M200 envelope.
    - Use a moving reference and constrained guidance. A full-state LQR about rest cannot stabilize arbitrary lateral position.
- The initial deployment closes the motor loops in ArduRover.
  - Orin sends feasible speed and turn-rate references. Route tracking or an outer-loop regulator can be evaluated without introducing a competing motor controller.
  - An LQR that outputs individual forces requires a separate low-level implementation, allocation, saturation handling, and validated failsafes.
    - Under 30 s recovery, under 10% overshoot, under 0.3 m position error, and under 15° heading error are candidate controller targets. They have not been demonstrated on this BlueBoat model.

The competition configuration also changes the boat’s physical model. The 2027 event is listed for February 18–23 in Sarasota, Florida; its handbook is pending as of October 8, 2026 @RoboNation2026Event2027. The available 2026 requirements define the present integration checks @RoboNation2026Vehicle @RoboNation2026Rules.

- Geometry must fit the competition envelope.
  - The published BlueBoat beam is 0.93 m; the 2026 width limit is 3 ft, or 0.9144 m. The nominal hull exceeds that limit by 15.6 mm.
    - Measure the assembled hull and guards. Obtain the current rule interpretation or design narrower crossbars before claiming eligibility.
- Propulsion must include guards and independent stopping.
  - The requirements specify protected propellers and physical and wireless kill functions that disconnect motor/actuator power.
    - Add guards to the final mounting layout, then remeasure thrust. Route the kill circuit outside the Orin software path shown in @feedback.
- Power and navigation require installation-level checks.
  - Use regulated, fused power and thermal management for Orin and the GMSL2 capture hardware; the hull’s 5 V auxiliary rail is rated at 5 A @BlueRobotics2025BlueBoat.
  - Use local RTK corrections from equipment in the operating tent; the 2026 rules prohibit outside internet connections, including LTE corrections, during semifinal and final runs.
    - Recheck these requirements against the 2027 handbook when released.

These checks lead directly to the next experiment. Install the selected sensor stack, synchronize its logs, identify the loaded hull and guarded propulsion response, and benchmark the execution deadlines. Then evaluate feasible guidance and feedback against the selected recovery targets with measured component parameters.

#pagebreak()
#bibliography("references.bib", style: "ieee", title: [References])
