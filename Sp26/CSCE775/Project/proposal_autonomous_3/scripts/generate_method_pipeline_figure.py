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
    y_top = 3.5
    y_bot = 1.0
    
    x_asv = 2.0
    x_obs = 5.0
    x_rl = 8.0
    
    box_w = 2.2
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
            ax.text(mid_x, mid_y + 0.2, label, ha='center', va='bottom', 
                    fontsize=8, fontweight='bold', color=color, zorder=12)

    # Nodes
    draw_node(x_asv, y_top, GARNET, "Marine Env\\n(Simulator)", "Currents, Waves\\nObstacles")
    draw_node(x_obs, y_top, ATLANTIC, "State Estimator", "Inputs: Sensors + Battery\\nOutput: $s_t$")
    draw_node(x_rl, y_top, HONEYCOMB, "RL Policy", "Input: $s_t$, EnvType\\nOutput: Action $a_t$", bg_color=SANDSTORM)
    
    # Bottom nodes for feedback components
    draw_node(x_rl, y_bot, CONGAREE, "Reward Calc", "$r_t = \Delta$Info - EnergyCost")
    
    # Edges
    # Env -> State
    draw_arrow(x_asv + box_w/2, y_top, x_obs - box_w/2, y_top, label="Sensor Data")
    
    # State -> RL
    draw_arrow(x_obs + box_w/2, y_top, x_rl - box_w/2, y_top, label="State $s_t$")
    
    # RL -> Action (to Env) - LONG LOOP BACK
    # Draw curved arrow from RL top to Env top
    ax.annotate("", xy=(x_asv, y_top + box_h/2), xytext=(x_rl, y_top + box_h/2),
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", 
                                lw=1.2, color=HORSESHOE, connectionstyle="arc3,rad=0.4"),
                zorder=5)
    ax.text((x_asv + x_rl)/2, y_top + box_h/2 + 0.8, "Action $a_t$: Velocity + Duty Cycle", 
            ha='center', va='center', fontsize=9, fontweight='bold', color=HORSESHOE)

    # RL -> Reward
    draw_arrow(x_rl, y_top - box_h/2, x_rl, y_bot + box_h/2, label="Transition")
    
    # Reward -> RL (Update)
    # Self-loop style or side arrow
    ax.text(x_rl + box_w/2 + 0.2, (y_top + y_bot)/2, "Update $\pi$", 
            ha='left', va='center', fontsize=9, fontweight='bold', color=HONEYCOMB, rotation=90)
    
    # Env Context Input
    ax.text(x_rl, y_top + box_h/2 + 0.2, "Context: Lake/River/Coast", 
            ha='center', va='bottom', fontsize=8, color=NEUTRAL_90)

    plt.tight_layout()
    plt.savefig(FIG_DIR / "fig_method_pipeline.pdf", bbox_inches='tight')
    print(f"Wrote {FIG_DIR / 'fig_method_pipeline.pdf'}")

if __name__ == "__main__":
    create_pipeline_diagram()
