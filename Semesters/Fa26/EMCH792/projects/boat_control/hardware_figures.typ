#import "@preview/lilaq:0.6.0" as lq
#import "@preview/cetz:0.4.2" as cetz
#let garnet = rgb("#73000A")
#let cr = json("data/component_runs.json")
#let sensors = json("data/component_sensors.json")
#let arrow = (end: "stealth", fill: black, stroke: black)
#let hull() = {
  set text(size: 9.5pt)
  cetz.canvas(length: 0.95cm, {
    import cetz.draw: *
    let dimension = (start: "stealth", end: "stealth", fill: black, stroke: black)
    let tag(pos, number) = {
      rect((pos.at(0) - 0.23, pos.at(1) - 0.23), (pos.at(0) + 0.23, pos.at(1) + 0.23), fill: white, stroke: 0.8pt)
      content(pos, [#number])
    }
    // Bow to the right; the envelope retains the published aspect ratio.
    line((0, 0), (7.35, 0), (8, 0.6), (7.35, 1.2), (0, 1.2), close: true, fill: luma(94%), stroke: 0.85pt)
    line((0, 5), (7.35, 5), (8, 5.6), (7.35, 6.2), (0, 6.2), close: true, fill: luma(94%), stroke: 0.85pt)
    rect((1.75, 1.2), (2.1, 5), fill: luma(85%), stroke: 0.65pt)
    rect((6.5, 1.2), (6.85, 5), fill: luma(85%), stroke: 0.65pt)
    content((8.5, 3.1), [BOW])
    content((-0.45, 3.1), angle: 90deg, [STERN])
    content((5.2, 5.6), [PORT])
    content((5.2, 0.6), [STARBOARD])

    rect((4.9, 2.15), (6.25, 4.05), fill: white, stroke: 0.8pt)
    tag((5.58, 3.1), 1)
    line((2.96, 3.1), (3.24, 3.1), stroke: 1pt)
    line((3.1, 2.96), (3.1, 3.24), stroke: 1pt)
    content((3.62, 3.1), [$O$])

    // Number each thruster in its footprint; both positive forces point forward.
    for (n, y, force) in ((2, 5.6, $T_L$), (3, 0.6, $T_R$)) {
      rect((0.05, y - 0.27), (0.55, y + 0.27), fill: garnet, stroke: black)
      content((0.3, y), text(fill: white)[#n])
      line((0.55, y), (2.5, y), mark: arrow, stroke: 1.1pt)
      content((3.05, y), force)
    }

    line((0, 7.05), (8, 7.05), mark: dimension, stroke: 0.65pt)
    line((0, 6.3), (0, 7.25), stroke: 0.45pt + luma(45%))
    line((8, 6.3), (8, 7.25), stroke: 0.45pt + luma(45%))
    content((4, 7.45), [Length 1.20 m])
    line((9.05, 0), (9.05, 6.2), mark: dimension, stroke: 0.65pt)
    line((8.1, 0), (9.25, 0), stroke: 0.45pt + luma(45%))
    line((8.1, 6.2), (9.25, 6.2), stroke: 0.45pt + luma(45%))
    content((9.65, 3.1), angle: 90deg, [Beam 0.93 m])
    line((-1.15, 0.6), (-1.15, 5.6), mark: dimension, stroke: 0.65pt)
    line((-1.35, 0.6), (-0.75, 0.6), stroke: 0.45pt + luma(45%))
    line((-1.35, 5.6), (-0.75, 5.6), stroke: 0.45pt + luma(45%))
    content((-1.75, 3.1), angle: 90deg, [$B$ · thrust-line separation])

    // Three entries run across the bottom, with no coordinate-frame panel.
    content((4, -0.8), [Equipment key])
    for (n, x, body) in (
      (1, -0.1, [Computer and#linebreak()sensors]),
      (2, 3.8, [Port thruster#linebreak()M200, $T_L$]),
      (3, 7.3, [Starboard thruster#linebreak()M200, $T_R$]),
    ) {
      tag((x, -1.65), n)
      content((x + 0.6, -1.65), anchor: "west", body)
    }
  })
}

#let feedback() = {
  set text(size: 8.5pt)
  cetz.canvas(length: 0.80cm, {
    import cetz.draw: *
    let box(a, b, body, fill: white) = {
      rect(a, b, fill: fill, stroke: 0.8pt)
      content(((a.at(0) + b.at(0))/2, (a.at(1) + b.at(1))/2), body)
    }
    box((0, 4), (3.6, 6.1), [Mission input#linebreak()waypoints, task#linebreak()target identity])
    box((5, 4), (11, 6.1), [AGX Orin#linebreak()perception + state fusion#linebreak()guidance], fill: luma(95%))
    box((13, 4), (19, 6.1), [Pi 4 / Navigator#linebreak()ArduRover#linebreak()speed / yaw-rate loops])
    box((13, 0), (19, 2), [ESCs + M200 motors#linebreak()PWM → actual thrust#linebreak()$T_L$, $T_R$])
    box((7, 0), (11, 2), [Boat dynamics#linebreak()$x,y,psi,u,v,r$])
    box((0, 0), (5.5, 2), [mosaic-H + VN-110#linebreak()ZED X#linebreak()timestamped measurements])
    line((3.6, 5.1), (5, 5.1), mark: arrow)
    line((11, 5.1), (13, 5.1), mark: arrow)
    content((12, 5.8), [$u_d,r_d$])
    line((16, 4), (16, 2), mark: arrow)
    content((17.6, 3), [PWM#linebreak()µs])
    line((13, 1), (11, 1), mark: arrow)
    content((12, 1.7), [Forces])
    line((7, 1), (5.5, 1), mark: arrow)
    content((6.25, 1.7), [Motion])
    line((2.75, 2), (2.75, 3), (8, 3), (8, 4), mark: arrow)
    content((5.7, 3.35), [Measurements, status, time])
    box((0, -3.0), (5.5, -1.1), [Local RTK base#linebreak()operating tent])
    line((2.75, -1.1), (2.75, 0), mark: arrow)
    content((1.55, -0.55), [RTCM])
    box((13, -3.0), (19, -1.1), [Physical / wireless kill#linebreak()independent power cut], fill: luma(95%))
    line((16, -1.1), (16, 0), mark: arrow)
    content((17.5, -0.55), [Enable])
    box((7, -3.0), (11, -1.1), [Scene / targets])
    line((9, -1.1), (9, -0.5), (4.5, -0.5), (4.5, 0), mark: arrow)
    line((9.5, 2.7), (9.5, 2), mark: arrow)
    content((10.7, 2.7), [Wind / waves])
  })
}
#let lowlevel() = {
  set text(size: 8.5pt)
  cetz.canvas(length: 0.8cm, {
    import cetz.draw: *
    let box(x, y, w, body, fill: white) = {
      rect((x, y), (x+w, y+1.6), fill: fill, stroke: 0.8pt)
      content((x+w/2, y+0.8), body)
    }
    box(0, 3.4, 5, [Perception#linebreak()class, bearing, depth])
    box(7, 3.4, 5, [State estimator#linebreak()$hat(eta),hat(nu),P$])
    box(14, 3.4, 5, [Guidance#linebreak()$u_d$, $r_d$])
    line((5, 4.2), (6, 4.2), (6, 2.6), (13, 2.6), (13, 4.2), (14, 4.2), stroke: 0.6pt, mark: arrow)
    content((9.5, 2.1), [Target / obstacle geometry])
    // State estimate goes to guidance on a separate lower lane.
    line((12, 4.6), (14, 4.6), mark: arrow)
    content((13, 5.0), [State])
    line((2.5, 6.1), (2.5, 5), mark: arrow)
    content((2.5, 6.45), [ZED frames])
    line((9.5, 6.1), (9.5, 5), mark: arrow)
    content((9.5, 6.45), [GNSS + IMU])
    line((16.5, 6.1), (16.5, 5), mark: arrow)
    content((16.5, 6.45), [Mission goal])
    box(14, -0.5, 5, [Speed / yaw regulator#linebreak()ArduRover], fill: luma(95%))
    line((16.5, 3.4), (16.5, 1.1), mark: arrow)
    content((17.9, 2.25), [50 Hz#linebreak()MAVLink])
    box(7, -0.5, 5, [Mixer + saturation#linebreak()$p_L,p_R$ in µs])
    box(0, -0.5, 5, [ESC → motor → propeller#linebreak()$T_L,T_R$ in N])
    line((14, 0.3), (12, 0.3), mark: arrow)
    content((13, 0.9), [Effort])
    line((7, 0.3), (5, 0.3), mark: arrow)
    content((6, 0.9), [PWM])
    box(7, -3.5, 5, [Autopilot navigation EKF#linebreak()RTK GNSS + Navigator IMU])
    line((9.5, -1.9), (9.5, -1.4), (16.5, -1.4), (16.5, -0.5), mark: arrow)
    content((13, -1.05), [State feedback])
    content((9.5, 7.25), [AGX Orin functions])
  })
}
#let timing() = {
  set text(size: 9pt)
  cetz.canvas(length: 0.8cm, {
    import cetz.draw: *
    for (a, b, title) in ((0, 6.727, [Wait for tick#linebreak()0–20 ms]), (6.727, 8.409, [Compute#linebreak()5 ms]), (8.409, 11.773, [Transport#linebreak()10 ms]), (11.773, 18.5, [Actuator delay#linebreak()20 ms])) {
      rect((a, 0), (b, 1.5), fill: if a == 0 { luma(94%) } else { white }, stroke: 0.8pt)
      content(((a+b)/2, 0.75), title)
    }
    line((0, -0.7), (18.5, -0.7), mark: arrow)
    content((9.25, -1.25), [Command change → thrust begins within 55 ms])
    content((9.25, 2.1), [Budget, followed by thrust lag $tau_T=0.2$ s])
  })
}
#let schedule() = {
  set text(size: 9pt)
  let schedule = json("data/schedule.json")
  let stop = schedule.chosen_cutoff_s
  let force = schedule.chosen_total_force_N / 2
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    lq.diagram(width: 100%, height: 0% + 1.65in, title: [BlueBoat force command], xlabel: [Time (s)], ylabel: [Each M200 (N)], xlim: (0,90), ylim: (-1,18), xaxis: (ticks: (0,15,30,45,60,75,90)),
      lq.plot((0, stop, stop, 90), (force,force,0,0), mark: none)),
    lq.diagram(width: 100%, height: 0% + 1.65in, title: [Cutoff at #calc.round(stop,digits:4) s], xlabel: [Time (s)], ylabel: [Each M200 (N)], xlim: (stop - 0.8,stop + 0.8), ylim: (-1,18),
      lq.plot((stop - 0.8, stop, stop, stop + 0.8), (force,force,0,0), mark: none)),
  )
}
#let motor() = {
  set text(size: 9pt)
  let static = json("data/m200_static.json")
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    lq.diagram(width: 100%, height: 0% + 2.1in, title: [M200 and installed-map assumption, 16 V], xlabel: [PWM pulse (µs)], ylabel: [Component thrust (N)], xlim: (1100,1900), ylim: (-35,65),
      legend: (radius: 0pt, fill: white, position: top + left),
      lq.plot(static.pwm_us, static.force_N, mark: none, label: [M200 component]),
      lq.plot(static.pwm_us, static.force_N.map(v => v * json("data/parameters.json").installation_scale), mark: none, label: [Installed assumption], stroke: (dash: "dashed", thickness: 1pt))),
    lq.diagram(width: 100%, height: 0% + 2.1in, title: [Installed saturation and reversal], xlabel: [Time (s)], ylabel: [Thrust (N)], xlim: (0,7), ylim: (-35,65), legend: (radius: 0pt, fill: white, position: top + right),
      lq.plot(cr.motor.time, cr.motor.demand_left, mark: none, label: [Static demand], stroke: (dash: "dashed", thickness: 1pt)),
      lq.plot(cr.motor.time, cr.motor.left, mark: none, label: [Lagged force])),
  )
}
#let boat-response() = {
  set text(size: 9pt)
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    lq.diagram(width: 100%, height: 0% + 2.0in, title: [Motor-lag sensitivity], xlabel: [Time (s)], ylabel: [Surge speed (m/s)], xlim: (0,4), ylim: (0,1.7), legend: (radius: 0pt, fill: white, position: top + left),
      ..("equal_ideal", "equal_0.1", "equal_0.2", "equal_0.4").enumerate().map(pair => {
        let d = cr.at(pair.last())
        lq.plot(d.time, d.u, mark: none, label: ([Ideal], [$tau_T=0.1$ s], [$tau_T=0.2$ s], [$tau_T=0.4$ s]).at(pair.first()))
      })),
    lq.diagram(width: 100%, height: 0% + 2.0in, title: [Unequal thrust then coast], xlabel: [Time (s)], ylabel: [Yaw rate (rad/s)], xlim: (0,12), ylim: (-0.005,0.07),
      lq.plot(cr.differential.time, cr.differential.r, mark: none)),
  )
}
#let sensor-response() = {
  set text(size: 9pt)
  let d = cr.differential
  let g = sensors.gnss
  let i = sensors.imu
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    lq.diagram(width: 100%, height: 0% + 2.0in, title: [Position at GNSS antenna], xlabel: [Delivery time (s)], ylabel: [East (m)], xlim: (0,12.25), xaxis: (ticks: (0,2,4,6,8,10,12)), legend: (radius: 0pt, fill: white, position: top + left),
      lq.plot(d.time, d.x.zip(d.psi).map(p => p.first() - 0.5*calc.cos(p.last())), mark: none, label: [Antenna truth]),
      lq.plot(g.available_time, g.x, mark: "x", stroke: none, mark-size: 1.2pt, label: [20 Hz, delayed])),
    lq.diagram(width: 100%, height: 0% + 2.0in, title: [Yaw-rate measurement], xlabel: [Delivery time (s)], ylabel: [Yaw rate (rad/s)], xlim: (0,12.25), xaxis: (ticks: (0,2,4,6,8,10,12)), legend: (radius: 0pt, fill: white, position: top + right),
      lq.plot(d.time, d.r, mark: none, label: [Truth]),
      lq.plot(i.available_time.enumerate().filter(p => calc.rem(p.first(),10)==0).map(p=>p.last()), i.r.enumerate().filter(p => calc.rem(p.first(),10)==0).map(p=>p.last()), mark: "x", mark-size: 1pt, stroke: none, label: [IMU samples])),
  )
}
#let camera-response() = {
  set text(size: 9pt)
  let c = sensors.camera
  let valid = c.valid.enumerate().filter(p=>p.last()).map(p=>p.first())
  let e = json("data/camera_range_sensitivity.json")
  grid(columns: (1fr, 1fr), column-gutter: 14pt,
    lq.diagram(width: 100%, height: 0% + 2.0in, title: [Target range and missing frames], xlabel: [Delivery time (s)], ylabel: [Range (m)], xlim: (0,12.25), xaxis: (ticks: (0,2,4,6,8,10,12)), legend: (radius: 0pt, fill: white, position: top + right),
      lq.plot(c.sample_time, c.true_distance, mark: none, label: [Truth]),
      lq.plot(valid.map(k=>c.available_time.at(k)), valid.map(k=>c.stereo_distance.at(k)), mark: "x", mark-size: 1pt, stroke: none, label: [Stereo, valid only])),
    lq.diagram(width: 100%, height: 0% + 2.0in, title: [Stereo error grows with distance], xlabel: [Forward depth (m)], ylabel: [Range σ (m)], xlim: (5,50), ylim: (0,16),
      lq.plot(e.distance_m, e.sigma_range_m, mark: none)),
  )
}
