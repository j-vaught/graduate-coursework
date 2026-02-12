#!/usr/bin/env python3
import pathlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

ROOT = pathlib.Path(__file__).resolve().parents[1]
FIG_DIR = ROOT / "drafts" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

# USC brand palette
GARNET = "#73000A"
BLACK = "#000000"
WHITE = "#FFFFFF"
ATLANTIC = "#466A9F"
CONGAREE = "#1F414D"
HORSESHOE = "#65780B"
HONEYCOMB = "#A49137"

def create_pipeline_diagram():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    # Boxes
    # 1. Simulator
    sim_box = patches.FancyBboxPatch((0.5, 3.5), 2, 1.5, boxstyle="square,pad=0.1", fc=WHITE, ec=GARNET, lw=2)
    ax.add_patch(sim_box)
    ax.text(1.5, 4.25, "Radar Simulator\n$\\mathcal{S}(\\theta, e)$", ha='center', va='center', fontweight='bold', color=GARNET)

    # 2. Synthetic Data
    syn_box = patches.FancyBboxPatch((3.5, 3.5), 2, 1.5, boxstyle="square,pad=0.1", fc=WHITE, ec=ATLANTIC, lw=2)
    ax.add_patch(syn_box)
    ax.text(4.5, 4.25, "Synthetic Radar\n$D_{syn}$", ha='center', va='center', fontweight='bold', color=ATLANTIC)

    # 3. Model (Inner Loop)
    model_box = patches.FancyBboxPatch((6.5, 3.5), 2, 1.5, boxstyle="square,pad=0.1", fc=WHITE, ec=CONGAREE, lw=2)
    ax.add_patch(model_box)
    ax.text(7.5, 4.25, "Downstream Model\n$\\mathcal{M}^*(\\theta)$\n(MRISNet)", ha='center', va='center', fontweight='bold', color=CONGAREE)

    # 4. Real Data
    real_box = patches.FancyBboxPatch((6.5, 1.0), 2, 1.0, boxstyle="square,pad=0.1", fc=WHITE, ec=HORSESHOE, lw=2)
    ax.add_patch(real_box)
    ax.text(7.5, 1.5, "Real Radar Data\n$D_{real}$ (MOANA)", ha='center', va='center', fontweight='bold', color=HORSESHOE)

    # 5. RL Policy (Outer Loop)
    rl_box = patches.FancyBboxPatch((2.5, 1.0), 3, 1.0, boxstyle="square,pad=0.1", fc=WHITE, ec=HONEYCOMB, lw=2)
    ax.add_patch(rl_box)
    ax.text(4.0, 1.5, "RL Outer-Loop Policy\n(Soft Actor-Critic)", ha='center', va='center', fontweight='bold', color=HONEYCOMB)

    # Arrows
    # theta to Sim
    ax.annotate("", xy=(1.5, 3.5), xytext=(3.0, 2.0), arrowprops=dict(arrowstyle="->", lw=1.5, color=HONEYCOMB, connectionstyle="arc3,rad=0.2"))
    ax.text(2.3, 2.7, "Update $\\theta$", color=HONEYCOMB, fontweight='bold', rotation=45)

    # Sim to Syn
    ax.annotate("", xy=(3.5, 4.25), xytext=(2.5, 4.25), arrowprops=dict(arrowstyle="<-", lw=1.5, color=BLACK))

    # Syn to Model
    ax.annotate("", xy=(6.5, 4.25), xytext=(5.5, 4.25), arrowprops=dict(arrowstyle="<-", lw=1.5, color=BLACK))

    # Model to RL (Rewards)
    ax.annotate("", xy=(5.5, 1.5), xytext=(6.5, 1.5), arrowprops=dict(arrowstyle="<-", lw=1.5, color=HORSESHOE))
    ax.text(6.0, 1.7, "Eval $R$", color=HORSESHOE, ha='center', fontweight='bold')

    # Environment label to Sim
    ax.annotate("", xy=(0.5, 4.25), xytext=(-0.5, 4.25), arrowprops=dict(arrowstyle="->", lw=1.5, color=BLACK))
    ax.text(-0.7, 4.4, "Env Type $e$", fontweight='bold')

    # Title
    plt.title("Bi-Level Optimization Pipeline for Environment-Conditioned Radar Sim-to-Real", fontsize=14, fontweight='bold', pad=20, color=CONGAREE)

    pdf_path = FIG_DIR / "fig_method_pipeline.pdf"
    plt.savefig(pdf_path, bbox_inches='tight')
    print(f"Wrote {pdf_path}")

if __name__ == "__main__":
    create_pipeline_diagram()
