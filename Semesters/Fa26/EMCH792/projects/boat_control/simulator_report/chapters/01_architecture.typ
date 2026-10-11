#import "../style.typ": note, data-table
#import "../figures/architecture.typ": architecture

= Simulator architecture

The simulator advances a planar BlueBoat model while keeping motor response, command scheduling, and sensor delivery explicit. It accepts prerecorded signed motor-percentage commands or a callback at configured decision ticks. The callback boundary is ready for future control software, while the current presets use command tapes and do not supply a controller, estimator, guidance law, or stock autopilot.

== Signals and model boundary

The signal path separates physical truth from information available to a policy. That distinction lets experiments score a simulated trajectory against its generated measurements without giving the policy access to hidden state.

#figure(architecture(), caption: [Signal flow from percentage inputs through motor and vessel dynamics to measurements and logged truth.]) <arch-signal-flow>

The internal state has six vessel coordinates and two motor-force states.

- Vessel position and attitude are $(x,y,psi)$, where $x$ is east position in metres, $y$ is north position in metres, and $psi$ is heading in radians measured counter-clockwise from east.
  - Body velocities are $u$ in surge metres per second, $v$ in sway metres per second, and $r$ in yaw radians per second.
  - In nonlinear kinematics, the world-frame position rates are $dot(x)=cos(psi)u-sin(psi)v$ and $dot(y)=sin(psi)u+cos(psi)v$. Heading evolves as $dot(psi)=r$.
- Motor states are port and starboard thrust, $T_p$ and $T_s$, in newtons.
  - Port and starboard percentages are input commands from -100% to +100%. A selected thrust map converts each command to a target force, with optional saturation, neutral deadband, reverse asymmetry, motor mismatch, force lag, and force slew limiting.
  - The vessel receives total surge effort $T_p+T_s$ and yaw moment $b(T_s-T_p)/2$, where $b$ is configured thruster spacing in metres. Sway thrust is not applied directly.

These variables define a state evolution of the form

$ dot(z) = f(z, q, d; c), quad q=(p_p,p_s), quad z=(x,y,psi,u,v,r,T_p,T_s), $

Here $q$ is the pair of applied port and starboard motor percentages, held between command-application events. The requested command can change before $q$ changes when command delay is enabled. The motor-force states in $z$ evolve toward thrust targets computed from $q$. The input $d$ denotes enabled environmental force and moment inputs, and $c$ collects physical and configuration parameters. Vessel motion uses a maximum-step, event-split fourth-order Runge-Kutta update. Motor lag and rate-limited transients are evaluated analytically within each integration step, so the motor state follows its held target independently of the Runge-Kutta approximation used for vessel motion.

== Initial trim and run schedule

The run begins from six configured vessel-state values, then appends a motor trim computed for the configured operating speed. For the default experiment, the initial state is $(0,0,0,1,0,0)$, meaning the reference point starts at the world origin, points east, and moves forward at $1$ m/s with zero sway and yaw rate. Trim force per motor balances half the configured surge drag at the operating speed. Its corresponding motor percentage is obtained from the inverse installed M200 static thrust map. The initialized motor states equal that trim force, avoiding an artificial startup transient.

The scheduler merges integration advances with discrete events. Its event priorities give a precise meaning to measurements and decisions sharing a timestamp.

- Sensor acquisition is scheduled at integer multiples of each sensor period, beginning at $t=0$.
  - Acquisition samples the current internal state, computes measurement values and validity, and records acquisition time. Enabled noise, bias, lever arm, occlusion, and dropout logic act at this point.
  - A sensor delivery event is scheduled at acquisition time plus its selected latency. If delay is disabled, latency is zero and delivery occurs at the acquisition timestamp.
- A decision occurs at each command-period tick when command sampling is enabled. Without command sampling, decisions occur at the times listed in the command tape.
  - At a shared timestamp, acquisition events run first, deliveries run next, and decisions run afterward. Therefore a zero-latency measurement acquired at a decision tick is available to that decision. A nonzero-latency measurement is visible only after its delivery event.
  - A returned command can be delayed by compute time, transport time, actuator dead time, and optional nonnegative jitter. The applied motor command updates the motor target; force lag and slew limits then determine how quickly force changes.
- Truth logging occurs after acquisition, delivery, decision, actuation, and watchdog events at the same time.
  - Logs include the eight state values, current motor percentages, and force targets. The run also exports acquisition and availability times, measurement values and validity, event records, and decision audits.

Each simulation interval is integrated only as far as the next event or integration-step boundary, whichever comes first. This allows sensor and command timing to stay exact relative to the event clock while retaining a fixed maximum physics step.

== Measurement access and information limits

Sensor models create observations from the internal truth, but a policy receives only the latest delivered observation from each enabled sensor. A measurement contains its sensor name, acquisition time, availability time, validity, and named values. Invalid samples contain missing values; pending future samples are not exposed.

- The Global Navigation Satellite System (GNSS) reports antenna position, heading, and earth-frame velocity. The configurable antenna lever arm shifts antenna position and includes rotational velocity when enabled.
  - The current configuration labels the GNSS solution as real-time kinematic (RTK) fixed. It does not simulate transitions among fixed, float, or single-point solutions.
- The inertial measurement unit (IMU) reports yaw rate and planar body-frame acceleration, including the configured gyro bias and measurement noise.
- The stereo-camera abstraction reports target range and bearing from configured target geometry, focal length, baseline, and image bounds.
  - It can mark observations invalid for geometry, maximum range, occlusion, or random loss. It computes geometric observations directly and does not render images or run perception software.

Truth is retained separately from measurements for audit and scoring. With `perfect_state_feedback=true`, the policy observation also includes the six vessel coordinates $(x,y,psi,u,v,r)$, but not motor force. With that flag disabled, the policy must work from delivered sensor records. An estimator that reconstructs vessel state from GNSS and inertial measurements remains future work.

== Worked measurement timeline

The default sensor periods are 0.05 s for GNSS, 0.005 s for the inertial unit, and $1/30$ s for the camera. The following example uses the `05_sensors` preset, where sensor delay is enabled with configured latencies of 0.080 s, 0.005 s, and 0.030 s respectively. At the first decision tick, $t=0.020$ s, recent samples have different acquisition ages and delivery status.

#data-table((1fr, 1fr, 1fr, 1fr, 2fr),
  [Sensor], [Sample time], [Available time], [At $t=0.020$ s], [Policy can use],
  [GNSS], [$0.000$ s], [$0.080$ s], [pending], [No GNSS sample yet.],
  [IMU], [$0.015$ s], [$0.020$ s], [arrives at decision], [Yes, after same-time delivery.],
  [Camera], [$0.000$ s], [$0.030$ s], [pending], [No camera sample yet.],
)

At $0.020$ s, the IMU sample is acquired at $0.015$ s and delivered exactly at the decision time. Event priority delivers it before the policy callback, so it is visible with a 5 ms age. The GNSS sample describes the state at time zero but remains unavailable until $0.080$ s; the camera sample becomes available at $0.030$ s. This schedule distinguishes when a sensor observed the boat from when decision software may use that observation.

== Implemented and future control boundary

The simulator implements a motor-percentage interface at the actuator boundary. A callback may return port and starboard percentages or return no command to hold the current command. Command sampling, transport delay, missed updates, and watchdog neutralization are configurable mechanisms around that boundary.

- Current experiments can replay a fixed command tape to compare model fidelity under identical inputs.
  - Comparison runs freeze a shared absolute motor-percentage tape and initial state. Independent random streams keep sensor, timing, and disturbance trials paired across feature configurations.
- A future controller can be connected through the policy callback after it defines decision timing and consumes delivered measurements.
  - State estimation, guidance, force allocation, and conversion from requested surge force and yaw moment to left/right motor percentages remain integration tasks.
  - The motor-command boundary does not reproduce the stock autopilot control loops or software.

#note[The current architecture supplies configurable plant, actuator, scheduler, and measurement models. Control and estimation behavior begins only when a user provides a policy callback.]
