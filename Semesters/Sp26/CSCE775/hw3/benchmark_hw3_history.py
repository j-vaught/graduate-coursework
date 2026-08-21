#!/usr/bin/env python3
import argparse
import csv
import json
import os
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import tempfile
from typing import Any, Dict, List

from PIL import Image, ImageDraw, ImageFont


PRIMARY_GARNET = "#73000A"
PRIMARY_BLACK = "#000000"
PRIMARY_WHITE = "#FFFFFF"
NEUTRAL_90 = "#363636"
NEUTRAL_70 = "#5C5C5C"
NEUTRAL_30 = "#C7C7C7"
NEUTRAL_10 = "#ECECEC"
ACCENT_ATLANTIC = "#466A9F"
ACCENT_CONGAREE = "#1F414D"

RUNNER_CODE = r"""
import contextlib
import io
import json
import os
import re
import sys

import numpy as np

hw3_dir = sys.argv[1]
os.chdir(hw3_dir)
np.random.seed(42)
sys.argv = ["run_hw3.py", "--grade"]

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import run_hw3
    run_hw3.main()

out = buf.getvalue().strip()
pat = re.compile(
    r"Average difference with optimal path cost: ([^,]+), %Solved: ([^%]+)%, %Optimal: ([^%]+)%, Total time: ([0-9.]+) secs"
)
m = pat.search(out)
if not m:
    raise SystemExit(f"Could not parse run_hw3 output: {out}")

print(
    json.dumps(
        {
            "avg_diff": float(m.group(1)),
            "pct_solved": float(m.group(2)),
            "pct_optimal": float(m.group(3)),
            "total_time_secs": float(m.group(4)),
            "raw_output": out,
        }
    )
)
"""


def run(cmd: List[str], cwd: Path, env: Dict[str, str] | None = None) -> str:
    proc = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout


def git_lines(repo_root: Path, args: List[str]) -> List[str]:
    out = run(["git", *args], cwd=repo_root)
    return [line for line in out.splitlines() if line.strip()]


def clean_hw3_artifacts(worktree_root: Path, hw3_rel: Path) -> None:
    hw3_dir = worktree_root / hw3_rel
    for path in hw3_dir.rglob("__pycache__"):
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    for path in (hw3_dir / "code_hw").glob("_cheapq*.so"):
        path.unlink(missing_ok=True)
    for path in (hw3_dir / "code_hw").glob("*.dylib"):
        path.unlink(missing_ok=True)
    for path in (hw3_dir / "code_hw").glob("*.o"):
        path.unlink(missing_ok=True)


def benchmark_once(hw3_dir: Path) -> Dict[str, Any]:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    proc = subprocess.run(
        [sys.executable, "-c", RUNNER_CODE, str(hw3_dir)],
        cwd=hw3_dir,
        env=env,
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(proc.stdout)


def get_commit_rows(repo_root: Path, hw3_rel: Path, baseline: str) -> List[Dict[str, str]]:
    lines = git_lines(
        repo_root,
        [
            "log",
            "--reverse",
            "--format=%H\t%h\t%ad\t%s",
            "--date=short",
            "--",
            str(hw3_rel / "code_hw" / "code_hw3.py"),
        ],
    )
    rows: List[Dict[str, str]] = []
    started = False
    for line in lines:
        full_sha, short_sha, date_str, subject = line.split("\t", 3)
        if full_sha.startswith(baseline) or short_sha.startswith(baseline):
            started = True
        if started:
            rows.append(
                {
                    "full_sha": full_sha,
                    "short_sha": short_sha,
                    "date": date_str,
                    "subject": subject,
                }
            )
    if not rows:
        raise ValueError(f"Baseline commit {baseline} not found in HW3 history")
    return rows


def draw_plot(summary_rows: List[Dict[str, Any]], out_path: Path) -> None:
    width = 1800
    height = 1000
    margin_left = 130
    margin_right = 60
    margin_top = 90
    margin_bottom = 250
    chart_left = margin_left
    chart_top = margin_top
    chart_right = width - margin_right
    chart_bottom = height - margin_bottom
    chart_width = chart_right - chart_left
    chart_height = chart_bottom - chart_top

    image = Image.new("RGB", (width, height), PRIMARY_WHITE)
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 18)
        small_font = ImageFont.truetype("DejaVuSans.ttf", 16)
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 26)
    except OSError:
        font = ImageFont.load_default()
        small_font = font
        title_font = font

    means = [row["mean_total_time_secs"] for row in summary_rows]
    max_mean = max(means)
    max_std = max(row["std_total_time_secs"] for row in summary_rows)
    y_max = max_mean + max_std
    y_max *= 1.15
    y_max = max(y_max, 1.0)

    def x_pos(idx: int) -> float:
        if len(summary_rows) == 1:
            return chart_left + chart_width / 2
        return chart_left + idx * chart_width / (len(summary_rows) - 1)

    def y_pos(val: float) -> float:
        return chart_bottom - (val / y_max) * chart_height

    for tick in range(6):
        value = y_max * tick / 5
        y = y_pos(value)
        draw.line((chart_left, y, chart_right, y), fill=NEUTRAL_30, width=1)
        label = f"{value:.1f}s"
        draw.text((chart_left - 72, y - 10), label, fill=NEUTRAL_70, font=small_font)

    draw.line((chart_left, chart_top, chart_left, chart_bottom), fill=PRIMARY_BLACK, width=3)
    draw.line((chart_left, chart_bottom, chart_right, chart_bottom), fill=PRIMARY_BLACK, width=3)

    point_xy: List[tuple[float, float]] = []
    for idx, row in enumerate(summary_rows):
        x = x_pos(idx)
        mean_y = y_pos(row["mean_total_time_secs"])
        lo_y = y_pos(max(row["mean_total_time_secs"] - row["std_total_time_secs"], 0.0))
        hi_y = y_pos(row["mean_total_time_secs"] + row["std_total_time_secs"])

        draw.line((x, hi_y, x, lo_y), fill=PRIMARY_BLACK, width=2)
        draw.line((x - 8, hi_y, x + 8, hi_y), fill=PRIMARY_BLACK, width=2)
        draw.line((x - 8, lo_y, x + 8, lo_y), fill=PRIMARY_BLACK, width=2)

        jitter_offsets = [-18, -9, 0, 9, 18]
        for run_idx, t in enumerate(row["run_total_time_secs"]):
            rx = x + jitter_offsets[run_idx % len(jitter_offsets)]
            ry = y_pos(t)
            draw.rectangle((rx - 4, ry - 4, rx + 4, ry + 4), outline=ACCENT_ATLANTIC, fill=ACCENT_ATLANTIC)

        draw.rectangle((x - 6, mean_y - 6, x + 6, mean_y + 6), outline=PRIMARY_GARNET, fill=PRIMARY_GARNET)
        point_xy.append((x, mean_y))

        label = row["short_sha"]
        text_bbox = draw.textbbox((0, 0), label, font=small_font)
        label_x = x - (text_bbox[2] - text_bbox[0]) / 2
        draw.text((label_x, chart_bottom + 20), label, fill=PRIMARY_BLACK, font=small_font)

    if len(point_xy) >= 2:
        draw.line(point_xy, fill=PRIMARY_GARNET, width=4)

    title = "HW3 Weighted A* Runtime Across Commits"
    subtitle = "5 measured runs per commit on a fixed seeded state set. Error bars show one standard deviation."
    draw.text((chart_left, 24), title, fill=PRIMARY_BLACK, font=title_font)
    draw.text((chart_left, 58), subtitle, fill=NEUTRAL_70, font=font)
    draw.text((36, chart_top - 14), "Time", fill=PRIMARY_BLACK, font=font)
    draw.text((chart_right - 86, chart_bottom + 54), "Commit", fill=PRIMARY_BLACK, font=font)

    legend_x = chart_left
    legend_y = height - 135
    draw.rectangle((legend_x, legend_y, legend_x + 16, legend_y + 16), outline=PRIMARY_GARNET, fill=PRIMARY_GARNET)
    draw.text((legend_x + 24, legend_y), "Mean search time", fill=PRIMARY_BLACK, font=font)
    draw.rectangle((legend_x + 190, legend_y, legend_x + 206, legend_y + 16), outline=ACCENT_ATLANTIC, fill=ACCENT_ATLANTIC)
    draw.text((legend_x + 214, legend_y), "Individual run", fill=PRIMARY_BLACK, font=font)
    draw.line((legend_x + 360, legend_y + 8, legend_x + 390, legend_y + 8), fill=PRIMARY_BLACK, width=2)
    draw.line((legend_x + 375, legend_y + 2, legend_x + 375, legend_y + 14), fill=PRIMARY_BLACK, width=2)
    draw.text((legend_x + 400, legend_y), "±1 std. dev.", fill=PRIMARY_BLACK, font=font)

    baseline = summary_rows[0]["mean_total_time_secs"]
    fastest = min(summary_rows, key=lambda row: row["mean_total_time_secs"])
    summary_text = (
        f"Baseline {summary_rows[0]['short_sha']} mean {baseline:.3f}s. "
        f"Fastest {fastest['short_sha']} mean {fastest['mean_total_time_secs']:.3f}s. "
        f"Speedup {baseline / fastest['mean_total_time_secs']:.2f}x."
    )
    draw.text((chart_left, height - 95), summary_text, fill=ACCENT_CONGAREE, font=font)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(out_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", default="7023948", help="First commit in the final working HW3 line.")
    parser.add_argument("--repeats", type=int, default=5, help="Measured runs per commit.")
    parser.add_argument("--warmup-runs", type=int, default=1, help="Unmeasured warm-up runs per commit.")
    parser.add_argument("--output-dir", default="benchmark_results", help="Directory for CSV/PNG outputs.")
    args = parser.parse_args()

    hw3_dir = Path(__file__).resolve().parent
    repo_root = Path(run(["git", "rev-parse", "--show-toplevel"], cwd=hw3_dir).strip())
    hw3_rel = hw3_dir.relative_to(repo_root)
    commits = get_commit_rows(repo_root, hw3_rel, args.baseline)

    output_dir = hw3_dir / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    runs_csv = output_dir / "hw3_commit_benchmark_runs.csv"
    summary_csv = output_dir / "hw3_commit_benchmark_summary.csv"
    plot_png = output_dir / "hw3_commit_benchmark.png"
    report_txt = output_dir / "hw3_commit_benchmark_report.txt"

    worktree_parent = Path(tempfile.mkdtemp(prefix="hw3-history-bench-"))
    worktree_root = worktree_parent / "repo"

    results: List[Dict[str, Any]] = []

    try:
        run(["git", "worktree", "add", "--detach", str(worktree_root), commits[-1]["full_sha"]], cwd=repo_root)

        for idx, commit in enumerate(commits, start=1):
            print(f"[{idx}/{len(commits)}] {commit['short_sha']} {commit['subject']}", flush=True)
            run(["git", "checkout", "--detach", commit["full_sha"]], cwd=worktree_root)
            clean_hw3_artifacts(worktree_root, hw3_rel)

            bench_hw3_dir = worktree_root / hw3_rel
            for _ in range(args.warmup_runs):
                benchmark_once(bench_hw3_dir)

            measured: List[Dict[str, Any]] = []
            for run_idx in range(1, args.repeats + 1):
                result = benchmark_once(bench_hw3_dir)
                result["run_idx"] = run_idx
                measured.append(result)
                print(
                    f"  run {run_idx}/{args.repeats}: "
                    f"{result['total_time_secs']:.5f}s, "
                    f"optimal={result['pct_optimal']:.2f}%",
                    flush=True,
                )

            times = [row["total_time_secs"] for row in measured]
            optimals = [row["pct_optimal"] for row in measured]
            solved = [row["pct_solved"] for row in measured]
            diffs = [row["avg_diff"] for row in measured]

            results.append(
                {
                    **commit,
                    "run_total_time_secs": times,
                    "mean_total_time_secs": statistics.mean(times),
                    "std_total_time_secs": statistics.stdev(times) if len(times) > 1 else 0.0,
                    "mean_pct_optimal": statistics.mean(optimals),
                    "mean_pct_solved": statistics.mean(solved),
                    "mean_avg_diff": statistics.mean(diffs),
                    "measured_runs": measured,
                }
            )
    finally:
        try:
            run(["git", "worktree", "remove", "--force", str(worktree_root)], cwd=repo_root)
        except subprocess.CalledProcessError:
            pass
        shutil.rmtree(worktree_parent, ignore_errors=True)

    with runs_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "commit_index",
                "full_sha",
                "short_sha",
                "date",
                "subject",
                "run_idx",
                "total_time_secs",
                "pct_solved",
                "pct_optimal",
                "avg_diff",
            ]
        )
        for commit_idx, row in enumerate(results, start=1):
            for run_row in row["measured_runs"]:
                writer.writerow(
                    [
                        commit_idx,
                        row["full_sha"],
                        row["short_sha"],
                        row["date"],
                        row["subject"],
                        run_row["run_idx"],
                        f"{run_row['total_time_secs']:.5f}",
                        f"{run_row['pct_solved']:.5f}",
                        f"{run_row['pct_optimal']:.5f}",
                        f"{run_row['avg_diff']:.5f}",
                    ]
                )

    with summary_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "commit_index",
                "full_sha",
                "short_sha",
                "date",
                "subject",
                "mean_total_time_secs",
                "std_total_time_secs",
                "mean_pct_solved",
                "mean_pct_optimal",
                "mean_avg_diff",
                "speedup_vs_baseline",
            ]
        )
        baseline_mean = results[0]["mean_total_time_secs"]
        for commit_idx, row in enumerate(results, start=1):
            writer.writerow(
                [
                    commit_idx,
                    row["full_sha"],
                    row["short_sha"],
                    row["date"],
                    row["subject"],
                    f"{row['mean_total_time_secs']:.5f}",
                    f"{row['std_total_time_secs']:.5f}",
                    f"{row['mean_pct_solved']:.5f}",
                    f"{row['mean_pct_optimal']:.5f}",
                    f"{row['mean_avg_diff']:.5f}",
                    f"{baseline_mean / row['mean_total_time_secs']:.5f}",
                ]
            )

    draw_plot(results, plot_png)

    lines = []
    lines.append(f"Baseline commit: {results[0]['short_sha']} {results[0]['subject']}")
    lines.append(f"Measured commits: {len(results)}")
    lines.append(f"Warm-up runs per commit: {args.warmup_runs}")
    lines.append(f"Measured runs per commit: {args.repeats}")
    lines.append("")
    lines.append("Per-commit mean search time:")
    for row in results:
        lines.append(
            f"{row['short_sha']}  {row['mean_total_time_secs']:.5f}s ± {row['std_total_time_secs']:.5f}s  "
            f"optimal={row['mean_pct_optimal']:.2f}%  solved={row['mean_pct_solved']:.2f}%  "
            f"{row['subject']}"
        )
    report_txt.write_text("\n".join(lines) + "\n")

    print("")
    print(report_txt.read_text().rstrip())
    print("")
    print(f"Wrote {runs_csv}")
    print(f"Wrote {summary_csv}")
    print(f"Wrote {plot_png}")
    print(f"Wrote {report_txt}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
