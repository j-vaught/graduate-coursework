import numpy as np
from PIL import Image
from scipy.ndimage import uniform_filter

# Create a 256x256 resolution test chart (simplified)
SIZE = 256
img = np.ones((SIZE, SIZE), dtype=np.float64) * 255  # white background

# === TOP: 3 groups of vertical bars (decreasing width) ===
y_top, y_bot = 15, 70
# Group 1: width=10, gap=10
for i in range(3):
    x0 = 15 + i * 20
    img[y_top:y_bot, x0:x0+10] = 0

# Group 2: width=5, gap=5
for i in range(5):
    x0 = 95 + i * 10
    img[y_top:y_bot, x0:x0+5] = 0

# Group 3: width=3, gap=3
for i in range(8):
    x0 = 170 + i * 6
    img[y_top:y_bot, x0:x0+3] = 0

# === MIDDLE: horizontal bars (same 3 groups) ===
y_mid = 80
# Group 1: height=10, gap=10
for i in range(3):
    y0 = y_mid + i * 20
    img[y0:y0+10, 15:70] = 0

# Group 2: height=5, gap=5
for i in range(5):
    y0 = y_mid + i * 10
    img[y0:y0+5, 95:150] = 0

# Group 3: height=3, gap=3
for i in range(8):
    y0 = y_mid + i * 6
    img[y0:y0+3, 170:225] = 0

# === BOTTOM: the key vertical bars (5px wide, 20px separation, 100px tall) ===
bar_y_top = 145
bar_y_bot = 245
for i in range(4):
    x0 = 15 + i * 25  # 5px bar + 20px gap = 25px period
    img[bar_y_top:bar_y_bot, x0:x0+5] = 0

# Gray patches (bottom right)
img[170:235, 140:190] = 170
img[170:235, 200:245] = 85

# Save original
original = img.copy()
Image.fromarray(original.astype(np.uint8), mode='L').save('figures/fig2_original.png')

# === Apply averaging filters ===
for n, label in [(23, 'a'), (25, 'b'), (45, 'c')]:
    filtered = uniform_filter(original, size=n, mode='reflect')
    filtered = np.clip(filtered, 0, 255)
    Image.fromarray(filtered.astype(np.uint8), mode='L').save(f'figures/fig3_{label}_n{n}.png')

print("Done! Generated:")
print("  figures/fig2_original.png")
print("  figures/fig3_a_n23.png")
print("  figures/fig3_b_n25.png")
print("  figures/fig3_c_n45.png")
