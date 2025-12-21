import os

# Common header for all files
header = r"""\documentclass[tikz,border=5mm]{standalone}
\usepackage{tikz}
\usetikzlibrary{arrows.meta, positioning, shapes.geometric, calc, backgrounds, fit, matrix, patterns, decorations.pathmorphing, shadows}

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
\definecolor{CBlack}{HTML}{000000}

\begin{document}
"""

footer = r"""
\end{document}
"""

def write_tex(filename, content):
    with open(filename, 'w') as f:
        f.write(header + content + footer)
    print(f"Generated {filename}")

# --- Option A: Minimalist Side-by-Side (Flat) ---
optA = r"""
\begin{tikzpicture}
    % Tripod/Mount Base
    \draw[line width=2pt, CDark] (-3, -2) -- (0, 0) -- (3, -2);
    \draw[line width=2pt, CDark] (0, 0) -- (0, -2);
    \fill[CGrayDark] (-2, 0) rectangle (2, 0.2); % Horizontal Bar

    % Camera 1 (Fixed) - Left
    \begin{scope}[shift={(-1, 0.2)}]
        \fill[CWhite] (-0.6, 0) rectangle (0.6, 0.8);
        \fill[CWhite] (0, 0.8) circle (0.5);
        \fill[CDark] (0.2, 0.9) circle (0.15); % Lens
        \node[below, CDark, font=\sffamily\bfseries] at (0, -0.2) {Fixed};
        \node[above, CDark, font=\tiny] at (0, 1.3) {FLIR (Ref)};
    \end{scope}

    % Camera 2 (Slew) - Right
    \begin{scope}[shift={(1, 0.2)}]
        \fill[CWhite] (-0.6, 0) rectangle (0.6, 0.8);
        \fill[CWhite] (0, 0.8) circle (0.5);
        \fill[CDark] (0, 0.8) circle (0.2); % Lens facing front
        \node[below, Garnet, font=\sffamily\bfseries] at (0, -0.2) {Slewable};
    \end{scope}
    
    % Annotations
    \draw[<->, >=stealth, CBlue] (-1, 1.6) -- (1, 1.6) node[midway, fill=white, inner sep=1pt] {Baseline};
\end{tikzpicture}
"""

# --- Option B: Isometric View ---
optB = r"""
\begin{tikzpicture}[x={(0.866cm,0.5cm)}, y={(-0.866cm,0.5cm)}, z={(0cm,1cm)}]
    % Platform
    \fill[CGrayDark] (-2, -1, 0) -- (2, -1, 0) -- (2, 1, 0) -- (-2, 1, 0) -- cycle;
    \draw[thick, CDark] (-2, -1, 0) -- (2, -1, 0) -- (2, 1, 0) -- (-2, 1, 0) -- cycle;

    % Camera 1 (Fixed)
    \begin{scope}[shift={(-1, 0, 0)}]
        \fill[CWhite] (-0.4, -0.4, 0) -- (0.4, -0.4, 0) -- (0.4, 0.4, 0) -- (-0.4, 0.4, 0) -- cycle;
        % Simple box rep
        \fill[CWhite, draw=CDark] (-0.4, -0.4, 0) -- (0.4, -0.4, 0) -- (0.4, -0.4, 1) -- (-0.4, -0.4, 1) -- cycle;
        \fill[CWhite, draw=CDark] (0.4, -0.4, 0) -- (0.4, 0.4, 0) -- (0.4, 0.4, 1) -- (0.4, -0.4, 1) -- cycle;
        \fill[CWhite, draw=CDark] (-0.4, -0.4, 1) -- (0.4, -0.4, 1) -- (0.4, 0.4, 1) -- (-0.4, 0.4, 1) -- cycle;
        % Dome
        \shade[ball color=CWhite] (0,0,1) circle (0.4);
        \fill[black] (0.2, -0.1, 1.1) circle (0.1);
    \end{scope}

    % Camera 2 (Slew)
    \begin{scope}[shift={(1, 0, 0)}]
        \fill[CWhite, draw=CDark] (-0.4, -0.4, 0) -- (0.4, -0.4, 0) -- (0.4, -0.4, 1) -- (-0.4, -0.4, 1) -- cycle;
        \fill[CWhite, draw=CDark] (0.4, -0.4, 0) -- (0.4, 0.4, 0) -- (0.4, 0.4, 1) -- (0.4, -0.4, 1) -- cycle;
        \fill[CWhite, draw=CDark] (-0.4, -0.4, 1) -- (0.4, -0.4, 1) -- (0.4, 0.4, 1) -- (-0.4, 0.4, 1) -- cycle;
        % Dome - Rotated
        \shade[ball color=CWhite] (0,0,1) circle (0.4);
        \fill[Garnet] (0.3, 0.2, 1.15) circle (0.12);
        
        \draw[->, Garnet, thick] (0,0,1.5) arc (0:90:0.3);
    \end{scope}
    
\end{tikzpicture}
"""

# --- Option C: Technical Front View (Schematic) ---
optC = r"""
\begin{tikzpicture}
    \matrix[column sep=1cm] {
        \node (cam1) {
            \begin{tikzpicture}
                \draw[thick, fill=CWhite] (-0.5,0) rectangle (0.5, 0.8);
                \draw[thick, fill=CWhite] (0, 0.8) circle (0.5);
                \draw[fill=black] (0, 0.8) circle (0.2);
                \node at (0, -0.5) {\textbf{Cam 1 (Fixed)}};
                \draw[<->] (-0.6, 0) -- (-0.6, 1.3) node[midway, left] {H};
            \end{tikzpicture}
        }; &
        \node (cam2) {
            \begin{tikzpicture}
                \draw[thick, fill=CWhite] (-0.5,0) rectangle (0.5, 0.8);
                \draw[thick, fill=CWhite] (0, 0.8) circle (0.5);
                \draw[fill=Garnet] (0.2, 0.9) circle (0.2);
                \draw[->, thick, Garnet] (0.6, 1.0) arc (30:-30:0.5);
                \node at (0, -0.5) {\textbf{Cam 2 (PTZ)}};
            \end{tikzpicture}
        }; \\
    };
    \draw[thick] (cam1.south west) ++(-0.2, 0.2) -- (cam2.south east) ++(0.2, 0.2) node[right] {Mounting Rail};
\end{tikzpicture}
"""

# --- Option D: Realistic FLIR M232 Style ---
optD = r"""
\begin{tikzpicture}
    \def\flircam{
        % Base
        \fill[CWhite!90!gray] (-0.7, 0) rectangle (0.7, 1.0);
        \draw[gray!30] (-0.7, 0.2) -- (0.7, 0.2);
        \node[font=\tiny\sffamily, text=CDark] at (0, 0.5) {FLIR};
        
        % Rotating Head (Dome)
        \shadedraw[ball color=CWhite] (0, 1.0) circle (0.75);
        \fill[black] (0.4, 1.1) ellipse (0.2 and 0.25); % Lens
        \fill[white, opacity=0.3] (0.45, 1.2) circle (0.05); % Glint
    }

    % Tripod Top Plate
    \fill[CGrayDark] (-3, -0.2) rectangle (3, 0);
    
    % Cam 1
    \begin{scope}[shift={(-1.5, 0)}]
        \flircam
        \node[below=0.3cm] {Fixed RGB};
    \end{scope}

    % Cam 2
    \begin{scope}[shift={(1.5, 0)}]
        % Base
        \fill[CWhite!90!gray] (-0.7, 0) rectangle (0.7, 1.0);
        \draw[gray!30] (-0.7, 0.2) -- (0.7, 0.2);
        \node[font=\tiny\sffamily, text=CDark] at (0, 0.5) {FLIR};
        
        % Rotating Head (Dome) - Tilted
        \begin{scope}[rotate around={20:(0, 1.0)}]
            \shadedraw[ball color=CWhite] (0, 1.0) circle (0.75);
            \fill[black] (0.6, 1.0) ellipse (0.15 and 0.25); % Lens side view
        \end{scope}
        
        % Motion arrows
        \draw[->, thick, Garnet] (0, 1.9) arc (90:0:0.8);
        
        \node[below=0.3cm] {Slewable RGB};
    \end{scope}

\end{tikzpicture}
"""

# --- Option E: Iconic / Functional ---
optE = r"""
\begin{tikzpicture}
    % Icons
    \node[circle, fill=CBlue, text=white, minimum size=1.5cm] (C1) at (0,0) {\LARGE \faVideoCamera}; % Placeholder text if fontawesome not avail, used standard shapes below
    
    % Custom icon logic since fa not standard in minimal install sometimes
    \def\camicon{
        \draw[fill=white, thick] (-0.3, -0.2) rectangle (0.3, 0.2);
        \draw[fill=white, thick] (0.3, 0) -- (0.6, 0.2) -- (0.6, -0.2) -- (0.3, 0) -- cycle;
    }

    \node[draw=CBlue, circle, minimum size=2cm, line width=2pt] (N1) at (-2,0) {};
    \node at (-2,0) {\textcolor{CBlue}{\textbf{Fixed}}};
    
    \node[draw=Garnet, circle, minimum size=2cm, line width=2pt] (N2) at (2,0) {};
    \node at (2,0) {\textcolor{Garnet}{\textbf{PTZ}}};
    
    % Representations
    \begin{scope}[shift={(-2, 0.5)}]
        \camicon
    \end{scope}
    \begin{scope}[shift={(2, 0.5)}]
        \camicon
        \draw[->, Garnet, thick] (0, 0.4) arc (90:0:0.4);
    \end{scope}
    
    % Data Flow
    \draw[->, dashed] (N1) -- (0, -2) node[midway, left] {Wide Stream};
    \draw[->, dashed] (N2) -- (0, -2) node[midway, right] {Zoom Stream};
    
    \node[draw, fill=CGrayLight] at (0, -2.5) {System Logic};
\end{tikzpicture}
"""

# --- Option F: Top-Down FoV Coverage ---
optF = r"""
\begin{tikzpicture}
    % Cameras
    \fill[CDark] (-1.5, 0) circle (0.3);
    \fill[CDark] (1.5, 0) circle (0.3);
    
    % FoV 1 (Fixed)
    \fill[CBlue, opacity=0.3] (-1.5, 0) -- (-0.5, 3) -- (-2.5, 3) -- cycle;
    \node[CBlue] at (-1.5, 3.2) {Fixed FoV};
    
    % FoV 2 (Slewable)
    \fill[Garnet, opacity=0.3] (1.5, 0) -- (2.0, 3) -- (1.0, 3) -- cycle;
    \draw[->, Garnet, thick] (1.5, 1.5) arc (90:45:1.5);
    \draw[->, Garnet, thick] (1.5, 1.5) arc (90:135:1.5);
    \node[Garnet] at (1.5, 3.2) {Slewable Region};
    
    % Labels
    \node[below] at (-1.5, -0.3) {Cam 1};
    \node[below] at (1.5, -0.3) {Cam 2};
\end{tikzpicture}
"""

# --- Option G: Abstract "Twin" ---
optG = r"""
\begin{tikzpicture}
    % Stylized Twin Cams
    \foreach \x/\c/\t in {-1.5/CBlue/Fixed, 1.5/Garnet/Slew} {
        \draw[line width=2pt, \c] (\x, 0) circle (1);
        \fill[\c!20] (\x, 0) circle (1);
        \fill[white] (\x, 0.4) circle (0.3); % Glint/Lens
        \node[below=1.2cm, font=\bfseries\sffamily] at (\x, 0) {\t};
    }
    
    % Connection
    \draw[dotted, thick] (-0.5, 0) -- (0.5, 0);
    \node[above, font=\tiny] at (0, 0) {Sync};
    
    % PTZ arrows on second
    \draw[->, Garnet, thick] (2.7, 0) arc (0:90:0.5);
    \draw[->, Garnet, thick] (0.3, 0) arc (180:90:0.5);
\end{tikzpicture}
"""

# --- Option H: Tripod Context Scale ---
optH = r"""
\begin{tikzpicture}[scale=0.5]
    % Tripod Legs
    \draw[thick, CDark] (0, 5) -- (-3, 0);
    \draw[thick, CDark] (0, 5) -- (3, 0);
    \draw[thick, CDark] (0, 5) -- (0, -1); % Middle leg perspective
    
    % Mount Plate
    \fill[CGrayDark] (-2, 5) rectangle (2, 5.5);
    
    % Cam 1 (Left)
    \fill[CWhite] (-1.5, 5.5) rectangle (-0.5, 6.5);
    \fill[CWhite] (-1, 6.5) circle (0.5);
    
    % Cam 2 (Right)
    \fill[CWhite] (0.5, 5.5) rectangle (1.5, 6.5);
    \fill[CWhite] (1, 6.5) circle (0.5);
    
    % Ground
    \draw[CGrayLight, line width=3pt] (-5, 0) -- (5, 0);
    
    \node[right] at (3, 2.5) {Tripod Setup};
    \draw[<-] (0.2, 5) -- (3, 2.7);
\end{tikzpicture}
"""

# --- Option I: Dynamic/Action ---
optI = r"""
\begin{tikzpicture}
    % Background glow
    \shade[inner color=CBlue!10, outer color=white] (-4,-2) rectangle (4,4);

    % Cam 1 (Static)
    \node[anchor=south] (C1) at (-2, 0) {
        \begin{tikzpicture}
            \fill[CWhite] (-0.5,0) rectangle (0.5, 1);
            \fill[CDark] (-0.5, 1) arc (180:0:0.5) -- cycle;
            \node at (0, -0.3) {Fixed};
        \end{tikzpicture}
    };
    
    % Cam 2 (Moving)
    \node[anchor=south] (C2) at (2, 0) {
        \begin{tikzpicture}
            \fill[CWhite] (-0.5,0) rectangle (0.5, 1);
            \fill[Garnet] (-0.5, 1) arc (180:0:0.5) -- cycle;
            % Motion blur lines
            \draw[Garnet, opacity=0.5, thick] (0.6, 1.2) arc (30:60:0.5);
            \draw[Garnet, opacity=0.3, thick] (0.7, 1.1) arc (30:60:0.6);
            \node at (0, -0.3) {Tracking};
        \end{tikzpicture}
    };
    
    \draw[ultra thick, gray] (-3, 0) -- (3, 0);
\end{tikzpicture}
"""

# --- Option J: Blueprint Style ---
optJ = r"""
\begin{tikzpicture}[background rectangle/.style={fill=CDark}, show background rectangle]
    \draw[help lines, step=0.5, cyan!20, thin] (-3,-1) grid (3,3);
    
    % Cam 1
    \draw[cyan, thick] (-2, 0) rectangle (-1, 1);
    \draw[cyan, thick] (-1.5, 1) circle (0.5);
    \node[cyan, font=\ttfamily] at (-1.5, -0.5) {CAM\_FIXED};
    
    % Cam 2
    \draw[cyan, thick] (1, 0) rectangle (2, 1);
    \draw[cyan, thick] (1.5, 1) circle (0.5);
    \draw[cyan, dashed] (1.5, 1.5) -- (2.5, 2.5); % Axis
    \node[cyan, font=\ttfamily] at (1.5, -0.5) {CAM\_PTZ};
    
    \draw[cyan, thick] (-2.5, 0) -- (2.5, 0);
\end{tikzpicture}
"""

# Map options to files
options = {
    "fig_hardware_setup_optA.tex": optA,
    "fig_hardware_setup_optB.tex": optB,
    "fig_hardware_setup_optC.tex": optC,
    "fig_hardware_setup_optD.tex": optD,
    "fig_hardware_setup_optE.tex": optE,
    "fig_hardware_setup_optF.tex": optF,
    "fig_hardware_setup_optG.tex": optG,
    "fig_hardware_setup_optH.tex": optH,
    "fig_hardware_setup_optI.tex": optI,
    "fig_hardware_setup_optJ.tex": optJ,
}

base_path = "/Users/jvaught/Downloads/COde/graduate-coursework/Fall 2025/Conf_Papers/AIAA Papers/Jackie_cue_to_slew/figures/"

for filename, content in options.items():
    write_tex(os.path.join(base_path, filename), content)
