#!/bin/bash
# Script to assemble the complete literature review

OUTFILE="/Volumes/MacShare/LLM_context/LLM_Context_Management_Literature_Review.tex"
TEMPFILE="/Volumes/MacShare/LLM_context/temp_assembly.tex"

# Start with preamble
cat > "$TEMPFILE" << 'EOF'
% ============================================================
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
  {\thesubsection}{1em}{}
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

\section{Introduction}
\label{sec:introduction}

The transformer architecture has fundamentally transformed natural language processing, establishing itself as the dominant paradigm for sequence modeling and the foundation for virtually all modern large language models. Central to its success is the self-attention mechanism, which enables direct pairwise interactions between all positions in a sequence without the sequential bottlenecks inherent in recurrent architectures. This architectural innovation has enabled the remarkable scaling of language models from millions to hundreds of billions of parameters, yielding systems capable of impressive feats of text generation, question answering, reasoning, and code synthesis.

However, the very mechanism that grants transformers their expressive power introduces a fundamental computational constraint: quadratic scaling with respect to sequence length. Processing a context of length $n$ requires $O(n^2)$ attention computations, meaning that doubling the context window quadruples the computational cost. For the million-token contexts now emerging in frontier models, this quadratic dependency poses severe challenges for both training and inference, motivating extensive research into techniques that extend effective context while managing computational demands.

The challenge of context management extends beyond raw computational complexity to encompass questions of effective utilization, information retention, and coherent integration of information distributed across extended sequences. Empirical research has revealed that models often fail to effectively utilize information positioned in the middle of long contexts, exhibiting a U-shaped performance curve where information at the beginning and end of sequences is more accessible than middle-positioned content. Furthermore, attention patterns in trained models exhibit systematic biases including primacy effects favoring early tokens, recency effects privileging recent tokens, and attention sink phenomena where initial tokens receive disproportionate attention regardless of semantic relevance.

These phenomena suggest that extending context windows requires more than architectural modifications to reduce computational complexity. Effective long-context processing demands sophisticated memory management strategies that selectively retain important information, compress or summarize less critical content, and maintain coherent representations across extended interactions. This recognition has motivated research drawing inspiration from human cognitive architectures, which successfully manage effectively unbounded information streams through multi-store memory systems, hierarchical organization, selective consolidation, and intelligent forgetting.

This survey provides a comprehensive examination of context management in large language models, organized around ten interconnected themes. Following this introduction, Section 2 examines transformer attention mechanisms and positional encoding schemes that determine sequence length capabilities. Section 3 surveys context window extension techniques including RoPE-based scaling methods and continual pre-training strategies. Section 4 analyzes sparse and efficient attention mechanisms that achieve sub-quadratic complexity. Section 5 investigates key-value cache optimization through eviction policies, quantization, and architectural modifications. Section 6 examines context compression techniques from hard prompt pruning to learned soft compression. Section 7 provides extensive treatment of memory-augmented and retrieval-augmented generation architectures. Section 8 constitutes the theoretical core, examining hierarchical human-inspired memory systems and their computational implementations. Section 9 analyzes hallucination phenomena arising from context management failures. Section 10 addresses multi-turn conversation management. Section 11 critically assesses evaluation methodologies for long-context capabilities. We conclude in Section 12 with synthesis and future directions.

EOF

# Append all section files
for i in {01..10}; do
    echo "% ============================================================" >> "$TEMPFILE"
    echo "% SECTION $i" >> "$TEMPFILE"
    echo "% ============================================================" >> "$TEMPFILE"
    cat "/Volumes/MacShare/LLM_context/sections/section_${i}.tex" >> "$TEMPFILE"
    echo "" >> "$TEMPFILE"
done

# Add Discussion and Conclusion

cat >> "$TEMPFILE" << 'EOFDISCUSSION'

% ============================================================
% DISCUSSION
% ============================================================

\section{Discussion: Synthesis and Future Directions}
\label{sec:discussion}

The preceding sections have surveyed a remarkably diverse ecosystem of techniques for managing context in large language models, spanning architectural innovations, algorithmic optimizations, memory-augmented systems, and human-inspired hierarchical memory architectures. This diversity reflects both the multifaceted nature of the context management challenge and the absence of a single dominant solution. As we synthesize insights across these approaches, several overarching themes emerge that illuminate the current state of the field and suggest productive directions for future research.

The first theme concerns the fundamental tension between context capacity and context utilization. While architectural innovations have extended nominal context windows from thousands to millions of tokens, empirical evaluation consistently reveals that effective utilization lags far behind theoretical capacity. The lost-in-the-middle phenomenon, whereby information positioned in central portions of long contexts becomes substantially less accessible than boundary-positioned content, persists across model scales and architectures. Evaluation on benchmarks such as BABILong demonstrates that models utilize only ten to twenty percent of their available context, effectively ignoring the vast majority of provided information. This gap between capacity and utilization suggests that raw context expansion, while necessary, is insufficient for robust long-context understanding. Future progress requires not merely larger windows but architectural modifications that enable uniform access to information regardless of position, training procedures that explicitly address positional biases, and memory systems that selectively maintain high-fidelity representations of important information while compressing or abstracting less critical content.

The second theme addresses the interplay between efficiency and expressiveness. Quadratic attention complexity creates an exponential barrier to context scaling, motivating extensive research into efficient alternatives including sparse attention patterns, linear attention approximations, state space models, and hardware-aware optimizations. Each approach navigates distinct trade-offs. Sparse attention methods such as Longformer and BigBird achieve linear complexity through structured sparsity while maintaining exact computation on the sparse support, but fixed patterns may miss task-relevant dependencies falling outside predefined structures. Linear approximations including Performer and Linformer reduce complexity through mathematical reformulation but introduce approximation error that compounds across layers. State space models such as S4 and Mamba abandon attention entirely in favor of recurrence-based alternatives, achieving impressive efficiency but requiring different training procedures and exhibiting different inductive biases. FlashAttention demonstrates that exact attention can be dramatically accelerated through memory hierarchy optimization without changing the underlying computation, achieving two to nine times speedup through algorithmic restructuring alone. The coexistence of these diverse approaches suggests that optimal solutions may be context-dependent, with different applications benefiting from different efficiency-expressiveness trade-offs. Hybrid architectures such as Jamba, which interleave transformer layers with Mamba layers and mixture-of-experts, exemplify the emerging recognition that heterogeneous designs selecting components based on computational role may outperform monolithic architectures committed to a single mechanism.

The third theme concerns the integration of parametric and non-parametric memory. Retrieval-augmented generation has emerged as a dominant paradigm for grounding generation in factual knowledge, enabling models to access information beyond their training cutoff and providing explicit source attribution for generated claims. The evolution from foundational RAG through advanced variants such as Self-RAG, CRAG, and GraphRAG demonstrates increasing sophistication in when, what, and how to retrieve, incorporating self-reflection mechanisms that decide whether retrieval is necessary, correction procedures that detect and remediate retrieval failures, and structured knowledge representations that enable multi-hop reasoning across graph-organized information. However, retrieval-augmented systems remain vulnerable to position effects, as retrieved passages positioned in middle contexts suffer from the same accessibility degradation observed in standard long-context processing. Furthermore, the separation between retrieval and generation introduces latency and complexity, motivating research into tighter integration such as RETRO's retrieval during pre-training and Fusion-in-Decoder's late fusion of multiple passages. The convergence of retrieval-augmented approaches with prompt compression techniques such as LLMLingua and context management systems such as MemGPT suggests a future where memory systems fluidly combine parametric knowledge in model weights, working memory in the context window, and long-term memory in external stores, with intelligent mechanisms managing information flow between these tiers.

The fourth theme addresses the productive application of cognitive science to computational memory systems. The hierarchical human-inspired memory architectures demonstrate that principles from experimental psychology and cognitive neuroscience provide valuable design guidance for artificial memory systems. The Atkinson-Shiffrin multi-store model, distinguishing sensory, short-term, and long-term memory with distinct characteristics and capacities, maps naturally onto systems with immediate context windows, working memory for active computation, and external long-term storage. Baddeley's working memory framework, decomposing working memory into phonological loop, visuospatial sketchpad, and central executive components, informs agent architectures with specialized buffers for different information types. Tulving's distinction between episodic memory for specific experiences and semantic memory for general knowledge motivates systems that maintain both event logs and abstracted summaries. Ebbinghaus's forgetting curve and the spacing effect inform decay mechanisms that naturally prioritize recently accessed and frequently retrieved information. McClelland's complementary learning systems theory, positing rapid episodic encoding in hippocampus and slow statistical learning in neocortex, parallels systems that combine fast few-shot in-context learning with slow parameter updates through fine-tuning.

The Generative Agents framework exemplifies these principles through its three-component memory system combining perception, reflection, and planning. MemoryBank advances this architecture through dynamic memory updating, knowledge retrieval, and memory consolidation via summarization. The Cognitive Architectures for Language Agents framework provides a general specification for memory-augmented agents, distinguishing working memory from long-term memory and defining interfaces for selective retention and consolidation. The Self-Controlled Memory framework introduces self-awareness and metacognitive control over memory operations, enabling agents to decide what to remember and when to forget based on task demands. These systems demonstrate that cognitively-inspired architectures can overcome limitations of purely engineering-driven approaches, producing more robust, interpretable, and human-like memory systems.

The fifth theme concerns the persistent challenge of hallucination and its intimate connection to context management. Hallucinations arise from multiple interacting factors including incomplete or biased training data, insufficient capacity to represent all factual knowledge, and context management failures that prevent access to relevant information during generation. The distinction between faithfulness to provided context and factual accuracy with respect to world knowledge proves critical, as interventions targeting one dimension may degrade the other. The lost-in-the-middle effect directly contributes to hallucination through making middle-positioned information inaccessible, causing models to generate content inconsistent with provided evidence. Mitigation strategies including self-consistency, chain-of-verification, and retrieval grounding demonstrate varying degrees of effectiveness, but hallucinations persist at non-negligible rates even in sophisticated systems combining multiple mitigation approaches. Future progress requires not only continued refinement of mitigation techniques but also architectural innovations addressing the root causes, including position-invariant attention mechanisms, improved position encoding schemes, and memory systems with explicit source tracking enabling verification of generated claims.

The sixth theme addresses multi-turn conversational coherence, which presents unique challenges beyond single-document processing. Conversations evolve incrementally over multiple turns and sessions, requiring coherent entity state tracking, coreference resolution, cross-session continuity, and management of progressive context growth that inevitably exceeds available windows. The 39 percent performance degradation observed in multi-turn scenarios compared to single-turn evaluation, persisting across frontier models regardless of context window size, indicates fundamental limitations in how current architectures integrate information across extended conversational sequences. Approaches from conversation summarization through hierarchical memory to dialogue state tracking each address specific aspects of this challenge, but no comprehensive solution has emerged. The convergence of techniques including intelligent truncation, recursive summarization, vectorized memory retrieval, and psychology-informed importance weighting suggests that robust multi-turn systems will require orchestrating multiple complementary mechanisms.

The seventh theme concerns evaluation methodology and the critical gaps between synthetic benchmarks and real-world performance. While benchmarks such as Needle-in-a-Haystack, RULER, LongBench, InfiniteBench, HELMET, BABILong, and SCROLLS provide valuable standardized evaluation, research increasingly reveals that strong performance on synthetic tasks fails to predict success on practical applications. Models achieving near-perfect scores on simple retrieval exhibit large performance drops on tasks requiring multi-hop reasoning, aggregation, or synthesis. The low correlation between different evaluation categories demonstrates that long-context understanding is not a unitary capability but a collection of specialized skills with limited transfer. Furthermore, evaluation predominantly employs single-turn question answering while real applications involve multi-turn interaction, adaptive behavior, and integration of user feedback. The development of more sophisticated metrics such as LongPPL, which focuses on key tokens showing long-short context differences, represents progress toward evaluation that better predicts downstream performance.

Looking forward, several research directions appear particularly promising for advancing the state of long-context language models. First, unified memory architectures integrating parametric knowledge, working memory, and long-term storage with principled mechanisms for information flow, resource allocation, and coherence maintenance across memory tiers could provide more robust and efficient context management than current approaches treating these components independently. Second, architecture-aware training procedures that explicitly address positional biases, teach uniform context access, and develop robust mechanisms for information integration across extended sequences may improve effective utilization toward theoretical capacity. Third, dynamic adaptation mechanisms that adjust compression ratios, retrieval strategies, and attention patterns based on task demands, input characteristics, and available computational resources could enable systems to navigate efficiency-quality trade-offs more intelligently. Fourth, neurosymbolic approaches combining neural pattern recognition with explicit symbolic reasoning and structured knowledge representation may address fundamental limitations in multi-hop reasoning and causal inference that persist despite scaling. Fifth, hardware-software co-design optimizing memory hierarchies, communication patterns, and computational kernels specifically for long-context workloads could unlock substantial efficiency gains beyond what general-purpose hardware permits.

The rapid pace of innovation in context management throughout 2023 through 2026, with weekly advances in compression techniques, memory architectures, attention mechanisms, and evaluation methodologies, reflects both the critical importance of this research area and the substantial remaining challenges. Context windows have expanded from thousands to millions of tokens, enabling applications from book-length document analysis to multi-session conversations spanning months. Yet effective utilization of these extended windows remains limited, with models struggling to maintain coherent reasoning across extended contexts, exhibiting systematic positional biases, and often ignoring the majority of provided information. Closing the gap between capacity and utilization, between synthetic benchmarks and practical performance, and between engineering optimization and cognitively-grounded memory systems constitutes the central challenge for the field moving forward.

EOFDISCUSSION

cat >> "$TEMPFILE" << 'EOFCONCLUSION'

% ============================================================
% CONCLUSION
% ============================================================

\section{Conclusion}
\label{sec:conclusion}

This survey has examined the multifaceted challenge of context management in large language models through ten interconnected perspectives, tracing a progression from foundational architectural constraints through diverse mitigation strategies to cognitively-inspired memory systems. The transformer's self-attention mechanism, while enabling the remarkable scaling and capabilities of modern language models, imposes a quadratic computational complexity that fundamentally limits context length. This constraint has motivated an ecosystem of techniques spanning architectural modifications to reduce complexity, algorithmic optimizations to improve efficiency, memory-augmented systems to extend effective capacity, and human-inspired hierarchical architectures to manage information across multiple timescales and granularities.

The central insight emerging from this survey is that effective context management requires coordinated advances across multiple dimensions rather than optimization of any single component in isolation. Architectural efficiency techniques including sparse attention, state space models, and hardware-aware implementations address computational bottlenecks but do not resolve challenges of effective utilization and information integration. Memory-augmented and retrieval-augmented systems ground generation in external knowledge and enable access to information beyond parametric capacity but remain vulnerable to position effects and retrieval failures. Context compression methods achieve substantial size reduction but face inevitable information loss and must balance compression ratio against task performance. Human-inspired memory architectures provide cognitively-grounded design principles for hierarchical organization, selective consolidation, and intelligent forgetting but require substantial engineering to implement effectively and scale to production deployment.

The persistent gap between nominal context capacity and effective utilization, evidenced by phenomena such as lost-in-the-middle effects and the observation that models utilize only ten to twenty percent of available context, indicates that raw window expansion alone is insufficient. Future progress requires architectural innovations enabling position-invariant attention, training procedures explicitly addressing positional biases, memory systems with explicit structure and access patterns, and evaluation frameworks that accurately predict real-world performance rather than synthetic benchmark scores. The convergence of insights from computer architecture, algorithm design, cognitive science, and empirical machine learning provides the foundation for this continued progress.

As language models continue their trajectory toward even longer contexts, more sophisticated reasoning, and broader deployment in critical applications, the importance of principled context management will only intensify. The techniques surveyed in this work demonstrate that diverse perspectives and approaches contribute essential insights. The future of long-context language understanding lies not in any single technique but in the intelligent orchestration of complementary mechanisms, drawing inspiration from both computational efficiency and human cognition to build systems capable of coherent, scalable, and robust reasoning over effectively unbounded information streams.

EOFCONCLUSION

# Add bibliography
cat >> "$TEMPFILE" << 'EOFBIB'

% ============================================================
% BIBLIOGRAPHY
% ============================================================

\bibliographystyle{IEEEtran}
\bibliography{references_complete}

\end{document}
EOFBIB

# Move temp file to final location
mv "$TEMPFILE" "$OUTFILE"
echo "Assembly complete: $OUTFILE"

