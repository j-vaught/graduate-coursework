// Section 00: Title Page and Table of Contents

#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.65em, justify: true)

// --- Title Page ---

#v(2fr)

#align(center)[
  #text(size: 18pt, weight: "bold")[
    From Genetic Algorithms to LLM-Guided Evolutionary Discovery of Reinforcement Learning Algorithms: A Comprehensive Review
  ]

  #v(1.5em)

  #text(size: 13pt)[J.C. Vaught]

  #v(0.75em)

  #text(size: 11pt)[
    CSCE 775: Deep Reinforcement Learning and Search \
    April 2026
  ]
]

#v(2fr)

// --- Abstract ---

#align(center)[
  #text(size: 13pt, weight: "bold")[Abstract]
]

#v(0.5em)

This review traces the intellectual trajectory from classical evolutionary computation to the emerging paradigm of using large language models as evolutionary operators for the automated discovery of reinforcement learning algorithms. We begin with the foundational principles of genetic algorithms, genetic programming, and evolution strategies, then examine their intersection with neural networks through neuroevolution. The exposition proceeds through the deep reinforcement learning revolution, covering value-based and policy gradient methods, trust-region optimization, and the role of RL in large language model alignment via RLHF and GRPO. We survey meta-learning and automated RL as precursors to algorithm discovery, before turning to LLM-based program synthesis. The core of the review examines LLM-guided evolutionary search frameworks, including FunSearch and AlphaEvolve, which leverage LLMs to generate and refine code within evolutionary loops. We culminate with a detailed analysis of recent work on evolving RL loss functions, particularly the REvolve framework and the Sygkounas et al. GECCO 2026 study, which demonstrates that LLM-guided evolution can produce novel, competitive RL algorithms. We conclude with a critical assessment of open problems and future directions.

#pagebreak()

// --- Table of Contents ---

#align(center)[
  #text(size: 14pt, weight: "bold")[Table of Contents]
]

#v(1.5em)

#set enum(numbering: "1.")

#text(size: 11pt)[
  + Evolutionary Computation: Foundations

  + Neuroevolution and Evolution Strategies for RL

  + Deep Reinforcement Learning: The Revolution

  + Policy Optimization: TRPO, PPO, and Beyond

  + RL for Large Language Model Alignment

  + Meta-Learning and Automated RL

  + LLMs as Program Synthesizers

  + LLM-Guided Evolutionary Search

  + Evolving RL Algorithms: The GECCO 2026 Paper

  + Critical Analysis and Open Problems

  + References
]

#pagebreak()
