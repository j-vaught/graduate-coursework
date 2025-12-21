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

# --- Option F.1: Top-Down with Range Break & Zoom Beam ---
# Concept: Strictly top down. 
# - Baseline labeled 'b'. 
# - Break lines (zigzag) to show distance.
# - Zoom shown as a narrow solid beam inside a lighter 'slew range' sector.
# - Tilt indicated by icon next to camera.
optF1 = r"""
\begin{tikzpicture}
    % Cameras
    \coordinate (C1) at (-0.5, 0);
    \coordinate (C2) at (0.5, 0);
    
    % Camera Bodies
    \fill[CDark] (C1) circle (0.15);
    \fill[CDark] (C2) circle (0.15);
    
    % Baseline annotation
    \draw[<->, >=stealth, thin] (-0.5, -0.4) -- (0.5, -0.4) node[midway, fill=white, inner sep=1pt, font=\tiny] {$b$};
    
    % Fixed FoV (Camera 1)
    \fill[CBlue, opacity=0.15] (C1) -- (-2, 4) -- (1, 4) -- cycle;
    \draw[CBlue, dashed] (C1) -- (-2, 4);
    \draw[CBlue, dashed] (C1) -- (1, 4);
    
    % Slew Range (Camera 2) - The potential area
    \draw[Garnet, dotted, thin] (C2) -- (-1.5, 4);
    \draw[Garnet, dotted, thin] (C2) -- (2.5, 4);
    \draw[<->, Garnet, thin] (0.5, 1) arc (90:60:1);
    \node[Garnet, font=\tiny] at (1.2, 0.8) {Pan};
    
    % Zoom Beam (Camera 2) - Active narrow beam
    \fill[Garnet, opacity=0.4] (C2) -- (0.8, 4) -- (1.2, 4) -- cycle;
    
    % Distance Break
    \draw[decoration={zigzag, segment length=5mm, amplitude=1mm}, decorate, thick, gray] (-2.5, 2.5) -- (3, 2.5);
    \node[fill=white, inner sep=2pt, font=\small, text=gray] at (0, 2.5) {$R \gg b$};
    
    % Object
    \node[star, star points=5, fill=CGold, minimum size=0.5cm] (Obj) at (1.0, 5) {};
    \node[right, font=\tiny, align=left] at (Obj.east) {Distant\\Target};
    
    % Tilt Indicator Icon (Side View graphic next to Cam 2)
    \node[draw, circle, inner sep=1pt, scale=0.5, anchor=west] at (0.8, 0) {
        \tikz{
            \draw[->] (0,0) arc (-45:45:0.3);
            \node[font=\tiny, left] at (0,0) {Tilt};
        }
    };
    
    % Labels
    \node[below=0.6cm, align=center, font=\scriptsize] at (C1) {\textbf{Fixed}\\(Wide)};
    \node[below=0.6cm, align=center, font=\scriptsize] at (C2) {\textbf{Slewable}\\(Zoom)};
\end{tikzpicture}
"""

# --- Option F.2: Isometric 3D View ---
# Concept: 3D view allows pitch (tilt) visualization naturally.
# - Cameras on platform.
# - Cones projecting out.
# - Target far away.
optF2 = r"""
\begin{tikzpicture}[x={(0.866cm,0.5cm)}, y={(-0.866cm,0.5cm)}, z={(0cm,1cm)}]
    % Platform
    \fill[CGrayDark] (-1, -0.5, 0) -- (1, -0.5, 0) -- (1, 0.5, 0) -- (-1, 0.5, 0) -- cycle;
    
    % Cam 1 (Fixed) at (-0.5, 0, 0)
    \node[cylinder, draw=CDark, fill=CWhite, rotate=90, minimum height=0.3cm, minimum width=0.3cm] at (-0.5, 0, 0.2) {};
    
    % Cam 2 (PTZ) at (0.5, 0, 0)
    \node[cylinder, draw=Garnet, fill=CWhite, rotate=90, minimum height=0.3cm, minimum width=0.3cm] (Cam2) at (0.5, 0, 0.2) {};
    
    % 3D Spherical Coordinate Arrows for Cam 2
    \draw[->, Garnet] (0.5, 0, 0.6) arc (90:0:0.3) node[right, font=\tiny] {Tilt};
    \draw[->, Garnet] (0.8, 0, 0.1) arc (0:90:0.3) node[above, font=\tiny] {Pan};
    
    % Projection Beams
    % Fixed Beam
    \fill[CBlue, opacity=0.2] (-0.5, 0, 0.4) -- (-2, 6, 2) -- (1, 6, 2) -- cycle;
    
    % Zoom Beam (Narrow, Directed Up)
    \fill[Garnet, opacity=0.4] (0.5, 0, 0.4) -- (3, 6, 3.5) -- (3.5, 6, 3) -- cycle;
    
    % Dashed line to distant target
    \draw[dashed, gray] (0, 0, 0) -- (3.25, 6, 3.25);
    \node[font=\tiny] at (1.5, 3, 1.5) {$R \gg b$};
    
    % Target
    \node[circle, fill=CGold, inner sep=1.5pt] at (3.25, 6, 3.25) {};
    \node[right, font=\tiny] at (3.25, 6, 3.25) {Target};
    
\end{tikzpicture}
"""

# --- Option F.3: Split View (Top & Side) ---
# Concept: Two panels. Top panel = Azimuth (Pan). Bottom panel = Elevation (Tilt).
# This is physically accurate and very schematic.
optF3 = r"""
\begin{tikzpicture}
    % --- TOP VIEW (Azimuth) ---
    \begin{scope}[yshift=2cm]
        \node[font=\bfseries\scriptsize, anchor=south west] at (-3, 2.5) {TOP VIEW (Azimuth)};
        \coordinate (TC1) at (-0.3, 0);
        \coordinate (TC2) at (0.3, 0);
        
        \fill[CDark] (TC1) circle (0.1);
        \fill[CDark] (TC2) circle (0.1);
        \draw[<->] (-0.3, -0.2) -- (0.3, -0.2) node[midway, below, font=\tiny] {$b \approx 0$};
        
        % Beams
        \fill[CBlue, opacity=0.15] (TC1) -- (-1.5, 2.5) -- (0.5, 2.5) -- cycle; % Wide
        \fill[Garnet, opacity=0.4] (TC2) -- (1.8, 2.5) -- (2.2, 2.5) -- cycle; % Zoom
        
        % Angles
        \draw[->, Garnet] (TC2)++(0, 0.5) arc (90:75:0.5) node[midway, right, font=\tiny] {$\psi$};
        
        \node[right, font=\tiny, CBlue] at (-1.5, 1) {Wide FoV};
        \node[left, font=\tiny, Garnet] at (2.2, 1) {Zoom FoV};
    \end{scope}

    % --- SIDE VIEW (Elevation) ---
    \begin{scope}[yshift=-1cm]
        \node[font=\bfseries\scriptsize, anchor=south west] at (-3, 2.5) {SIDE VIEW (Elevation)};
        % Ground
        \draw[thick, gray] (-3, 0) -- (3, 0);
        \fill[CDark] (-0.2, 0) rectangle (0.2, 0.4); % Tripod head
        \coordinate (SC) at (0, 0.4);
        
        % Wide Vertical FoV
        \fill[CBlue, opacity=0.15] (SC) -- (-1, 2.5) -- (1, 2.5) -- cycle;
        
        % Zoom Vertical FoV (Tilted Up)
        \fill[Garnet, opacity=0.4] (SC) -- (1.8, 2.2) -- (2.2, 1.8) -- cycle;
        
        % Tilt Angle
        \draw[dashed] (SC) -- (0, 1.5); % Zenith/Normal
        \draw[->, Garnet] (0, 1.0) arc (90:45:0.6) node[midway, above, font=\tiny] {$\theta$};
        
        % Distant Object Representation
        \draw[dotted, thick] (2.2, 2.0) -- (3.5, 3.3);
        \node[font=\tiny] at (2.8, 2.8) {To Object};
    \end{scope}
\end{tikzpicture}
"""

# --- Option F.4: The "Sniper Scope" Style ---
# Concept: Focuses on the "Zoom" aspect visually using nested circles/magnification metaphor.
# Shows the layout + "What the camera sees". This might meet the "variable zoom" request best.
optF4 = r"""
\begin{tikzpicture}
    % Layout (Left Side)
    \node (Layout) at (-2, 0) {
        \begin{tikzpicture}[scale=0.5]
            \fill[CDark] (-0.5, 0) circle (0.2);
            \fill[CDark] (0.5, 0) circle (0.2);
            \node[below, font=\tiny] at (-0.5, -0.2) {Fixed};
            \node[below, font=\tiny] at (0.5, -0.2) {PTZ};
            \draw[<->] (-0.5, 0.5) -- (0.5, 0.5) node[midway, above, font=\tiny] {Small $b$};
            
            % Pan/Tilt Arrows
            \draw[->, Garnet, thick] (0.8, 0.2) arc (0:90:0.4);
            \draw[->, Garnet, thick] (0.8, -0.2) arc (0:-90:0.4);
            \node[right, font=\tiny, align=left] at (1.2, 0) {Pan/\\Tilt};
        \end{tikzpicture}
    };
    
    % Beams to Target
    \coordinate (Center) at (0,0);
    \coordinate (Target) at (4, 0);
    
    % Wide Beam
    \fill[CBlue, opacity=0.1] (Layout.east) -- (Target) -- ($(Target)+(0,2)$) -- cycle;
    \fill[CBlue, opacity=0.1] (Layout.east) -- (Target) -- ($(Target)+(0,-2)$) -- cycle;
    
    % Zoom Beam (Variable)
    \fill[Garnet, opacity=0.3] (Layout.east) -- ($(Target)+(0,0.5)$) -- ($(Target)+(0,-0.5)$) -- cycle;
    
    % Variable Zoom Icon
    \draw[<->, >=stealth, white, thick] (2, 0.2) -- (2, -0.2) node[midway, right, font=\tiny, text=black] {Var Zoom};

    % Target "Far"
    \node[circle, fill=CGold, inner sep=2pt] at (Target) {};
    \node[right] at (Target) {Target};
    
    \node[font=\small, fill=white] at (1, -1.5) {$Distance \gg Baseline$};
    
\end{tikzpicture}
"""

# Map options to files
options = {
    "fig_hardware_setup_optF1.tex": optF1,
    "fig_hardware_setup_optF2.tex": optF2,
    "fig_hardware_setup_optF3.tex": optF3,
    "fig_hardware_setup_optF4.tex": optF4,
}

base_path = "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures/"

for filename, content in options.items():
    write_tex(os.path.join(base_path, filename), content)
