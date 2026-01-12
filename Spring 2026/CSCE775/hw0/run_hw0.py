import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.environments.farm_grid_world import FarmGridWorld
from shared.visualizer.farm_visualizer import InteractiveFarm, load_grid

from argparse import ArgumentParser


def main():
    parser: ArgumentParser = ArgumentParser()
    parser.add_argument('--map', type=str, required=True, help="")

    args = parser.parse_args()

    grid = load_grid(args.map)
    env: FarmGridWorld = FarmGridWorld("aifarm", grid.shape, 0.0)

    viz: InteractiveFarm = InteractiveFarm(env, grid)

    viz.mainloop()


if __name__ == "__main__":
    main()
