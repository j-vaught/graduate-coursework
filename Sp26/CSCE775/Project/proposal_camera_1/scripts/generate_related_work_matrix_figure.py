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
    columns = ["Method", "Dynamic?", "Joint Reg+Aug?", "Context-Aware?", "Feedback Loop?"]
    rows = [
        ["AutoAugment (2019)", "No (Static)", "No", "No", "No (Offline)"],
        ["RandAugment (2020)", "No (Random)", "No", "No", "No"],
        ["DeepReg (2016)", "No (Fixed)", "No", "No", "Yes (Supervised)"],
        ["Deep Homography (2020)", "Yes (Network)", "No", "Implicit", "No"],
        ["Ours (Proposal 2)", "Yes (Per-Frame)", "Yes", "Yes (Env Tag)", "Yes (Reward)"]
    ]

    colors = [["#FFFFFF"] * len(columns) for _ in range(len(rows))]
    # Highlight ours
    colors[-1] = ["#E6F4EA"] * len(columns)

    table = ax.table(cellText=rows, colLabels=columns, cellLoc='center', loc='center', cellColours=colors)
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)

    plt.title("Comparison with Related Augmentation & Registration Methods", fontweight='bold', y=1.05)
    plt.savefig(FIG_DIR / "fig_related_work_matrix.pdf", bbox_inches='tight')
    print(f"Wrote {FIG_DIR / 'fig_related_work_matrix.pdf'}")

if __name__ == "__main__":
    create_rw_matrix()
