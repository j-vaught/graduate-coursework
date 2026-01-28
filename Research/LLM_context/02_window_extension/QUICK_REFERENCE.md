# Quick Reference: Context Window Extension Papers

## Alphabetical Index with Key Details

| # | Paper Title | Authors | Year | Venue | Context | File |
|---|---|---|---|---|---|---|
| 1 | Position Interpolation | Chen et al. | 2023 | EMNLP 2024 | 32K | 01 |
| 2 | NTK-Aware Scaling | bloc97 | 2023 | Community | 8K+ | 01 |
| 3 | YaRN: Efficient Context Extension | Peng et al. | 2023 | ICLR 2024 | 128K | 01 |
| 4 | LongRoPE | Ding et al. | 2024 | ICML 2024 | 2M | 01 |
| 5 | Dynamic NTK Scaling | emozilla | 2023 | Community | Adaptive | 01 |
| 6 | ComRoPE | Yu et al. | 2025 | CVPR 2025 | Scalable | 01 |
| 7 | ALiBi: Train Short, Test Long | Press et al. | 2022 | ICLR 2022 | 2K-16K+ | 02 |
| 8 | RoFormer: Rotary Embeddings | Su et al. | 2021 | arXiv | Foundation | 02 |
| 9 | Ring Attention | Liu et al. | 2023 | arXiv | Near-infinite | 03 |
| 10 | Flash Attention | Dao et al. | 2022 | ICLR 2023 | Efficient | 03 |
| 11 | Sparse Transformers | Child et al. | 2019 | ICML 2019 | ~64K | 03 |
| 12 | Longformer | Beltagy et al. | 2020 | ACL 2020 | 4K-8K | 03 |
| 13 | BigBird | Zaheer et al. | 2020 | NeurIPS 2020 | 8x baseline | 03 |
| 14 | Reformer | Kitaev et al. | 2020 | ICLR 2020 | 1M | 03 |
| 15 | DistFlashAttention | Multiple | 2024 | COLM 2024 | 512K | 03 |
| 16 | S2-Attention | Multiple | 2024 | arXiv | 128K | 03 |
| 17 | Recycled Attention | Multiple | 2024 | arXiv | Inference | 03 |
| 18 | StreamingLLM | Xiao et al. | 2023 | ICLR 2024 | 4M+ | 04 |
| 19 | Landmark Attention | Mohtashami & Jaggi | 2023 | arXiv | 32K+ | 04 |
| 20 | Recurrent Memory Transformer | Bulatov et al. | 2022 | NeurIPS 2022 | 64K+ | 04 |
| 21 | LongMem | Multiple | 2023 | NeurIPS 2023 | 65K | 04 |
| 22 | Self-Extend (LLM Maybe LongLM) | Jing et al. | 2024 | arXiv | 32K+ | 04 |
| 23 | Attention ≈ SDM | Bricken et al. | 2021 | arXiv | Theory | 04 |
| 24 | ARMT | Multiple | 2024 | arXiv | 64K+ | 04 |
| 25 | SkyLadder | Multiple | 2025 | arXiv | Efficient | 04 |
| 26 | GATEAU | Multiple | 2024 | arXiv | Efficient | 04 |
| 27 | LongAlign | Bai et al. | 2024 | OpenReview | 64K | 05 |
| 28 | E²-LLM | Xnhyacinth et al. | 2024 | ACL 2024 | Extreme | 05 |
| 29 | CLEX | Multiple | 2024 | ICLR 2024 | 4-8x baseline | 05 |
| 30 | Code Llama | Meta | 2023 | arXiv | 100K | 05 |
| 31 | Data Engineering 128K | Multiple | 2024 | arXiv | 128K | 05 |
| 32 | LongSkywork | Skywork | 2024 | arXiv | 128K+ | 05 |
| 33 | Domain Adaptation CPT | Multiple | 2024 | arXiv | Domain | 05 |
| 34 | Context Length in SFT | Multiple | 2024 | arXiv | Training | 05 |
| 35 | Synthetic CPT | Yang & Zhu | 2024 | GitHub | Synthetic | 05 |
| 36 | Beyond the Limits Survey | Multiple | 2024 | IJCAI 2024 | Survey | 06 |
| 37 | Awesome LLM Long-Context | Xnhyacinth | 2024 | GitHub | Curated | 06 |
| 38 | Technical Deep Dive | Amaar Agarwal | 2025 | Blog | 512→2M | 06 |
| 39 | Positional Encoding Survey | Multiple | 2024 | EMNLP 2024 | Survey | 06 |
| 40 | Extending RoPE | EleutherAI | 2023 | Blog | Technical | 06 |
| 41 | Rotary Embeddings Foundation | EleutherAI | 2021 | Blog | Foundation | 06 |
| 42 | ALiBi Deep Dive | SambaNova | 2022 | Blog | Analysis | 06 |
| 43 | Inside RoPE | LearnOpenCV | 2024 | Blog | Educational | 06 |
| 44 | Decomposed Positional Vectors | Multiple | 2024 | arXiv | 2405.18009 | 07 |
| 45 | 100-Sample Training | Multiple | 2024 | arXiv | 2401.07004 | 07 |
| 46 | Tokenwise Attention Scaling | Multiple | 2024 | arXiv | Scaling | 07 |
| 47 | Context-Aware Routing | Multiple | 2024 | arXiv | Routing | 07 |
| 48 | Core Context Attention (CCA) | Multiple | 2024 | arXiv | 2412.12465 | 07 |
| 49 | Sliding Window Training | Multiple | 2025 | ACL 2025 | Training | 07 |
| 50 | TokenSelect | Multiple | 2025 | EMNLP 2025 | Inference | 07 |
| 51 | Adaptive Grouped Attention | Multiple | 2025 | ACL 2025 | Training | 07 |
| 52 | Partial Context Training | Multiple | 2024 | OpenReview | Training | 07 |
| 53 | MixAttention | Databricks | 2024 | Blog | Hybrid | 07 |
| 54 | Bayesian Attention | Multiple | 2025 | arXiv | Theory | 07 |
| 55 | Sparse Attention Survey | Multiple | 2024 | arXiv | Survey | 07 |

---

## Papers by Context Length Achieved

| Context Length | Papers | Key Method |
|---|---|---|
| 4K-8K | Longformer, BigBird, Code Llama (initial) | Sparse + scaling |
| 16K | ALiBi, PI (basic) | Position encoding |
| 32K | PI, Landmark, Self-Extend | Interpolation |
| 64K | LongAlign, LongMem, ARMT | Training recipe |
| 128K | LongSkywork, Data Engineering, YaRN | Continual PT |
| 256K | LongRoPE (progressive) | Progressive scaling |
| 1M+ | Gemini 1.5, GPT-4.1, StreamingLLM theory | Industry models |
| 2M | LongRoPE | Multi-stage extension |
| 10M+ | Emerging frontier | Future work |
| Infinite | StreamingLLM, Theoretical limits | Streaming/Memory |

---

## Papers by Method Category

### Position Encoding (6 papers)
- Position Interpolation (Chen et al., 2023)
- NTK-Aware Scaling (bloc97, 2023)
- YaRN (Peng et al., 2023)
- LongRoPE (Ding et al., 2024)
- ComRoPE (Yu et al., 2025)
- RoFormer/RoPE Foundation (Su et al., 2021)

### Attention Approximation (10 papers)
- Ring Attention (Liu et al., 2023)
- Flash Attention (Dao et al., 2022)
- Sparse Transformers (Child et al., 2019)
- Longformer (Beltagy et al., 2020)
- BigBird (Zaheer et al., 2020)
- Reformer (Kitaev et al., 2020)
- DistFlashAttention (2024)
- S2-Attention (2024)
- Recycled Attention (2024)
- Sparse Attention Survey (2024)

### Memory & Streaming (10 papers)
- StreamingLLM (Xiao et al., 2023)
- Landmark Attention (Mohtashami & Jaggi, 2023)
- Recurrent Memory Transformer (Bulatov et al., 2022)
- LongMem (2023)
- Self-Extend (Jing et al., 2024)
- Attention ≈ SDM (Bricken et al., 2021)
- ARMT (2024)
- SkyLadder (2025)
- GATEAU (2024)
- LongAlign (Bai et al., 2024)

### Training Methodologies (9 papers)
- LongAlign (Bai et al., 2024)
- E²-LLM (Xnhyacinth et al., 2024)
- CLEX (2024)
- Code Llama (Meta, 2023)
- Data Engineering for 128K (2024)
- LongSkywork (Skywork, 2024)
- Domain Adaptation via CPT (2024)
- Context Length in SFT (2024)
- Synthetic CPT (Yang & Zhu, 2024)

### Surveys & Foundational (8 papers)
- Beyond the Limits (2024)
- Awesome LLM Long-Context (Xnhyacinth, 2024)
- Technical Deep Dive (Amaar Agarwal, 2025)
- Positional Encoding Survey (2024)
- EleutherAI blogs (2021-2023)
- SambaNova ALiBi analysis (2022)
- LearnOpenCV RoPE guide (2024)
- Transformer Family v2.0 (Lilian Weng, 2023)

### Emerging/Specialized (8 papers)
- Decomposed Positional Vectors (2024)
- 100-Sample Training (2024)
- Context-Aware Routing (2024)
- Core Context Attention (2024)
- Sliding Window Training (2025)
- TokenSelect (2025)
- Adaptive Grouped Attention (2025)
- Partial Context Training (2024)
- MixAttention (Databricks, 2024)
- Bayesian Attention (2025)

---

## Papers by Publication Year

| Year | Count | Major Contributions |
|---|---|---|
| 2020 | 4 | Foundational (Reformer, Longformer, BigBird) |
| 2021 | 2 | RoPE introduction, theoretical foundations |
| 2022 | 3 | ALiBi, Flash Attention, RMT |
| 2023 | 7 | PI, NTK-aware, YaRN, Ring, StreamingLLM |
| 2024 | 20+ | Consolidation (LongRoPE, CLEX, E²-LLM) & surveys |
| 2025 | 5+ | Emerging (ComRoPE, SkyLadder, TokenSelect) |

---

## Papers by Venue

| Venue | Count | Papers |
|---|---|---|
| ICLR | 7 | Pi, NTK, YaRN, Flash Attn, Reformer, CLEX, and others |
| NeurIPS | 2 | BigBird, RMT |
| ACL | 3 | Longformer, E²-LLM, others |
| EMNLP | 3 | Positional encoding survey, context window papers |
| CVPR | 1 | ComRoPE |
| IJCAI | 1 | Beyond the Limits survey |
| ArXiv | 25+ | Preprints and recent work |
| Industry Blogs | 8+ | Technical resources |
| GitHub/Community | 5+ | Implementations and curations |

---

## Papers by Citation Key (ArXiv IDs)

### 2306.15595 - Position Interpolation
### 2309.00071 - YaRN
### 2108.12409 - ALiBi
### 2402.13753 - LongRoPE
### 2310.01889 - Ring Attention
### 2205.14135 - Flash Attention
### 2004.05150 - Longformer
### 2007.14062 - BigBird
### 2001.04451 - Reformer
### 2309.17453 - StreamingLLM
### 2305.16300 - Landmark Attention
### 2207.06881 - Recurrent Memory Transformer
### 2401.01325 - Self-Extend
### 2401.06951 - E²-LLM
### 2310.16450 - CLEX
### 2401.18058 - LongAlign
### 2406.00605 - LongSkywork
### 2402.02244 - Beyond the Limits Survey
### 2506.03737 - ComRoPE

---

## Key Statistics

**Total Papers:** 55+
**Total Resources:** 70+
**Years Covered:** 2020-2025
**Venues:** 9 different (ICLR, NeurIPS, ACL, EMNLP, CVPR, IJCAI, ArXiv, blogs, community)
**Context Range:** 512 tokens → 2M tokens (LongRoPE) → Theoretical infinite
**Most Cited Method:** RoPE (foundation for 80%+ of extension methods)
**Most Recent:** 2025 papers on training efficiency and inference optimization

---

## Quick Search Guide

### Find papers on...

**Position Encoding:** Files 01, 02, 06
**Attention Mechanisms:** File 03
**Memory Systems:** File 04
**Training Methods:** File 05
**Surveys:** File 06
**Emerging Work:** File 07

**Specific Methods:**
- RoPE variants: 01
- ALiBi: 02
- Sparse attention: 03
- StreamingLLM: 04
- YaRN: 01, 05, 06
- LongRoPE: 01, 06
- RMT: 04, 06
- Flash Attention: 03, 06
- Ring Attention: 03, 06

**By Venue:**
- ICLR papers: 01, 03, 05, 06
- NeurIPS papers: 03, 04
- ACL/EMNLP: 03, 05, 06, 07
- Community/ArXiv: All files

---

## Direct Access Guide

All papers include ArXiv IDs or direct URLs. Use:
- **ArXiv.org:** https://arxiv.org/abs/[ID]
- **PDF direct:** https://arxiv.org/pdf/[ID].pdf
- **HuggingFace Papers:** https://huggingface.co/papers/[ID]
- **Conference proceedings:** Links in individual files

---

Last updated: January 27, 2026
