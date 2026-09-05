// Semantic, color-blind-safe figure palette.
// Keep literal color definitions in this file so the palette can be changed
// without editing individual figures.

#let homework-palette = sys.inputs.at("palette", default: "reference") == "homework"
#let color-garnet-rose = if homework-palette { rgb("#0072b2") } else { rgb("#8b3a4a") }
#let color-deep-teal = if homework-palette { rgb("#0072b2") } else { rgb("#005f73") }
#let color-graphite = rgb("#25282a")
#let color-slate = rgb("#50565b")
#let color-cool-grey = rgb("#7b858c")
#let color-brass = if homework-palette { rgb("#d55e00") } else { rgb("#a49137") }

#let color-ink = color-graphite
#let color-muted = color-slate
#let color-primary = color-garnet-rose
#let color-secondary = color-deep-teal
#let color-tertiary = color-brass
#let color-accent = color-graphite
#let color-gold = color-slate
#let color-cyan = color-cool-grey
#let color-yellow = rgb("#f0e442")

#let color-background = rgb("#ffffff")
#let color-on-light = rgb("#000000")
#let color-surface = rgb("#f6f6f5")
#let color-surface-strong = rgb("#e8e9e9")
#let color-guide = color-cool-grey
#let color-grid = rgb("#d8dbdc")
#let color-border = color-slate

#let color-input = color-primary
#let color-output = color-secondary
#let color-feedback = color-tertiary
#let color-force = color-secondary
#let color-displacement = color-secondary
#let color-mechanical = color-ink

#let plot-color-cycle = if homework-palette {
  (rgb("#0072b2"), rgb("#d55e00"), color-graphite, rgb("#009e73"), color-slate, color-cool-grey)
} else { (
  color-garnet-rose,
  color-deep-teal,
  color-graphite,
  color-brass,
  color-slate,
  color-cool-grey,
) }
