# KV-Cache Quantization: KIVI, KVQuant, and Related Methods

## Overview
KV-cache quantization reduces memory consumption and bandwidth requirements by storing key and value tensors at lower precision (sub-4-bit), enabling longer context windows and larger batch sizes.

---

## KIVI: A Tuning-Free Asymmetric 2-bit Quantization for KV Cache

### Paper Overview
**Title**: KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache
**Authors**: Jing Yuan et al.
**Year**: 2024
**Venue**: ICML 2024
**arXiv ID**: 2402.02750
**URLs**:
- arXiv: [https://arxiv.org/abs/2402.02750](https://arxiv.org/abs/2402.02750)
- ICML 2024: [https://proceedings.mlr.press/v235/liu24bz.html](https://proceedings.mlr.press/v235/liu24bz.html)
- PDF: [https://raw.githubusercontent.com/mlresearch/v235/main/assets/liu24bz/liu24bz.pdf](https://raw.githubusercontent.com/mlresearch/v235/main/assets/liu24bz/liu24bz.pdf)
- GitHub: [https://github.com/jy-yuan/KIVI](https://github.com/jy-yuan/KIVI)
- HuggingFace Blog: [https://huggingface.co/blog/kv-cache-quantization](https://huggingface.co/blog/kv-cache-quantization)

### Core Innovation

KIVI is a **plug-and-play 2-bit KV cache quantization algorithm requiring zero fine-tuning**.

#### Asymmetric Quantization Strategy
- **Key cache**: Per-channel quantization
- **Value cache**: Per-token quantization
- **Rationale**: Keys exhibit channel-wise outliers; values exhibit token-wise patterns

#### Why Asymmetry Matters
- Keys have high-magnitude outliers concentrated in specific channels
- Values don't show pronounced per-channel outlier patterns
- Per-channel key quantization preserves outlier information
- Per-token value quantization aligns with streaming inference

### Performance Results

#### Memory Efficiency
- **2.6× reduction** in peak memory (including model weights)
- Enables **4× larger batch sizes**
- Direct memory savings for long-context inference

#### Throughput Improvements
- **2.35× ~ 3.47× throughput** increase on real LLM workloads
- Hardware-friendly implementation with optimized CUDA kernels
- Streaming-compatible design

#### Model Coverage
- **Llama family** (Llama, Llama-2)
- **Falcon**
- **Mistral**
- Maintains quality across models

#### Quality Preservation
- Minimal perplexity degradation
- Compatible with existing quantization-aware inference systems

### Technical Approach

#### Per-Channel Key Quantization
- Quantizes each channel independently
- Handles outliers naturally through channel-specific scaling
- Preserves critical attention patterns

#### Per-Token Value Quantization
- Quantizes values per token rather than per channel
- Aligns with streaming inference patterns
- Allows efficient cache appending

#### Streaming Compatibility
- New quantized tokens appended directly to existing cache
- No re-quantization of previous tokens needed
- Maintains constant-time append operations

### Hardware Implementation

- **Custom CUDA kernels** for efficient quantization/dequantization
- **Streaming-friendly** design for online inference
- **Low overhead** computation during decoding

---

## KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization

### Paper Overview
**Title**: KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization
**Authors**: Hooper et al. (SqueezeAILab)
**Year**: 2024
**Venue**: NeurIPS 2024
**arXiv ID**: 2401.18079
**URLs**:
- arXiv: [https://arxiv.org/abs/2401.18079](https://arxiv.org/abs/2401.18079)
- NeurIPS 2024: [https://proceedings.neurips.cc/paper_files/paper/2024/file/028fcbcf85435d39a40c4d61b42c99a4-Paper-Conference.pdf](https://proceedings.neurips.cc/paper_files/paper/2024/file/028fcbcf85435d39a40c4d61b42c99a4-Paper-Conference.pdf)
- OpenReview: [https://openreview.net/forum?id=0LXotew9Du](https://openreview.net/forum?id=0LXotew9Du)
- GitHub: [https://github.com/SqueezeAILab/KVQuant](https://github.com/SqueezeAILab/KVQuant)
- vLLM Integration: [https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/)

### Core Problem

**Challenge**: Existing quantization methods fail to represent KV activations accurately at sub-4-bit precision, limiting context length.

### Key Innovations

#### 1. Per-Channel Key Quantization
- Adjusts quantization dimension to match key distribution
- Handles outliers better than standard approaches
- Improves key representation quality

#### 2. Pre-RoPE Key Quantization
- Quantizes keys **before** rotary positional embedding application
- Mitigates RoPE's impact on quantization distribution
- Improves quantized representation accuracy

#### 3. Non-Uniform KV Cache Quantization
- Derives **per-layer sensitivity-weighted non-uniform datatypes**
- Different layers use different quantization schemes
- Matches layer-specific activation distributions

#### 4. Per-Vector Dense-and-Sparse Quantization
- Isolates **numerical outliers** separately
- Handles outlier patterns explicitly
- Improves precision for remaining values

### Performance Results

#### Long-Context Capability
- **LLaMA-7B**: Up to 1 million tokens on single A100-80GB
- **Distributed**: Up to 10 million tokens on 8-GPU system
- **Quality**: < 0.1 perplexity degradation at 3-bit

#### Efficiency Gains
- **Custom CUDA kernels**: 1.7× speedups for matrix-vector multiplications
- **3-bit precision**: Achieves < 0.1 perplexity loss
- **Benchmarks**: WikiText-2 and C4 datasets

#### Model Compatibility
- **LLaMA** (all versions)
- **Llama-2**
- **Llama-3**
- **Mistral**

### Context Length Scaling

| Config | Context Length | Device(s) |
|--------|----------------|-----------|
| LLaMA-7B | 1M | Single A100-80GB |
| LLaMA-7B | 10M | 8× GPU system |
| Llama-2-13B | 512K | Single A100-80GB |

---

## Comparison: KIVI vs KVQuant

### KIVI Characteristics
- **Precision**: 2-bit
- **Fine-tuning**: None required
- **Quantization style**: Asymmetric (per-channel keys, per-token values)
- **Focus**: Streaming compatibility, ease of deployment
- **Throughput**: 2.35-3.47× improvement
- **Memory**: 2.6× reduction

### KVQuant Characteristics
- **Precision**: Sub-4-bit (down to 1-bit experiments)
- **Fine-tuning**: Training-free but technique-heavy
- **Quantization style**: Non-uniform, adaptive per-layer
- **Focus**: Ultra-long contexts (up to 10M tokens)
- **Latency**: 1.7× CUDA kernel speedups
- **Memory**: Enables massive context scaling

---

## Related Quantization Methods

### KITTY: Accurate and Efficient 2-Bit KV Cache Quantization
**Status**: Recent arxiv paper (2024)
**URL**: [https://arxiv.org/pdf/2511.18643](https://arxiv.org/pdf/2511.18643)
**Focus**: Improving 2-bit quantization accuracy

### Other Emerging Methods
- KVQuant variations for specific hardware
- Hybrid quantization (mixed precision per layer)
- Dynamic quantization with adaptive bit-width

---

## Integration with Inference Systems

### vLLM Support
- KVQuant integrated in vLLM
- Configuration via quantization parameters
- Hardware-optimized execution

### HuggingFace Integration
- Blog posts and guides on KV cache quantization
- Community implementations

---

## Quantization Challenges

### 1. Outlier Handling
- Large-magnitude values in keys and values
- Requires specialized quantization schemes
- Trade-off between precision and memory

### 2. Distribution Variance
- Keys and values have different distributions
- Per-layer sensitivity varies significantly
- Requires fine-grained quantization configuration

### 3. Attention Pattern Preservation
- Must preserve critical attention computation accuracy
- Errors propagate through attention mechanism
- Quality degradation difficult to prevent at very low bits

### 4. Hardware Efficiency
- Existing hardware designed for FP32/FP16
- Custom kernels needed for full speedup
- Dequantization overhead during attention

---

## Future Directions

1. **Sub-2-bit quantization**: Push to 1-bit KV cache
2. **Mixed precision**: Different bits for different layers
3. **Learned quantization**: Fine-tuning of quantization schemes
4. **Hardware co-design**: Specialized processors for quantized attention
5. **Dynamic quantization**: Adaptive precision per query

---

## Key Takeaways

- **KIVI**: Practical 2-bit solution, zero fine-tuning, streaming-friendly
- **KVQuant**: Comprehensive sub-4-bit approach, ultra-long contexts, research-grade
- **Together**: Represent frontier of KV cache quantization (2024)
- **Impact**: Enabling 1M+ token contexts on consumer hardware
- **Future**: Integration into standard inference systems

---

**Sources Referenced**:
- [https://arxiv.org/abs/2402.02750](https://arxiv.org/abs/2402.02750) (KIVI)
- [https://arxiv.org/abs/2401.18079](https://arxiv.org/abs/2401.18079) (KVQuant)
- [https://huggingface.co/blog/kv-cache-quantization](https://huggingface.co/blog/kv-cache-quantization)
- [https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/](https://docs.vllm.ai/en/latest/features/quantization/quantized_kvcache/)

**Generated**: January 27, 2026
**Status**: Literature Review Data Collection
