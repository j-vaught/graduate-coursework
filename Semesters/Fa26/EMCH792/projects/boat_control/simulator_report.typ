#import "simulator_report/style.typ": *
#set document(title: "BlueBoat Configurable Simulator. Design and Verification", author: "J.C. Vaught", date: datetime(year: 2026, month: 10, day: 11))
#set page(paper: "us-letter", margin: (x: 0.72in, top: 0.73in, bottom: 0.72in),
  header: [#text(size: 8.5pt, fill: slate)[BLUEBOAT SIMULATOR] #h(1fr) #text(size: 8.5pt, fill: slate)[J.C. Vaught]],
  footer: context align(center, text(size: 9pt, counter(page).display("1"))))
#set text(font: "Times New Roman", size: 10.5pt, lang: "en")
#set par(justify: false, leading: 0.54em, spacing: 0.65em)
#set heading(numbering: "1.1")
#show heading.where(level: 1): set text(size: 17pt, fill: ink, weight: "bold")
#show heading.where(level: 2): set text(size: 12pt, fill: ink, weight: "bold")
#show heading.where(level: 3): set text(size: 10.5pt, fill: ink, weight: "bold")
#show heading: set block(above: 13pt, below: 7pt)
#set list(indent: 0.85em, body-indent: 0.5em, spacing: 4pt)
#set list(marker: ([•], [-], [▪]))
#set figure(gap: 7pt)
#show figure.caption: set text(size: 9pt)
#set math.equation(numbering: "(1)")
#show raw: set text(font: "Menlo", size: 8.5pt)
#show table: set text(size: 9pt)
#show link: set text(fill: teal)

#v(0.2in)
#text(size: 25pt, fill: ink)[BlueBoat Configurable Simulator]
#v(7pt)
#text(size: 16pt)[Design, assumptions, configuration, and verification]
#v(12pt)
J.C. Vaught #h(1fr) October 11, 2026
#v(16pt)
The simulator supplies a repeatable environment for developing boat controllers. It separates hull motion, M200 propulsion, command execution, and sensor delivery so that each assumption can be tested independently. This report documents the implemented equations and information flow, gives the complete flag reference, and explains the saved model comparisons.

- Begin with a local linear plant around a declared operating speed.
  - Add nonlinear hull and propulsion effects, then motor response, timing, sensing, and disturbances.
    - Compare identical commands and initial conditions before attributing a change to the selected feature.
- Keep simulated motion separate from controller observations.
  - The internal state supplies numerical integration and scoring; measurement delivery supplies the future feedback interface.
    - An explicit perfect-state switch supports ideal controller tests. Ordinary sensor tests require an estimator.
- Distinguish implementation verification from boat validation.
  - Automated checks establish consistency, causality, bounds, and repeatability.
    - Measured boat logs establish predictive accuracy. Added model detail does not by itself establish improvement.

#note[
The saved demonstration uses an open-loop command program. The companion controller report adds proportional-integral-derivative control, linear quadratic regulation, pole placement, and state estimation through the same motor-percentage interface.
]

The physical demonstration follows baseline revision `ea307b3`, with its commands now expressed as signed motor percentages. The companion controller report supplies the subsequently implemented feedback study. Its diagrams use a dedicated navy-and-teal language, and its quantitative charts use standard plot colors. Every figure is authored in Typst with CeTZ or Lilaq, with inspectable source data retained beside the chapters.

#pagebreak()
#outline(title: [Report contents], depth: 2)
#pagebreak()
#include "simulator_report/chapters/01_architecture.typ"
#include "simulator_report/chapters/02_dynamics.typ"
#include "simulator_report/chapters/03_actuation.typ"
#include "simulator_report/chapters/04_sensors.typ"
#include "simulator_report/chapters/06_configuration.typ"
#include "simulator_report/chapters/05_experiments.typ"
#pagebreak()
#include "simulator_report/chapters/07_parameter_reference.typ"
#pagebreak()
#bibliography("references.bib", title: [References], style: "ieee")
