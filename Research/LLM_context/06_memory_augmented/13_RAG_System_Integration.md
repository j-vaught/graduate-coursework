# RAG System Integration: Practical Frameworks and Tools

## Overview of RAG Frameworks (2024-2025)

### LlamaIndex (Previously GPT-Index)

**Description**: Comprehensive Python framework for building RAG applications

**Key Components**:
1. **Data Connectors**: Load from PDF, JSON, SQL, APIs, etc.
2. **Indexing**: Create indexes from documents (vector, keyword, graph)
3. **Query Engines**: Retrieve and generate responses
4. **Chat Engines**: Multi-turn conversational RAG

**Features**:
- **40+ integrations**: Support for different embedding models, LLMs, vector DBs
- **Index Types**:
  - Vector Index: Dense similarity search
  - Keyword Index: BM25 sparse retrieval
  - Knowledge Graph Index: Entity-relationship structure
  - Tree Index: Hierarchical organization

**Example Workflow**:
```python
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader

# Load documents
documents = SimpleDirectoryReader("./data").load_data()

# Create index
index = GPTVectorStoreIndex.from_documents(documents)

# Create query engine
query_engine = index.as_query_engine()

# Query
response = query_engine.query("What is...?")
```

**Documentation**: https://developers.llamaindex.ai/

---

### LangChain

**Description**: Framework for chaining LLM operations with retrieval

**Key Components**:
1. **Document Loaders**: Load various document formats
2. **Text Splitters**: Chunk documents (fixed, recursive, semantic)
3. **Embeddings**: Integrate embedding models
4. **Vector Stores**: Interface with vector databases
5. **Retrievers**: Create retrieval chains
6. **Chains**: Combine retrieval with generation

**RAG Chains**:
- **RAGChain**: Basic retrieval → generation
- **RetrievalQA**: Q&A with retrieved context
- **ConversationalRetrievalChain**: Multi-turn conversations

**Advanced Features**:
- **Document Compression**: Summarize retrieved documents
- **Ensemble Retrieval**: Combine multiple retrievers
- **Re-ranking**: Re-rank retrieved documents
- **Lost-in-the-Middle**: Reorder documents (recent first/last)

**Example**:
```python
from langchain.retrievers import EnsembleRetriever
from langchain.chains import RetrievalQA

# Create ensemble retriever
retriever = EnsembleRetriever(
    retrievers=[dense_retriever, bm25_retriever],
    weights=[0.5, 0.5]
)

# Create QA chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever
)

answer = qa.run(query)
```

**Documentation**: https://python.langchain.com/

---

### Haystack (DeepSet)

**Description**: Production-ready RAG framework with advanced features

**Key Components**:
1. **Pipeline Architecture**: DAG-based component orchestration
2. **Components**: Retrievers, generators, rankers, etc.
3. **Document Storage**: Hybrid storage with metadata
4. **Evaluation**: Built-in evaluation framework

**Advanced Features**:
- **Generators**: Multiple LLM backends
- **Rankers**: Re-rankers and re-scorers
- **Web Search Integration**: Search web if needed
- **Evaluation Metrics**: Retrieval and generation metrics

**Pipeline Example**:
```yaml
components:
  retriever:
    type: BM25Retriever
  reranker:
    type: SentenceTransformersRanker
  llm:
    type: GPT3.5

pipelines:
  rag_pipeline:
    - retriever.run(queries)
    - reranker.run(documents)
    - llm.run(prompt)
```

**Documentation**: https://docs.deepset.ai/

---

## Vector Database Options

### FAISS (Facebook AI Similarity Search)

**Type**: In-memory, open-source

**Characteristics**:
- No external service required
- Fast similarity search
- Supports various index types
- Memory limitations for very large datasets

**Use Cases**: Development, research, smaller deployments

---

### Pinecone

**Type**: Managed cloud service

**Characteristics**:
- Fully managed
- Auto-scaling
- High availability
- Costs money

**Use Cases**: Production deployments, large-scale applications

**Integration with RAG**:
```python
from pinecone import Pinecone

pc = Pinecone(api_key="...")
index = pc.Index("rag-index")

# Upsert embeddings
index.upsert(vectors=embeddings)

# Query
results = index.query(query_embedding, top_k=10)
```

---

### Weaviate

**Type**: Open-source, cloud available

**Characteristics**:
- GraphQL interface
- Vector + keyword search
- Knowledge graph capabilities
- Flexible deployment (self-hosted or cloud)

**Use Cases**: Complex queries, semantic search, knowledge graphs

---

### Qdrant

**Type**: Open-source, managed available

**Characteristics**:
- High performance
- Filtering capabilities
- Distributed architecture
- Good balance of features and simplicity

**Use Cases**: Production deployments, large-scale search

---

## RAG Pipeline Architecture

### Standard Pipeline
```
User Query
  ↓
Query Preprocessing (normalization, expansion)
  ↓
Embedding Generation
  ↓
Vector Search (FAISS/Pinecone)
  ↓
Retrieved Documents
  ↓
Re-ranking (optional)
  ↓
Document Formatting
  ↓
Prompt Construction
  ↓
LLM Generation
  ↓
Response Post-processing
  ↓
User Response
```

### Advanced Pipeline (Production)
```
User Query
  ├─ Intent Classification
  │   ├─ If need retrieval → Proceed
  │   └─ If parametric only → Skip retrieval
  ↓
Retrieval Module
├─ Dense Retrieval (SBERT)
├─ Sparse Retrieval (BM25)
├─ Web Search (if needed)
└─ Ensemble combination
  ↓
Document Filtering
├─ Remove duplicates
├─ Relevance filtering
└─ Authority scoring
  ↓
Re-ranking (Cross-encoder)
  ↓
Context Construction
├─ Summarization
└─ Format selection
  ↓
Prompt Engineering
├─ System prompt
├─ Retrieved context
├─ Few-shot examples
└─ User query
  ↓
LLM Generation with streaming
  ↓
Response Validation
├─ Factuality check
├─ Consistency check
└─ Length check
  ↓
User Response with Citation
```

---

## Best Practices for RAG Systems

### Retrieval Quality
1. **Multiple Retrievers**: Combine dense and sparse
2. **Re-ranking**: Use more accurate ranking than retrieval
3. **Query Expansion**: Generate multiple queries
4. **Document Processing**: Clean, well-chunked documents

### Generation Quality
1. **Prompt Engineering**: Clear instructions, examples
2. **Context Length**: Balance between coverage and brevity
3. **Citation**: Include sources for retrieved information
4. **Fact-checking**: Verify claims against retrieved context

### System Robustness
1. **Error Handling**: Fallbacks for failed retrieval
2. **Caching**: Cache embeddings and results
3. **Monitoring**: Track retrieval and generation quality
4. **Evaluation**: Regular benchmarking on test sets

### Performance Optimization
1. **Batching**: Process multiple queries together
2. **Indexing**: Pre-compute and cache embeddings
3. **Hardware**: Use GPU for embeddings
4. **Latency Reduction**: Streaming, early response (don't wait for full generation)

---

## Configuration Patterns

### Configuration Pattern: Modular RAG
```python
class RAGPipeline:
    def __init__(self, config):
        self.retriever = self._build_retriever(config)
        self.reranker = self._build_reranker(config)
        self.generator = self._build_generator(config)
        self.formatter = self._build_formatter(config)

    def run(self, query):
        # Retrieve
        docs = self.retriever.retrieve(query)

        # Re-rank
        reranked = self.reranker.rank(query, docs)

        # Format
        context = self.formatter.format(reranked)

        # Generate
        response = self.generator.generate(query, context)

        return response
```

### Configuration Pattern: Adaptive RAG
```python
class AdaptiveRAG:
    def run(self, query):
        # Decide if retrieval needed
        if self.should_retrieve(query):
            docs = self.retrieve(query)
            response = self.generate_with_context(query, docs)
        else:
            response = self.generate_without_context(query)

        return response

    def should_retrieve(self, query):
        # Could use Self-RAG approach
        # or confidence threshold
        pass
```

---

## Common RAG Failure Modes and Solutions

### Problem: Retrieved Documents Not Relevant
**Causes**:
- Poor embeddings
- Query-document mismatch
- Bad chunking

**Solutions**:
- Better embedding models (SBERT → ColBERT)
- Query expansion (HyDE, multi-query)
- Better chunking (semantic chunking)
- Re-ranking (cross-encoder)

### Problem: Information Dispersed Across Multiple Documents
**Causes**:
- Required information split across passages
- Single retrieval insufficient

**Solutions**:
- Multi-pass retrieval
- Iterative retrieval (FLARE)
- Multi-hop reasoning
- Increase number of retrieved documents

### Problem: Generated Answer Contradicts Retrieved Context
**Causes**:
- Hallucination from parametric knowledge
- Contradictory documents retrieved

**Solutions**:
- Stronger grounding (Self-RAG critique)
- Consistency checking
- Document filtering before generation
- Better prompting

### Problem: Long Latency
**Causes**:
- Embedding computation
- Network calls
- LLM inference

**Solutions**:
- Batch processing
- Streaming responses
- Caching
- Quantized embeddings

---

## Evaluation and Testing

### Unit Tests
```python
def test_retriever_returns_relevant_docs():
    query = "What is photosynthesis?"
    docs = retriever.retrieve(query)
    assert any("photosynthesis" in doc.text.lower() for doc in docs)

def test_generator_respects_context():
    context = "The sky is green."
    response = generator.generate("What color is the sky?", context)
    assert "green" in response.lower()
```

### Integration Tests
```python
def test_rag_pipeline_end_to_end():
    query = "What is the capital of France?"
    response = rag_pipeline.run(query)

    # Check response quality
    assert "Paris" in response
    assert len(response) > 20

    # Check that retrieval was used
    retrieved_docs = rag_pipeline.last_retrieved_docs
    assert len(retrieved_docs) > 0
```

### Evaluation Metrics
```python
from ragas import evaluate
from ragas.metrics import context_recall, answer_relevance

dataset = {
    "queries": [...],
    "retrieved_contexts": [...],
    "answers": [...]
}

results = evaluate(dataset, metrics=[context_recall, answer_relevance])
```

---

## File Metadata
- **Research Area**: RAG Systems, Software Architecture, Implementation
- **Focus**: Practical frameworks and integration patterns
- **Tools Covered**: LlamaIndex, LangChain, Haystack, Vector DBs
- **Target Audience**: ML Engineers, Systems Builders
- **Code Availability**: All tools open-source
- **Documentation**: Links to official docs for all tools

## Cross-References
- Implementation of: All RAG papers and methods
- Used by: Production systems and research
- Integration point for: Embedding models, LLMs, vector databases
