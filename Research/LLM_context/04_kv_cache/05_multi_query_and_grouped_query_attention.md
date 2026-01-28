# Multi-Query Attention and Grouped-Query Attention

## Part 1: Multi-Query Attention (MQA)

### Paper Overview
**Title**: Fast Transformer Decoding: One Write-Head is All You Need
**Authors**: Noam Shazeer (Google)
**Year**: 2019
**arXiv ID**: 1911.02150
**URLs**:
- arXiv: [https://arxiv.org/abs/1911.02150](https://arxiv.org/abs/1911.02150)
- PDF: [https://arxiv.org/pdf/1911.02150](https://arxiv.org/pdf/1911.02150)
- HuggingFace: [https://huggingface.co/papers/1911.02150](https://huggingface.co/papers/1911.02150)

### Core Problem

During **incremental decoding** (autoregressive generation), memory bandwidth becomes the bottleneck.

#### Why Standard Multi-Head Attention (MHA) is Slow
- Repeatedly loads large "keys" and "values" tensors
- Memory-bandwidth cost dominates computation time
- Per-token generation becomes I/O bound
- High memory footprint for K and V projections

### Key Innovation: Shared KV Heads

**Multi-Query Attention**: A single set of keys and values are shared across all attention heads.

#### Mechanism
```
Standard MHA:    Q_h1, Q_h2, ..., Q_h_n  →  K_h1, K_h2, ..., K_h_n (separate)
                                              V_h1, V_h2, ..., V_h_n (separate)

MQA:             Q_h1, Q_h2, ..., Q_h_n  →  K (shared across heads)
                                              V (shared across heads)
```

#### Benefits
- **Reduced memory**: Single K, V vs. H copies (H = number of heads)
- **Reduced bandwidth**: Load K, V once per token
- **Faster decoding**: Less memory-bound computation

### Performance Results

#### Decoding Speed
- **Significantly faster** incremental decoding
- **Minimal quality degradation** from baseline MHA
- Trade-off: Slight decrease in model quality for substantial speedup

#### Memory Reduction
For typical model configurations:
- **Single KV copy** instead of per-head copies
- **Substantial bandwidth reduction** (8-16× typical head counts)
- **Proportional speedup** in memory-bound operations

### Model Adoption

#### Early Adopters
- **Llama-2**: Meta adopted MQA
- **Falcon**: TII incorporated multi-query attention
- Later superseded by GQA in most models

---

## Part 2: Grouped-Query Attention (GQA)

### Paper Overview
**Title**: GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints
**Authors**: Joshua Ainslie, James Lee-Thorp, et al. (Google)
**Year**: 2023
**Venue**: EMNLP 2023
**arXiv ID**: 2305.13245
**URLs**:
- arXiv: [https://arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245)
- EMNLP 2023: [https://aclanthology.org/2023.emnlp-main.298/](https://aclanthology.org/2023.emnlp-main.298/)
- PDF: [https://arxiv.org/pdf/2305.13245](https://arxiv.org/pdf/2305.13245)
- Semantic Scholar: [https://www.semanticscholar.org/paper/GQA:-Training-Generalized-Multi-Query-Transformer-Ainslie-Lee-Thorp/5ae6fb6b5a3c7df515ff4a82ac9673bae6a8e200](https://www.semanticscholar.org/paper/GQA:-Training-Generalized-Multi-Query-Transformer-Ainslie-Lee-Thorp/5ae6fb6b5a3c7df515ff4a82ac9673bae6a8e200)

### Core Innovation

**Grouped-Query Attention**: Intermediate number of KV heads between MHA and MQA.

#### Mechanism
```
MHA: H query heads, H key heads, H value heads
MQA: H query heads, 1 key head,  1 value head

GQA: H query heads, G key heads, G value heads (1 < G < H)
     where each group of Q heads shares one KV pair
```

#### Design Rationale
- **Balance efficiency and quality**: Trade-off sweet spot between MHA and MQA
- **Uptraining from MHA**: Convert existing MHA models to GQA
- **Scalability**: Group heads intelligently to maintain quality

### Technical Approach

#### Uptraining Recipe
- **Cost**: Only 5% of original pre-training compute
- **Source**: Multi-head attention checkpoints
- **Target**: Multi-query or grouped-query attention
- **Mechanism**: Knowledge transfer from MHA → GQA/MQA

#### Group Configuration
- **Number of groups**: G is hyperparameter (typically 4-8)
- **Queries per group**: H/G query heads per KV head
- **Flexibility**: Different group sizes for different models

### Performance Results

#### Quality Metrics
- **GQA achieves quality close to MHA**
- **Speed comparable to MQA**
- **Sweet spot** in efficiency-quality trade-off

#### Comparison on Benchmarks
| Metric | MHA | GQA | MQA |
|--------|-----|-----|-----|
| Quality | High | High | Medium |
| Speed | Slow | Fast | Very Fast |
| KV Memory | High | Medium | Low |
| Bandwidth | High | Medium | Low |

#### Real-World Impact
- Enables larger batch sizes
- Faster inference latency
- Reduced KV cache memory

### KV Cache Memory Reduction Example

#### Llama 3 8B Model
- **With MHA**: 280 GB KV cache (OOM on many systems)
- **With GQA**: ~70 GB KV cache (fits on consumer GPUs)
- **Reduction**: **75% memory savings**

### Industrial Adoption Timeline

#### 2023
- **May 2023**: Paper publication (arXiv)
- **July 2023**: Meta adopted for Llama-2
- **September 2023**: Mistral AI used in Mistral-7B

#### 2024
- **January**: Llama-3 with GQA
- **Widespread**: Standard in new model releases
- **De facto**: Industry-wide adoption for efficient inference

### Relationship to Uptraining

#### Why Uptraining Matters
1. **Reuse existing checkpoints**: No need to retrain from scratch
2. **Low cost**: 5% of original compute
3. **Fast deployment**: Rapid conversion to efficient models
4. **Knowledge transfer**: Leverage MHA model knowledge

#### Uptraining Process
1. Initialize GQA model from MHA checkpoint
2. Fine-tune with grouped head sharing
3. Minimal additional training needed
4. Excellent convergence properties

---

## Attention Mechanism Comparison

### Standard Multi-Head Attention (MHA)
```
Attention(Q, K, V) = softmax(QK^T/√d)V

With H attention heads (independent):
- H query projections: Q_1, ..., Q_H
- H key projections: K_1, ..., K_H
- H value projections: V_1, ..., V_H
- Each head: Attention(Q_i, K_i, V_i)
```

### Multi-Query Attention (MQA)
```
Attention with shared K, V:
- H query projections: Q_1, ..., Q_H
- 1 shared key projection: K
- 1 shared value projection: V
- Each head: Attention(Q_i, K, V)
```

### Grouped-Query Attention (GQA)
```
Attention with grouped K, V:
- H query projections: Q_1, ..., Q_H
- G key projections: K_1, ..., K_G (where G < H)
- G value projections: V_1, ..., V_G
- Groups: Q_{(i-1)*H/G + 1} to Q_{i*H/G} share K_i, V_i
```

---

## Implementation Considerations

### GQA Implementation
- **Straightforward modification**: Standard attention kernels
- **Backward compatible**: Drop-in replacement for MHA
- **Hardware efficient**: No special CUDA kernels required
- **Framework support**: PyTorch, TensorFlow, etc.

### Uptraining Implementation
1. Reshape weight matrices
2. Average or interpolate for group sharing
3. Fine-tune with standard training

---

## Comparison with Other KV Reduction Methods

| Method | Technique | Memory Reduction | Quality | Training |
|--------|-----------|-----------------|---------|----------|
| MQA | Sharing | ~8-16× | Slight loss | Training-free |
| GQA | Grouped sharing | ~2-8× | Minimal loss | Uptraining required |
| KV Quantization | Precision reduction | ~4-8× | Minimal loss | Training-free |
| Token eviction | Selection | ~2-4× | Medium loss | Training-free |

---

## Research Follow-ups

### Related Work Using GQA
- **Llama-3** (2024): GQA as standard
- **Mistral** models: GQA incorporation
- **Open-source models**: GQA adoption trend

### Theoretical Questions
- Optimal group count selection
- Why does uptraining work so well?
- Head specialization in groups
- Quality-efficiency trade-off analysis

---

## Practical Guidance

### When to Use MQA
- Maximum speed priority
- Acceptable quality degradation
- Streaming/edge deployment
- Small model size

### When to Use GQA
- Balanced efficiency-quality
- Standard production inference
- Large model deployment
- Converting from MHA models

### When to Use MHA
- Quality critical
- Sufficient memory/bandwidth
- Fine-tuning or adaptation
- Research/exploration

---

## Key Takeaways

1. **MQA (2019)**: Pioneer method, significant speedups, quality trade-off
2. **GQA (2023)**: Balanced approach, uptraining recipe, industry standard
3. **Adoption**: GQA now default in new model releases
4. **Impact**: Major component of modern efficient LLM serving
5. **Combination**: GQA + quantization for maximum efficiency

---

**Sources Referenced**:
- [https://arxiv.org/abs/1911.02150](https://arxiv.org/abs/1911.02150) (MQA)
- [https://arxiv.org/abs/2305.13245](https://arxiv.org/abs/2305.13245) (GQA)
- [https://aclanthology.org/2023.emnlp-main.298/](https://aclanthology.org/2023.emnlp-main.298/)
- [https://www.ibm.com/think/topics/grouped-query-attention](https://www.ibm.com/think/topics/grouped-query-attention)

**Generated**: January 27, 2026
**Status**: Literature Review Data Collection
