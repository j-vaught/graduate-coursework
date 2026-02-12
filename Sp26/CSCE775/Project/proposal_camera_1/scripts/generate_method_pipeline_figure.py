#!/usr/bin/env python3
import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "drafts" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# Colors
GARNET = "#73000A"
BLACK = "#000000"
WHITE = "#FFFFFF"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
SANDSTORM = "#FFF2E3"
NEUTRAL_90 = "#363636"

def create_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Layout
    y_main = 2.5
    
    x_input = 1.0
    x_rl = 3.5
    x_aug = 6.0
    x_task = 8.5
    
    box_w = 1.8
    box_h = 1.2

    def draw_node(x, y, color, text, subtext="", bg_color=WHITE, width=box_w):
        rect = patches.Rectangle((x - width/2, y - box_h/2), width, box_h, 
                                 fc=bg_color, ec=color, lw=1.5, zorder=10)
        ax.add_patch(rect)
        ax.text(x, y + 0.15 if subtext else y, text, 
                ha='center', va='center', fontsize=9, fontweight='bold', color=color, zorder=11)
        if subtext:
            ax.text(x, y - 0.25, subtext, 
                    ha='center', va='center', fontsize=8, color=BLACK, zorder=11)

    def draw_arrow(x1, y1, x2, y2, label=None, color=BLACK, lw=1.2, connectionstyle="arc3"):
        arrow_props = dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", 
                           lw=lw, color=color, connectionstyle=connectionstyle)
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props, zorder=5)
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            # Simple offset for straight lines, complex logic needed for arcs usually, 
            # but we keep it simple for now
            ax.text(mid_x, mid_y + 0.2, label, ha='center', va='bottom', 
                    fontsize=8, fontweight='bold', color=color, zorder=12)

    # Nodes
    draw_node(x_input, y_main, GARNET, "Input Frames", "IR + RGB\\n(Misaligned)")
    draw_node(x_rl, y_main, HONEYCOMB, "RL Policy", "State: Quality\\nAction: Reg+Aug", bg_color=SANDSTORM)
    draw_node(x_aug, y_main, ATLANTIC, "Preprocessor", "Apply Action\\n$T(I_{ir}, I_{rgb})$")
    draw_node(x_task, y_main, CONGAREE, "Downstream\\nDetector", "YOLO/FasterRCNN")

    # Edges - Forward
    draw_arrow(x_input + box_w/2, y_main, x_rl - box_w/2, y_main, label="State $s_t$")
    draw_arrow(x_rl + box_w/2, y_main, x_aug - box_w/2, y_main, label="Action $a_t$")
    draw_arrow(x_aug + box_w/2, y_main, x_task - box_w/2, y_main, label="Processed")

    # Feedback Loop (Task -> RL)
    # Draw curved arrow from Task bottom to RL bottom
    ax.annotate("", xy=(x_rl, y_main - box_h/2), xytext=(x_task, y_main - box_h/2),
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", 
                                lw=1.2, color=HORSESHOE, connectionstyle="arc3,rad=-0.4"),
                zorder=5)
    
    ax.text((x_rl + x_task)/2, 1.0, "Reward: $\\Delta$mAP + Consistency", 
            ha='center', va='center', fontsize=9, fontweight='bold', color=HORSESHOE)

    # Context Input
    ax.text(x_rl, y_main + box_h/2 + 0.5, "Environment Context\\n(Day/Night, Fog)", 
            ha='center', va='center', fontsize=8, color=NEUTRAL_90)
    draw_arrow(x_rl, y_main + box_h/2 + 0.3, x_rl, y_main + box_h/2, color=NEUTRAL_90)

    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig_method_pipeline.pdf", bbox_inches='tight')
    print(f"Wrote {FIG_DIR / 'fig_method_pipeline.pdf'}")

if __name__ == "__main__":
    create_pipeline_diagram()
