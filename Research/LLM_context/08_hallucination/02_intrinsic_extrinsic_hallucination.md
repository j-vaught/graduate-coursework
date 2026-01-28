# Intrinsic vs. Extrinsic Hallucination

## Foundational Work: On Faithfulness and Factuality in Abstractive Summarization (Maynez et al. 2020)

**Authors:** Joshua Maynez, Shashi Narayan, Bernd Bohnet, Ryan McDonald

**Title:** On Faithfulness and Factuality in Abstractive Summarization

**Year:** 2020

**Venue:** Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL), pages 1906-1919

**URL:** https://aclanthology.org/2020.acl-main.173/

**ArXiv:** https://arxiv.org/abs/2005.00661

**PDF:** https://aclanthology.org/2020.acl-main.173.pdf

**Semantic Scholar:** https://www.semanticscholar.org/paper/On-Faithfulness-and-Factuality-in-Abstractive-Maynez-Narayan/dbeeca8466e0c177ec67c60d529899232415ca87

**GitHub Resources:** https://github.com/google-research-datasets/xsum_hallucination_annotations

---

## Key Definitions and Framework

### Intrinsic Hallucination
- **Definition:** Output content that **contradicts the source document**
- **Characteristics:**
  - Information that logically cannot be inferred from source
  - Factually false combinations of source information
  - Direct contradictions with source content
  - Task-specific violation of coherence with input
- **Example:** Summarizing "The event was successful" as "The event was a failure"

### Extrinsic Hallucination
- **Definition:** Output content that **cannot be verified by the source**
- **Characteristics:**
  - Information absent from source document
  - Externally correct but not grounded in input
  - Cannot be refuted by source (source simply doesn't mention it)
  - May be factually accurate but unverifiable from given context
- **Example:** Adding facts about related topics not discussed in source

---

## Critical Distinction

| Aspect | Intrinsic | Extrinsic |
|--------|-----------|-----------|
| Source Relationship | Contradicts source | Absent from source |
| Verifiability | Provably false from source | Cannot verify from source |
| Factual Accuracy | Often factually incorrect | May be factually correct |
| Risk Level | High - demonstrably wrong | Medium - ungrounded in context |
| Detection Method | NLI entailment violation | Coverage/grounding check |

---

## Research Methodology (Maynez et al. 2020)

### Large-Scale Human Evaluation
- Multiple neural abstractive summarization systems evaluated
- XSum dataset with faithfulness and factuality annotations
- Substantial hallucinated content found in all model-generated summaries

### Key Findings

**Hallucination Prevalence:**
- Intrinsic hallucinations: Frequent across all models
- Extrinsic hallucinations: More common than intrinsic in many cases
- All abstractive summarizers exhibit both types

**Model Comparisons:**
- Pretrained models (BART, PEGASUS) better at faithfulness/factuality
- Standard sequence-to-sequence models more prone to hallucinations
- Performance gap correlates with ROUGE and human metrics

**Evaluation Method Innovation:**
- Textual entailment (TE) correlates better with faithfulness than ROUGE
- TE-based metrics outperform standard overlap metrics (ROUGE)
- Potential path for automatic evaluation and training objectives

---

## Important Nuance: Extrinsic Hallucination Caveat

**Critical Insight from Maynez et al.:**
- Extrinsic hallucination is NOT always erroneous
- External information could be factually correct
- Example: Summary mentions president's education not in article
  - Can be verified as true in external sources
  - Still represents hallucination relative to article
  - But may not be "wrong" in absolute terms

**Practical Implications:**
- Must distinguish task requirements (summary from source vs. standalone factuality)
- Extrinsic hallucinations require caution due to unverifiable aspects
- Different applications tolerate different levels:
  - Medical: Very low tolerance for extrinsic
  - Creative: May accept extrinsic factually correct info
  - News: Should minimize extrinsic hallucinations

---

## Follow-up Research Building on Maynez et al.

### Intrinsic/Extrinsic Framework Adoption

**VideoHallUcer (2024)**
- Extends intrinsic/extrinsic framework to video-language models
- URL: https://arxiv.org/html/2406.16338v1
- Applies similar taxonomy to multimodal domain

**FADE Dataset (Factual Dialogue Hallucination Detection)**
- Applies intrinsic/extrinsic distinction to dialogue
- Knowledge-grounded conversation evaluation
- Benchmark for dialogue-specific hallucination detection

### Refinements and Extensions

**Factuality vs. Faithfulness Distinction**
- **Factuality:** Consistency with real-world facts
- **Faithfulness:** Consistency with provided context
- Maynez et al. unified these concepts for summarization task
- Later work (Huang et al.) separates them for LLM contexts

---

## Evaluation Metrics Derived from Framework

### Intrinsic Hallucination Detection
1. **Natural Language Inference (NLI)**
   - Check if summary contradicts source
   - Entailment detection
   - Semantic contradiction identification

2. **Question Answering Pairs**
   - Generate questions from source
   - Check if summary answers them consistently

3. **Span Extraction**
   - Extract supporting spans from source
   - Verify coverage and consistency

### Extrinsic Hallucination Detection
1. **Information Retrieval Grounding**
   - Retrieve passages supporting claims
   - Coverage metrics

2. **Entity Linking**
   - Link entities to knowledge base
   - Verify existence and properties

3. **Knowledge Base Consistency**
   - Check against structured KB
   - Verify claims against knowledge graphs

---

## Applications Across NLG Tasks

### Abstractive Summarization (Primary Domain)
- CNN/DailyMail and XSum datasets
- Most extensively studied task

### Data-to-Text Generation
- Intrinsic: Contradictions with structured input
- Extrinsic: Facts about entities not in table

### Dialogue Systems
- Intrinsic: Contradicting conversation history or knowledge
- Extrinsic: Introducing unsupported facts to conversation

### Machine Translation
- Intrinsic: Contradicting source language meaning
- Extrinsic: Adding information not in source text

### Question Answering
- Intrinsic: Contradicting question or context
- Extrinsic: Adding facts not in retrieval context

---

## Maynez et al. Impact and Citation

- **Highly Cited:** Foundational framework for hallucination taxonomy
- **Influence:** Cited by Ji et al. (2023), Huang et al. (2023), and nearly all subsequent hallucination surveys
- **Dataset Legacy:** XSum hallucination annotations widely used in research
- **Methodological Impact:** Intrinsic/extrinsic framework adopted across NLG tasks and multimodal models

---

## Related Datasets and Benchmarks

**XSum Hallucination Annotations** (from Maynez et al.)
- URL: https://github.com/google-research-datasets/xsum_hallucination_annotations
- Human annotations for intrinsic/extrinsic hallucinations
- Used in subsequent hallucination research

**FaithDial**
- Knowledge-grounded dialogue with faithfulness annotations
- Applies Maynez framework to dialogue domain

**FADE**
- Factual Dialogue Hallucination Detection Dataset
- Multi-domain dialogue hallucination annotations

