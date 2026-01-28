# KV-Cache Optimization Research Collection Index

**Generated**: January 27, 2026
**Total Documents**: 11 markdown files + 1 index
**Total Lines**: 2,961 lines of research data
**Collection Scope**: 50+ papers spanning 2019-2026

---

## Files Overview

### 1. README.md (316 lines)
**Purpose**: Navigation guide and overview
- Directory structure explanation
- Research statistics
- Implementation roadmap
- Quick navigation by use case
- Recommended reading order

### 2. 01_kv_cache_memory_bottleneck.md (70 lines)
**Topic**: Fundamental KV cache challenges
- **Covered Papers**:
  - Survey on KV Cache Management (2024)
  - KV Cache Compression Review (2024)
  - LLM Inference Handbook (BentoML)
  - Inference-Time Hyper-Scaling (OpenReview)
- **Key Findings**: 30× model size memory, 70%→10% efficiency drop
- **Optimization Directions**: Quantization, GQA, compression

### 3. 02_h2o_heavy_hitter_oracle.md (119 lines)
**Topic**: Token eviction via attention importance
- **Paper**: H₂O (Zhang et al., NeurIPS 2023)
- **arXiv**: 2306.14048
- **Key Innovation**: Heavy-hitter identification
- **Performance**: 29× throughput vs. DeepSpeed/Hugging Face, 1.9× latency reduction
- **Coverage**: OPT, LLaMA, GPT-NeoX
- **Limitations**: Overhead during prefill, task-dependent effectiveness

### 4. 03_streamingllm_attention_sinks.md (184 lines)
**Topic**: Streaming LLMs with attention sinks
- **Paper**: Efficient Streaming Language Models (Xiao et al., ICLR 2024)
- **arXiv**: 2309.17453
- **Core Innovation**: Attention sink phenomenon (initial tokens get high attention)
- **Capability**: 4M+ token contexts
- **Performance**: 22.2× speedup vs. sliding window recomputation
- **Models**: Llama-2, Mistral, MPT, Falcon, Pythia, GPT-NeoX
- **Mechanism**: Retain initial tokens + sliding window recent tokens

### 5. 04_kv_cache_quantization.md (252 lines)
**Topic**: Sub-4-bit KV cache quantization
- **Papers**:
  - KIVI (Yuan et al., ICML 2024) - arXiv 2402.02750
  - KVQuant (Hooper et al., NeurIPS 2024) - arXiv 2401.18079
  - KITTY (2024)
- **KIVI Performance**: 2.6× memory reduction, 4× batch size, 2.35-3.47× throughput
- **KVQuant Performance**: <0.1 PPL at 3-bit, 1M tokens on A100, 10M on 8-GPU
- **Methods**: Per-channel keys, per-token values, non-uniform quantization, outlier handling
- **Models**: Llama, Llama-2, Llama-3, Mistral, Falcon

### 6. 05_multi_query_and_grouped_query_attention.md (278 lines)
**Topic**: Multi-head KV reduction architectures
- **Papers**:
  - MQA: Fast Transformer Decoding (Shazeer, 2019) - arXiv 1911.02150
  - GQA: Generalized Multi-Query (Ainslie et al., EMNLP 2023) - arXiv 2305.13245
- **MQA**: Single KV shared across heads, faster decoding, quality trade-off
- **GQA**: Grouped KV heads (1 < G < H), balanced efficiency-quality
- **Performance**: GQA on Llama-3 8B reduces 280GB→70GB (75% savings)
- **Adoption**: Llama-2 (July 2023), Mistral-7B (Sept 2023), Llama-3 (2024)
- **Uptraining**: 5% of original pretraining cost to convert MHA→GQA

### 7. 06_pagedattention_vllm.md (290 lines)
**Topic**: Virtual memory for KV cache management
- **Paper**: Efficient Memory Management (Kwon et al., SOSP 2023) - arXiv 2309.06180
- **vLLM**: Serving system implementing PagedAttention
- **Core Innovation**: OS paging principles applied to KV cache
- **Architecture**: Block-based allocation, logical→physical mapping, near-zero waste
- **Performance**: 2-4× throughput vs. FasterTransformer, improved with longer sequences
- **Variants**:
  - PagedEviction (block-wise pruning)
  - vAttention (OS demand paging, ASPLOS 2025)

### 8. 07_token_eviction_methods.md (350 lines)
**Topic**: Token selection and dropping strategies
- **Methods Covered**:
  - ScissorHands: Attention score accumulation
  - FastGen: Adaptive layer-wise selection
  - Q-HITTER: Heavy-hitter + quantization (MLSys 2024)
  - HashEvict: LSH pre-attention eviction (arXiv 2412.16187)
  - MiniCache: Depth-wise merging (NeurIPS 2024)
  - KVReviver: Reversible compression (arXiv 2512.17917)
  - RocketKV: Two-stage compression (arXiv 2502.14051)
- **Performance**: 30-70% compression with minimal quality loss
- **FastGen**: Outperforms H2O and Scissorhands with adaptive selection
- **Q-HITTER**: 20× memory reduction, 33× vs. Hugging Face, 1.3× vs. H2O
- **HashEvict**: 1.5-2× prefill speedup, 30-70% compression on Llama-3

### 9. 08_cross_layer_kv_sharing.md (368 lines)
**Topic**: Sharing KV cache across transformer layers
- **Papers**:
  - Systematic Study (NAACL 2025 short) - arXiv 2410.14442
  - LCKV (Layer-Condensed KV, ACL 2024)
  - YOCO: You Only Cache Once (NeurIPS 2024) - arXiv 2405.05254
  - SqueezeAttention (ICLR 2025) - arXiv 2404.04793
- **Methods**:
  - CLA: Uniform group sharing
  - LCKV: Adaptive per-layer sharing
  - YOCO: O(N) instead of O(N×L) memory via decoder-decoder architecture
  - SqueezeAttention: 2D optimization (sequence + layer dimensions)
- **YOCO Performance**: Architectural alternative, 1M token context
- **SqueezeAttention Performance**: 30-70% memory reduction, 2.2× throughput
- **Key Insight**: Not all layers equally need KV cache

### 10. 09_dynamic_memory_management.md (368 lines)
**Topic**: Runtime memory allocation and adaptation
- **Systems**:
  - PagedAttention/vLLM (reference)
  - vAttention (OS demand paging, ASPLOS 2025) - arXiv 2405.04437
  - eLLM (Elastic management) - arXiv 2506.15155
- **Optimization Techniques**:
  - Entropy-guided budget (MDPI, 2024)
  - Prompt Cache (Yale + Google, MLSys 2024) - arXiv 2311.04934
  - Expected Attention (predictive) - arXiv 2510.00636
- **Prompt Cache**: 8-60× improvement, structured prompt reuse
- **vAttention**: 1.97× faster token generation, simpler kernel design
- **Entropy-guided**: 4.18% memory reduction (Qwen3 4B), 46.6% decode speedup (Mistral)

### 11. 10_additional_research_papers.md (366 lines)
**Topic**: Long-context and supplementary methods
- **Long-Context Methods**:
  - LM-Infinite (NAACL 2024) - arXiv 2308.16137
  - InfLLM (NeurIPS 2024, ICML oral) - arXiv 2402.04617
- **Foundational Work**:
  - FlashAttention (Dao et al., NeurIPS 2022) - arXiv 2205.14135
- **Analysis Papers**:
  - When Attention Sink Emerges (ICLR 2025)
  - Why Do LLMs Attend to First Token?
  - Hold Onto That Thought: Compression on Reasoning
  - The Pitfalls of KV Cache Compression
- **Sparse Attention**: The Sparse Frontier (2024)
- **Advanced Methods**: KITTY (info-theoretic), Reviving Efficient Attention
- **Performance Summary Table**: All methods compared

---

## Research Statistics

### By Optimization Category

**Quantization Methods** (5 papers)
- KIVI, KVQuant, KITTY, Q-HITTER integration, others

**Eviction/Selection** (6+ papers)
- H2O, Scissorhands, FastGen, HashEvict, entropy-guided, etc.

**Architectural Changes** (5 papers)
- MQA, GQA, YOCO, others

**Memory Management** (4 papers)
- PagedAttention, vAttention, eLLM, Prompt Cache

**Long-Context** (3 papers)
- StreamingLLM, LM-Infinite, InfLLM

**Cross-Layer Sharing** (4 papers)
- CLA, LCKV, YOCO, SqueezeAttention

**Foundational/Analysis** (5+ papers)
- FlashAttention, When Attention Sink Emerges, etc.

### By Venue

| Venue | Count | Notable Papers |
|-------|-------|-----------------|
| NeurIPS | 4 | H2O, KVQuant, YOCO, InfLLM (oral) |
| ICLR | 4 | StreamingLLM, SqueezeAttention, When Attention Sink, others |
| EMNLP | 1 | GQA |
| SOSP | 1 | PagedAttention |
| NAACL | 1 | Cross-Layer KV Sharing |
| ACL | 2 | LCKV, others |
| MLSys | 2 | Prompt Cache, Q-HITTER |
| ICML | 2 | KIVI, InfLLM (oral) |
| ASPLOS | 1 | vAttention |
| arXiv/Preprint | 20+ | KITTY, FlashAttention, LM-Infinite, etc. |

### Timeline

- **2019**: 1 paper (MQA)
- **2022**: 1 paper (FlashAttention)
- **2023**: 7 papers (H2O, GQA, StreamingLLM, PagedAttention, etc.)
- **2024**: 16+ papers (KVQuant, KIVI, YOCO, LCKV, SqueezeAttention, etc.)
- **2025**: 3+ papers (When Attention Sink, ASPLOS/vAttention, NAACL)

---

## Key Performance Summary

### Memory Reduction Achieved
- **GQA**: 2-8× (75% reduction Llama-3)
- **KIVI**: 2.6×
- **KVQuant**: 4-10× (1M tokens on A100)
- **Quantization + other**: Cumulative

### Throughput Improvement
- **H2O**: 29× vs. DeepSpeed
- **PagedAttention**: 2-4× vs. FasterTransformer
- **vAttention**: 1.97× vs. vLLM
- **Prompt Cache**: 8-60× (prompt processing)

### Context Length Capability
- **Standard**: 4K-8K tokens (pre-trained limit)
- **StreamingLLM**: 4M+ tokens
- **InfLLM**: 1M tokens
- **YOCO**: Theoretically unlimited
- **KVQuant**: 10M tokens (8-GPU)

### Quality Preservation
- **GQA**: Minimal loss (uptraining helps)
- **KIVI**: Near-lossless (2-bit)
- **KVQuant**: <0.1 PPL at 3-bit
- **Token eviction**: 20-30% cache, <5% quality loss

---

## Research Quality Indicators

### Citation Impact
- Most papers from top-tier venues
- Recent papers (2023-2025) likely highly cited
- Mix of foundational (FlashAttention) and cutting-edge (YOCO)

### Code Availability
- **Open Source**: vLLM, PagedAttention, KIVI, KVQuant, many others
- **GitHub**: Links provided for most papers
- **Community**: Active development and integration

### Reproducibility
- **Benchmarks**: Standard datasets (WikiText-2, C4, MMLU)
- **Models**: Major models covered (Llama, Mistral, Falcon, etc.)
- **Hardware**: A100, GPUs specified
- **Implementation**: Many have released code

---

## Cross-References and Relationships

### Method Combinations (Recommended)

**For Maximum Efficiency**
1. PagedAttention (memory management)
2. GQA (architecture optimization)
3. KIVI (quantization)
4. Token eviction (H2O or HashEvict)
5. Prompt caching (API service optimization)

**For Long Contexts**
1. YOCO (architecture)
2. KVQuant (quantization for extreme length)
3. Cross-layer sharing (optional)

**For Production Systems**
1. vLLM with PagedAttention
2. GQA models
3. Optional: Prompt caching
4. Optional: Token eviction for specific tasks

### Papers Building on Others
- Q-HITTER improves H2O with quantization awareness
- FastGen selects from H2O/Scissorhands strategies
- SqueezeAttention extends H2O + layer-wise tuning
- vAttention proposed as alternative to PagedAttention

---

## Data Validation

### Sources
- Academic repositories (arXiv)
- Conference proceedings (NeurIPS, ICLR, ACM DL)
- GitHub repositories
- Official blogs (Google Research, NVIDIA, etc.)

### Completeness
- All major papers in KV-cache optimization (2019-2026) included
- Coverage across all technique categories
- Both foundational and cutting-edge work represented

### Currency
- Data current as of January 27, 2026
- Includes NeurIPS 2024 and ICLR 2025 papers
- Recent arXiv preprints included

---

## Usage Recommendations

### For Literature Review
- Start with README.md for navigation
- Read papers by topic in sequence
- Use "Sources Referenced" for detailed citations

### For Implementation
- Follow "Implementation Roadmap" in README
- Select techniques based on use case
- Refer to "Quick Navigation Guide"

### For Research
- Review "Cross-layer KV Sharing" framework (NAACL 2025)
- Analyze performance tables in each file
- Check "Open Research Directions" section

---

**Collection Metadata**:
- **Format**: Markdown (portable, version-controllable)
- **Organization**: Topic-based (10 topics + index)
- **Detail Level**: Deep dives per topic with full citations
- **Total Content**: 2,961 lines of research analysis
- **Status**: Complete and validated

---

## Files Generated

```
04_kv_cache/
├── README.md                                    (Navigation & overview)
├── 01_kv_cache_memory_bottleneck.md            (Problem fundamentals)
├── 02_h2o_heavy_hitter_oracle.md               (Token selection via H2O)
├── 03_streamingllm_attention_sinks.md          (Streaming + sinks)
├── 04_kv_cache_quantization.md                 (KIVI, KVQuant)
├── 05_multi_query_and_grouped_query_attention.md (MQA, GQA)
├── 06_pagedattention_vllm.md                   (Virtual memory)
├── 07_token_eviction_methods.md                (Eviction strategies)
├── 08_cross_layer_kv_sharing.md                (Layer sharing)
├── 09_dynamic_memory_management.md             (Runtime allocation)
├── 10_additional_research_papers.md            (Supplementary)
└── COLLECTION_INDEX.md                         (This file)
```

**Total Files**: 11 markdown content files + 1 index
**Total Lines**: 2,961 (documentation) + this index
**Ready For**: Literature review, implementation, research

---

**End of Collection Index**
**Compiled**: January 27, 2026
