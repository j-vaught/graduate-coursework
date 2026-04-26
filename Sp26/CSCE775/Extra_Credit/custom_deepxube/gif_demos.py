"""Generate consistent GIF demos for the custom DeepXube domains."""

from __future__ import annotations

import argparse
import io
from collections import deque
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
    goal_hint: tuple[float, float, float] | None = None
    start_joints: tuple[int, ...] | None = None
    min_goal_distance: int | None = None
    sample_attempts: int = 1


DEMO_CONFIGS: dict[str, DemoConfig] = {
    "hanoi": DemoConfig("hanoi", "hanoi.6.3", 14, (6.0, 5.0)),
    "pancake": DemoConfig("pancake", "pancake.10", 12, (6.0, 5.0)),
    "mapf": DemoConfig("mapf", "mapf.28_28_4_64", 12, (8.0, 8.0)),
    "mapf30": DemoConfig("mapf30", "mapf.28_28_30_256_dist", 12, (8.0, 8.0)),
    "mapf60": DemoConfig("mapf60", "mapf.28_28_60_256_dist", 12, (8.0, 8.0)),
    "arm": DemoConfig("arm", "arm.6_12_64", 12, (13.0, 5.0)),
    "retro": DemoConfig("retro", "retro.7", 12, (7.5, 6.0)),
}


MODEL_CONFIGS: dict[str, ModelConfig] = {
    "hanoi": ModelConfig("resnet_fc.512H_3B_bn", "runs/models/hanoi/model.pt", 50),
    "pancake": ModelConfig("resnet_fc.1024H_4B_bn", "runs/models/pancake/model.pt", 20),
    "mapf": ModelConfig(
        "resnet_fc.128H_2B_bn", "runs/models/mapf4/model.pt", 20,
        search_step_cap=5000,
    ),
    "mapf30": ModelConfig(
        "resnet_2d.32C_2B_bn", "runs/models/mapf30_dist/model.pt", 40,
        search_step_cap=5000,
        min_goal_distance=20,
        sample_attempts=5,
    ),
    "mapf60": ModelConfig(
        "resnet_2d.32C_2B_bn", "runs/models/mapf60_dist/model.pt", 40,
        search_step_cap=5000,
        min_goal_distance=20,
        sample_attempts=5,
    ),
    "arm": ModelConfig(
        "resnet_fc.1024H_4B_bn", "runs/models/arm_64bins/model.pt", 30,
        goal_hint=(2.0, -2.0, -2.0),
        search_step_cap=1000,
    ),
    "retro": ModelConfig("resnet_fc.1024H_4B_bn", "runs/models/retro/model.pt", 30),
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


def _sample_problem(domain: Any, model_cfg: ModelConfig) -> tuple[Any, Any]:
    if model_cfg.min_goal_distance is not None and hasattr(domain, "_distance_maps_for_state"):
        return _sample_mapf_problem(domain, model_cfg.min_goal_distance)
    if model_cfg.goal_hint is not None and hasattr(domain, "_ee_position"):
        from domains.robotic_arm import ArmGoal, ArmState
        target = np.asarray(model_cfg.goal_hint, dtype=np.float64)
        n_joints = getattr(domain, "n_joints", 6)
        n_steps = getattr(domain, "n_angle_steps", 12)
        best_joints = None
        best_dist = np.inf
        for _ in range(200000):
            joints = np.random.randint(0, n_steps, size=n_joints).astype(np.int8)
            if not domain._is_valid_state(joints):
                continue
            ee = domain._ee_position(joints)
            dist = float(np.linalg.norm(ee - target))
            if dist < best_dist:
                best_dist = dist
                best_joints = joints
                if best_dist < 1e-3:
                    break
        if best_joints is not None:
            goal_ee = domain._ee_position(best_joints)
            goal = ArmGoal(domain._position_to_bins(goal_ee))
            seed_state = ArmState(best_joints)
            start_states = domain.random_walk_rev([seed_state], [model_cfg.scramble_steps])
            print(f"[arm] goal bin {tuple(goal.bins.tolist())} at {domain._bins_to_position(goal.bins)} "
                  f"(dist {best_dist:.3f} from {tuple(target.tolist())})")
            return start_states[0], goal
    states, goals = domain.sample_problem_instances([model_cfg.scramble_steps])
    return states[0], goals[0]


def _sample_mapf_problem(domain: Any, min_goal_distance: int) -> tuple[Any, Any]:
    from domains.warehouse_mapf import MAPFState

    dist_inf = int(np.iinfo(np.int16).max)
    for _attempt in range(200):
        states_goal, goals = domain.sample_goalstate_goal_pairs(1)
        goal = goals[0]
        goal_positions = goal.positions.copy()
        goal_cells = domain._goal_cells_from_goal(goal)
        goal_state = MAPFState(goal_positions.copy(), goal_positions.copy())
        dist_maps = domain._distance_maps_for_state(goal_state, goal_cells)

        positions = np.zeros_like(goal_positions)
        occupied: set[tuple[int, int]] = set()
        per_robot_distances: list[int] = []
        ok = True
        for robot_idx in range(domain.K):
            near_candidates: list[tuple[int, int, int]] = []
            far_candidates: list[tuple[int, int, int]] = []
            for r, c in domain.free_cells:
                if (r, c) in occupied:
                    continue
                dist = int(dist_maps[robot_idx][r, c])
                if dist >= dist_inf or dist < min_goal_distance:
                    continue
                candidate = (dist, r, c)
                far_candidates.append(candidate)
                if dist <= min_goal_distance + 12:
                    near_candidates.append(candidate)

            candidates = near_candidates if near_candidates else far_candidates
            if not candidates:
                ok = False
                break

            dist, r, c = candidates[np.random.randint(len(candidates))]
            occupied.add((r, c))
            domain._set_pos(positions, robot_idx, r, c)
            per_robot_distances.append(dist)

        if ok:
            start_state = MAPFState(positions, goal_positions.copy())
            print(
                f"[mapf] per-robot dock distance "
                f"min/mean/max: {min(per_robot_distances)}/"
                f"{float(np.mean(per_robot_distances)):.1f}/"
                f"{max(per_robot_distances)}"
            )
            return start_state, goal

    raise RuntimeError(
        f"could not sample MAPF problem with every robot at least "
        f"{min_goal_distance} steps from its dock"
    )


def _mapf_goal_distances(domain: Any, state: Any, goal: Any) -> list[int]:
    from domains.warehouse_mapf import MAPFState

    dist_inf = int(np.iinfo(np.int16).max)
    goal_cells = domain._goal_cells_from_goal(goal)
    state_for_goal = MAPFState(state.positions, goal.positions.copy())
    dist_maps = domain._distance_maps_for_state(state_for_goal, goal_cells)

    dists: list[int] = []
    for robot_idx in range(domain.K):
        r, c = domain._get_pos(state, robot_idx)
        dist = int(dist_maps[robot_idx][r, c])
        dists.append(domain.H + domain.W if dist >= dist_inf else dist)
    return dists


def _plan_single_reserved_mapf_path(
    domain: Any,
    start_cell: tuple[int, int],
    goal_cell: tuple[int, int],
    robot_idx: int,
    goal_cells: dict[tuple[int, int], int],
    reserved_vertices: set[tuple[int, int]],
    reserved_edges: set[tuple[int, int, int]],
    horizon: int,
) -> list[tuple[int, int]] | None:
    from domains.warehouse_mapf import DIR_OFFSETS

    start_flat = start_cell[0] * domain.W + start_cell[1]
    goal_flat = goal_cell[0] * domain.W + goal_cell[1]
    start_key = (0, start_flat)
    queue: deque[tuple[int, int]] = deque([start_key])
    parent: dict[tuple[int, int], tuple[int, int] | None] = {start_key: None}

    while queue:
        time_idx, cell_flat = queue.popleft()
        if cell_flat == goal_flat:
            path_cells: list[tuple[int, int]] = []
            key: tuple[int, int] | None = (time_idx, cell_flat)
            while key is not None:
                _, flat = key
                path_cells.append(divmod(flat, domain.W))
                key = parent[key]
            return path_cells[::-1]

        if time_idx >= horizon:
            continue

        r, c = divmod(cell_flat, domain.W)
        next_time = time_idx + 1
        for dr, dc in DIR_OFFSETS:
            nr, nc = r + dr, c + dc
            if not domain._is_passable(nr, nc, robot_idx, goal_cells):
                continue

            next_flat = nr * domain.W + nc
            if (next_time, next_flat) in reserved_vertices:
                continue
            if (next_time, next_flat, cell_flat) in reserved_edges:
                continue

            next_key = (next_time, next_flat)
            if next_key in parent:
                continue

            parent[next_key] = (time_idx, cell_flat)
            queue.append(next_key)

    return None


def _build_reserved_mapf_path(
    domain: Any,
    start_state: Any,
    goal: Any,
    order: list[int],
    horizon: int,
) -> list[Any] | None:
    from domains.warehouse_mapf import MAPFState

    goal_cells = domain._goal_cells_from_goal(goal)
    reserved_vertices: set[tuple[int, int]] = set()
    reserved_edges: set[tuple[int, int, int]] = set()
    robot_paths: list[list[tuple[int, int]] | None] = [None] * domain.K

    for robot_idx in order:
        path_cells = _plan_single_reserved_mapf_path(
            domain,
            domain._get_pos(start_state, robot_idx),
            domain._get_goal_pos(goal, robot_idx),
            robot_idx,
            goal_cells,
            reserved_vertices,
            reserved_edges,
            horizon,
        )
        if path_cells is None:
            return None

        robot_paths[robot_idx] = path_cells
        for time_idx, (r, c) in enumerate(path_cells):
            cell_flat = r * domain.W + c
            reserved_vertices.add((time_idx, cell_flat))
            if time_idx > 0:
                pr, pc = path_cells[time_idx - 1]
                prev_flat = pr * domain.W + pc
                reserved_edges.add((time_idx, prev_flat, cell_flat))

        gr, gc = path_cells[-1]
        goal_flat = gr * domain.W + gc
        for time_idx in range(len(path_cells), horizon + 1):
            reserved_vertices.add((time_idx, goal_flat))

    planned_paths = [path for path in robot_paths if path is not None]
    if len(planned_paths) != domain.K:
        return None

    num_frames = max(len(path) for path in planned_paths)
    states: list[Any] = []
    for time_idx in range(num_frames):
        positions = np.zeros_like(goal.positions)
        for robot_idx, path_cells in enumerate(planned_paths):
            r, c = path_cells[time_idx] if time_idx < len(path_cells) else path_cells[-1]
            domain._set_pos(positions, robot_idx, r, c)
        states.append(MAPFState(positions, goal.positions.copy()))

    for time_idx, state in enumerate(states):
        cells = [domain._get_pos(state, robot_idx) for robot_idx in range(domain.K)]
        if len(set(cells)) != domain.K:
            return None
        if time_idx == 0:
            continue
        prev_cells = [
            domain._get_pos(states[time_idx - 1], robot_idx)
            for robot_idx in range(domain.K)
        ]
        for robot_i in range(domain.K):
            for robot_j in range(robot_i + 1, domain.K):
                if cells[robot_i] == prev_cells[robot_j] and cells[robot_j] == prev_cells[robot_i]:
                    return None

    return states


def _try_shorten_mapf_path(domain: Any, path_states: list[Any], goal: Any,
                           domain_name: str) -> list[Any]:
    if len(path_states) < 2 or not hasattr(domain, "_distance_maps_for_state"):
        return path_states

    start_state = path_states[0]
    dists = _mapf_goal_distances(domain, start_state, goal)
    lower_bound = max(dists) if dists else 0
    horizon = max(lower_bound + (4 * domain.K), lower_bound + 80)

    rng = np.random.default_rng(775)
    orders: list[list[int]] = []
    seen_orders: set[tuple[int, ...]] = set()

    def add_order(order: list[int]) -> None:
        order_t = tuple(order)
        if order_t in seen_orders:
            return
        seen_orders.add(order_t)
        orders.append(order)

    add_order(sorted(range(domain.K), key=lambda idx: (-dists[idx], idx)))
    add_order(sorted(range(domain.K), key=lambda idx: (dists[idx], idx)))
    add_order(list(range(domain.K)))
    add_order(list(reversed(range(domain.K))))
    add_order(sorted(range(domain.K), key=lambda idx: (domain._get_goal_pos(goal, idx)[0], domain._get_goal_pos(goal, idx)[1], idx)))
    add_order(sorted(range(domain.K), key=lambda idx: (domain._get_goal_pos(goal, idx)[1], domain._get_goal_pos(goal, idx)[0], idx)))
    for _ in range(6):
        order = list(range(domain.K))
        rng.shuffle(order)
        add_order(order)

    best_path: list[Any] | None = None
    for order in orders:
        candidate = _build_reserved_mapf_path(domain, start_state, goal, order, horizon)
        if candidate is None:
            continue
        if best_path is None or len(candidate) < len(best_path):
            best_path = candidate
            if len(candidate) - 1 <= lower_bound:
                break

    if best_path is None or len(best_path) >= len(path_states):
        return path_states

    print(
        f"[{domain_name}] MAPF path polish shortened "
        f"{len(path_states) - 1} -> {len(best_path) - 1} steps "
        f"(lower bound {lower_bound})"
    )
    return best_path


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

    for sample_attempt in range(max(1, model_cfg.sample_attempts)):
        start_state, goal = _sample_problem(domain, model_cfg)

        pathfind = get_pathfind_from_arg(domain, pathfind_functions, model_cfg.pathfind)[0]
        instance = pathfind.make_instances([start_state], [goal], None, True)[0]
        pathfind.add_instances([instance])

        steps_taken = 0
        while not instance.finished() and steps_taken < model_cfg.search_step_cap:
            pathfind.step(verbose=False)
            steps_taken += 1

        goal_node = instance.goal_node
        if goal_node is not None:
            path_states, _, _ = get_path(goal_node)
            path_states = _try_shorten_mapf_path(domain, path_states, goal, domain_name)
            if sample_attempt > 0:
                print(f"[{domain_name}] solved sampled problem on attempt {sample_attempt + 1}")
            return path_states, goal

        print(
            f"[{domain_name}] sampled problem attempt {sample_attempt + 1} "
            f"not solved within {model_cfg.search_step_cap} search steps"
        )

    raise RuntimeError(
        f"search did not solve instance within {model_cfg.search_step_cap} steps"
    )


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
        if model_cfg is not None and model_cfg.model_file:
            model_file = Path(model_cfg.model_file)
        elif model_cfg is not None:
            model_file = model_dir / config.key / "model.pt"
        else:
            model_file = None
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
