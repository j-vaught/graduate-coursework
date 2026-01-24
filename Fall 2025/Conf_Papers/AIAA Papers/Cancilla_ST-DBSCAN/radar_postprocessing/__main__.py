"""
Main entry point for running radar_postprocessing as a module.

Usage:
    python -m radar_postprocessing process --input ./data --output ./out --config config.toml
    python -m radar_postprocessing convert --input ./data.csv --output ./data.npy
    python -m radar_postprocessing evaluate --predictions ./pred.json --ground-truth ./gt.json
    python -m radar_postprocessing info
"""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
