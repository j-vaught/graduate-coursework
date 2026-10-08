"""Reconstruct the slide-deck experiments and export data for Typst figures."""

from __future__ import annotations

import hashlib
import json
import posixpath
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray
from PIL import Image
from scipy.integrate import solve_ivp
from scipy.optimize import least_squares, root_scalar

ROOT = Path(__file__).resolve().parent
DECK = ROOT.parent / "boat_control_project.pptx"
DATA = ROOT / "data"
SOURCE = ROOT / "source" / "slides"
FloatArray = NDArray[np.float64]
COLORS = {"blue": (63, 144, 218), "orange": (255, 169, 14), "red": (189, 31, 1)}


@dataclass(frozen=True)
class Parameters:
    mass_kg: float = 180.0
    yaw_inertia_kg_m2: float = 446.0
    thruster_spacing_m: float = 2.4
    surge_linear_N_s_m: float = 51.3
    surge_quadratic_N_s2_m2: float = 72.4
    sway_linear_N_s_m: float = 40.0
    yaw_linear_N_m_s: float = 400.0
    wind_force_N: float = 15.3
    thrust_min_N: float = -100.0
    thrust_max_N: float = 250.0


P = Parameters()


def extract_source_images() -> None:
    """Keep the exact embedded source images, with their relationships and hashes."""
    ns = {
        "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
        "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
        "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    }
    manifest: dict[str, Any] = {
        "deck": "../boat_control_project.pptx",
        "sha256": hashlib.sha256(DECK.read_bytes()).hexdigest(),
        "images": [],
    }
    with zipfile.ZipFile(DECK) as archive:
        for slide in (3, 4):
            document = ET.fromstring(archive.read(f"ppt/slides/slide{slide}.xml"))
            relations = {
                item.attrib["Id"]: item.attrib["Target"]
                for item in ET.fromstring(archive.read(f"ppt/slides/_rels/slide{slide}.xml.rels"))
            }
            for picture in document.findall(".//p:pic", ns):
                blip = picture.find(".//a:blip", ns)
                if blip is None:
                    continue
                relation = blip.attrib["{" + ns["r"] + "}embed"]
                target = posixpath.normpath("ppt/slides/" + relations[relation])
                content = archive.read(target)
                name = f"slide-{slide}-{Path(target).name}"
                (SOURCE / name).write_bytes(content)
                manifest["images"].append(
                    {"slide": slide, "file": name, "sha256": hashlib.sha256(content).hexdigest()}
                )
    write_json(ROOT / "source" / "manifest.json", manifest)


def digitize(
    number: int,
    color: str,
    bounds: tuple[int, int, int, int],
    x_pixels: tuple[float, float],
    x_values: tuple[float, float],
    y_pixels: tuple[float, float],
    y_values: tuple[float, float],
    exclusions: tuple[tuple[int, int, int, int], ...] = (),
) -> FloatArray:
    """Read a colored trace using explicitly recorded tick-to-pixel calibration."""
    image = np.asarray(Image.open(SOURCE / f"slide-4-image{number}.png").convert("RGB"))
    distance = np.linalg.norm(image.astype(float) - np.array(COLORS[color]), axis=2)
    mask = distance < 32.0
    x0, x1, y0, y1 = bounds
    allowed = np.zeros(mask.shape, dtype=bool)
    allowed[y0:y1, x0:x1] = True
    for ex0, ex1, ey0, ey1 in exclusions:
        allowed[ey0:ey1, ex0:ex1] = False
    mask &= allowed
    points = []
    for x in range(x0, x1):
        ys = np.flatnonzero(mask[:, x])
        if not ys.size:
            continue
        y = float(np.median(ys))
        tx = np.interp(x, x_pixels, x_values)
        # Y pixels are intentionally ordered from the top to the bottom of the image.
        ty = np.interp(y, y_pixels, y_values)
        if x_pixels[0] <= x <= x_pixels[1] and y_pixels[0] <= y <= y_pixels[1]:
            points.append((tx, ty))
    return np.asarray(points, dtype=float).reshape(-1, 2)


def source_traces() -> dict[str, FloatArray]:
    traces = {
        "equal_u": digitize(
            16,
            "blue",
            (143, 915, 48, 516),
            (141.5, 915.0),
            (0, 40),
            (54.0, 493.0),
            (1.4, 0),
            ((520, 962, 437, 516),),
        ),
        "differential_u": digitize(
            17,
            "blue",
            (153, 784, 48, 595),
            (152.0, 784.5),
            (0, 60),
            (55.5, 573.0),
            (1.6, -1),
            ((550, 824, 270, 375),),
        ),
        "differential_v": digitize(
            17,
            "orange",
            (153, 784, 48, 595),
            (152.0, 784.5),
            (0, 60),
            (55.5, 573.0),
            (1.6, -1),
            ((550, 824, 270, 375),),
        ),
        "differential_r": digitize(
            17,
            "red",
            (153, 784, 48, 595),
            (152.0, 784.5),
            (0, 60),
            (55.5, 573.0),
            (1.6, -1),
            ((550, 824, 270, 375),),
        ),
        "pulse_v": digitize(
            18,
            "blue",
            (155, 927, 48, 398),
            (154.5, 927.5),
            (0, 30),
            (66.5, 381.0),
            (0.08, 0),
            ((810, 975, 50, 98),),
        ),
        "pulse_r": digitize(
            18,
            "blue",
            (162, 934, 523, 873),
            (161.0, 934.5),
            (0, 30),
            (540.17, 825.5),
            (0, -0.4),
            ((780, 980, 525, 575),),
        ),
        "decay_u": digitize(
            19,
            "blue",
            (143, 914, 48, 516),
            (141.5, 914.5),
            (0, 30),
            (71.0, 492.5),
            (1, 0),
            ((670, 962, 57, 184),),
        ),
        "decay_v": digitize(
            19,
            "orange",
            (143, 914, 48, 516),
            (141.5, 914.5),
            (0, 30),
            (71.0, 492.5),
            (1, 0),
            ((670, 962, 57, 184),),
        ),
        "decay_r": digitize(
            19,
            "red",
            (143, 914, 48, 516),
            (141.5, 914.5),
            (0, 30),
            (71.0, 492.5),
            (1, 0),
            ((670, 962, 57, 184),),
        ),
        "wind_y": digitize(
            21,
            "orange",
            (135, 907, 48, 516),
            (134.0, 907.5),
            (0, 60),
            (56.0, 493.0),
            (22, 0),
            ((90, 287, 54, 131),),
        ),
        "blind_calm_distance": digitize(
            22,
            "blue",
            (846, 1408, 47, 594),
            (845.5, 1408.0),
            (0, 90),
            (115.5, 566.5),
            (30, 0),
            ((815, 1073, 49, 154),),
        ),
        "blind_crosswind_distance": digitize(
            22,
            "orange",
            (846, 1408, 47, 594),
            (845.5, 1408.0),
            (0, 90),
            (115.5, 566.5),
            (30, 0),
            ((815, 1073, 49, 154),),
        ),
        "blind_headwind_distance": digitize(
            22,
            "red",
            (846, 1408, 47, 594),
            (845.5, 1408.0),
            (0, 90),
            (115.5, 566.5),
            (30, 0),
            ((815, 1073, 49, 154),),
        ),
    }
    for name, points in traces.items():
        np.savetxt(
            DATA / f"slide_trace_{name}.csv", points, delimiter=",", header="x,y", comments=""
        )
    write_json(DATA / "slide_traces.json", {k: v.tolist() for k, v in traces.items()})
    return traces


def rhs(state: FloatArray, left: float, right: float, wind: tuple[float, float]) -> FloatArray:
    """Six-state, planar rigid-body dynamics with body-frame hydrodynamic damping."""
    _, _, heading, u, v, r = state
    c, s = np.cos(heading), np.sin(heading)
    wind_x, wind_y = wind
    fx, fy = c * wind_x + s * wind_y, -s * wind_x + c * wind_y
    return np.array(
        [
            c * u - s * v,
            s * u + c * v,
            r,
            v * r
            + (
                left
                + right
                - P.surge_linear_N_s_m * u
                - P.surge_quadratic_N_s2_m2 * u * abs(u)
                + fx
            )
            / P.mass_kg,
            -u * r + (-P.sway_linear_N_s_m * v + fy) / P.mass_kg,
            (P.thruster_spacing_m / 2 * (right - left) - P.yaw_linear_N_m_s * r)
            / P.yaw_inertia_kg_m2,
        ],
        dtype=float,
    )


def run(
    name: str,
    duration: float,
    segments: list[tuple[float, float, float, float]],
    initial: tuple[float, ...] = (0, 0, 0, 0, 0, 0),
    wind: tuple[float, float] = (0, 0),
    max_step: float = 0.05,
) -> dict[str, Any]:
    """Integrate each constant-input interval separately, preserving input switches."""
    time = np.linspace(0, duration, round(duration / 0.05) + 1)
    states = np.full((time.size, 6), np.nan)
    state = np.asarray(initial, dtype=float)
    thrust = np.zeros((time.size, 2))
    for start, end, left, right in segments:
        solution = solve_ivp(
            lambda _t, y, tl=left, tr=right: rhs(y, tl, tr, wind),
            (start, end),
            state,
            rtol=1e-10,
            atol=1e-12,
            max_step=max_step,
            dense_output=True,
        )
        assert solution.success and solution.sol is not None
        indices = (time >= start) & (time <= end)
        states[indices] = solution.sol(time[indices]).T
        thrust[indices] = (left, right)
        state = solution.y[:, -1]
    assert np.isfinite(states).all()
    result: dict[str, Any] = {"name": name, "time": time.tolist(), "states": states.tolist()}
    for i, field in enumerate(("x", "y", "psi", "u", "v", "r")):
        result[field] = states[:, i].tolist()
    result["left"] = thrust[:, 0].tolist()
    result["right"] = thrust[:, 1].tolist()
    result["distance"] = np.hypot(20 - states[:, 0], states[:, 1]).tolist()
    result["wind_world_N"] = list(wind)
    result["segments"] = segments
    return result


def coast_distance(speed: float) -> float:
    return (
        P.mass_kg
        / P.surge_quadratic_N_s2_m2
        * np.log1p(P.surge_quadratic_N_s2_m2 * speed / P.surge_linear_N_s_m)
    )


def forward_endpoint(total_force: float, cutoff: float) -> float:
    result = run("nominal_acceleration", cutoff, [(0, cutoff, total_force / 2, total_force / 2)])
    return result["x"][-1] + coast_distance(result["u"][-1])


def reconstruct_schedule(traces: dict[str, FloatArray]) -> tuple[float, float, dict[str, Any]]:
    """Infer the simplest coast-to-target input from the calm trace, then test wind cases."""
    trace = traces["blind_calm_distance"]
    trace = trace[(trace[:, 0] >= 0.3) & (trace[:, 0] <= 35)]

    def residual(vector: FloatArray) -> FloatArray:
        force, cutoff = vector
        result = run(
            "fit",
            90,
            [(0, cutoff, force / 2, force / 2), (cutoff, 90, 0, 0)],
            max_step=0.25,
        )
        prediction = np.interp(trace[:, 0], result["time"], result["distance"])
        return np.r_[prediction - trace[:, 1], 2 * (forward_endpoint(force, cutoff) - 20)]

    fitted = least_squares(residual, np.array([200.0, 12.0]), bounds=([10, 1], [500, 50]))
    force, cutoff = (float(x) for x in fitted.x)
    # A nominal 200 N total step is directly established elsewhere in the deck.
    # Select it when the fit supports that rounded force, then solve the exact coast distance.
    candidate_force = 200.0
    candidate_cutoff = float(
        root_scalar(lambda t: forward_endpoint(candidate_force, t) - 20, bracket=(1, 50)).root
    )
    metadata = {
        "unconstrained_fit_total_force_N": force,
        "unconstrained_fit_cutoff_s": cutoff,
        "chosen_total_force_N": candidate_force,
        "chosen_cutoff_s": candidate_cutoff,
        "nominal_endpoint_m": forward_endpoint(candidate_force, candidate_cutoff),
        "method": "Fit constant equal thrust followed by zero thrust to calm slide trace; solve coast distance to 20 m.",
        "source_schedule_status": "inferred; original schedule is not provided in the slides",
    }
    return candidate_force, candidate_cutoff, metadata


def write_json(path: Path, content: Any) -> None:
    path.write_text(json.dumps(content, indent=2, allow_nan=False) + "\n")


def main() -> None:
    DATA.mkdir(exist_ok=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    extract_source_images()
    traces = source_traces()
    force, cutoff, schedule = reconstruct_schedule(traces)
    runs = {
        "equal": run("Equal thrust", 40, [(0, 1, 0, 0), (1, 40, 100, 100)]),
        "differential": run("Differential thrust", 60, [(0, 1, 0, 0), (1, 60, 100, 150)]),
        "pulse": run("Differential pulse", 30, [(0, 1, 0, 0), (1, 2, 150, -100), (2, 30, 0, 0)]),
        "decay": run("Free decay", 30, [(0, 30, 0, 0)], (0, 0, 0, 1, 0.5, 0.5)),
        "wind": run("Crosswind drift", 60, [(0, 60, 0, 0)], wind=(0, P.wind_force_N)),
    }
    segments: list[tuple[float, float, float, float]] = [
        (0, cutoff, force / 2, force / 2),
        (cutoff, 90, 0, 0),
    ]
    for label, wind in (
        ("calm", (0, 0)),
        ("crosswind", (0, P.wind_force_N)),
        ("headwind", (-P.wind_force_N, 0)),
    ):
        runs["blind_" + label] = run(label, 90, segments, wind=wind)
    phases: dict[str, Any] = {}
    for surge in (0, 1):
        responses = []
        for v0 in np.linspace(-1, 1, 5):
            for r0 in np.linspace(-0.5, 0.5, 5):
                t = np.linspace(0, 30, 301)
                a, b = P.sway_linear_N_s_m / P.mass_kg, P.yaw_linear_N_m_s / P.yaw_inertia_kg_m2
                r = r0 * np.exp(-b * t)
                v = v0 * np.exp(-a * t) - surge * r0 * (np.exp(-b * t) - np.exp(-a * t)) / (a - b)
                responses.append(
                    {"v": v.tolist(), "r": r.tolist(), "v0": float(v0), "r0": float(r0)}
                )
        phases[str(surge)] = responses
    write_json(DATA / "runs.json", runs)
    write_json(DATA / "phases.json", phases)
    write_json(DATA / "parameters.json", asdict(P))
    write_json(DATA / "schedule.json", schedule)
    for name, result in runs.items():
        columns = ("time", "x", "y", "psi", "u", "v", "r", "left", "right", "distance")
        np.savetxt(
            DATA / f"{name}.csv",
            np.column_stack([result[field] for field in columns]),
            delimiter=",",
            header=",".join(columns),
            comments="",
            fmt="%.10g",
        )
    print(json.dumps(schedule, indent=2))
    for name, result in runs.items():
        print(
            name,
            "final",
            {field: round(result[field][-1], 6) for field in ("x", "y", "u", "v", "r", "distance")},
        )


if __name__ == "__main__":
    main()
