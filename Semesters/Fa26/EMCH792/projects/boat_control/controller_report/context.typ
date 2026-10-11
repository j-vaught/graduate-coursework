#let d = json("data/design.json")
#let summary = json("data/summary.json")
#let traces = json("data/traces.json")
#let methods = ("pid", "lqr", "pole_placement")
#let names = ("PID", "LQR + integral", "Pole placement + integral")
#let pretty(x, digits: 3) = if x == none { [Not settled] } else { str(calc.round(x, digits: digits)) }
#let aggregate(case, method, metric) = summary.aggregate.find(r => r.case == case and r.method == method).metrics.at(metric)
