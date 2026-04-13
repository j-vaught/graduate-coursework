// main.typ — Comprehensive Review: LLM-Guided Evolutionary Discovery of RL Algorithms

#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.65em, justify: true)
#set heading(numbering: "1.")

// Title page and table of contents
#include "sections/00_title.typ"

// Section 1
#include "sections/01_evolutionary_computation.typ"

// Section 2
#include "sections/02_neuroevolution.typ"

// Section 3
#include "sections/03_deep_rl.typ"

// Section 4
#include "sections/04_policy_optimization.typ"

// Section 5
#include "sections/05_rl_alignment.typ"

// Section 6
#include "sections/06_meta_learning.typ"

// Section 7
#include "sections/07_llm_code.typ"

// Section 8
#include "sections/08_funsearch_alphaevolve.typ"

// Section 9
#include "sections/09_gecco_paper.typ"

// Section 10
#include "sections/10_critical_analysis.typ"

// References
#pagebreak()
#bibliography("references.bib", style: "ieee", title: "References")
