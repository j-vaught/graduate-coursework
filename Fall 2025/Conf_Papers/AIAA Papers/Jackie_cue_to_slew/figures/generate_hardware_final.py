import os

# Common header
header = r"""\documentclass[tikz,border=5mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, calc, backgrounds, fit, matrix, patterns, decorations.pathmorphing, decorations.markings, shadows, spy}

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

# --- Helper for FLIR Camera Art (Micro-macro) ---
# Defines a reusable small pic for the FLIR M232 style camera
flir_cam_def = r"""
\tikzset{
    flir_cam/.pic={
        % Body Base
        \fill[CWhite] (-0.2, 0) rectangle (0.2, 0.25);
        \draw[gray, thin] (-0.2, 0) rectangle (0.2, 0.25);
        % Dome Head
        \shade[ball color=CWhite] (0, 0.35) circle (0.2);
        % Lens (Black dot)
        \fill[black] (0.12, 0.35) ellipse (0.05 and 0.08);
        % Logo text hint
        \node[font=\tiny, scale=0.2, text=gray] at (0, 0.12) {FLIR};
    }
}
"""

# --- Final Option A: Polished nested cones with Callout Bubble ---
# - Better camera icons (white domes)
# - "Spy" style magnification bubble showing the target up close
# - Clearer labels
finalA = flir_cam_def + r"""
\begin{tikzpicture}[x={(0.866cm,0.4cm)}, y={(-0.866cm,0.4cm)}, z={(0cm,1cm)}]
    % Setup
    \coordinate (CamL) at (-0.8, -0.5, 0.1); % Fixed Left
    \coordinate (CamR) at (0.8, -0.5, 0.1);  % PTZ Right
    \coordinate (TargetDist) at (8, 0, 0);   % Far away
    
    % --- Base Plate ---
    \fill[CDark] (-1.5, -1.5, 0) -- (1.5, -1.5, 0) -- (1.5, 0.5, 0) -- (-1.5, 0.5, 0) -- cycle;
    \node[white, font=\tiny\sffamily] at (-1.2, -1.2, 0) {Sensor Rig};
    
    % --- Cameras (Using Pic) ---
    % Fixed Cam
    \pic at (CamL) {flir_cam};
    \node[below, font=\tiny\sffamily, align=center] at (-0.8, -0.6, 0) {Fixed\\(Wide)};

    % PTZ Cam (Rotated slightly visually by adjusting lens pos? Hard in 2D pic, so we use label)
    \pic at (CamR) {flir_cam};
    \node[below, font=\tiny\sffamily, align=center] at (0.8, -0.6, 0) {Slewable\\(Zoom)};

    % --- Geometry Targets ---
    \coordinate (T1) at (9, -3, 2);
    \coordinate (T2) at (9, 0, 4); % Active Target
    \coordinate (T3) at (9, 3, 1);
    
    % --- Wide Coverage (Blue Pyramid) ---
    \coordinate (BL) at (9, -6, -2);
    \coordinate (BR) at (9, 6, -2);
    \coordinate (TR) at (9, 6, 8);
    \coordinate (TL) at (9, -6, 8);
    
    % Frustum Edges
    \draw[CBlue, thin, opacity=0.3] (CamL) -- (BL);
    \draw[CBlue, thin, opacity=0.3] (CamL) -- (BR);
    \draw[CBlue, thin, opacity=0.3] (CamL) -- (TR);
    \draw[CBlue, thin, opacity=0.3] (CamL) -- (TL);
    
    % Back Face (The Field)
    \fill[CBlue, opacity=0.03] (BL) -- (BR) -- (TR) -- (TL) -- cycle;
    \draw[CBlue, dashed, opacity=0.4] (BL) -- (BR) -- (TR) -- (TL) -- cycle;
    \node[CBlue, font=\small\sffamily] at (9, 0, 7.5) {Global Wide FoV};
    
    % --- Objects ---
    \foreach \p in {T1,T3} {
        \node[star, star points=5, fill=gray!70, inner sep=1.5pt] at (\p) {};
    }
    
    % Active Target Star
    \node[star, star points=5, fill=CGold, inner sep=2pt] (ActiveStar) at (T2) {};
    
    % --- Slew Beam (Red Cone) ---
    % Tip of PTZ
    \coordinate (PTZTip) at ($(CamR)+(0,0.4,0)$);
    
    % Circle around target
    \fill[Garnet, opacity=0.2] (T2) circle (0.5);
    \draw[Garnet, thick] (PTZTip) -- (T2);
    % Side cone edges
    \fill[Garnet, opacity=0.1] (PTZTip) -- ($(T2)+(0,-0.5,0)$) -- ($(T2)+(0,0.5,0)$) -- cycle;
    
    % --- Zoom Inset Bubble (Magnifying Glass) ---
    \node[circle, draw=Garnet, thick, fill=white, inner sep=0pt, minimum size=1.5cm] (ZoomBubble) at (5, 4, 5) {};
    \node[star, star points=5, fill=CGold, minimum size=0.8cm] at (ZoomBubble.center) {};
    \node[below, font=\tiny\sffamily] at (ZoomBubble.south) {Zoom View};
    
    % Connecting line
    \draw[Garnet, dashed] (T2) -- (ZoomBubble);
    
    % --- Distance Annote ---
    \draw[<->, gray] (-1.5, -2, 0) -- (9, -2, 0) node[midway, below, fill=white] {Range $R \gg b$};
    
\end{tikzpicture}
"""

# --- Final Option B: With Tripod Legs and clearer separation ---
# Similar to A but adds tripod legs to ground it in reality
finalB = flir_cam_def + r"""
\begin{tikzpicture}[x={(0.866cm,0.4cm)}, y={(-0.866cm,0.4cm)}, z={(0cm,1cm)}]
    % --- Tripod ---
    \coordinate (CenterBase) at (0,-1,0);
    \draw[thick, CDark] (CenterBase) -- ++(-1, -3, -2);
    \draw[thick, CDark] (CenterBase) -- ++(1, -3, -2);
    \draw[thick, CDark] (CenterBase) -- ++(0, -3, 2);
    \fill[CDark] (-1.5, -1.5, 0) -- (1.5, -1.5, 0) -- (1.5, 0.5, 0) -- (-1.5, 0.5, 0) -- cycle;
    
    % Cameras
    \pic at (-0.8, -0.5, 0) {flir_cam};
    \pic at (0.8, -0.5, 0) {flir_cam};
    
    % Targets
    \coordinate (T) at (10, 0, 4);
    
    % Wide Beam (Simplified)
    \coordinate (SourceL) at (-0.8, -0.2, 0);
    \fill[CBlue, opacity=0.1] (SourceL) -- (10, -5, -2) -- (10, 5, -2) -- (10, 5, 8) -- (10, -5, 8) -- cycle;
    \draw[CBlue, dashed] (SourceL) -- (10, -5, 8);
    \draw[CBlue, dashed] (SourceL) -- (10, 5, 8);
    \draw[CBlue, dashed] (SourceL) -- (10, -5, -2);
    \draw[CBlue, dashed] (SourceL) -- (10, 5, -2);
    
    % Zoom Beam
    \coordinate (SourceR) at (0.8, -0.2, 0);
    \fill[Garnet, opacity=0.3] (SourceR) -- ($(T)+(0,-0.5,-0.5)$) -- ($(T)+(0,0.5,0.5)$) -- cycle;
    \draw[Garnet, thick] (SourceR) -- (T);
    
    % Target
    \node[circle, fill=CGold, inner sep=2pt] at (T) {};
    \node[right, font=\bfseries] at (T) {Object};
    
    % Labels
    \node[below, font=\scriptsize, align=center] at (-0.8, -1.5, 0) {Wide};
    \node[below, font=\scriptsize, align=center] at (0.8, -1.5, 0) {Zoom};
    
\end{tikzpicture}
"""


# Map options to files
options = {
    "fig_hardware_setup_finalA.tex": finalA,
    "fig_hardware_setup_finalB.tex": finalB,
}

base_path = "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures/"

for filename, content in options.items():
    write_tex(os.path.join(base_path, filename), content)
