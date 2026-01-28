# Hallucination Surveys in LLMs

## 1. Survey of Hallucination in Natural Language Generation (Ji et al. 2023)

**Authors:** Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, Pascale Fung

**Title:** Survey of Hallucination in Natural Language Generation

**Year:** 2023

**Venue:** ACM Computing Surveys, 55(12):1-38

**DOI/URL:** https://dl.acm.org/doi/10.1145/3571730

**ArXiv:** https://arxiv.org/abs/2202.03629

**Key Findings:**
- Comprehensive review of hallucination phenomena across NLG tasks
- Covers metrics, mitigation methods, and future directions
- Task-specific analysis of hallucinations in:
  - Abstractive summarization
  - Dialogue generation
  - Generative question answering
  - Data-to-text generation
  - Machine translation
  - Visual-language generation
  - Large language models (LLMs)
- Surveys improvements through sequence-to-sequence deep learning and Transformer-based language models

**GitHub:** https://github.com/EdinburghNLP/awesome-hallucination-detection

---

## 2. A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions (Huang et al. 2023/2025)

**Authors:** Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua Peng, Xiaocheng Feng, Bing Qin

**Title:** A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions

**Year:** 2023 (arXiv) / 2025 (Published)

**Venue:** ACM Transactions on Information Systems, 43(2):1-55

**DOI/URL:** https://dl.acm.org/doi/10.1145/3703155

**ArXiv:** https://arxiv.org/abs/2311.05232

**Key Findings:**
- Refined taxonomy building upon Ji et al. work
- Distinguishes between factuality hallucination and faithfulness hallucination
- Comprehensive coverage of hallucination types in LLMs
- Analysis of challenges and open research questions
- Encapsulates distinct intricacies specific to LLM hallucinations

**Related Resource:** HTML version available at https://arxiv.org/html/2311.05232

---

## 3. Survey and Analysis of Hallucinations in Large Language Models: Attribution to Prompting Strategies or Model Behavior

**Authors:** Various contributors to systematic survey

**Title:** Survey and Analysis of Hallucinations in Large Language Models: Attribution to Prompting Strategies or Model Behavior

**Year:** 2025

**Venue:** Frontiers in Artificial Intelligence

**URL:** https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1622292/full

**PMC:** https://pmc.ncbi.nlm.nih.gov/articles/PMC12518350/

**Key Findings:**
- Distinguishes hallucinations caused by prompting strategies vs. inherent model behavior
- Comprehensive analysis across multiple dimensions
- Evaluates role of prompt engineering in hallucination causation
- Systematic literature review methodology

---

## 4. A Survey on Hallucination in Large Vision-Language Models

**Title:** A Survey on Hallucination in Large Vision-Language Models

**Year:** 2024

**ArXiv:** https://arxiv.org/html/2402.00253v1

**Key Findings:**
- Extends hallucination research to multimodal domain
- Addresses hallucinations in vision-language models
- Cross-modal hallucination phenomena
- Evaluation and mitigation strategies for VLMs

---

## 5. Additional Hallucination Survey Resources

**Awesome Hallucination Detection Repository**
- GitHub: https://github.com/EdinburghNLP/awesome-hallucination-detection
- Comprehensive curated list of hallucination detection papers
- Includes links to datasets, benchmarks, and methodologies

**Cognitive Mirage: A Review of Hallucinations in Large Language Models**
- Provides psychological perspective on hallucination mechanisms
- URL: https://ceur-ws.org/Vol-3818/paper2.pdf

**The Pitfalls of Defining Hallucination**
- Published in Computational Linguistics, MIT Press
- DOI: https://direct.mit.edu/coli/article/50/2/807/119144/The-Pitfalls-of-Defining-Hallucination
- Addresses fundamental definitional challenges in hallucination research

---

## Key Taxonomies and Definitions Across Surveys

### Hallucination Categories
1. **Content-Based:** Hallucinations about actual content in source material
2. **Knowledge-Based:** Hallucinations due to incorrect pre-trained knowledge
3. **Task-Specific:** Hallucinations unique to particular NLG tasks

### Evaluation Dimensions
- Factuality: Consistency with verifiable facts
- Faithfulness: Consistency with provided context
- Coherence: Internal consistency of generated text
- Relevance: Appropriateness to query/task

### Mitigation Approaches (Survey Coverage)
1. Training-based methods
2. Decoding strategies
3. Post-processing and filtering
4. Knowledge grounding
5. Retrieval-augmented generation

---

## Cross-Reference Summary

All three major surveys (Ji et al. 2023, Huang et al. 2023-2025, and contemporary systematic reviews) converge on:
- Hallucination is a pervasive problem across NLG tasks and LLMs
- Clear distinction between intrinsic and extrinsic hallucinations
- Need for task-specific evaluation and mitigation strategies
- Growing importance of retrieval-grounding mechanisms
- Trade-offs between different types of accuracy

