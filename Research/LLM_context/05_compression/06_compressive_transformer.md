# Compressive Transformers for Long-Range Sequence Modelling

**Authors:** Jack W. Rae, Anna Potapenko, Siddhant M. Jayakumar, Timothy P. Lillicrap

**Year:** 2020

**Venue:** International Conference on Learning Representations (ICLR 2020)

**arXiv ID:** 1911.05507

**Institution:** DeepMind

**Key Concept:**
The Compressive Transformer is an attentive sequence model which compresses past memories for long-range sequence learning, extending context windows while maintaining computational efficiency.

**Architecture:**
- Builds on standard Transformer architecture
- Adds memory compression mechanism
- Maintains recurrent state of compressed memories
- Attention mechanism spans both recent and compressed historical context

**Memory Compression Mechanism:**
- Compresses older memories into a compact representation
- Recent context maintained in full detail
- Two-tier memory system:
  1. Recent attention memory (full resolution)
  2. Compressed historical memory (lower resolution)
- Compression achieved through convolutional pooling

**Key Features:**
- Compresses past memories for long-range modeling
- Maintains interpretability of attention patterns
- Scalable to very long sequences
- Can be applied to multiple modalities

**Performance Results:**
- State-of-the-art language modeling results:
  - WikiText-103: 17.1 ppl (perplexity)
  - Enwik8: 0.97 bpc (bits per character)
- Effective on multiple tasks and modalities

**Applications:**
1. **Language Modeling:**
   - Long-range sequence understanding
   - Extended context window modeling

2. **Speech Modeling:**
   - Effective high-frequency speech processing
   - Long-term temporal dependencies

3. **Reinforcement Learning:**
   - Memory mechanism for RL agents
   - Object matching and visual reasoning tasks

**Advantages:**
- Theoretical foundation for long-range modeling
- Maintains computational efficiency
- Interpretable memory compression
- Versatile across different modalities
- State-of-the-art performance metrics

**Novel Contributions:**
- New open-vocabulary language modeling benchmark (PG-19)
- Derived from books for challenging long-range tasks
- Promotes domain of long-range sequence learning

**Memory Size Trade-offs:**
- Hyperparameter control of compression ratio
- Balance between context length and memory footprint
- Tunable based on task requirements

**Attention Patterns:**
- Maintains full attention over recent context
- Sparse attention patterns for compressed memory
- Efficient computational scaling

## References
- [Compressive Transformers for Long-Range Sequence Modelling - arXiv](https://arxiv.org/abs/1911.05507)
- [Compressive Transformers - OpenReview](https://openreview.net/forum?id=SylKikSYDH)
- [ICLR 2020 Poster Presentation](https://iclr.cc/virtual_2020/poster_SylKikSYDH.html)
- [Compressive Transformers PyTorch Implementation](https://github.com/lucidrains/compressive-transformer-pytorch)
- [Paper Page - Hugging Face](https://huggingface.co/papers/1911.05507)
