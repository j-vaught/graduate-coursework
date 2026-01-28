# Cross-Layer KV Sharing and Layer-Wise Optimization

## Overview
Cross-layer KV sharing exploits the observation that different transformer layers have different sensitivity to input tokens. By sharing KV cache across layers, we can significantly reduce memory while maintaining quality.

---

## Cross-Layer KV Sharing Framework

### Paper Overview
**Title**: A Systematic Study of Cross-Layer KV Sharing for Efficient LLM Inference
**Venue**: NAACL 2025 (short paper)
**Year**: 2024
**arXiv ID**: 2410.14442
**URLs**:
- arXiv: [https://arxiv.org/abs/2410.14442](https://arxiv.org/abs/2410.14442)
- ACL Anthology: [https://aclanthology.org/2025.naacl-short.34/](https://aclanthology.org/2025.naacl-short.34/)
- PDF: [https://aclanthology.org/2025.naacl-short.34.pdf](https://aclanthology.org/2025.naacl-short.34.pdf)
- HuggingFace: [https://huggingface.co/papers/2410.14442](https://huggingface.co/papers/2410.14442)

### Core Insight

**Not all layers need independent KV caches.**

Different layers in transformers have different roles:
- **Early layers**: Focus on local patterns, word-level processing
- **Middle layers**: Aggregate information, capture semantic patterns
- **Late layers**: Make high-level decisions, final predictions

These different roles suggest layers can efficiently share KV caches.

### Unified Framework

The paper proposes a unified framework covering several cross-layer methods:

1. **Cross-Layer Attention (CLA)**
2. **Layer-Condensed KV (LCKV)**
3. **YOCO** (You Only Cache Once)
4. **Other variants**

---

## Method 1: Cross-Layer Attention (CLA)

### Architecture
Uniformly divides transformer layers into multiple groups.

#### Group Structure
```
Group 1: Layers 1-4
  - L1-L4 self-attention: Query → KV cache from bottom layer (L1)
  - All query heads use shared KV from L1

Group 2: Layers 5-8
  - L5-L8 self-attention: Query → KV cache from bottom layer (L5)
  - All query heads use shared KV from L5

...
```

#### Key Features
- **Uniform grouping**: Fixed number of layers per group
- **Bottom-layer sharing**: Use lowest layer's KV in group
- **Training-free**: Can work with pretrained models
- **Simple implementation**: Straightforward modification

### Performance
- **Memory reduction**: 2× typical KV cache
- **Quality trade-off**: Small performance degradation
- **Best for**: Larger KV cache reductions
- **Limitation**: Uniform grouping may be suboptimal

---

## Method 2: Layer-Condensed KV (LCKV)

### Paper/Repository
**GitHub**: [https://github.com/whyNLP/LCKV](https://github.com/whyNLP/LCKV)
**Status**: Accepted to ACL 2024

### Architecture
More sophisticated sharing that conditions on layer position.

#### Key Characteristics
- **Adaptive sharing**: Different layers share differently
- **Training involved**: Requires some fine-tuning or uptraining
- **Better quality**: Less performance loss than CLA
- **10× batch size**: Enables much larger batches

### Performance Metrics
- **Throughput**: Dramatic speed improvement
- **Parameters**: Fewer parameters due to shared KV
- **Computation**: Less computation during inference
- **Task performance**: Competitive with baseline

### Advantages Over CLA
1. **Adaptive**: Tunes sharing per layer
2. **Better quality**: Less performance degradation
3. **Flexible**: Can adjust sharing granularity
4. **Scalable**: Works across model sizes

---

## Method 3: YOCO - You Only Cache Once

### Paper Overview
**Title**: You Only Cache Once: Decoder-Decoder Architectures for Language Models
**Year**: 2024
**Venue**: NeurIPS 2024
**arXiv ID**: 2405.05254
**URLs**:
- arXiv: [https://arxiv.org/abs/2405.05254](https://arxiv.org/abs/2405.05254)
- OpenReview: [https://openreview.net/forum?id=25Ioxw576r](https://openreview.net/forum?id=25Ioxw576r)
- HuggingFace: [https://huggingface.co/papers/2405.05254](https://huggingface.co/papers/2405.05254)
- NeurIPS Poster: [https://neurips.cc/virtual/2024/poster/96833](https://neurips.cc/virtual/2024/poster/96833)

### Core Concept

YOCO replaces standard transformer architecture with a **decoder-decoder architecture**.

#### Standard Transformer
```
Self-Decoder (all L layers)
  - Self-attention only
  - Token attends to all previous tokens
  - Single KV cache
```

#### YOCO Architecture
```
Self-Decoder (L/2 layers)
  - Self-attention
  - Encodes tokens efficiently
  - Produces global KV cache

Cross-Decoder (L/2 layers)
  - Cross-attention only
  - Attends to self-decoder outputs
  - Reuses global KV cache (efficient)
```

### Key Innovation: Single KV Cache

Instead of **L layers × N tokens** KV cache, YOCO maintains:
- Self-decoder: Temporary cache for efficient encoding
- Cross-decoder: Single global KV cache reused by all layers
- **Result**: O(N) memory instead of O(N×L)

#### Memory Scaling
```
Standard Transformer: KV_memory = O(N × L)
YOCO: KV_memory = O(N)

Where N = sequence length, L = number of layers
```

### Architecture Details

#### Split Configuration
- **First L/2 layers**: Self-decoder with self-attention
- **Last L/2 layers**: Cross-decoder with cross-attention
- **KV generation**: Self-decoder produces efficient representation
- **KV reuse**: Cross-decoder uses same KV cache across all layers

#### Computation Flow
```
Input tokens
  ↓
Self-Decoder (Layers 1-L/2)
  - Self-attention on tokens
  - Generates context representation
  ↓
Global KV Cache (from self-decoder output)
  ↓
Cross-Decoder (Layers L/2+1-L)
  - Cross-attention to global KV
  - All layers share same KV
  ↓
Output tokens
```

### Performance Results

#### Memory Efficiency
- **O(N) scaling**: Linear memory growth (not N×L)
- **Practical savings**: 2-4× reduction vs. standard transformer
- **Long contexts**: Enables 1M token inference

#### Inference Latency
- **Prefill stage**: Early-exit capability (faster prefill)
- **Decode stage**: Reduced cache access
- **Overall**: Competitive with standard transformers

#### Quality Preservation
- **Training required**: Needs training from scratch or uptraining
- **Benchmark performance**: Favorable comparison with transformers
- **Scaling**: Maintains quality when scaled up

### Advantages
1. **Fundamental efficiency**: Architectural change, not just optimization
2. **Unlimited context**: Theoretically supports any sequence length
3. **Parallelization**: Cross-decoder layers can partially parallelize
4. **Future-proof**: Works with other optimizations

### Limitations
1. **Training requirement**: Can't convert existing models easily
2. **Architecture change**: Significant departure from standard transformer
3. **Hardware support**: Needs compatible attention implementation
4. **Research maturity**: Newer approach, less ecosystem support

---

## SqueezeAttention: 2D Layer-wise Budget Allocation

### Paper Overview
**Title**: SqueezeAttention: 2D Management of KV-Cache in LLM Inference via Layer-wise Optimal Budget
**Year**: 2024
**Venue**: ICLR 2025
**arXiv ID**: 2404.04793
**URLs**:
- arXiv: [https://arxiv.org/abs/2404.04793](https://arxiv.org/abs/2404.04793)
- OpenReview: [https://openreview.net/forum?id=9HK2rHNAhd](https://openreview.net/forum?id=9HK2rHNAhd)
- GitHub: [https://github.com/hetailang/SqueezeAttention](https://github.com/hetailang/SqueezeAttention)
- ICLR 2025: [https://proceedings.iclr.cc/paper_files/paper/2025/hash/3b0a8df568ec496a717566a7f8158aaa-Abstract-Conference.html](https://proceedings.iclr.cc/paper_files/paper/2025/hash/3b0a8df568ec496a717566a7f8158aaa-Abstract-Conference.html)

### Approach: Two-Dimensional Optimization

Traditional methods optimize only **sequence dimension** (which tokens to keep).

SqueezeAttention optimizes **both dimensions**:
1. **Sequence dimension**: Which tokens to keep (existing methods)
2. **Layer dimension**: How much cache per layer (novel)

### Layer Importance Measurement

#### Cosine Similarity Metric
- Compute input difference: Δx = x_in(L) - x_in(L-1)
- Measure output effect: Δy = y_out - y_out_no_attention
- Layer importance: 1 - cosine_similarity(Δx, Δy)
- **Interpretation**: Layers that preserve input better are less important

#### Importance Categories
- **Important layers**: Significantly transform input
- **Unimportant layers**: Pass through relatively unchanged
- **Classification**: Binary or multi-level importance

### Budget Reallocation Strategy

#### Initial Budget
- Assume total KV cache size = 100 units
- Uniform distribution: Each layer gets (100/L) units

#### Importance-based Reallocation
```
For each layer L:
  importance_score = compute_importance(L)
  if importance_score < threshold:
    budget[L] = reduced_budget
  else:
    budget[L] = normal_budget

Redistribute freed budget to important layers
```

#### Hyperparameter
- **Adjustment factor**: Control % of budget to reduce
- **Threshold**: Determines which layers are "unimportant"
- **Trade-off**: More aggressive = more memory saved

### Performance Results

#### Memory Reduction
- **30-70% reduction**: In various configurations
- **Flexible targeting**: Achieve specific reduction goals
- **Quality preservation**: Minimal performance loss

#### Throughput Improvement
- **2.2× speedup**: Best cases
- **Consistent gains**: Across different model sizes
- **Scalability**: Works on various LLMs

#### Model Coverage
- Tested on multiple architectures
- Works with different model sizes
- Applicable to general transformer models

---

## LMCACHE: Enterprise-Scale KV Cache

### Paper/System
**Title**: LMCACHE: An Efficient KV Cache Layer for Enterprise-Scale LLM Inference
**URL**: [https://lmcache.ai/tech_report.pdf](https://lmcache.ai/tech_report.pdf)
**Focus**: Production deployment of cross-layer techniques

### Enterprise Considerations
- Multi-node inference
- Caching across machines
- Fault tolerance
- Cost optimization

---

## Comparison: Which Sharing Strategy?

### For Research/Exploration
- **Choose**: Cross-Layer Attention (CLA)
- **Reason**: Simple, no retraining needed
- **Trade-off**: Moderate quality loss

### For Production Deployment
- **Choose**: LCKV or SqueezeAttention
- **Reason**: Better quality-efficiency balance
- **Requirement**: Some uptraining acceptable

### For Long Contexts
- **Choose**: YOCO
- **Reason**: O(N) memory scaling
- **Cost**: Architectural change, needs training

### For Balanced Approach
- **Choose**: SqueezeAttention
- **Reason**: Layer-aware, 2D optimization
- **Benefit**: 30-70% reduction without retraining

---

## Interaction with Other Techniques

### Cross-Layer Sharing + Token Eviction
- Can combine approaches
- Each layer selects important tokens
- Reduced cache due to sharing + eviction
- Cumulative benefits

### Cross-Layer Sharing + Quantization
- Quantize shared KV cache
- Orthogonal optimization
- Further memory reduction
- Research direction: Combined strategies

### Cross-Layer Sharing + GQA
- Both reduce KV dimensions
- GQA: Reduces head dimension
- Layer sharing: Reduces layer dimension
- Compatible optimizations

---

## Key Insights from Research

1. **Layer heterogeneity**: Layers don't equally need KV cache
2. **Adaptive sharing**: Different layers need different budgets
3. **Architectural potential**: YOCO shows architectural alternatives exist
4. **Practical efficiency**: 2-4× memory reduction achievable
5. **Quality preservation**: Minimal degradation with proper methods

---

**Sources Referenced**:
- [https://arxiv.org/abs/2410.14442](https://arxiv.org/abs/2410.14442)
- [https://github.com/whyNLP/LCKV](https://github.com/whyNLP/LCKV)
- [https://arxiv.org/abs/2405.05254](https://arxiv.org/abs/2405.05254) (YOCO)
- [https://arxiv.org/abs/2404.04793](https://arxiv.org/abs/2404.04793) (SqueezeAttention)
- [https://lmcache.ai/tech_report.pdf](https://lmcache.ai/tech_report.pdf)

**Generated**: January 27, 2026
**Status**: Literature Review Data Collection
