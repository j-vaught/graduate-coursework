#!/usr/bin/env python3
"""
Script to generate LaTeX document with 6-panel TikZ figure showing cropped images 
with bounding box annotations and frame IDs as titles.
"""

import os
from pathlib import Path

def generate_latex_document(processed_data_dir, selected_frames, output_latex_path):
    """Generate LaTeX document with 6-panel figure"""

    # Run the processing script again to get the latest selected frames
    # Since we just ran it, we can use the new frames from the most recent run
    # ['000633', '000285', '001618', '001605', '000394', '000178']
    actual_selected_frames = ['000633', '000285', '001618', '001605', '000394', '000178']

    # LaTeX document template
    latex_content = r"""% Radar3000 Dataset Sample Images with Annotations
\documentclass[10pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{graphicx}
\usepackage{subcaption}
\usepackage{xcolor}
\usepackage{tikz}
\usepackage{import}

\begin{document}

\title{Radar3000 Dataset: Sample Images with Annotations}
\author{}
\date{}
\maketitle

\section{Sample Annotations from Radar3000 Dataset}

% 6-panel figure with annotated images
\begin{figure}[htbp]
\centering
"""

    # Create 2 rows of 3 columns with the actual selected frames
    latex_content += "\\begin{subfigure}{0.32\\textwidth}\n"
    latex_content += "\\centering\n"
    latex_content += f"\\includegraphics[width=\\textwidth]{{{'processed_images/000633_annotated.jpg'}}}\n"
    latex_content += "\\caption{Frame ID: 000633}\n"
    latex_content += "\\end{subfigure}\n"
    latex_content += "\\hfill\n"
    latex_content += "\\begin{subfigure}{0.32\\textwidth}\n"
    latex_content += "\\centering\n"
    latex_content += f"\\includegraphics[width=\\textwidth]{{{'processed_images/000285_annotated.jpg'}}}\n"
    latex_content += "\\caption{Frame ID: 000285}\n"
    latex_content += "\\end{subfigure}\n"
    latex_content += "\\hfill\n"
    latex_content += "\\begin{subfigure}{0.32\\textwidth}\n"
    latex_content += "\\centering\n"
    latex_content += f"\\includegraphics[width=\\textwidth]{{{'processed_images/001618_annotated.jpg'}}}\n"
    latex_content += "\\caption{Frame ID: 001618}\n"
    latex_content += "\\end{subfigure}\n\n"

    latex_content += "\\vspace{0.2cm}\n\n"  # Add vertical space between rows

    latex_content += "\\begin{subfigure}{0.32\\textwidth}\n"
    latex_content += "\\centering\n"
    latex_content += f"\\includegraphics[width=\\textwidth]{{{'processed_images/001605_annotated.jpg'}}}\n"
    latex_content += "\\caption{Frame ID: 001605}\n"
    latex_content += "\\end{subfigure}\n"
    latex_content += "\\hfill\n"
    latex_content += "\\begin{subfigure}{0.32\\textwidth}\n"
    latex_content += "\\centering\n"
    latex_content += f"\\includegraphics[width=\\textwidth]{{{'processed_images/000394_annotated.jpg'}}}\n"
    latex_content += "\\caption{Frame ID: 000394}\n"
    latex_content += "\\end{subfigure}\n"
    latex_content += "\\hfill\n"
    latex_content += "\\begin{subfigure}{0.32\\textwidth}\n"
    latex_content += "\\centering\n"
    latex_content += f"\\includegraphics[width=\\textwidth]{{{'processed_images/000178_annotated.jpg'}}}\n"
    latex_content += "\\caption{Frame ID: 000178}\n"
    latex_content += "\\end{subfigure}\n\n"

    latex_content += r"""
\caption{Sample images from the Radar3000 dataset with bounding box annotations. Each panel shows a different frame with radar targets marked using bounding boxes.}
\label{fig:radar3000_samples}
\end{figure}

\end{document}
"""
    
    # Write LaTeX content to file
    with open(output_latex_path, 'w') as f:
        f.write(latex_content)
    
    print(f"LaTeX document generated: {output_latex_path}")

def get_selected_frames_from_log(log_file_path):
    """Extract the selected frame IDs from the processing script output"""
    # In a real implementation, you'd parse the actual output
    # For now, we'll return the frames from our previous run
    return ['001961', '002250', '001289', '000819', '000977', '001675']

if __name__ == "__main__":
    # Define paths
    processed_data_dir = "/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/processed_images"
    output_latex_path = "/Users/jacobvaught/Downloads/Classes/Fall 2025/Conf_Papers/IEEE Papers/one_click_annotation_paper/radar3000_samples.tex"
    
    # For now, using the frame IDs from the previous run
    selected_frames = ['001961', '002250', '001289', '000819', '000977', '001675']
    
    # Generate the LaTeX document
    generate_latex_document(processed_data_dir, selected_frames, output_latex_path)
    
    print("LaTeX document with 6-panel figure has been generated successfully!")