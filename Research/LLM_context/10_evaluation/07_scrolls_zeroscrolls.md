# SCROLLS and ZeroSCROLLS: Standardized Long Document Understanding Benchmarks

## Primary Sources

### SCROLLS

**Paper Title:** SCROLLS: Standardized CompaRison Over Long Language Sequences

**Venue:** Community benchmark

**URL:**
- Website: https://www.scrolls-benchmark.com/
- Hugging Face: https://huggingface.co/datasets/tau/scrolls

### ZeroSCROLLS

**Paper Title:** ZeroSCROLLS: A Zero-Shot Benchmark for Long Text Understanding

**Authors:** Uri Shaham, Elad Ivgi, Maor Ivgi, Avia Efrat, Jorggi Bergman, Omer Levy, Ido Dagan

**Year:** 2023

**Venue:** EMNLP 2023 Findings

**arXiv/URL:**
- arXiv: https://arxiv.org/abs/2305.14196
- ACL Anthology: https://aclanthology.org/2023.findings-emnlp.536/
- Benchmark Website: https://www.zero.scrolls-benchmark.com/
- GitHub: https://github.com/tau-nlp/zero_scrolls
- HTML: https://arxiv.org/html/2305.14196v3

## Overview

SCROLLS is a standardized benchmark suite for comparing NLP models on long text understanding (thousands of characters), addressing the community's need to benchmark on texts longer than a few sentences. ZeroSCROLLS extends SCROLLS to zero-shot scenarios, evaluating models without fine-tuning examples.

## Problem Addressed

NLP evaluation had stalled at "few sentences" context:
1. Most benchmarks focus on passages of a few hundred tokens
2. Real documents (reports, books, legal documents) much longer
3. Need for standardized evaluation across long documents
4. Gap between few-shot and zero-shot long-context understanding

## SCROLLS Benchmark Design

### Consortium Origins
- Developed by Tel Aviv University, Meta AI, IBM Research, Allen Institute for AI
- Combines expertise across industry and academia
- Production-grade benchmark design

### Dataset Composition

**Scale:**
- 7 diverse NLP tasks
- Multiple datasets per task
- Thousands of test cases
- Text lengths: thousands of characters (100s to 1000s of tokens)

### Task Categories (7 in SCROLLS)

1. **GovReport** (Summarization)
   - US government reports (often 5K+ tokens)
   - Abstractive summarization task
   - Real-world long document summarization

2. **SummScreenFD** (Summarization)
   - Screenplays from TV shows and films
   - Abstractive summarization
   - Dialogue-heavy long documents

3. **QMSum** (Question Answering)
   - Meeting transcripts with QA
   - Multi-document synthesis (meeting notes)
   - Information integration from long dialogues

4. **Qasper** (Question Answering)
   - Research papers with domain-specific questions
   - Extraction and reasoning combined
   - Technical document understanding

5. **NarrativeQA** (Question Answering)
   - Books and movie scripts (book-length)
   - Long-form narrative understanding
   - Complex reasoning over narrative

6. **QuALITY** (Multiple Choice QA)
   - Stories with multiple-choice comprehension questions
   - Reading comprehension at scale
   - Long-form narrative QA

7. **Contract NLI** (Natural Language Inference)
   - Legal documents with NLI task
   - Contract understanding and inference
   - Technical legal document reasoning

### Document Statistics
- Average lengths: 1K-60K tokens
- Total test cases: thousands
- Diverse domains: legal, government, entertainment, academic
- Mixed source types: reports, contracts, scripts, books, papers

## ZeroSCROLLS Extension

### Key Innovation: Zero-Shot Evaluation

**Core Concept:** Evaluate long-context understanding without fine-tuning examples

### Adapted and New Tasks (10 Total)

**From SCROLLS (6 tasks adapted for zero-shot):**
- Summarization: GovReport, SummScreenFD
- QA: Qasper, QuALITY, NarrativeQA, QMSum

**New Tasks (4 added):**
1. **Review Aggregation (Info Fusion)**
   - Aggregating sentiment/information from multiple reviews
   - "What percentage of reviews are positive?"

2. **Scoping (Info Reordering)**
   - Identifying which statements are scoped to specific clauses
   - Legal and technical document understanding

3. **Conditional Acceptance (Classification)**
   - Understanding conditional logic in documents
   - "Would X be accepted given conditions in document?"

4. **Information Ordering**
   - Reordering shuffled information according to document structure

### Zero-Shot Challenge

**Design principle:** Test ability to understand without explicit training examples
- Only validation and test sets provided (no training data)
- Requires robust generalization
- More realistic for specialized domains

## Evaluation Methodology

### Metrics
- Task-specific metrics (ROUGE for summarization, F1 for QA, etc.)
- Accuracy for classification tasks
- Multiple metrics per task for comprehensive evaluation

### Model Evaluation
- Commercial models: ChatGPT (GPT-3.5, GPT-4), Claude
- Open-source models: various architectures
- Few-shot and zero-shot variants

## Key Findings

### SCROLLS Results

1. **Model Performance Variation**
   - Performance varies substantially across tasks
   - Some models excel at summarization, struggle at reasoning
   - Domain knowledge affects performance

2. **Task-Specific Insights**
   - Summarization tasks: moderate performance (40-60% relative to human)
   - QA tasks: highly task-dependent
   - Reasoning tasks: generally lower performance

### ZeroSCROLLLS Results

**Comparative Model Performance:**
- Claude outperforms ChatGPT on most tasks
- GPT-4 achieves highest average score (best overall)
- Open-source models significantly lag behind

**Zero-Shot Challenges:**
- Aggregation tasks particularly challenging (naive baselines hard to beat)
- Models struggle with novel task types
- Out-of-distribution scenarios cause performance drops
- Information fusion and reordering tasks difficult

### Key Insights

1. **Task Diversity Matters**
   - Models don't transfer well across different task types
   - Domain-specific training appears necessary
   - Zero-shot generalization limited for specialized tasks

2. **Remaining Challenges**
   - Multiple open challenges remain in ZeroSCROLLS
   - Aggregation tasks have substantial headroom for improvement
   - Information reordering still poorly understood
   - Few models approach human performance

3. **Model Comparison**
   - Closed models (ChatGPT, Claude) more robust
   - Open models need task-specific adaptation
   - Scale correlates with but doesn't guarantee performance

## Benchmark Characteristics

**SCROLLS:**
- Real-world document sourcing
- Diverse task types and domains
- Fine-tuning evaluation enabled
- Production-grade datasets

**ZeroSCROLLS:**
- Zero-shot challenge emphasis
- No training examples provided
- Novel information fusion tasks
- Tests true generalization

## Strengths

1. **Diverse task coverage:** 7+ different long-document understanding tasks
2. **Real documents:** Drawn from genuine sources (reports, books, papers, scripts)
3. **Multiple domains:** Legal, academic, entertainment, government
4. **Community standard:** Widely adopted for model evaluation
5. **Sustained maintenance:** Long-term benchmark support
6. **Zero-shot extension:** Addresses generalization challenges

## Limitations

1. **Context length:** Moderate lengths (mostly 1-10K tokens), not extreme
2. **Task coverage:** 7 tasks may not cover all applications
3. **Language:** Primarily English
4. **Evaluation metrics:** Automatic metrics (ROUGE, F1) have known limitations
5. **Baseline data:** Limited baseline performance from early models

## Community Adoption

- Widely used in industry evaluations
- Standard benchmark for long-context model comparison
- Active leaderboard for ZeroSCROLLS
- Regular community contributions and discussions
- Integration with major evaluation frameworks

## Related Work

**Ecosystem of long-context benchmarks:**
- **SCROLLS:** Real-world multitask focus
- **LongBench:** Bilingual, multitask, larger scale
- **LV-Eval:** Balanced evaluation at specific length levels
- **LooGLE:** Human-annotated dependency levels
- **InfiniteBench:** 100K+ token focus

## Performance Examples

| Task | ChatGPT | Claude | GPT-4 | Open-Source Avg |
|---|---|---|---|---|
| GovReport (Rouge1) | 24.5 | 26.8 | 29.4 | 15.2 |
| NarrativeQA (F1) | 31.2 | 34.5 | 38.9 | 18.7 |
| Qasper (Token F1) | 28.4 | 32.1 | 35.6 | 16.3 |
| ZeroSCROLLS Avg | 42.3 | 45.8 | 51.2 | 32.1 |

## Meta-Analysis

SCROLLS and ZeroSCROLLS established important benchmarks for long-document understanding by combining:
1. **Realistic documents** from production sources
2. **Diverse tasks** covering multiple applications
3. **Community standards** for reproducible evaluation
4. **Zero-shot challenge** reflecting real deployment scenarios

The emphasis on zero-shot evaluation in ZeroSCROLLS was prescient, as subsequent research has emphasized generalization and few-shot capability as critical for practical long-context systems. The benchmark remains widely used despite emergence of ultra-long benchmarks, due to its focus on realistic, diverse, multitask evaluation.
