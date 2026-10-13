# BlueBoat simulator report sources

The report is `../simulator_report.pdf`, built from the directly editable `../simulator_report.tex`. Its six sections retain the hull equations, propulsion and command timing, sensor measurements, configuration, experiment interpretation, and complete parameter defaults. Nested bullets, 23 numbered equations, 15 tables, and eight figures remain in the report. The architecture chapter remains excluded.

All prose, equations, table cells, captions, and references to figures are editable in the single LaTeX source. Citations use the project-level `../references.bib`. Builds compile the source as edited; they never regenerate it from Typst or overwrite manual edits.

Each figure has its own standalone `.typ` document and compiled `.pdf` in `figures/standalone/`. Those documents import the shared `style.typ` and retained JSON data. The report imports their PDFs with `\includegraphics`; it does not draw figures in LaTeX.

Run from `EMCH792/projects/boat_control`. The build requires Typst, `latexmk`, pdfLaTeX, and BibTeX.

```sh
uv sync
uv run python simulator_report/scripts/build_latex.py
```

Rebuild after text-only edits, or rebuild only the figure PDFs.

```sh
uv run python simulator_report/scripts/build_latex.py --skip-figures
uv run python simulator_report/scripts/build_latex.py --figures-only
```

The script stores LaTeX auxiliary files under `build/simulator-report-latex/` and copies the completed report to the existing project-level PDF. Figure PDFs remain beside their editable Typst sources. The in-app LaTeX editor can edit the source; its standalone preview compiler currently cannot resolve external figure PDFs or the project bibliography. Use the local build command for the complete report.

| Figure | Standalone source and PDF basename |
| --- | --- |
| Coordinate frames and thrust allocation. | `01_coordinates` |
| Surge drag and local tangent. | `02_surge_drag` |
| Signed M200 command-to-thrust map. | `03_thrust_map` |
| Motor reversal response. | `04_motor_reversal` |
| Sensor acquisition and delivery timing. | `05_sensor_timing` |
| Stereo range uncertainty. | `06_stereo_uncertainty` |
| Common motor commands and open-loop paths. | `07_command_tape_paths` |
| Separation between cumulative model stages. | `08_stage_offsets` |

For example, compile one figure directly from the project directory.

```sh
typst compile --root . \
  simulator_report/figures/standalone/03_thrust_map.typ \
  simulator_report/figures/standalone/03_thrust_map.pdf
```

The actuation and sensor data generators remain under `scripts/`. The experiment generator reduces the saved paired trials in `data/configurable_simulator/comparison.json`. To deliberately refresh their inputs, run the three data generators, review the worked numerical examples and parameter tables in LaTeX, and rebuild the figures and report.

```sh
uv run python simulator_report/scripts/actuation_data.py
uv run python simulator_report/scripts/sensors_data.py
uv run python simulator_report/scripts/experiments_data.py
uv run python simulator_report/scripts/build_latex.py
```

The complete parameter tables are an editable snapshot of `configs/simulator/00_linear.json` at conversion. They are not rewritten during builds. Update them when changing the model defaults. The original `.typ` report, chapter files, and function-based figure modules remain historical sources; they are not inputs to the active LaTeX build.

`DESIGN.md` records the square navy/teal diagram language and standard plotting colors. All figure sources use CeTZ or Lilaq. Intermediate previews and compilation files are ignored; the editable LaTeX, standalone Typst figures, compiled PDFs, bibliography, and data remain versioned.
