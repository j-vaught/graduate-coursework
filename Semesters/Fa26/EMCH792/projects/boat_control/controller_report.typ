#import "simulator_report/style.typ": *
#set document(title: "BlueBoat Controller Design and Nonlinear Comparison", author: "J.C. Vaught", date: datetime(year: 2026, month: 10, day: 11))
#set page(paper: "us-letter", margin: (x: 0.72in, top: 0.73in, bottom: 0.72in),
  header: [#text(size: 8.5pt, fill: slate)[BLUEBOAT CONTROLLER STUDY] #h(1fr) #text(size: 8.5pt, fill: slate)[J.C. Vaught]],
  footer: context align(center, text(size: 9pt, counter(page).display("1"))))
#set text(font: "Times New Roman", size: 10.5pt, lang: "en")
#set par(leading: 0.54em, spacing: 0.65em)
#set heading(numbering: "1.1")
#show heading.where(level: 1): set text(size: 17pt, fill: ink, weight: "bold")
#show heading.where(level: 2): set text(size: 12pt, fill: ink, weight: "bold")
#show heading: set block(above: 13pt, below: 7pt)
#set list(indent: 0.85em, body-indent: 0.5em, spacing: 4pt, marker: ([•], [-], [▪]))
#set figure(gap: 7pt)
#show figure.caption: set text(size: 9pt)
#set math.equation(numbering: "(1)")
#show raw: set text(font: "Menlo", size: 8pt)
#show table: set text(size: 9pt)
#show link: set text(fill: teal)
#let d = json("controller_report/data/design.json")
#let summary = json("controller_report/data/summary.json")
#let traces = json("controller_report/data/traces.json")
#let methods = ("pid", "lqr", "pole_placement")
#let names = ("PID", "LQR + integral", "Pole placement + integral")
#let pretty(x, digits: 3) = if x == none { [Not settled] } else { str(calc.round(x, digits: digits)) }
#let aggregate(case, method, metric) = summary.aggregate.find(r => r.case == case and r.method == method).metrics.at(metric)

#text(size: 25pt, fill: ink)[BlueBoat Controller Design]
#v(7pt)
#text(size: 16pt)[PID, LQR, and pole placement on the nonlinear simulator]
#v(12pt)
J.C. Vaught #h(1fr) October 11, 2026
#v(16pt)
This study implements three controllers for the most complete BlueBoat simulator and compares them with fixed tuning. All controllers track a straight east-going line at a surge speed of 1 m/s. Wind, gusts, prescribed wave forcing, nonlinear hull motion, installed M200 propulsion, motor dynamics, command timing, sensor errors, and added inertia remain enabled in the full-model tests.

- The task is moving line tracking.
  - Recover from a 2 m northward displacement, a 0.12 rad heading error, and an initial surge speed of 0.8 m/s.
    - North position should approach zero while surge speed approaches 1 m/s. East position is free; there is no timed arrival or along-track position target.
- The comparison uses the same feedback and actuator boundaries.
  - Delivered global navigation satellite system (GNSS) and inertial measurement unit (IMU) records feed a common timestamp-aware state estimate.
    - Camera observations remain simulated but are unused by these navigation controllers. Perfect-state feedback is enabled only in the explicitly named oracle ablation.
- Tuning is frozen before the comparison sweep.
  - #summary.runs.len() runs cover #summary.cases.len() cases and #summary.seeds.len() paired seeds per method.
    - The results describe this simulator and operating envelope. The simulator report documents which physical coefficients require boat measurements.

#note[The controller named LQR includes integral augmentation and is therefore a linear-quadratic-integral regulator. Pole placement uses the same augmented states. Their integral terms let sustained disturbances produce a corrective bias rather than a permanent line error.]

#pagebreak()
#outline(title: [Contents], depth: 2)
#pagebreak()
#include "controller_report/design.typ"
#include "controller_report/results.typ"
#pagebreak()
#bibliography("references.bib", title: [References], style: "ieee")
