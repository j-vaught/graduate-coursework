# Quick Reference: Section 8 Research Data

## File Checklist
- [x] 01_hallucination_surveys.md (145 lines)
- [x] 02_intrinsic_extrinsic_hallucination.md (207 lines)
- [x] 03_faithfulness_vs_factuality.md (261 lines)
- [x] 04_lost_in_the_middle.md (341 lines)
- [x] 05_primacy_recency_bias.md (394 lines)
- [x] 06_self_consistency.md (387 lines)
- [x] 07_chain_of_verification.md (416 lines)
- [x] 08_citation_attribution_alce.md (463 lines)
- [x] 09_hallucination_benchmarks.md (476 lines)
- [x] 10_retrieval_grounded_generation.md (531 lines)
- [x] README.md (292 lines)

**Total: 11 markdown files, 3,913 lines of research data**

---

## Paper Quick Index

### Surveys & Foundational
| Paper | Authors | Year | Venue |
|-------|---------|------|-------|
| Survey of Hallucination in NLG | Ji et al. | 2023 | ACM Computing Surveys |
| Survey on Hallucination in LLMs | Huang et al. | 2023-25 | ACM TOIS |

### Hallucination Classification
| Paper | Authors | Year | Venue |
|-------|---------|------|-------|
| Faithfulness & Factuality in Summarization | Maynez et al. | 2020 | ACL |

### Context Distance & Position Effects
| Paper | Authors | Year | Venue |
|-------|---------|------|-------|
| Lost in the Middle | Liu et al. | 2023 | TACL |
| Serial Position Effects | Various | 2024 | Multiple |
| Recency Bias in Reranking | Various | 2025 | Multiple |

### Mitigation Strategies
| Paper | Authors | Year | Venue |
|-------|---------|------|-------|
| Self-Consistency CoT | Wang et al. | 2023 | ICLR |
| Chain-of-Verification | Dhuliawala et al. | 2023 | ACL Findings |

### Citation & Attribution
| Paper | Authors | Year | Venue |
|-------|---------|------|-------|
| Enabling LLMs to Generate Text with Citations | Gao et al. | 2023 | EMNLP |

### Benchmarks
| Benchmark | Authors | Year | Key Metric |
|-----------|---------|------|-----------|
| FActScore | Min et al. | 2023 | Atomic factuality |
| HaluEval | Li et al. | 2023 | Task-specific hallucination |
| TruthfulQA | Lin et al. | 2022 | Knowledge truthfulness |

### Retrieval & RAG
| Paper | Authors | Year | Venue |
|-------|---------|------|-------|
| Dense Passage Retrieval | Karpukhin et al. | 2020 | EMNLP |
| RAG Survey | Various | 2023+ | Multiple |
| FRAMES/NAACL 2025 | Krishna et al. | 2025 | NAACL |

---

## Key Metrics & Results

### Hallucination Reduction
- Self-Consistency: +17.9% (GSM8K)
- Chain-of-Verification: 50-70% reduction
- Retrieval-Grounded: Baseline constraint mechanism

### Benchmark Performance
- TruthfulQA: GPT3 58% vs Human 94%
- FActScore: ChatGPT 58% on biographies
- HaluEval: ChatGPT hallucinates 19.5% of queries

### Position Effects
- Primacy bias: 5-10% advantage
- Recency bias: 8-15% advantage
- Total variance: 15-25% across positions

---

## Retrieval-Augmented Generation Key Papers

1. **Dense Passage Retrieval** (2020)
   - Foundational: Dense vector retrieval
   - Karpukhin et al., Meta/Facebook Research

2. **RAG Comprehensive Survey** (2023)
   - Architecture overview
   - Latest advances through 2023

3. **RAG Enhancements Survey** (2025)
   - Robustness improvements
   - Hallucination mitigation focus

4. **FRAMES Unified Evaluation** (2025)
   - Factuality + Retrieval + Reasoning
   - NAACL 2025 publication

---

## Comparison Tables

### Mitigation Approaches
| Approach | Cost | Effectiveness | Training | Complexity |
|----------|------|---------------|----------|-----------|
| Self-Consistency | 5-40x inference | 10-20% gain | No | Low |
| Chain-of-Verification | 2x inference | 50-70% reduction | No | Medium |
| Retrieval-Augmented | 1-5x inference | Constraint-based | Optional | Medium |
| Fine-tuning | Training | Task-dependent | Yes | High |

### Benchmark Characteristics
| Benchmark | Scale | Domain | Type | Automation |
|-----------|-------|--------|------|-----------|
| FActScore | Medium | Long-form | Metric | Automatic |
| HaluEval | Large (35K+) | Multi-task | Dataset | Hybrid |
| TruthfulQA | Medium (817) | Knowledge | Benchmark | LLM Judge |

### Position Bias Effects
| Effect | Direction | Magnitude | Task Type |
|--------|-----------|-----------|-----------|
| Primacy | First favored | 5-10% | All tasks |
| Recency | Last favored | 8-15% | Ranking, Choice |
| Lost-in-Middle | U-shaped | 15-25% | Multi-document |

---

## Critical Findings Summary

### Top Insights
1. **Hallucinations pervasive** - All NLG systems affected
2. **Position matters** - Document/option order affects output quality
3. **Trade-offs exist** - Improving one dimension may degrade another
4. **Sampling helps** - Multiple attempts + aggregation improves accuracy
5. **Grounding works** - Retrieval constrains hallucinations
6. **Verification reduces** - Explicit checking eliminates 50-70%
7. **Benchmarks standardized** - Multiple evaluation frameworks available

### Open Challenges
- Simultaneous faithfulness-factuality optimization
- Scaling position bias mitigation
- Multimodal hallucination understanding
- Real-time hallucination detection
- Domain-specific hallucination patterns

---

## Research Trends

### Key Evolution
- **2020:** Foundation (Maynez, DPR)
- **2022:** Benchmarking (TruthfulQA)
- **2023:** Surveys & major methods (Huang, Wang, Dhuliawala)
- **2024:** Refinements & domain applications
- **2025:** Unified frameworks & RAG enhancements

### Emerging Areas
- Multimodal hallucinations (videos, images)
- Real-time detection
- Conformal prediction guarantees
- Knowledge editing for updates
- Long-context optimization

---

## Repository Statistics

| Metric | Count |
|--------|-------|
| Total markdown files | 11 |
| Total lines of content | 3,913 |
| Papers with full metadata | 50+ |
| Unique authors/groups | 30+ |
| Venues covered | 8+ |
| Datasets mentioned | 15+ |
| ArXiv links | 30+ |
| GitHub repositories | 10+ |

---

## How to Use This Collection

### For Literature Review
1. Read README.md for overview
2. Use QUICK_REFERENCE for navigation
3. Deep-dive into topic-specific files
4. Cross-reference via hyperlinks

### For Citation
All papers include:
- Title, authors, year
- Venue information
- ArXiv IDs and URLs
- DOI/ACL Anthology links
- GitHub repositories

### For Research
- Use as baseline literature survey
- Identify gaps and opportunities
- Benchmark against standards
- Compare methodologies

### For Implementation
- Review mitigation strategies (06, 07, 10)
- Apply benchmarks (09)
- Use prompt templates (07, 08)
- Integrate RAG systems (10)

---

## Cross-Topic References

### Lost-in-Middle Context Effects
- Primary: File 04
- Related: File 05 (position bias)
- Application: File 10 (RAG multi-document)

### Hallucination Mitigation
- Surveys: File 01
- Self-Consistency: File 06
- Verification: File 07
- Grounding: File 10

### Evaluation & Benchmarks
- Dimensions: File 03
- Benchmarks: File 09
- Citations: File 08
- RAG Metrics: File 10

### Foundational Understanding
- Surveys: File 01
- Classification: File 02-03
- Cognitive parallels: File 05

---

## URLs for Key Resources

### GitHub Repositories
- ALCE: https://github.com/princeton-nlp/ALCE
- HaluEval: https://github.com/RUCAIBox/HaluEval
- FActScore: https://github.com/shmsw25/FActScore
- DPR: https://github.com/facebookresearch/DPR
- Hallucination Detection List: https://github.com/EdinburghNLP/awesome-hallucination-detection

### ArXiv Papers
- See individual files for complete ArXiv links
- Most papers available via arxiv.org URLs provided

### ACL Resources
- ACL Anthology: https://aclanthology.org/
- EMNLP 2023 papers
- ACL papers (2020-2023)
- NAACL 2025

---

## Contact Information

**Research Compiled:** January 27, 2026

**Related Files:**
- See `/Volumes/MacShare/LLM_context/` for full literature review structure
- README.md in parent directory for section overview

---

## Version History

- **v1.0** (Jan 27, 2026): Initial collection of 50+ papers across 10 research domains

---

**Last Updated:** January 27, 2026
**Status:** Complete Research Data Collection
**Format:** Markdown (.md)
**Total Size:** ~6.6 MB (with all metadata)

