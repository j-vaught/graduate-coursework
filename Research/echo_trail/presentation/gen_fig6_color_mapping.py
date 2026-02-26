"""Generate E4 color mapping bar chart from real A4 experiment data.

Two panels side by side:
  (a) No-Clutter: mAP50 by class for Mono / Two-tone / Gradient / Intensity
  (b) Clutter: same breakdown
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
HORSESHOE = '#65780B'
HONEYCOMB = '#A49137'
BLACK50 = '#A2A2A2'
BLACK70 = '#5C5C5C'
BLACK90 = '#363636'

DATA_DIR = '/Volumes/MacShare/graduate-coursework/Research/echo_trail/paper/data'
OUT_DIR = '/Volumes/MacShare/graduate-coursework/Research/echo_trail/presentation'

with open(f'{DATA_DIR}/A4/a4_full_results.json') as f:
    a4 = json.load(f)

schemes = ['mono', 'twotone', 'gradient', 'intensity']
scheme_labels = ['Mono', 'Two-tone', 'Gradient', 'Intensity']
scheme_colors = [BLACK50, ATLANTIC, GARNET, HONEYCOMB]
categories = ['Stationary', 'Moving', 'Overall']

def extract(condition):
    d = a4[condition]
    return [d['per_class']['stationary']['mAP50'],
            d['per_class']['moving']['mAP50'],
            d['overall_mAP50']]

# ── Figure ──
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), sharey=True)

x = np.arange(len(categories))
width = 0.18
offsets = [-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width]

for ax, env, title in [(ax1, 'noclutter', '(a) No-Clutter Condition'),
                        (ax2, 'clutter',   '(b) Clutter Condition')]:
    for i, (scheme, label, color) in enumerate(zip(schemes, scheme_labels, scheme_colors)):
        vals = extract(f'{env}_{scheme}')
        bars = ax.bar(x + offsets[i], vals, width, label=label,
                      color=color, edgecolor='white', linewidth=0.5)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.006,
                    f'{h:.3f}', ha='center', va='bottom',
                    fontsize=6.5, color=BLACK70, rotation=0)

    ax.set_title(title, fontsize=13, fontweight='bold', color=BLACK90, pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='y', labelsize=9)
    ax.grid(axis='y', alpha=0.3, linewidth=0.5)

ax1.set_ylabel('mAP$_{50}$', fontsize=12)
ax1.set_ylim(0.45, 0.95)
ax1.yaxis.set_major_locator(MultipleLocator(0.05))
ax1.legend(fontsize=9, loc='upper left', framealpha=0.9)

fig.tight_layout(pad=2.0)

out_png = f'{OUT_DIR}/fig6_color_mapping.png'
out_pdf = f'{OUT_DIR}/fig6_color_mapping.pdf'
fig.savefig(out_png, dpi=200, bbox_inches='tight')
fig.savefig(out_pdf, bbox_inches='tight')
plt.close(fig)
print(f'Saved: {out_png}')
print(f'Saved: {out_pdf}')

# Print values
for env in ['noclutter', 'clutter']:
    print(f'\n── {env.title()} ──')
    for scheme, label in zip(schemes, scheme_labels):
        vals = extract(f'{env}_{scheme}')
        print(f'  {label:10s}  Stat: {vals[0]:.4f}  Mov: {vals[1]:.4f}  Overall: {vals[2]:.4f}')
