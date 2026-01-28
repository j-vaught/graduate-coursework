# Dialogue History Retrieval and Relevance Ranking

## Overview
Dialogue history retrieval systems identify relevant past context from long conversation records using semantic similarity, relevance ranking, and multi-granularity retrieval approaches to improve context-aware response generation.

## Core Research

### Primary Papers

1. **Effective and Efficient Conversation Retrieval for Dialogue State Tracking with Implicit Text Summaries**
   - Venue: arXiv
   - Year: 2024
   - ID: 2402.13043
   - Key Findings:
     - Text summaries effective for conversation retrieval
     - LLM-based conversation summarizer for query generation
     - Multi-key and multi-query retrieval strategy
     - Re-ranking retrieved dialogues by similarity
   - URL: https://arxiv.org/html/2402.13043v1

2. **Evaluating Very Long-Term Conversational Memory of LLM Agents**
   - Source: LoCoMo (SNAP Research)
   - Year: 2024
   - ID: 2402.17753
   - Key Findings:
     - Benchmark for evaluating long-term memory
     - Agent ability to reference information from 1M+ tokens ago
     - Memory degradation over time
     - Retrieval effectiveness in extended interactions
   - URL: https://arxiv.org/html/2402.17753v1
   - Project: https://snap-research.github.io/locomo/

3. **BEYOND A MILLION TOKENS: BENCHMARKING AND ENHANCING LONG-TERM MEMORY IN LLMS**
   - Venue: arXiv
   - Year: 2024
   - ID: 2510.27246
   - Key Findings: Evaluation and improvement of memory beyond 1M tokens
   - URL: https://www.arxiv.org/pdf/2510.27246

4. **In Prospect and Retrospect: Reflective Memory**
   - Venue: arXiv
   - Year: 2025
   - Key Findings: Reflective approach to memory management
   - URL: https://arxiv.org/pdf/2503.08026

5. **Generate then Retrieve: Conversational Response Retrieval Using LLMs as Answer and Query Generators**
   - Venue: arXiv
   - Year: 2024
   - ID: 2403.19302
   - Key Findings:
     - Two-stage retrieval: generate then retrieve
     - LLM as query generator
     - LLM as potential answer generator
     - Improves conversational context matching
   - URL: https://arxiv.org/html/2403.19302v1

### Implementation Guides

6. **Conversational Memory for LLMs with Langchain**
   - Author: Pinecone
   - Platform: Pinecone Learning Series
   - Year: 2024
   - Key Findings: Practical implementation in LangChain framework
   - URL: https://www.pinecone.io/learn/series/langchain/langchain-conversational-memory/

7. **Enhancing RAG and Knowledge Graphs with Discourse**
   - Author: Boris Galitsky
   - Venue: Dialogue Conference
   - Year: 2025
   - Key Findings: Integration of discourse analysis with RAG and KG
   - URL: https://dialogue-conf.org/wp-content/uploads/2025/04/GalitskyBIlvovskyDMorkovkinA.110.pdf

8. **Long-Term Dialogue Memory**
   - Source: Emergent Mind
   - Year: 2024
   - Key Findings: Topic overview and resources for long-term dialogue memory
   - URL: https://www.emergentmind.com/topics/long-term-dialogue-memory

## Retrieval Strategies

### 1. Soft Retrieval with Relevance Scoring

**Approach**:
- Soft retrieval based on latest user utterance
- Network outputs relevance score (0-1) for each token in history
- Probabilistic selection rather than hard thresholding

**Mechanism**:
```
Latest Utterance → Encoder
                    ↓
                Neural Network
                    ↓
Conversation History → Scoring Layer
                    ↓
Relevance Scores [0-1]
                    ↓
Weighted Selection
```

**Advantages**:
- Probabilistic, differentiable
- Can be learned end-to-end
- Captures fine-grained relevance
- Soft attention properties

**Implementation**:
```python
def soft_retrieval(history, query, max_context):
    scores = relevance_network(history, query)
    weighted_history = weighted_sum(history, scores)
    return top_k_by_score(weighted_history, max_context)
```

### 2. Summary-Based Retrieval

**Approach**:
- Maintain summaries of conversation segments
- Use summaries as search keys
- Retrieve based on summary-level relevance

**Process**:
```
Conversation Segments (5-10 messages each)
    ↓
LLM Summarization
    ↓
Summary Storage
    ↓
Latest User Input → Summary Queries
                    ↓
Semantic Similarity Search
                    ↓
Top-K Similar Summaries
                    ↓
Full Messages Retrieved
```

**Benefits**:
- Compression before retrieval
- Multiple summary levels possible
- Efficient for very long conversations
- Reduces storage/search cost

**Trade-offs**:
- Summary quality affects retrieval
- Cascading errors with multiple summaries
- Loss of detail in compression

### 3. Multi-Key and Multi-Query Retrieval

**Two-Query Strategy**:
```
Query 1: Latest user utterance
Query 2: Summary of conversation context

Both → Vector DB Search
     → Top-K retrieval per query
     → Merge and re-rank results
```

**Benefits**:
- Captures different relevance signals
- Balances recent turns with broader context
- Reduces missed relevant context
- More robust retrieval

**Re-ranking Process**:
```
Retrieved Dialogues (from both queries)
    ↓
Re-rank by:
  - Similarity to latest utterance
  - Relevance to conversation flow
  - Temporal proximity
    ↓
Top-K Dialogues Return
```

### 4. Dense Retrieval Methods

**Vector Encoding Approach**:
```
Dialogue Context → Encoder (BERT, GPT)
                    ↓
                Dense Vector (768-1024 dims)
                    ↓
Vector Database Storage
                    ↓
Query → Vector Encoder
     → Cosine Similarity / MIPS
     → Top-K by similarity
```

**Advantages**:
- Semantic matching vs keyword
- Sub-millisecond retrieval
- Handles paraphrasing
- Works across languages

**Implementations**:
- Pinecone
- Weaviate
- FAISS
- Milvus

### 5. Adaptive Multi-Granularity Ranking

**Granularity Levels**:
```
Turn-level: Individual speaker turns
Session-level: Dialogue segments/scenes
Summary-level: High-level conversation summaries
Keyword-level: Entity and keyword indices
```

**Retrieval Process**:
```
Query → Entropy-based Router
     → Select retrieval granularity
     → Retrieve at chosen level
     → Aggregate results
     → Return top-K
```

**Advantages**:
- Learns optimal granularity per query
- Flexible in scope
- Handles diverse queries
- Reduces over/under-retrieval

**LD-Agent Approach**:
- Combines semantic similarity
- Topic overlap scoring
- Time decay weighting
- Multi-granularity selection

## Relevance Scoring Components

### 1. Semantic Similarity
```
Relevance_Semantic = cosine(embedding(query), embedding(history_segment))
Range: [0, 1]
```

### 2. Recency Weighting
```
Relevance_Recency = 1 - (current_time - segment_time) / max_history_age
Decays older content
Range: [0, 1]
```

### 3. Importance Scoring
```
Relevance_Importance = learned_importance_score(segment)
Explicit annotation or derived from interaction
Range: [0, 1]
```

### 4. Topic Overlap
```
Relevance_Topic = topic_similarity(query_topics, segment_topics)
Topics extracted from embeddings or NLP
Range: [0, 1]
```

### 5. Combined Scoring
```
Score = α*Semantic + β*Recency + γ*Importance + δ*Topic

Example (equal weights):
Score = 0.25*Semantic + 0.25*Recency + 0.25*Importance + 0.25*Topic
```

## Architecture Patterns

### Pattern 1: Retrieval-Augmented Generation (RAG) for Dialogue

```
User Query
    ↓
[Retrieve Relevant History] ← Conversation Database
    ↓
    [Augment with Retrieved Context]
    ↓
[Generate Response using augmented context]
```

**Implementation**:
```python
def dialogue_rag(user_query, conversation_db, llm):
    # Retrieve relevant history
    relevant_history = retrieve(
        query=user_query,
        db=conversation_db,
        top_k=5
    )

    # Augment context
    context = format_history(relevant_history)

    # Generate response
    response = llm.generate(
        system_prompt=system,
        context=context,
        query=user_query
    )

    return response
```

### Pattern 2: Conversation Summarization + Retrieval

```
Long Conversation
    ↓
[Segment into chunks]
    ↓
[Summarize each chunk]
    ↓
[Store summaries + originals]
    ↓
Query → Search summaries
     → Retrieve original messages
```

### Pattern 3: Memory-Augmented Networks

```
Query → [Attention over Memory]
     → [Read relevant memories]
     → [Generate with augmented context]
```

**Components**:
- External memory (conversation history)
- Addressing mechanism (what to read)
- Reading mechanism (how to extract)
- Integration (combine with generation)

## Dialogue-Specific Challenges

### 1. Pronoun Resolution
```
User: "I want to book a flight"
Agent: "Where would you like to go?"
User: "Can it be non-stop?"  ← "it" = flight (requires history)
```

**Solution**: Retrieve dialogue context with explicit coreference

### 2. Ellipsis Resolution
```
User: "I prefer Italian cuisine"
Agent: "We have several Italian restaurants"
User: "What about their prices?"  ← "their" = restaurants
```

**Solution**: Maintain entity references across history

### 3. Implicit Context
```
User: "The red one"  ← which item?
Agent: "That's $50"  ← referring to previously mentioned item
```

**Solution**: Retrieve full dialogue context for clarification

### 4. Topic Shift Detection
```
Context 1: Restaurant conversation (turns 1-20)
Shift Point: Turn 21 changes topic
Context 2: Movie conversation (turns 21-40)
```

**Solution**: Segment by topic; retrieve within relevant segment

## Evaluation Metrics

### Retrieval Quality
```
Mean Reciprocal Rank (MRR):
MRR = (1/N) * Σ(1/rank_of_first_relevant)

Recall@K:
Recall = (relevant_retrieved) / (total_relevant)
```

### Dialogue Quality
```
BLEU Score: Compare generated response with reference
ROUGE Score: Overlap with reference response
Human Evaluation: Coherence, relevance, naturalness
```

### Task Success
```
Dialogue Task Completion Rate
State Tracking Accuracy
Entity Extraction F1
```

## Real-World Implementation

### Production System Architecture

```
Conversation Database
    ├─ Recent (In-Memory)
    │  └─ Last 50 messages
    ├─ Cached (Redis)
    │  └─ Last 500 messages + embeddings
    └─ Archive (Vector DB)
       └─ Full history + embeddings

Query Routing:
- Recent history → in-memory search
- Medium history → cache + re-rank
- Old history → Vector DB with semantic search
```

### Query Processing Pipeline

```
User Query
    ↓
[Normalize & Encode]
    ↓
[Route to appropriate store]
    ↓
[Retrieve candidates]
    ↓
[Re-rank by relevance]
    ↓
[Aggregate with recent context]
    ↓
Return top-K
```

## Optimization Techniques

### 1. Caching
```
Frequently accessed segments → In-memory cache
Popular queries → Cache results
Embeddings → Pre-compute and cache
```

### 2. Indexing
```
Primary index: Chronological (by timestamp)
Secondary index: Topic-based
Tertiary index: Entity-based
Full-text index: Keyword search
```

### 3. Batch Processing
```
Compute embeddings in batches
Process multiple queries together
Amortize encoding cost
```

### 4. Approximation
```
Approximate nearest neighbor (ANN)
Locality-sensitive hashing (LSH)
Quantization for compression
Trade recall for speed
```

## Open Research Questions

1. Optimal combination of relevance scoring components?
2. Can dialogue-specific features improve retrieval?
3. How to handle temporal dynamics in topic shift?
4. Best methods for coreference resolution in retrieval?
5. Can retrieval improve with reinforcement learning?
6. How to detect when retrieved context is insufficient?
