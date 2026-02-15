"""
Monte Carlo evaluation of the blackjack stick-on-20-or-21 policy.
Generates Figure 5.1 from Sutton & Barto (2020) for Exercise 5.1.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

# ── Blackjack environment ──────────────────────────────────────────
def draw_card():
    """Draw a card (1-10) from an infinite deck. Face cards = 10."""
    card = min(np.random.randint(1, 14), 10)
    return card

def draw_hand():
    """Return (sum, usable_ace, num_cards) for an initial two-card hand."""
    cards = [draw_card(), draw_card()]
    s = sum(cards)
    usable = (1 in cards)
    if usable and s + 10 <= 21:
        s += 10
    return s, usable

def hit(player_sum, usable_ace):
    """Player takes a card. Returns (new_sum, usable_ace, bust)."""
    card = draw_card()
    if card == 1 and player_sum + 11 <= 21:
        player_sum += 11
        usable_ace = True
    else:
        player_sum += card
    # if bust and holding a usable ace, convert it
    if player_sum > 21 and usable_ace:
        player_sum -= 10
        usable_ace = False
    bust = player_sum > 21
    return player_sum, usable_ace, bust


def play_episode():
    """
    Simulate one blackjack game under the policy:
        stick if player_sum >= 20, else hit.
    Returns list of (state, reward) where state = (player_sum, dealer_showing, usable_ace).
    """
    # ── Deal ──
    player_sum, player_usable = draw_hand()
    dealer_showing = draw_card()
    dealer_hidden = draw_card()

    # Handle naturals (sum == 21 from two cards, with one ace)
    # The textbook says natural = ace + 10-card = 21 immediately
    # For simplicity, if player gets 21 on deal, they stick immediately.

    # Record states visited
    states = []

    # ── Player's turn ──
    while player_sum < 20:
        # Record state before action
        state = (player_sum, dealer_showing, player_usable)
        states.append(state)
        player_sum, player_usable, bust = hit(player_sum, player_usable)
        if bust:
            # All visited states get reward -1
            return [(s, -1) for s in states]

    # Record the final stick state
    state = (player_sum, dealer_showing, player_usable)
    states.append(state)

    # ── Dealer's turn ──
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

    # ── Outcome ──
    if dealer_sum > 21:
        reward = 1
    elif dealer_sum > player_sum:
        reward = -1
    elif dealer_sum < player_sum:
        reward = 1
    else:
        reward = 0

    return [(s, reward) for s in states]


def mc_prediction(num_episodes):
    """First-visit MC prediction. Returns V[usable_ace][player_sum][dealer_showing]."""
    # V indexed as V[usable_ace (0/1)][player_sum 12..21][dealer_showing 1..10]
    value_sum = np.zeros((2, 10, 10))
    value_count = np.zeros((2, 10, 10))

    for _ in range(num_episodes):
        episode = play_episode()
        visited = set()
        for state, reward in episode:
            psum, dshow, usable = state
            if psum < 12 or psum > 21:
                continue  # player always hits below 12, skip
            idx = (int(usable), psum - 12, dshow - 1)
            if idx not in visited:
                visited.add(idx)
                value_sum[idx] += reward
                value_count[idx] += 1

    with np.errstate(divide='ignore', invalid='ignore'):
        V = np.where(value_count > 0, value_sum / value_count, 0)
    return V


def plot_value_function(V, title, ax):
    """Plot a 3D surface of the value function."""
    player_range = np.arange(12, 22)  # 12..21
    dealer_range = np.arange(1, 11)   # 1..10 (1=ace)
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

# Brand colors
garnet = '#73000A'
black90 = '#363636'
plt.rcParams.update({
    'font.family': 'serif',
    'text.color': black90,
    'axes.labelcolor': black90,
    'xtick.color': black90,
    'ytick.color': black90,
})

print("Running 10,000 episodes...")
V_10k = mc_prediction(10_000)
print("Running 500,000 episodes...")
V_500k = mc_prediction(500_000)

fig = plt.figure(figsize=(12, 10))
fig.suptitle('Exercise 5.1: Blackjack Value Function (stick on 20/21)',
             fontsize=14, fontweight='bold', color=garnet, y=0.98)

# Usable ace, 10k
ax1 = fig.add_subplot(2, 2, 1, projection='3d')
plot_value_function(V_10k[1], 'Usable ace — 10k episodes', ax1)

# Usable ace, 500k
ax2 = fig.add_subplot(2, 2, 2, projection='3d')
plot_value_function(V_500k[1], 'Usable ace — 500k episodes', ax2)

# No usable ace, 10k
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
plot_value_function(V_10k[0], 'No usable ace — 10k episodes', ax3)

# No usable ace, 500k
ax4 = fig.add_subplot(2, 2, 4, projection='3d')
plot_value_function(V_500k[0], 'No usable ace — 500k episodes', ax4)

plt.tight_layout(rect=[0, 0, 1, 0.95])
out_path = '/Volumes/MacShare/graduate-coursework/Sp26/CSCE775/course_notes/ch5_exercises/blackjack_value_function.png'
plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor='white')
plt.close()
print(f"Saved figure to {out_path}")

# ── Print some diagnostic values for the solution ──────────────────
print("\n=== 500k episode value function (No usable ace) ===")
print("Player sum | Dealer Ace (col 0) | Dealer 10 (col 9)")
for psum in range(12, 22):
    row = psum - 12
    print(f"  {psum:>3}      |    {V_500k[0, row, 0]:+.3f}           |    {V_500k[0, row, 9]:+.3f}")

print("\n=== 500k episode value function (Usable ace) ===")
print("Player sum | Dealer Ace (col 0) | Dealer 10 (col 9)")
for psum in range(12, 22):
    row = psum - 12
    print(f"  {psum:>3}      |    {V_500k[1, row, 0]:+.3f}           |    {V_500k[1, row, 9]:+.3f}")
