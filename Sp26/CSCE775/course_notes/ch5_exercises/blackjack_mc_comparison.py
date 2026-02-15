"""
Exercise 5.2: Compare first-visit MC vs every-visit MC on blackjack.
Generates a side-by-side comparison figure and computes max absolute difference.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# ── Blackjack environment (same as exercise 5.1) ──────────────────
def draw_card():
    card = min(np.random.randint(1, 14), 10)
    return card

def draw_hand():
    cards = [draw_card(), draw_card()]
    s = sum(cards)
    usable = (1 in cards)
    if usable and s + 10 <= 21:
        s += 10
    return s, usable

def hit(player_sum, usable_ace):
    card = draw_card()
    if card == 1 and player_sum + 11 <= 21:
        player_sum += 11
        usable_ace = True
    else:
        player_sum += card
    if player_sum > 21 and usable_ace:
        player_sum -= 10
        usable_ace = False
    bust = player_sum > 21
    return player_sum, usable_ace, bust

def play_episode():
    player_sum, player_usable = draw_hand()
    dealer_showing = draw_card()
    dealer_hidden = draw_card()
    states = []

    while player_sum < 20:
        state = (player_sum, dealer_showing, player_usable)
        states.append(state)
        player_sum, player_usable, bust = hit(player_sum, player_usable)
        if bust:
            return [(s, -1) for s in states]

    state = (player_sum, dealer_showing, player_usable)
    states.append(state)

    dealer_sum = sum([dealer_showing, dealer_hidden])
    dealer_usable = (dealer_showing == 1 or dealer_hidden == 1)
    if dealer_usable and dealer_sum + 10 <= 21:
        dealer_sum += 10

    while dealer_sum < 17:
        card = draw_card()
        if card == 1 and dealer_sum + 11 <= 21:
            dealer_sum += 11
            dealer_usable = True
        else:
            dealer_sum += card
        if dealer_sum > 21 and dealer_usable:
            dealer_sum -= 10
            dealer_usable = False

    if dealer_sum > 21:
        reward = 1
    elif dealer_sum > player_sum:
        reward = -1
    elif dealer_sum < player_sum:
        reward = 1
    else:
        reward = 0

    return [(s, reward) for s in states]


# ── MC prediction (both variants) ─────────────────────────────────
def mc_prediction_both(num_episodes):
    """Run first-visit and every-visit MC in a single pass over the same episodes."""
    fv_sum = np.zeros((2, 10, 10))
    fv_count = np.zeros((2, 10, 10))
    ev_sum = np.zeros((2, 10, 10))
    ev_count = np.zeros((2, 10, 10))

    # Also track how often states are revisited within an episode
    revisit_total = 0
    revisit_episodes = 0

    for _ in range(num_episodes):
        episode = play_episode()
        visited = set()
        episode_states = set()
        had_revisit = False

        for state, reward in episode:
            psum, dshow, usable = state
            if psum < 12 or psum > 21:
                continue
            idx = (int(usable), psum - 12, dshow - 1)

            # Every-visit: always count
            ev_sum[idx] += reward
            ev_count[idx] += 1

            # First-visit: only count first occurrence
            if idx not in visited:
                visited.add(idx)
                fv_sum[idx] += reward
                fv_count[idx] += 1

            if idx in episode_states:
                had_revisit = True
            episode_states.add(idx)

        if had_revisit:
            revisit_episodes += 1
        revisit_total += 1

    with np.errstate(divide='ignore', invalid='ignore'):
        V_fv = np.where(fv_count > 0, fv_sum / fv_count, 0)
        V_ev = np.where(ev_count > 0, ev_sum / ev_count, 0)

    revisit_pct = 100.0 * revisit_episodes / revisit_total if revisit_total > 0 else 0
    return V_fv, V_ev, fv_count, ev_count, revisit_pct


def plot_value_function(V, title, ax):
    player_range = np.arange(12, 22)
    dealer_range = np.arange(1, 11)
    X, Y = np.meshgrid(dealer_range, player_range)
    ax.plot_surface(X, Y, V, cmap=cm.coolwarm, linewidth=0.3,
                    edgecolors='#363636', antialiased=True, alpha=0.9)
    ax.set_xlabel('Dealer showing', fontsize=9, labelpad=8)
    ax.set_ylabel('Player sum', fontsize=9, labelpad=8)
    ax.set_zlabel('')
    ax.set_zlim(-1, 1)
    ax.set_xticks([1, 4, 7, 10])
    ax.set_xticklabels(['A', '4', '7', '10'])
    ax.set_yticks([12, 15, 18, 21])
    ax.set_title(title, fontsize=11, fontweight='bold', pad=10)
    ax.view_init(elev=20, azim=-120)
    ax.tick_params(labelsize=7)


# ── Main ───────────────────────────────────────────────────────────
np.random.seed(42)

garnet = '#73000A'
black90 = '#363636'
atlantic = '#466A9F'
plt.rcParams.update({
    'font.family': 'serif',
    'text.color': black90,
    'axes.labelcolor': black90,
    'xtick.color': black90,
    'ytick.color': black90,
})

print("Running 500,000 episodes (both first-visit and every-visit)...")
V_fv, V_ev, fv_count, ev_count, revisit_pct = mc_prediction_both(500_000)

# ── Comparison stats ──────────────────────────────────────────────
diff = np.abs(V_fv - V_ev)
print(f"\n=== Comparison: First-Visit vs Every-Visit (500k episodes) ===")
print(f"Max absolute difference:  {diff.max():.4f}")
print(f"Mean absolute difference: {diff.mean():.4f}")
print(f"Episodes with any state revisited: {revisit_pct:.1f}%")
print(f"\nTotal first-visit counts:  {fv_count.sum():.0f}")
print(f"Total every-visit counts:  {ev_count.sum():.0f}")
print(f"Extra samples from revisits: {ev_count.sum() - fv_count.sum():.0f} "
      f"({100*(ev_count.sum() - fv_count.sum())/fv_count.sum():.1f}% more)")

# Per-state difference table (no usable ace)
print(f"\n=== Per-state difference (No usable ace) ===")
print(f"{'Psum':>5} | {'FV vs Ace':>10} {'EV vs Ace':>10} {'Diff':>8} | "
      f"{'FV vs 10':>10} {'EV vs 10':>10} {'Diff':>8}")
for psum in range(12, 22):
    r = psum - 12
    print(f"  {psum:>3} | {V_fv[0,r,0]:>+10.4f} {V_ev[0,r,0]:>+10.4f} {diff[0,r,0]:>8.4f} | "
          f"{V_fv[0,r,9]:>+10.4f} {V_ev[0,r,9]:>+10.4f} {diff[0,r,9]:>8.4f}")

# ── Figure 1: Side-by-side surfaces ──────────────────────────────
fig = plt.figure(figsize=(12, 10))
fig.suptitle('Exercise 5.2: First-Visit vs Every-Visit MC (500k episodes)',
             fontsize=14, fontweight='bold', color=garnet, y=0.98)

ax1 = fig.add_subplot(2, 2, 1, projection='3d')
plot_value_function(V_fv[1], 'First-Visit — Usable Ace', ax1)
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
plot_value_function(V_ev[1], 'Every-Visit — Usable Ace', ax2)
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
plot_value_function(V_fv[0], 'First-Visit — No Usable Ace', ax3)
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
plot_value_function(V_ev[0], 'Every-Visit — No Usable Ace', ax4)

plt.tight_layout(rect=[0, 0, 1, 0.95])
out1 = '/Volumes/MacShare/graduate-coursework/Sp26/CSCE775/course_notes/ch5_exercises/fv_vs_ev_surfaces.png'
plt.savefig(out1, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f"\nSaved surface comparison to {out1}")

# ── Figure 2: Difference heatmap ─────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
fig.suptitle('Absolute Difference: First-Visit minus Every-Visit MC',
             fontsize=13, fontweight='bold', color=garnet, y=1.02)

for i, (ax, label) in enumerate(zip(axes, ['No Usable Ace', 'Usable Ace'])):
    im = ax.imshow(diff[i], cmap='Reds', aspect='auto', origin='lower',
                   vmin=0, vmax=max(diff.max(), 0.02))
    ax.set_xticks(range(10))
    ax.set_xticklabels(['A'] + [str(x) for x in range(2, 11)])
    ax.set_yticks(range(10))
    ax.set_yticklabels(range(12, 22))
    ax.set_xlabel('Dealer Showing', fontsize=10)
    ax.set_ylabel('Player Sum', fontsize=10)
    ax.set_title(label, fontsize=11, fontweight='bold')
    # Annotate each cell
    for r in range(10):
        for c in range(10):
            val = diff[i, r, c]
            color = 'white' if val > diff.max() * 0.6 else black90
            ax.text(c, r, f'{val:.3f}', ha='center', va='center',
                    fontsize=6, color=color)

cbar = fig.colorbar(im, ax=axes, shrink=0.8, pad=0.02)
cbar.set_label('|V_FV - V_EV|', fontsize=10)

plt.tight_layout()
out2 = '/Volumes/MacShare/graduate-coursework/Sp26/CSCE775/course_notes/ch5_exercises/fv_vs_ev_diff_heatmap.png'
plt.savefig(out2, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved difference heatmap to {out2}")
