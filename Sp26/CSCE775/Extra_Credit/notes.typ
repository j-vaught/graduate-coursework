// ======================================================================
// DeepXube — Paper & Software Summary Notes
// CSCE 775 Extra Credit
// ======================================================================

#set document(
  title: "DeepXube: Paper & Software Summary",
  author: "J.C. Vaught",
  date: datetime(year: 2026, month: 3, day: 30),
)

// ── Page & text ──────────────────────────────────────────────────────
#set page(paper: "us-letter", margin: 0.75in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(justify: true, first-line-indent: 0pt, spacing: 1.2em, leading: 0.65em)

// Headings
#set heading(numbering: "1.1")
#show heading.where(level: 1): it => {
  v(0.5em)
  text(size: 14pt, weight: "bold", it)
  v(0.4em)
}
#show heading.where(level: 2): it => {
  v(0.6em)
  text(size: 12pt, weight: "bold", it)
  v(0.3em)
}
#show heading.where(level: 3): it => {
  v(0.4em)
  text(size: 11pt, weight: "bold", it)
  v(0.2em)
}

// Brand colors
#let garnet = rgb("#73000A")
#let atlantic = rgb("#466A9F")
#let congaree = rgb("#1F414D")

// Links styled
#show link: set text(fill: atlantic)

// ── Title block ─────────────────────────────────────────────────────
#align(center)[
  #text(size: 18pt, weight: "bold", fill: garnet)[DeepXube: Paper & Software Summary]
  #v(0.3em)
  #text(size: 12pt)[CSCE 775 — Extra Credit Notes]
  #v(0.2em)
  #text(size: 11pt)[J.C. Vaught #h(1em) March 30, 2026]
]

#v(1em)

= Paper Summary

The paper, _The DeepXube Software Package for Solving Pathfinding Problems with Learned Heuristic Functions and Search_, is authored by Forest Agostinelli. It introduces a comprehensive software framework that combines deep neural networks with classical search algorithms to solve combinatorial pathfinding problems.

== Main Contributions

DeepXube bridges the gap between deep learning and classical heuristic search. The primary contributions are threefold. First, the system integrates learned heuristics with search by training deep neural networks as admissible heuristic functions and coupling them with classical pathfinding algorithms such as A\* search. Second, it provides a practical, reusable software framework for solving complex combinatorial problems including Rubik's cube solving and related puzzles. Third, the hybrid optimization approach demonstrates that neural network-based heuristics can effectively guide systematic search, outperforming both traditional uninformed search and hand-crafted heuristics alone.

== Methodology

The approach combines several key technical components. Deep neural networks are trained using supervised learning on optimal solution data to learn distance-to-goal heuristics that are admissible, meaning they never overestimate the true distance to the goal state. These learned heuristics are then integrated into classical search algorithms such as A\* search, which uses the heuristic estimates to prioritize which states to explore next.

Problems are systematically encoded into representations suitable for neural network processing, enabling generalization across problem instances. The software package is designed with a scalable architecture that supports multiple domains and problem types, providing tools for problem instantiation, heuristic network training, and search execution.

== Key Results

The system successfully solves highly complex combinatorial problems with significantly reduced computational overhead compared to traditional uninformed search methods. Learned heuristics demonstrate strong generalization across various problem instances, and the hybrid approach enables faster solution discovery than conventional hand-crafted heuristic methods alone. The package proves practical for real-world combinatorial optimization tasks.

== Conclusions

DeepXube demonstrates that combining neural network-based heuristics with classical search algorithms creates an effective hybrid framework for combinatorial optimization. The learned heuristics substantially improve the efficiency of pathfinding algorithms, validating the viability of integrating deep learning with systematic search methods.

= Software Package

The DeepXube software package is available at #link("https://github.com/forestagostinelli/deepxube").

== Overview

DeepXube is a Python framework that combines deep reinforcement learning with heuristic search algorithms to solve combinatorial pathfinding problems. The core innovation is learning problem-specific heuristics through neural networks that guide search algorithms to find optimal solutions more efficiently than uninformed search methods.

== Key Features

The framework offers a domain-independent architecture where users can define custom problem domains and the framework automatically generates appropriate neural network inputs and training procedures. It supports multiple search algorithms including batch weighted A\*, Q\* search with deep Q-networks, and beam search. Users can specify custom neural network architectures for heuristic functions, with built-in support for residual networks. The package also includes visualization tools for interactive exploration of problem instances and solution paths.

== Installation and Usage

Installation is handled through pip.

```bash
pip install deepxube
```

The command-line interface provides several entry points for working with the framework.

```bash
# Explore available domains
deepxube domain_info

# Visualize a problem instance
deepxube viz --domain grid.7 --steps 10

# Train a heuristic network
deepxube train --domain grid.7 --heur resnet_fc.100H_2B_bn

# Solve problem instances
deepxube solve --domain grid.7 --heur_type V
```

== Applications

DeepXube addresses the challenge of efficiently solving combinatorial search problems such as path planning, puzzle solving, and graph traversal by learning domain-specific heuristics through deep learning. This significantly reduces the number of states that search algorithms must explore compared to uninformed search methods, leading to faster solution times for complex problems. It is particularly valuable for NP-hard problems where traditional heuristics may be limited.
