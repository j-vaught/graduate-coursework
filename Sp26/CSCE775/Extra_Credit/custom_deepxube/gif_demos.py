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
from PIL import Image, ImageDraw

plt.rcParams["font.family"] = "Georgia"
plt.rcParams["font.serif"] = ["Georgia"]
plt.rcParams["mathtext.fontset"] = "custom"
plt.rcParams["mathtext.rm"] = "Georgia"
plt.rcParams["mathtext.it"] = "Georgia:italic"
plt.rcParams["mathtext.bf"] = "Georgia:bold"

import deepxube  # noqa: F401
from deepxube.base.domain import StateGoalVizable
from deepxube.base.pathfinding import get_path
from deepxube.factories.pathfinding_factory import get_pathfind_functions
from deepxube.nnet import nnet_utils
from deepxube.utils.command_line_utils import (
    get_domain_from_arg,
    get_heur_nnet_par_from_arg,
    get_pathfind_from_arg,
    get_pathfind_name_kwargs,
)
from torch import nn


BLACK_90 = "#363636"
BLACK_10 = "#ECECEC"
WHITE = "#FFFFFF"


@dataclass(frozen=True)
class DemoConfig:
    key: str
    domain: str
    steps: int
    figsize: tuple[float, float]


@dataclass(frozen=True)
class ModelConfig:
    heur: str
    model_file: str
    scramble_steps: int
    pathfind: str = "graph_v.1B"
    search_step_cap: int = 500


DEMO_CONFIGS: dict[str, DemoConfig] = {
    "hanoi": DemoConfig("hanoi", "hanoi.6.3", 14, (6.0, 5.0)),
    "pancake": DemoConfig("pancake", "pancake.10", 12, (6.0, 5.0)),
    "linkage": DemoConfig("linkage", "linkage.64_64_64", 14, (7.0, 6.0)),
    "mapf": DemoConfig("mapf", "mapf.28_28_30_64", 12, (8.0, 8.0)),
    "arm": DemoConfig("arm", "arm.6_12_8", 12, (6.5, 6.0)),
    "retro": DemoConfig("retro", "retro.7", 12, (7.0, 5.5)),
}


MODEL_CONFIGS: dict[str, ModelConfig] = {
    "hanoi": ModelConfig("resnet_fc.512H_3B_bn", "runs/models/hanoi/model.pt", 50),
    "pancake": ModelConfig("resnet_fc.1024H_4B_bn", "runs/models/pancake/model.pt", 20),
    "arm": ModelConfig("resnet_fc.1024H_4B_bn", "runs/models/arm/model.pt", 20),
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
    parser.add_argument(
        "--use-model",
        action="store_true",
        help="Render the trained-agent solution path instead of a random walk.",
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path("runs/models"),
        help="Root directory containing <domain>/model.pt files.",
    )
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


def _solve_with_model(
    domain: Any,
    domain_name: str,
    model_cfg: ModelConfig,
    model_file: Path,
) -> tuple[List[Any], Any]:
    heur_par = get_heur_nnet_par_from_arg(domain, domain_name, model_cfg.heur, "V")[0]
    device, _, _ = nnet_utils.get_device()
    nnet: nn.Module = nnet_utils.load_nnet(str(model_file), heur_par.get_nnet())
    nnet.eval()
    nnet.to(device)
    nnet = nn.DataParallel(nnet)
    heur_fn = heur_par.get_nnet_fn(nnet, None, device, None)

    pathfind_name = get_pathfind_name_kwargs(model_cfg.pathfind)[0]
    pathfind_functions = get_pathfind_functions(pathfind_name, heur_fn, None)

    states, goals = domain.sample_problem_instances([model_cfg.scramble_steps])
    start_state, goal = states[0], goals[0]

    pathfind = get_pathfind_from_arg(domain, pathfind_functions, model_cfg.pathfind)[0]
    instance = pathfind.make_instances([start_state], [goal], None, True)[0]
    pathfind.add_instances([instance])

    steps_taken = 0
    while not instance.finished() and steps_taken < model_cfg.search_step_cap:
        pathfind.step(verbose=False)
        steps_taken += 1

    goal_node = instance.goal_node
    if goal_node is None:
        raise RuntimeError(
            f"search did not solve instance within {model_cfg.search_step_cap} steps"
        )

    path_states, _, _ = get_path(goal_node)
    return path_states, goal


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
    draw = ImageDraw.Draw(copied)
    w, h = copied.size
    draw.rectangle([(0, 0), (w - 1, h - 1)], outline=(0, 0, 0, 255), width=1)
    return copied


def _render_frame(
    domain: StateGoalVizable,
    state: Any,
    goal: Any,
    step_idx: int,
    total_steps: int,
    config: DemoConfig,
    dpi: int,
    show_title: bool = False,
) -> Image.Image:
    fig = plt.figure(figsize=config.figsize, facecolor=WHITE)
    domain.visualize_state_goal(state, goal, fig)
    fig.text(
        0.5,
        0.02,
        str(step_idx),
        ha="center",
        va="bottom",
        color=BLACK_90,
        fontsize=14,
        family="Georgia",
    )
    if show_title:
        fig.text(
            0.5,
            0.5,
            "START",
            ha="center",
            va="center",
            color="black",
            fontsize=28,
            family="Georgia",
            fontweight="bold",
            bbox={
                "facecolor": "#CED318",
                "edgecolor": "black",
                "linewidth": 1.2,
                "pad": 12,
                "boxstyle": "square,pad=0.6",
            },
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
    use_model: bool = False,
    model_dir: Path = Path("runs/models"),
) -> Path:
    np.random.seed(seed)
    domain, domain_name = get_domain_from_arg(config.domain)
    if not isinstance(domain, StateGoalVizable):
        raise TypeError(f"{config.domain} does not provide a state-goal visualizer")

    path: List[Any]
    goal: Any
    used_model = False
    if use_model:
        model_cfg = MODEL_CONFIGS.get(config.key)
        model_file = (model_dir / config.key / "model.pt") if model_cfg else None
        if model_cfg is None:
            print(f"[{config.key}] no model config registered; falling back to random walk")
        elif not model_file.is_file():
            print(f"[{config.key}] model file {model_file} not found; falling back to random walk")
        else:
            try:
                import torch
                torch.manual_seed(seed)
                path, goal = _solve_with_model(domain, domain_name, model_cfg, model_file)
                used_model = True
                print(f"[{config.key}] solved with trained model in {len(path) - 1} steps")
            except Exception as exc:
                print(f"[{config.key}] model solve failed ({exc}); falling back to random walk")

    if not used_model:
        state_goal, goal = _sample_goal_pair(domain)
        path = _walk_from_goal(
            domain,
            state_goal,
            config.steps if steps is None else steps,
            action_retries,
        )
    total_steps = len(path) - 1
    frames = [
        _render_frame(domain, state, goal, idx, total_steps, config, dpi,
                      show_title=(idx == 0))
        for idx, state in enumerate(path)
    ]

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{config.key}_gif_demo.gif"
    duration_ms = max(1, int(round(1000.0 / fps)))
    durations = [duration_ms] * len(frames)
    durations[0] = duration_ms * 2
    durations[-1] = duration_ms * 3
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
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
            use_model=args.use_model,
            model_dir=args.model_dir,
        )
        print(f"wrote {out_path}")


def main_for_domain(key: str) -> None:
    import sys

    main([key, *sys.argv[1:]])


if __name__ == "__main__":
    main()
