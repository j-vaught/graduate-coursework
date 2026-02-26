"""Regenerate fig5_binary_proportional from real A3 experiment data.

Panel (a): Grouped bar chart - Stationary / Moving / Overall mAP50
           comparing No Trail (A1 N=0), Binary, Proportional
           Top row: no clutter, bottom row: clutter
Panel (b): Intensity encoding concept - how binary vs proportional
           encode trail pixel intensity over scan age
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator

# Brand colors
GARNET = '#73000A'
ATLANTIC = '#466A9F'
BLACK50 = '#A2A2A2'
BLACK70 = '#5C5C5C'
BLACK90 = '#363636'

DATA_DIR = '/Volumes/MacShare/graduate-coursework/Research/echo_trail/paper/data'
OUT_DIR = '/Volumes/MacShare/graduate-coursework/Research/echo_trail/presentation'

# Load data
with open(f'{DATA_DIR}/A3/a3_full_results.json') as f:
    a3 = json.load(f)
with open(f'{DATA_DIR}/A1/a1_perclass_results.json') as f:
    a1 = json.load(f)

# Extract values for panel (a)
# No Trail baseline = A1 N=0
baseline_nc = a1['noclutter']['0']
baseline_cl = a1['clutter']['0']

categories = ['Stationary', 'Moving', 'Overall']

# No-clutter condition
no_trail_nc = [baseline_nc['stationary']['mAP50'],
               baseline_nc['moving']['mAP50'],
               baseline_nc['all']['mAP50']]
binary_nc   = [a3['noclutter_binary']['per_class']['stationary']['mAP50'],
               a3['noclutter_binary']['per_class']['moving']['mAP50'],
               a3['noclutter_binary']['overall_mAP50']]
prop_nc     = [a3['noclutter_proportional']['per_class']['stationary']['mAP50'],
               a3['noclutter_proportional']['per_class']['moving']['mAP50'],
               a3['noclutter_proportional']['overall_mAP50']]

# Clutter condition
no_trail_cl = [baseline_cl['stationary']['mAP50'],
               baseline_cl['moving']['mAP50'],
               baseline_cl['all']['mAP50']]
binary_cl   = [a3['clutter_binary']['per_class']['stationary']['mAP50'],
               a3['clutter_binary']['per_class']['moving']['mAP50'],
               a3['clutter_binary']['overall_mAP50']]
prop_cl     = [a3['clutter_proportional']['per_class']['stationary']['mAP50'],
               a3['clutter_proportional']['per_class']['moving']['mAP50'],
               a3['clutter_proportional']['overall_mAP50']]

# ── Figure ──
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5),
                                gridspec_kw={'width_ratios': [1.3, 1]})

# ────────────────────────────────────────────
# Panel (a): Grouped bar chart
# ────────────────────────────────────────────
x = np.arange(len(categories))
width = 0.22

bars_nt = ax1.bar(x - width, no_trail_nc, width, label='No Trail',
                  color=BLACK50, edgecolor='white', linewidth=0.5)
bars_bi = ax1.bar(x,         binary_nc,   width, label='Binary',
                  color=GARNET, edgecolor='white', linewidth=0.5)
bars_pr = ax1.bar(x + width, prop_nc,     width, label='Proportional',
                  color=ATLANTIC, edgecolor='white', linewidth=0.5)

# Value labels on bars
for bars in [bars_nt, bars_bi, bars_pr]:
    for bar in bars:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2, h + 0.008,
                 f'{h:.3f}', ha='center', va='bottom',
                 fontsize=7, color=BLACK70)

ax1.set_ylabel('mAP$_{50}$', fontsize=12)
ax1.set_title('(a) No-Clutter Condition', fontsize=13, fontweight='bold',
              color=BLACK90, pad=10)
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=11)
ax1.set_ylim(0.55, 0.95)
ax1.yaxis.set_major_locator(MultipleLocator(0.05))
ax1.legend(fontsize=9, loc='upper left', framealpha=0.9)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.tick_params(axis='y', labelsize=9)
ax1.grid(axis='y', alpha=0.3, linewidth=0.5)

# ────────────────────────────────────────────
# Panel (b): Intensity encoding concept
# ────────────────────────────────────────────
k = np.linspace(0, 12.5, 100)  # trail pixel age in scans
tau = 3.0  # exponential decay constant (N/3 for N=10 trail)
decay = np.exp(-k / tau)

# Strong target: original intensity ~1.0
prop_strong = 1.0 * decay
# Weak target: original intensity ~0.3
prop_weak = 0.3 * decay
# Binary: always 1.0 until trail end (step at N)
binary_line = np.ones_like(k)
binary_line[k > 11.5] = 0  # sharp cutoff at trail boundary

ax2.plot(k, prop_strong, '-o', color=GARNET, markersize=4, markevery=8,
         linewidth=2, label='Proportional (high intensity)')
ax2.plot(k, prop_weak, '-s', color=ATLANTIC, markersize=4, markevery=8,
         linewidth=2, label='Proportional (low intensity)')
ax2.plot(k, binary_line, '--^', color=BLACK50, markersize=4, markevery=8,
         linewidth=2, label='Binary (any intensity)', alpha=0.8)

ax2.set_xlabel('Trail pixel age (scans)', fontsize=11)
ax2.set_ylabel('Displayed intensity', fontsize=11)
ax2.set_title('(b) Intensity Encoding', fontsize=13, fontweight='bold',
              color=BLACK90, pad=10)
ax2.set_xlim(0, 12.5)
ax2.set_ylim(-0.02, 1.08)
ax2.legend(fontsize=9, loc='center right', framealpha=0.9)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.tick_params(labelsize=9)
ax2.grid(alpha=0.3, linewidth=0.5)

fig.tight_layout(pad=2.0)

# Save both PNG and PDF
out_png = f'{OUT_DIR}/fig5_binary_proportional.png'
out_pdf = f'{OUT_DIR}/fig5_binary_proportional.pdf'
fig.savefig(out_png, dpi=200, bbox_inches='tight')
fig.savefig(out_pdf, bbox_inches='tight')
plt.close(fig)
print(f'Saved: {out_png}')
print(f'Saved: {out_pdf}')

# Print the values for reference
print('\n── No-Clutter Values ──')
for i, cat in enumerate(categories):
    print(f'  {cat:12s}  No Trail: {no_trail_nc[i]:.4f}  '
          f'Binary: {binary_nc[i]:.4f}  Proportional: {prop_nc[i]:.4f}')

print('\n── Clutter Values ──')
for i, cat in enumerate(categories):
    print(f'  {cat:12s}  No Trail: {no_trail_cl[i]:.4f}  '
          f'Binary: {binary_cl[i]:.4f}  Proportional: {prop_cl[i]:.4f}')
