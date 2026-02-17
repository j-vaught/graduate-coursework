import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import uniform_filter

# Create a 256x256 resolution test chart
SIZE = 256
img = np.ones((SIZE, SIZE), dtype=np.float64) * 255  # white background

# === TOP SECTION: 4 groups of vertical bars + horizontal bars ===
# Group 1 (largest): 3 vertical bars, width=12, gap=8
y_top, y_bot = 10, 50
for i in range(3):
    x0 = 10 + i * 20
    img[y_top:y_bot, x0:x0+12] = 0

# Horizontal bars for group 1
for i in range(3):
    y0 = 55 + i * 14
    img[y0:y0+8, 10:45] = 0

# Group 2: 4 vertical bars, width=8, gap=6
for i in range(4):
    x0 = 80 + i * 14
    img[y_top:y_bot, x0:x0+8] = 0

# Horizontal bars for group 2
for i in range(4):
    y0 = 55 + i * 11
    img[y0:y0+5, 80:115] = 0

# Group 3: 5 vertical bars, width=5, gap=5
for i in range(5):
    x0 = 145 + i * 10
    img[y_top:y_bot, x0:x0+5] = 0

# Horizontal bars for group 3
for i in range(5):
    y0 = 55 + i * 8
    img[y0:y0+3, 145:178] = 0

# Group 4 (smallest): 6 vertical bars, width=3, gap=4
for i in range(6):
    x0 = 205 + i * 7
    img[y_top:y_bot, x0:x0+3] = 0

# Horizontal bars for group 4
for i in range(6):
    y0 = 55 + i * 6
    img[y0:y0+2, 205:235] = 0

# === MIDDLE SECTION ===
# Three dots
for i in range(3):
    cx, cy = 20 + i * 15, 115
    rr, cc = np.ogrid[-cy:SIZE-cy, -cx:SIZE-cx]
    mask = rr*rr + cc*cc <= 5*5
    img[mask] = 0

# Large "a" character
try:
    font = ImageFont.truetype("/System/Library/Fonts/Times.ttc", 60)
except:
    font = ImageFont.load_default()

pil_img = Image.fromarray(img.astype(np.uint8), mode='L')
draw = ImageDraw.Draw(pil_img)
draw.text((110, 95), "a", fill=0, font=font)
img = np.array(pil_img, dtype=np.float64)

# Horizontal ruled lines (left side, below dots)
for i in range(8):
    y0 = 135 + i * 7
    img[y0:y0+3, 10:85] = 0

# === BOTTOM SECTION ===
# Vertical bars: 5 pixels wide, 20 pixels separation (period = 25), 100 pixels high
# 4 bars
bar_y_top = 145
bar_y_bot = 245
for i in range(4):
    x0 = 10 + i * 25  # 5px bar + 20px gap = 25px period
    img[bar_y_top:bar_y_bot, x0:x0+5] = 0

# Gray patches (lower right)
img[185:240, 130:180] = 180  # light gray
img[185:240, 190:240] = 100  # darker gray

# Bottom row: small squares
for i in range(10):
    x0 = 10 + i * 24
    img[246:254, x0:x0+10] = 0

# Save original
original = img.copy()
Image.fromarray(original.astype(np.uint8), mode='L').save('figures/fig2_original.png')

# === Apply averaging filters ===
for n, label in [(23, 'a'), (25, 'b'), (45, 'c')]:
    # Use reflect padding to avoid dark edges
    filtered = uniform_filter(original, size=n, mode='reflect')
    filtered = np.clip(filtered, 0, 255)
    Image.fromarray(filtered.astype(np.uint8), mode='L').save(f'figures/fig3_{label}_n{n}.png')

print("Done! Generated:")
print("  figures/fig2_original.png")
print("  figures/fig3_a_n23.png")
print("  figures/fig3_b_n25.png")
print("  figures/fig3_c_n45.png")
