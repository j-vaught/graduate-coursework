from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from scipy import ndimage


HW4_DIR = Path(__file__).resolve().parent
FIG_DIR = HW4_DIR / "figures"
INPUT_PATH = FIG_DIR / "fig1_test_pattern.png"
OUT_DIR = FIG_DIR / "problem3_filter_outputs"
KERNEL_SIZE = 9


def load_binary_image(path: Path) -> np.ndarray:
    img = Image.open(path).convert("L")
    arr = np.array(img, dtype=np.float64)
    # Problem statement assumes strict black/white levels: 0 and 255.
    return np.where(arr >= 128.0, 255.0, 0.0)


def save_grayscale(path: Path, arr: np.ndarray) -> None:
    clipped = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(clipped, mode="L").save(path)


def geometric_mean_func(window: np.ndarray) -> float:
    if np.any(window <= 0):
        return 0.0
    return float(np.exp(np.mean(np.log(window))))


def harmonic_mean_func(window: np.ndarray) -> float:
    if np.any(window <= 0):
        return 0.0
    return float(window.size / np.sum(1.0 / window))


def contraharmonic_func(window: np.ndarray, q: float) -> float:
    if q < 0 and np.any(window <= 0):
        return 0.0
    numerator = np.sum(np.power(window, q + 1))
    denominator = np.sum(np.power(window, q))
    if np.isclose(denominator, 0.0):
        return 0.0
    return float(numerator / denominator)


def compute_filters(img: np.ndarray) -> dict[str, np.ndarray]:
    mode = "constant"
    cval = 0.0

    arithmetic = ndimage.uniform_filter(img, size=KERNEL_SIZE, mode=mode, cval=cval)
    geometric = ndimage.generic_filter(
        img,
        function=geometric_mean_func,
        size=KERNEL_SIZE,
        mode=mode,
        cval=cval,
    )
    harmonic = ndimage.generic_filter(
        img,
        function=harmonic_mean_func,
        size=KERNEL_SIZE,
        mode=mode,
        cval=cval,
    )
    contra_q1 = ndimage.generic_filter(
        img,
        function=lambda w: contraharmonic_func(w, 1.0),
        size=KERNEL_SIZE,
        mode=mode,
        cval=cval,
    )
    contra_q0 = ndimage.generic_filter(
        img,
        function=lambda w: contraharmonic_func(w, 0.0),
        size=KERNEL_SIZE,
        mode=mode,
        cval=cval,
    )
    contra_qm1 = ndimage.generic_filter(
        img,
        function=lambda w: contraharmonic_func(w, -1.0),
        size=KERNEL_SIZE,
        mode=mode,
        cval=cval,
    )
    median = ndimage.median_filter(img, size=KERNEL_SIZE, mode=mode, cval=cval)
    maxf = ndimage.maximum_filter(img, size=KERNEL_SIZE, mode=mode, cval=cval)
    minf = ndimage.minimum_filter(img, size=KERNEL_SIZE, mode=mode, cval=cval)
    midpoint = 0.5 * (maxf + minf)

    return {
        "original": img,
        "a_arithmetic_mean": arithmetic,
        "b_geometric_mean": geometric,
        "c_harmonic_mean": harmonic,
        "d_contraharmonic_q1": contra_q1,
        "e_contraharmonic_q0": contra_q0,
        "f_contraharmonic_q-1": contra_qm1,
        "g_median": median,
        "h_max": maxf,
        "i_min": minf,
        "j_midpoint": midpoint,
    }


def render_panel(outputs: dict[str, np.ndarray], out_path: Path) -> None:
    tiles = [
        ("Original", outputs["original"]),
        ("(a) Arithmetic", outputs["a_arithmetic_mean"]),
        ("(b) Geometric", outputs["b_geometric_mean"]),
        ("(c) Harmonic", outputs["c_harmonic_mean"]),
        ("(d) Contra Q=1", outputs["d_contraharmonic_q1"]),
        ("(e) Contra Q=0", outputs["e_contraharmonic_q0"]),
        ("(f) Contra Q=-1", outputs["f_contraharmonic_q-1"]),
        ("(g) Median", outputs["g_median"]),
        ("(h) Max", outputs["h_max"]),
        ("(i) Min", outputs["i_min"]),
        ("(j) Midpoint", outputs["j_midpoint"]),
    ]

    fig, axes = plt.subplots(3, 4, figsize=(11, 8.8), facecolor="#FFFFFF")
    flat_axes = axes.flatten()

    for ax in flat_axes:
        ax.axis("off")

    for idx, (title, arr) in enumerate(tiles):
        ax = flat_axes[idx]
        ax.imshow(np.clip(arr, 0, 255), cmap="gray", vmin=0, vmax=255, interpolation="nearest")
        ax.set_title(title, fontsize=9, color="#73000A", pad=5)

    # Empty last slot (12th tile)
    flat_axes[-1].axis("off")

    fig.suptitle(
        "HW4 Problem 3: 9x9 Filter Outputs",
        fontsize=13,
        fontweight="bold",
        color="#000000",
        y=0.98,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out_path, dpi=220, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    img = load_binary_image(INPUT_PATH)
    outputs = compute_filters(img)

    for name, arr in outputs.items():
        save_grayscale(OUT_DIR / f"{name}.png", arr)

    render_panel(outputs, OUT_DIR / "problem3_filter_comparison.png")

    print(f"Wrote outputs to: {OUT_DIR}")


if __name__ == "__main__":
    main()
