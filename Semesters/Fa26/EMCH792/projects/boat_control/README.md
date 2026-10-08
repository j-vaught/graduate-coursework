# Twin-thruster boat project report

The eight-page `boat_control_report.pdf` develops the original six-slide presentation into a technical report with recreated simulations, vector figures, equations, numerical checks, and control-design analysis. The author is J.C. Vaught. The retained presentation is `../boat_control_project.pptx`.

The report reproduces the equal-thrust step, differential-thrust step and trajectory, differential pulse, free decay, frozen-surge phase portraits, unpowered crosswind drift, and blind target approach. Thirteen digitized time traces agree with the reconstruction to within 0.806 pixel RMS. The 90 s target errors are 0.0000 m in calm conditions, 32.7038 m in crosswind, and 17.5518 m in headwind. These are simulated results for the slide model.

## Rebuild

Run the following commands from this directory. Python dependencies are pinned in `uv.lock`. Typst 0.15.1, Lilaq 0.6.0, and CeTZ 0.4.2 were used for the delivered figures and report.

```sh
uv sync --locked
uv run python simulate.py
uv run python validate.py
uv run ruff format .
uv run ruff check . --fix
uv run ty check .
typst compile report.typ boat_control_report.pdf
```

`simulate.py` extracts the original embedded images, digitizes the traces, reconstructs the nonlinear dynamics, and writes all simulation data. `validate.py` checks exact surge, yaw, and wind solutions, integration-step refinement, energy dissipation, thrust limits, linearizations, and agreement with the slides. A failing numerical assertion stops validation. No plotting library is used in Python. `figures.typ` draws every plot in Lilaq and both diagrams in CeTZ.

Individual figures can also be exported as standalone PDFs. The renderer accepts `hull`, `feedback`, `equal`, `differential`, `turning-path`, `pulse`, `decay`, `phase`, `wind`, `schedule`, `blind`, or `overlays`.

```sh
typst compile --input figure=blind render_figure.typ figures/blind.pdf
```

## Model and reconstruction

The state order is `(x, y, psi, u, v, r)`. Position uses east and north axes, heading is counterclockwise from east, surge points forward, sway points left, and positive yaw turns left. Thrusters act along the body surge axis with a 2.4 m force-line separation. Wind forces remain fixed in the inertial frame and are rotated into the body frame during integration. Wind has no yaw moment in this model.

Mass, yaw inertia, thrust limits, geometry, surge drag, and sway drag come from the slides. The yaw damping of 400 N m s is inferred from the differential-step steady rate and pulse response. The constant 15.3 N wind force is the value in the slide plots. The blind schedule was not specified, so a constant equal-thrust interval followed by coasting was fitted to the calm trace. The selected input is 100 N per thruster for 13.8329077722 s, followed by zero thrust. The same schedule is evaluated in both wind cases without refitting.

The original MATLAB or Python source remains unavailable. This directory is a new reproducible reconstruction, with the inferred quantities identified in the report. Raster agreement measures consistency with the retained slide images, while analytic and integration checks assess the reconstructed implementation. The trajectory and phase plots are recreated from the same equations; the thirteen raster comparisons cover time histories rather than every graphical element.

The presentation proposes a linear-quadratic regulator and performance targets but contains no closed-loop results. The report preserves that scope. Its additional controllability calculation gives rank four at rest and rank six at a 1 m/s straight-running reference. Thus, full-state linear regulation at rest cannot control the lateral-position integrator, and guidance must account for the operating point and the lack of direct sway thrust.

## Retained files

`data/` contains CSV runs, complete JSON histories, digitized slide samples, the inferred schedule, parameter values, and validation results. `source/slides/` contains the exact embedded images, and `source/manifest.json` records their SHA-256 hashes and the presentation hash. `references.bib` centralizes the presentation and technical references. The editable report and figure sources are `report.typ` and `figures.typ`. `figures/` contains standalone vector exports of every figure.
