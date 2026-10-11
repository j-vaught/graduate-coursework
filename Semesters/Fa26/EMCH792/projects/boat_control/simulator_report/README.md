# BlueBoat simulator report sources

The combined report is `../simulator_report.pdf`, built from `../simulator_report.typ`. Seven chapters explain the implemented architecture, hull equations, propulsion and command timing, sensor measurements, configuration, experiment interpretation, and complete parameter defaults. The report uses nested bullets, numbered equations, and nine figures in the shared design defined by `style.typ`.

Run from the project directory.

```sh
uv sync
uv run python simulator_report/scripts/actuation_data.py
uv run python simulator_report/scripts/sensors_data.py
uv run python simulator_report/scripts/experiments_data.py
typst compile simulator_report.typ simulator_report.pdf
```

The actuation data generator calls the current simulator functions. The sensor data generator reads current sensor defaults. The experiment data generator reduces the saved paired runs in `data/configurable_simulator/comparison.json`; it does not create new controller results. The parameter chapter reads the complete baseline JSON template directly. Coordinate diagrams and analytic drag curves are authored directly in Typst.

The physical demonstration retains the baseline model and input levels. Its public commands now use signed motor percentages; the companion controller report documents the subsequent feedback implementation. Rebuild saved model trials with the commands in `SIMULATOR.md` when deliberately changing their numerical inputs. Updating figure data from a changed simulator requires reviewing the report's worked examples and assumptions.

`DESIGN.md` records the shared diagram and plot conventions. All publication figures use CeTZ or Lilaq. Intermediate previews are stored in ignored build directories. Final PDF, editable chapter files, and input data remain versioned.
