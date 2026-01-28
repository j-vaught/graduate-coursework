# Additional KV-Cache Research Papers and Methods

## Long-Context Generalization Methods

### LM-Infinite: Zero-Shot Extreme Length Generalization

**Paper Overview**
**Title**: LM-Infinite: Zero-Shot Extreme Length Generalization for Large Language Models
**Authors**: Han et al.
**Year**: 2023 (arXiv) / 2024 (NAACL publication)
**Venue**: NAACL 2024
**URLs**:
- arXiv: [https://arxiv.org/abs/2308.16137](https://arxiv.org/abs/2308.16137)
- NAACL 2024: [https://aclanthology.org/2024.naacl-long.222/](https://aclanthology.org/2024.naacl-long.222/)
- GitHub: [https://github.com/Glaciohound/LM-Infinite](https://github.com/Glaciohound/LM-Infinite)
- HuggingFace: [https://huggingface.co/papers/2308.16137](https://huggingface.co/papers/2308.16137)

#### Core Method
- **Lambda-shaped attention mask**: Simple geometric attention pattern
- **Distance limit**: Cap attention distance
- **Training-free**: Works with existing models
- **No parameter updates**: Pure inference-time technique

#### Performance
- **Length generalization**: 2K→32K tokens without retraining
- **Memory savings**: 7.5× memory reduction
- **Speed**: 2.7× decoding speedup
- **Quality**: Maintained on downstream tasks (Passkey Retrieval, Qasper)

#### Model Compatibility
- Llama, Llama-2, GPT-J, MPT-7B series
- Pythia models
- Works across diverse architectures

---

### InfLLM: Training-Free Long-Context Extrapolation

**Paper Overview**
**Title**: InfLLM: Training-Free Long-Context Extrapolation for LLMs with an Efficient Context Memory
**Authors**: Xiao Zhang et al. (THUNLP)
**Year**: 2024
**Venue**: NeurIPS 2024, ICML 2024 (oral)
**arXiv ID**: 2402.04617
**URLs**:
- arXiv: [https://arxiv.org/abs/2402.04617](https://arxiv.org/abs/2402.04617)
- NeurIPS 2024: [https://proceedings.neurips.cc/paper_files/paper/2024/file/d842425e4bf79ba039352da0f658a906-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/d842425e4bf79ba039352da0f658a906-Paper-Conference.pdf)
- OpenReview: [https://openreview.net/forum?id=bTHFrqhASY](https://openreview.net/forum?id=bTHFrqhASY)
- GitHub: [https://github.com/thunlp/InfLLM](https://github.com/thunlp/InfLLM)

#### Concept: Memory-Based Long Context Handling
- **Distant context memory**: Separate storage for out-of-window tokens
- **Token-relevant lookup**: Select relevant memory units per query
- **Efficient computation**: Limited context window + smart memory access
- **Training-free**: No fine-tuning required

#### Performance
- **Extreme lengths**: Handles 1,024K (1M) token sequences
- **Quality preservation**: Captures long-distance dependencies
- **Baseline competition**: Comparable to models trained on long sequences
- **No training**: Works with models pre-trained on short windows

#### Key Innovation
Instead of expanding context window (expensive), expand memory units and implement efficient lookup mechanism.

---

## Advanced Attention Mechanisms

### FlashAttention: IO-Aware Exact Attention

**Paper Overview**
**Title**: FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness
**Authors**: Tri Dao, Daniel Y. Fu, Stefano Ermon, Atri Rudra, Christopher Ré
**Year**: 2022
**Venue**: NeurIPS 2022
**arXiv ID**: 2205.14135
**URLs**:
- arXiv: [https://arxiv.org/abs/2205.14135](https://arxiv.org/abs/2205.14135)
- PDF: [https://arxiv.org/pdf/2205.14135](https://arxiv.org/pdf/2205.14135)
- NeurIPS 2022: [https://proceedings.neurips.cc/paper_files/paper/2022/hash/67d57c32e20fd0a7a302cb81d36e40d5-Abstract-Conference.html](https://proceedings.neurips.cc/paper_files/paper/2022/hash/67d57c32e20fd0a7a302cb81d36e40d5-Abstract-Conference.html)
- GitHub: [https://github.com/Dao-AILab/flash-attention](https://github.com/Dao-AILab/flash-attention)

#### Core Innovation: IO-Aware Algorithm
- **Principle**: Account for memory hierarchy (HBM vs. SRAM)
- **Tiling**: Reduce memory reads/writes between GPU levels
- **Exact computation**: Still computes exact attention (not approximation)
- **Hardware optimization**: Minimizes memory movement costs

#### Performance
- **Up to 3× faster**: Standard attention on sequences 128-2K
- **Scales to 64K**: Maintains efficiency for long sequences
- **20× more memory efficient**: Compared to baseline methods
- **Up to sequence length 512**: Both faster AND more memory efficient

#### Impact
- Foundation for subsequent fast attention methods
- Enabled longer sequence training
- Standard in modern frameworks (PyTorch, etc.)

---

### Sparse Attention Mechanisms

**Paper Overview**
**Title**: The Sparse Frontier: Sparse Attention Trade-offs in Transformer LLMs
**Year**: 2024
**arXiv**: [https://arxiv.org/pdf/2504.17768](https://arxiv.org/pdf/2504.17768)

#### Sparse Attention Patterns
- **Sliding window**: Local token context
- **Global tokens**: Fixed set of important tokens
- **Random**: Stochastic connections
- **Block-sparse**: Structured sparsity patterns

#### Effectiveness
- **Computational savings**: Reduce attention complexity
- **Memory efficiency**: Smaller attention matrices
- **Trade-off**: Lose some long-range dependencies
- **Best for**: Specific task types (retrieval, QA)

#### Implementation Challenges
- Custom CUDA kernels needed
- Hardware support varies
- Integration with standard frameworks

---

## Token Management Techniques

### MiniCache: Depth-wise KV Cache Merging

**Paper Overview**
**Title**: MiniCache: KV Cache Compression in Depth Dimension for Large Language Models
**Venue**: NeurIPS 2024
**URLs**:
- NeurIPS 2024: [https://proceedings.neurips.cc/paper_files/paper/2024/file/fd0705710bf01b88a60a3d479ea341d9-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/fd0705710bf01b88a60a3d479ea341d9-Paper-Conference.pdf)

#### Concept: Depth-Dimension Compression
- **Traditional**: Reduce tokens (sequence dimension)
- **MiniCache**: Consolidate states across layers (depth dimension)
- **Mechanism**: Merge KV from multiple layers into shared state
- **Application**: Every N layers, consolidate to single state

#### Benefits
- **Novel dimension**: Different approach than sequence pruning
- **Effectiveness**: Significant memory reduction
- **Complementary**: Works alongside token eviction
- **Quality**: Minimal degradation with proper merging

---

### KVReviver: Reversible KV Cache Compression

**Paper Overview**
**Title**: KVReviver: Reversible KV Cache Compression with Sketch-Based Token Reconstruction
**arXiv ID**: 2512.17917
**URLs**:
- arXiv: [https://arxiv.org/html/2512.17917](https://arxiv.org/html/2512.17917)

#### Innovation: Reversible Compression
- **Trade-off**: Memory vs. computation
- **Mechanism**: Sketch algorithm for compression
- **Reconstruction**: Can regenerate compressed tokens
- **Flexibility**: Choose amount of compression

#### Key Insight
Don't permanently discard tokens—store compressed version for reconstruction if needed.

---

### RocketKV: Two-Stage KV Cache Compression

**Paper Overview**
**Title**: RocketKV: Accelerating Long-Context LLM Inference via Two-Stage KV Cache Compression
**arXiv**: [https://arxiv.org/html/2502.14051v3](https://arxiv.org/html/2502.14051v3)

#### Two-Stage Approach

**Stage 1: Permanent Eviction**
- Determine minimum essential tokens (attention sinks, recent)
- Remove permanently during prefill
- Cannot recover these tokens

**Stage 2: Dynamic Selection**
- Adaptive selection during decoding
- Maintain flexible pool of candidates
- Reselect based on actual queries

#### Optimization
- **Prefill phase**: Optimize with long-horizon knowledge
- **Decode phase**: Adapt to actual query patterns
- **Combined**: Better overall efficiency

---

## Attention Pattern Analysis

### When Attention Sink Emerges (ICLR 2025)

**Paper Overview**
**Title**: When Attention Sink Emerges
**Venue**: ICLR 2025
**URLs**:
- Proceedings: [https://proceedings.iclr.cc/paper_files/paper/2025/file/f1b04face60081b689ba740d39ea8f37-Paper-Conference.pdf](https://proceedings.iclr.cc/paper_files/paper/2025/file/f1b04face60081b689ba740d39ea8f37-Paper-Conference.pdf)

#### Research Questions
- **When**: At what point in training do sinks emerge?
- **Why**: Fundamental reasons for emergence
- **How**: Conditions that promote sink formation
- **Impact**: Implications for model design

#### Key Findings
- Sinks emerge after sufficient training
- Stronger in larger models
- Predictable and learnable phenomenon
- Design implications for future models

---

### Why Do LLMs Attend to the First Token?

**Paper Overview**
**Title**: Why do LLMs attend to the first token?
**arXiv**: [https://arxiv.org/html/2504.02732v1](https://arxiv.org/html/2504.02732v1)

#### Analysis
- Theoretical explanation for attention sink phenomenon
- Mechanistic interpretation
- Why softmax drives initial attention
- Implications for model behavior

---

## Advanced Compression and Merging

### Hold Onto That Thought: KV Cache Compression and Reasoning

**Paper Overview**
**Title**: Hold Onto That Thought: Assessing KV Cache Compression On Reasoning
**arXiv**: [https://arxiv.org/html/2512.12008v1](https://arxiv.org/html/2512.12008v1)

#### Focus: Reasoning Task Sensitivity
- **Key finding**: Compression affects reasoning disproportionately
- **Task dependency**: QA robust, reasoning brittle
- **Analysis**: Which compression methods preserve reasoning?
- **Guidance**: Selecting compression for different tasks

#### Implications
- Task-specific compression strategy needed
- Not all compression equal for all use cases
- Reasoning particularly important to preserve

---

### The Pitfalls of KV Cache Compression

**Paper Overview**
**Title**: The Pitfalls of KV Cache Compression
**arXiv**: [https://arxiv.org/pdf/2510.00231](https://arxiv.org/pdf/2510.00231)

#### Critical Analysis
- Empirical examination of compression limitations
- When compression fails
- Distribution shift issues
- Out-of-domain behavior

#### Lessons
- Compression not universal solution
- Context-dependent effectiveness
- Need for careful evaluation
- Task and model specific

---

## Specialized Inference Optimizations

### KITTY: Accurate and Efficient 2-Bit KV Cache Quantization

**Paper Overview**
**Title**: KITTY: Accurate and Efficient 2-Bit KV Cache Quantization with Information Theory-Guided Token-wise Clustering
**arXiv**: [https://arxiv.org/pdf/2511.18643](https://arxiv.org/pdf/2511.18643)

#### Innovation: Information Theory
- Theoretical foundation for quantization
- Token-wise clustering approach
- Improved 2-bit accuracy
- Information-theoretic guarantees

---

### Reviving Efficient Attention for Long Context Language

**Paper Overview**
**Title**: Reviving Efficient Attention for Long Context Language Modeling
**Year**: 2024
**Venue**: IJCAI
**URL**: [https://www.ijcai.org/proceedings/2024/0904.pdf](https://www.ijcai.org/proceedings/2024/0904.pdf)

#### Approach: Re-examine Sparse Attention
- Efficient attention for long context
- When sparse attention effective
- Modern optimization opportunities
- Practical implementation

---

## Industry/Practical Papers

### NVIDIA Technical Blog: KV Cache Offload

**Title**: Accelerate Large-Scale LLM Inference and KV Cache Offload with CPU-GPU Memory Sharing
**URL**: [https://developer.nvidia.com/blog/accelerate-large-scale-llm-inference-and-kv-cache-offload-with-cpu-gpu-memory-sharing/](https://developer.nvidia.com/blog/accelerate-large-scale-llm-inference-and-kv-cache-offload-with-cpu-gpu-memory-sharing/)

#### Topics
- CPU-GPU memory coordination
- KV cache offloading strategies
- Practical deployment considerations
- Hardware-software co-design

---

### LLM Inference Handbook

**Title**: KV Caching in LLM Inference A Comprehensive Review
**Author**: Rohan Paul
**URL**: [https://www.rohan-paul.com/p/kv-caching-in-llm-inference-a-comprehensive](https://www.rohan-paul.com/p/kv-caching-in-llm-inference-a-comprehensive)

#### Coverage
- Comprehensive KV cache overview
- Multiple optimization techniques
- Practical considerations
- Benchmark comparisons

---

## Summary Table: All Methods

| Method | Type | Memory Reduction | Quality Impact | Requirement |
|--------|------|-----------------|----------------|-------------|
| KIVI | Quantization | 2.6× | Minimal | None |
| KVQuant | Quantization | 4-10× | <0.1 PPL | None |
| H2O | Eviction | 2-4× | Medium | None |
| Scissorhands | Eviction | 2-4× | Medium | None |
| FastGen | Eviction | 2-4× | Low | None |
| HashEvict | Eviction | 2-3× | Low | None |
| GQA | Architecture | 2-8× | Minimal | Uptraining |
| MQA | Architecture | 8-16× | Medium | Training |
| PagedAttention | Management | 2-3× | None | Framework |
| vAttention | Management | 2-3× | None | OS support |
| YOCO | Architecture | 4× | Minimal | Architecture change |
| LCKV | Sharing | 2-3× | Low | Uptraining |
| SqueezeAttention | Sharing | 2-3× | Low | None |
| LM-Infinite | Attention mask | 2-3× | Low | None |
| InfLLM | Memory-based | 2-4× | Low | None |
| FlashAttention | Kernel | 1.3-3× | None | Hardware |
| Prompt Cache | Reuse | 2-10× | None | Schema |

---

**Key Reference Collections**:
- [GitHub: Awesome KV-Cache Compression](https://github.com/October2001/Awesome-KV-Cache-Compression)
- Cold-Compress toolkit: [https://www.answer.ai/posts/2024-08-01-cold-compress.html](https://www.answer.ai/posts/2024-08-01-cold-compress.html)

**Generated**: January 27, 2026
**Status**: Literature Review Data Collection
