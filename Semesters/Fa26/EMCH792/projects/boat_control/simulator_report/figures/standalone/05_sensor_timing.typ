#import "../../style.typ": cetz, ink, teal, pale, slate, arrow, node, plot-panel
#let data = json("../../data/sensors.json")

#let sensor-timing() = {
  import cetz.draw: line, content
  set text(font: "Times New Roman", size: 9pt)
  let x = (t) => 1.9 + 8.6 * t / 0.12
  cetz.canvas(length: 0.8cm, {
    content((6.2, 3.9), [Configured acquisition and delivery schedule])
    content((11.5, 3.45), [Period / latency (ms)])
    for (i, stream) in data.streams.enumerate() {
      let y = 3.1 - i * 1.15
      content((0.2, y), stream.name)
      line((1.5, y), (10.6, y), stroke: 0.7pt + slate)
      let step = stream.period_s
      let t = 0.0
      while t <= 0.12 + 1e-8 {
        let tx = x(t)
        line((tx, y - 0.12), (tx, y + 0.12), stroke: 1.2pt + teal)
        t += step
      }
      let dx = x(stream.latency_s)
      line((x(0), y - 0.24), (dx, y - 0.24), stroke: 0.8pt + ink, mark: arrow)
      line((dx, y - 0.36), (dx, y - 0.12), stroke: 1.2pt + ink)
      content((11.5, y), [#calc.round(stream.period_s * 1000, digits: 1) / #calc.round(stream.latency_s * 1000)])
    }
    line((x(0), -0.15), (x(0.12), -0.15), stroke: 0.7pt + slate)
    for t in (0.0, 0.04, 0.08, 0.12) {
      let tx = x(t)
      line((tx, -0.24), (tx, -0.06), stroke: 0.7pt + slate)
      content((tx, -0.42), [#calc.round(t * 1000) ms])
    }
    content((5.1, -0.82), [teal ticks = acquisitions; navy arrows = configured delays, not measured hardware latency])
  })
}


#set document(title: "BlueBoat. 05 sensor timing", author: "J.C. Vaught")
#set page(width: 7.06in, height: auto, margin: 0pt)
#set text(font: "Times New Roman", size: 9pt)
#align(center, sensor-timing())
