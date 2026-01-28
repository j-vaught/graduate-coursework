# Dynamic Memory Management for LLM Inference

## Overview
Dynamic memory management systems address the challenge of allocating and deallocating KV cache memory in response to variable sequence lengths and batch compositions during LLM inference.

---

## PagedAttention and Memory Managers

### Covered In-Depth In: `06_pagedattention_vllm.md`

PagedAttention is the dominant dynamic memory management approach.

#### Key Characteristics
- **Virtual memory principle**: OS paging concepts applied to KV cache
- **Block-based allocation**: Fixed-size blocks instead of contiguous sequences
- **On-demand allocation**: Allocate blocks as tokens generated
- **Flexible sharing**: Multiple requests share block pools
- **Near-zero waste**: Minimal fragmentation

#### Memory Management Components
1. **Free block pool**: Available blocks for allocation
2. **Block table**: Per-request logical→physical mapping
3. **Request queue**: Pending and active requests
4. **Eviction policy**: Unused block recovery (if needed)

---

## vAttention: OS-Level Demand Paging

### Paper Overview
**Title**: vAttention: Dynamic Memory Management for Serving LLMs without PagedAttention
**Authors**: Microsoft Research
**Year**: 2024
**Venue**: ASPLOS 2025 (ACM International Conference on Architectural Support for Programming Languages and Operating Systems, Volume 1)
**URLs**:
- arXiv: [https://arxiv.org/html/2405.04437v1](https://arxiv.org/html/2405.04437v1)
- ACM DL: [https://dl.acm.org/doi/10.1145/3669940.3707256](https://dl.acm.org/doi/10.1145/3669940.3707256)
- MS Research: [https://www.microsoft.com/en-us/research/publication/vattention-dynamic-memory-management-for-serving-llms-without-pagedattention/](https://www.microsoft.com/en-us/research/publication/vattention-dynamic-memory-management-for-serving-llms-without-pagedattention/)
- GitHub: [https://github.com/microsoft/vattention](https://github.com/microsoft/vattention)

### Core Insight

**Alternative to PagedAttention**: Use OS-level demand paging instead of application-level paging.

#### Problem with PagedAttention
1. **Kernel modification**: Requires custom attention kernels
2. **Complexity**: Developers must handle paging logic
3. **Overhead**: Block management adds complexity
4. **Maintenance**: Custom kernels need updates

### vAttention Approach

#### Key Principle
Leverage **operating system support for demand paging** instead of implementing paging in application.

#### Design
```
Standard: Contiguous KV cache → Non-contiguous (PagedAttention)
vAttention: Contiguous KV cache → Contiguous virtual memory with OS paging
```

#### How It Works
1. **Virtual memory**: Keep KV cache in virtual memory address space
2. **Demand paging**: OS brings pages to physical memory on access
3. **Transparent to kernel**: Attention kernel sees contiguous memory
4. **Implicit paging**: OS handles physical allocation
5. **Lazy allocation**: Physical pages allocated only when accessed

### Advantages Over PagedAttention

#### 1. Kernel Simplicity
- **No kernel rewriting**: Standard attention implementations work
- **No block management**: OS handles physical allocation
- **Compatibility**: Works with existing kernels
- **Maintenance**: No custom CUDA code needed

#### 2. System Leverage
- **OS support**: Modern systems support demand paging
- **Existing infrastructure**: Proven, well-tested mechanism
- **GPU memory**: Some GPUs support virtual memory and demand paging
- **Future-ready**: Aligns with hardware evolution

#### 3. Performance Trade-offs
- **Contiguity**: Virtual memory appears contiguous
- **Simplicity**: Cleaner implementation
- **Paging overhead**: Demand paging has minor overhead
- **Benefits**: Worth the overhead for most scenarios

### Performance Results

#### Compared to PagedAttention Variants
- **Token generation**: 1.97× faster than vLLM
- **Prompt processing**:
  - 3.92× faster than FlashAttention variant
  - 1.45× faster than FlashInfer variant
- **End-to-end**: Consistent improvements

#### Memory Efficiency
- **Same as PagedAttention**: Near-zero waste
- **Simplified management**: Less memory overhead for bookkeeping
- **Scalability**: Handles large models efficiently

#### Practical Deployment
- Works with existing inference systems
- Minimal changes to codebase
- Strong compatibility

### Implementation Challenges

#### GPU Memory Support
- **GPU capabilities**: Not all GPUs have unified virtual memory
- **Host memory**: CPU-side memory also manageable
- **Limitations**: Some hardware doesn't support demand paging
- **Future**: Improving with newer GPU architectures

#### Page Size Tuning
- **Trade-off**: Larger pages → fewer faults, more memory
- **Optimal**: 64KB-4MB typically best
- **Workload-dependent**: Performance varies with access pattern

---

## eLLM: Elastic Memory Management

### Paper Overview
**Title**: eLLM: Elastic Memory Management Framework for Efficient LLM Serving
**Status**: Recent work (2024-2025)
**arXiv**: [https://arxiv.org/html/2506.15155v1](https://arxiv.org/html/2506.15155v1)

### Concept: Elastic Memory

**Elastic memory**: Dynamically adjust memory allocation based on changing requirements.

#### Characteristics
- **Dynamic adjustment**: Real-time memory reallocation
- **Workload-aware**: Adapt to request patterns
- **Cost optimization**: Minimize memory usage for target throughput
- **Quality-awareness**: Preserve model quality

### Key Features
1. **Monitoring**: Track memory usage patterns
2. **Prediction**: Forecast future memory needs
3. **Adaptation**: Adjust allocation strategy
4. **Fallback**: Gracefully degrade if memory insufficient

---

## Entropy-Guided KV Cache Budget Allocation

### Paper Overview
**Title**: Entropy-Guided KV Caching for Efficient LLM Inference
**Venue**: MDPI Mathematics (2024)
**URLs**:
- MDPI: [https://www.mdpi.com/2227-7390/13/15/2366](https://www.mdpi.com/2227-7390/13/15/2366)
- PDF: [https://www.researchgate.net/publication/393953496_Entropy-Guided-KV-Caching-for-Efficient-LLM-Inference](https://www.researchgate.net/publication/393953496_Entropy-Guided-KV-Caching-for-Efficient-LLM-Inference)

### Core Innovation

Uses **attention entropy** to allocate KV cache budget dynamically across layers.

#### Entropy Metric
- **Definition**: Shannon entropy of attention weight distribution
- **High entropy**: Broad attention dispersion (needs good cache)
- **Low entropy**: Concentrated attention (can use smaller cache)
- **Computation**: Per-layer entropy from attention heads

#### Budget Allocation Strategy
```
For each layer:
  entropy = compute_attention_entropy()
  if entropy > high_threshold:
    cache_budget[layer] = full_budget
  elif entropy > low_threshold:
    cache_budget[layer] = medium_budget
  else:
    cache_budget[layer] = reduced_budget
```

### Performance Results

#### Qwen3 4B Model
- **Memory reduction**: 4.18% with ROUGE preservation
- **Quality**: Maintains benchmark performance
- **Trade-off**: Minimal quality loss for memory savings

#### Mistral 0.1v 7B Model
- **Decoding time**: 46.6% reduction
- **Latency improvement**: Significant speedup
- **Task coverage**: Tested on multiple benchmarks

### Advantages
1. **Layer-aware**: Recognizes different layer requirements
2. **Quality-preserving**: Minimal degradation
3. **Efficiency**: Entropy-based metric effective
4. **Simple**: Straightforward to implement

---

## Prompt Caching: Structured Reuse

### Paper Overview
**Title**: Prompt Cache: Modular Attention Reuse for Low-Latency Inference
**Authors**: Yale University and Google
**Year**: 2024
**Venue**: MLSys 2024
**URLs**:
- Google Research: [https://research.google/pubs/prompt-cache-modular-attention-reuse-for-low-latency-inference/](https://research.google/pubs/prompt-cache-modular-attention-reuse-for-low-latency-inference/)
- arXiv: [https://arxiv.org/abs/2311.04934](https://arxiv.org/abs/2311.04934)
- MLSys 2024: [https://proceedings.mlsys.org/paper_files/paper/2024/file/a66caa1703fe34705a4368c3014c1966-Paper-Conference.pdf](https://proceedings.mlsys.org/paper_files/paper/2024/file/a66caa1703fe34705a4368c3014c1966-Paper-Conference.pdf)
- GitHub: [https://github.com/MachineLearningSystem/24MLSYS-prompt-cache](https://github.com/MachineLearningSystem/24MLSYS-prompt-cache)

### Problem: Redundant Computation

Many prompts contain **common text segments**:
- System messages (repeated across users)
- Prompt templates (standardized structure)
- Context documents (reused in batches)
- Instructions (common across similar tasks)

Each request re-computes attention for these shared segments!

### Solution: Prompt Caching

#### Mechanism
1. **Schema definition**: Explicitly mark reusable prompt segments
2. **Computation**: Pre-compute attention states for segments
3. **Storage**: Cache attention outputs (KV states)
4. **Reuse**: Fetch cached states when segment appears in new prompt
5. **Assembly**: Combine cached and newly-computed states

#### Example
```
System message: "You are a helpful assistant." [CACHE]
User context: "Document: ...{long document}..." [CACHE]
User query: "Summarize the document." [NEW]

First request: Compute all three components
Subsequent requests: Reuse cached system + context, compute only query
```

### Schema for Caching

#### Prompt Modules
- Explicit markers for cache boundaries
- User-defined reusable segments
- Positional accuracy maintained
- Clear caching policy

### Performance Results

#### Latency Improvement
- **Time-to-first-token (TTFT)**: Dramatic improvement (8-60×)
  - GPU-based: 8× improvement
  - CPU-based: 60× improvement
- **Total latency**: Significant reduction
- **End-to-end**: Preserves output quality

#### Throughput Improvement
- **Batch processing**: More requests served
- **Cost reduction**: Fewer computations per batch
- **Resource usage**: Better GPU utilization

### Practical Benefits

#### Use Cases
1. **Chatbots**: Shared system prompts
2. **RAG systems**: Repeated documents
3. **Multi-turn**: Conversation history
4. **Batch inference**: Common instructions

#### Deployment
- **API services**: OpenAI, Anthropic support prompt caching
- **Self-hosted**: MLSys implementation available
- **Cost**: Reduced compute → reduced billing

---

## Expected Attention: Future Query Prediction

### Paper Overview
**Title**: Expected Attention: KV Cache Compression by Estimating Attention from Future Queries Distribution
**arXiv**: [https://arxiv.org/html/2510.00636v1](https://arxiv.org/html/2510.00636v1)

### Concept

**Predict** which tokens will be important for future queries, compress ahead of time.

#### Approach
1. **Distribution modeling**: Learn query distribution
2. **Expectation**: Compute expected attention patterns
3. **Pre-compression**: Compress low-importance tokens early
4. **Adaptive**: Adjust compression based on predictions

### Benefits
- **Proactive compression**: Evict before actually needed
- **Better decisions**: Use global information
- **Reduced latency**: Less per-token processing

---

## Scheduling and Memory Coordination

### Request Scheduling
Different scheduling strategies interact with memory management:

#### Continuous Batching
- Add new requests as soon as slots available
- Memory allocation dynamic
- Requires flexible memory management
- vLLM pioneered this approach

#### Iteration-Based Batching
- Fixed-size batches, process together
- Memory more predictable
- Simpler management but less flexible

#### Hybrid Scheduling
- Combine approaches based on memory state
- Adapt to workload
- Dynamic memory management needed

### Memory Pressure Handling

When memory runs out:

1. **Eviction**: Remove KV cache for slowest-to-finish request
2. **Pause**: Stop accepting new requests
3. **Compression**: Trigger compression (quantization, eviction)
4. **Graceful degradation**: Reduce batch size

---

## Optimization Frameworks

### Decision Points for Memory Management

| Scenario | Recommended Approach |
|----------|-------------------|
| Batching many short requests | PagedAttention or vAttention |
| Long sequences, few requests | Quantization + streaming |
| Mixed workload | Entropy-guided budget + PagedAttention |
| Real-time/low-latency | Prompt caching |
| Maximum throughput | Combined PagedAttention + eviction |

---

## Key Takeaways

1. **PagedAttention**: Application-level dynamic memory management (standard)
2. **vAttention**: OS-level alternative with simpler kernels
3. **Entropy-guided**: Dynamic layer-wise budget allocation
4. **Prompt caching**: Structured reuse of computation
5. **Expected Attention**: Predictive compression for future queries
6. **Elastic**: Real-time memory adaptation
7. **Combination**: Most effective systems combine multiple techniques

---

**Sources Referenced**:
- [https://arxiv.org/html/2405.04437v1](https://arxiv.org/html/2405.04437v1) (vAttention)
- [https://arxiv.org/html/2506.15155v1](https://arxiv.org/html/2506.15155v1) (eLLM)
- [https://www.mdpi.com/2227-7390/13/15/2366](https://www.mdpi.com/2227-7390/13/15/2366) (Entropy-guided)
- [https://proceedings.mlsys.org/paper_files/paper/2024/file/a66caa1703fe34705a4368c3014c1966-Paper-Conference.pdf](https://proceedings.mlsys.org/paper_files/paper/2024/file/a66caa1703fe34705a4368c3014c1966-Paper-Conference.pdf) (Prompt Cache)
- [https://arxiv.org/html/2510.00636v1](https://arxiv.org/html/2510.00636v1) (Expected Attention)

**Generated**: January 27, 2026
**Status**: Literature Review Data Collection
