#set page(paper: "us-letter", flipped: true, margin: (x: 0.55in, y: 0.43in),
  footer: context [#set text(size: 9pt); J.C. Vaught #h(1fr) EMCH 574 · Homework 03 #h(1fr) #counter(page).display() / #counter(page).final().first()])
#set text(font: "New Computer Modern", size: 12pt)
#set document(title: "Homework 03 figure comparison", author: "J.C. Vaught")
#let pair(number, title, note, before, after) = block(width: 100%)[
  #line(length: 100%, stroke: 0.55pt)
  #v(2pt)
  #text(size: 15pt, weight: "bold")[#number #h(5pt) #title]
  #v(2pt)
  #grid(columns: (1fr, 1fr), gutter: 20pt,
    [#text(size: 10pt)[Original assignment] #v(1pt)
     #image(before, width: 100%, height: 1.22in, fit: "contain")],
    [#text(size: 10pt)[HW01-style redraw] #v(1pt)
     #image(after, width: 100%, height: 1.22in, fit: "contain")])
  #v(3pt)
  #note
]
#let heading(title) = [
  #text(size: 11pt)[EMCH 574 / Homework 03 figure comparison]
  #v(2pt)
  #text(size: 23pt, weight: "bold")[#title]
  #v(6pt)
]
#heading[Transverse string vibration]
#pair("A.2", "Taut string", [Equal outward tensions act at the two pins. The displaced string returns to the reference line at both ends.], "../extracted-001.png", "../generated/a2.pdf")
#v(10pt)
#pair("A.5", "Plucked string", [The pluck sets the peak displacement at distance $d$ from the left pin. Two straight segments define the initial shape.], "../extracted-003.png", "../generated/a5.pdf")
#pagebreak()
#heading[Cantilever vibration]
#pair("B.2", "Uniform cantilever", [The wall and span follow HW01’s cantilever drawings. Here the free end at $x=L$ carries no attached mass.], "../extracted-007.png", "../generated/b2.pdf")
#v(10pt)
#pair("B.5", "Plucked reed", [The same clamped support anchors the reed. The tip arrow specifies the initial displacement $w_"max"$.], "../extracted-011.png", "../generated/b5.pdf")
#v(4pt)
#grid(columns: (1.8in, 1fr), gutter: 8pt, align: horizon,
  image("/HW01/figures/generated/fig_pC2.pdf", width: 100%),
  text(size: 10pt)[HW01 reference · C.2 and C.6 use the same tip-mass cantilever drawing. The HW03 beam and reed share its clamped support and span geometry.])
#pagebreak()
#heading[Axial vibration of slender bars]
#pair("C.6", "Wave motion in a uniform bar", [The arrow shows axial displacement $u(x,t)$ along the bar. The cross-sectional area $A$, density $rho$, and elastic modulus $E$ are uniform.], "../extracted-014.png", "../generated/c6.pdf")
#v(10pt)
#pair("C.9", "Finite bar with two free ends", [The bar extends from $x=0$ to $x=L$. Both ends are free, and $c$ denotes the axial wave speed.], "../extracted-016.png", "../generated/c9.pdf")
