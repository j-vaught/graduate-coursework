#!/usr/bin/env python3
"""
Generate TikZ/PGFPlots figures for model training from extracted CSV data.
Following the IEEE conference style guide.
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
      at={(0.95,0.05)},
      anchor=south east,
    },
  },
  linestyle/.style={
    line width=0.8pt,
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
            val_loss = row['val_loss'].strip()
            data.append({
                'epoch': int(row['epoch']),
                'train_loss': float(row['train_loss']),
                'val_loss': float(val_loss) if val_loss and val_loss != 'None' else None,
                'mAP50': float(row['mAP50']),
                'mAP50_95': float(row['mAP50_95']),
            })
    return data

def create_tikz_data_point(epoch, value):
    """Create a TikZ coordinate."""
    if value is None:
        return None
    return f"({epoch},{value:.6f})"

def create_plot_command(data, metric_name, metric_key, ylabel, has_val=False, ymax=None):
    """Generate PGFPlots axis for a single metric."""
    plot_code = f"""
\\begin{{axis}}[
  xlabel={{Epoch}},
  ylabel={{{ylabel}}},
  width=5.5cm,
  height=4.5cm,
  legend pos=south east,
]
"""

    # Add training data
    coords = [create_tikz_data_point(d['epoch'], d[metric_key]) for d in data]
    coords = [c for c in coords if c is not None]

    plot_code += "\\addplot[linestyle, color=black] coordinates {\n"
    plot_code += "\n".join(f"  {c}" for c in coords)
    plot_code += "\n};\n\\addlegendentry{train}\n"

    # Add validation data if available
    if has_val and any(d['val_loss'] is not None for d in data):
        val_metric = 'val_loss' if metric_key == 'train_loss' else metric_key
        coords = [create_tikz_data_point(d['epoch'], d[val_metric]) for d in data if d[val_metric] is not None]
        if coords:
            plot_code += "\\addplot[linestyle, color=Gray50] coordinates {\n"
            plot_code += "\n".join(f"  {c}" for c in coords)
            plot_code += "\n};\n\\addlegendentry{val}\n"

    plot_code += "\\end{axis}\n"
    return plot_code

def create_model_figure(model_name, data, figure_number):
    """Create a complete TikZ figure for a model showing 4 metrics."""
    tikz_code = f"""
% {model_name} Training Progress
\\begin{{figure}}[h]
\\centering
\\begin{{tikzpicture}}
"""

    # Determine if we have validation data
    has_val = any(d['val_loss'] is not None for d in data)

    # Loss plot
    tikz_code += "\\begin{scope}\n"
    tikz_code += create_plot_command(data, 'train_loss', 'train_loss', 'Training Loss', has_val=has_val)
    tikz_code += "\\end{scope}\n"

    # mAP50 plot (offset to the right)
    tikz_code += "\\begin{scope}[xshift=6cm]\n"
    tikz_code += create_plot_command(data, 'mAP50', 'mAP50', 'mAP50')
    tikz_code += "\\end{scope}\n"

    # mAP50-95 plot (below)
    tikz_code += "\\begin{scope}[yshift=-5cm]\n"
    tikz_code += create_plot_command(data, 'mAP50-95', 'mAP50_95', 'mAP50-95')
    tikz_code += "\\end{scope}\n"

    tikz_code += "\\end{tikzpicture}\n"
    tikz_code += f"\\caption{{{model_name} training progress over epochs.}}\n"
    tikz_code += "\\end{figure}\n"

    return tikz_code

def create_single_metric_figure(model_name, data, metric_key, ylabel, figure_number):
    """Create a focused single-metric TikZ figure."""
    tikz_code = f"""
% {model_name} {ylabel}
\\begin{{figure}}[h]
\\centering
\\begin{{tikzpicture}}
\\begin{{axis}}[
  xlabel={{Epoch}},
  ylabel={{{ylabel}}},
  width=6.5cm,
  height=5.5cm,
]
"""

    # Add training data
    coords = [create_tikz_data_point(d['epoch'], d[metric_key]) for d in data]
    coords = [c for c in coords if c is not None]

    tikz_code += "\\addplot[linestyle, color=black] coordinates {\n"
    tikz_code += "\n".join(f"  {c}" for c in coords)
    tikz_code += "\n};\n"

    tikz_code += "\\end{axis}\n"
    tikz_code += "\\end{tikzpicture}\n"
    tikz_code += "\\end{figure}\n"

    return tikz_code

def generate_all_plots():
    """Generate TikZ plots for all models."""
    models = {
        'yolov12_single': ('YOLOv12-L Single', 'fig31_yolov12_single_training.tex'),
        'yolov12_ddp': ('YOLOv12-L DDP', 'fig32_yolov12_ddp_training.tex'),
        'so_detr': ('SO-DETR', 'fig33_so_detr_training.tex'),
        'ms_detr': ('MS-DETR', 'fig34_ms_detr_training.tex'),
        'rf_detr': ('RF-DETR', 'fig35_rf_detr_training.tex'),
    }

    fig_num = 31
    for csv_name, (display_name, filename) in models.items():
        csv_path = RESULTS_DIR / f"{csv_name}_training_data.csv"

        if not csv_path.exists():
            print(f"Warning: {csv_path} not found")
            continue

        data = read_csv(csv_path)

        # Create single-metric plots for efficiency
        tikz_code = TIKZ_PREAMBLE

        # Add plots for mAP50 and mAP50-95 (most important metrics)
        tikz_code += create_single_metric_figure(display_name, data, 'mAP50', 'mAP50', fig_num)
        tikz_code += create_single_metric_figure(display_name, data, 'mAP50_95', 'mAP50-95', fig_num + 1)

        tikz_code += TIKZ_POSTAMBLE

        output_path = LATEX_FIG_DIR / filename
        with open(output_path, 'w') as f:
            f.write(tikz_code)

        print(f"Generated {filename} with {len(data)} epochs")
        fig_num += 2

if __name__ == "__main__":
    generate_all_plots()
