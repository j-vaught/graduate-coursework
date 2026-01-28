# Embedding Models and Retrieval Architectures

## Paper 1: Sentence-BERT (Reimers & Gurevych 2019)

**Title:** Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks

**Authors:** Nils Reimers, Iryna Gurevych

**Year:** 2019

**Venue:** EMNLP 2019

**arXiv ID:** 1908.10084

**arXiv URL:** https://arxiv.org/abs/1908.10084

**ACL Anthology:** https://aclanthology.org/D19-1410/

**Official Website:** https://www.sbert.net/

**GitHub:** https://github.com/UKPLab/sentence-transformers

---

## Paper 2: ColBERT (Khattab & Zaharia 2020)

**Title:** ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT

**Authors:** Omar Khattab, Matei Zaharia

**Year:** 2020

**Venue:** SIGIR 2020

**PDF:** https://people.eecs.berkeley.edu/~matei/papers/2020/sigir_colbert.pdf

**GitHub:** Multiple implementations available

---

## Sentence-BERT: Semantic Similarity at Scale

### Problem Statement
Standard BERT requires feeding both sentences to model in cross-encoder fashion:
- Computational Cost: O(n²) for n sentences
- Latency: ~1 second per sentence pair
- Impractical for semantic search across large collections

Solution needed: Fast semantic similarity via embeddings.

### Core Innovation: Siamese BERT Networks

#### Architecture Overview
```
Sentence A → BERT Encoder → Mean Pooling → Embedding_A
                                               ↓
                                           Cosine Similarity
                                               ↑
Sentence B → BERT Encoder → Mean Pooling → Embedding_B
```

#### Key Components
1. **Dual Encoding**: Process sentences independently
2. **Shared Parameters**: Same BERT weights for both encoders
3. **Pooling Strategy**: Mean-pool over token embeddings
4. **Similarity Metric**: Cosine similarity in embedding space

### Training Strategy

#### Siamese Network Training
- **Input Pairs**: (sentence_a, sentence_b, label)
- **Loss Function**: Triplet loss or Contrastive loss
- **Triplet Loss**: L = max(0, m + sim(anchor, neg) - sim(anchor, pos))
  - m: margin parameter
  - pos: positive example
  - neg: negative example

#### Data for Training
- **Supervised**: Sentence pairs with similarity labels (NLI)
- **Unsupervised**: Duplicate sentence pairs
- **Pre-training**: STS (Semantic Textual Similarity) datasets

### Embedding Properties
- **Dimensionality**: 384 (small SBERT) to 768 (base SBERT)
- **Interpretability**: Semantic direction in embedding space
- **Compositionality**: Average embeddings for longer texts
- **Language-Agnostic**: Multilingual variants available

### Performance Results

#### Speed Improvements
- **Inference Time**: ~65 hours (BERT cross-encoder) → ~5 seconds (SBERT)
- **Search Speed**: ~1000× faster for semantic search
- **Scalability**: Can handle millions of documents

#### Accuracy Preservation
- Maintains comparable accuracy to cross-encoders
- Slight trade-off: 1-2% accuracy loss for 1000× speedup
- Often preferable: Speed gain outweighs small accuracy loss

#### Downstream Tasks
- **Semantic Search**: Excellent performance
- **Semantic Textual Similarity**: State-of-the-art on STS benchmarks
- **Clustering**: Natural clustering properties
- **Paraphrase Mining**: Effective paraphrase detection

### Advantages
1. **Efficiency**: Pre-compute embeddings, fast inference
2. **Simplicity**: Easy to use, minimal dependencies
3. **Flexibility**: Works with any text length
4. **Transfer Learning**: Generalizes across domains

---

## ColBERT: Token-Level Dense Retrieval

### Problem Statement
Dense retrievers (like DPR) create single embedding per passage:
- Information Loss: Rich token-level details lost in aggregation
- Late Interaction: Query and passage interact late (after aggregation)
- Trade-off: Either accurate (slow) or efficient (fast)

### Core Innovation: Late Interaction with Token-Level Embeddings

#### Architecture Overview
```
Query: "Who won the World Cup?"
  ↓
BERT Encode → Token Embeddings [who: emb_1, won: emb_2, ...]
  ↓
Per-Token Representation

Passage: "France won the 2022 World Cup in Qatar"
  ↓
BERT Encode → Token Embeddings [France: emb_a, won: emb_b, ...]
  ↓
Per-Token Representation
  ↓
Similarity: Max pooling of token similarities
  = max(emb_1·emb_a, emb_1·emb_b, ..., emb_2·emb_a, emb_2·emb_b, ...)
```

#### Key Components
1. **Token-Level Embeddings**: Preserve granularity
2. **Contextualized Representations**: BERT handles context
3. **Late Interaction**: Compute similarity after encoding
4. **Max Pooling**: Conservative aggregation (most similar tokens count)

### Technical Details

#### Similarity Computation
```
Score(Query Q, Passage P) = Σ_q max_p (Q[q] · P[p])
    where:
    - Q[q]: Query token q's embedding
    - P[p]: Passage token p's embedding
    - max_p: Maximum similarity across all passage tokens
```

This means each query token needs to find its best match in passage.

#### Storage and Indexing
- **Vector Storage**: One vector per token (not per passage)
- **Index Structure**: FAISS or similar for fast retrieval
- **Memory Trade-off**: Higher memory than single-vector (but quantizable)
- **Retrieval Speed**: Similar to DPR despite richer representation

### Performance Results

#### Accuracy
- **Retrieval Accuracy**: Outperforms DPR by 2-5%
- **End-to-end QA**: Better than single-vector methods
- **Correlation**: Stronger correlation with downstream performance

#### Efficiency Trade-offs
- **Faster than Cross-Encoders**: 1000× speedup vs. BERT-based re-rankers
- **Slower than DPR**: 10-100× slower than simple inner product
- **Practical Speed**: Milliseconds per query on modern hardware

#### Interpretability
- Can see which tokens matched which documents
- Explainable retrieval (unlike black-box dense methods)
- Easier debugging of retrieval failures

---

## Comparative Analysis: SBERT vs ColBERT

| Aspect | Sentence-BERT | ColBERT |
|--------|---------------|---------|
| **Representation** | Single vector | Multi-vector (per token) |
| **Interaction** | Late | Late (but at token level) |
| **Memory** | Low (1 vector/passage) | Higher (tokens/passage) |
| **Accuracy** | Good | Excellent |
| **Speed** | Very fast | Fast |
| **Interpretability** | Limited | High |
| **Use Case** | Fast search | Accurate retrieval |

---

## Embedding Model Ecosystem

### Available Models (2024-2025)
- **Sentence-Transformers**: 10,000+ pre-trained models on Hugging Face
- **Multilingual Models**: Support for 100+ languages
- **Domain-Specific**: Scientific papers, medical texts, code
- **Instruction-Following**: E.g., E5, BGE models with instructions

### Model Selection Criteria
1. **Task-Specific Fine-tuning**: Better performance than general models
2. **Domain Relevance**: Domain-specific models outperform generic
3. **Language Support**: Multilingual for cross-lingual applications
4. **Dimension Trade-off**: Smaller dimensions (256) vs. larger (1024)

---

## Advanced Retrieval Architectures

### Hybrid Retrieval: Combining Dense and Sparse
```
Query
  ├─ Dense Retrieval (SBERT/ColBERT) → Top 100 documents
  └─ Sparse Retrieval (BM25) → Top 100 documents
       ↓
   Union/Intersection → Rerank
       ↓
   Top-k documents
```

Benefits: Combines semantic and keyword matching.

### Multi-Stage Retrieval
```
Stage 1: Dense Retrieval (Fast, approximate)
  Query → 100 candidates

Stage 2: Semantic Reranking (Accurate)
  Top 100 → ColBERT re-rank → Top 20

Stage 3: Cross-Encoder (Most accurate)
  Top 20 → BERT cross-encoder → Top 10
```

Benefits: Balance speed and accuracy.

### Learned Sparse Retrieval (uniLM, SPLADE)
```
Input: Query → BERT → Output: Sparse weights over vocabulary
  ↓
Weighted bag-of-words for retrieval
  ↓
Combines benefits of dense (semantic) and sparse (interpretable)
```

---

## Practical Implementation

### Using Sentence-Transformers
```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Encode documents
documents = [...]
embeddings = model.encode(documents)

# Semantic search
query_embedding = model.encode(query)
similarities = util.pytorch_cos_sim(query_embedding, embeddings)
top_k = torch.topk(similarities, k=5)
```

### Using ColBERT
```python
from colbert.infra import ColBERTConfig
from colbert import Indexer, Searcher

# Index documents
config = ColBERTConfig(doc_maxlen=220, nbits=1)
indexer = Indexer(checkpoint=checkpoint, config=config)
indexer.index(name="documents", collection=documents)

# Search
searcher = Searcher(index="documents")
results = searcher.search(query, k=10)
```

---

## Embedding Space Properties

### Desirable Properties
1. **High Intra-Class Similarity**: Similar texts close together
2. **Low Inter-Class Similarity**: Different texts far apart
3. **Isotropy**: Embeddings uniformly distributed
4. **Compositionality**: Mean of embeddings meaningful
5. **Robustness**: Small text changes produce small embedding changes

### Common Issues
- **Isotropy**: Some embedding spaces skew toward certain directions
- **Domain Shift**: Models perform worse on out-of-domain text
- **Scaling**: Performance degrades with corpus size
- **Ambiguity**: Polysemous terms encode multiple meanings

---

## Retrieval Evaluation Metrics

### Standard Metrics
- **MRR (Mean Reciprocal Rank)**: Position of first relevant document
- **NDCG (Normalized Discounted Cumulative Gain)**: Ranking quality
- **Recall@k**: % of relevant documents in top-k
- **Precision@k**: % of top-k documents that are relevant

### RAG-Specific Metrics
- **Context Relevance**: Retrieved documents relevant to query
- **Answer Faithfulness**: Generated answer faithful to retrieved context
- **Answer Relevance**: Generated answer addresses query

---

## File Metadata
- **Research Area**: Semantic Embeddings, Dense Retrieval, Information Retrieval
- **Method Types**: Siamese Networks, Token-Level Embeddings, Late Interaction
- **Publication Tier**: Top-tier (EMNLP, SIGIR)
- **Citation Count**: Highly cited (1000s+)
- **Code Availability**: Official implementations released
- **Reproducibility**: Excellent; pre-trained models widely available

## Cross-References
- Related to: DPR, RAG, Neural Retrieval
- Foundation for: Self-RAG, CRAG, GraphRAG
- Used in: All modern RAG systems
