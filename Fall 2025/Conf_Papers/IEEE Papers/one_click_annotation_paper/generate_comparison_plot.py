#!/usr/bin/env python3
"""
Generate comparison TikZ plot showing all models' mAP50 training curves.
"""
import csv
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "training_results"
LATEX_FIG_DIR = Path(__file__).parent / "latex_figures"

TIKZ_PREAMBLE = r"""\documentclass{article}
\usepackage{pgfplots}
\usepackage{xcolor}

\pgfplotsset{compat=1.18}

\definecolor{Garnet}{HTML}{73000A}
\definecolor{Gray10}{gray}{0.10}
\definecolor{Gray30}{gray}{0.30}
\definecolor{Gray50}{gray}{0.50}
\definecolor{Gray70}{gray}{0.70}
\definecolor{Gray90}{gray}{0.90}

\pgfplotsset{
  every axis/.style={
    axis line style={draw=black, line width=0.6pt},
    tick style={draw=black, line width=0.6pt},
    tick label style={font=\footnotesize\color{black}},
    label style={font=\small\color{black}},
    grid=both,
    grid style={draw=Gray90, line width=0.3pt},
    legend style={
      draw=none,
      font=\footnotesize\color{black},
      fill=white,
      at={(0.5,0.05)},
      anchor=south,
    },
  },
  linestyle/.style={
    line width=0.9pt,
    mark=none,
  },
}

\begin{document}
"""

TIKZ_POSTAMBLE = r"""\end{document}
"""

def read_csv(filepath):
    """Read training data from CSV."""
    data = []
    with open(filepath) as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                'epoch': int(row['epoch']),
                'mAP50': float(row['mAP50']),
            })
    return data

def create_tikz_data_string(data):
    """Create TikZ coordinates string."""
    coords = []
    for d in data:
        coords.append(f"({d['epoch']},{d['mAP50']:.6f})")
    return "\n  ".join(coords)

def generate_comparison_plot():
    """Generate comparison plot for all models."""

    models = [
        ('yolov12_single', 'YOLOv12-L (Single)', 'black'),
        ('yolov12_ddp', 'YOLOv12-L (DDP)', 'Gray30'),
        ('so_detr', 'SO-DETR', 'Gray50'),
        ('ms_detr', 'MS-DETR', 'Gray70'),
        ('rf_detr', 'RF-DETR', 'Garnet'),
    ]

    tikz_code = TIKZ_PREAMBLE
    tikz_code += """
% Model Training Comparison - mAP50
\\begin{figure}[h]
\\centering
\\begin{tikzpicture}
\\begin{axis}[
  xlabel={Epoch},
  ylabel={mAP50},
  width=8cm,
  height=6cm,
  xmax=150,
  legend pos=south east,
]
"""

    for csv_name, display_name, color in models:
        csv_path = RESULTS_DIR / f"{csv_name}_training_data.csv"

        if not csv_path.exists():
            print(f"Warning: {csv_path} not found")
            continue

        data = read_csv(csv_path)
        coords = create_tikz_data_string(data)

        tikz_code += f"""
\\addplot[linestyle, color={color}] coordinates {{
  {coords}
}};
\\addlegendentry{{{display_name}}}
"""

    tikz_code += """
\\end{axis}
\\end{tikzpicture}
\\caption{Training progress comparison: mAP50 across all models over epochs.}
\\end{figure}

"""
    tikz_code += TIKZ_POSTAMBLE

    output_path = LATEX_FIG_DIR / "fig36_training_comparison_mAP50.tex"
    with open(output_path, 'w') as f:
        f.write(tikz_code)

    print(f"Generated training comparison plot: {output_path}")
    return output_path

if __name__ == "__main__":
    generate_comparison_plot()
