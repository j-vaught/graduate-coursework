#!/usr/bin/env python3
"""
Assemble the complete LLM Context Management Literature Review
Author: J.C. Vaught
"""

import os

BASE_DIR = "/Volumes/MacShare/LLM_context"
OUTPUT_FILE = os.path.join(BASE_DIR, "LLM_Context_Management_Literature_Review.tex")

# Preamble
PREAMBLE = r"""% ============================================================
% Context Management in Large Language Models:
% A Survey of Human-Inspired Memory Architectures
% ============================================================
% Author: J.C. Vaught
% Date: January 2026
% ============================================================

\documentclass[11pt,letterpaper]{article}

% --- Core Packages ---
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage[margin=1in]{geometry}
\usepackage{setspace}
\usepackage{parskip}
\usepackage{xcolor}
\usepackage{titlesec}
\usepackage{hyperref}
\usepackage[numbers,sort&compress]{natbib}
\usepackage{graphicx}
\usepackage{amsmath,amssymb}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{array}
\usepackage{tabularx}
\usepackage{fancyhdr}
\usepackage{caption}
\usepackage{float}

% --- Brand Colors ---
\definecolor{garnet}{RGB}{115,0,10}
\definecolor{atlantic}{RGB}{70,106,159}
\definecolor{congaree}{RGB}{31,65,77}
\definecolor{black90}{RGB}{54,54,54}
\definecolor{black70}{RGB}{92,92,92}
\definecolor{black50}{RGB}{162,162,162}
\definecolor{rose}{RGB}{204,46,64}

% --- Section Formatting ---
\titleformat{\section}
  {\Large\bfseries\color{garnet}}
  {\thesection}{1em}{}
\titleformat{\subsection}
  {\large\bfseries\color{congaree}}
  {\thesubsection}{1em}{}
\titleformat{\subsubsection}
  {\normalsize\bfseries\color{black90}}
  {\thesubsubsection}{1em}{}
\titleformat{\paragraph}[runin]
  {\normalsize\bfseries\color{black70}}
  {}{0em}{}[.]

% --- Hyperlink Colors ---
\hypersetup{
    colorlinks=true,
    linkcolor=garnet,
    citecolor=atlantic,
    urlcolor=atlantic
}

% --- Header/Footer ---
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small\color{black70}Context Management in Large Language Models}
\fancyhead[R]{\small\color{black70}J.C. Vaught}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}

% --- Spacing ---
\onehalfspacing

\begin{document}

% === Title Page ===
\begin{titlepage}
\centering
\vspace*{2cm}
{\Huge\bfseries\color{garnet} Context Management in\\Large Language Models\par}
\vspace{0.75cm}
{\LARGE\color{congaree} A Survey of Human-Inspired\\Memory Architectures\par}
\vspace{2cm}
{\Large J.C. Vaught\par}
\vspace{0.5cm}
{\large January 2026\par}
\vspace{3cm}
{\large\color{black70}
A comprehensive literature review examining context window limitations, memory architectures, and human-inspired approaches to persistent memory in large language models. This survey spans attention mechanisms, positional encoding strategies, key-value cache optimization, context compression, retrieval-augmented generation, hierarchical memory systems grounded in cognitive science, hallucination phenomena arising from context mismanagement, multi-turn dialogue coherence, and evaluation methodologies for long-context capabilities.\par}
\end{titlepage}

% === Abstract ===
\begin{abstract}
\noindent
Large language models have demonstrated remarkable capabilities across diverse natural language processing tasks, yet they remain fundamentally constrained by finite context windows that limit the amount of information available during inference. This survey provides a comprehensive examination of context management strategies, organized around ten interconnected themes. We begin with the foundational attention mechanism and its quadratic computational complexity, then trace the evolution of positional encoding methods from absolute embeddings through rotary position encodings and their scaling variants that have progressively extended effective context lengths from thousands to millions of tokens. We analyze sparse and efficient attention architectures, including Longformer, BigBird, and state-space models such as Mamba, that achieve sub-quadratic complexity while preserving modeling quality. The survey examines key-value cache optimization techniques encompassing eviction policies, quantization schemes, and dynamic memory management systems such as PagedAttention and vAttention. Context compression methods, including prompt compression frameworks like LLMLingua and learned compression via gist tokens and in-context autoencoders, are analyzed for their trade-offs between information preservation and computational efficiency. We provide an extensive treatment of memory-augmented architectures spanning classical neural memory networks, retrieval-augmented generation and its modern variants including Self-RAG, CRAG, and GraphRAG, and operating-system-inspired designs such as MemGPT. The core of this survey is dedicated to hierarchical, human-inspired memory architectures, where we draw systematic parallels between cognitive science constructs including the Atkinson-Shiffrin model, Baddeley's working memory, Tulving's memory taxonomy, Ebbinghaus's forgetting curve, and McClelland's complementary learning systems, and their computational analogues in systems such as Generative Agents, MemoryBank, the Cognitive Architectures for Language Agents framework, the Self-Controlled Memory framework, and the Hierarchical Memory Transformer. We examine how hallucination phenomena arise from context management failures, including the lost-in-the-middle effect and positional biases. Multi-turn dialogue presents unique challenges for memory persistence, and we survey approaches from conversation summarization to episodic memory buffers. Finally, we critically assess evaluation methodologies including Needle-in-a-Haystack, RULER, LongBench, InfiniteBench, HELMET, and domain-specific benchmarks, identifying gaps between benchmark performance and real-world long-context utilization. Throughout, we argue that human cognitive memory architectures provide essential design principles for building language model systems capable of coherent, persistent, and scalable context management.
\end{abstract}

\newpage

"""

INTRODUCTION = r"""\section{Introduction}
\label{sec:introduction}

The transformer architecture has fundamentally transformed natural language processing, establishing itself as the dominant paradigm for sequence modeling and the foundation for virtually all modern large language models. Central to its success is the self-attention mechanism, which enables direct pairwise interactions between all positions in a sequence without the sequential bottlenecks inherent in recurrent architectures. This architectural innovation has enabled the remarkable scaling of language models from millions to hundreds of billions of parameters, yielding systems capable of impressive feats of text generation, question answering, reasoning, and code synthesis.

However, the very mechanism that grants transformers their expressive power introduces a fundamental computational constraint: quadratic scaling with respect to sequence length. Processing a context of length $n$ requires $O(n^2)$ attention computations, meaning that doubling the context window quadruples the computational cost. For the million-token contexts now emerging in frontier models, this quadratic dependency poses severe challenges for both training and inference, motivating extensive research into techniques that extend effective context while managing computational demands.

The challenge of context management extends beyond raw computational complexity to encompass questions of effective utilization, information retention, and coherent integration of information distributed across extended sequences. Empirical research has revealed that models often fail to effectively utilize information positioned in the middle of long contexts, exhibiting a U-shaped performance curve where information at the beginning and end of sequences is more accessible than middle-positioned content. Furthermore, attention patterns in trained models exhibit systematic biases including primacy effects favoring early tokens, recency effects privileging recent tokens, and attention sink phenomena where initial tokens receive disproportionate attention regardless of semantic relevance.

These phenomena suggest that extending context windows requires more than architectural modifications to reduce computational complexity. Effective long-context processing demands sophisticated memory management strategies that selectively retain important information, compress or summarize less critical content, and maintain coherent representations across extended interactions. This recognition has motivated research drawing inspiration from human cognitive architectures, which successfully manage effectively unbounded information streams through multi-store memory systems, hierarchical organization, selective consolidation, and intelligent forgetting.

This survey provides a comprehensive examination of context management in large language models, organized around ten interconnected themes. Following this introduction, Section 2 examines transformer attention mechanisms and positional encoding schemes that determine sequence length capabilities. Section 3 surveys context window extension techniques including RoPE-based scaling methods and continual pre-training strategies. Section 4 analyzes sparse and efficient attention mechanisms that achieve sub-quadratic complexity. Section 5 investigates key-value cache optimization through eviction policies, quantization, and architectural modifications. Section 6 examines context compression techniques from hard prompt pruning to learned soft compression. Section 7 provides extensive treatment of memory-augmented and retrieval-augmented generation architectures. Section 8 constitutes the theoretical core, examining hierarchical human-inspired memory systems and their computational implementations. Section 9 analyzes hallucination phenomena arising from context management failures. Section 10 addresses multi-turn conversation management. Section 11 critically assesses evaluation methodologies for long-context capabilities. We conclude in Section 12 with synthesis and future directions.

"""

with open(OUTPUT_FILE, 'w') as f:
    # Write preamble and introduction
    f.write(PREAMBLE)
    f.write(INTRODUCTION)

    # Write all 10 section files
    for i in range(1, 11):
        section_file = os.path.join(BASE_DIR, "sections", f"section_{i:02d}.tex")
        print(f"Adding {section_file}...")
        with open(section_file, 'r') as sf:
            f.write(sf.read())
            f.write("\n\n")

    # Write discussion and conclusion
    with open(os.path.join(BASE_DIR, "discussion_conclusion.txt"), 'r') as dc:
        f.write(dc.read())

    # Write bibliography
    f.write("\n\\bibliographystyle{IEEEtran}\n")
    f.write("\\bibliography{references_complete}\n\n")
    f.write("\\end{document}\n")

print(f"Document assembled: {OUTPUT_FILE}")
