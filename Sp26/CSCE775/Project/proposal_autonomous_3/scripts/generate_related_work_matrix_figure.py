#!/usr/bin/env python3
import pathlib
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "drafts" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def create_rw_matrix():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.axis('off')
    ax.axis('tight')

    # Data from proposal_related_work_matrix.md
    columns = ["Method", "Exploration?", "Energy Aware?", "Env Adaptive?", "Joint Control?"]
    rows = [
        ["Frontier Exp (1997)", "Yes", "No", "No", "No"],
        ["Active SLAM (2014)", "Yes", "Rarely", "No", "No"],
        ["Energy-Aware Plan (2016)", "No (Goal)", "Yes", "No", "No"],
        ["Deep RL Nav (2017)", "No (Goal)", "No", "Implicit", "No"],
        ["Ours (Proposal 3)", "Yes", "Yes (Battery)", "Yes (River/Lake)", "Yes (Motion+Sensor)"]
    ]

    colors = [["#FFFFFF"] * len(columns) for _ in range(len(rows))]
    # Highlight ours
    colors[-1] = ["#E6F4EA"] * len(columns)

    table = ax.table(cellText=rows, colLabels=columns, cellLoc='center', loc='center', cellColours=colors)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)

    plt.title("Comparison with Related Exploration & Energy Methods", fontweight='bold', y=1.05)
    plt.savefig(FIG_DIR / "fig_related_work_matrix.pdf", bbox_inches='tight')
    print(f"Wrote {FIG_DIR / 'fig_related_work_matrix.pdf'}")

if __name__ == "__main__":
    create_rw_matrix()
