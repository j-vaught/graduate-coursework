# Performer: Rethinking Attention with Performers

## Paper Information
- **Title:** Rethinking Attention with Performers
- **Authors:** Krzysztof Choromanski, Valerii Likhosherstov, David Dohan, Xinyi Song, Andreea Gane, Tamas Sarlos, Peter Hawkins, Jared Davis, Afroz Ubaru, Yunyang Xiong, Oanh Nguyen, Jason Wills
- **Year:** 2020-2021
- **Month:** September 2020 (arXiv), ICLR 2021 (accepted)
- **Venue:** International Conference on Learning Representations (ICLR 2021) - Oral Presentation
- **arXiv ID:** 2009.14794
- **Organization:** Google Research

## Key Innovation
Introduces Performers with FAVOR+ (Fast Attention Via positive Orthogonal Random features), enabling linear-time approximation of standard softmax attention without relying on sparsity patterns or low-rank assumptions.

## Technical Approach: FAVOR+
**Core Mechanism:**
- Approximates softmax attention kernel using positive random features
- Enables linear space and time complexity O(n) vs. quadratic O(n²)
- Unbiased or nearly-unbiased estimation of attention matrix
- Low estimation variance with theoretical guarantees

**Random Features:**
- Uses orthogonal random projections
- Kernel-based approximation of softmax similarity
- Maintains expressiveness through randomized projections
- Different variants for different attention kernels

## Theoretical Guarantees
- **Unbiased Estimation**: Provides unbiased or nearly-unbiased approximation
- **Convergence**: Uniform convergence guarantees with low variance
- **Stability**: Stable learning without the instabilities of other kernel approximations
- **Compatibility**: Works with any kernelizable attention mechanism

## Computational Complexity
- **Time Complexity**: O(n) instead of O(n²) for sequence length n
- **Space Complexity**: Linear memory footprint
- **Practical Speed**: 3-4x speedup on moderately long sequences (1K tokens)
- **Parallelizability**: Fully compatible with existing transformer implementations

## Performance Results
**Language Modeling:**
- Competitive with or better than standard transformers
- Effective on Text Summarization tasks
- Strong results on machine translation

**Vision Tasks:**
- Pixel prediction on high-resolution images
- Image classification with long sequences
- Competitive with Vision Transformers

**Protein Sequence Modeling:**
- State-of-the-art or near state-of-the-art on protein folding
- Excellent long-range dependency learning
- Effective on biological sequence tasks

**Benchmarks:**
- Long Range Arena (LRA): Competitive performance
- Machine Translation (WMT): Strong BLEU scores
- GLUE Benchmark: Comparable to standard BERT

## Architecture Design
- Drop-in replacement for standard transformer attention
- Compatible with existing model architectures
- Can be integrated into BERT, GPT, and other models
- Maintains compatibility with pre-trained checkpoints

## Advantages Over Other Efficient Attention Methods
- **vs. Sparse Attention**: No need to design sparse patterns; automatic and general
- **vs. Linformer**: Different mathematical approach; both achieve O(n) but with different characteristics
- **vs. BigBird**: More general approximation without hand-crafted patterns
- **vs. Linear Transformers**: More stable training with theoretical guarantees

## Limitations and Challenges
- Random feature approximation adds variance
- May require more features for very high-dimensional cases
- Kernel approximation quality depends on feature count
- Still somewhat slower than hand-optimized sparse patterns in practice

## Implementation Details
- Orthogonal random matrix generation
- Efficient cumulative sum operations for linear computation
- Support for various attention kernel functions
- Flexible random feature dimensions

## Applications
- Long document processing
- Genomic sequence analysis
- High-resolution image processing
- Protein structure prediction
- Music and audio modeling
- Efficient pretraining of large models

## Code Availability
- Official implementation available
- Integrated into multiple deep learning frameworks
- PyTorch implementations widely available
- Hugging Face integration available

## Extension Work
- **FAVOR#**: Improved kernel approximations via positive random features
- Application to other attention variants
- Combination with other efficiency techniques
- Scaling to extreme sequence lengths

## Related Papers
- FAVOR+ builds on positive random features literature
- Connection to kernel methods and random features
- Related to sketching and streaming algorithms

## Citation Reference
Choromanski, K., Likhosherstov, V., Dohan, D., Song, X., Gane, A., Sarlos, T., ... & Xiong, Y. (2021). Rethinking Attention with Performers. In International Conference on Learning Representations (ICLR).

## Key Insights
- Randomized kernel methods can effectively approximate attention
- Linear complexity approximation maintains quality
- General theoretical framework applicable to various kernels
- Important step toward universal efficient attention mechanisms
