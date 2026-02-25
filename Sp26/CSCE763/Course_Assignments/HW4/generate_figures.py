from pathlib import Path

import numpy as np
from PIL import Image


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def make_test_pattern(output_path: Path) -> None:
    # Figure parameters from problem statement.
    bar_width = 7
    bar_height = 210
    gap = 17
    n_bars = 9

    # Canvas sized to keep the original near-square framing.
    margin_x = 22
    margin_y = 20
    width = (2 * margin_x) + (n_bars * bar_width) + ((n_bars - 1) * gap)
    height = (2 * margin_y) + bar_height

    bg = np.array(hex_to_rgb("#363636"), dtype=np.uint8)
    fg = np.array(hex_to_rgb("#FFFFFF"), dtype=np.uint8)

    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:, :] = bg

    for i in range(n_bars):
        x0 = margin_x + i * (bar_width + gap)
        x1 = x0 + bar_width
        y0 = margin_y
        y1 = y0 + bar_height
        image[y0:y1, x0:x1] = fg

    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(image, mode="RGB").save(output_path)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent / "figures" / "fig1_test_pattern.png"
    make_test_pattern(out)
    print(f"Wrote {out}")
