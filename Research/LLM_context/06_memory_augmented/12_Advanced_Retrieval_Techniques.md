# Advanced Retrieval Techniques: FLARE, Active Retrieval, and Query Expansion

## Paper 1: FLARE (Active Retrieval Augmented Generation)

**Title:** Active Retrieval Augmented Generation

**Authors:** Zhengbao Jiang, Frank F. Xu, Luyu Gao, Zhiqing Sun, Qian Liu, Jane Dwivedi-Yu, Yiming Yang, Jamie Kiros, Panupong Pasupat

**Year:** 2023

**Venue:** EMNLP 2023

**arXiv ID:** 2305.06983

**arXiv URL:** https://arxiv.org/abs/2305.06983

**ACL Anthology:** https://aclanthology.org/2023.emnlp-main.495/

**GitHub:** https://github.com/jzbjyb/FLARE

---

## Paper 2: Hypothetical Document Embeddings (HyDE)

**Title:** Precise Zero-Shot Dense Retrieval without Relevance Labels

**Authors:** Luyu Gao, Xueguang Ma, Jimmie Lin, Jamie Kiros

**Year:** 2022

**Venue:** EMNLP 2022 (Findings)

**arXiv ID:** 2212.10496

**arXiv URL:** https://arxiv.org/abs/2212.10496

---

## FLARE: Forward-Looking Active Retrieval

### Problem Statement
Standard RAG retrieves once based on input query. For long-form generation:
- Cannot anticipate information needs during generation
- Generates inaccurate text without retrieval
- Retrieval timing suboptimal (fixed after k tokens)

Need dynamic, adaptive retrieval based on generation quality.

### Core Innovation: Predictive Retrieval Trigger

#### Key Mechanism
```
Generate candidate sentence
  ↓
Evaluate confidence (low-probability tokens?)
  ↓
If low confidence:
  - Retrieve using partial sentence as query
  - Regenerate with retrieved context
  ↓
If high confidence:
  - Continue generation
```

#### How It Works

1. **Forward-Looking**: Predict next sentence
2. **Confidence Check**: Compute token probabilities
3. **Trigger Decision**: Retrieve if confidence < threshold
4. **Retrieve**: Use predicted sentence as query
5. **Regenerate**: Produce sentence again with retrieved context

### Technical Details

#### Confidence Metric
```
confidence = min(p(token_1), p(token_2), ..., p(token_n))
    where p(token_i) = probability of token i

Alternative: Mean probability
confidence = mean(log p(token_1), log p(token_2), ...)
```

#### Retrieval Query Formation
```
If generating: "The capital of France is"
  - Generate candidate: "The capital of France is Madrid"
  - Check confidence on tokens: [Madrid]
  - If low confidence, retrieve using query: "The capital of France is"
  - Get relevant documents
  - Regenerate: "The capital of France is Paris"
```

#### Comparison with Fixed-Interval Retrieval
| Method | Retrieval Trigger | Pros | Cons |
|--------|------------------|------|------|
| **No Retrieval** | Never | Fast | Hallucinations |
| **Fixed Interval** | Every N tokens | Systematic | Unnecessary retrieval |
| **FLARE** | Low confidence | Adaptive | Overhead per check |

### Performance Results

#### Long-Form Generation Tasks
- **ALCE (Retrieval-Augmented Long-Form QA)**: Better performance than fixed-interval
- **ASQA (Aspect-based QA)**: Improved aspect coverage
- **QAMPARI (Multiple Attributes)**: Better handling of multiple attributes

#### Metrics
- **Retrieval Accuracy**: Retrieves relevant information when needed
- **Generation Quality**: Fewer hallucinations
- **Efficiency**: Fewer retrievals than fixed-interval approach

#### Comparisons
- **Better than RAG**: Only retrieves when needed
- **Better than parametric LM**: Grounded in retrieved context
- **Better than Fixed-Interval**: More efficient, better quality

### Advantages
1. **Adaptive**: Retrieves when necessary
2. **Efficient**: Reduces unnecessary retrievals
3. **Flexible**: Works with any retriever
4. **Practical**: Can be added to existing systems

### Limitations
1. **Latency**: Multiple retrievals add overhead
2. **Confidence Calibration**: Threshold selection task-dependent
3. **Rollback Cost**: May need to regenerate text
4. **Partial Sentences**: Retrieving on incomplete text sometimes awkward

---

## HyDE: Hypothetical Document Embeddings

### Problem Statement
Dense retrieval needs query embedding, but:
- Queries are often short and ambiguous
- Semantic gap between short query and long document
- Hard to encode query meaningfully

Solution: Generate hypothetical relevant document, embed that.

### Core Innovation: Generate Then Embed

#### Process
```
Query: "What is DNA?"
  ↓
Generate Hypothetical Answer (using LLM):
"DNA (deoxyribonucleic acid) is a molecule that
carries genetic instructions for living organisms.
It consists of a double helix structure with
four bases: adenine, thymine, guanine, and cytosine.
DNA is found in all living cells..."
  ↓
Embed Hypothetical Answer → Query Embedding
  ↓
Retrieve Real Documents Similar to Hypothesis
```

#### Why It Works
- Hypothetical document richer than query
- Better captures semantic intent
- Shares vocabulary with relevant documents
- Positions query in document space naturally

### Technical Implementation

#### Hypothesis Generation
```python
# Using instruction-following LLM (GPT-3.5)
prompt = f"""
Instruction: Write a document that would answer the following query.

Query: {query}

Hypothetical Document:
"""

hypothesis = llm.generate(prompt, temperature=0.7)
```

#### Zero-Shot Application
- No fine-tuning needed
- Works with any query
- Uses readily available LLM

#### Embedding and Retrieval
```python
# Generate hypothesis
hypothesis = generate_hypothesis(query)

# Embed hypothesis
query_embedding = retriever.encode(hypothesis)

# Retrieve documents
documents = retriever.search(query_embedding, top_k=10)
```

### Performance Results

#### Zero-Shot Evaluation
- **TREC-DL**: Competitive with fine-tuned dense retrievers
- **BEIR Benchmark**: Strong zero-shot performance
- **NQ**: Good performance without domain-specific training

#### Comparison with Fine-tuning
| Method | Training | Performance |
|--------|----------|-------------|
| **BM25** | None | Baseline |
| **DPR** | Fine-tuned | High |
| **HyDE (Zero-shot)** | None | Competitive with DPR |
| **HyDE + Fine-tune** | Fine-tuned | Outperforms DPR |

### Advantages
1. **Zero-Shot**: Works without training data
2. **Simple**: Straightforward pipeline
3. **Modular**: Works with any embedder
4. **Effective**: Competitive with trained methods

### Limitations
1. **Dependency on LLM**: Quality depends on hypothesis generator
2. **Latency**: Hypothesis generation adds overhead
3. **Language-Specific**: Works best in languages with good instruction-following models
4. **Hallucinations**: Generator may produce incorrect hypotheses

---

## Other Advanced Retrieval Techniques

### Query Expansion
**Idea**: Expand query to include related terms

**Methods**:
- **PRF (Pseudo-Relevance Feedback)**: Assume top docs relevant, extract new terms
- **Multi-Query**: Generate multiple queries, union results
- **Chain-of-Thought Expansion**: Use LLM to decompose query

**Benefits**: Improved recall, better handling of ambiguity

### Re-ranking and Re-scoring
**Idea**: Re-rank initial retrieval results using more accurate method

**Methods**:
- **Cross-Encoder Re-ranking**: Use BERT cross-encoder
- **LLM Re-ranking**: Use LLM to score documents
- **RankGPT**: Use GPT for pairwise ranking

**Benefits**: Better top-k precision at cost of latency

### Iterative Retrieval
**Idea**: Retrieve multiple times, refining query based on feedback

**Process**:
1. Initial retrieval
2. Evaluate retrieved documents
3. Refine query if needed
4. Retrieve again
5. Combine results

**Use Cases**: Multi-hop reasoning, complex information needs

### Hybrid Search (Dense + Sparse)
**Idea**: Combine dense and sparse retrieval

**Methods**:
- **Union**: Combine top-k from both methods
- **Intersection**: Keep documents in both top-k
- **Weighted Average**: Combine scores with weights

**Benefits**: Combines semantic and keyword matching

---

## Practical Considerations

### Computational Trade-offs
| Technique | Latency | Accuracy | Complexity |
|-----------|---------|----------|-----------|
| Single retrieval | Low | Medium | Low |
| Re-ranking | Medium | High | Medium |
| Multi-query | High | Medium | Medium |
| Iterative retrieval | Very High | High | High |
| Hybrid search | Medium | High | Medium |

### Implementation Tips

#### For FLARE
```python
def flare_generate(prompt, retriever):
    output = ""
    for step in range(max_steps):
        # Generate next sentence
        partial = generate_next_sentence(output, prompt)

        # Check confidence
        confidence = compute_confidence(partial)

        if confidence < threshold:
            # Retrieve and regenerate
            query = output + partial
            docs = retriever.retrieve(query)
            partial = regenerate_with_context(output, prompt, docs)

        output += partial
        if should_stop(output):
            break

    return output
```

#### For HyDE
```python
def hyde_retrieve(query, retriever, llm):
    # Generate hypothesis
    hypothesis = llm.generate(
        f"Write a document answering: {query}"
    )

    # Embed hypothesis
    embedding = retriever.encode(hypothesis)

    # Retrieve
    documents = retriever.search(embedding, top_k=k)

    return documents
```

---

## Comparison: FLARE vs HyDE

| Aspect | FLARE | HyDE |
|--------|-------|------|
| **Purpose** | Adaptive retrieval during generation | Better query representation |
| **When to Use** | Long-form generation | Any retrieval task |
| **Overhead** | Multiple retrievals | Single hypothesis generation |
| **Effectiveness** | Better confidence | Better query-doc alignment |
| **Complexity** | Medium | Low |

---

## Recent Variations (2024-2025)

### Multi-Hop Retrieval with Planning
- Decompose complex queries into sub-queries
- Retrieve for each sub-query
- Synthesize answers across retrievals

### Retrieval-Augmented Reasoning
- Use retrieved information for reasoning steps
- Generate reasoning traces
- Improve interpretability

### Retrieval with Fallback Strategies
- Primary retrieval strategy
- Fallback to broader search if needed
- Cascade of retrieval methods

---

## File Metadata
- **Research Area**: Adaptive Retrieval, Query Representation, Long-Form Generation
- **Method Types**: Confidence-Based Retrieval, Query Expansion
- **Publication Status**: Published (EMNLP 2023, EMNLP 2022)
- **Code Availability**: Official implementations available
- **Reproducibility**: Good experimental documentation

## Cross-References
- Related to: RAG, Self-RAG, CRAG
- Foundation for: Iterative RAG, Multi-hop retrieval
- Used in: Production RAG systems for long-form generation
