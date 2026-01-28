# Continual Pretraining and Fine-Tuning for Context Extension

## 1. LongAlign: A Recipe for Long Context Alignment
**Authors:** Bai et al. (and collaborators)
**Year:** 2024
**Venue:** ICLR 2024 (appears in OpenReview)
**ArXiv ID:** 2401.18058
**Status:** OpenReview submission
**URL:** https://openreview.net/pdf/93c2ba049b662e3e2740a768f098238bf0299a16.pdf

**Key Findings:**
LongAlign provides comprehensive recipe for long-context alignment extending to 64K tokens through: expanding RoPE base frequency 200x (10K to 2M), conducting continual training on ≤64K sequences for 10B tokens, and developing loss-weighting strategies for packed training with varied lengths. Outperforms existing recipes by up to 30% on long-context tasks while maintaining short-context proficiency through carefully engineered data construction and training procedures.

---

## 2. E²-LLM: Efficient and Extreme Length Extension
**Authors:** Xnhyacinth et al.
**Year:** 2024
**Venue:** ACL 2024 Findings
**ArXiv ID:** 2401.06951
**Title:** E^2-LLM: Efficient and Extreme Length Extension of Large Language Models
**URL:** https://arxiv.org/abs/2401.06951

**Key Findings:**
E²-LLM achieves extreme length extension through single efficient training on short sequences (e.g., 4K) with dual RoPE augmentation strategy that scales and adjusts position indices across samples. Dramatically reduces continual pretraining cost and eliminates need for long-context data collection while supporting variable evaluation context windows, demonstrating superior performance on long-context benchmarks.

---

## 3. CLEX: Continuous Length Extrapolation for Large Language Models
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** ICLR 2024
**ArXiv ID:** 2310.16450
**Title:** CLEX: Continuous Length Extrapolation for Large Language Models
**URL:** https://arxiv.org/abs/2310.16450

**Key Findings:**
CLEX models continuous length extrapolation dynamics through ordinary differential equations over length scaling factors, enabling smooth context extension to 4x-8x training length without performance degradation. A 4K-trained model achieves competitive 32K-performance on LongBench, with minimal training/inference latency impact and seamless integration into RoPE-equipped LLMs (LLaMA, GPT-NeoX).

---

## 4. Data Engineering for Scaling Language Models to 128K Context
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2402.10171
**Status:** Industry implementation paper
**URL:** https://huggingface.co/papers/2402.10171

**Key Findings:**
Comprehensive study of data engineering for long-context scaling to 128K tokens, addressing challenges in training data construction, curriculum design, and evaluation. Demonstrates that data quality and diversity are critical for effective continual pretraining, with strategic data selection outperforming naive long-sequence collection approaches.

---

## 5. Code Llama: Open Foundation Models for Code
**Authors:** Meta AI (Rozière et al.)
**Year:** 2023
**Venue:** arXiv/Blog
**ArXiv ID:** 2308.12950
**Status:** Production model
**URL:** https://arxiv.org/abs/2308.12950

**Key Findings:**
Code Llama incorporates length extension through continual pretraining on code sequences, leveraging code's structural properties for extended context. The model achieves 8K-100K context windows through careful fine-tuning and position embedding scaling, demonstrating effectiveness of continual pretraining approach for specialized domain (programming) long-context extension.

---

## 6. LongSkywork: A Training Recipe for Context Extension
**Authors:** Skywork Team
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2406.00605
**Title:** LongSkywork: A Training Recipe for Efficiently Extending Context Length in Large Language Models
**URL:** https://arxiv.org/html/2406.00605v1

**Key Findings:**
LongSkywork provides end-to-end training recipe for efficient context extension through: dynamic batching with sorted sequences, efficient packed training with loss weighting, context window scheduling, and instruction tuning. Demonstrates state-of-the-art long-context performance through careful engineering of training procedures without requiring massive long-context datasets.

---

## 7. Domain Adaptation through Continual Pre-Training and Model Merging
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2406.14971
**Title:** Domain Adaptation of Llama3-70B-Instruct through Continual Pre-Training and Model Merging: A Comprehensive Evaluation
**URL:** https://arxiv.org/html/2406.14971v1

**Key Findings:**
Comprehensive evaluation of continual pretraining for domain adaptation showing that catastrophic forgetting is a significant challenge, mitigated through learning rate warming-then-decaying. Provides practical guidance on balancing downstream task performance with general knowledge retention, applicable to long-context adaptation scenarios.

---

## 8. When Long Helps Short: How Context Length in Supervised Fine-tuning Affects Behavior
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** arXiv
**ArXiv ID:** 2509.18762
**Title:** When Long Helps Short: How Context Length in Supervised Fine-tuning Affects Behavior of Large Language Models
**URL:** https://arxiv.org/html/2509.18762v1

**Key Findings:**
Analysis showing supervised fine-tuning at extended context lengths improves short-context performance, contrary to expectations. Demonstrates bidirectional relationship between short and long-context capabilities during training, informing design of efficient multi-scale context training procedures.

---

## 9. SkyLadder: Context Window Scheduling for Efficient Pretraining
**Authors:** Multiple researchers
**Year:** 2025
**Venue:** arXiv
**ArXiv ID:** 2503.15450
**Title:** SkyLadder: Better and Faster Pretraining via Context Window Scheduling
**URL:** https://arxiv.org/html/2503.15450v1

**Key Findings:**
Introduces context window scheduling during pretraining, progressively increasing sequence length across training phases. Reduces total compute while improving final model quality, demonstrating that curriculum-based sequence length scheduling is more efficient than static long-context training.

---

## 10. Synthetic Continued Pretraining
**Authors:** Yang & Zhu (ZitongYang collaborators)
**Year:** 2024
**Venue:** GitHub/arXiv
**Status:** Implementation and evaluation
**URL:** https://github.com/zitongyang/synthetic_continued_pretraining

**Key Findings:**
Explores synthetic data generation for continued pretraining to extend context, reducing dependency on natural long-context corpora. Demonstrates feasibility of synthesizing training data for length extension, relevant for resource-constrained settings where natural long sequences are scarce.

---

## Training Strategy Comparison

| Method | Training Cost | Data Required | Context Achieved | Key Strategy |
|--------|--------------|---------------|------------------|----------------|
| LongAlign | Moderate | 10B tokens | 64K | RoPE scaling + continual training |
| E²-LLM | Low | Short sequences only | Extreme | Dual RoPE augmentation |
| CLEX | Low | Standard pretrain | 4-8x baseline | ODE-based extrapolation |
| LongSkywork | Moderate | Curated long data | 128K+ | Curriculum + packed training |
| Code Llama | Moderate | Code corpus | 100K | Domain-specific continual training |
| SkyLadder | Low | Standard pretrain | Long | Progressive scheduling |

---

## Key Technical Components

### RoPE Frequency Scaling
- Base frequency expansion: typically 10K → 2M (200x) or adaptive factors
- Used in conjunction with position interpolation variants (PI, NTK-aware, YaRN)

### Training Procedures
1. **Packed Training:** Process variable-length sequences efficiently with loss weighting
2. **Curriculum Learning:** Progressive increase in sequence length during training
3. **Data Construction:** Mix of synthetic and natural long-sequence data
4. **Loss Weighting:** Balanced contribution across packed sequences

### Evaluation
- **LongBench:** Standard benchmark for real-world long-context tasks
- **Needle-in-Haystack:** Synthetic tests for retrieval in extended contexts
- **Domain-specific:** Code understanding, long document QA, summarization

---

## References

- Awesome LLM Long-Context: https://github.com/Xnhyacinth/Awesome-LLM-Long-Context-Modeling
- Continued Pretraining Guide: https://docs.unsloth.ai/basics/continued-pretraining
- Continue Pretraining Tutorials: https://unsloth.ai/blog/contpretraining
