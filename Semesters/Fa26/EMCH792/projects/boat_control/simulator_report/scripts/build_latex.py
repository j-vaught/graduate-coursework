"""Compile standalone Typst figures, then the editable LaTeX simulator report."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
FIGURES = PROJECT / "simulator_report" / "figures" / "standalone"
BUILD = PROJECT / "build" / "simulator-report-latex"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skip-figures", action="store_true", help="Reuse compiled figure PDFs")
    parser.add_argument(
        "--figures-only", action="store_true", help="Compile only the Typst figures"
    )
    args = parser.parse_args()
    if args.skip_figures and args.figures_only:
        parser.error("Choose either --skip-figures or --figures-only")
    if not args.skip_figures:
        for source in sorted(FIGURES.glob("*.typ")):
            subprocess.run(
                [
                    "typst",
                    "compile",
                    "--root",
                    str(PROJECT),
                    str(source),
                    str(source.with_suffix(".pdf")),
                ],
                cwd=PROJECT,
                check=True,
            )
            print(f"Compiled {source.name}", flush=True)
    if args.figures_only:
        return
    BUILD.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "latexmk",
            "-pdf",
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-outdir={BUILD}",
            "simulator_report.tex",
        ],
        cwd=PROJECT,
        check=True,
    )
    shutil.copy2(BUILD / "simulator_report.pdf", PROJECT / "simulator_report.pdf")
    print(f"Wrote {PROJECT / 'simulator_report.pdf'}")


if __name__ == "__main__":
    main()
