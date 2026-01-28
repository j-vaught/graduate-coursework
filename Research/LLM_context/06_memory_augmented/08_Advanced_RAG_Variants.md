# Advanced RAG Variants: Self-RAG, CRAG, GraphRAG, and Beyond

## Paper 1: Self-RAG (Asai et al. 2023)

**Title:** Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection

**Authors:** Akari Asai, Zeqiu Wu, Yizhong Wang, Avirup Sil, Hannaneh Hajishirzi

**Year:** 2023

**Venue:** ICLR 2024

**arXiv ID:** 2310.11511

**arXiv URL:** https://arxiv.org/abs/2310.11511

**Official Website:** https://selfrag.github.io/

**GitHub:** https://github.com/AkariAsai/self-rag

---

## Paper 2: CRAG (Yan et al. 2024)

**Title:** Corrective Retrieval Augmented Generation

**Authors:** Yan, et al.

**Year:** 2024

**Venue:** ACL/Major Conference

**arXiv ID:** 2401.15884

**arXiv URL:** https://arxiv.org/abs/2401.15884

**GitHub:** https://github.com/HuskyInSalt/CRAG

---

## Paper 3: GraphRAG (Microsoft Research)

**Title:** Retrieval-Augmented Generation with Graphs

**Authors:** Microsoft Research

**Year:** 2024-2025

**arXiv ID:** 2501.00309

**Official Website:** https://microsoft.github.io/graphrag/

**GitHub:** https://github.com/microsoft/graphrag

**Survey:** https://arxiv.org/abs/2408.08921 - Graph Retrieval-Augmented Generation: A Survey

---

## Self-RAG: Adaptive Retrieval with Self-Critique

### Problem Statement
Standard RAG indiscriminately retrieves fixed number of passages regardless of whether retrieval is necessary or whether passages are relevant. This can degrade performance by:
- Adding noise from irrelevant passages
- Reducing model flexibility
- Forcing retrieval even when parametric knowledge sufficient

### Core Innovation: Reflection Tokens

#### Token Types
1. **Retrieval Token**: Decides whether retrieval is needed
   - `[Ret]`: Decide to retrieve
   - `[NoRet]`: Use parametric knowledge

2. **Relevance Token**: Evaluates passage relevance
   - `[Rel]`: Passage supports generation
   - `[Irrel]`: Passage not relevant

3. **Critique Token**: Evaluates response quality
   - `[Utility]`: Response is useful
   - `[NonUtil]`: Response not useful

#### How It Works
```
Input: Query
  ↓
Generate/Predict: Should retrieve? (Retrieval token)
  ↓
If Retrieval Decision = Retrieve:
  - Retrieve passages
  - For each passage: Evaluate relevance token
  - Keep only [Rel] passages
  ↓
Generate: Final answer
  ↓
Self-Critique: Is output good? (Critique token)
  ↓
Output: Final response
```

### Key Features
- **Adaptive Retrieval**: Retrieves only when beneficial
- **Controllable Generation**: Can adjust behavior via token manipulation
- **Self-Reflective**: Learns to evaluate own outputs
- **Single Model**: No separate retriever; integrated in main LM

### Performance
- **7B and 13B Models**: Outperforms ChatGPT and Llama2-chat
- **Open-Domain QA**: Superior accuracy
- **Fact Verification**: Better factuality and citation
- **Reasoning Tasks**: Improved complex reasoning

### Advantages
1. Reduces hallucination through selective retrieval
2. More efficient than always-retrieve RAG
3. Better factuality and citation accuracy
4. Interpretable retrieval decisions

---

## CRAG: Corrective Retrieval-Augmented Generation

### Problem Statement
Standard RAG assumes retrieved documents are relevant. In practice, retrieval often fails:
- Irrelevant documents retrieved
- Missing information
- Conflicting information

Need mechanism to evaluate and correct retrieval quality.

### Core Innovation: Retrieval Evaluator

#### Evaluation Process
```
Input: Query
  ↓
Retrieve: Top-k documents
  ↓
Evaluate: Check document quality
  - Compute confidence score
  - If confidence low: Trigger corrective action
  ↓
If Confidence High:
  - Proceed with retrieved docs
  Else:
  - Perform web search
  - Refine retrieval
  ↓
Generate: Final answer
```

#### Confidence Threshold Strategy
- Threshold: ~70% document relevance
- If < 70% relevant: Declare retrieval failure
- Corrective Actions:
  1. **Web Search**: Broaden search to internet
  2. **Local Search**: Expand query, retrieve more
  3. **Decompose**: Break query into sub-queries

### Key Metrics
- **Relevance Evaluation**: What % of documents are truly relevant?
- **Confidence Score**: How confident is retriever?
- **Ambiguity Handling**: When query is ambiguous, expand search

### Performance
- Significantly reduces hallucinations
- Better accuracy than vanilla RAG
- Plug-and-play with any RAG pipeline

### Advantages
1. Self-aware: Knows when retrieval fails
2. Corrective: Takes action to improve
3. Flexible: Multiple corrective strategies
4. Robust: Handles retrieval failures

---

## GraphRAG: Graph-Based Retrieval-Augmented Generation

### Problem Statement
Standard RAG uses flat text chunks. Doesn't capture:
- Relationships between entities
- Hierarchical information structure
- Complex dependencies across documents
- Context for synthesizing information

### Core Innovation: Knowledge Graph Structure

#### Processing Pipeline
```
Raw Text → Entity/Relationship Extraction → Knowledge Graph
            ↓
        Community Detection (Hierarchical)
            ↓
        Generate Summaries
            ↓
        Index for Retrieval
            ↓
        Query-Time Retrieval
```

#### Graph Components
1. **Nodes**: Entities (people, places, concepts)
2. **Edges**: Relationships between entities
3. **Attributes**: Properties of entities/relationships
4. **Communities**: Hierarchical groupings

#### Query Modes

**Local Search**: For specific entity queries
```
Query: "Tell me about person X"
  ↓
Find X in graph
  ↓
Retrieve X's properties
  ↓
Fan-out to neighbors
  ↓
Summarize neighbor information
  ↓
Generate response
```

**Global Search**: For broad/holistic questions
```
Query: "What is the overall structure?"
  ↓
Traverse community hierarchy
  ↓
Retrieve community summaries
  ↓
Synthesize across communities
  ↓
Generate comprehensive answer
```

### Key Components
1. **Entity Recognition**: Extract entities from text
2. **Relationship Detection**: Identify connections
3. **Community Structure**: Group related entities
4. **Hierarchical Summaries**: Summaries at each level
5. **Semantic Index**: Enable fast retrieval

### Performance
- **Precision**: Up to 35% improvement over vector-only retrieval
- **Context Coverage**: More comprehensive context
- **Reasoning**: Better for multi-hop reasoning
- **Interpretability**: Explicit relationships visible

### Advantages
1. Captures relationships: Not just text similarity
2. Hierarchical: Natural summaries at different levels
3. Comprehensive: Multiple paths to answer
4. Structured: Explicit graph provides interpretability

---

## Comparative Analysis

### When to Use Each

| Method | Best For | Limitations |
|--------|----------|-------------|
| **Self-RAG** | Mixed queries (some need retrieval) | Single model, inference overhead |
| **CRAG** | Unreliable retrieval scenarios | Requires confidence evaluation |
| **GraphRAG** | Complex relationships, multi-hop | Requires entity extraction |

### Combining Approaches
- **Self-RAG + CRAG**: Adaptive + corrective retrieval
- **Self-RAG + GraphRAG**: Adaptive + structured retrieval
- **CRAG + GraphRAG**: Corrective graph-based retrieval

---

## Technical Implementation Details

### Self-RAG Implementation
```python
# Model learns to generate reflection tokens
def generate_with_reflection(query):
    # Step 1: Should retrieve?
    retrieval_token = model.predict_token(query)

    if retrieval_token == "[Ret]":
        documents = retrieve(query)
        # Step 2: Filter by relevance
        relevant = [d for d in documents
                   if model.predict_relevance(query, d) == "[Rel]"]
    else:
        relevant = []

    # Step 3: Generate
    answer = model.generate(query, relevant)

    # Step 4: Evaluate
    critique = model.predict_critique(query, answer)
    return answer, critique
```

### CRAG Implementation
```python
def corrective_rag(query):
    docs = retrieve(query)

    # Evaluate quality
    confidence = evaluate_relevance(query, docs)

    if confidence < 0.7:
        # Corrective action
        if ambiguous(query):
            docs += expand_search(query)
        else:
            docs += web_search(query)

    answer = generate(query, docs)
    return answer
```

### GraphRAG Implementation
```python
def graph_rag(query):
    # Extract entities from query
    entities = extract_entities(query)

    # Decide: Local or Global search?
    if specific_entity(query):
        # Local search
        relevant = local_search(entities, graph)
    else:
        # Global search
        relevant = global_search(query, graph)

    # Generate from retrieved context
    answer = generate(query, relevant)
    return answer
```

---

## Research Impact and Future Directions

### Impact
- **Self-RAG**: Showed models can learn to be selective about retrieval
- **CRAG**: Introduced retrieval evaluation and correction
- **GraphRAG**: Demonstrated power of structured knowledge

### Recent Extensions
1. **Dynamic Retrieval**: Retrieve multiple times during generation
2. **Iterative Refinement**: Refine based on feedback
3. **Multi-Source Fusion**: Combine multiple retrieval strategies
4. **Uncertainty Quantification**: Explicit uncertainty tracking

---

## File Metadata
- **Research Area**: Advanced RAG, Retrieval Control, Knowledge Graphs
- **Method Types**: Adaptive Retrieval, Corrective RAG, Structured Retrieval
- **Publication Status**: Published/arXiv preprints
- **Code Availability**: Official implementations released
- **Reproducibility**: Good experimental documentation

## Related Papers
- RAG (Lewis et al. 2020): Foundation for all variants
- DPR (Karpukhin et al. 2020): Underlying retriever
- REALM (Guu et al. 2020): Pre-training with retrieval
- RETRO (Borgeaud et al. 2022): Retrieval in pre-training
