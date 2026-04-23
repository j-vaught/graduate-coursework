"""
Train and solve script for the Retrosynthesis domain.

Usage:
    python train_retro.py train [--step_max 20] [--max_itrs 50000] [--dir training/retro]
    python train_retro.py solve --file retro_test_easy.pkl [--dir training/retro]
    python train_retro.py generate [--num 100] [--step_min 5] [--step_max 30] [--file retro_test.pkl]
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "deepxube"))

import argparse
import pickle
import time
import numpy as np
from typing import List, Optional

import deepxube.domains
import deepxube.heuristics
import deepxube.pathfinding

from deepxube.utils.command_line_utils import (
    get_domain_from_arg, get_heur_nnet_par_from_arg,
)
from deepxube.factories.updater_factory import get_updater
from deepxube.base.updater import UpArgs, UpdateHeur
from deepxube.base.trainer import TrainArgs
from deepxube.base.domain import State, Goal
from deepxube.trainers.utils.train_loop import TestArgs, train
from deepxube._solve import solve_cli


def cmd_train(args: argparse.Namespace) -> None:
    domain, domain_name = get_domain_from_arg(args.domain)
    heur_par, _ = get_heur_nnet_par_from_arg(domain, domain_name, args.heur, "V")

    up_args = UpArgs(
        args.procs, args.up_itrs, args.step_max, args.search_itrs,
        ub_heur_solns=False, backup=1,
        policy_rand_prob=0.0, up_gen_itrs=args.up_gen_itrs,
        up_batch_size=args.up_batch_size,
        nnet_batch_size=args.up_nnet_batch_size,
        sync_main=False, v=False,
    )
    update_heur: UpdateHeur = get_updater(domain, args.pathfind, up_args, args.her, "heur")

    train_args = TrainArgs(
        args.batch_size, args.lr, args.lr_d, args.max_itrs,
        balance_steps=args.bal, rb=args.rb, loss_thresh=np.inf,
        skip_heur=False, skip_policy=True, display=0,
    )

    test_args: Optional[TestArgs] = None
    if args.t_file is not None:
        data = pickle.load(open(args.t_file, "rb"))
        states: List[State] = data["states"]
        goals: List[Goal] = data["goals"]
        test_args = TestArgs(
            states, goals, args.t_search_itrs,
            args.t_pathfinds.split(","),
            args.up_nnet_batch_size, args.t_up_freq, args.t_init,
        )

    train(domain, heur_par, update_heur, None, None, args.dir, train_args,
          test_args=test_args, debug=args.debug)


def cmd_solve(args: argparse.Namespace) -> None:
    ns = argparse.Namespace(
        domain=args.domain,
        heur=args.heur,
        heur_type="V",
        policy=None,
        policy_samp=10,
        policy_rand=5,
        pathfind=args.pathfind,
        dir=args.dir,
        file=args.file,
        search_itrs=args.search_itrs,
        nnet_batch_size=10000,
    )
    solve_cli(ns)


def cmd_generate(args: argparse.Namespace) -> None:
    domain, _ = get_domain_from_arg(args.domain)
    num_steps = list(np.random.randint(args.step_min, args.step_max + 1, size=args.num))
    print(f"Generating {args.num} problem instances (steps {args.step_min}-{args.step_max})...")
    t0 = time.time()
    states, goals = domain.sample_problem_instances(num_steps)
    print(f"Generated in {time.time() - t0:.2f}s")
    data = {"states": states, "goals": goals}
    pickle.dump(data, open(args.file, "wb"), protocol=-1)
    print(f"Saved to {args.file}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrosynthesis training/solving")
    sub = parser.add_subparsers(dest="cmd")

    p_train = sub.add_parser("train")
    p_train.add_argument("--domain", default="retro.5")
    p_train.add_argument("--heur", default="resnet_fc.500H_4B")
    p_train.add_argument("--pathfind", default="graph_v")
    p_train.add_argument("--dir", default="training/retro")
    p_train.add_argument("--step_max", type=int, default=20)
    p_train.add_argument("--max_itrs", type=int, default=50000)
    p_train.add_argument("--batch_size", type=int, default=1000)
    p_train.add_argument("--lr", type=float, default=0.001)
    p_train.add_argument("--lr_d", type=float, default=0.9999993)
    p_train.add_argument("--procs", type=int, default=1)
    p_train.add_argument("--up_itrs", type=int, default=100)
    p_train.add_argument("--up_gen_itrs", type=int, default=100)
    p_train.add_argument("--up_batch_size", type=int, default=100)
    p_train.add_argument("--up_nnet_batch_size", type=int, default=10000)
    p_train.add_argument("--search_itrs", type=int, default=500)
    p_train.add_argument("--her", action="store_true", default=False)
    p_train.add_argument("--bal", action="store_true", default=False)
    p_train.add_argument("--rb", type=int, default=0)
    p_train.add_argument("--t_file", default="retro_test_easy.pkl")
    p_train.add_argument("--t_search_itrs", type=int, default=200)
    p_train.add_argument("--t_pathfinds", default="graph_v")
    p_train.add_argument("--t_up_freq", type=int, default=10)
    p_train.add_argument("--t_init", action="store_true", default=False)
    p_train.add_argument("--debug", action="store_true", default=False)

    p_solve = sub.add_parser("solve")
    p_solve.add_argument("--domain", default="retro.5")
    p_solve.add_argument("--heur", default="resnet_fc.500H_4B")
    p_solve.add_argument("--pathfind", default="graph_v")
    p_solve.add_argument("--dir", default="training/retro")
    p_solve.add_argument("--file", required=True)
    p_solve.add_argument("--search_itrs", type=int, default=1000)

    p_gen = sub.add_parser("generate")
    p_gen.add_argument("--domain", default="retro.5")
    p_gen.add_argument("--num", type=int, default=100)
    p_gen.add_argument("--step_min", type=int, default=5)
    p_gen.add_argument("--step_max", type=int, default=30)
    p_gen.add_argument("--file", default="retro_test.pkl")

    args = parser.parse_args()
    if args.cmd == "train":
        cmd_train(args)
    elif args.cmd == "solve":
        cmd_solve(args)
    elif args.cmd == "generate":
        cmd_generate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
