#!/bin/bash
cd "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures"

for char in {A..J}; do
    filename="fig_hardware_setup_opt${char}.tex"
    echo "Compiling $filename..."
    /Library/TeX/texbin/pdflatex -interaction=nonstopmode "$filename"
    rm "fig_hardware_setup_opt${char}.aux" "fig_hardware_setup_opt${char}.log"
done

echo "Done compiling all variants."
