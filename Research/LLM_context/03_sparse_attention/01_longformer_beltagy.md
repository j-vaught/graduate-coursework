# Longformer: The Long-Document Transformer

## Paper Information
- **Title:** Longformer: The Long-Document Transformer
- **Authors:** Iz Beltagy, Matthew E. Peters, Arman Cohan
- **Year:** 2020
- **Month:** April 2020
- **Venue:** Published at ACL 2020
- **arXiv ID:** 2004.05150
- **Organization:** Allen Institute for Artificial Intelligence (AI2)

## Key Innovation
Longformer introduces a drop-in replacement for the standard transformer self-attention mechanism that reduces complexity from quadratic O(n²) to linear O(n) with respect to sequence length, enabling processing of documents with thousands of tokens.

## Attention Mechanism Design
Combines two complementary attention patterns:
1. **Local Windowed Attention**: A sliding window mechanism where each token attends to its immediate neighbors (e.g., window size of 512 tokens). Similar to attention with convolutional kernels.
2. **Task-Motivated Global Attention**: Applied to special tokens (CLS token at beginning, ending tokens, and mask tokens) that attend to the entire document and receive attention from all tokens.

## Technical Details
- Maintains full expressiveness by combining local and global patterns
- Local attention captures fine-grained context and patterns
- Global attention enables long-range dependencies through selected tokens
- Two-dimensional factorization preserves model's ability to learn complex patterns

## Performance Benchmarks
- **Pretraining**: Consistently outperforms RoBERTa on long document tasks
- **WikiHop**: Sets new state-of-the-art results (65.10% F1)
- **TriviaQA**: Strong performance on long document question answering (80.51% F1)
- **Context Window**: Effective with sequences from 1K to 4K tokens
- **CIFAR-10**: 91% accuracy without data augmentation
- **Speedup**: Generates 60x faster than comparable models on generation tasks

## Practical Applications
- Legal document analysis and contract processing
- Scientific paper summarization and information extraction
- Book summarization and long-form document understanding
- Genomic sequence analysis and DNA processing
- Question answering over long documents

## Memory and Computational Benefits
- Memory usage linear in sequence length (vs. quadratic for standard attention)
- Significant speedup on long sequences compared to RoBERTa
- 10X memory savings at sequence length 2K, 20X at 4K
- Compatible with pre-training on RoBERTa checkpoints

## Comparison with Other Methods
- **vs. BigBird**: Both use sparse attention but with different patterns
- **vs. Reformer**: Reformer uses LSH hashing; Longformer uses structured sparse patterns
- **vs. Linformer**: Different approximation strategy; Longformer maintains exact computation on sparse subset

## Limitations
- Still requires careful tuning of local window size
- Global tokens must be manually specified for each task
- Performance depends on proper selection of global attention tokens

## Code Availability
- Open-source implementation available at: https://github.com/allenai/longformer
- Integrated into Hugging Face Transformers library

## Citation References
Beltagy, I., Peters, M.E., & Cohan, A. (2020). Longformer: The Long-Document Transformer. In Proceedings of the 2020 Conference of the Association for Computational Linguistics (ACL).

## Follow-up Works & Extensions
- Longformer-Encoder-Decoder (LED) for sequence-to-sequence tasks
- MultiLingual Longformer for non-English languages
- Fine-tuning approaches for downstream tasks
