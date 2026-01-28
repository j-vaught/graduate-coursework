# Attention Approximation Methods for Long Context

## 1. Ring Attention with Blockwise Transformers
**Authors:** Liu et al. (Hao Liu, Matei Zaharia, Pieter Abbeel)
**Year:** 2023
**Venue:** arXiv
**ArXiv ID:** 2310.01889
**Title:** Ring Attention with Blockwise Transformers for Near-Infinite Context
**URL:** https://arxiv.org/abs/2310.01889

**Key Findings:**
Ring Attention enables training and inference on sequences up to device-count times longer than baselines through blockwise attention computation with fully overlapped communication. The approach allows million-token context training without approximations or computational overhead, using a ring topology where devices send key-value blocks to neighbors while computing blockwise attention, achieving 22x speedup over sliding window recomputation in streaming settings.

---

## 2. Flash Attention: Fast and Memory-Efficient Exact Attention
**Authors:** Dao et al. (Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré)
**Year:** 2022
**Venue:** ICLR 2023
**ArXiv ID:** 2205.14135
**Title:** FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
**URL:** https://arxiv.org/abs/2205.14135

**Key Findings:**
FlashAttention uses IO-aware tiling to reduce memory reads/writes between GPU HBM and SRAM, achieving 7.6x speedup on GPT-2 and linear sequence length memory usage rather than quadratic. The algorithm requires O(N²d²M⁻¹) HBM accesses compared to Ω(Nd + N²) for standard attention, enabling longer sequences to be processed efficiently on hardware while maintaining exact attention computation.

---

## 3. Sparse Attention: Generating Long Sequences with Sparse Transformers
**Authors:** Child et al.
**Year:** 2019
**Venue:** ICML 2019
**ArXiv ID:** 1904.10509
**Title:** Generating Long Sequences with Sparse Transformers
**URL:** https://arxiv.org/abs/1904.10509

**Key Findings:**
Sparse attention reduces computational complexity from O(n²) to O(n√n) through factorization of the attention matrix using fixed patterns (strided, fixed, local), enabling generation of long sequences like images and music at high resolution. The method proves that factorized sparse attention preserves the expressiveness of full attention for many tasks.

---

## 4. Sparser is Faster and Less is More: Efficient Sparse Attention
**Authors:** Multiple authors
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2406.16747
**Title:** Sparser is Faster and Less is More: Efficient Sparse Attention for Long-Range Transformers
**URL:** https://arxiv.org/abs/2406.16747

**Key Findings:**
Modern sparse attention approaches achieve linear complexity O(n) through learned patterns, block-wise routing, and clustering strategies. SPARSEK attention integrates scoring networks and differentiable top-k masking to select constant KV pairs per query, offering both linear complexity and constant memory footprint during generation with significant speedups on language modeling and downstream tasks.

---

## 5. Longformer: The Long-Document Transformer
**Authors:** Beltagy et al. (Iz Beltagy, Matthew E. Peters, Arman Cohan)
**Year:** 2020
**Venue:** ACL 2020
**ArXiv ID:** 2004.05150
**Title:** Longformer: The Long-Document Transformer
**URL:** https://arxiv.org/abs/2004.05150

**Key Findings:**
Longformer introduces a hybrid attention mechanism combining sliding window local attention (CNN-inspired) with task-motivated global attention, enabling linear-scaling attention for sequences up to 4096-8192 tokens. The model consistently outperforms RoBERTa on long document tasks and achieves SOTA on WikiHop and TriviaQA, demonstrating the effectiveness of combining local and global attention patterns.

---

## 6. BigBird: Transformers for Longer Sequences
**Authors:** Zaheer et al. (Manzil Zaheer, Guru Guruganesh, Avinava Dubey, Joshua Ainslie, Chris Alberti, Santiago Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang)
**Year:** 2020
**Venue:** NeurIPS 2020
**ArXiv ID:** 2007.14062
**Title:** Big Bird: Transformers for Longer Sequences
**URL:** https://arxiv.org/abs/2007.14062

**Key Findings:**
BigBird combines three attention patterns: global tokens attending to full sequence, all tokens attending to local windows, and random token connections, reducing attention from quadratic to linear complexity. The method is Turing complete and universal approximator, handling sequences 8x longer than previous methods, with SOTA on long document summarization and question-answering tasks.

---

## 7. Reformer: The Efficient Transformer
**Authors:** Kitaev et al. (Nikita Kitaev, Łukasz Kaiser, Anselm Levskaya)
**Year:** 2020
**Venue:** ICLR 2020
**ArXiv ID:** 2001.04451
**Title:** Reformer: The Efficient Transformer
**URL:** https://arxiv.org/abs/2001.04451

**Key Findings:**
Reformer uses locality-sensitive hashing (LSH) attention to reduce complexity from O(L²) to O(L log L), grouping similar items by hash and computing attention within segments. Combined with reversible residual layers for memory efficiency, Reformer processes sequences up to 1 million tokens on single 16GB accelerator, revolutionizing memory efficiency in long-sequence transformers.

---

## 8. DistFlashAttention: Distributed Memory-Efficient Attention
**Authors:** Multiple authors
**Year:** 2024
**Venue:** COLM 2024
**ArXiv ID:** 2310.03294
**Title:** DistFlashAttention: Distributed Memory-efficient Attention for Long-context LLMs Training
**URL:** https://arxiv.org/abs/2310.03294

**Key Findings:**
DistFlashAttention extends FlashAttention to distributed training with token-level workload balancing, overlapping KV communication, and rematerialization-aware checkpointing, achieving 8x longer sequences and 4.45-5.64x speedup over Ring Attention. Successfully trains Llama-7B with sequences up to 512K, advancing distributed training for ultra-long contexts.

---

## 9. S2-Attention: Hardware-Aware Context Sharding
**Authors:** Multiple authors
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2407.17678
**Title:** Efficient LLM Training and Serving with Heterogeneous Context Sharding among Attention Heads
**URL:** https://arxiv.org/abs/2407.17678

**Key Findings:**
S2-Attention heterogeneously shards context across attention heads, where each head attends to different token subsets while collectively covering full context, achieving 8.79X-25.3X wall-clock speedup versus FlashAttention-2. Maintains full attention performance and perfect 128K context retrieval with optimized memory IO and parallelization across heads.

---

## 10. Recycled Attention: Efficient Inference for Long-Context LLMs
**Authors:** Multiple authors
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2411.05787
**Title:** Recycled Attention: Efficient inference for long-context language models
**URL:** https://arxiv.org/html/2411.05787v1

**Key Findings:**
Recycled Attention alternates between full attention steps (all past tokens) and recycled attention steps (reduced KV cache of key tokens) during generation, balancing computational efficiency with semantic preservation. The approach addresses KV cache memory growth and quadratic attention computation time for long-context inference.

---

## Complexity Comparison

| Method | Complexity | Memory | Training Required | Context Limit |
|--------|-----------|--------|-------------------|---------------|
| Standard Attention | O(n²) | O(n²) | N/A | ~4K-8K |
| Sparse Attention | O(n√n) | O(n) | Yes | ~64K+ |
| BigBird | O(n) | O(n) | Yes | ~8x baseline |
| Reformer (LSH) | O(n log n) | O(n) | Yes | 1M |
| Flash Attention | O(n²) | O(n) | No | Hardware dependent |
| Ring Attention | O(n²) | O(n/d) | Yes | Near-infinite |

---

## References

- GPU MODE Lecture 13: https://christianjmills.com/posts/cuda-mode-notes/lecture-013/
- Research Google Blog: https://research.google/blog/constructing-transformers-for-longer-sequences-with-sparse-attention-methods/
- Medium Guide: https://medium.com/@rajboopathiking/demystifying-sparse-attention-longformer-bigbird-reformer-and-linformer-explained-029b97588144
