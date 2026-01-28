# PagedAttention and vLLM: Virtual Memory for LLM Serving

## Paper Overview
**Title**: Efficient Memory Management for Large Language Model Serving with PagedAttention
**Authors**: Woosuk Kwon et al. (UC Berkeley)
**Year**: 2023
**Venue**: SOSP 2023 (29th Symposium on Operating Systems Principles)
**arXiv ID**: 2309.06180
**URLs**:
- arXiv: [https://arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180)
- PDF: [https://arxiv.org/pdf/2309.06180](https://arxiv.org/pdf/2309.06180)
- SOSP 2023: [https://dl.acm.org/doi/10.1145/3600006.3613165](https://dl.acm.org/doi/10.1145/3600006.3613165)
- vLLM Blog: [https://blog.vllm.ai/2023/06/20/vllm.html](https://blog.vllm.ai/2023/06/20/vllm.html)
- GitHub: [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
- Lecture Slides: [https://llmsystem.github.io/llmsystem2025spring/assets/files/llmsys-22-vLLM_woosuk_kwon-1f34697dbb1a1fb5b798daf6eff14b67.pdf](https://llmsystem.github.io/llmsystem2025spring/assets/files/llmsys-22-vLLM_woosuk_kwon-1f34697dbb1a1fb5b798daf6eff14b67.pdf)

## Core Problem: KV Cache Memory Fragmentation

### Challenges in Batched LLM Serving

#### 1. Dynamic Memory Growth
- Each request has unique KV cache size
- KV cache grows during token generation
- Growth rate unpredictable (variable length sequences)
- Memory requirements change per request

#### 2. Memory Fragmentation
- Sequence lengths vary dramatically
- Pre-allocating maximum size wastes memory
- Dynamic allocation causes fragmentation
- Unused memory scattered across GPU memory

#### 3. Redundant Duplication
- Beam search: multiple hypotheses share prefixes
- Prompt sharing: multiple requests share common prefixes
- Duplication not exploited in standard systems
- Wasted memory in shared computation

### Scale of the Problem
- **High batch serving**: 64-128 concurrent requests typical
- **Memory waste**: 50-80% of allocated KV cache unused
- **Throughput impact**: Severely limits batch size
- **Latency degradation**: Fragmentation causes stalls

## Key Innovation: PagedAttention

### Inspiration from Operating Systems

PagedAttention applies classical OS virtual memory concepts to KV cache management.

#### OS Virtual Memory Principles
- **Paging**: Divide memory into fixed-size pages
- **Non-contiguous allocation**: Pages need not be contiguous
- **Dynamic mapping**: Virtual→physical address translation
- **Efficient sharing**: Share pages across processes

### PagedAttention Mechanism

#### KV Cache Partitioning
```
Traditional: [K_0, K_1, K_2, ..., K_n, V_0, V_1, V_2, ..., V_n]
             (must be contiguous)

PagedAttention: [Page 1: K_0-K_7, V_0-V_7]
                [Page 2: K_8-K_15, V_8-V_15]
                [Page 3: K_16-K_23, V_16-V_23]
                (pages can be non-contiguous)
```

#### Block Structure
- **Block size**: Fixed number of tokens per page (typically 16)
- **Pages**: Logical unit of K, V storage
- **Block table**: Maps logical page→physical memory location
- **Per-request tracking**: Each request has block table

#### Attention Computation
- Standard attention algorithm unchanged
- Iterate through pages instead of contiguous memory
- Block table translates logical→physical addresses
- Seamless to attention kernel

### Benefits of Paging

#### 1. Near-Zero Memory Waste
- Last block of sequence partially filled
- No need for contiguous pre-allocation
- Share incomplete pages across requests
- Flexible, fine-grained memory management

#### 2. Flexible Sharing
- **Prefix sharing**: Multiple requests share prompt KV blocks
- **Beam search**: Hypotheses share partial KV cache
- **Batching**: Interleave blocks from different sequences
- **Dynamic scheduling**: Reuse freed blocks immediately

#### 3. Efficient Memory Utilization
- On-demand allocation
- Fragmentation-free design
- Blocks allocated from free pool
- Enables larger effective batch sizes

## Implementation: vLLM

### vLLM Architecture

#### Components
1. **Attention kernel**: Modified for paged access
2. **Memory manager**: Block allocation/deallocation
3. **Request scheduler**: Batch composition
4. **Block table**: Per-request page mapping

#### Memory Manager Responsibilities
- Maintain free block pool
- Allocate blocks on demand
- Track block ownership
- Handle block eviction (if needed)

#### Attention Kernel Modifications
- Accept block table as parameter
- Translate logical→physical block indices
- Scatter-gather for non-contiguous blocks
- Standard attention computation on scattered blocks

### Scheduling Strategy

#### Iteration-Level Scheduling
1. **Prefill phase**: Process all new tokens in batch
2. **Decode phase**: Generate one token per request
3. **Block allocation**: Allocate as needed per request
4. **Adaptive batching**: Adjust batch composition dynamically

#### Scheduling Decisions
- Which requests to include in next batch?
- When to start new requests vs. continue existing?
- How to manage memory pressure?
- Trade-off latency vs. throughput

## Performance Results

### Throughput Improvements

#### Comparison with Baselines
- **vs. FasterTransformer**: 2-4× throughput improvement
- **vs. Orca**: 2-4× throughput improvement
- **Improvements grow with sequence length**: More benefit for long contexts
- **Improvements grow with batch size**: More benefit for large batches

### Latency Characteristics

#### Time-to-First-Token (TTFT)
- Time from request arrival to first generated token
- Faster batch processing → shorter TTFT
- Improved by better memory utilization

#### Inter-token Latency
- Time between consecutive generated tokens
- More stable with vLLM
- Consistent regardless of batch size

### Real-World Impact

| Configuration | Throughput | Improvement |
|---------------|-----------|-------------|
| Llama-7B, batch 8 | High | 2.5-3× |
| Llama-13B, batch 8 | High | 2.5-3× |
| Llama-7B, batch 32 | Very High | 3-4× |
| Long sequences (2K) | Very High | 4× |

### Model Coverage
- **LLaMA** (Meta)
- **Mistral** (Mistral AI)
- **OPT** (Meta)
- **Falcon** (TII)
- Any standard transformer

## Practical Advantages

### For System Developers
1. Attention kernel becomes more manageable
2. Memory fragmentation eliminated
3. Flexible scheduling opportunities
4. Easier to reason about memory

### For Users
1. Higher throughput on same hardware
2. Lower latency for large batches
3. Support for longer sequences
4. Better resource utilization

### For Hardware Vendors
1. More efficient memory utilization
2. Better GPU utilization rates
3. Compelling use case for GPU upgrades
4. Foundation for future optimizations

## Integration with Other Techniques

### Combining with Quantization
- PagedAttention + KV cache quantization
- Paging helps both reduce memory
- Complementary optimizations

### Combining with Eviction Policies
- PagedAttention as foundation
- Token eviction on top of paging
- H2O, Scissorhands work with PagedAttention

### Combining with Compression
- Token merging integrates with paging
- Block-level compression strategies
- Nested optimization opportunities

## Comparison with vAttention (2024)

### vAttention Alternative Approach
**Title**: vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention
**Authors**: Microsoft Research
**arXiv**: [https://arxiv.org/html/2405.04437v1](https://arxiv.org/html/2405.04437v1)
**GitHub**: [https://github.com/microsoft/vattention](https://github.com/microsoft/vattention)

#### Key Differences
- **Approach**: OS demand paging vs. explicit block management
- **Implementation**: System-level paging vs. application-level
- **Kernel modification**: Minimal required
- **Performance**: 1.97× faster token generation vs. vLLM
- **Trade-offs**: Different design decisions

#### vAttention Benefits
- **Kernel simplicity**: Less kernel modification needed
- **System leverage**: Uses OS demand paging
- **Flexibility**: Dynamic physical allocation
- **Prompt processing**: 3.92× faster than PagedAttention FlashAttention

---

## Industry Impact and Adoption

### vLLM Ecosystem
- **De facto standard** for LLM serving
- **Industry adoption**: Used by major LLM providers
- **Open source**: MIT license, active development
- **Framework integration**: PyTorch, HuggingFace compatibility

### Research Impact
- **Foundation for subsequent work**: PagedAttention variants
- **Standard comparison baseline**: Benchmarked in many papers
- **Scheduling optimization**: Launched research direction
- **Memory management**: Inspiration for other systems

### Production Deployment
- **Major cloud providers**: Integrated in commercial offerings
- **Research labs**: Standard tool for LLM serving research
- **Open-source projects**: Community adoption

## Extensions and Variations

### PagedEviction
**Title**: PagedEviction: Structured Block-wise KV Cache Pruning
**URL**: [https://arxiv.org/pdf/2509.04377](https://arxiv.org/pdf/2509.04377)
**Innovation**: Token eviction at block granularity with PagedAttention

### Future Directions
1. **Adaptive block sizing**: Dynamic block size per request
2. **Cross-request optimization**: Better prefix sharing
3. **Speculative execution**: Prefetch blocks speculatively
4. **Hardware co-design**: GPU support for paging
5. **Tiered memory**: CPU-GPU memory hierarchy

---

## Key Takeaways

1. **Virtual memory principle**: OS concepts apply to ML systems
2. **Memory efficiency**: Near-zero waste through paging
3. **Sharing benefits**: Prefix sharing and beam search
4. **Practical impact**: 2-4× throughput on real workloads
5. **Industry standard**: De facto solution for LLM serving
6. **Foundation**: Enables further optimizations (quantization, eviction)

---

**Sources Referenced**:
- [https://arxiv.org/abs/2309.06180](https://arxiv.org/abs/2309.06180)
- [https://dl.acm.org/doi/10.1145/3600006.3613165](https://dl.acm.org/doi/10.1145/3600006.3613165)
- [https://blog.vllm.ai/2023/06/20/vllm.html](https://blog.vllm.ai/2023/06/20/vllm.html)
- [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm)
- [https://arxiv.org/html/2405.04437v1](https://arxiv.org/html/2405.04437v1) (vAttention)

**Generated**: January 27, 2026
**Status**: Literature Review Data Collection
