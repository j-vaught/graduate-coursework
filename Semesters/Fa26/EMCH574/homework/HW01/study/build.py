"""Calculate HW01 responses, verify the models, and build the study artifacts."""

from __future__ import annotations

import json
import math
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
from matplotlib.axes import Axes
from numpy.typing import NDArray
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
FIG = OUT / "figures"
Array = NDArray[np.float64]
GARNET, BLACK, GRAY, ATLANTIC = "#73000A", "#000000", "#5C5C5C", "#466A9F"
COLORS = [GARNET, BLACK, ATLANTIC, "#1F414D", "#CC2E40"]
RESULTS: dict[str, Any] = {}
TABLES: dict[str, str] = {}
HTML: list[str] = []
CHECKS: dict[str, float | str] = {}
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": BLACK,
        "axes.labelcolor": BLACK,
        "text.color": BLACK,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "grid.color": "#C7C7C7",
        "grid.linewidth": 0.5,
        "legend.fancybox": False,
        "lines.solid_capstyle": "butt",
        "lines.solid_joinstyle": "miter",
        "savefig.dpi": 180,
    }
)


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


def axes(title: str, ylabel: str, xlabel: str = "Time (s)") -> tuple[Any, Axes]:
    fig, ax = plt.subplots(figsize=(8, 3.6), layout="constrained")
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.grid(True)
    return fig, ax


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
    fig, ax = axes(title, ylabel, xlabel)
    interactive = go.Figure()
    for i, (label, y) in enumerate(curves):
        color = COLORS[i % len(COLORS)]
        dash = "--" if i % 2 else "-"
        ax.plot(t, y, color=color, lw=1.35, ls=dash, label=label)
        interactive.add_trace(
            go.Scatter(
                x=t.tolist(),
                y=np.asarray(y).tolist(),
                name=label,
                mode="lines",
                line={"color": color, "width": 2, "dash": "dash" if i % 2 else "solid"},
                hovertemplate="%{x:.6g}<br>%{y:.6g}<extra>%{fullData.name}</extra>",
            )
        )
    if band is not None:
        for value in (-band, band):
            ax.axhline(value, color=GRAY, ls=":", lw=1)
            interactive.add_hline(y=value, line_dash="dot", line_color=GRAY)
        ax.axhspan(-band, band, color="#ECECEC", zorder=0)
    for i, (label, x, y) in enumerate(events or []):
        ax.plot(x, y, "s", color=BLACK, ms=4)
        ax.annotate(
            f"{label}\n({fmt(x)}, {fmt(y)})",
            xy=(x, y),
            xytext=(0.02 + 0.32 * (i % 3), 0.96 if i < 3 else 0.70),
            textcoords="axes fraction",
            ha="left",
            va="top",
            fontsize=8,
            bbox={"boxstyle": "square,pad=0.2", "fc": "white", "ec": "#C7C7C7"},
            arrowprops={"arrowstyle": "-", "color": GRAY},
        )
        interactive.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                name=label,
                mode="markers",
                marker={"color": BLACK, "symbol": "square", "size": 9},
                hovertemplate="%{x:.8g}<br>%{y:.8g}<extra>" + label + "</extra>",
            )
        )
    if len(curves) > 1:
        ax.legend(loc="lower right", fontsize=8)
    ax.margins(y=0.3 if events else 0.08)
    fig.savefig(FIG / f"{name}.png")
    plt.close(fig)
    interactive.update_layout(
        title=title,
        xaxis_title=xlabel,
        yaxis_title=ylabel,
        template="plotly_white",
        font={"family": "Arial", "color": BLACK},
        height=440,
        margin={"l": 65, "r": 30, "t": 70, "b": 70},
        legend={"orientation": "h", "y": -0.23},
        hovermode="closest",
    )
    HTML.append(
        interactive.to_html(
            full_html=False,
            include_plotlyjs=True if not HTML else False,
            div_id=name,
            config={"responsive": True, "displaylogo": False},
        )
    )


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
    unit_circle()
    free_body_diagrams()
    (OUT / "results.json").write_text(json.dumps(RESULTS, indent=2) + "\n")
    (OUT / "verification.json").write_text(json.dumps(CHECKS, indent=2) + "\n")
    source = (ROOT / "solutions_source.md").read_text()
    for key, content in TABLES.items():
        source = source.replace("{{" + key + "}}", content)
    assert "{{" not in source, "Unresolved result placeholder"
    (ROOT / "solutions.md").write_text(source)
    page = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>EMCH 574 HW01 response explorer</title>
<style>body{max-width:1100px;margin:30px auto;padding:0 20px;font:17px Arial;color:#000}
h1,h2{color:#73000A}section{border-top:2px solid #73000A;padding-top:12px;margin-top:30px}
a{color:#73000A} .note{background:#ECECEC;padding:16px;border-left:4px solid #73000A}</style>
</head><body><h1>EMCH 574 HW01 response explorer</h1><p>J.C. Vaught</p>
<p>Hover for numerical data tips. Drag to zoom, double-click to reset, and click legend
entries to compare curves. This file works offline.</p>
<p class="note">All inputs are in SI units in inputs.json. Displacement plots show the labeled
engineering units. Square markers evaluate the exact analytical response at the specified event.
C6 is a formal linear prediction whose large deflection and dynamic yield exceed the model limits.
C8 uses the course-note approximation on PDF page 252.</p>"""
    html_document = page + "".join("<section>" + h + "</section>" for h in HTML) + "</body></html>"
    (OUT / "interactive.html").write_text(
        "\n".join(line.rstrip() for line in html_document.splitlines()) + "\n"
    )
    (OUT / "pdf").mkdir(exist_ok=True)
    subprocess.run(
        [
            "pandoc",
            "solutions.md",
            "--standalone",
            "--pdf-engine=xelatex",
            "--toc",
            "--toc-depth=1",
            "-V",
            "geometry:margin=0.78in",
            "-V",
            "fontsize=10pt",
            "-V",
            "colorlinks=true",
            "-V",
            "linkcolor=black",
            "-V",
            "urlcolor=black",
            "-o",
            "output/pdf/HW01_worked_solutions.pdf",
        ],
        cwd=ROOT,
        check=True,
    )
    print(f"Built {len(HTML)} interactive plots and verified {len(CHECKS)} checks.")


def unit_circle() -> None:
    fig, ax = plt.subplots(figsize=(5, 5), layout="constrained")
    theta = np.linspace(0, 2 * math.pi, 501)
    ax.plot(np.cos(theta), np.sin(theta), color=GRAY)
    ax.axhline(0, color=BLACK, lw=0.8)
    ax.axvline(0, color=BLACK, lw=0.8)
    angles = [math.pi / 2, 3 * math.pi / 2, math.pi / 4, -math.pi / 4]
    labels = [r"$i=e^{i\pi/2}$", r"$-i=e^{i3\pi/2}=e^{-i\pi/2}$", r"$e^{i\pi/4}$", r"$e^{-i\pi/4}$"]
    for angle, label in zip(angles, labels, strict=True):
        x, y = math.cos(angle), math.sin(angle)
        ax.plot(x, y, "s", color=GARNET)
        ax.annotate(
            label, (x, y), xytext=(8, 8 if y >= 0 else -20), textcoords="offset points", fontsize=10
        )
    ax.set(
        xlim=(-1.35, 1.65),
        ylim=(-1.35, 1.35),
        xlabel="Real part",
        ylabel="Imaginary part",
        title="C9. Locations on the complex unit circle",
        aspect="equal",
    )
    fig.savefig(FIG / "C9.png")
    plt.close(fig)


def free_body_diagrams() -> None:
    fig, axes_array = plt.subplots(2, 3, figsize=(10, 6), layout="constrained")
    titles = [
        "A1. Pendulum",
        "B1 / C3. Horizontal free",
        "B2 / B6. Damped / forced",
        "C1 / C2. Vertical",
        "C5 / C6. Sudden load",
        "C7. Course-note projection",
    ]
    for ax, title in zip(axes_array.flat, titles, strict=True):
        ax.set(xlim=(-2, 2), ylim=(-2, 2), aspect="equal", title=title)
        ax.axis("off")

    def arrow(
        ax: Axes, end: tuple[float, float], label: str, label_pos: tuple[float, float] | None = None
    ) -> None:
        ax.annotate(
            "", xy=end, xytext=(0, 0), arrowprops={"arrowstyle": "->", "color": GARNET, "lw": 1.5}
        )
        pos = end if label_pos is None else label_pos
        ax.text(*pos, label, fontsize=9, ha="center", va="bottom")

    for ax in axes_array.flat:
        ax.plot(0, 0, "s", color=BLACK, ms=8)
    ax = axes_array.flat[0]
    arrow(ax, (-0.65, 1.35), "$T$")
    arrow(ax, (0, -1.4), "$mg$", (0.3, -1.6))
    ax.plot([-0.65, 0], [1.35, 0], color=GRAY, ls="--")
    ax.text(-1.8, -1.7, r"Tangential force $=-mg\sin\theta$", fontsize=9)
    ax = axes_array.flat[1]
    arrow(ax, (-1.3, 0), "$ku$")
    arrow(ax, (0, 1.1), "$N$")
    arrow(ax, (0, -1.1), "$mg$", (0.3, -1.4))
    ax.text(0.5, 0.35, r"$+u\ \rightarrow$", fontsize=10)
    ax = axes_array.flat[2]
    arrow(ax, (-1.4, 0), r"$ku+c\dot u$")
    arrow(ax, (1.2, 0), "$F(t)$")
    ax.text(-1.7, -1.6, "Vertical weight and support balance.\nSet F = 0 for B2.", fontsize=9)
    ax = axes_array.flat[3]
    arrow(ax, (0, 1.2), r"$k(\delta_{\rm st}+u)$")
    arrow(ax, (0, -1.2), "$mg$", (0.4, -1.5))
    ax.text(0.6, 0, r"$+u\ \downarrow$", fontsize=10)
    ax = axes_array.flat[4]
    arrow(ax, (0, 1.2), "$ku$")
    arrow(ax, (0, -1.2), "$F_0$", (0.4, -1.5))
    ax.text(-1.7, -1.9, "u measured from the unloaded position.", fontsize=9)
    ax = axes_array.flat[5]
    arrow(ax, (-1.3, 0), r"$ku+mg\theta$")
    ax.text(-1.7, -1.4, r"$\theta\approx 3u/(2L)$" + "\nProjected restoring forces.", fontsize=10)
    fig.savefig(FIG / "free_body_diagrams.png")
    plt.close(fig)


if __name__ == "__main__":
    main()
