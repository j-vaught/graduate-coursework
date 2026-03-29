// ======================================================================
// RL-Based Prompt Optimization for SAM — Comprehensive Technical Analysis
// Typst main document
// ======================================================================

#set document(
  title: "RL-Based Prompt Optimization for the Segment Anything Model: A Comprehensive Technical Analysis",
  author: "J.C. Vaught",
  date: datetime(year: 2026, month: 3, day: 28),
)

// ── Page & text ──────────────────────────────────────────────────────
#set page(paper: "us-letter", margin: 0.75in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true)

// No indent, extra spacing between paragraphs
#set par(first-line-indent: 0pt, spacing: 1.2em, leading: 0.65em)

// Headings
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  pagebreak(weak: true)
  v(0.5em)
  text(size: 14pt, weight: "bold", it)
  v(0.4em)
}
#show heading.where(level: 2): it => {
  v(0.6em)
  text(size: 12pt, weight: "bold", it)
  v(0.3em)
}
#show heading.where(level: 3): it => {
  v(0.4em)
  text(size: 11pt, weight: "bold", it)
  v(0.2em)
}

// Numbered equations
#set math.equation(numbering: "(1)")

// Brand colors
#let garnet = rgb("#73000A")
#let atlantic = rgb("#466A9F")
#let congaree = rgb("#1F414D")
#let horseshoe = rgb("#65780B")
#let rose = rgb("#CC2E40")
#let honeycomb = rgb("#A49137")

// Links & refs styled
#show link: set text(fill: atlantic)
#show ref: set text(fill: garnet)

// Figures
#set figure(gap: 0.8em)
#show figure.caption: set text(size: 10pt)

// Tables
#set table(stroke: none, align: left)

// ── Title page ───────────────────────────────────────────────────────
#v(3em)
#align(center)[
  #text(size: 18pt, weight: "bold")[
    RL-Based Prompt Optimization for SAM:\
    A Comprehensive Technical Analysis
  ]
  #v(0.2em)
  #text(size: 13pt)[J.C. Vaught; Xeerak Muhammed; Jacob Whisenant]
  #v(0.3em)
  #text(size: 11pt, fill: luma(100))[March 2026]
]

#v(2em)

// ── Abstract ─────────────────────────────────────────────────────────
#include "sections/abstract.typ"

// ── Table of Contents ────────────────────────────────────────────────
#pagebreak()
//#outline(indent: 1.5em, depth: 3) //un-comment this before sending to Agostinelli

// ── Sections ─────────────────────────────────────────────────────────
#include "sections/introduction.typ"
#include "sections/related-work.typ"
#include "sections/ppo-framework.typ"
#include "sections/qlearning.typ"
#include "sections/dataset.typ"
#include "sections/v1.typ"
#include "sections/v2.typ"
#include "sections/v3.typ"
#include "sections/results.typ"
#include "sections/discussion.typ"
#include "sections/engineering.typ"
#include "sections/conclusion.typ"

// ── Bibliography ─────────────────────────────────────────────────────
#pagebreak()
#bibliography("references.bib", style: "ieee")
