#!/usr/bin/env python3
import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "drafts" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# USC / CLAUDE.md Palette
GARNET = "#73000A"
BLACK = "#000000"
WHITE = "#FFFFFF"
NEUTRAL_90 = "#363636"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"
SANDSTORM = "#FFF2E3"

def create_pipeline_diagram():
    # Compact, professional aspect ratio
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # --- LAYOUT CONFIG ---
    y_top = 3.5
    y_bot = 1.0
    
    x_sim = 2.0
    x_syn = 5.0
    x_mod = 8.0
    x_real = 8.0
    x_rl = 3.5

    box_w = 2.0
    box_h = 1.2

    # --- HELPER FUNCTIONS ---
    def draw_node(x, y, color, text, subtext="", bg_color=WHITE, width=box_w):
        rect = patches.Rectangle((x - width/2, y - box_h/2), width, box_h, 
                                 fc=bg_color, ec=color, lw=1.5, zorder=10)
        ax.add_patch(rect)
        
        ax.text(x, y + 0.15 if subtext else y, text, 
                ha='center', va='center', fontsize=10, fontweight='bold', color=color, zorder=11)
        if subtext:
            ax.text(x, y - 0.25, subtext, 
                    ha='center', va='center', fontsize=9, color=BLACK, zorder=11)

    def draw_arrow(x1, y1, x2, y2, label=None, color=BLACK, lw=1.2):
        # Sleek, sharp arrow style
        arrow_props = dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", 
                           lw=lw, color=color, mutation_scale=15)
        
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=arrow_props, zorder=5)

        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            ax.text(mid_x, mid_y + 0.1, label, ha='center', va='bottom', 
                    fontsize=8, fontweight='bold', color=color, zorder=12)

    # --- DRAW NODES ---
    draw_node(x_sim, y_top, GARNET, "Radar Simulator", "$\\mathcal{S}(\\theta, e)$")
    draw_node(x_syn, y_top, ATLANTIC, "Synthetic Buffer", "$D_{syn}$")
    draw_node(x_mod, y_top, CONGAREE, "Downstream\nModel", "$\\mathcal{M}^*(\\theta)$")
    draw_node(x_real, y_bot, HORSESHOE, "Real Validation", "$D_{real}$ (MOANA)")
    draw_node(x_rl, y_bot, HONEYCOMB, "RL Policy", "Soft Actor-Critic", bg_color=SANDSTORM, width=3.5)

    # --- CONNECTIONS ---

    # Env -> Sim
    draw_arrow(x_sim - box_w/2 - 1.2, y_top, x_sim - box_w/2, y_top)
    ax.text(x_sim - box_w/2 - 1.3, y_top, "Env Type\n(Lake, River)", ha='right', va='center', fontsize=9, fontweight='bold')

    # Sim -> Buffer
    draw_arrow(x_sim + box_w/2, y_top, x_syn - box_w/2, y_top, label="Generate")

    # Buffer -> Model
    draw_arrow(x_syn + box_w/2, y_top, x_mod - box_w/2, y_top, label="Train")

    # Model -> Real (Vertical)
    draw_arrow(x_mod, y_top - box_h/2, x_real, y_bot + box_h/2, label="Evaluate", color=HORSESHOE)

    # Real -> RL (Feedback)
    draw_arrow(x_real - box_w/2, y_bot, x_rl + 1.75, y_bot, label="Reward $R$", color=HONEYCOMB)

    # RL -> Sim (Update Action) - Orthogonal Path
    rl_top_y = y_bot + box_h/2
    sim_bot_y = y_top - box_h/2
    mid_y = (rl_top_y + sim_bot_y) / 2
    
    # Path coordinates
    ax.plot([x_rl, x_rl, x_sim, x_sim], [rl_top_y, mid_y, mid_y, sim_bot_y], color=GARNET, lw=1.2, zorder=5)
    # Arrowhead at the very end
    ax.annotate("", xy=(x_sim, sim_bot_y), xytext=(x_sim, mid_y), 
                arrowprops=dict(arrowstyle="-|>,head_width=0.3,head_length=0.5", lw=1.2, color=GARNET, mutation_scale=15),
                zorder=5)
    
    ax.text((x_rl + x_sim)/2, mid_y + 0.1, "Update $\\theta$", ha='center', va='bottom', 
            fontsize=9, fontweight='bold', color=GARNET, zorder=12)

    plt.tight_layout()
    pdf_path = FIG_DIR / "fig_method_pipeline.pdf"
    png_path = FIG_DIR / "fig_method_pipeline.png"
    plt.savefig(pdf_path, bbox_inches='tight')
    plt.savefig(png_path, bbox_inches='tight', dpi=300)
    print(f"Wrote {pdf_path}")
    print(f"Wrote {png_path}")

if __name__ == "__main__":
    create_pipeline_diagram()
