# Token Eviction and KV Cache Pruning Methods

## Overview
Token eviction methods selectively discard tokens from the KV cache to reduce memory consumption. Eviction strategies determine which tokens to keep (important) and which to remove (less important).

---

## ScissorHands: Token Importance via Attention Scores

### Concept
**ScissorHands** drops tokens based on accumulated attention scores to identify and retain important "heavy hitter" tokens.

#### Token Importance Metric
- **Accumulated attention**: Sum of attention weights across all layers/heads
- **Ranking**: Score each token by total attention received
- **Retention**: Keep top-K tokens by score, evict others
- **Compression ratio**: Target specific cache reduction (e.g., 30% of original)

#### Mechanism
```
For each token:
  importance = sum(attention_weights from all heads/layers)

Select: top-K tokens by importance
Evict: remaining tokens
```

### Eviction Strategy
- **Type**: Least Frequently Used (LFU) variant
- **Metric**: Frequency of attention (cumulative across time)
- **Locality**: Recent tokens often retained together
- **Balance**: Combine frequency and recency

### Performance Characteristics
- Training-free implementation
- Low computational overhead during inference
- Reasonable quality-efficiency trade-off
- Works across different model architectures

### Limitations
1. Attention scores may not reflect true importance
2. No theoretical guarantee on effectiveness
3. Layer-specific analysis not considered
4. Limited for long sequences

---

## FastGen: Adaptive Layer-wise Selection

### Paper/Method Overview
**Repository**: [https://github.com/machilusZ/FastGen](https://github.com/machilusZ/FastGen)
**Title**: Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs

### Core Insight
Different layers have fundamentally different attention patterns and require different eviction strategies.

#### Key Observation
- **Layer variation**: Lower layers focus on local patterns, higher layers on semantic content
- **Head variation**: Different heads within same layer have different patterns
- **Task variation**: Eviction strategy should adapt per task
- **Position-dependency**: Some layers prefer recent tokens, others prefer special tokens

### Technical Approach

#### Profiling Phase
1. Process prefill stage normally
2. Analyze attention matrix for each head
3. Determine which eviction strategy works best
4. Select from portfolio of strategies

#### Strategy Portfolio
- **Sliding window**: Recent tokens only (e.g., last 512 tokens)
- **Special tokens**: Attention sinks + recent (StreamingLLM-style)
- **Local and frequency**: Heavy-hitter + recent (H2O-style)
- **Sparse selection**: Topk attention recipients (ScissorHands-style)

#### Per-Head Assignment
1. Profile each attention head's pattern
2. Assign optimal strategy from portfolio
3. Use unified cache budget per strategy
4. Different heads may use different strategies

### Performance
- Consistent improvement over:
  - **H2O**: Heavy-hitter baseline
  - **Scissorhands**: Frequency baseline
  - **Fixed policies**: Uniform strategy across heads
- Adaptive selection achieves better quality-efficiency trade-off

### Advantages
1. **Principled selection**: Based on actual attention patterns
2. **Layer-aware**: Adapts to layer characteristics
3. **Head-specific**: Customized per attention head
4. **Low overhead**: Profiling at prefill time
5. **Flexible**: Mix-and-match strategies

---

## Q-HITTER: Combined Heavy-Hitter and Quantization

### Paper Overview
**Title**: Q-HITTER: A Better Token Oracle for Efficient LLM Inference via Sparse-Quantized KV Cache
**Venue**: MLSys 2024
**URLs**:
- PDF: [https://proceedings.mlsys.org/paper_files/paper/2024/file/bbb7506579431a85861a05fff048d3e1-Paper-Conference.pdf](https://proceedings.mlsys.org/paper_files/paper/2024/file/bbb7506579431a85861a05fff048d3e1-Paper-Conference.pdf)
- GitHub: [https://github.com/VITA-Group/Q-Hitter](https://github.com/VITA-Group/Q-Hitter)

### Problem: H2O + Quantization

#### Insight
Combining H2O token selection with low-bit quantization reveals issues:

1. **Selection accuracy degrades**: Low-bit quantization corrupts attention patterns
   - Heavy-hitter selection relies on accurate attention computation
   - Quantization distorts attention before H2O selection
   - Selected tokens may not be optimal for quantized case

2. **Quantization-unfriendly tokens**: H2O selects tokens important for attention
   - But these tokens may be difficult to quantize
   - High-magnitude outliers in selected tokens
   - Quantization error propagates through attention

### Solution: Dual-Metric Selection

#### Quantization Friendliness
- **Metric**: How well can token be quantized?
- **Computation**: Analyze distribution properties
- **Score**: Tokens with amenable distributions rate higher
- **Examples**: Smooth distributions score higher than outlier-heavy

#### Combined Scoring
```
Token_score = α * attention_importance + β * quantization_friendliness

Selection: Keep top-K tokens by combined score
```

### Improvements Over H2O

#### Accuracy Preservation
- Better quality at 4-bit and lower precision
- Handles quantization effects explicitly
- Maintains model performance

#### Performance Impact
- **Memory**: Up to 20× reduction
- **Throughput**: Improvements across baselines:
  - **vs. Hugging Face Accelerate**: 33×
  - **vs. DeepSpeed**: 7×
  - **vs. FlexGen**: 4×
  - **vs. H2O**: 1.3×

### Technical Contributions
1. Identifies H2O quantization vulnerability
2. Proposes quantization-aware selection
3. Combines sparsification and quantization
4. State-of-the-art efficiency metrics

---

## HashEvict: Locality-Sensitive Hashing for KV Cache

### Paper Overview
**Title**: HashEvict: A Pre-Attention KV Cache Eviction Strategy using Locality-Sensitive Hashing
**Year**: 2024
**arXiv ID**: 2412.16187
**URLs**:
- arXiv: [https://arxiv.org/abs/2412.16187](https://arxiv.org/abs/2412.16187)
- PDF: [https://arxiv.org/pdf/2412.16187](https://arxiv.org/pdf/2412.16187)
- ResearchGate: [https://www.researchgate.net/publication/387349709](https://www.researchgate.net/publication/387349709)

### Core Innovation

Uses **Locality-Sensitive Hashing (LSH)** to quickly identify dissimilar tokens for eviction.

#### Why LSH?
- **Problem**: Attention-based selection requires computing attention scores
- **Cost**: Full attention computation expensive during prefill
- **Insight**: Can approximate similarity without full attention
- **Solution**: LSH provides fast approximate similarity

#### Mechanism
```
For each new query token q:
  1. Compute LSH hash of q
  2. Hash all cached key tokens k_i
  3. Compute Hamming distance between hashes
  4. Evict tokens with high Hamming distance (dissimilar)
  5. Retain tokens with low Hamming distance (similar)
```

### Technical Details

#### LSH Implementation
- **Binarization**: Gaussian projections create binary hashes
- **Projection dimension**: Much smaller than embedding dimension
- **Hamming distance**: Cheap to compute between binary vectors
- **Trade-off**: Approximate similarity, but very fast

#### Pre-Attention Computation
- **Timing**: Eviction decisions made before attention computation
- **Savings**: Avoids computing attention on evicted tokens
- **Efficiency**: Cumulative savings across layers

### Performance Results

#### Compression
- **Llama 3**: 30-70% KV cache compression
- **Task coverage**: Q&A, retrieval, free-response
- **Quality**: Minimal performance drop

#### Speed Improvements
- **Prefill phase**: 1.5-2× speedup vs. H2O/ScissorHands
- **Decoding phase**: Competitive with baseline methods
- **Overall**: 1.5-2× prefill vs. 2× decoding vs. FastGen

### Comparison with Baselines

| Method | Decision Timing | Speedup | Quality |
|--------|----------------|---------|---------|
| H2O | Post-attention | Baseline | Good |
| ScissorHands | Post-attention | Baseline | Good |
| FastGen | Pre-attention | 1.5× | Good |
| HashEvict | Pre-attention | 1.5-2× | Good |

### Advantages
1. **Pre-attention**: No attention computation overhead
2. **Fast similarity**: LSH speeds up comparison
3. **Simple**: Easy to implement and integrate
4. **Effective**: 30-70% compression with minimal loss

---

## Other Token Eviction Strategies

### Sliding Window
- Keep only recent N tokens
- Simple, no overhead
- Loss of long-range dependencies
- Used in streaming scenarios

### Attention Sink + Sliding Window
- Combine with StreamingLLM approach
- Keep special initial tokens
- Maintain recent window
- Balance local and global context

### Random Eviction
- Baseline for comparison
- Surprisingly competitive in some cases
- No computational cost
- High quality variance

### Semantic-Aware Eviction
- Group similar tokens
- Evict duplicates/redundancy
- Preserve diversity
- Research direction

---

## KV Cache Compression: Merging Approaches

### Token Merging vs. Eviction
- **Eviction**: Delete less important tokens
- **Merging**: Combine multiple tokens into one
- **Complementary**: Can be combined

### MiniCache: Depth-wise Merging
**URL**: [https://proceedings.neurips.cc/paper_files/paper/2024/file/fd0705710bf01b88a60a3d479ea341d9-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/fd0705710bf01b88a60a3d479ea341d9-Paper-Conference.pdf)

- Merges KV cache across depth (layers)
- Consolidates states every N layers
- Reduces cache size significantly
- Different approach than token-level eviction

### KVReviver: Reversible Compression
**URL**: [https://arxiv.org/html/2512.17917](https://arxiv.org/html/2512.17917)

- Uses sketch algorithm for compression
- Allows reconstruction of compressed tokens
- Trade memory for computation
- Flexible accuracy control

### RocketKV: Two-Stage Compression
**URL**: [https://arxiv.org/html/2502.14051v3](https://arxiv.org/html/2502.14051v3)

- Combines permanent eviction with dynamic selection
- Two-stage approach:
  - Stage 1: Permanent eviction (can't recover)
  - Stage 2: Dynamic selection (per-batch optimization)
- Optimizes both prefill and decode phases

---

## Eviction Strategy Selection Guidelines

### For Streaming Applications
- **Recommend**: Attention Sinks + Sliding Window
- **Reason**: Constant memory, preserves recent context
- **Alternative**: HashEvict for faster processing

### For Batch Inference
- **Recommend**: H2O or ScissorHands
- **Reason**: Good quality-efficiency trade-off
- **Alternative**: FastGen for layer-aware optimization

### For Long Contexts with Quality Focus
- **Recommend**: Q-HITTER with quantization
- **Reason**: Best combined efficiency
- **Alternative**: KVQuant for pure quantization

### For Latency-Critical Applications
- **Recommend**: HashEvict
- **Reason**: Pre-attention computation, fast
- **Alternative**: Simple sliding window

---

## Evaluation Metrics

### Common Benchmarks
- **Perplexity**: WikiText-2, C4 datasets
- **QA Tasks**: MMLU, SQuAD, etc.
- **Retrieval**: Needle-in-haystack tests
- **Generation**: BLEU, ROUGE scores

### Quality-Efficiency Trade-off
- **Compression ratio**: % of original KV cache retained
- **Quality drop**: Perplexity increase threshold
- **Sweet spot**: 20-50% compression with minimal degradation

---

**Key Takeaways**:
1. **Eviction diversity**: Multiple strategies for different scenarios
2. **Adaptive selection**: FastGen shows benefits of per-layer tuning
3. **Complementary techniques**: Combine with quantization (Q-HITTER)
4. **Pre-attention optimization**: HashEvict avoids attention overhead
5. **Practical deployment**: Choose based on application requirements

---

**Sources Referenced**:
- [https://github.com/machilusZ/FastGen](https://github.com/machilusZ/FastGen)
- [https://arxiv.org/abs/2412.16187](https://arxiv.org/abs/2412.16187) (HashEvict)
- [https://proceedings.mlsys.org/paper_files/paper/2024/file/bbb7506579431a85861a05fff048d3e1-Paper-Conference.pdf](https://proceedings.mlsys.org/paper_files/paper/2024/file/bbb7506579431a85861a05fff048d3e1-Paper-Conference.pdf) (Q-HITTER)

**Generated**: January 27, 2026
**Status**: Literature Review Data Collection
