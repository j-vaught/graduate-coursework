#import "../style.typ": note
#import "../figures/actuation.typ": thrust-map, reversal-response

= Actuation and Command Timing <actuation-chapter>

== From PWM to thrust

The propulsion model starts from Blue Robotics' signed M200 static samples at 16 V, then scales both motors uniformly to match the BlueBoat's published 8.2 kgf forward rating. This joins a component curve to an installed-boat rating as a provisional model assumption. The product information supplies the 8.2 kgf figure, and the retained technical-reference samples supply the M200 curve @BlueRobotics2026M200Reference @BlueRobotics2026BlueBoatProduct.

The force assigned to a motor at PWM command $p$ follows

$ F_"inst"(p) = s F_"16"(p), quad s = (8.2 "kgf")(9.80665 "N"/"kgf") / (2 max_(p) F_"16"(p)). $

Here $F_16$ is the piecewise-linear interpolation of the retained 16 V samples, and $s = 0.72824$ is dimensionless. The result sets the positive limit to $40.207 N$ per motor and the native reverse limit to $-20.068 N$ per motor. The forward limit is anchored to the product rating. Uniform scaling of reverse and intermediate values is the model's installation assumption.

#figure(
  thrust-map(),
  caption: [The installed map matches the pair's forward rating; the tangent is local to trim.],
) <actuation-thrust-map>

The simulator offers two actuator descriptions so the experiment can isolate nonlinear effects from a local approximation.

- The nonlinear lookup path uses the installed curve and clips PWM to 1100-1900 µs when thrust saturation is enabled.
  - With neutral deadband enabled, commands from 1475 through 1525 µs produce zero thrust.
  - With reverse asymmetry enabled, commands below neutral use the signed reverse branch, retaining the lower reverse limit. When disabled, the model mirrors the forward branch into reverse and therefore removes the measured map asymmetry.
- The local model computes $F = F_0 + k (p-p_0)$ around a selected trim.
  - At 1 m/s, the standard linear and quadratic surge drag values require $7.0 N$ per motor. The map gives $p_0 = 1589.9 "µs"$, with a local slope $k = 0.09614 N/"µs"$.
  - At 1600 µs, both predict $7.971 N$ because trim and 1600 µs lie in the same piecewise-linear map segment. At 1700 µs, the lookup gives $18.854 N$ while the tangent extrapolation gives $17.585 N$, a $1.269 N$ difference.

The force path also allows a channel mismatch after PWM-to-force conversion. Port and starboard gains default to 0.95 and 1.05, then thrust bounds are reapplied if saturation is active. For example, at the plotted 1700 µs command, the native installed lookup gives $18.85 N$ before channel gains. The channel targets become $17.91 N$ and $19.80 N$, so equal PWM commands can create a $1.89 N$ thrust difference and an unintended yaw moment.

== Motor response after a command

Once an applied command sets a new target, the simulator evolves motor force with an optional first-order lag and optional force slew limit. With lag time constant $τ$ and rate limit $R$, define error magnitude $m = |F_t-F_0|$, direction $q in {-1,0,1}$ from current force toward target, and transition time $t_r = max(m-R τ,0)/R$. The remaining error is

$ e(t) = cases(
  m-R t, & 0 <= t <= t_r,
  min(m,R τ) exp(-(t-t_r)/τ), & t > t_r,
) quad F(t)=F_t-q e(t). $

This combined law initially slews at up to $R$ and then follows the first-order exponential tail. When only lag is enabled, the full response is exponential. When only the rate limit is enabled, force moves at constant rate until it reaches the target. With both features disabled, target force applies immediately.

#figure(
  reversal-response(),
  caption: [Motor force response to a 1700-to-1300 µs reversal after the target applies.],
) <actuation-reversal-response>

For this plotted reversal, each motor changes target from forward to reverse while its state starts at the corresponding 1700 µs steady force. The port target moves from $17.91 N$ to $-9.17 N$, and the starboard target moves from $19.80 N$ to $-10.14 N$. With $τ=0.2 s$ and $R=80 N/s$, the port error magnitude is $27.09 N$ and the linear portion lasts about $0.139 s$, followed by an exponential tail. The starboard linear portion lasts about $0.174 s$. The delay from command decision to applied target is separate from these motor dynamics.

== Command clock and delivery faults

When command sampling is enabled, the configured $20 "ms"$ period gives a 50 Hz decision rate. When command delay is enabled, each command then passes through three configured delay terms: $5 "ms"$ for computation, $10 "ms"$ for transport, and $20 "ms"$ of actuator dead time. Their nominal sum is $35 "ms"$, or 1.75 command periods. Optional timing jitter adds a uniform value from zero to $3 "ms"$ per decision. Because delayed commands are queued as events, more than one command may be in flight.

- Sampling and delays affect when a new PWM pair can change the target.
  - A missed update creates no application event, so the previously applied PWM and force target remain in effect.
  - The default missed-command probability is zero; fault experiments can raise it.
- The optional watchdog monitors applied command freshness.
  - Its default timeout is $100 "ms"$. Each applied command schedules a timeout, and newer applications invalidate older timeout events.
  - If the active timeout expires, both PWM commands return to 1500 µs and both force targets become zero. Enabled lag and slew limits still govern how actual force approaches zero.

The 50 Hz command period, delay values, jitter bound, motor lag, rate limit, mismatch, and watchdog timeout are configuration values for engineering experiments. They are not measurements of onboard timing. Orin timing is represented only by an assumed computation delay; this simulator does not emulate an Orin processor, operating system, or software scheduling load. The exposed boundary accepts paired PWM commands and produces simulated thrust. It does not implement the stock autopilot software.

#note[Interpret each delay as an explicit test input. For a command issued at $t=1.000 s$, the nominal application time is $1.035 s$ before jitter, and the post-application force response then follows the selected motor model.]
