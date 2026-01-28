# Faithfulness vs. Factuality in LLMs

## Core Concepts and Definitions

### Faithfulness (Groundedness)
- **Definition:** Output is consistent with the **provided context/source**
- **Scope:** Relative to given input (retrieved passages, user documents, conversation history)
- **Evaluation:** Does not require external fact verification
- **Type:** Intrinsic hallucination detection
- **Example:** "The article says X is Y" - checking if generation respects this

### Factuality
- **Definition:** Output is consistent with **real-world verifiable facts**
- **Scope:** Absolute truth values regardless of input
- **Evaluation:** Requires fact-checking against external sources
- **Type:** Extrinsic hallucination detection
- **Example:** "Is it true that X happened in 2023?" - checking against world knowledge

---

## The Trade-off Problem: Key Research Finding

**Critical Discovery:** Improving one dimension often degrades the other

### Research Evidence

**Paper:** "Is Factuality Enhancement a Free Lunch For LLMs? Better Factuality Can Lead to Worse Context-Faithfulness"

**URL:** https://openreview.net/forum?id=asGQQc7gNo

**Key Finding:**
- Methods targeting factual accuracy cause severe context-faithfulness decline
- Maximum observed degradation: 69.7% decrease in faithfulness
- Interventions create unexpected trade-offs
- Cannot simultaneously optimize both without careful design

### Implications
1. Factuality and faithfulness require different mitigation strategies
2. Single-objective optimization insufficient
3. Task requirements must specify which dimension to prioritize
4. Hybrid approaches needed for both simultaneously

---

## Recent Paper: Two Birds with One Stone

**Title:** Two Birds with One Stone: Improving Factuality and Faithfulness of LLMs via Dynamic Interactive Subspace Editing

**URL:** https://arxiv.org/html/2506.11088v1

**Year:** 2025

**Key Contribution:** Proposes method to improve BOTH factuality and faithfulness simultaneously through:
- Dynamic interactive subspace editing
- Model parameter adjustments
- Avoids naive fine-tuning degradation

---

## Distinction in Different Contexts

### Retrieval-Augmented Generation (RAG)
- **Primary Concern:** Faithfulness to retrieved passages
- **Secondary Concern:** External factuality of source documents
- **Evaluation Focus:** Context grounding

### Open-Domain Question Answering
- **Primary Concern:** Factuality of answers
- **Secondary Concern:** Faithfulness to retrieval context (if used)
- **Evaluation Focus:** World knowledge accuracy

### Summarization
- **Primary Concern:** Faithfulness to source document
- **Secondary Concern:** Internal factual consistency
- **Integrated:** Maynez et al. unified for summarization

### Dialogue Systems
- **Primary Concern:** Faithfulness to conversation history and knowledge
- **Secondary Concern:** Factuality of introduced claims
- **Challenge:** Both essential for trusted interaction

---

## Evaluation Approaches

### Faithfulness Evaluation Methods

**1. LLM-as-a-Judge**
- Use strong LLM to assess context consistency
- Check if output contradicts provided passages
- Examples: GPT-4 based evaluation frameworks
- Tool: DeepEval framework
  - URL: https://deepeval.com/docs/metrics-faithfulness

**2. Self-Consistency Checks**
- If LLM claims words are important for prediction
- Should not be able to make prediction without them
- Reveals logical inconsistencies

**3. Question-Answering Based Methods**
- Generate questions from context
- Check if generation answers them consistently
- Span extraction and verification

**4. Natural Language Inference (NLI)**
- Check entailment between context and output
- Identify contradictions
- Measure coherence

### Factuality Evaluation Methods

**1. External Knowledge Base Verification**
- Compare claims against structured KBs
- Fact extraction and verification
- Entity linking to canonical sources

**2. Retrieval Grounding**
- Use IR to find supporting passages
- Coverage metrics
- Supporting evidence extraction

**3. Knowledge Graph Consistency**
- Verify relations in structured knowledge
- Entity property validation
- Link correctness

**4. Human Expert Evaluation**
- Domain expert fact-checking
- Necessary for critical domains (medical, legal)
- Gold standard for evaluation

---

## Task-Specific Guidance

### When Faithfulness Dominates
1. **Summarization:** Never add facts beyond source
2. **Translation:** Preserve source language meaning
3. **Dialogue (knowledge-grounded):** Respect provided knowledge
4. **Data-to-text:** Only express table contents

### When Factuality Dominates
1. **Open-domain QA:** World knowledge crucial
2. **Instruction following:** Correctness paramount
3. **Medical/Legal:** Absolute accuracy required
4. **Creative writing:** Some flexibility on strict faithfulness

### When Both Matter Equally
1. **RAG for knowledge-intensive tasks**
2. **Multi-document QA**
3. **Fact-checking and verification**
4. **Scientific/technical writing**

---

## Metrics and Benchmarks

### ALCE Benchmark (Citation/Attribution)
- Evaluates three dimensions:
  1. **Fluency:** Coherence of generation
  2. **Correctness:** Factuality accuracy
  3. **Citation Quality:** Faithfulness to cited sources
- URL: https://github.com/princeton-nlp/ALCE
- arXiv: https://arxiv.org/abs/2305.14627

### FActScore (Factuality Focus)
- Atomic fact evaluation for factuality
- Long-form generation assessment
- URL: https://github.com/shmsw25/FActScore
- arXiv: https://arxiv.org/abs/2305.14251

### RAG Evaluation Framework
**FRAMES (Factuality, Retrieval, And reasoning MEasurement Set)**
- URL: https://aclanthology.org/2025.naacl-long.243/
- Paper: "Fact, Fetch, and Reason: A Unified Evaluation of Retrieval-Augmented Generation"
- Evaluates:
  - Factual accuracy of responses
  - Quality of retrieval
  - Reasoning correctness

---

## Recent Advances (2024-2025)

### Walk the Talk: Measuring Faithfulness of LLM Explanations
**URL:** https://arxiv.org/abs/2504.14150

**Key Finding:** Significant gap between explanation quality and decision faithfulness
- Models produce explanations that don't match actual decision factors
- Highlights disconnect between stated and actual reasoning

### Evaluating Faithfulness in Agentic RAG Systems
**URL:** https://www.mdpi.com/2504-2289/9/12/309

**Application:** E-governance systems
- Specialized evaluation frameworks for mission-critical RAG
- Combines LLM-based judging with domain verification
- Emphasis on context grounding

### Faithful AI in Medicine
**Survey:** https://pmc.ncbi.nlm.nih.gov/articles/PMC10312867/

**Domain Specific Focus:**
- Medical domain requires both faithfulness and factuality
- Strict standards for hallucination prevention
- Clinical decision support requirements

---

## Implementation Strategies

### For RAG Systems
1. Implement dual evaluation:
   - Faithfulness: Retrieved passage consistency
   - Factuality: Retrieved source authority verification

2. Prioritize based on use case:
   - Internal documents RAG: Faithfulness critical
   - Web search RAG: Factuality critical
   - Hybrid: Both required

3. Use conformal prediction for guarantees
   - Language Models with Conformal Factuality Guarantees
   - URL: https://arxiv.org/abs/2402.10978
   - Provides probabilistic correctness bounds

### For LLM Fine-tuning
1. Separate training objectives:
   - Factuality: World knowledge consistency
   - Faithfulness: Input context consistency

2. Knowledge editing for factuality:
   - Knowledge Editing for LLMs Survey
   - URL: https://arxiv.org/abs/2310.16218
   - Update outdated or incorrect knowledge

3. Context-aware prompt engineering:
   - Few-shot demonstrations
   - Chain-of-thought with verification
   - Self-consistency checking

---

## Common Pitfalls

1. **Conflating the two:** Different evaluation approaches needed
2. **Ignoring task context:** Different tasks prioritize differently
3. **Single metric optimization:** Creates opposite-side degradation
4. **Neglecting data quality:** Source document accuracy affects both
5. **Human evaluation gaps:** Hard to get consistent human labels

---

## Future Research Directions

1. **Joint optimization methods** for both dimensions
2. **Domain-specific trade-off analysis**
3. **Automatic metric design** that captures both
4. **Knowledge update methods** for factuality maintenance
5. **Context-faithful factuality retrieval** for RAG

