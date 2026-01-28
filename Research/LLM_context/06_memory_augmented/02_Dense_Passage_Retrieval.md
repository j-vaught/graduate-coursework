# Dense Passage Retrieval (DPR) and Dense Retrieval Methods

## Primary Paper: Karpukhin et al. 2020

**Title:** Dense Passage Retrieval for Open-Domain Question Answering

**Authors:** Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Mike Lewis, Wen-tau Yih

**Year:** 2020

**Venue:** EMNLP 2020

**arXiv ID:** 2004.04906

**ACL Anthology:** https://aclanthology.org/2020.emnlp-main.550/

**arXiv URL:** https://arxiv.org/abs/2004.04906

**GitHub:** https://github.com/facebookresearch/DPR

---

## Key Contributions

### Problem Statement
Traditional sparse retrieval (BM25) suffers from vocabulary mismatch problem. Semantic similarity cannot be captured by exact keyword matching. Needed: Dense embeddings for semantic retrieval.

### Core Innovation: Dual-Encoder Architecture
- **Query Encoder**: BERT-based encoder for queries
- **Passage Encoder**: Separate BERT-based encoder for passages
- **Embedding Space**: Shared latent space where similarity computed via inner product or cosine
- **Efficiency**: Pre-computed passage embeddings stored in vector index (e.g., FAISS)

### Technical Approach

#### Training Process
1. **Contrastive Learning**: Positive pairs (relevant query-passage), negative pairs (irrelevant)
2. **In-batch Negatives**: Use other queries' positive passages as negatives
3. **Hard Negative Mining**: Mine additional negatives from BM25 retrieval to improve training
4. **Loss Function**: Pairwise or triplet loss with InfoNCE objective

#### Inference
- Query encoded once
- Nearest neighbor search against pre-indexed passage embeddings
- Top-k passages retrieved via FAISS or similar ANN method
- Sub-millisecond latency for billion-scale corpora

---

## Performance Results

### Open-Domain QA Benchmarks
- **Natural Questions**: State-of-the-art retrieval accuracy
- **TriviaQA**: Significant improvement over BM25 (9-19% absolute top-20 accuracy)
- **WebQuestions**: Consistent improvements

### Comparison with BM25
- DPR outperforms BM25 by 9-19% in top-20 passage retrieval accuracy
- End-to-end QA system using DPR: New SOTA on multiple benchmarks
- Better semantic understanding of queries and passages

---

## Key Technical Details

### Model Architecture
- **Encoder**: Pre-trained BERT (12 layers, 768 hidden)
- **Dimensionality**: 768-dimensional embeddings
- **Search**: FAISS with inner product similarity
- **Scale**: Evaluated on Wikipedia (~21M passages)

### Training Hyperparameters
- **Batch Size**: 128-256 query-passage pairs
- **Negative Sampling**: In-batch negatives + hard negatives from BM25
- **Learning Rate**: 1e-5
- **Optimization**: Adam optimizer
- **Warmup**: Linear warmup over first 10% of steps

### Indexing and Retrieval
- **Index Type**: FAISS (Flat or IVF with quantization)
- **Retrieval Time**: ~10ms for top-100 passages from 21M corpus
- **Storage**: ~1.6GB for 768-dim embeddings of 21M passages

---

## Research Impact

### Foundational for Modern RAG
- Established dense retrieval as preferred paradigm
- Made practical billion-scale semantic search feasible
- Backbone for most contemporary RAG systems

### Subsequent Advances Built Upon DPR
- **ColBERT** (2020): Token-level late interaction improvements
- **RAG** (2020): First integrated retrieval+generation framework using DPR
- **ANCE** (2021): Improved negative sampling strategies
- **Contriever** (2021): Better pre-training for dense retrieval

---

## Comparison with Other Methods

### vs. BM25 (Sparse Retrieval)
| Aspect | DPR | BM25 |
|--------|-----|------|
| Semantic Understanding | High | Low (keyword-based) |
| Vocabulary Mismatch | Handles naturally | Fails |
| Speed | Fast (pre-computed) | Very fast (inverted index) |
| Explainability | Low | High (matching terms) |

### vs. ColBERT (Token-Level)
- DPR: Single vector per passage (simple, memory-efficient)
- ColBERT: Vector per token (richer, more memory)

### vs. Cross-Encoders
- DPR: Bi-encoder (efficient for large-scale retrieval)
- Cross-encoder: More accurate but too slow for initial retrieval

---

## Limitations

1. **Semantic Drift**: Subtle semantic mismatch between query and passage encodings can accumulate
2. **Vocabulary Mismatch Not Fully Solved**: Some rare concepts still problematic
3. **Training Data Dependency**: Performance heavily depends on quality of training pairs
4. **Computational Cost of Training**: Requires large-scale negative mining
5. **Out-of-Distribution Generalization**: Can struggle on queries/domains very different from training

---

## Practical Implementation Considerations

### FAISS Index Configuration
- **Flat Index**: Exhaustive search, accurate but slow
- **IVF (Inverted File)**: Faster but potential quality loss
- **Product Quantization**: Compression for memory efficiency

### Hard Negative Mining
- Initial retrieval using BM25 to find hard negatives
- Iterative refinement with hard negatives
- Critical for strong performance

### Hybrid Search (DPR + BM25)
- Combine dense and sparse retrieval
- Fusion at scoring level
- Often outperforms either alone

---

## File Metadata
- **Research Area**: Dense Retrieval, Open-Domain QA, Information Retrieval
- **Method Type**: Dual-Encoder, Bi-Encoder
- **Code Availability**: Official implementation at Facebook Research GitHub
- **Reproducibility**: Full experimental details, hyperparameters provided
- **Follow-up Work**: DPR-FID, DPR-ANCE, DPR with hard negatives
