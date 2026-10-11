#import "simulator_report/style.typ": *
#set document(title: "BlueBoat Objective, Open Loop, and Feedback", author: "J.C. Vaught", date: datetime(year: 2026, month: 10, day: 11))
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

#text(size: 25pt, fill: ink)[What Is the Boat Trying to Do?]
#v(7pt)
#text(size: 16pt)[Open loop first, then PID, LQR, and pole placement]
#v(10pt)
J.C. Vaught #h(1fr) October 11, 2026
#v(12pt)
= The objective. Return to a line and follow it
The previous report chose a moving-line test to compare controllers. This revision begins with the physical task. The boat should recover an east-going route from an initial position and heading error, then keep traveling close to that route at a forward speed of 1 m/s. This is a selected test objective, not a complete competition mission.

#figure({
  import "controller_report/figures/visual_story.typ" as visual
  visual.objective
}, caption: [Start north of the route. Recover it, then continue east.])

- Where should it go?
  - Follow the line $N_d = 0$ m, with east to the right and north upward.
    - The hull origin starts at $(E,N)=(0,2)$ m. Its bow points $0.12$ rad, or 6.9°, north of east. It begins at 0.8 m/s forward speed.
- How should it move?
  - Bring its north position toward zero while bringing forward speed $u$ toward 1 m/s.
    - Forward speed is along the boat's own axis. East ground speed is not a separately controlled reference, and there is no required destination or arrival time.
- What counts as recovery?
  - After the transient, keep line distance within 0.25 m and forward speed within 0.1 m/s of the reference.
    - A settled run stays inside both bounds through the end of the 40 s test. The report also gives continuous error scores so that a late gust does not hide otherwise good tracking.

#note[Read the report in order. First identify the target route, then watch fixed equal thrust, then add feedback. The mathematical controller design is retained in the appendix after the visual comparison.]

#include "controller_report/results.typ"
#pagebreak()
#counter(heading).update(0)
#set heading(numbering: "A.1")
#include "controller_report/design.typ"
#pagebreak()
#bibliography("references.bib", title: [References], style: "ieee")
