#import "../style.typ": ink
#let defaults = json("../../configs/simulator/00_linear.json")
#let fmt(value) = {
  if type(value) == float { str(calc.round(value, digits: 6)) }
  else if type(value) == array { value.map(v => str(v)).join(", ") }
  else { str(value) }
}
#let units(key) = {
  if key == "initial_state" { [m, m, rad, m/s, m/s, rad/s] }
  else if key.ends-with("_N_s2_m2") { [N s²/m²] }
  else if key.ends-with("_N_m_s2") { [N m s²] }
  else if key.ends-with("_N_s") { [N/s] }
  else if key.ends-with("_N_m") { [N m] }
  else if key.ends-with("_m_s2") { [m/s²] }
  else if key.ends-with("_rad_s") { [rad/s] }
  else if key.ends-with("_m_s") { [m/s] }
  else if key.ends-with("_m2") { [m²] }
  else if key.ends-with("_percent") { [percentage points] }
  else if key.ends-with("_us") { [µs] }
  else if key.ends-with("_px") { [px] }
  else if key.ends-with("_rad") { [rad] }
  else if key.ends-with("_deg") { [deg] }
  else if key.ends-with("_s") { [s] }
  else if key.ends-with("_m") { [m] }
  else if key.ends-with("_N") { [N] }
  else { [dimensionless / identifier] }
}
= Complete parameter reference <param-chapter>

The flag catalog selects behavior, while this reference records every non-Boolean field in the baseline JSON template. Values are generated directly from that template to keep the report aligned with its runnable configuration. Field names preserve the command-line spelling. Numerical values are rounded to six decimal places here; the saved JSON retains their full precision.

- The baseline keeps most physical effects disabled while retaining their numerical settings.
  - Enabling a flag activates its associated values without replacing them.
    - The cumulative uncertainty preset changes three probabilities. Missed commands become 0.02, GNSS dropout becomes 0.05, and camera dropout becomes 0.10. It also disables perfect-state feedback as inherited from the sensor stage.
- Each group below supplies the prefix used in `--set group.field=value`.
  - Top-level experiment settings use `--set field=value`.
    - The initial-state sequence is ordered $x,y,psi,u,v,r$. A custom initial velocity does not automatically change the operating-point trim used to initialize motor force.
- Camera geometry and measurement-error fields specify this simulator abstraction.
  - They do not replace camera calibration, noise characterization, or receiver status logs.
    - Delay, noise, bias, dropout, and disturbance magnitudes become physical claims only after identification under documented conditions.

#for (label, group) in (
  ([Experiment settings], none),
  ([Hull parameters], "hull"),
  ([Actuator and command parameters], "actuator"),
  ([Environmental parameters], "environment"),
  ([Sensor parameters], "sensors"),
) {
  heading(level: 2, label)
  let entries = if group == none {
    defaults.pairs().filter(pair => type(pair.last()) != dictionary)
  } else { defaults.at(group).pairs() }
  text(size: 8.8pt)[
    #table(columns: (2.75in, 1.1in, 1fr), inset: (x: 5pt, y: 4pt), stroke: 0.3pt + luma(75%),
      table.header([Field], [Default value], [Unit / kind]),
      ..entries.map(pair => (raw(pair.first()), [#fmt(pair.last())], units(pair.first()))).flatten(),
    )
  ]
}
