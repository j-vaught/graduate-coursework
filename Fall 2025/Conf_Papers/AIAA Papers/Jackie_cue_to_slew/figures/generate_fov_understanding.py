import os

# Common header
header = r"""\documentclass[tikz,border=5mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, calc, patterns}

% --- COLOR DEFINITIONS ---
\definecolor{Garnet}{HTML}{73000A}
\definecolor{CBlue}{HTML}{466A9F}
\definecolor{CDark}{HTML}{1F414D}
\definecolor{CGold}{HTML}{A49137}
\definecolor{CGrayLight}{HTML}{E5E5E5}
\definecolor{CGrayDark}{HTML}{555555}
\definecolor{CWhite}{HTML}{FFFFFF}

\begin{document}
"""

footer = r"""
\end{document}
"""

def write_tex(filename, content):
    with open(filename, 'w') as f:
        f.write(header + content + footer)
    print(f"Generated {filename}")

# --- TOP-DOWN VIEW with FOV ---
# Looking straight down - shows the horizontal (azimuth/pan) FOV coverage
top_down_fov = r"""
\begin{tikzpicture}[scale=0.8]
    % Title
    \node[font=\bfseries\large] at (0, -1.5) {TOP-DOWN VIEW};
    
    % Cameras (simple dots, side by side)
    \fill[CBlue] (-0.3, 0) circle (0.15);
    \fill[Garnet] (0.3, 0) circle (0.15);
    \node[below, font=\tiny] at (-0.3, -0.3) {Fixed};
    \node[below, font=\tiny] at (0.3, -0.3) {PTZ};
    
    % Wide FOV (Blue) - Large triangle pointing up
    \fill[CBlue, opacity=0.15] (-0.3, 0) -- (-5, 8) -- (5, 8) -- cycle;
    \draw[CBlue, thick] (-0.3, 0) -- (-5, 8);
    \draw[CBlue, thick] (-0.3, 0) -- (5, 8);
    \node[CBlue, font=\small] at (0, 7.5) {Wide FoV};
    
    % Zoom FOV (Red) - Narrow triangle INSIDE the blue one
    % Currently pointing slightly to the right
    \fill[Garnet, opacity=0.3] (0.3, 0) -- (2, 8) -- (3, 8) -- cycle;
    \draw[Garnet, thick] (0.3, 0) -- (2, 8);
    \draw[Garnet, thick] (0.3, 0) -- (3, 8);
    \node[Garnet, font=\small] at (2.5, 6) {Zoom FoV};
    
    % Target inside zoom beam
    \node[star, star points=5, fill=CGold, minimum size=0.4cm] at (2.5, 7) {};
    
    % Other objects in wide FOV but outside zoom
    \node[circle, fill=gray, inner sep=2pt] at (-2, 5) {};
    \node[circle, fill=gray, inner sep=2pt] at (0, 4) {};
    
    % Pan arrows showing zoom can move
    \draw[->, Garnet, dashed, thick] (1.5, 4) arc (70:20:2);
    \draw[->, Garnet, dashed, thick] (1.5, 4) arc (70:120:2);
    \node[Garnet, font=\tiny] at (1.5, 3.5) {Pan Range};
    
\end{tikzpicture}
"""

# --- SIDE VIEW with FOV ---
# Looking from the side - shows the vertical (elevation/tilt) FOV coverage
side_view_fov = r"""
\begin{tikzpicture}[scale=0.8]
    % Title
    \node[font=\bfseries\large] at (4, -1) {SIDE VIEW};
    
    % Cameras (appear as one dot since they are side-by-side in this view)
    \fill[CDark] (0, 0) circle (0.2);
    \node[below, font=\tiny] at (0, -0.3) {Cameras};
    
    % Wide FOV (Blue) - Vertical spread
    \fill[CBlue, opacity=0.15] (0, 0) -- (8, 3) -- (8, -2) -- cycle;
    \draw[CBlue, thick] (0, 0) -- (8, 3);
    \draw[CBlue, thick] (0, 0) -- (8, -2);
    \node[CBlue, font=\small] at (7, 3.5) {Wide FoV};
    
    % Zoom FOV (Red) - Narrow, tilted upward to track target
    \fill[Garnet, opacity=0.3] (0, 0) -- (8, 2.5) -- (8, 1.5) -- cycle;
    \draw[Garnet, thick] (0, 0) -- (8, 2.5);
    \draw[Garnet, thick] (0, 0) -- (8, 1.5);
    \node[Garnet, font=\small] at (6, 1) {Zoom FoV};
    
    % Target
    \node[star, star points=5, fill=CGold, minimum size=0.4cm] at (7, 2) {};
    
    % Tilt arrows
    \draw[->, Garnet, dashed, thick] (2, 1) arc (30:60:1.5);
    \draw[->, Garnet, dashed, thick] (2, 1) arc (30:0:1.5);
    \node[Garnet, font=\tiny] at (2, 0.3) {Tilt Range};
    
    % Horizon line
    \draw[gray, dashed] (0, 0) -- (8, 0);
    \node[gray, font=\tiny] at (8.5, 0) {Horizon};
    
\end{tikzpicture}
"""

# Map options to files
options = {
    "fig_fov_understanding_topdown.tex": top_down_fov,
    "fig_fov_understanding_side.tex": side_view_fov,
}

base_path = "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures/"

for filename, content in options.items():
    write_tex(os.path.join(base_path, filename), content)
