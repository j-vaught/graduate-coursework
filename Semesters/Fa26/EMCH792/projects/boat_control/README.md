# BlueBoat dynamics and control feasibility

All active simulations and figures use one BlueBoat configuration. The report covers equal M200 thrust, differential thrust and turning, a reversing pulse, free decay, frozen-surge phase portraits, unpowered wind drift, a 20 m open-loop approach, parameter sensitivity, delayed propulsion, and GNSS/IMU/stereo observations. Authorship is J.C. Vaught. Controller design remains the next task; no PID, LQR, or pole-placement controller is implemented.

## Shared configuration

`platform.json` is the editable physical configuration. The published hull is 1.20 m long, 0.93 m wide, and 14.5 kg without batteries or payload. The selected two standard batteries contribute 2.4 kg, and a provisional 5 kg equipment/mount allowance gives 21.9 kg loaded mass. The allowance is a budget rather than a measured component bill of materials. The manufacturer permits 15 kg of batteries plus payload, giving a maximum total mass of 29.5 kg.

The nominal thrust-line spacing is an estimated 0.75 m. Yaw inertia is a uniform-envelope geometric proxy, 4.20644 kg m². Surge drag coefficients of 4 N s/m and 10 N s²/m², sway damping of 35 N s/m, and yaw damping of 12 N m s are engineering assumptions. Added mass and three-dimensional motion are omitted. These values require identification with the final loaded hull; they are not coefficients from the larger boat in the original slides.

`propulsion.py` retains the signed manufacturer M200/112 mm weedless-propeller curve at 16 V. The raw component forward maximum is 55.2134 N. A provisional installation factor of 0.728242 scales the entire curve so the two forward maxima equal BlueBoat's published total static thrust of 8.2 kgf, or 80.4145 N. This gives 40.2073 N forward and -20.0679 N reverse per side. Uniform reverse/intermediate scaling remains an assumption. All active experiments use this shared installed map, including PWM saturation and neutral deadband. Voltage-dependent and inflow-dependent thrust are not inferred from a single static curve.

The battery is nominally 14.8 V and fully charged at 16.8 V; the 16 V curve is an explicit test-voltage snapshot. Wind tests use 5 m/s wind, air density 1.225 kg/m³, drag coefficient 1, and assumed frontal/lateral exposed areas of 0.18/0.30 m². Constant world-frame forces are rotated into the boat frame. Apparent-wind changes and wind-induced yaw moment are omitted.

## Rebuild

Run from this directory. Dependencies are pinned in `uv.lock`. Figures are authored in Typst with Lilaq 0.6.0 and CeTZ 0.4.2.

```sh
uv sync --locked
uv run ruff format .
uv run ruff check . --fix
uv run ty check .
uv run python simulate.py
uv run python validate.py
uv run python components.py
typst compile report.typ boat_control_report.pdf
```

`simulate.py` exports current BlueBoat runs and separate mass/drag sensitivity tests. The ideal-thrust reference tests apply bounded forces instantaneously; `components.py` applies the same physical plant with command sampling, delay, and first-order thrust lag. Both import the same propulsion and physical parameters.

`validate.py` checks analytic surge, yaw, and wind solutions, integration refinement, energy dissipation, feasible loading and thrust, shared parameters, finite-difference linearizations, and controllability. Component checks cover exact motor transients, common hull parameters, saturation, deadband, causal timestamps, and camera visibility. Numerical agreement verifies the implementation; it does not validate the coefficients against on-water measurements.

Standalone figures use the same data as the report.

```sh
typst compile --input figure=blind render_figure.typ figures/blind.pdf
```

Renderer choices are `hull`, `feedback`, `equal`, `differential`, `turning-path`, `pulse`, `decay`, `phase`, `wind`, `schedule`, `blind`, `overlays`, `lowlevel`, `timing`, `motor`, `boat-response`, `sensors`, and `camera`. The retained `overlays` renderer name now exports mass/drag sensitivity, replacing slide comparisons.

## Hardware and sensor models

The configuration selects AGX Orin 64 GB, one forward ZED X with ZED Link Duo, VectorNav VN-110, and Septentrio mosaic-H with two PolaNt-xMF antennas. Orin owns perception, fusion, and guidance; ArduRover retains speed/yaw-rate loops and PWM on the stock Pi 4/Navigator. The report describes interfaces and coordinate conversion, rather than claiming deployed autonomy.

`components.py` exposes configurable 50 Hz guidance, 20 Hz GNSS, 200 Hz IMU, and 30 Hz stereo sampling. The command-onset budget is 55 ms. The default thrust time constant is 0.2 s, with 0.1 and 0.4 s sensitivity runs. Compute times, latencies, motor lag, and sensor noise are design assumptions. The sensor run uses a fixed random seed, a primary GNSS antenna 0.5 m aft of the hull center, fixed RTK status, and a camera at the planar hull origin observing a target at (15, 3) m. Occlusion from 5 to 6 s suppresses observations; 331 of 361 frames are valid in the default run. No rendered images, learned detector, estimator, or autonomous controller are simulated.

## Provenance and historical material

`data/` contains only current model results, physical parameters, retained manufacturer M200 samples, and validation records. `source/hardware/` preserves manufacturer curve source and hash provenance. `references.bib` centralizes the primary references used in the report.

The original presentation remains at `../boat_control_project.pptx`. Its exact embedded images and hash manifest remain in `source/slides/` and `source/manifest.json`. Earlier digitized slide traces and residuals are archived in `source/digitized_slides/` as historical material; no active simulation or figure reads them. Previous larger-boat simulations remain recoverable through Git history.

On-water measurements of loaded mass, motor spacing, mass distribution, thrust, coast-down, turns, and sensor timestamps should replace the provisional configuration. The report's competition integration section retains the current geometry, local RTK, and independent stopping checks.
