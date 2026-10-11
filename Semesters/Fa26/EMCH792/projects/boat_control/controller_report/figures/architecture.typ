#import "../../simulator_report/style.typ": *
#cetz.canvas(length: 1cm, {
  import cetz.draw: *
  set-style(content: (padding: 2pt), stroke: 0.8pt + ink)
  node((0, 2.4), (2.8, 3.7), [#text(size: 9pt)[Line and speed#linebreak()reference]])
  node((3.5, 2.4), (6.4, 3.7), [#text(size: 9pt)[PID / LQR /#linebreak()pole placement]])
  node((7.1, 2.4), (10.2, 3.7), [#text(size: 9pt)[Allocation +#linebreak()M200 inverse map]])
  node((10.9, 2.4), (14, 3.7), [#text(size: 9pt)[Timing + motors#linebreak()+ nonlinear hull]])
  for (a, b) in (((2.8, 3.05), (3.5, 3.05)), ((6.4, 3.05), (7.1, 3.05)), ((10.2, 3.05), (10.9, 3.05))) {
    line(a, b, mark: arrow)
  }
  node((7.1, 0), (10.2, 1.3), [#text(size: 9pt)[GNSS + IMU#linebreak()acquisition / delivery]])
  node((3.5, 0), (6.4, 1.3), [#text(size: 9pt)[Time + lever arm#linebreak()state estimate]])
  line((12.45, 2.4), (12.45, 0.65), (10.2, 0.65), mark: arrow)
  line((7.1, 0.65), (6.4, 0.65), mark: arrow)
  line((4.95, 1.3), (4.95, 2.4), mark: arrow)
  content((12.4, 1.6), [#text(size: 8pt)[Physical state]])
})
