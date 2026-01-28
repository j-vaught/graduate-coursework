# LLMLingua: Compressing Prompts for Accelerated Inference

**Authors:** Jiang et al. (Huiqiang Jiang, Qianhui Wu, Chin-Yew Lin, Yuqing Yang, Lili Qiu)

**Year:** 2023

**Venue:** Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)

**arXiv ID:** 2310.05736

**Publication:** ACL Anthology 2023.emnlp-main.825

**Key Concept:**
LLMLingua is a coarse-to-fine prompt compression method that leverages small language models' perplexity to measure token redundancy and identify low-importance tokens for removal.

**Motivation:**
- Advancements in Chain-of-Thought (CoT) prompting create increasingly lengthy prompts
- In-context learning (ICL) requires extensive examples
- Need to accelerate LLM inference and reduce costs
- Prompts can exceed tens of thousands of tokens

**Technical Approach:**
1. **Budget Controller:** Maintains semantic integrity under high compression ratios
2. **Token-level Iterative Compression:** Better models interdependence between compressed contents
3. **Instruction Tuning:** Distribution alignment between language models
4. **Perplexity-based Importance Ranking:** Uses small language model perplexity

**Key Components:**
- Uses well-trained small language models (GPT2-small, LLaMA-7B)
- Coarse-to-fine compression strategy
- Three modules assigning varying compression rates to different prompt segments
- Iterative refinement for optimal compression

**Performance Results:**
- Up to 20× compression with minimal performance loss
- Tested on four different datasets:
  - GSM8K (in-context learning)
  - BBH (reasoning)
  - ShareGPT (conversation)
  - Arxiv-March23 (summarization)
- State-of-the-art performance maintained

**Applications:**
- In-context learning acceleration
- Chain-of-Thought reasoning optimization
- Conversation compression
- Summarization tasks
- Cost reduction for LLM API calls

**Advantages:**
- High compression ratios (up to 20×)
- Minimal performance degradation
- Works with different small language models
- Applicable to diverse downstream tasks
- Reduces inference latency and cost

**Distribution Alignment:**
- Instruction tuning-based method
- Ensures compressed prompts align with LLM's typical input distribution
- Improves robustness across different models

## References
- [LLMLingua: Compressing Prompts for Accelerated Inference - arXiv](https://arxiv.org/abs/2310.05736)
- [LLMLingua - ACL Anthology](https://aclanthology.org/2023.emnlp-main.825/)
- [LLMLingua Official Website](https://llmlingua.com/llmlingua.html)
- [LLMLingua Research Blog - Microsoft Research](https://www.microsoft.com/en-us/research/blog/llmlingua-innovating-llm-efficiency-with-prompt-compression/)
- [LLMLingua GitHub Repository](https://github.com/microsoft/LLMLingua)
