# Big Bird: Transformers for Longer Sequences

## Paper Information
- **Title:** Big Bird: Transformers for Longer Sequences
- **Authors:** Manzil Zaheer, Guru Guruganesh, Avinava Dubey, Joshua Ainslie, Chris Albertson, Santiago Ontanon, Philip Pham, Anirudh Ravula, Qifan Wang, Li Yang
- **Year:** 2020
- **Month:** July 2020
- **Venue:** Advances in Neural Information Processing Systems (NeurIPS 2020)
- **arXiv ID:** 2007.14062
- **Organization:** Google Research

## Key Contribution
Introduces BigBird, a sparse-attention based transformer that extends BERT-like models to much longer sequences (up to 4096 tokens) while maintaining Turing completeness and universal approximation properties of standard transformers.

## Sparse Attention Mechanism Design
Combines three complementary attention patterns:
1. **Local Window Attention**: Each query attends to w/2 tokens to the left and w/2 to the right (local context window)
2. **Random Attention**: Each query attends to r randomly selected keys throughout the full sequence for diversity
3. **Global Attention**: A set of g special global tokens attend to entire sequence and receive attention from all positions

## Theoretical Guarantees
- **Turing Completeness**: BigBird with sparse attention is Turing complete, equivalent to standard full-attention transformers
- **Universal Approximation**: Preserves universal approximator properties - sparse attention mechanisms are as powerful as full-attention
- **Sequence Function Approximation**: Can approximate any sequence-to-sequence function with sparse patterns

## Computational Complexity
- Reduces quadratic O(n²) complexity to linear O(n) complexity
- **Block-wise Sparse Pattern**: Computational complexity O(n√n) with structured sparsity
- **Parameters**: Typical configuration: w (window size), r (random keys), g (global tokens)

## Performance Results
**Long Sequence Processing:**
- Handles sequences up to 4096 tokens (8x longer than previous similar hardware)
- Effective on sequences up to 8000 tokens
- Maintains performance with extreme sequence lengths

**Benchmark Performance:**
- Question Answering: Superior on long-document QA tasks
- Document Classification: Strong results on long document classification
- Genomic Sequences: State-of-the-art on DNA sequence prediction
- Wikipedia and News: Effective on Wikipedia and news document processing

## Practical Applications
- Legal document analysis and long contract processing
- Genomic and DNA sequence analysis
- Code understanding and bug detection
- Scientific paper analysis and citations
- Long document summarization
- Patent analysis and classification

## Comparison with Other Sparse Attention Methods
- **vs. Longformer**: Similar sparse structure but different global token selection strategy
- **vs. Linformer**: BigBird uses structured sparse patterns; Linformer uses low-rank approximation
- **vs. Reformer**: Both sparse but BigBird provides theoretical guarantees Reformer lacks

## Key Advantages
- Theoretically grounded with universal approximation proof
- Can be applied as drop-in replacement for BERT
- Turing complete - maintains full expressiveness
- Combines multiple attention patterns for robustness
- Handles extreme sequence lengths effectively

## Limitations
- Requires careful tuning of window size w, random keys r, and global tokens g
- Global tokens must be manually specified
- Hyperparameter selection impacts performance and efficiency

## Implementation Details
- Attention matrix is sparse with density proportional to 1/√n
- Random sampling adds computational overhead
- Global tokens typically include [CLS], special tokens, and task-specific tokens
- Window size typically set to 64-256 tokens

## Code Availability
- Official implementation: https://github.com/google-research/bigbird
- Available in Hugging Face Transformers
- TensorFlow and PyTorch implementations available

## Related Work & Extensions
- BigBird-RoBERTa: Adapted RoBERTa with BigBird attention
- BigBird-PEGASUS: Sequence-to-sequence variant
- BigBird for multilingual tasks
- Application to very long sequences (8K+ tokens)

## Citation Reference
Zaheer, M., Guruganesh, G., Dubey, A., Ainslie, J., Albertson, C., Ontanon, S., ... & Yang, L. (2020). Big Bird: Transformers for Longer Sequences. In Advances in Neural Information Processing Systems (NeurIPS 2020).

## Key Findings Summary
- Sparse attention maintains theoretical properties of full attention
- Combination of local, random, and global patterns is effective
- Can extend transformers to 4x-8x longer sequences with similar compute
- Provides principled approach to long sequence modeling
