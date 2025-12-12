# Figure Style Guide (LaTeX / TikZ / PGFPlots)

This document defines the required visual style for all paper figures as they are converted from Python outputs into LaTeX-native graphics. The goals are: consistent academic look, print-friendly grayscale readability, and simple geometry.

---

## 1. Color Palette

Only these colors may be used:

- **Black**: `#000000`
- **White**: `#FFFFFF`
- **Grays**: any shade of gray between black and white
- **Garnet (accent)**: `#73000A`

LaTeX definitions to include in any figure preamble:

```tex
\usepackage{xcolor}
\definecolor{Garnet}{HTML}{73000A}
% Optional named grays for convenience
\definecolor{Gray10}{gray}{0.10}
\definecolor{Gray30}{gray}{0.30}
\definecolor{Gray50}{gray}{0.50}
\definecolor{Gray70}{gray}{0.70}
\definecolor{Gray90}{gray}{0.90}
```

**Usage rules**
- Garnet is the *only* chromatic accent; use it sparingly to highlight key series/blocks.
- Prefer grays/black for secondary elements.
- Ensure every figure remains legible when printed in grayscale.

---

## 2. Typography

- Use **default LaTeX serif font** (Computer Modern / Latin Modern).  
  Do **not** use any sans‑serif fonts or font overrides.
- **All text must be black.**
- **No bold text** anywhere (including titles, legends, annotations, or axis labels).
- Italics are allowed for variables or mild emphasis.
- Keep font sizes consistent within a figure (typically `\small` or `\footnotesize` for labels/annotations).

---

## 3. Shapes & Boxes

- **No rounded corners.**  
  Allowed primitives:
  - **Rectangle** with sharp corners
  - **Circle**
  - **Polygon** (only when needed)
- **No ovals/ellipses** and **no rounded rectangles**.
- **All boxes/nodes must have a black outline.**
- Fills may use any allowed palette color, optionally with transparency.

TikZ defaults:

```tex
\tikzset{
  box/.style={
    draw=black,
    line width=0.6pt,
    inner sep=3pt,
    align=center,
    font=\small\color{black}
  },
  circ/.style={
    circle,
    draw=black,
    line width=0.6pt,
    inner sep=2.5pt,
    font=\small\color{black}
  }
}
```

---

## 4. Arrows & Connectors

- **No curved arrows.**
- Connectors must be:
  - single straight segments, or
  - orthogonal paths with **90° bends** only.
- No rounded joins; keep corners sharp.
- Arrow color: black.

TikZ defaults:

```tex
\tikzset{
  conn/.style={
    draw=black,
    -{Stealth[length=2.2mm,width=1.6mm]},
    line width=0.6pt,
    line cap=butt,
    line join=miter
  }
}
% Use |- or -| for 90-degree routes.
```

---

## 5. Charts (PGFPlots)

**Required**
- Every chart **must** have axis labels (x and y).
- **No plot titles.**
- Grid should be visible and light gray.

**Bars**
- Bars must be **outlined in black**.
- Bar fills must be **semi‑transparent** (grid visible behind).  
  Typical `fill opacity` between `0.5–0.7`.

Recommended PGFPlots style:

```tex
\pgfplotsset{
  compat=1.18,
  every axis/.style={
    axis line style={draw=black, line width=0.6pt},
    tick style={draw=black, line width=0.6pt},
    tick label style={font=\footnotesize\color{black}},
    label style={font=\small\color{black}},
    grid=both,
    grid style={draw=Gray70, line width=0.4pt},
    legend style={
      draw=none,
      font=\footnotesize\color{black},
      fill=white,
    },
    title style={font=\small\color{black}}, % keep empty; no titles used
  },
  barstyle/.style={
    ybar,
    bar width=6pt,
    draw=black,
    fill=Garnet,
    fill opacity=0.6
  }
}
```

**Lines/markers**
- Primary series: black or garnet.
- Secondary series: gray shades.
- Marker edges black; marker fills may be garnet/gray with modest opacity.
- Avoid heavy saturation; keep contrast clear.

---

## 6. Layout & Export

- Prefer **vector** figures (`.pdf` or LaTeX `.tex` via TikZ/PGFPlots). Avoid raster unless unavoidable.
- Match paper column widths:
  - single‑column: `width=\linewidth`
  - two‑column/large: `width=0.95\textwidth` (as needed)
- Keep whitespace tight but readable; use consistent margins.

---

## 7. File Organization & Naming

- LaTeX sources go in `latex_figures/` as `figXX_short_name.tex`.
- If a compiled vector output is needed, place it in `figures/` as `figXX_short_name.pdf`.
- Maintain the existing numbering scheme (`fig01_…`, `fig02_…`, etc.) to align with the paper.

---

## 8. Python → LaTeX Conversion Guidance

Prefer **rewriting charts/diagrams directly in TikZ/PGFPlots** for full style control.  
If exporting from Matplotlib, use the PGF backend and strict rcParams.

Matplotlib rcParams baseline (for PGF export):

```python
import matplotlib as mpl
mpl.rcParams.update({
    "pgf.texsystem": "pdflatex",
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": [],      # default LaTeX serif
    "font.sans-serif": [], # do not use
    "font.size": 10,
    "text.color": "black",
    "axes.labelcolor": "black",
    "axes.edgecolor": "black",
    "axes.linewidth": 0.6,
    "xtick.color": "black",
    "ytick.color": "black",
    "grid.color": "0.7",
    "grid.linewidth": 0.4,
    "patch.edgecolor": "black",
})
```

Palette in Matplotlib:

```python
GARNET = "#73000A"
GRAY = ["#000000", "#333333", "#666666", "#999999", "#CCCCCC"]
```

Bar example:

```python
plt.bar(x, y, color=GARNET, alpha=0.6, edgecolor="black", linewidth=0.6)
plt.grid(True, color="#B3B3B3", linewidth=0.4)
```

---

## 9. Pre‑Submit Checklist

Before considering a figure final:

- Uses only black/white/grays and garnet.
- Default serif font only; all text black; no bold.
- No rounded shapes; only rectangles, circles, or polygons.
- All boxes outlined in black.
- Arrows straight or orthogonal; no curves.
- No figure titles; annotations/callouts OK.
- Charts have axis labels; grids visible.
- Bar fills semi‑transparent with black outlines.
- Exports as vector `.tex`/`.pdf` when possible.

---

If you want, I can start by converting a specific figure (e.g., `fig23_annotator_gui` or a PGFPlots chart) following this guide.
