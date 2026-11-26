// Operating geometry: vessel-mounted radar observing a buoy over waves.
// Side elevation. Level beam axis and vessel-fixed beam axis share the
// antenna phase center A; the line of sight runs from A to the buoy
// reflector and grazes the last crest before the buoy.
// Standalone figure, 6.5 in wide. Caption is supplied by the manuscript.

#import "@preview/cetz:0.5.2"

// ---------------------------------------------------------------------------
// Editable settings (lengths in cm of drawing space)
// ---------------------------------------------------------------------------
#let fig-width = 6.5in
#let base-size = 9pt

#let garnet = rgb("#73000A")     // vessel-fixed beam axis only
#let water = rgb("#ECECEC")      // 10% black
#let line-w = 0.6pt
#let axis-w = 0.8pt

#let pitch-angle = 10deg         // vessel pitch in the look direction

// Wave profile: crest-sharpened cosine (flat troughs, peaked crests) whose
// amplitude grows from the vessel toward the buoy (a passing wave group).
#let x-min = 0.0
#let x-max = 16.3
#let y-floor = -1.35
#let lam = 7.0                   // wavelength
#let amp-near = 0.42             // amplitude at the vessel
#let amp-far = 0.8               // amplitude at the grazing crest and buoy
#let grow-from = 5.0             // amplitude transition start (x)
#let grow-to = 10.0              // amplitude transition end (x)
#let skew = 0.2                  // second-harmonic ratio (crest sharpening)
#let pivot-x = 2.7               // vessel pivot: mid-slope, bow toward crest
#let x-crest = pivot-x + lam / 4 // crest just ahead of the bow
#let envelope(x) = {
  let u = calc.clamp((x - grow-from) / (grow-to - grow-from), 0.0, 1.0)
  amp-near + (amp-far - amp-near) * u * u * (3 - 2 * u)
}
#let wave(x) = {
  let p = 2 * calc.pi * (x - x-crest) / lam
  envelope(x) * (calc.cos(p) + skew * calc.cos(2 * p))
}

// Vessel: pivot on the free surface, hull rotated bow-up by pitch-angle
#let phase-local = (-0.6, 2.6)   // antenna phase center in vessel frame
#let ant-top-local = (-0.67, 2.9) // top center of antenna aperture in vessel frame

// Buoy sits in the trough behind the grazing crest
#let buoy-x = x-crest + 1.5 * lam
#let refl-r = 0.2                // half-diagonal of reflector

// Axis lengths and label text
#let ref-len = 6.0
#let beam-len = 7.0
#let arc-r = 5.4
#let lbl-ref = [level beam axis]
#let lbl-beam = [vessel-fixed beam axis]
#let lbl-los = [line of sight]
#let lbl-crest = [grazing crest]
#let lbl-radar = [Radar]
#let lbl-buoy = [Buoy]

// ---------------------------------------------------------------------------
// Derived geometry
// ---------------------------------------------------------------------------
#let ct = calc.cos(pitch-angle)
#let st = calc.sin(pitch-angle)
#let P = (pivot-x, wave(pivot-x))
#let to-page(q) = (
  P.at(0) + q.at(0) * ct - q.at(1) * st,
  P.at(1) + q.at(0) * st + q.at(1) * ct,
)
#let A = to-page(phase-local)
#let T = to-page(ant-top-local)

// Line of sight: steepest-upward line from A that still clears the waves
// up to the buoy, so it touches the surface at exactly one crest.
#let n-search = 1400
#let x-lo = A.at(0) + 2.0
#let x-hi = buoy-x
#let slope-at(x) = (wave(x) - A.at(1)) / (x - A.at(0))
#let graze-x = {
  range(n-search + 1)
    .map(i => x-lo + (x-hi - x-lo) * i / n-search)
    .fold(x-lo, (best, x) => if slope-at(x) > slope-at(best) { x } else { best })
}
#let los-slope = slope-at(graze-x)
#let G = (graze-x, wave(graze-x))
#let B = (buoy-x, A.at(1) + los-slope * (buoy-x - A.at(0)))
#let los-y(x) = A.at(1) + los-slope * (x - A.at(0))

// Line of sight stops on the reflector outline (left face of the diamond)
#let los-len = calc.sqrt(1 + los-slope * los-slope)
#let ux = 1 / los-len
#let uy = los-slope / los-len
#let t-face = refl-r / (calc.abs(ux) + calc.abs(uy))
#let E = (B.at(0) - t-face * ux, B.at(1) - t-face * uy)

// ---------------------------------------------------------------------------
// Page and text
// ---------------------------------------------------------------------------
#set page(width: fig-width, height: auto, margin: (x: 0.04in, y: 0.04in), fill: white)
#set text(font: "New Computer Modern", size: base-size, fill: black,
  top-edge: "ascender", bottom-edge: "descender")
#show math.equation: set text(font: "New Computer Modern Math")

#let arrow-mark(c) = (
  end: "stealth", fill: c, scale: 0.75,
  stroke: (paint: c, thickness: 0.4pt, dash: none, join: "miter"),
)
#let sq(pt, s: 0.11) = cetz.draw.rect(
  (pt.at(0) - s / 2, pt.at(1) - s / 2),
  (pt.at(0) + s / 2, pt.at(1) + s / 2),
  fill: black, stroke: none,
)

#align(center, cetz.canvas(length: 1cm, {
  import cetz.draw: *
  set-style(stroke: (paint: black, thickness: line-w, join: "miter", cap: "butt"))

  // --- Sea --------------------------------------------------------------
  let n = 330
  let pts = range(n + 1).map(i => {
    let x = x-min + (x-max - x-min) * i / n
    (x, wave(x))
  })
  line(..pts, (x-max, y-floor), (x-min, y-floor), close: true, fill: water, stroke: none)
  line(..pts)

  // --- Vessel (rigid body rotated by pitch-angle about the pivot) --------
  group({
    set-origin(P)
    rotate(pitch-angle)
    // hull
    line((-2.1, 0.45), (2.0, 0.45), (2.35, 0.72), (1.65, -0.42), (-1.85, -0.42),
      close: true, fill: white)
    // deckhouse
    rect((-1.35, 0.45), (0.15, 1.05), fill: white)
    // mast
    line((-0.66, 1.05), (-0.66, 2.3))
    // antenna aperture; its forward face carries the phase center
    rect((-0.74, 2.3), (-0.6, 2.9), fill: black)
  })

  // --- Buoy ---------------------------------------------------------------
  let wb = wave(buoy-x)
  line((buoy-x, wb + 0.16), (buoy-x, B.at(1) - refl-r))
  rect((buoy-x - 0.3, wb - 0.2), (buoy-x + 0.3, wb + 0.16), fill: white)
  line(
    (buoy-x, B.at(1) - refl-r), (buoy-x + refl-r, B.at(1)),
    (buoy-x, B.at(1) + refl-r), (buoy-x - refl-r, B.at(1)),
    close: true, fill: white,
  )

  // --- Line of sight (straight path, grazes one crest) -------------------
  line(A, E, mark: arrow-mark(black))
  sq(G, s: 0.09)

  // --- Axes from the common phase center --------------------------------
  let R-end = (A.at(0) + ref-len, A.at(1))
  let Bm-end = (A.at(0) + beam-len * ct, A.at(1) + beam-len * st)
  line(A, R-end, stroke: (thickness: axis-w, dash: "dashed"))
  line(A, Bm-end,
    stroke: (paint: garnet, thickness: axis-w, dash: "dashed"),
    mark: arrow-mark(garnet))
  sq(A)

  // --- Pitch angle --------------------------------------------------------
  arc(A, start: 0deg, stop: pitch-angle, radius: arc-r, anchor: "origin",
    mark: arrow-mark(black))
  let th-r = arc-r + 0.18
  content(
    (A.at(0) + th-r * calc.cos(pitch-angle / 2), A.at(1) + th-r * calc.sin(pitch-angle / 2)),
    text(fill: black, $theta$), anchor: "west", padding: 0)

  // --- Labels -------------------------------------------------------------
  content((R-end.at(0) + 0.15, R-end.at(1)), lbl-ref, anchor: "west", padding: 0)
  content((Bm-end.at(0) + 0.15, Bm-end.at(1)), lbl-beam, anchor: "west", padding: 0)
  // line-of-sight labels run parallel to the sloped path, offset along its normal
  let los-angle = calc.atan(los-slope)
  let off(x, d) = (x - d * uy, los-y(x) + d * ux)
  let x-los = A.at(0) + 6.6
  content(off(x-los, -0.12), lbl-los, anchor: "north", angle: los-angle, padding: 0)
  content(off(G.at(0), 0.12), lbl-crest, anchor: "south", angle: los-angle, padding: 0)
  content((T.at(0), T.at(1) + 0.15), lbl-radar, anchor: "south", padding: 0)
  content((B.at(0) + refl-r + 0.15, B.at(1)), lbl-buoy, anchor: "west", padding: 0)
}))
