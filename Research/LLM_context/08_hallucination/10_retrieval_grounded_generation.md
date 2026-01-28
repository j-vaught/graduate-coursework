# Retrieval-Grounded Generation for Hallucination Mitigation

---

## Overview: RAG and Hallucination Reduction

**Core Principle:**
Hallucinations occur when LLMs rely solely on pre-trained knowledge, which may be:
- Outdated
- Incomplete
- Conflicting
- Never learned

**Solution:** Retrieval-Augmented Generation (RAG)
- Retrieve relevant passages before generation
- Ground generation in retrieved evidence
- Reduces hallucination through constraint to factual sources

---

## Foundational Paper: Dense Passage Retrieval for Open-Domain Question Answering

### Paper Information

**Authors:** Vladimir Karpukhin, Barlas Oguz, Sewon Min, Patrick Lewis, Ledell Wu, Sergey Edunov, Mike Lewis, Wen-tau Yih

**Title:** Dense Passage Retrieval for Open-Domain Question Answering

**Year:** 2020

**Venue:** Conference on Empirical Methods in Natural Language Processing (EMNLP) 2020, pages 6371-6381

**DOI/URL:** https://aclanthology.org/2020.emnlp-main.550/

**ArXiv:** https://arxiv.org/abs/2004.04906

**PDF:** https://arxiv.org/pdf/2004.04906

**GitHub:** https://github.com/facebookresearch/DPR

**Meta Research:** https://ai.meta.com/research/publications/dense-passage-retrieval-for-open-domain-question-answering/

**Semantic Scholar:** https://www.semanticscholar.org/paper/Dense-Passage-Retrieval-for-Open-Domain-Question-Karpukhin-O%C4%9Fuz/b26f2037f769d5ffc5f7bdcec2de8da28ec14bee

---

### Dense Passage Retrieval (DPR) Methodology

**Problem Addressed:**
Traditional retrieval using sparse methods (BM25) is suboptimal:
- Lexical mismatch problems
- Limited semantic understanding
- Inefficient for dense vector spaces

**DPR Solution: Dense Vector Representations**

**Architecture:**
- **Question Encoder:** Encodes queries to dense vectors
- **Passage Encoder:** Encodes passages to dense vectors
- **Matching:** Maximum inner product between query and passage vectors
- **Indexing:** FAISS for efficient similarity search

**Key Innovation:**
- Learned dual-encoder framework
- Dense representations capture semantics
- Efficient retrieval via vector similarity
- Scales to large passage collections

### Training Approach

**Data Requirements:**
- Question-passage pairs from QA datasets
- Only question-positive pairs needed (minimal supervision)
- No extensive annotation necessary

**Learning Objective:**
- Maximize similarity between question and relevant passages
- Minimize similarity to irrelevant passages
- Contrastive learning framework

### Retrieval Performance

**Empirical Results:**
- Top-20 passage retrieval accuracy: 9%-19% improvement over BM25
- Consistent improvements across multiple benchmarks
- Enables new SOTA on open-domain QA tasks

**Efficiency:**
- Practical implementation using FAISS
- Fast retrieval from large document collections
- Millions of passages searchable

### Integration with Generation

**End-to-End QA Pipeline:**
1. **Retrieve:** Top-K passages using DPR
2. **Rank:** Optional reranking of passages
3. **Generate:** Reader generates answer conditioned on passages
4. **Result:** Factually grounded answer

**Hallucination Reduction Mechanism:**
- Limited to information in retrieved passages
- Cannot hallucinate beyond passage content
- Constrains generation to grounded information

---

## Retrieval-Augmented Generation (RAG) Framework

### Broader RAG Context

**RAG Applications:**
- Open-domain QA
- Knowledge-intensive NLP tasks
- Fact-checking and verification
- Long-document understanding
- Dialogue systems with knowledge

### Why RAG Reduces Hallucinations

**1. Information Grounding**
- Generation constrained to retrieved evidence
- Cannot fabricate facts outside passages
- Direct connection to sources

**2. Evidence Availability**
- Relevant information provided
- Model doesn't rely on pre-training alone
- Reduces knowledge gaps

**3. Source Verification**
- Retrieved passages can be traced
- Citations possible
- Fact-checking enabled

**4. Knowledge Updates**
- Retrieval documents can be updated
- No need for retraining
- Dynamic knowledge incorporation

---

## Recent RAG Hallucination Mitigation Work

### Paper: Hallucination Mitigation for Retrieval-Augmented Large Language Models: A Review

**Title:** Hallucination Mitigation for Retrieval-Augmented Large Language Models: A Review

**Year:** 2025

**URL:** https://www.mdpi.com/2227-7390/13/5/856

**Focus:** Systematic review of hallucination in RAG systems

**Key Mitigation Strategies Covered:**

**1. Retrieval Quality Improvements**
- Better ranking and reranking
- Hybrid retrieval (dense + sparse)
- Query reformulation
- Iterative retrieval

**2. Generation Constraints**
- Restricting to retrieved content
- Token masking for out-of-passage terms
- Constrained decoding

**3. Prompt Engineering**
- Few-shot demonstrations
- Explicit instructions for grounding
- Chain-of-thought with retrieval
- Verification prompts

**4. Model Refinement**
- Fine-tuning on retrieval data
- Knowledge injection training
- Preference learning with grounding

---

## Specific Hallucination Sources in RAG Systems

### Paper: Hallucination Detection and Mitigation in Large Language Models

**Title:** Hallucination Detection and Mitigation in Large Language Models

**URL:** https://arxiv.org/pdf/2601.09929

**Year:** 2026

**Key Insight: Sources of Hallucination in RAG**

**Retrieval Phase Issues:**
1. **Data Source Problems**
   - Incomplete knowledge bases
   - Outdated or incorrect source documents
   - Missing relevant information

2. **Query Issues**
   - Ambiguous or poorly formulated queries
   - Semantic mismatch with queries
   - Context-dependent interpretation problems

3. **Retriever Problems**
   - Poor ranking of relevant documents
   - Missing relevant passages
   - Retrieving irrelevant passages
   - Effectiveness limitations

4. **Retrieval Strategy Issues**
   - Single pass insufficient for complex queries
   - Multi-hop reasoning requires multiple retrieval steps
   - Context length limitations

### Generation Phase Issues

1. **Context Noise**
   - Retrieved passages contain conflicting information
   - Distracting or irrelevant context
   - Noisy passages degrading quality

2. **Context Conflict**
   - Multiple retrieved passages contradict each other
   - Model must resolve conflicts
   - May hallucinate resolution

3. **Middle Curse**
   - Lost-in-the-middle effect
   - Middle-positioned evidence underutilized
   - Critical information missed

4. **Alignment Problems**
   - Generation doesn't match question intent
   - Mismatch between retrieval and query
   - Semantic drift in generation

5. **Model Capability Boundaries**
   - Tasks beyond model capability
   - Training distribution mismatch
   - Domain-specific knowledge gaps

---

## Framework: GRAVITI - Grounded Retrieval Generation

### Paper: GRAVITI: Grounded Retrieval Generation Framework for VideoLLM Hallucination Mitigation

**Title:** GRAVITI: Grounded Retrieval Generation Framework for VideoLLM Hallucination Mitigation

**URL:** https://www.researchsquare.com/article/rs-7900022/v1

**PDF:** https://www.researchsquare.com/article/rs-7900022/v1.pdf

**Year:** 2024-2025

**Domain:** Vision-language models (extends RAG to multimodal)

**Key Contribution:**
Grounded retrieval generation where each generated token is conditioned on evidence

**Approach:**
1. **Evidence Retrieval:** Video features and metadata
2. **Grounded Decoding:** Each token conditioned on evidence
3. **Hallucination Prevention:** Tokens not grounded in evidence are suppressed
4. **Verification:** Evidence justifies each generation step

---

## Enhanced RAG Approaches

### CREAM-RAG: Enhanced Retrieval Augmented Generation to Limit Hallucination

**Title:** CREAM-RAG: Enhanced Retrieval Augmented Generation to Limit Hallucination

**URL:** https://openreview.net/pdf?id=56DSmK9GnS

**Key Innovations:**
- Improved passage filtering
- Better context selection
- Enhanced generation constraints
- Hallucination detection in RAG

---

## Legal Domain Application

### Paper: Hallucinations in Legal RAG Systems

**Title:** Journal of Empirical Legal Studies, 2025; Hallucinations in Legal RAG

**URL:** https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf

**Year:** 2025

**Domain-Specific Findings:**
- Legal documents require precise citation
- Hallucinations have legal consequences
- Citation accuracy critical
- Domain-specific mitigation needed

**Key Findings:**
- Legal RAG systems still hallucinate despite grounding
- Document complexity affects hallucination rates
- Requirement for perfect accuracy essential
- Enhanced verification necessary

---

## Multi-Document RAG and Context Distance Effects

### Interaction with Lost-in-the-Middle Effect

**Challenge:** Multiple document retrieval with middle-position bias

**Multi-Document Question Answering Context:**
- Retrieve 5-40 documents
- Evidence scattered across documents
- Need to aggregate information
- Position of documents affects performance (see Lost in the Middle)

**Solutions:**
1. **Document Ordering:** Place critical documents at boundaries
2. **Hierarchical Retrieval:** Retrieve subtopic first, then specific passages
3. **Evidence Aggregation:** Explicit combination of evidence
4. **Iterative Retrieval:** Multiple passes with focused queries

---

## Groundedness in Retrieval-Augmented Long-Form Generation

### Paper: Groundedness in Retrieval-augmented Long-form Generation: An Empirical Study

**Title:** Groundedness in Retrieval-augmented Long-form Generation: An Empirical Study

**URL:** https://arxiv.org/html/2404.07060v1

**Year:** 2024

**Focus:** How well RAG systems ground long-form generation

**Key Questions:**
- How much of generated text is grounded in retrieval?
- What parts tend to hallucinate?
- How to improve groundedness?

**Findings:**
- Even with retrieval, hallucinations persist
- Long-form generation harder to ground
- Position effects matter (beginning more grounded)
- Explicit grounding mechanisms help

---

## Retrieval-Augmented Generation Survey

### Paper: Retrieval-Augmented Generation for Large Language Models: A Survey

**Title:** Retrieval-Augmented Generation for Large Language Models: A Survey

**URL:** https://arxiv.org/pdf/2312.10997

**Year:** 2023

**Comprehensive Coverage:**
- RAG architectures and variations
- Retrieval methods
- Generation techniques
- Evaluation approaches
- Challenges and future directions

**Key RAG Variants:**
1. **Naive RAG:** Retrieve then generate
2. **Advanced RAG:** Iterative retrieval and refinement
3. **Modular RAG:** Separate retrieval and generation components
4. **Agent-Based RAG:** Agentic decision-making with retrieval

---

## Comprehensive Survey on RAG

### Paper: Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers

**Title:** Retrieval-Augmented Generation: A Comprehensive Survey of Architectures, Enhancements, and Robustness Frontiers

**URL:** https://arxiv.org/html/2506.00054v1

**Year:** 2025

**Scope:** Latest advances in RAG

**Focus Areas:**
- Architecture innovations
- Robustness improvements
- Hallucination mitigation
- Evaluation methodologies
- Real-world applications

---

## Healthcare RAG Application

### Paper: Retrieval Augmented Generation for Large Language Models in Healthcare: A Systematic Review

**Title:** Retrieval Augmented Generation for Large Language Models in Healthcare: A Systematic Review

**URL:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12157099/

**Year:** 2024

**Domain-Specific Insights:**
- Healthcare RAG implementations
- Clinical decision support
- Medical knowledge integration
- Hallucination risks in medicine
- Regulatory compliance
- Safety and reliability

---

## Unified RAG Evaluation Framework

### Paper: Fact, Fetch, and Reason: A Unified Evaluation of Retrieval-Augmented Generation

**Title:** Fact, Fetch, and Reason: A Unified Evaluation of Retrieval-Augmented Generation

**URL:** https://aclanthology.org/2025.naacl-long.243/

**Year:** 2025

**Venue:** NAACL 2025

**Key Contribution:** FRAMES Benchmark

**Three Evaluation Dimensions:**

1. **Factuality (F)**
   - Accuracy of final answers
   - Consistency with real-world facts
   - Correctness of responses

2. **Retrieval (R)**
   - Quality of retrieved passages
   - Relevance ranking
   - Coverage of needed information

3. **Reasoning (E)**
   - Reasoning steps correctness
   - Aggregation of multi-document evidence
   - Inference quality

**Unified Assessment:**
- End-to-end RAG evaluation
- Component-level analysis
- Holistic system quality
- Identifies failure points

---

## Practical Hallucination Mitigation in RAG

### Best Practices

**1. Retrieval Quality**
- Use hybrid retrieval (dense + sparse)
- Implement reranking
- Query expansion techniques
- Ensure comprehensive coverage

**2. Generation Constraints**
- Restrict to retrieved content
- Use token masking
- Constrained decoding
- Explicit attribution

**3. Evidence Grounding**
- Track retrieved passages used
- Cite sources explicitly
- Verify source-claim alignment
- Enable user verification

**4. Verification Layers**
- Self-consistency checking
- Chain-of-verification
- Fact-checking post-processing
- Human review for critical items

**5. Iterative Improvement**
- Identify hallucination patterns
- Refine retrieval strategy
- Adjust generation parameters
- Continuous evaluation

---

## Challenges and Limitations

### Retrieval Limitations

1. **Coverage:** Retrieved documents may not contain answer
2. **Noise:** Retrieved passages contain distracting information
3. **Conflict:** Multiple sources contradict
4. **Latency:** Retrieval adds inference time

### Generation Over Retrieval

1. **Preference:** Models may prefer pre-training knowledge
2. **Overconfidence:** Generate even when evidence insufficient
3. **Mixing:** Combine retrieval with hallucinated content
4. **Paraphrasing:** Reformulate beyond source evidence

### System Integration

1. **Complexity:** Multi-component systems hard to debug
2. **Coupling:** Error propagation across components
3. **Efficiency:** Retrieval adds computational cost
4. **Generalization:** Task-specific optimization needed

---

## Key Takeaway for Literature Review

Retrieval-grounded generation is fundamental hallucination mitigation:
- **Core Strategy:** Ground generation in retrieved evidence
- **Dense Passage Retrieval:** Efficient passage ranking foundation
- **Constraint-Based:** Limits hallucination through information grounding
- **Source Verification:** Enables traceability and fact-checking
- **Active Research:** Ongoing improvements in RAG architectures
- **Practical Impact:** Widely deployed in production systems
- **Challenges:** Still hallucinations despite retrieval
- **Future:** Improved retrieval, generation, and verification integration

