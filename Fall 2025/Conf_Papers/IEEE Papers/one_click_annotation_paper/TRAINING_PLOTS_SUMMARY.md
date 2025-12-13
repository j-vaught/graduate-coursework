# Training Visualization Summary

Generated TikZ/PGFPlots training progress figures for all models following the IEEE conference style guide.

## Generated Figures

### Individual Model Training Plots

Each model has two dedicated figures showing training metrics:

| Figure | Model | Epochs | File |
|--------|-------|--------|------|
| fig31 | YOLOv12-L (Single GPU) | 150 | `fig31_yolov12_single_training.tex` |
| fig32 | YOLOv12-L (DDP) | 150 | `fig32_yolov12_ddp_training.tex` |
| fig33 | SO-DETR | 150 | `fig33_so_detr_training.tex` |
| fig34 | MS-DETR | 50 | `fig34_ms_detr_training.tex` |
| fig35 | RF-DETR | 50 | `fig35_rf_detr_training.tex` |

**Content per figure:**
- mAP50 curve over training epochs
- mAP50-95 curve over training epochs

### Comparison Plot

| Figure | Content | File |
|--------|---------|------|
| fig36 | All models' mAP50 training curves overlaid | `fig36_training_comparison_mAP50.tex` |

## Style Compliance

All figures follow the IEEE conference style guide:

✓ Color palette: Black/white/gray + Garnet accent only
✓ Typography: Default LaTeX serif, all black text, no bold
✓ Grid: Light gray (Gray90), visible but unobtrusive
✓ Line width: 0.8pt for data lines
✓ Axis labels: Present on both x and y axes
✓ No figure titles (per style guide)
✓ Vector format: PDF + LaTeX source for integration

## File Organization

```
latex_figures/
  fig31_yolov12_single_training.tex    (YOLOv12 Single - 150 epochs)
  fig31_yolov12_single_training.pdf
  fig32_yolov12_ddp_training.tex       (YOLOv12 DDP - 150 epochs)
  fig32_yolov12_ddp_training.pdf
  fig33_so_detr_training.tex           (SO-DETR - 150 epochs)
  fig33_so_detr_training.pdf
  fig34_ms_detr_training.tex           (MS-DETR - 50 epochs)
  fig34_ms_detr_training.pdf
  fig35_rf_detr_training.tex           (RF-DETR - 50 epochs)
  fig35_rf_detr_training.pdf
  fig36_training_comparison_mAP50.tex  (All models comparison)
  fig36_training_comparison_mAP50.pdf
```

## Usage in LaTeX

### Standalone Compilation

```bash
cd latex_figures/
pdflatex fig31_yolov12_single_training.tex
```

### Integration into Paper

```latex
% Include individual figure
\input{latex_figures/fig31_yolov12_single_training.tex}

% Or reference the PDF directly
\includegraphics[width=\linewidth]{latex_figures/fig31_yolov12_single_training.pdf}
```

## Data Sources

- **YOLOv12**: CSV with 150 epochs each (single and DDP variants)
- **SO-DETR**: CSV with 150 epochs
- **MS-DETR**: JSON array with 50 epochs
- **RF-DETR**: JSONL log with 50 epochs

All data extracted and consolidated in:
- `training_results/*_training_data.csv`

## Generation Scripts

Scripts used to generate the figures:

1. `extract_training_data.py` - Extracts metrics from various training log formats
2. `generate_tikz_plots.py` - Generates individual model training plots
3. `generate_comparison_plot.py` - Generates the comparison plot

## Efficiency Notes

For IEEE conference submissions with space constraints:

- Single-column width: Use 6–6.5cm for width parameter
- Two-column/full width: Use 8–9cm for width
- Height: 5.5–6cm maintains aspect ratio and readability
- Current plots use: 6.5cm width × 5.5cm height (efficient single-column)

## Notes

- All metrics plotted directly from training logs
- No Python image outputs used - pure TikZ/PGFPlots for publication quality
- Grid styling follows style guide (light gray at 0.3pt width)
- Legends positioned to minimize whitespace (south east for individual plots, centered bottom for comparison)
- Color assignments:
  - Black: YOLOv12-L (Single)
  - Gray30: YOLOv12-L (DDP)
  - Gray50: SO-DETR
  - Gray70: MS-DETR
  - Garnet: RF-DETR (accent color for best/emphasized model)
