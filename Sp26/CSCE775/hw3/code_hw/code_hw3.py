from typing import Dict, List, Optional, Tuple
from environments.environment_abstract import Environment, State
import heapq

import numpy as np
import torch
from torch import nn


_BATCH_SIZE = 4
_WEIGHT = 5.0
_MAX_HEURISTIC_CACHE_SIZE = 250_000
_MAX_TERMINAL_CACHE_SIZE = 250_000

_HEURISTIC_CACHE: Dict[Tuple[int, int], Dict[State, float]] = {}
_TERMINAL_CACHE: Dict[int, Dict[State, bool]] = {}


def _reconstruct_path(parent: Dict[State, Tuple[State, int]], state: State) -> List[int]:
    actions: List[int] = []
    while state in parent:
        state, action = parent[state]
        actions.append(action)
    actions.reverse()
    return actions


def _get_terminal_cached(state: State, is_terminal, terminal_cache: Dict[State, bool]) -> bool:
    cached = terminal_cache.get(state)
    if cached is not None:
        return cached

    solved = is_terminal(state)
    if len(terminal_cache) >= _MAX_TERMINAL_CACHE_SIZE:
        terminal_cache.clear()
    terminal_cache[state] = solved
    return solved


def search(env: Environment, state_start: State, nnet: nn.Module) -> Optional[List[int]]:
    """Find a path from the start state to a goal using batched weighted A*."""

    is_terminal = env.is_terminal
    if is_terminal(state_start):
        return []

    get_actions = env.get_actions
    state_action_dynamics = env.state_action_dynamics
    param = next(nnet.parameters(), None)
    device = param.device if param is not None else torch.device("cpu")
    inf = float("inf")
    heappush = heapq.heappush
    heappop = heapq.heappop

    heuristic_cache_key = (id(env), id(nnet))
    heuristic_cache = _HEURISTIC_CACHE.setdefault(heuristic_cache_key, {})
    if len(heuristic_cache) >= _MAX_HEURISTIC_CACHE_SIZE:
        heuristic_cache.clear()

    terminal_cache = _TERMINAL_CACHE.setdefault(id(env), {})
    if len(terminal_cache) >= _MAX_TERMINAL_CACHE_SIZE:
        terminal_cache.clear()

    def heuristic(states: List[State]) -> np.ndarray:
        values = np.empty(len(states), dtype=np.float32)
        missing_indices: List[int] = []
        missing_states: List[State] = []

        for idx, state in enumerate(states):
            cached = heuristic_cache.get(state)
            if cached is None:
                missing_indices.append(idx)
                missing_states.append(state)
            else:
                values[idx] = cached

        if missing_states:
            nnet_input = env.states_to_nnet_input(missing_states)
            tensor = torch.from_numpy(nnet_input)
            if device.type != "cpu":
                tensor = tensor.to(device)

            heuristics = torch.clamp(-nnet(tensor).amax(dim=1), min=0.0).cpu().numpy()

            if len(heuristic_cache) + len(missing_states) >= _MAX_HEURISTIC_CACHE_SIZE:
                heuristic_cache.clear()

            for idx, state, h_val in zip(missing_indices, missing_states, heuristics):
                heuristic_value = float(h_val)
                heuristic_cache[state] = heuristic_value
                values[idx] = heuristic_value

        return values

    parent: Dict[State, Tuple[State, int]] = {}
    best_g: Dict[State, float] = {state_start: 0.0}
    closed = set()

    with torch.inference_mode():
        start_h = float(heuristic([state_start])[0])
        heap = [(start_h, 0, state_start, 0.0)]
        counter = 1

        while heap:
            batch: List[Tuple[State, float]] = []
            while heap and len(batch) < _BATCH_SIZE:
                _, _, state, g = heappop(heap)

                if state in closed or g > best_g.get(state, inf):
                    continue

                if _get_terminal_cached(state, is_terminal, terminal_cache):
                    return _reconstruct_path(parent, state)

                batch.append((state, g))

            if not batch:
                continue

            pending_best_g: Dict[State, float] = {}
            for state, g in batch:
                if state in closed:
                    continue

                closed.add(state)

                for action in get_actions(state):
                    reward, next_states, _ = state_action_dynamics(state, action)
                    if not next_states:
                        continue

                    next_state = next_states[0]
                    if next_state in closed:
                        continue

                    new_g = g - reward
                    if new_g >= best_g.get(next_state, inf):
                        continue

                    best_g[next_state] = new_g
                    parent[next_state] = (state, action)

                    if _get_terminal_cached(next_state, is_terminal, terminal_cache):
                        return _reconstruct_path(parent, next_state)

                    pending_g = pending_best_g.get(next_state)
                    if pending_g is None or new_g < pending_g:
                        pending_best_g[next_state] = new_g

            if not pending_best_g:
                continue

            pending_states = list(pending_best_g)
            h_vals = heuristic(pending_states)
            for next_state, h_val in zip(pending_states, h_vals):
                next_g = pending_best_g[next_state]
                heappush(heap, (next_g + _WEIGHT * float(h_val), counter, next_state, next_g))
                counter += 1

    return None
