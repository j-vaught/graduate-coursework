import os

# Common header
header = r"""\documentclass[tikz,border=5mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, calc, backgrounds, fit, matrix, patterns, decorations.pathmorphing, decorations.markings, shadows}

% --- COLOR DEFINITIONS ---
\definecolor{Garnet}{HTML}{73000A}
\definecolor{CSecondaryRed}{HTML}{CC2E40}
\definecolor{CBlue}{HTML}{466A9F}
\definecolor{CDark}{HTML}{1F414D}
\definecolor{COlive}{HTML}{65780B}
\definecolor{CLime}{HTML}{CED318}
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

# --- Option F2.1: The "Nested Cone" Approach ---
# Large transparent blue pyramid (Wide) completely engulfing the scene.
# Small red cone (PTZ) inside it, pointing at one object.
optF2_1 = r"""
\begin{tikzpicture}[x={(0.866cm,0.5cm)}, y={(-0.866cm,0.5cm)}, z={(0cm,1cm)}]
    % Setup
    \coordinate (Origin) at (0,0,0);
    \coordinate (TargetPlaneDist) at (8,0,0); % Distance to target plane
    
    % Platform
    \fill[CGrayDark] (-1, -1, 0) -- (1, -1, 0) -- (1, 1, 0) -- (-1, 1, 0) -- cycle;
    \node[above, font=\tiny, white] at (0,0,0) {Base};

    % Targets in the distance
    % Let's define a virtual plane at x=8
    \coordinate (T1) at (8, -2, 1);
    \coordinate (T2) at (8, 0, 3);
    \coordinate (T3) at (8, 2, -1);
    
    % --- Wide Camera Coverage (The "Pyramid") ---
    % Originating roughly from center-left
    \coordinate (CamFixed) at (-0.5, 0, 0.5);
    \fill[CDark] (CamFixed) circle (0.1); 
    
    % Wide frustum corners at x=8
    \coordinate (BL) at (8, -5, -4);
    \coordinate (BR) at (8, 5, -4);
    \coordinate (TR) at (8, 5, 6);
    \coordinate (TL) at (8, -5, 6);
    
    % Draw Wide FoV Edges
    \draw[CBlue, thin, opacity=0.3] (CamFixed) -- (BL);
    \draw[CBlue, thin, opacity=0.3] (CamFixed) -- (BR);
    \draw[CBlue, thin, opacity=0.3] (CamFixed) -- (TR);
    \draw[CBlue, thin, opacity=0.3] (CamFixed) -- (TL);
    
    % Draw Wide FoV Face (The "Screen")
    \fill[CBlue, opacity=0.05] (BL) -- (BR) -- (TR) -- (TL) -- cycle;
    \draw[CBlue, dashed, opacity=0.5] (BL) -- (BR) -- (TR) -- (TL) -- cycle;
    \node[CBlue, font=\small] at (8, 0, 5) {Fixed Wide FoV Coverage};

    % --- Objects ---
    \foreach \p in {T1,T3} {
        \node[star, star points=5, fill=gray, inner sep=1.5pt] at (\p) {};
    }
    % Active Target
    \node[star, star points=5, fill=CGold, inner sep=2.5pt] (ActiveT) at (T2) {};
    \node[right, CGold, font=\scriptsize] at (T2) {Target};

    % --- PTZ Camera & Beam ---
    \coordinate (CamPTZ) at (0.5, 0, 0.5);
    \node[cylinder, draw=Garnet, fill=white, rotate=100, minimum height=0.4cm, minimum width=0.3cm] at (CamPTZ) {};
    
    % PTZ Beam (Narrow) pointing to T2
    % We create a small cone around T2
    \coordinate (P1) at ($(T2) + (0, -0.5, -0.5)$);
    \coordinate (P2) at ($(T2) + (0, 0.5, -0.5)$);
    \coordinate (P3) at ($(T2) + (0, 0.5, 0.5)$);
    \coordinate (P4) at ($(T2) + (0, -0.5, 0.5)$);
    
    \fill[Garnet, opacity=0.3] (CamPTZ) -- (P1) -- (P2) -- (P3) -- (P4) -- cycle;
    \draw[Garnet, thick] (CamPTZ) -- (T2);
    
    % Annotation
    \node[Garnet, align=center, font=\scriptsize] at (4, -2, 2) {High-Res\\Inspection};

\end{tikzpicture}
"""

# --- Option F2.2: The "Projector" View (Simplified Geometry) ---
# A simpler, cleaner version focusing on the ground plane projection.
# Shows the Wide FoV projecting a large "trapazoid" on the ground/sky.
# PTZ projects a spotlight circle within it.
optF2_2 = r"""
\begin{tikzpicture}
    % Perspective
    \begin{scope}[rotate around x=70, rotate around z=-10]
        
        % Cameras
        \fill[gray] (-1,0) rectangle (1,0.5); % Mount
        \node[circle, fill=CBlue, inner sep=2pt] (CF) at (-0.5, 0.25) {};
        \node[circle, fill=Garnet, inner sep=2pt] (CZ) at (0.5, 0.25) {};
        
        % Field Distance
        \def\dist{6}
        
        % Wide Field (Blue)
        \coordinate (WL) at (-\dist, \dist);
        \coordinate (WR) at (\dist, \dist);
        
        \fill[CBlue, opacity=0.1] (CF) -- (WL) -- (WR) -- cycle;
        \draw[CBlue, dashed] (CF) -- (WL);
        \draw[CBlue, dashed] (CF) -- (WR);
        \draw[CBlue, thick] (WL) -- (WR) node[midway, above, opacity=1] {Global Wide FoV};
        
        % Targets
        \coordinate (Obj1) at (-2, \dist-1);
        \coordinate (Obj2) at (3, \dist-2);
        
        \fill[gray] (Obj1) circle (0.2);
        \node[diamond, fill=CGold, minimum size=0.4cm] (Target) at (Obj2) {};
        
        % Zoom Field (Red Spotlight)
        \fill[Garnet, opacity=0.4] (CZ) -- ($(Target)+(-0.5,0)$) -- ($(Target)+(0.5,0)$) -- cycle;
        %\draw[Garnet, thick] (CZ) -- (Target);
        
        % Labels
        \node[left, font=\tiny, CBlue] at (CF) {Fixed};
        \node[right, font=\tiny, Garnet] at (CZ) {PTZ};
        \node[right, font=\tiny] at (Target) {Zoomed Target};
        
        % R >> b annotation
        \draw[<->] (-1, -0.5) -- (1, -0.5) node[midway, below] {$b$};
        \draw[->] (0, 0.5) -- (0, \dist/2) node[midway, right] {$R \gg b$};
        
    \end{scope}
\end{tikzpicture}
"""


# Map options to files
options = {
    "fig_hardware_setup_optF2_1.tex": optF2_1,
    "fig_hardware_setup_optF2_2.tex": optF2_2,
}

base_path = "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures/"

for filename, content in options.items():
    write_tex(os.path.join(base_path, filename), content)
