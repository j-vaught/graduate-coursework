#import "@preview/cetz:0.3.4"
#import "@preview/fancy-tiling:1.0.0": *

// --- Page & text ---
#let page-margin = 10pt
#let text-size = 10pt

// --- Scale factor (multiply all CeTZ coordinates by this) ---
#let fig-scale = 1.2

// --- Stroke widths ---
#let box-stroke = 1.0pt
#let arrow-stroke = 1.0pt
#let divider-stroke = 1.0pt
#let hatch-thickness = 0.2pt

// --- Colors ---
#let hatch-color = luma(180)
#let divider-color = luma(180)

// --- Arrow config ---
#let arrow-end = "stealth"
#let arrow-fill = black
#let arrow-mark-scale = 1.3

// --- Derived styles ---
#let hatch-fill = diagonal-stripes(size: 5pt, angle: 45deg, mirror: true, thickness: hatch-thickness, stripe-color: hatch-color, background-color: white)
#let box-style = (stroke: box-stroke + black, fill: white)
#let model-style = (stroke: box-stroke + black, fill: hatch-fill)
#let arrow-style = (stroke: arrow-stroke + black, mark: (end: arrow-end, fill: arrow-fill, scale: arrow-mark-scale))
#let line-style = (stroke: arrow-stroke + black)
#let divider-style = (stroke: divider-stroke + divider-color)

// --- Helpers ---
#let cm-to-pt(cm) = cm * 28.35pt
#let model-label(body) = align(center, strong(body))
