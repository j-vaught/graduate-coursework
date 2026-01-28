# InfiniteBench: Extending Long Context Evaluation Beyond 100K Tokens

## Primary Source

**Paper Title:** ∞Bench: Extending Long Context Evaluation Beyond 100K Tokens

**Authors:** Xinrong Zhang, Yeyun Gong, Yelong Shen, Jiancheng Lv, Nan Duan, Weizhu Chen

**Year:** 2024

**Venue:** ACL 2024

**arXiv/URL:**
- arXiv: https://arxiv.org/abs/2402.13718
- ACL Anthology: https://aclanthology.org/2024.acl-long.814/
- GitHub: https://github.com/OpenBMB/InfiniteBench
- Hugging Face Datasets: https://huggingface.co/datasets/xinrongzhang2022/InfiniteBench
- HTML version: https://arxiv.org/html/2402.13718v3

## Overview

InfiniteBench is the first LLM benchmark featuring an average data length surpassing 100K tokens, with synthetic and realistic tasks spanning diverse domains in both English and Chinese. It addresses the critical gap in evaluation for models claiming to handle 100K+ token contexts.

## Problem Addressed

Despite recent progress in extending LLM context windows beyond 100K tokens, existing public benchmarks typically focus on contexts around 10K tokens. This creates:
1. Lack of standardized evaluation at 100K+ token ranges
2. Uncertainty about models' actual 100K+ capabilities
3. Need for comprehensive 100K+ evaluation framework
4. Evaluation gap between marketed capabilities and actual performance

## Benchmark Design

### Benchmark Composition

**Scale:**
- Average document length: >100K tokens (surpassing all previous benchmarks)
- Multiple length categories: 16K, 32K, 64K, 128K, 200K+ tokens
- Bilingual: English and Chinese evaluation

**Task Coverage:**
- Synthetic tasks for controlled testing
- Realistic tasks from real-world applications
- Diverse domains and task types
- Long-dependency requirement design

### Task Categories

1. **Document Retrieval**
   - Finding specific information in very long documents
   - Evaluates needle-in-haystack at extreme scales

2. **Query-Focused Summarization**
   - Creating summaries answering specific queries
   - Requires understanding of long-form documents

3. **Kv-Retrieval (Key-Value)**
   - Retrieving specific attribute values from large documents
   - Tests precise information location capability

4. **Question Answering**
   - Open-domain QA on long documents
   - Requires synthesis and reasoning

5. **Pass-Key Task**
   - Finding random numbers embedded in text
   - Evaluates pure retrieval at scale

6. **Reasoning Tasks**
   - Multi-hop reasoning over extreme lengths
   - Tests logical inference over distributed facts

7. **Real-world Tasks**
   - Practical applications of long-context understanding
   - Domain-specific tasks

### Design Principle: Long Dependency Focus

**Critical innovation:** Tasks are designed such that:
- Simply retrieving a limited number of passages is insufficient
- Requires understanding long-range dependencies
- Synthetic structure prevents shortcut solutions
- Meaningful dependency relationships embedded in tasks

## Evaluation Methodology

### Metrics
- Task-specific accuracy and F1 scores
- Length-based performance analysis
- Success/failure curves across context lengths
- Domain-specific metrics

### Model Coverage
- Major commercial models (GPT-4, Claude, etc.)
- Leading open-source models
- Different model sizes and architectures

## Key Findings

### Overall Performance

**Critical Finding: Significant Room for Improvement**
- Existing long-context LLMs still require substantial advancement
- Performance degrades substantially at 100K+ tokens
- Gap between claimed and effective context window

### Performance Patterns

1. **Domain Variation**
   - Performance varies significantly across different domains
   - Natural language tasks: generally higher performance
   - Code/math domains: more challenging
   - Domain knowledge required for consistent performance

2. **Length Effects**
   - Performance degradation accelerates at extreme lengths
   - 32K-64K: manageable for most models
   - 100K+: significant challenges emerge
   - No model approaches human-level performance at 200K+

3. **Task-Specific Insights**
   - Retrieval tasks: more stable performance
   - Reasoning tasks: sharp performance drops
   - Summarization: quality degrades with length
   - QA: moderate performance but with clear length effects

### Model Comparison
- Commercial closed-source models: generally better
- Open-source models: significant but narrower capability
- Model size correlates with but doesn't fully determine performance
- Fine-tuning on long sequences helps but has limits

## Benchmark Characteristics

- **100K+ focus:** First benchmark with this scale
- **Realistic and synthetic:** Mix of real and controlled tasks
- **Bilingual:** Multilingual capability assessment
- **Long-dependency design:** Tasks require true long-range understanding
- **Comprehensive:** Multiple task types and domains
- **Reproducible:** Standard evaluation protocol

## Strengths vs. Other Benchmarks

| Aspect | InfiniteBench | LongBench | RULER | NIAH |
|--------|---|---|---|---|
| Extreme lengths (100K+) | ✓ | ✗ | ✗ | ✗ |
| Realistic tasks | ✓ | ✓ | ✗ | ✗ |
| Long-dependency design | ✓ | Partial | ✓ | ✗ |
| Task diversity | ✓ | ✓ | Partial | ✗ |
| Reasoning-focused | Partial | Partial | ✓ | ✗ |

## Limitations

1. **Extreme length overhead:** 100K+ tokens make evaluation computationally expensive
2. **Model scalability:** Not all models can handle these lengths
3. **Baseline models:** Limited baseline performance data
4. **Task coverage:** 7 task types may not cover all use cases
5. **Evaluation cost:** Testing at scale requires significant resources

## Subsequent Research Impact

### Influence on Model Development
- Prompted development of new architectures for 100K+ handling
- Validated need for specialized training for extreme lengths
- Influenced research on attention mechanisms for long contexts

### Related Work
- Extensions to multimodal models
- Multilingual expansion efforts
- Specialized domain variants

## Implementation and Access

- Open-source code and data on GitHub
- Integrated into evaluation harnesses (LM Evaluation Harness)
- Hugging Face Datasets integration
- Community contributions and variants

## Performance Summary

**Key Result:** Most existing long-context LLMs still require significant advancement to effectively process 100K+ contexts, with:
- Synthetic tasks showing clearer patterns
- Real-world tasks showing larger performance variance
- Domain-specific performance heterogeneity
- Clear degradation beyond 128K tokens for most models

## Meta-Analysis

InfiniteBench fills a critical evaluation gap by being the first comprehensive benchmark for 100K+ token contexts. Its combination of synthetic control (ensuring long dependencies matter) and realistic tasks (ensuring relevance) provides a more complete picture than prior benchmarks. The finding that even models claiming 100K+ capabilities still significantly underperform at those scales has implications for production deployment and realistic capability assessment.

The benchmark's cost—both computational and in terms of development time—positions it as a gold-standard evaluation resource for ultra-long-context model development, though its use is primarily limited to well-resourced research teams.
