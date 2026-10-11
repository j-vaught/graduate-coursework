#import "../style.typ": note, data-table
#import "../figures/sensors.typ": sensor-timing, stereo-error

= Sensor measurement models

The simulator schedules global navigation satellite system (GNSS), inertial, and stereo observations from one vessel truth state. Each stream has its own sampling period, seeded noise and dropout draws, and delivery event. The selected hardware motivates these measurement channels, while the simulator equations below define exactly what its controller boundary receives @Septentrio2026MosaicH @VectorNav2026VN110 @Stereolabs2026ZEDX.

#figure(sensor-timing(), caption: [Acquisition ticks and configured delivery delays for the three independent sensor streams.]) <sens-timing>

== GNSS position, velocity, and heading

GNSS samples the vessel reference pose and body velocity, then rotates those quantities into the east-north frame. The configurable antenna location lies a distance $ell$ forward or aft along the boat axis. Let $(x,y,psi)$ denote vessel reference position and heading, $(u,v)$ body surge and sway speed, and $r$ yaw rate. The antenna position and velocity are

$ x_a=x+ell cos psi, quad y_a=y+ell sin psi, $
$ v_(a,e)=u cos psi-v sin psi-ell r sin psi, quad v_(a,n)=u sin psi+v cos psi+ell r cos psi. $

- `antenna_lever_arm` selects $ell="gnss_x_m"$; otherwise $ell=0$.
  - The default configured offset is $-0.5$ m, so the antenna is behind the reference point. Rotation contributes the tangential velocity terms proportional to $ell r$.
  - GNSS heading is the simulated $psi$ with configured heading noise. The selected Mosaic-H is a dual-antenna heading receiver; a geometric baseline measurement can be represented as $psi="atan2"(Delta_N,Delta_E)$, where $(Delta_E,Delta_N)$ is the baseline vector between antennas. Baseline heading is not separately simulated.
- Position, velocity, and heading are one named measurement record.
  - Default standard deviations are 0.02 m per position coordinate, 0.03 m/s per earth-frame velocity coordinate, and 0.15 degrees for heading. The configuration calls its solution mode `RTK_FIXED`; it does not model solution-mode transitions.
  - Default position bias is zero. Configurable east and north biases and an optional antenna lever arm affect generated values when their flags are enabled.

== Planar inertial measurements

The inertial channel reports yaw rate and body-frame specific acceleration at the vessel reference point. Its acceleration equations preserve the rotating body-frame kinematics, so directly exposing derivatives of $u$ and $v$ would omit the centripetal coupling terms:

$ omega_z=r, quad f_x=dot(u)-v r, quad f_y=dot(v)+u r. $

- The channel samples at 200 Hz by default and reports $omega_z$, $f_x$, and $f_y$.
  - Configured white-noise standard deviations are 0.002 rad/s for yaw rate and 0.02 m/s² for each acceleration component.
  - Yaw-rate bias defaults to 0.001 rad/s. Acceleration bias is zero in this model.
- The accelerometer values are computed from the planar physics derivative at acquisition time.
  - Gravity projection, roll and pitch, sensor-axis misalignment, scale factors, and temperature effects are not represented.
  - This output is suitable as an estimator input, but the simulator supplies no attitude filter or inertial integration.

== Stereo target range and bearing

The camera abstraction uses a configured static world target and pinhole stereo geometry. It computes ideal target image center and disparity from truth, applies configured pixel noise, and converts those measurements to range and bearing. It does not produce image frames or perform detection, matching, or perception @Stereolabs2026ZEDX.

The default target is at east-north coordinates $(15,3)$ m, while the initial vessel pose is $(0,0,0)$, so the initial target lies 15 m forward and 3 m to port. The resulting 15.3 m horizontal range is within the configured 20 m validity limit and projects inside the 1920 px image.

For world target $(X_T,Y_T)$ and boat pose $(x,y,psi)$, define forward depth $Z$ and lateral offset $Y$ in the boat frame. The true horizontal range and bearing are $R=sqrt(Z^2+Y^2)$ and $beta="atan2"(Y,Z)$. The image center coordinate $c$ and stereo disparity $d$ follow

$ c=c_0-f_x Y/Z, quad d=f_x B/Z, $

where $c_0$ is half the image width, $f_x$ is focal length in pixels, and $B$ is stereo baseline. The noisy pixel coordinate produces $hat(beta)="atan"((c_0-hat(c))/f_x)$. The model recovers horizontal range as $hat(R)=f_x B/[hat(d)cos(hat(beta))]$.

- A sample is geometrically valid only when depth and disparity are positive, the noisy target center lies within the configured image width, the target range is no greater than 20 m, and the configured occlusion window is inactive.
  - Random dropout can invalidate an otherwise valid observation. Invalid measurements retain their keys but carry missing values.
  - Default focal length is 700 px, baseline is 0.12 m, image width is 1920 px, center-coordinate noise is 2 px, and disparity noise is 0.5 px.
- Disparity uncertainty produces rapidly growing range uncertainty.
  - For a front-facing target with small bearing error, $R approx Z=f_x B/d$. Linearizing this inverse-depth relation gives $sigma_R approx Z^2 sigma_d/(f_x B)$.
  - The plotted curve uses configured $f_x$, $B$, and $sigma_d$ and spans the valid 20 m range for an on-axis target. It defines uncertainty as one standard deviation from disparity noise alone; pixel-center noise contributes additional bearing and horizontal-range error off the centerline.

#figure(stereo-error(), caption: [First-order stereo range standard uncertainty from the configured disparity noise and camera geometry.]) <sens-range-error>

At 10 m, the model predicts disparity $700(0.12)/10=8.4$ px and first-order range standard uncertainty of about 0.60 m. At 20 m, disparity falls to 4.2 px while uncertainty grows to about 2.38 m. These values expose a geometry limit for downstream estimation; they are not output from image processing or a camera noise experiment.

== Timing, uncertainty, and estimation boundary

The defaults below combine rates, delay settings, and noise scales from `Sensors`. Latency affects when a sample becomes visible, while uncertainty affects its value at acquisition. Each feature is gated independently by the corresponding experiment flags.

#data-table(
  (1.0fr, 0.75fr, 0.9fr, 1.55fr),
  [Stream], [Rate], [Latency], [Default value uncertainty],
  [GNSS], [20 Hz], [80 ms], [0.02 m; 0.03 m/s; 0.15 deg],
  [Inertial], [200 Hz], [5 ms], [0.002 rad/s; 0.02 m/s²],
  [Stereo], [30 Hz], [30 ms], [0.5 px disparity; 2 px center],
)

#note[Rates and latencies are configuration values. The standard deviations are injected only when sensor_noise is enabled; biases, delay, and random dropout likewise require their respective flags.]

An acquisition record stores sample time, availability time, validity, delivered values, and the separate truth used to generate those values. The scheduler exposes only the latest delivered measurement per stream to a policy, so stale and delayed observations are distinguishable from the current state. Independent random streams let noise and dropout draws remain reproducible without coupling one sensor's samples to another's.

- Measurement history supports direct comparison against truth for scoring and debugging.
  - Invalid samples are recorded and delivered with missing values, preserving the timing of a lost update.
  - A pending sample is not available before its scheduled delivery time, even though its acquisition truth is already logged for evaluation.
- State estimation remains a consumer responsibility.
  - GNSS provides intermittent pose and earth-frame velocity, while the inertial stream supplies fast body motion cues and stereo supplies target-relative geometry.
  - A filter would need to handle asynchronous sample times, lever-arm corrections, noise and bias, and delayed or missing updates. The simulator does not combine these records into a fused state estimate.
