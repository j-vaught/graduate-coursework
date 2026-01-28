# Position Encoding Alternatives to RoPE

## 1. ALiBi (Attention with Linear Biases)
**Authors:** Press et al. (Ofir Press, Noah Smith, Mike Lewis)
**Year:** 2022
**Venue:** ICLR 2022
**ArXiv ID:** 2108.12409
**Title:** Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation
**URL:** https://arxiv.org/abs/2108.12409

**Key Findings:**
ALiBi replaces positional embeddings with learnable linear biases on attention scores proportional to distance between query-key pairs, enabling strong length extrapolation without sinusoidal embeddings. A 1.3B parameter model trained on 1024-length sequences achieves 2048-length performance with 11% faster training and 11% less memory, with empirical evidence showing ALiBi maintains low perplexity even when extrapolating to 16,000 tokens while RoPE perplexity explodes.

---

## 2. Extrapolation vs Interpolation: Theoretical Comparison
**Authors:** Multiple researchers (Press, Chen et al.)
**Year:** 2022-2023
**Venue:** Various (ICLR 2022-2024)
**Status:** Foundational comparison in position encoding literature
**URL:** https://sambanova.ai/blog/alibi-interpolation-vs-extrapolation

**Key Findings:**
ALiBi uses extrapolation (linear distance penalty) while Position Interpolation uses interpolation, with theoretical tradeoffs: interpolation requires choosing a fixed scaling factor with short-sequence degradation tradeoff, while ALiBi's linear bias naturally extrapolates but requires learned parameters. RoPE struggles with extrapolation due to frequency domain assumptions, leading to development of hybrid methods like dynamic scaling and NTK-aware variants.

---

## 3. Rotary Embeddings Mathematical Foundation
**Author:** Su et al. (foundational RoFormer paper referenced in context extension literature)
**Year:** 2021
**Venue:** arXiv
**ArXiv ID:** 2104.09864
**Title:** RoFormer: Enhanced Transformer with Rotary Position Embedding
**URL:** https://arxiv.org/abs/2104.09864

**Key Findings:**
RoPE encodes position information through rotation matrices in 2D planes, providing explicit relative position dependency with theoretical guarantees. The approach is now dominant in modern LLMs (LLaMA, Mistral, Gemma, GPT-J), enabling smooth frequency scaling for context extension when combined with scaling techniques like NTK-aware or YaRN methods.

---

## 4. Distributional Perspective on Positional Encoding
**Authors:** Zhang et al. (Multiple authors from EMNLP 2024 findings)
**Year:** 2024
**Venue:** EMNLP 2024 Findings
**Status:** Recent distributional analysis approach
**URL:** https://aclanthology.org/2024.findings-emnlp.582.pdf

**Key Findings:**
Analysis shows rotary angle distributions are critical for context extension success, with existing methods introducing out-of-distribution angles causing suboptimal performance. A distributional minimization approach selectively applies interpolation or extrapolation per dimension based on disturbance scores, achieving 4.33% improvement over Position Interpolation when extending LLaMA2-7B to 16K tokens.

---

## 5. Impact of Positional Encoding on Length Generalization
**Authors:** Multiple researchers
**Year:** 2023
**Venue:** Various conferences
**Status:** Foundational analysis
**URL:** https://arxiv.org/pdf/2305.19466

**Key Findings:**
Comprehensive analysis of how positional encoding design affects model ability to generalize to longer sequences, comparing sinusoidal embeddings, learned embeddings, relative position biases (ALiBi), and rotary embeddings. Shows fundamental tradeoffs between extrapolation capability, training efficiency, and performance on original context lengths.

---

## Comparative Summary

| Method | Type | Extrapolation | Training Required | Key Advantage |
|--------|------|---------------|-------------------|----------------|
| ALiBi | Linear Bias | Excellent | Minimal | Native extrapolation, no embeddings |
| RoPE (vanilla) | Rotary | Poor | None | Stable frequencies, relative position |
| Position Interpolation | Interpolation | Moderate | Light fine-tuning | Simple, stable |
| NTK-Aware | Interpolation | Good | No fine-tuning | Dimension-aware scaling |
| YaRN | Interpolation + Temperature | Excellent | Light fine-tuning | Industry standard, robust |
| Dynamic NTK | Interpolation | Excellent | No fine-tuning | Adaptive scaling at inference |

---

## Resources

- EleutherAI Rotary Embeddings: https://blog.eleuther.ai/rotary-embeddings/
- Towards Data Science Guide: https://towardsdatascience.com/positional-embeddings-in-transformers-a-math-guide-to-rope-alibi/
- Medium: Position Encoding Evolution: https://medium.com/@pajakamy/alibi-attention-with-linear-biases-942abe042e9f
