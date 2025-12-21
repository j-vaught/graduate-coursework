#!/bin/bash
cd "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures"

for char in {1..4}; do
    filename="fig_hardware_setup_optF${char}.tex"
    echo "Compiling $filename..."
    /Library/TeX/texbin/pdflatex -interaction=nonstopmode "$filename"
    rm "fig_hardware_setup_optF${char}.aux" "fig_hardware_setup_optF${char}.log"
done

echo "Done compiling F variants."
