# Memory-Augmented and Streaming Methods for Long Context

## 1. StreamingLLM: Efficient Streaming Language Models with Attention Sinks
**Authors:** Xiao et al. (Tianle Xiao, Yushun Dong, Yilun Du, Shiyu Chang, Arvind Krishnamurthy, Ying Nian Wu)
**Year:** 2023
**Venue:** ICLR 2024
**ArXiv ID:** 2309.17453
**Title:** Efficient Streaming Language Models with Attention Sinks
**URL:** https://arxiv.org/abs/2309.17453

**Key Findings:**
StreamingLLM enables finite-context LLMs to generalize to infinite sequence lengths without fine-tuning by leveraging the "attention sink" phenomenon where initial tokens receive disproportionately high attention. By retaining initial tokens as attention sinks in the KV cache and using sliding-window KV for recent context, StreamingLLM enables LLaMA-2, MPT, Falcon, and Pythia to process 4M+ tokens with 22.2x speedup over sliding window recomputation in streaming settings.

---

## 2. Landmark Attention: Random-Access Infinite Context Length for Transformers
**Authors:** Mohtashami & Jaggi (Mohammad Mohtashami, Martin Jaggi)
**Year:** 2023
**Venue:** ICLR 2024 (accepted)
**ArXiv ID:** 2305.16300
**Title:** Landmark Attention: Random-Access Infinite Context Length for Transformers
**URL:** https://arxiv.org/abs/2305.16300

**Key Findings:**
Landmark Attention uses landmark tokens to represent blocks of input, training attention to select relevant blocks directly through the mechanism instead of separate retrieval, enabling random-access to full context. Fine-tuning LLaMA-7B extends context to 32K tokens (GPT-4 level), allowing block-level retrieval while maintaining full context access through learned landmark-based routing.

---

## 3. Recurrent Memory Transformer
**Authors:** Bulatov et al. (Aydar Bulatov, Yuri Kuratov, Dmitry Sorokin)
**Year:** 2022
**Venue:** NeurIPS 2022
**ArXiv ID:** 2207.06881
**Title:** Recurrent Memory Transformer
**URL:** https://arxiv.org/abs/2207.06881

**Key Findings:**
Recurrent Memory Transformer (RMT) uses special memory tokens to create segment-level recurrence, processing long sequences through recurrent segment connections with O(n) complexity. Memory tokens provide additional capacity for cross-segment information aggregation, outperforming Transformer-XL on tasks requiring long-term dependencies while scaling linearly with sequence length.

---

## 4. Augmenting Language Models with Long-Term Memory
**Authors:** Multiple researchers
**Year:** 2023
**Venue:** NeurIPS 2023
**ArXiv ID:** 2306.07174
**Title:** Augmenting Language Models with Long-Term Memory
**URL:** https://arxiv.org/abs/2306.07174

**Key Findings:**
LongMem augments LLMs with external memory modules using a decoupled architecture: original backbone LLM frozen as memory encoder, adaptive residual side-network as memory retriever/reader. Extends long-form memory to 65K tokens for caching many-shot demonstrations, enabling few-shot learning with extensive in-context examples while maintaining original model performance.

---

## 5. Self-Extend: LLM Maybe LongLM - Context Window Without Tuning
**Authors:** Jing et al.
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2401.01325
**Title:** LLM Maybe LongLM: Self-Extend LLM Context Window Without Tuning
**URL:** https://arxiv.org/abs/2401.01325

**Key Findings:**
Self-Extend extends context windows through bi-level attention without training: grouped attention captures far-apart token dependencies via position remapping (FLOOR operation), neighbor attention captures adjacent token dependencies. With only 4 lines of code modification, achieves performance matching or exceeding fine-tuning methods on synthetic and real long-context tasks by addressing out-of-distribution positional encodings.

---

## 6. Attention Approximates Sparse Distributed Memory
**Authors:** Bricken et al. (Trenton Bricken, Cengiz Pehlevan, Ila R. Fiete)
**Year:** 2021
**Venue:** OpenReview
**ArXiv ID:** 2111.05498
**Title:** Attention Approximates Sparse Distributed Memory
**URL:** https://arxiv.org/abs/2111.05498

**Key Findings:**
Theoretical analysis showing attention mechanisms approximate sparse distributed memory (SDM) storage and retrieval systems, providing interpretability for how transformers use attention as an associative memory. This framework explains why transformers are effective for long-context processing and guides design of memory-augmented architectures.

---

## 7. Associative Recurrent Memory Transformer
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2407.04841
**Title:** Associative Recurrent Memory Transformer
**URL:** https://arxiv.org/abs/2407.04841

**Key Findings:**
ARMT extends RMT with associative memory mechanisms for improved task-specific information distribution across long contexts. Combines local attention for immediate context with segment-level recurrence for long-term memory storage, advancing memory-augmented transformer designs for improved long-context reasoning.

---

## 8. SkyLadder: Better and Faster Pretraining via Context Window Scheduling
**Authors:** Multiple researchers
**Year:** 2025
**Venue:** arXiv
**ArXiv ID:** 2503.15450
**Title:** SkyLadder: Better and Faster Pretraining via Context Window Scheduling
**URL:** https://arxiv.org/html/2503.15450v1

**Key Findings:**
SkyLadder introduces context window scheduling during pretraining, progressively increasing sequence length during training phases to improve efficiency and downstream performance. Reduces pretraining compute while improving model quality, addressing the challenge of training efficient long-context LLMs through intelligent curriculum learning on sequence lengths.

---

## 9. GATEAU: Selecting Influential Samples for Long Context Alignment
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2410.15633
**Title:** GATEAU: Selecting Influential Sample for Long Context Alignment
**URL:** https://arxiv.org/html/2410.15633v2

**Key Findings:**
GATEAU selects influential training samples for efficient long-context alignment through importance scoring, reducing data requirements for context extension. The method identifies which data samples contribute most to long-context performance, enabling efficient fine-tuning without large-scale long-context corpora.

---

## 10. LongSkywork: A Training Recipe for Extending Context Length
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2406.00605
**Title:** LongSkywork: A Training Recipe for Efficiently Extending Context Length in Large Language Models
**URL:** https://arxiv.org/html/2406.00605v1

**Key Findings:**
LongSkywork provides comprehensive training recipes for context extension including data construction, training strategies, and evaluation methodology. Demonstrates effective long-context alignment through careful engineering of training procedures, synthetic data generation, and loss weighting strategies.

---

## Key Characteristics of Memory-Augmented Methods

| Method | Memory Type | Training | Context Achievable | Key Innovation |
|--------|------------|----------|-------------------|-----------------|
| StreamingLLM | Attention Sink | None | Infinite | Sink phenomenon exploitation |
| Landmark | Block Markers | Light | 32K+ | Block-level routing |
| RMT | Recurrent Tokens | Yes | 64K+ | Segment-level recurrence |
| LongMem | External Memory | Yes | 65K | Side-network retrieval |
| Self-Extend | Positional Remap | None | 32K+ | No training needed |

---

## Related Concepts

- **Memorize-while-Reading:** New paradigm using memory agents to digest documents chunk-by-chunk with memory overwriting strategies
- **Look-Back Mechanisms:** "Look Back to Reason Forward" - revisitable memory for agent long-context tasks
- **Memory-Augmented Architecture:** Dedicated systems for long-term context handling in agent-based LLMs

## References

- MIT-HAN-Lab StreamingLLM: https://github.com/mit-han-lab/streaming-llm
- Attention Sinks Implementation: https://github.com/tomaarsen/attention_sinks
- Awesome LLM Long-Context: https://github.com/Xnhyacinth/Awesome-LLM-Long-Context-Modeling
