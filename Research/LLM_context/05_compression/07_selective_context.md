# Selective Context: Compressing Context to Enhance Inference Efficiency

**Authors:** Li et al. (Yucheng Li, Bo Dong, Frank Guerin, Chenghua Lin)

**Year:** 2023

**Venue:** Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)

**arXiv ID:** 2310.06201

**Publication:** Proceedings of EMNLP 2023, Main Conference

**Key Concept:**
Selective Context is a method that enhances the inference efficiency of large language models by identifying and pruning redundancy in the input context to make the input more compact.

**Problem Statement:**
- LLMs face challenges managing long documents and extended conversations
- Significantly increased computational requirements in memory and inference time
- Context truncation when input exceeds LLM's fixed context length
- Need to balance compression with semantic preservation

**Technical Approach:**
1. **Redundancy Identification:** Detects redundant information in input
2. **Selective Pruning:** Removes identified redundancy while preserving key information
3. **Context Compaction:** Creates more compact input representation
4. **Semantic Preservation:** Maintains critical information for downstream tasks

**Performance Results:**
- 50% reduction in context cost
- 36% reduction in inference memory usage
- 32% reduction in inference time
- Minor performance drop:
  - 0.023 drop in BERTscore
  - 0.038 drop in faithfulness
- Maintains comparable performance to full context

**Evaluation Datasets:**
Tested on diverse document types and tasks:
1. **Document Types:**
   - arXiv papers (academic content)
   - News articles (journalistic content)
   - Long conversations (dialogue)

2. **Tasks:**
   - Summarization
   - Question answering
   - Response generation

**Key Metrics:**
- Memory cost reduction: 50%
- Memory usage: 36% reduction
- Inference time: 32% reduction
- Semantic preservation quality measures

**Applications:**
- Long document processing
- Conversation history compression
- Knowledge-intensive tasks
- Multi-turn dialogue systems
- Document summarization with resource constraints

**Advantages:**
- Significant memory and latency improvements
- Minimal performance degradation
- Applicable to diverse document types
- Task-agnostic compression approach
- Production-ready efficiency gains

**Implementation Details:**
- Context pruning algorithm
- Redundancy detection mechanism
- Integration with LLM inference pipeline

**Availability:**
- Available on PyPI: selective-context package
- GitHub repository: Selective_Context
- Python-based implementation

## References
- [Compressing Context to Enhance Inference Efficiency of Large Language Models - ACL Anthology](https://aclanthology.org/2023.emnlp-main.391/)
- [Selective Context - arXiv](https://arxiv.org/abs/2310.06201)
- [Selective Context GitHub Repository](https://github.com/liyucheng09/Selective_Context)
- [Selective Context PyPI Package](https://pypi.org/project/selective-context/)
- [Paper on ResearchGate](https://www.researchgate.net/publication/376401484_Compressing_Context_to_Enhance_Inference_Efficiency_of_Large_Language_Models)
