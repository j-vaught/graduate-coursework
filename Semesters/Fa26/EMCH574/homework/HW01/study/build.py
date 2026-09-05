"""Calculate HW01 responses, render Typst figures, and solve the rewritten assignment."""

from __future__ import annotations

import json
import math
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
WORKSHOP = ROOT.parent.parent / "typst-figures"
FIG = WORKSHOP / "generated/homework/HW01/solutions"
SOURCE_FIG = WORKSHOP / "src/homework/HW01/solutions"
DATA = SOURCE_FIG / "data"
Array = NDArray[np.float64]
RESULTS: dict[str, Any] = {}
TABLES: dict[str, str] = {}
CHECKS: dict[str, float | str] = {}
PLOTS: list[str] = []


def fmt(x: float) -> str:
    """Assignment precision, applied only at display time."""
    if x == 0:
        return "0"
    exponent = math.floor(math.log10(abs(x)))
    leading = abs(x) / 10**exponent
    digits = 4 if leading < 2 else 3
    if exponent < -3 or exponent >= digits:
        return f"{x:.{digits - 1}e}"
    return f"{x:.{max(0, digits - 1 - exponent)}f}"


def table(name: str, rows: list[tuple[str, float, str]]) -> None:
    display_rows = [(label.replace("|", r"\vert{}"), value, unit) for label, value, unit in rows]
    TABLES[name] = "| Quantity | Value | Unit |\n|---|---:|---|\n" + "\n".join(
        f"| {label} | {fmt(float(value))} | {unit} |" for label, value, unit in display_rows
    )
    RESULTS[name] = {label: {"value": float(value), "unit": unit} for label, value, unit in rows}


def grid(end: float, *events: float) -> Array:
    return np.unique(np.r_[np.linspace(0, end, 5001), [x for x in events if 0 <= x <= end]])


@dataclass
class Oscillator:
    wn: float
    zeta: float = 0
    u0: float = 0
    v0: float = 0

    @property
    def alpha(self) -> float:
        return self.zeta * self.wn

    @property
    def wd(self) -> float:
        return self.wn * math.sqrt(1 - self.zeta**2)

    @property
    def period(self) -> float:
        return 2 * math.pi / self.wd

    def displacement(self, t: Array | float) -> Any:
        t = np.asarray(t)
        if self.zeta < 1:
            b = (self.v0 + self.alpha * self.u0) / self.wd
            return np.exp(-self.alpha * t) * (
                self.u0 * np.cos(self.wd * t) + b * np.sin(self.wd * t)
            )
        if self.zeta == 1:
            return (self.u0 + (self.v0 + self.wn * self.u0) * t) * np.exp(-self.wn * t)
        s1, s2, c1, c2 = self.real_constants()
        return c1 * np.exp(s1 * t) + c2 * np.exp(s2 * t)

    def real_constants(self) -> tuple[float, float, float, float]:
        q = math.sqrt(self.zeta**2 - 1)
        s1 = -self.wn / (self.zeta + q)
        s2 = -self.wn * (self.zeta + q)
        c1 = (self.v0 - s2 * self.u0) / (s1 - s2)
        return s1, s2, c1, self.u0 - c1

    def settling(self) -> tuple[float, float]:
        """Exact final 2% crossing for underdamped displacement release."""
        assert 0 < self.zeta < 1 and self.v0 == 0 and self.u0 != 0
        # Extrema occur at n*pi/wd and shrink monotonically for this IVP.
        last_peak = math.floor(math.log(50) * self.wd / (math.pi * self.alpha))
        start = last_peak * math.pi / self.wd
        zero = (last_peak * math.pi + math.pi / 2 + math.asin(self.zeta)) / self.wd
        threshold = 0.02 * abs(self.u0)
        ts = brentq(lambda t: abs(float(self.displacement(t))) - threshold, start, zero)
        envelope = abs(self.u0) / math.sqrt(1 - self.zeta**2)
        bound = math.log(envelope / threshold) / self.alpha
        return ts, bound


def verify(name: str, model: Oscillator, end: float) -> None:
    times = np.linspace(0, end, 701)
    sol = solve_ivp(
        lambda t, y: [y[1], -2 * model.alpha * y[1] - model.wn**2 * y[0]],
        (0, end),
        [model.u0, model.v0],
        t_eval=times,
        method="DOP853",
        rtol=1e-11,
        atol=1e-13,
    )
    assert sol.success
    error = float(np.max(np.abs(sol.y[0] - model.displacement(times))))
    scale = max(abs(model.u0), abs(model.v0 / model.wn), 1e-6)
    assert error < scale * 1e-8, (name, error)
    CHECKS[name + " max analytic/integration error (m)"] = error
    if 0 < model.zeta < 1 and model.v0 == 0:
        ts, bound = model.settling()
        later = np.linspace(ts + 1e-7, max(bound, ts) + 3 * model.period, 10001)
        assert np.max(np.abs(model.displacement(later))) <= 0.02 * abs(model.u0) * (1 + 1e-9)
        assert abs(model.displacement(ts - 1e-7)) > 0.02 * abs(model.u0)
        CHECKS[name + " final 2% crossing verified"] = "passed"


def compile_figure(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "typst",
            "compile",
            "--root",
            str(WORKSHOP),
            "--ignore-system-fonts",
            "--input",
            "palette=homework",
            str(source),
            str(destination),
        ],
        check=True,
        env={**os.environ, "SOURCE_DATE_EPOCH": "0"},
    )


def plot(
    name: str,
    title: str,
    t: Array,
    curves: list[tuple[str, Array]],
    events: list[tuple[str, float, float]] | None = None,
    band: float | None = None,
    ylabel: str = "Displacement (mm)",
    xlabel: str = "Time (s)",
) -> None:
    values = np.concatenate([np.asarray(y) for _, y in curves])
    low, high = float(values.min()), float(values.max())
    extent = max(high - low, 1e-10)
    payload = {
        "title": title,
        "xlabel": xlabel,
        "ylabel": ylabel,
        "x": t.tolist(),
        "xlim": [float(t[0]), float(t[-1])],
        "ylim": [low - 0.13 * extent, high + (0.38 if events else 0.13) * extent],
        "curves": [{"label": label, "y": np.asarray(y).tolist()} for label, y in curves],
        "band": band,
        "events": [
            {"label": label, "x": x, "y": y, "value": f"({fmt(x)}, {fmt(y)})"}
            for label, x, y in events or []
        ],
    }
    DATA.mkdir(parents=True, exist_ok=True)
    (DATA / f"{name}.json").write_text(json.dumps(payload, separators=(",", ":")) + "\n")
    figure_source = SOURCE_FIG / f"{name}.typ"
    figure_source.write_text(
        '#import "/styles/homework-response.typ": response-figure\n'
        f'#response-figure(json("data/{name}.json"))\n'
    )
    compile_figure(figure_source, FIG / f"{name}.pdf")
    PLOTS.append(name)


def damped(name: str, mass: float, k: float, zeta: float, u0: float) -> Oscillator:
    wn = math.sqrt(k / mass)
    model = Oscillator(wn, zeta, u0)
    b = model.alpha * u0 / model.wd
    amplitude = math.hypot(u0, b)
    ts, bound = model.settling()
    table(
        name,
        [
            (r"$k$", k, "N/m"),
            (r"$\omega_n$", wn, "rad/s"),
            (r"$f_n$", wn / (2 * math.pi), "Hz"),
            (r"$c_{\rm cr}$", 2 * mass * wn, "N s/m"),
            (r"$\zeta$", zeta, "1"),
            (r"$c$", 2 * zeta * mass * wn, "N s/m"),
            (r"$\omega_d$", model.wd, "rad/s"),
            (r"$f_d$", 1 / model.period, "Hz"),
            (r"$\tau_d$", model.period, "s"),
            (r"$\operatorname{Re}(s_{1,2})$", -model.alpha, "1/s"),
            (r"$|\operatorname{Im}(s_{1,2})|$", model.wd, "1/s"),
            (r"$A$", u0 * 1000, "mm"),
            (r"$B$", b * 1000, "mm"),
            (r"$C$", amplitude * 1000, "mm"),
            (r"$\phi$ (sine convention)", math.atan2(u0, b), "rad"),
            (r"$\operatorname{Re}(C_1)=\operatorname{Re}(C_2)$", u0 * 500, "mm"),
            (r"$\operatorname{Im}(C_1)=-\operatorname{Im}(C_2)$", -b * 500, "mm"),
            (r"$u(\tau_d)$", float(model.displacement(model.period)) * 1000, "mm"),
            (r"$0.02u_0$", 0.02 * u0 * 1000, "mm"),
            (r"$t_s$ (last crossing)", ts, "s"),
            (r"$t_{\rm envelope}$", bound, "s"),
        ],
    )
    times = grid(10 * model.period, model.period, ts)
    plot(
        name,
        f"{name.replace('_', ' ')}. Displacement release",
        times,
        [("Response", model.displacement(times) * 1000)],
        [
            ("Initial maximum", 0, u0 * 1000),
            ("One period", model.period, float(model.displacement(model.period)) * 1000),
            ("Final 2% crossing", ts, float(model.displacement(ts)) * 1000),
        ],
        band=0.02 * u0 * 1000,
    )
    if name == "B3":
        detail_t = np.unique(
            np.r_[np.linspace(ts - 0.6 * model.period, ts + model.period, 1501), ts]
        )
        plot(
            name + "_settling",
            "B3. Final crossing of the 2% band",
            detail_t,
            [("Response", model.displacement(detail_t) * 1000)],
            [("Final crossing", ts, float(model.displacement(ts)) * 1000)],
            band=0.02 * u0 * 1000,
        )
    verify(name, model, 10 * model.period)
    return model


def beam(d: dict[str, Any], factor: float = 3) -> tuple[float, float, float]:
    inertia = d["b"] * d["h"] ** 3 / 12
    rigidity = d["E"] * inertia
    return inertia, rigidity, factor * rigidity / d["L"] ** 3


def impact(name: str, d: dict[str, Any], wn: float) -> None:
    mass = d["M"] + d["projectile_mass"]
    v0 = d["projectile_mass"] * d["projectile_speed"] / mass
    model = Oscillator(wn, v0=v0)
    peak = v0 / wn
    time = d["query_time"]
    rows = [
        (r"$M+m_p$", mass, "kg"),
        (r"$v_0$", v0, "m/s"),
        (r"$\omega_n$", wn, "rad/s"),
        (r"$f_n$", wn / (2 * math.pi), "Hz"),
        (r"$\tau$", model.period, "s"),
        (r"$u(10)$", float(model.displacement(time)) * 1000, "mm"),
        (r"$u_{\max}$", peak * 1000, "mm"),
        (r"$t_{\rm first\ peak}$", model.period / 4, "s"),
        (r"$10\tau$", 10 * model.period, "s"),
    ]
    if "E" in d:
        inertia, rigidity, k = beam(d)
        rows = [
            (r"$I$", inertia * 1e12, r"mm$^4$"),
            (r"$EI$", rigidity, r"N m$^2$"),
            (r"$k$", k, "N/m"),
        ] + rows
    table(name, rows)
    t = grid(10 * model.period, time, model.period / 4)
    plot(
        name,
        f"{name}. Response after an embedded-projectile impact",
        t,
        [("Linear response", model.displacement(t) * 1000)],
        [
            ("First maximum", model.period / 4, peak * 1000),
            ("At 10 s", time, float(model.displacement(time)) * 1000),
        ],
    )
    verify(name, model, 10 * model.period)
    assert math.isclose(mass * v0, d["projectile_mass"] * d["projectile_speed"])
    if name == "A3":
        nonlinear = solve_ivp(
            lambda t, y: [y[1], -d["g"] / d["L"] * math.sin(y[0])],
            (0, 10 * model.period),
            [0, v0 / d["L"]],
            t_eval=t,
            method="DOP853",
            rtol=1e-11,
            atol=1e-13,
        )
        assert nonlinear.success
        nonlinear_arc = d["L"] * nonlinear.y[0]
        exact_angle = math.acos(1 - v0**2 / (2 * d["g"] * d["L"]))
        table(
            "A3_accuracy",
            [
                (r"$\theta_{\max}$ (linear)", peak / d["L"] * 180 / math.pi, "deg"),
                (r"$\theta_{\max}$ (energy)", exact_angle * 180 / math.pi, "deg"),
                (
                    "Largest arc-displacement difference over ten linear periods",
                    float(np.max(np.abs(nonlinear_arc - model.displacement(t)))) * 1000,
                    "mm",
                ),
            ],
        )
        plot(
            "A3_nonlinear",
            "A3. Small-angle approximation accumulates phase error",
            t,
            [
                ("Linear arc displacement", model.displacement(t) * 1000),
                ("Nonlinear arc displacement", nonlinear_arc * 1000),
            ],
        )


def main() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    d = json.loads((ROOT / "inputs.json").read_text())
    a = d["A2"]
    lengths = np.array(a["lengths_mm"]) / 1000
    wn = np.sqrt(a["g"] / lengths)
    freq = wn / (2 * math.pi)
    period = 1 / freq
    np.savetxt(
        OUT / "A2_lengths.csv",
        np.c_[lengths * 1000, wn, freq, period],
        delimiter=",",
        header="L_mm,omega_n_rad_s,f_n_Hz,period_s",
        comments="",
        fmt="%.12g",
    )
    TABLES["A2_lengths"] = (
        r"| Set | $L$ (mm) | $\omega_n$ (rad/s) | $f_n$ (Hz) | $\tau$ (s) |" + "\n"
    )
    TABLES["A2_lengths"] += "|---:|---:|---:|---:|---:|\n"
    TABLES["A2_lengths"] += "\n".join(
        f"| {i + 1} | {a['lengths_mm'][i]:.3f} | {fmt(w)} | {fmt(f)} | {fmt(p)} |"
        for i, (w, f, p) in enumerate(zip(wn, freq, period, strict=True))
    )
    wm, fm, pm = float(wn.mean()), float(freq.mean()), float(period.mean())
    model = Oscillator(wm, u0=a["u0"])
    duration = a["cycles"] * pm
    table(
        "A2",
        [
            (r"$\overline{\omega_n}$", wm, "rad/s"),
            (r"$\overline{f_n}$", fm, "Hz"),
            (r"$\overline{\tau}$", pm, "s"),
            (r"$u(10)$", float(model.displacement(10)) * 1000, "mm"),
            (r"$10\overline{\tau}$", duration, "s"),
            (r"$u(10\overline{\tau})$", float(model.displacement(duration)) * 1000, "mm"),
            (r"$10(2\pi/\overline{\omega_n})$", 10 * model.period, "s"),
        ],
    )
    t = grid(duration, 10)
    plot(
        "A2",
        "A2. Pendulum released from 2 mm",
        t,
        [("Mean-frequency model", model.displacement(t) * 1000)],
        [("At 10 s", 10, float(model.displacement(10)) * 1000)],
    )
    verify("A2", model, duration)
    a = d["A3"]
    impact("A3", a, math.sqrt(a["g"] / a["L"]))
    sketch_t = grid(22)
    envelope = np.exp(-0.2 * sketch_t)
    sketch_u = envelope * np.sin(math.sqrt(1 - 0.2**2) * sketch_t + 0.5)
    plot(
        "B2_envelope",
        "B2. Underdamped response and exponential envelope",
        sketch_t,
        [("Response", sketch_u), ("Upper envelope", envelope), ("Lower envelope", -envelope)],
        ylabel="Displacement / C",
        xlabel="Natural frequency x time",
    )
    a = d["B3"]
    damped("B3", a["mass"], a["k"], a["c"] / (2 * math.sqrt(a["mass"] * a["k"])), a["u0"])
    a = d["B4"]
    inertia, rigidity, k = beam(a, 48)
    table(
        "B4_beam",
        [
            (r"$I$", inertia * 1e12, r"mm$^4$"),
            (r"$EI$", rigidity, r"N m$^2$"),
            (r"$k$", k, "N/m"),
            (r"$mg/k$ using $g=9.81$", a["mass"] * 9.81 / k, "m"),
        ],
    )
    healthy = damped("B4_healthy", a["mass"], k, a["zeta"], a["u0"])
    worn = damped("B4_worn", a["mass"], k, a["worn_zeta"], a["u0"])
    t = grid(10 * healthy.period)
    plot(
        "B4_compare",
        "B4. Worn damping increases the duration of motion",
        t,
        [
            ("25% damping", healthy.displacement(t) * 1000),
            ("10% damping", worn.displacement(t) * 1000),
        ],
        band=2.5,
    )
    a = d["B5"]
    wn5 = 2 * math.pi * a["fn"]
    over = Oscillator(wn5, a["overdamped_zeta"], a["u0"])
    critical = Oscillator(wn5, 1, a["u0"])
    s1, s2, c1, c2 = over.real_constants()
    table(
        "B5",
        [
            (r"$\omega_n$", wn5, "rad/s"),
            (r"$s_1$ (overdamped)", s1, "1/s"),
            (r"$s_2$ (overdamped)", s2, "1/s"),
            (r"$C_1$ (overdamped)", c1 * 1000, "mm"),
            (r"$C_2$ (overdamped)", c2 * 1000, "mm"),
            (r"$C_1$ (critical)", a["u0"] * 1000, "mm"),
            (r"$C_2$ (critical)", wn5 * a["u0"] * 1000, "mm/s"),
        ],
    )
    for end, suffix in [(3.0, ""), (0.65, "_detail")]:
        t = grid(end)
        plot(
            "B5" + suffix,
            "B5. Critical and overdamped displacement release",
            t,
            [
                ("Critical, damping ratio 1", critical.displacement(t) * 1000),
                ("Overdamped, damping ratio 2.3", over.displacement(t) * 1000),
            ],
        )
    verify("B5_overdamped", over, 3)
    verify("B5_critical", critical, 3)
    a = d["B7"]
    inertia, rigidity, k = beam(a)
    wn7 = math.sqrt(k / a["mass"])
    zeta = a["zeta"]
    wr = wn7 * math.sqrt(1 - 2 * zeta**2)
    wd = wn7 * math.sqrt(1 - zeta**2)
    fn = wn7 / (2 * math.pi)
    uqst = a["force"] / k

    def frf(f: Any) -> Any:
        p = 2 * math.pi * np.asarray(f) / wn7
        return 1 / (1 - p**2 + 2j * zeta * p)

    table(
        "B7",
        [
            (r"$I$", inertia * 1e12, r"mm$^4$"),
            (r"$EI$", rigidity, r"N m$^2$"),
            (r"$k$", k, "N/m"),
            (r"$\omega_n$", wn7, "rad/s"),
            (r"$f_n$", fn, "Hz"),
            (r"$c_{\rm cr}$", 2 * a["mass"] * wn7, "N s/m"),
            (r"$c$", 2 * zeta * a["mass"] * wn7, "N s/m"),
            (r"$u_{\rm qst}$", uqst * 1e6, r"$\mu$m"),
            (r"$\omega_r$", wr, "rad/s"),
            (r"$\omega_d$", wd, "rad/s"),
            (r"$f_r$", wr / (2 * math.pi), "Hz"),
            (r"$N_r$", 60 * wr / (2 * math.pi), "rpm"),
            (r"$N_{90}$", 60 * fn, "rpm"),
            (r"$M_r$", 1 / (2 * zeta * math.sqrt(1 - zeta**2)), "1"),
            (r"$M_{90}$", 1 / (2 * zeta), "1"),
            (r"$|\hat u_{90}|$", uqst / (2 * zeta) * 1e6, r"$\mu$m"),
            (r"$\tau_{90}$", 1 / fn, "s"),
            (r"$f_0$", a["rpm"] / 60, "Hz"),
            (r"$\omega_0$", 2 * math.pi * a["rpm"] / 60, "rad/s"),
            (r"$|\hat u(f_0)|$", abs(frf(a["rpm"] / 60)) * uqst * 1e6, r"$\mu$m"),
        ],
    )
    f = np.linspace(0, a["rpm"] / 60, a["frequency_samples"])
    points = [
        ("Phase resonance", fn, float(abs(frf(fn)))),
        ("Double resonance RPM", 2 * fn, float(abs(frf(2 * fn)))),
        ("Operating RPM", a["rpm"] / 60, float(abs(frf(a["rpm"] / 60)))),
    ]
    table(
        "B7_FRF",
        [(label + r" $f$", x, "Hz") for label, x, y in points]
        + [(label + r" $|\mathrm{FRF}|$", y, "1") for label, x, y in points],
    )
    plot(
        "B7_magnitude",
        "B7. Normalized frequency response, 5000 samples",
        f,
        [("FRF magnitude", np.abs(frf(f)))],
        events=points,
        ylabel="Magnification (dimensionless)",
        xlabel="Excitation frequency (Hz)",
    )
    plot(
        "B7_phase",
        "B7. Response phase relative to force",
        f,
        [("FRF phase", np.angle(frf(f), deg=True))],
        ylabel="Phase (deg)",
        xlabel="Excitation frequency (Hz)",
    )
    t = grid(10 / fn)
    amp = uqst / (2 * zeta)
    steady = amp * np.sin(wn7 * t)
    transient = Oscillator(wn7, zeta, v0=-amp * wn7)
    started = steady + transient.displacement(t)
    plot(
        "B7_time",
        "B7. Phase-resonant response",
        t,
        [("Steady state", steady * 1e6), ("Switched on from rest", started * 1e6)],
        ylabel="Displacement (micrometres)",
    )
    sol = solve_ivp(
        lambda t, y: [
            y[1],
            a["force"] / a["mass"] * math.cos(wn7 * t) - 2 * zeta * wn7 * y[1] - wn7**2 * y[0],
        ],
        (0, float(t[-1])),
        [0, 0],
        t_eval=t,
        method="DOP853",
        rtol=1e-11,
        atol=1e-14,
    )
    assert sol.success
    error = float(np.max(np.abs(sol.y[0] - started)))
    assert error < 1e-10
    CHECKS["B7 forced response integration error (m)"] = error
    assert math.isclose(abs(frf(fn)), 1 / (2 * zeta))
    a = d["B8"]
    impact("B8", a, math.sqrt(beam(a)[2] / (a["M"] + a["projectile_mass"])))
    a = d["C4"]
    inertia, rigidity, k = beam(a)
    model = Oscillator(math.sqrt(k / a["mass"]), u0=a["u0"])
    table(
        "C4",
        [
            (r"$I$", inertia * 1e12, r"mm$^4$"),
            (r"$EI$", rigidity, r"N m$^2$"),
            (r"$k$", k, "N/m"),
            (r"$\omega_n$", model.wn, "rad/s"),
            (r"$f_n$", 1 / model.period, "Hz"),
            (r"$\tau$", model.period, "s"),
            (r"$u(10)$", float(model.displacement(10)) * 1000, "mm"),
            (r"$25\tau$", 25 * model.period, "s"),
        ],
    )
    t = grid(25 * model.period, 10)
    plot(
        "C4",
        "C4. Horizontal cantilever displacement release",
        t,
        [("Response", model.displacement(t) * 1000)],
        [("At 10 s", 10, float(model.displacement(10)) * 1000)],
    )
    verify("C4", model, 25 * model.period)
    a = d["C6"]
    inertia, rigidity, k = beam(a)
    force = a["mass"] * a["g"]
    static = force / k
    stress = force * a["L"] * (a["h"] / 2) / inertia
    wn6 = math.sqrt(k / a["mass"])
    period6 = 2 * math.pi / wn6
    table(
        "C6",
        [
            (r"$I$", inertia * 1e12, r"mm$^4$"),
            (r"$EI$", rigidity, r"N m$^2$"),
            (r"$k$", k, "N/m"),
            (r"$\omega_n$", wn6, "rad/s"),
            (r"$f_n$", 1 / period6, "Hz"),
            (r"$\tau$", period6, "s"),
            (r"$F_0$", force, "N"),
            (r"$u_{\rm st}$", static * 1000, "mm"),
            (r"$u_{\rm dyn,max}$", 2 * static * 1000, "mm"),
            (r"$\sigma_{\rm st}$", stress / 1e6, "MPa"),
            (r"$\sigma_{\rm dyn}$", 2 * stress / 1e6, "MPa"),
            (r"$\mathrm{SF}_{\rm st}$", a["yield_stress"] / stress, "1"),
            (r"$\mathrm{SF}_{\rm dyn}$", a["yield_stress"] / (2 * stress), "1"),
            (r"$u_{\rm dyn,max}/L$", 2 * static / a["L"], "1"),
        ],
    )
    t = grid(10 * period6, period6 / 2)
    response = static * (1 - np.cos(wn6 * t))
    plot(
        "C6",
        "C6. Ideal linear response to suddenly applied weight",
        t,
        [
            ("Dynamic displacement", response * 1000),
            ("Static displacement", np.full_like(t, static * 1000)),
        ],
        [("First maximum", period6 / 2, 2 * static * 1000)],
    )
    assert math.isclose(0.5 * k * (2 * static) ** 2, force * 2 * static)
    CHECKS["C6 work/strain energy balance at maximum"] = "passed"
    a = d["C8"]
    impact(
        "C8", a, math.sqrt(beam(a)[2] / (a["M"] + a["projectile_mass"]) + 3 * a["g"] / (2 * a["L"]))
    )
    (OUT / "results.json").write_text(json.dumps(RESULTS, indent=2) + "\n")
    (OUT / "verification.json").write_text(json.dumps(CHECKS, indent=2) + "\n")
    for diagram in ["pendulum_fbd", "horizontal_fbd", "vertical_fbd", "flex_pendulum_fbd", "C9"]:
        compile_figure(SOURCE_FIG / f"{diagram}.typ", FIG / f"{diagram}.pdf")
    source = (ROOT / "solutions_source.md").read_text()
    for key, content in TABLES.items():
        source = source.replace("{{" + key + "}}", content)
    assert "{{" not in source
    write_solutions(source)
    assignment = ROOT.parent / "HW01_EMCH574.tex"
    for figure in sorted(
        set(re.findall(r"includegraphics.*?\{(\.\./typst-figures/[^}]+)\}", assignment.read_text()))
    ):
        destination = (assignment.parent / figure).resolve()
        relative = destination.relative_to(WORKSHOP / "generated")
        original_source = WORKSHOP / "src" / relative.with_suffix(".typ")
        compile_figure(original_source, destination)
    subprocess.run(
        ["latexmk", "-xelatex", "-interaction=nonstopmode", "-halt-on-error", "HW01_EMCH574.tex"],
        cwd=ROOT.parent,
        check=True,
        stdout=(OUT / "latex-build.log").open("w"),
        stderr=subprocess.STDOUT,
    )
    print(f"Solved HW01 in place; rendered {len(PLOTS)} Lilaq plots; passed {len(CHECKS)} checks.")


def write_solutions(source: str) -> None:
    destination = ROOT.parent / "solutions"
    destination.mkdir(exist_ok=True)
    matches = list(re.finditer(r"^## ([ABC])\.(\d+)\..*$", source, re.MULTILINE))
    assert len(matches) == 20
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        content = source[match.end() : end].strip()
        content = re.sub(r"^# [BC]\..*$", "", content, flags=re.MULTILINE).strip()
        key = match[1] + match[2]
        content = content.replace(
            "output/figures/", "../typst-figures/generated/homework/HW01/solutions/"
        )
        content = content.replace(".png)", ".pdf)")
        content = re.sub(r"!\[Free-body diagrams.*?\}\n", "", content)
        diagram = {
            "A1": "pendulum_fbd",
            "B1": "horizontal_fbd",
            "B2": "horizontal_fbd",
            "B6": "horizontal_fbd",
            "C1": "vertical_fbd",
            "C2": "vertical_fbd",
            "C3": "horizontal_fbd",
            "C5": "horizontal_fbd",
            "C7": "flex_pendulum_fbd",
        }.get(key)
        if diagram:
            content = (
                f"![Free-body diagram for Problem {match[1]}.{match[2]}.]"
                f"(../typst-figures/generated/homework/HW01/solutions/{diagram}.pdf)"
                "{width=95%}\n\n" + content
            )
        content = content.replace(
            "The B.3 plot illustrates", "The response plot in B.3 illustrates"
        )
        content = content.replace(
            "Zoom the companion HTML plot to inspect the small final lobe.",
            "The square marker identifies the final crossing of the band.",
        )
        content = content.replace("The companion curve shows", "The second curve shows")
        content = content.replace("The companion", "The second")
        result = subprocess.run(
            ["pandoc", "--from=markdown", "--to=latex", "--wrap=none"],
            input=content,
            text=True,
            capture_output=True,
            check=True,
        )
        latex = result.stdout.replace(r"\begin{figure}", r"\begin{figure}[H]")
        latex = latex.replace(r"\def\LTcaptype{none}", "")
        latex = latex.replace(r"\begin{longtable}[]", r"\begin{center}\small\begin{tabular}")
        latex = latex.replace("\\endhead\n\\bottomrule\\noalign{}\n\\endlastfoot\n", "")
        latex = latex.replace(r"\end{longtable}", r"\bottomrule\end{tabular}\end{center}")
        (destination / f"{key}.tex").write_text(latex)


if __name__ == "__main__":
    main()
