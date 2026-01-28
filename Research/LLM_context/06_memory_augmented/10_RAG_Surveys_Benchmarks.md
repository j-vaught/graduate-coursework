# RAG Surveys, Evaluation, and Benchmarks

## Major Survey Papers (2023-2025)

### Survey 1: General RAG Survey (2023)
**Title:** Retrieval-Augmented Generation for Large Language Models: A Survey

**arXiv ID:** 2312.10997

**Year:** 2023

**URL:** https://arxiv.org/abs/2312.10997

---

### Survey 2: RAG Evaluation Survey (2024)
**Title:** Evaluation of Retrieval-Augmented Generation: A Survey

**Authors:** Peter, et al.

**arXiv ID:** 2405.07437

**Year:** 2024

**URL:** https://arxiv.org/abs/2405.07437

**GitHub:** https://github.com/YHPeter/Awesome-RAG-Evaluation

---

### Survey 3: Comprehensive RAG Architecture Survey (2025)
**Title:** Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers

**arXiv ID:** 2506.00054

**Year:** 2025

**URL:** https://arxiv.org/abs/2506.00054

---

### Survey 4: Graph RAG Survey (2024)
**Title:** Graph Retrieval-Augmented Generation: A Survey

**arXiv ID:** 2408.08921

**Year:** 2024

**URL:** https://arxiv.org/abs/2408.08921

---

## RAG Paradigm Evolution

### Naive RAG (2020-2022)
**Architecture**:
```
Input Query
  ↓
Retrieve: Get top-k documents
  ↓
Concatenate: Put documents in context
  ↓
Generate: LLM produces answer
```

**Characteristics**:
- Simple, straightforward pipeline
- No feedback or refinement
- Fixed retrieval count (top-k)
- May include irrelevant documents

**Pros**: Easy to implement, baseline effectiveness
**Cons**: No quality control, inflexible retrieval

### Advanced RAG (2022-2024)
**Enhancements**:
1. **Retrieval**: Improve quality (better embeddings, re-ranking)
2. **Augmentation**: Better document processing, summaries
3. **Generation**: Improved prompting, chain-of-thought
4. **Fusion**: Combine multiple retrieval methods
5. **Iteration**: Multi-round retrieval and generation

**Methods**: Self-RAG, CRAG, FLARE, Active Retrieval

**Characteristics**:
- Adaptive, dynamic retrieval
- Quality evaluation and filtering
- Multiple retrieval stages
- Iterative refinement

**Pros**: Better accuracy, more efficient, adaptable
**Cons**: Higher complexity, more computational cost

### Modular RAG (2024-2025)
**Architecture**:
```
Query Analysis
  ↓
Route to Specific Module
  ├─ Fast Retrieval Path
  ├─ Slow Accurate Path
  ├─ Knowledge Graph Path
  └─ Web Search Path
  ↓
Combine Outputs
  ↓
Generate
```

**Characteristics**:
- Pluggable components
- Task-specific optimization
- Flexible routing
- Multiple knowledge sources

---

## Key RAG Evaluation Frameworks

### RAG Evaluation Pyramid (Auepora)

#### Level 1: Component Evaluation
- **Retriever Evaluation**:
  - Recall: Does retriever find relevant documents?
  - Precision: Are retrieved documents relevant?
  - MRR/NDCG: Ranking quality
  - Metrics: Top-10/20 accuracy

- **Generator Evaluation**:
  - Fluency: Is text grammatical and coherent?
  - Relevance: Does answer address query?
  - Factuality: Is answer factually correct?
  - Faithfulness: Does answer follow retrieved context?

#### Level 2: Integration Evaluation
- **Context Relevance**: Do retrieved documents support query?
- **Answer Relevance**: Does answer address input query?
- **Answer Faithfulness**: Is answer grounded in retrieved context?
- **Hallucination Rate**: % of answers with ungrounded claims

#### Level 3: End-to-End Evaluation
- **Task Performance**: Downstream task accuracy
- **User Satisfaction**: Human evaluation of helpfulness
- **Robustness**: Performance under adversarial inputs
- **Efficiency**: Latency and computational cost

---

## Major RAG Benchmarks

### CRAG Benchmark (2024)
**Focus**: Comprehensive RAG evaluation

**Dataset Characteristics**:
- **Size**: 5,000+ questions
- **Domains**: Finance, medicine, law, science, technology
- **Question Types**: 8 different types (factoid, complex, multi-doc, etc.)
- **Evaluation**: Multiple metrics per question

**Features**:
- Diverse domain coverage
- Multiple reasoning types
- Real-world complexity

### RAGBench (2024)
**Focus**: Explainable benchmark for RAG

**Dataset**:
- **Size**: 100,000+ examples
- **Coverage**: Open-domain QA, fact verification, summarization
- **Annotation**: Detailed relevance and retrieval labels

**Key Contribution**: Explainability through detailed annotations

### Natural Questions (2019)
**Original Focus**: Open-domain QA

**Dataset**:
- **Size**: 320K questions
- **Source**: Google search queries
- **Annotations**: Multiple answer spans
- **Standard for**: Evaluating DPR, RAG, FiD

### TriviaQA (2017)
**Original Focus**: Trivia question answering

**Dataset**:
- **Size**: 950K QA pairs
- **Coverage**: Diverse topics
- **Multiple Evidence**: Wikipedia and web evidence
- **Hard Negatives**: Challenging for retrieval

---

## Recent Benchmark Innovations (2024-2025)

### RGB: Robustness Evaluation
**Focuses On**:
1. **Noise Robustness**: Irrelevant documents in retrieval
2. **Negative Rejection**: Rejecting non-answers
3. **Information Integration**: Combining multiple sources
4. **Counterfactual Resistance**: Handling contradictions

### RAGTruth: Hallucination Annotation
**Dataset**:
- 18,000+ annotated examples
- QA, summarization, data-to-text tasks
- Response-level and span-level labels
- Detailed hallucination analysis

### Meta CRAG Benchmark (KDD 2024)
**Focus**: Industry-standard RAG evaluation

**Features**:
- Real-world queries
- Domain-specific challenges
- Practical deployment scenarios
- Competition track

---

## Evaluation Metrics in Detail

### Retrieval Metrics

**Recall@k**
```
Recall@k = (# relevant docs in top-k) / (total # relevant docs)
Range: [0, 1]
Interpretation: Can retriever find all relevant documents?
```

**Precision@k**
```
Precision@k = (# relevant docs in top-k) / k
Range: [0, 1]
Interpretation: What % of top-k documents are relevant?
```

**MRR (Mean Reciprocal Rank)**
```
MRR = (1 / rank of first relevant document)
Range: [0, 1]
Interpretation: How quickly does retriever find first match?
```

**NDCG (Normalized Discounted Cumulative Gain)**
```
NDCG@k = (DCG@k) / (Ideal DCG@k)
DCG@k = Σ (relevance_i / log2(i+1))
Interpretation: Ranking quality considering position
```

### Generation Metrics

**BLEU, ROUGE, METEOR**
- **BLEU**: n-gram overlap with reference
- **ROUGE**: Longest common subsequence-based
- **METEOR**: Synonym-aware matching
- **Limitation**: Lexical match, not semantic

**Semantic Metrics**
- **BERTScore**: Contextual token similarity
- **BLEURT**: Learned metric (trained on human judgments)
- **ChrF**: Character-level n-gram similarity

**Factuality-Specific Metrics**
- **Faithfulness Score**: Answer grounded in context? (0-1)
- **Answer Relevance**: Answer addresses query? (0-1)
- **Context Relevance**: Retrieved context relevant? (0-1)

### LLM-as-Judge Evaluation
```
Prompt to LLM:
"Given query: {query}
Retrieved context: {context}
Generated answer: {answer}

Evaluate on:
- Faithfulness (0-10): Is answer grounded in context?
- Relevance (0-10): Does answer address query?
- Coherence (0-10): Is answer well-written?"

Score = Average of three dimensions
```

**Pros**: Semantic understanding, handles nuance
**Cons**: LLM-dependent, potential bias, more expensive

---

## Chunking Strategies and Their Impact

### Fixed-Size Chunking
- **Method**: Split documents into n-token chunks
- **Typical Size**: 256-512 tokens, 50% overlap
- **Pros**: Simple, deterministic, predictable
- **Cons**: Breaks semantics, arbitrary boundaries
- **Impact on RAG**: Medium retrieval quality, fast processing

### Semantic Chunking
- **Method**: Split at semantic boundaries (sentences, paragraphs)
- **Tool**: Using NLP to identify boundaries
- **Pros**: Preserves meaning, natural units
- **Cons**: Variable chunk sizes, more computation
- **Impact on RAG**: Better retrieval, more flexible

### Recursive Chunking
- **Method**: Try multiple separators (paragraph → sentence → character)
- **Tool**: LangChain default strategy
- **Pros**: Balanced chunks, respects hierarchy
- **Cons**: More complex logic
- **Impact on RAG**: Good retrieval quality, moderate speed

### LLM-Based Chunking
- **Method**: Use LLM to intelligently chunk
- **Tool**: Prompt LLM to decide chunk boundaries
- **Pros**: Semantic awareness, high quality
- **Cons**: Expensive, slow, less deterministic
- **Impact on RAG**: Best retrieval quality, high cost

### Agentic Chunking
- **Method**: Agent analyzes document, decides chunking strategy
- **Tool**: Multi-step decision process
- **Pros**: Adaptive to document type, high quality
- **Cons**: Complex, expensive
- **Impact on RAG**: Optimal per-document, highest cost

---

## Metrics for Different RAG Scenarios

### For Open-Domain QA
- **Recall@k**: Can retriever find answer?
- **Exact Match**: Exact answer in top-k?
- **F1 Score**: Partial credit for close matches

### For Long-Form Generation
- **ROUGE**: Overlap with reference
- **BERTScore**: Semantic similarity
- **Faithfulness**: No hallucination

### For Fact Verification
- **Precision**: Avoid false positives
- **Recall**: Don't miss real facts
- **Supported/Refuted**: Classification accuracy

---

## Benchmarking Best Practices

### Comprehensive Evaluation
1. **Multiple Datasets**: Test across domains
2. **Multiple Metrics**: Use complementary metrics
3. **Human Evaluation**: Spot-check results
4. **Error Analysis**: Understand failure modes

### Avoiding Pitfalls
1. **Data Leakage**: Ensure test set separate from training
2. **Metric Gaming**: Avoid optimizing for wrong metric
3. **Statistical Significance**: Report confidence intervals
4. **Reproducibility**: Document all hyperparameters

### Baselines and Comparisons
1. **Weak Baseline**: Simple baseline (e.g., BM25 only)
2. **Strong Baseline**: Established methods (RAG, DPR)
3. **State-of-the-art**: Latest methods
4. **Ablation Study**: Understand component contributions

---

## File Metadata
- **Research Area**: RAG Evaluation, Benchmarking, Metrics
- **Focus Areas**: Comprehensive surveys, standard benchmarks
- **Publication Status**: Multiple surveys published/in prep
- **Data Availability**: Most benchmarks publicly available
- **Code Availability**: Evaluation frameworks available
- **Reproducibility**: Detailed evaluation protocols documented

## Cross-References
- Related Surveys: General NLP evaluation, QA benchmarks
- Connected to: All RAG papers (methods evaluated on benchmarks)
- Tools: MTEB (Massive Text Embeddings Benchmark), LangChain Eval
