"""Generate charts for async pipeline report."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Computer Modern Roman', 'CMU Serif', 'Times New Roman'],
    'font.size': 10,
    'axes.linewidth': 0.5,
    'axes.edgecolor': '#363636',
    'xtick.color': '#363636',
    'ytick.color': '#363636',
    'text.color': '#363636',
    'figure.dpi': 300,
})

GARNET = '#73000A'
ATLANTIC = '#466A9F'
GRID_COLOR = '#C7C7C7'

baseline_tots = [10.71, 10.43, 10.45, 10.59, 10.66, 10.54, 10.67, 10.94, 10.83, 10.76, 11.62, 11.43, 11.45, 11.45, 11.66, 11.52, 11.61, 11.68, 11.62, 11.71, 11.50, 11.55, 11.43, 11.49, 12.63, 11.47, 11.48, 11.64, 11.59, 11.59, 11.44, 11.49, 11.61, 11.50, 11.72, 11.75, 11.61, 11.47, 11.39, 11.62, 11.70, 11.47, 11.45, 11.57, 11.45, 11.35, 11.76, 11.66, 11.80, 11.48]
async_tots = [10.52, 6.41, 6.33, 6.68, 6.55, 6.49, 6.71, 6.60, 6.66, 6.65, 6.73, 6.69, 6.79, 6.61, 6.76, 6.62, 6.79, 6.62, 6.94, 6.64, 6.92, 6.58, 6.82, 6.88, 6.77, 6.92, 6.84, 6.67, 7.02, 6.65, 6.85, 6.93, 6.76, 6.74, 6.73, 6.81, 7.03, 6.61, 6.71, 6.71, 6.92, 6.70, 6.66, 6.84, 6.77, 7.00, 6.66, 6.75, 6.62, 6.82]

baseline_solved = [8.58, 12.95, 16.16, 21.58, 19.55, 21.36, 24.80, 28.29, 26.77, 29.77, 29.93, 30.10, 32.70, 32.68, 31.06, 33.84, 32.34, 30.86, 33.79, 34.78, 35.15, 33.75, 34.77, 32.96, 34.87, 33.47, 35.20, 35.90, 35.86, 35.09, 33.80, 35.58, 30.75, 32.49, 34.26, 36.10, 32.76, 35.03, 34.16, 36.36, 33.50, 33.32, 36.13, 36.60, 35.30, 36.11, 33.62, 35.68, 36.05, 35.09]
async_solved = [8.05, 7.39, 12.14, 12.45, 16.49, 16.11, 18.93, 19.67, 22.16, 22.01, 23.91, 24.79, 26.45, 27.64, 26.85, 27.57, 29.33, 27.40, 28.11, 30.18, 28.64, 31.91, 29.59, 33.35, 29.25, 33.44, 34.40, 32.96, 34.13, 32.85, 33.24, 32.64, 32.32, 32.85, 32.44, 34.07, 35.15, 35.34, 32.56, 34.18, 35.23, 33.07, 35.31, 35.14, 35.14, 34.15, 35.53, 37.11, 37.77, 34.85]

x = np.arange(1, 51)

# Chart 1: Per-update wall time
fig, ax = plt.subplots(figsize=(6, 2.4))
ax.plot(x, baseline_tots, color=GARNET, linewidth=1.2, label='Baseline')
ax.plot(x, async_tots, color=ATLANTIC, linewidth=1.2, label='Async')
ax.set_xlabel('Update round')
ax.set_ylabel('Time per update (s)')
ax.set_xlim(1, 50)
ax.set_ylim(0, 14)
ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
ax.grid(True, alpha=0.3, color=GRID_COLOR)
ax.legend(framealpha=1, edgecolor=GRID_COLOR)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
fig.savefig('chart_time.png', bbox_inches='tight')
plt.close()

# Chart 2: Solve rate convergence
fig, ax = plt.subplots(figsize=(6, 2.4))
ax.plot(x, baseline_solved, color=GARNET, linewidth=1.2, label='Baseline')
ax.plot(x, async_solved, color=ATLANTIC, linewidth=1.2, label='Async')
ax.set_xlabel('Update round')
ax.set_ylabel('Solve rate (%)')
ax.set_xlim(1, 50)
ax.set_ylim(0, 45)
ax.set_yticks([0, 10, 20, 30, 40])
ax.grid(True, alpha=0.3, color=GRID_COLOR)
ax.legend(framealpha=1, edgecolor=GRID_COLOR)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
fig.tight_layout()
fig.savefig('chart_solve.png', bbox_inches='tight')
plt.close()

print("Charts saved: chart_time.png, chart_solve.png")
