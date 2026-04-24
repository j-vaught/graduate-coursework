"""Generate consistent GIF demos for the custom DeepXube domains."""

from __future__ import annotations

import argparse
import io
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import deepxube  # noqa: F401
from deepxube.base.domain import StateGoalVizable
from deepxube.utils.command_line_utils import get_domain_from_arg


BLACK_90 = "#363636"
BLACK_10 = "#ECECEC"
WHITE = "#FFFFFF"


@dataclass(frozen=True)
class DemoConfig:
    key: str
    domain: str
    steps: int
    figsize: tuple[float, float]


DEMO_CONFIGS: dict[str, DemoConfig] = {
    "hanoi": DemoConfig("hanoi", "hanoi.6.3", 14, (6.0, 5.0)),
    "pancake": DemoConfig("pancake", "pancake.10", 12, (6.0, 5.0)),
    "linkage": DemoConfig("linkage", "linkage.64_64_64", 14, (7.0, 6.0)),
    "mapf": DemoConfig("mapf", "mapf.28_28_30_64", 12, (8.0, 8.0)),
    "arm": DemoConfig("arm", "arm.6_12_8", 12, (6.5, 6.0)),
    "retro": DemoConfig("retro", "retro.7", 12, (7.0, 5.5)),
}


def _parse_args(argv: Sequence[str] | None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate GIF demos through each domain visualizer."
    )
    parser.add_argument(
        "demo",
        choices=["all", *DEMO_CONFIGS.keys()],
        nargs="?",
        default="all",
    )
    parser.add_argument("--out-dir", type=Path, default=Path("demo_gifs"))
    parser.add_argument("--steps", type=int, default=None)
    parser.add_argument("--fps", type=float, default=2.0)
    parser.add_argument("--dpi", type=int, default=110)
    parser.add_argument("--seed", type=int, default=775)
    parser.add_argument("--action-retries", type=int, default=8)
    return parser.parse_args(argv)


def _sample_goal_pair(domain: Any) -> tuple[Any, Any]:
    if hasattr(domain, "sample_goalstate_goal_pairs"):
        states_goal, goals = domain.sample_goalstate_goal_pairs(1)
        return states_goal[0], goals[0]
    states, goals = domain.sample_problem_instances([0])
    return states[0], goals[0]


def _walk_from_goal(
    domain: Any,
    state_goal: Any,
    steps: int,
    action_retries: int,
) -> List[Any]:
    states = [state_goal]
    state = state_goal
    for _ in range(steps):
        next_state = state
        for _retry in range(max(1, action_retries)):
            action = domain.sample_state_action([state])[0]
            candidate = domain.next_state([state], [action])[0][0]
            next_state = candidate
            if candidate != state:
                break
        states.append(next_state)
        state = next_state
    return list(reversed(states))


def _fig_to_frame(fig: plt.Figure, dpi: int) -> Image.Image:
    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        dpi=dpi,
        bbox_inches="tight",
        facecolor=fig.get_facecolor(),
    )
    buf.seek(0)
    frame = Image.open(buf).convert("RGBA")
    copied = frame.copy()
    buf.close()
    return copied


def _render_frame(
    domain: StateGoalVizable,
    state: Any,
    goal: Any,
    step_idx: int,
    total_steps: int,
    config: DemoConfig,
    dpi: int,
) -> Image.Image:
    fig = plt.figure(figsize=config.figsize, facecolor=WHITE)
    domain.visualize_state_goal(state, goal, fig)
    solved = domain.is_solved([state], [goal])[0]
    label = f"{config.key} demo | step {step_idx}/{total_steps} | solved={solved}"
    fig.text(
        0.5,
        0.985,
        label,
        ha="center",
        va="top",
        color=BLACK_90,
        fontsize=11,
        fontweight="bold",
        bbox={"facecolor": BLACK_10, "edgecolor": BLACK_90, "pad": 4},
    )
    image = _fig_to_frame(fig, dpi)
    plt.close(fig)
    return image


def generate_demo(
    config: DemoConfig,
    out_dir: Path,
    steps: int | None = None,
    fps: float = 2.0,
    dpi: int = 110,
    seed: int = 775,
    action_retries: int = 8,
) -> Path:
    np.random.seed(seed)
    domain, _ = get_domain_from_arg(config.domain)
    if not isinstance(domain, StateGoalVizable):
        raise TypeError(f"{config.domain} does not provide a state-goal visualizer")

    state_goal, goal = _sample_goal_pair(domain)
    path = _walk_from_goal(
        domain,
        state_goal,
        config.steps if steps is None else steps,
        action_retries,
    )
    total_steps = len(path) - 1
    frames = [
        _render_frame(domain, state, goal, idx, total_steps, config, dpi)
        for idx, state in enumerate(path)
    ]

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{config.key}_gif_demo.gif"
    duration_ms = max(1, int(round(1000.0 / fps)))
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        disposal=2,
    )
    return out_path


def main(argv: Sequence[str] | None = None) -> None:
    args = _parse_args(argv)
    keys = list(DEMO_CONFIGS) if args.demo == "all" else [args.demo]
    for key in keys:
        out_path = generate_demo(
            DEMO_CONFIGS[key],
            args.out_dir,
            steps=args.steps,
            fps=args.fps,
            dpi=args.dpi,
            seed=args.seed,
            action_retries=args.action_retries,
        )
        print(f"wrote {out_path}")


def main_for_domain(key: str) -> None:
    import sys

    main([key, *sys.argv[1:]])


if __name__ == "__main__":
    main()
