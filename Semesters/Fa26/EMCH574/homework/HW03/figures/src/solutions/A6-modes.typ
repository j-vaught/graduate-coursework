#import "/typst-figures/styles/figure.typ": *
#let d = json("data/A6.json")
#let kind = "modes"
#let xs = if kind == "modes" { d.x } else if kind == "frf" { d.f } else { d.t }
#let ys = if kind == "modes" { d.modes } else if kind == "frf" { d.ys } else { (d.response,) }
#book-layout[
  #standalone[
    #book-diagram(size: "full", height: 65mm,
      xlabel: if kind == "modes" { [Position (x/L)] } else if kind == "frf" { [Frequency (Hz)] } else { [Time / period] },
      ylabel: if kind == "modes" { [Displacement] } else if kind == "frf" { [FRF (dB re 1 m/N)] } else { [Normalized displacement] },
      xlim: if kind == "modes" { (0,1) } else if kind == "frf" { (20,2000) } else { (0,3) },
      legend: if kind == "frf" { (position: top + right) } else { none },
      ..ys.enumerate().map(pair => {
        let (i,y) = pair
        plot(xs,y,stroke:(paint:plot-color-cycle.at(calc.rem(i,plot-color-cycle.len())),thickness:0.8pt),
          label: if kind == "frf" { ("(a)", "(b)", "(c)").at(i) } else { none })
      }))
  ]
]
