#import "@preview/cetz:0.4.2": canvas, draw

#set page(width: auto, height: auto, margin: 10pt)

#canvas(length: 1cm, {
  import draw: *

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  //  Mechanism symbol library
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  let ink  = rgb("#363636")
  let _lnk = (paint: ink, thickness: 0.9pt)
  let _jnt = (paint: ink, thickness: 0.7pt)
  let _thin = (paint: ink, thickness: 0.4pt)

  /// Hatched ground / ceiling fixture.
  ///   pos   – centre of the attachment edge
  ///   dir   – "up" hatching rises, "down" hatching falls
  let ground(pos, width: 1.6, depth: 0.3, dir: "up") = {
    let (px, py) = pos
    let s = if dir == "up" { 1 } else { -1 }
    let left = px - width / 2
    let sp = 0.13
    for i in range(int(calc.ceil((width + depth) / sp))) {
      let x0 = left + i * sp
      let x1 = x0 + depth
      let lx = calc.max(x0, left)
      let rx = calc.min(x1, left + width)
      if lx < rx {
        line(
          (lx, py + (lx - x0) * s),
          (rx, py + (depth - (x1 - rx)) * s),
          stroke: _thin,
        )
      }
    }
    line((left, py), (left + width, py), stroke: (paint: ink, thickness: 0.6pt))
  }

  /// Revolute joint – cylinder symbol.
  ///   pos   – geometric centre of the cylinder
  ///   axis  – "z" (vertical) or "x" (horizontal)
  ///   hw/hh – half-width / half-height of the cylinder body
  let revolute(pos, axis: "z", hw: 0.25, hh: 0.425) = {
    let (px, py) = pos
    let er = hw * 0.32
    if axis == "z" {
      rect((px - hw, py - hh), (px + hw, py + hh), stroke: _jnt, fill: white)
      circle((px, py + hh), radius: (hw, er), stroke: _jnt, fill: white)
      circle((px, py - hh), radius: (hw, er), stroke: _jnt, fill: white)
    } else {
      rect((px - hh, py - hw), (px + hh, py + hw), stroke: _jnt, fill: white)
      circle((px - hh, py), radius: (er, hw), stroke: _jnt, fill: white)
      circle((px + hh, py), radius: (er, hw), stroke: _jnt, fill: white)
    }
  }

  /// Prismatic joint – square block with guide rail.
  ///   dir – sliding direction: "x" (horizontal) or "z" (vertical/down)
  ///   rail-side – which side the rail sits on: "left"/"right" or "top"/"bottom"
  ///   rail-gap – distance from box edge to rail line
  let slider(pos, size: 0.30, dir: "x", rail-side: auto, rail-gap: 0.10) = {
    let (px, py) = pos
    let hs = size / 2
    rect((px - hs, py - hs), (px + hs, py + hs), stroke: _jnt, fill: white)
    let ext = hs
    if dir == "x" {
      let side = if rail-side == auto { "right" } else { rail-side }
      let sx = if side == "left" { px - hs - rail-gap } else { px + hs + rail-gap }
      line((sx, py - ext), (sx, py + ext), stroke: _jnt)
    } else {
      let side = if rail-side == auto { "bottom" } else { rail-side }
      let sy = if side == "top" { py + hs + rail-gap } else { py - hs - rail-gap }
      line((px - ext, sy), (px + ext, sy), stroke: _jnt)
    }
  }

  /// Compound joint: revolute cylinder seated in a prismatic housing.
  let revolute-in-housing(pos, axis: "z",
      housing: 0.35, cw: 0.22, ch: 0.38) = {
    let (px, py) = pos
    rect((px - housing, py - housing), (px + housing, py + housing),
         stroke: _jnt, fill: white)
    if axis == "z" {
      let top = py + ch
      let bot = py - ch + 0.13
      line((px - cw, top), (px - cw, bot), stroke: _jnt)
      line((px + cw, top), (px + cw, bot), stroke: _jnt)
      circle((px, top), radius: (cw, 0.07), stroke: _jnt, fill: white)
      circle((px, bot), radius: (cw, 0.07), stroke: _jnt, fill: white)
    }
  }

  /// Rigid link – straight line.
  let rigid-link(from, to) = {
    line(from, to, stroke: _lnk)
  }

  /// End-effector plate.
  let end-plate(pos, width: 0.7, dir: "x") = {
    let (px, py) = pos
    let hw = width / 2
    if dir == "x" {
      line((px - hw, py), (px + hw, py), stroke: _lnk)
    } else {
      line((px, py - hw), (px, py + hw), stroke: _lnk)
    }
  }

  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  //  Robot definition — change constants, everything reflows
  // ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  let L1  = 3.2
  let L2  = 3.5
  let d2v = 1.75
  let L3  = 2.05
  let d4v = 0.85

  // Joint symbol sizes (must match library defaults if you
  // want anchor arithmetic to stay correct)
  let cyl-hh  = 0.425
  let housing = 0.35

  // ── Derived positions ──
  let ceiling  = (0, 0)
  let j1       = (0, -cyl-hh)                          // joint 1 centre
  let j1-bot   = (0, -2 * cyl-hh)                      // bottom of joint 1 cylinder
  let elbow    = (0, -L1)                               // 90° bend
  let act      = (L2 * 0.5, -L1)                        // prismatic actuator on L2
  let j3       = (L2 + d2v, -L1)                        // joint 3 centre
  let j3-right = (L2 + d2v + housing, -L1)              // right edge of J3 housing
  let j4       = (L2 + d2v + L3, -L1)                   // joint 4 mount
  let ee       = (L2 + d2v + L3, -L1 - d4v)             // end-effector tip

  // ── Draw links first (behind joint symbols) ──
  rigid-link(j1-bot, elbow)              // L1 vertical
  rigid-link(elbow, (j3.at(0) + housing, j3.at(1)))  // horizontal through to J3
  rigid-link(j3-right, j4)              // L3
  rigid-link(j4, ee)                    // d4 shaft

  // ── Draw joint symbols on top ──
  ground(ceiling)                        // ceiling fixture
  revolute(j1, axis: "z")               // θ₁
  slider(act, dir: "x", rail-side: "right") // d₂ prismatic actuator (slides horizontal)
  revolute-in-housing(j3, axis: "z")     // θ₃ inside d₂ housing
  slider(j4, dir: "z")                    // d₄ prismatic mount (slides vertical/down)
  end-plate(ee)                          // gripper / end plate
})
