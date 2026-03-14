#!/bin/bash
# Compile each slide to its own PDF.
# Concatenates preamble + slide content + \end{document} into a temp file,
# avoiding beamer's #-parameter issues with \input inside frames.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Extract preamble (everything up to and including \begin{document})
# from build_single.tex, minus the \input{\SLIDEFILE} and \end{document} lines
PREAMBLE=$(sed -n '1,/\\begin{document}/p' build_single.tex)

SLIDES=(
  slide00_title
  slide01_hook
  slide02_metric_ambiguity
  slide03_taxonomy
  slide04_architecture
  slide05_focal_length
  slide06_cstm_label
  slide07_cstm_image
  slide08_joint_optimization
  slide09_supervision_sources
  slide10_rpnl
  slide11_loss_summary
  slide12_training_scale
  slide13_benchmarks
  slide14_downstream
  slide15_strengths
  slide16_limitations
  slide17_takeaways
)

echo "Building ${#SLIDES[@]} individual slide PDFs..."

for slide in "${SLIDES[@]}"; do
  printf "  %-35s" "${slide}.tex"

  # Build a self-contained .tex: preamble + slide body + end
  {
    echo "$PREAMBLE"
    cat "${slide}.tex"
    echo ""
    echo "\\end{document}"
  } > "_tmp_${slide}.tex"

  pdflatex -interaction=nonstopmode "_tmp_${slide}.tex" > /dev/null 2>&1
  pdflatex -interaction=nonstopmode "_tmp_${slide}.tex" > /dev/null 2>&1

  mv "_tmp_${slide}.pdf" "${slide}.pdf"
  rm -f "_tmp_${slide}".{tex,aux,log,nav,out,snm,toc,vrb}

  echo "OK"
done

echo ""
echo "Done! Individual PDFs:"
ls -lh "$SCRIPT_DIR"/slide*.pdf
