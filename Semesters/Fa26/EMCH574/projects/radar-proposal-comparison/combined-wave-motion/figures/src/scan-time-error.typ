#import "@preview/cetz:0.5.2" as cetz

#set page(width: 6.5in, height: 3.0in, margin: 0pt)
#set text(font: "Latin Modern Roman", size: 10pt, fill: black)
#show math.equation: set text(font: "Latin Modern Math")

#let arrow = (end: "stealth", fill: black, length: 2.4mm, width: 1.5mm)
#let p-ray = (26, 24)
#let p-mid = (68, 24)
#let r-meas = (70, 32)
#let x-true = (p-ray.at(0) + r-meas.at(0), p-ray.at(1) + r-meas.at(1))
#let x-recon = (p-mid.at(0) + r-meas.at(0), p-mid.at(1) + r-meas.at(1))

#align(center + horizon)[
  #cetz.canvas(length: 1mm, {
    import cetz.draw: *

    rect((0, 0), (165, 76), fill: white, stroke: none)
    content((5, 71), anchor: "west", text(size: 9pt, style: "italic")[Plan view, $t_i < t_"mid"$])

    // Identical measured range-bearing vectors from the two mapping origins.
    line(p-ray, x-true, stroke: 1.15pt, mark: arrow)
    line(p-mid, x-recon, stroke: (paint: black, thickness: 1pt, dash: "dashed"), mark: arrow)
    content((61, 46), [$bold(r)_i (rho_i, alpha_i)$])
    content((107, 35), [same $bold(r)_i$])

    // Actual acquisition pose and the pose incorrectly assigned at scan midpoint.
    rect((p-ray.at(0) - 3, p-ray.at(1) - 3), (p-ray.at(0) + 3, p-ray.at(1) + 3), fill: black, stroke: 1pt)
    rect((p-mid.at(0) - 3, p-mid.at(1) - 3), (p-mid.at(0) + 3, p-mid.at(1) + 3), fill: white, stroke: 1pt)
    line((p-ray.at(0) - 4, 31), (p-ray.at(0) + 8, 31), stroke: 0.9pt, mark: arrow)
    line((p-mid.at(0) - 4, 31), (p-mid.at(0) + 8, 31), stroke: 0.9pt, mark: arrow)
    content((47, 28), [same heading])
    content((26, 5), [Actual pose $bold(p)(t_i)$])
    content((68, 5), [Assumed pose $bold(p)(t_"mid")$])

    // Platform translation used by the midpoint approximation.
    line((p-ray.at(0), 19), (p-ray.at(0), 15), stroke: 0.7pt)
    line((p-mid.at(0), 19), (p-mid.at(0), 15), stroke: 0.7pt)
    line((p-ray.at(0), 16), (p-mid.at(0), 16), stroke: 1pt, mark: arrow)
    content((47, 11), [$bold(Delta p)_i = bold(p)(t_"mid") - bold(p)(t_i)$])

    // One physical target and its location reconstructed with the wrong origin.
    rect((x-true.at(0) - 3, x-true.at(1) - 3), (x-true.at(0) + 3, x-true.at(1) + 3), fill: black, stroke: 1pt)
    rect((x-recon.at(0) - 3, x-recon.at(1) - 3), (x-recon.at(0) + 3, x-recon.at(1) + 3), fill: white, stroke: 1pt)
    line((x-recon.at(0) - 2, x-recon.at(1) - 2), (x-recon.at(0) + 2, x-recon.at(1) + 2), stroke: 0.7pt)
    line((x-recon.at(0) - 2, x-recon.at(1) + 2), (x-recon.at(0) + 2, x-recon.at(1) - 2), stroke: 0.7pt)
    content((96, 47), text(size: 9pt)[True target $bold(x)_i$])
    content((138, 47), text(size: 9pt)[Reconstructed point $hat(bold(x))_i$])

    // Reconstruction error equals the sensor translation vector.
    line((x-true.at(0), 60), (x-true.at(0), 65), stroke: 0.7pt)
    line((x-recon.at(0), 60), (x-recon.at(0), 65), stroke: 0.7pt)
    line((x-true.at(0), 64), (x-recon.at(0), 64), stroke: 1pt, mark: arrow)
    content((117, 69), [$E_h = norm(bold(Delta p)_i) = U abs(t_i - t_"mid")$])
  })
]
