# RETRO and Retrieval-Enhanced Pre-training

## Primary Paper: Borgeaud et al. 2022

**Title:** Improving Language Models by Retrieving from Trillions of Tokens

**Authors:** Borgeaud, Mensch, Hoffmann, Cai, Rutherford, Glaese, et al.

**Year:** 2022

**Venue:** ICML 2022

**arXiv ID:** 2112.04426

**Conference Link:** https://proceedings.mlr.press/v162/borgeaud22a.html

**arXiv URL:** https://arxiv.org/abs/2112.04426

---

## Key Contributions

### Problem Statement
Large language models scaled to tremendous parameter counts (175B+ GPT-3). RETRO shows comparable performance with 25× fewer parameters by incorporating retrieval during pre-training and inference.

### Core Innovation: Retrieval-Enhanced Pre-training

#### Architecture Components
1. **Frozen BERT Retriever**: Bi-encoder retriever providing document chunks
2. **Retrieval-Enhanced Encoder**: Encodes retrieved context and local context
3. **Chunked Cross-Attention**: Special attention mechanism over retrieved chunks
4. **Auto-regressive Decoder**: Generates tokens conditioned on retrieved context

#### Key Mechanism: Chunked Cross-Attention
- Decodes token streams with interleaved retrieval
- Retrieves nearest neighbor document chunks based on preceding tokens
- Attention over both local context window and retrieved chunks
- Reduces context size needed from internal parameters

---

## Technical Architecture

### Pre-training Corpus
- **2 Trillion Tokens**: Massive retrieval database for chunk lookup
- **Index**: Semantic nearest neighbor index for efficient retrieval
- **Chunk Size**: 64 tokens per chunk
- **Retrieval**: Retrieve top-2 chunks per position

### Model Configuration
- **Autoregressive Decoder**: 248 parameter layers
- **Total Parameters**: 6.7B (compared to GPT-3 175B)
- **Context Window**: 2048 tokens
- **Compute Budget**: Similar to baseline without retrieval

### Retrieval Strategy
- **Query Formation**: Based on preceding token embeddings
- **Database**: Massive database of 2 trillion tokens
- **Efficiency**: FAISS index for fast nearest neighbor lookup
- **Backpropagation**: Retrieval not directly differentiable; frozen retriever

---

## Performance Results

### Language Modeling Benchmarks
- **Perplexity on Pile**: Comparable to GPT-3 with 25× fewer parameters
- **Zero-shot Performance**: Strong zero-shot results on downstream tasks
- **Fine-tuning**: Excellent few-shot and fine-tuning performance

### Knowledge-Intensive Tasks
- **Open-Domain QA**: State-of-the-art on Natural Questions, TriviaQA
- **Question Answering**: After fine-tuning, matches large dense baselines
- **Fact Verification**: Improved factuality

### Scaling Properties
- Performance scales well with retrieval database size
- Larger retrieval corpus = better performance
- Demonstrates utility of very large-scale external memory

---

## Comparison with RAG

| Aspect | RETRO | RAG |
|--------|-------|-----|
| Retrieval Timing | During pre-training + inference | During fine-tuning + inference |
| Scale | Trillion-scale database | Million-scale database |
| Integration | Built into model training | Post-hoc augmentation |
| Efficiency | Parameter-efficient (6.7B) | Parametric + retriever overhead |
| Flexibility | Less flexible (frozen retriever) | More flexible (end-to-end) |

---

## Key Technical Details

### Chunked Cross-Attention Mechanism
```
Input: query (preceding tokens) + retrieved chunks
Output: context representation for next token prediction

For each position:
1. Form query from preceding token embeddings
2. Retrieve top-k nearest chunks
3. Compute attention weights over chunks
4. Aggregate chunk representations
5. Combine with local attention for final output
```

### Efficient Retrieval During Training
- **Retrieval Indexing**: Pre-computed FAISS index
- **No Gradient Flow Through Retriever**: Reduces computational cost
- **Offline Index Updates**: Periodic updates rather than continuous

### Pre-training Approach
- Continues pre-training objective with retrieval
- Masked language modeling adapted for retrieval setting
- Learns to effectively use retrieved context without explicit supervision

---

## Research Impact

### Why RETRO Matters
1. **Efficiency Breakthrough**: Demonstrates extreme parameter efficiency through retrieval
2. **Scalability**: Shows retrieval from 2 trillion tokens is tractable
3. **Pre-training Integration**: First major success integrating retrieval into pre-training
4. **Knowledge Externalization**: Suggests moving knowledge to external non-parametric store

### Subsequent Work
- **RETRO+**: Improved context window and retrieval
- **Memorizing Transformers**: Similar ideas for retrieval-augmented generation
- **RETROREG**: Regularization techniques for retrieval-augmented models
- **Industry Adoption**: Inspired Anthropic's retrieval-augmented approaches

---

## Limitations and Challenges

1. **Frozen Retriever**: Cannot learn task-specific retrieval through gradients
2. **Chunk Granularity**: Fixed chunk size may not match semantic boundaries
3. **Computational Overhead**: Despite efficiency, retrieval adds latency
4. **Index Staleness**: Retrieval index not updated during training
5. **Scaling Challenges**: Managing trillion-token database requires specialized infrastructure

---

## Practical Considerations

### Computational Requirements
- **Retrieval Latency**: ~1-10ms per token during inference
- **Index Construction**: Hours to days for trillion-scale database
- **Hardware**: GPU memory for efficient retrieval operations

### Hyperparameters
- **Chunk Size**: 64 tokens (explored 32-128)
- **Number of Chunks**: 2 (explored 1-4)
- **Retriever**: Frozen BERT-base
- **Training Duration**: Hundreds of billions tokens

### Deployment Considerations
- Requires maintaining massive retrieval index
- Serving latency must account for retrieval + generation
- Cold-start problem for new documents (index not updated online)

---

## File Metadata
- **Research Area**: Retrieval-Augmented Pre-training, Parameter Efficiency, Large-Scale LMs
- **Method Type**: Hybrid (Retrieval + Auto-regressive Generation)
- **Publication Tier**: Top-tier (ICML)
- **Citation Count**: 1000+ citations
- **Code Availability**: DeepMind released partial implementations
- **Reproducibility**: Good documentation of architecture; full model not released
