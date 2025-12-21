#!/bin/bash
cd "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures"

for char in {1..2}; do
    filename="fig_hardware_setup_optF2_${char}.tex"
    echo "Compiling $filename..."
    /Library/TeX/texbin/pdflatex -interaction=nonstopmode "$filename"
    rm "fig_hardware_setup_optF2_${char}.aux" "fig_hardware_setup_optF2_${char}.log"
done

echo "Done compiling F2 variants."
