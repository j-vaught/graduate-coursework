// ═══════════════════════════════════════════════════════════════════════
// Style sandbox: mirrors the preamble of report.typ so we can iterate
// on heading / layout styling without risking the real report.
//
// Compile with:   ~/bin/typst compile report/style_test.typ report/style_test.pdf
// ═══════════════════════════════════════════════════════════════════════

// ── Brand palette ─────────────────────────────────────────────────────
#let garnet    = rgb("#73000A")
#let black     = rgb("#000000")
#let black-90  = rgb("#363636")
#let black-70  = rgb("#5C5C5C")
#let black-50  = rgb("#A2A2A2")
#let black-30  = rgb("#C7C7C7")
#let black-10  = rgb("#ECECEC")
#let warm-grey = rgb("#676156")
#let sandstorm = rgb("#FFF2E3")
#let rose      = rgb("#CC2E40")
#let atlantic  = rgb("#466A9F")
#let congaree  = rgb("#1F414D")
#let horseshoe = rgb("#65780B")
#let honeycomb = rgb("#A49137")

// ── Document setup (same as report.typ) ──────────────────────────────
#set document(title: "Style Test", author: "style-sandbox")

#set heading(numbering: "1.")

#set page(
  paper: "us-letter",
  margin: (top: 0.9in, bottom: 1in, x: 0.85in),
  numbering: "1 / 1",
  number-align: center,
  footer: context [
    #set text(size: 8pt, fill: black-70)
    #grid(
      columns: (1fr, auto, 1fr),
      align: (left, center, right),
      [Style Sandbox],
      counter(page).display("1 / 1", both: true),
      [DRAFT],
    )
  ],
)

#set text(
  font: ("New Computer Modern", "Latin Modern Roman", "STIX Two Text", "Times New Roman"),
  size: 10pt,
  lang: "en",
  hyphenate: true,
)

#set par(justify: true, leading: 0.55em, first-line-indent: 0pt)

// ─────────────────────────────────────────────────────────────────────
// HEADING STYLES (the focus of this sandbox — tweak these freely)
// ─────────────────────────────────────────────────────────────────────
// Tightened heading styles — pulls the underline close to the title text
// and reduces the gap before body copy.
#show heading.where(level: 1): it => {
  set text(fill: garnet, size: 12pt, weight: "bold")
  set block(above: 0.7em, below: 0.5em)
  block[
    #smallcaps(it.body)
    #v(-6pt)            // small absolute gap under title, before rule
    #line(length: 100%, stroke: 1pt + garnet)
  ]
}
#show heading.where(level: 2): it => {
  set text(fill: black-90, size: 10.5pt, weight: "bold")
  block(above: 0.7em, below: 0.3em)[#it.body]
}
#show heading.where(level: 3): it => {
  set text(fill: black-90, size: 10pt, weight: "semibold", style: "italic")
  block(above: 0.7em, below: 0.3em)[#it.body]
}

// ── Link / ref / caption styles (mirror report.typ) ──────────────────
#show link: it => text(fill: atlantic)[#it]
#show ref: it => text(fill: garnet, weight: "semibold")[#it]
#show figure.caption: it => {
  set text(size: 9pt, fill: black-70)
  block(above: 0.35em)[
    #text(fill: garnet, weight: "bold")[#it.supplement #it.counter.display()#it.separator]
    #it.body
  ]
}
#set table(
  stroke: (_, y) => {
    if y == 0 { (bottom: 0.8pt + black, top: 0.8pt + black) }
    else { (bottom: 0.3pt + black-50) }
  },
  inset: 6pt,
)

// ── Title block ──────────────────────────────────────────────────────
#align(center)[
  #block(width: 100%, inset: (y: 0.4em))[
    #text(size: 17pt, weight: "bold", fill: black)[
      Heading & Layout Style Sandbox
    ]
  ]
  #v(0.3em)
  #text(size: 10pt, fill: black-70, style: "italic")[
    Lorem ipsum stress test for #emph[report.typ] — edit me, never the real thing.
  ]
]

#v(0.4em)
#line(length: 100%, stroke: 0.4pt + black-50)
#v(0.2em)

// ── Abstract callout ─────────────────────────────────────────────────
#block(
  fill: sandstorm,
  stroke: (left: 2pt + garnet),
  inset: (x: 14pt, y: 10pt),
  width: 100%,
)[
  #text(weight: "bold", size: 9.5pt, fill: garnet)[ABSTRACT.]
  #text(size: 9.5pt)[
    Lorem ipsum dolor sit amet, consectetur adipiscing elit.  Integer nec
    odio.  Praesent libero.  Sed cursus ante dapibus diam.  Sed nisi.
    Nulla quis sem at nibh elementum imperdiet.  Duis sagittis ipsum.
    Praesent mauris.  Fusce nec tellus sed augue semper porta.  Mauris
    massa.  Vestibulum lacinia arcu eget nulla.  Class aptent taciti
    sociosqu ad litora torquent per conubia nostra, per inceptos
    himenaeos.
  ]
]

#v(0.6em)

// ── Two-column body starts here ──────────────────────────────────────
#show: rest => columns(2, gutter: 18pt, rest)

// ═══════════════════════════════════════════════════════════════════════
// Level-1, level-2, level-3 showcase
// ═══════════════════════════════════════════════════════════════════════

= Introduction

Lorem ipsum dolor sit amet, consectetur adipiscing elit.  Quisque
vitae urna eget nisl cursus aliquet.  Vivamus hendrerit mauris vel
augue dapibus, sit amet fermentum lectus egestas.  Aenean pulvinar
tempor risus, id tempor est tincidunt vitae.  Curabitur posuere, mi at
semper ornare, arcu nunc pharetra urna, ac pulvinar magna ex eget
metus.  In hac habitasse platea dictumst.  Phasellus lacinia, dui a
viverra placerat, dolor ligula laoreet justo, sed hendrerit urna
ipsum in turpis.

Vestibulum ante ipsum primis in faucibus orci luctus et ultrices
posuere cubilia curae.  Proin dignissim lacus eget est viverra, eu
bibendum sem sodales.  Aliquam erat volutpat.  Nulla facilisi.  Donec
pharetra tincidunt mauris, a fringilla augue porta et.

== First Subsection

Nulla facilisi.  Nunc tincidunt semper lectus, eu vehicula mi
consectetur ut.  Morbi varius pulvinar eleifend.  Aliquam consequat
tortor id elit ultrices aliquam.  Etiam vitae felis non nulla
elementum convallis non nec tellus.

=== A Level-3 Heading

Cras ornare turpis eu sapien vestibulum, in feugiat lorem mollis.
Proin bibendum nec augue eu venenatis.  Integer luctus massa quis
nunc interdum, vitae lobortis quam efficitur.

== Second Subsection

Phasellus ac leo quis enim tincidunt rutrum a vitae nisi.  Sed ex mi,
feugiat vel est sed, maximus scelerisque velit.  Curabitur porta
efficitur gravida.  Integer tincidunt ligula eu ex sagittis, in
interdum sapien faucibus.

=== Another Level-3

Maecenas luctus imperdiet arcu, a lacinia sapien sollicitudin ut.
Ut sit amet sodales dui.  Aliquam mauris lorem, rhoncus vel viverra
ut, efficitur ut augue.

= Methods

Fusce vitae nibh sit amet nibh sagittis vestibulum.  Nunc elementum
nunc nibh, eget fermentum lacus pharetra id.  Vivamus vitae mattis
lectus, sed aliquet neque.  Nullam ut consequat lorem, id pharetra
lacus.  Sed ut sem ut nisi posuere egestas.

== Dataset

Suspendisse euismod viverra sollicitudin.  Vestibulum ante ipsum
primis in faucibus orci luctus et ultrices posuere cubilia curae.
Pellentesque ornare consequat velit sit amet aliquam.

=== Calibration

Fusce ac arcu lacus.  Mauris interdum eros quis purus sodales
convallis.  Aliquam vitae ex justo.  Suspendisse potenti.  Sed ac
convallis turpis, a sagittis nisl.  Praesent in lorem metus.

=== Splits

Cras ut magna vitae sem euismod vulputate.  Donec dictum turpis in
purus sollicitudin, eu fermentum quam aliquam.  Vestibulum ac
vestibulum ante.  Duis tempus turpis at est fermentum sagittis.

== Training Setup

Cras ultrices lectus et dolor maximus convallis.  Aenean non lectus
ac arcu aliquet efficitur.  Sed elementum, justo ut laoreet
condimentum, ex ante volutpat elit, in egestas sem quam at metus.

= Results

Curabitur fermentum odio nec lacus ultrices, a rutrum sem
consectetur.  Nunc commodo posuere quam id luctus.  In non elit
neque.  Nam dignissim nisl in augue cursus, sit amet condimentum ex
dictum.

#figure(
  placement: top,
  scope: "parent",
  kind: table,
  caption: [
    *Dummy results table.*  Lorem ipsum columns for style stress-testing.
    Bigger values are *bold* to verify emphasis renders well inside cells.
  ],
  table(
    columns: (2fr, 1fr, 1.4fr, 1.4fr, 1.6fr, 1.4fr, 1.3fr),
    align: (left, left, right, right, right, right, right),
    table.header[*Method*][*Type*][*AP\@0.50*][*AP\@0.75*][*AP\@[.50:.95]*][*AR\@100*][*Preds*],
    [Foo-Net],       [DL (×3)],   [*0.812 #text(size:7.5pt, fill: black-70)[±0.02]*],
                                   [0.750], [0.611], [0.812], [28,000],
    [Bar-R-CNN],     [DL (×3)],   [0.731], [0.701], [0.605], [0.840], [199,000],
    [Baz-Former],    [DL (×3)],   [0.545], [0.533], [0.422], [0.456], [4,523],
    [Morph-Baseline],[Classical], [0.537], [0.315], [0.311], [0.661], [4,289],
    [Otsu-Baseline], [Classical], [0.534], [0.338], [0.318], [0.676], [4,663],
  ),
) <tab:dummy>

== Headline Numbers

Donec et velit vitae ipsum luctus rutrum.  Etiam in viverra lorem.
Mauris vel suscipit elit.  Sed mollis lacinia metus.  @tab:dummy shows
the ranking.

=== Precision

Nulla euismod magna sit amet metus bibendum, non tempus urna ornare.
Aliquam erat volutpat.  Ut elementum, mauris et posuere viverra,
turpis dui ornare nisi, a cursus augue risus sit amet velit.

=== Recall

Pellentesque habitant morbi tristique senectus et netus et malesuada
fames ac turpis egestas.  Mauris eleifend, metus id rhoncus
venenatis, leo massa lacinia ligula, a ullamcorper quam urna sed
metus.

== Seed Stability

Curabitur condimentum, ligula in cursus rhoncus, nibh ipsum
porttitor ex, a aliquam erat nibh nec urna.  Nam a venenatis justo.

= Discussion

Ut fermentum erat nec ante dictum, ac dictum lectus pretium.  Aenean
lacinia tellus sit amet erat tristique, ac aliquet est tempus.
Phasellus eu consequat dui.

== What Went Well

Integer at suscipit est.  Suspendisse sed ornare elit.  Pellentesque
tempor risus leo, at pretium velit fringilla vitae.

== Limitations

Aenean euismod porttitor sapien.  Integer non porta erat.
Pellentesque vel sollicitudin libero.

=== Data Quality

Morbi scelerisque lacus non leo aliquet, a imperdiet lectus dignissim.
Nunc feugiat lorem neque, quis condimentum massa ultricies sit amet.

=== Compute

Fusce sed lorem sodales, hendrerit enim a, rutrum velit.  In viverra
elementum leo, a dictum elit dapibus in.

= Conclusion

Proin id eleifend felis.  Aliquam erat volutpat.  Phasellus sed metus
ut nibh interdum convallis vitae sit amet tortor.  Praesent at
pharetra tellus.  Donec eu diam id mi commodo tristique.  Sed in
nunc eget dui malesuada malesuada ac vitae lorem.

#heading(level: 1, numbering: none)[References]

#set text(size: 8.8pt)
#set par(justify: true, leading: 0.5em, first-line-indent: 0pt)

#enum(
  numbering: "[1]",
  indent: 0pt,
  body-indent: 0.7em,
  spacing: 0.35em,
  [A. Author, "Dummy reference one," _Journal_, vol. 1, 2024.],
  [B. Author, "Dummy reference two," _Proc. Conf._, 2025.],
  [C. Author, "Dummy reference three with a longer title for wrap
   testing," _Transactions_, vol. 42, 2026.],
)
