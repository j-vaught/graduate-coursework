# LongLLMLingua: Long Context Prompt Compression

**Authors:** Same team as LLMLingua (Microsoft Research)

**Year:** 2024

**Venue:** ACL 2024, ICLR ME-FoMo 2024

**arXiv ID:** 2310.06839

**Publication:** ACL Anthology 2024.acl-long.91

**Key Concept:**
LongLLMLingua extends the original LLMLingua approach to address specific challenges in long context scenarios, including position bias, performance reduction, and computational cost.

**Problem Statement:**
Three main challenges in long context scenarios:
1. Higher computational cost
2. Performance reduction due to long contexts
3. Position bias ("lost in the middle" problem)

**Technical Approach:**
Four key components:
1. **Question-aware Coarse-to-Fine Compression:** Task-specific compression rates
2. **Document Reordering Mechanism:** Strategic document positioning
3. **Dynamic Compression Ratios:** Adaptive compression based on input complexity
4. **Subsequence Recovery Strategy:** Improves LLM's perception of key information

**Performance Results:**
- Up to 21.4% performance boost on NaturalQuestions benchmark
- 4× compression with minimal token usage
- 1.4× to 2.6× end-to-end latency acceleration
- Tested on 10k-token prompts with 2-6× compression ratios

**Position Bias Mitigation:**
- Addresses "Lost in the Middle" phenomenon
- Mitigates position bias in long context scenarios
- Effective document scheduling within context window
- Optimizes utilization of limited context windows

**Applications:**
- Chain-of-Thought (CoT) prompting
- Long context processing
- Retrieval-Augmented Generation (RAG)
- Multi-document question answering
- Long context reasoning tasks

**Key Advantages:**
- Dramatically reduces computational overhead
- Maintains or improves performance with compression
- Addresses position bias in long contexts
- Effective for RAG systems
- Reduces costs for long-document processing

**Comparison to LLMLingua:**
- Specifically designed for long context scenarios
- More sophisticated document handling
- Dynamic compression instead of fixed ratios
- Better handling of position bias

**Use Cases:**
- RAG systems with multiple documents
- Long-form document understanding
- Extended conversation context
- Complex reasoning with multiple examples
- Knowledge-intensive tasks

## References
- [LongLLMLingua: Accelerating and Enhancing LLMs in Long Context Scenarios - arXiv](https://arxiv.org/abs/2310.06839)
- [LongLLMLingua - ACL Anthology](https://aclanthology.org/2024.acl-long.91/)
- [LongLLMLingua Official Website](https://llmlingua.com/longllmlingua.html)
- [LLMLingua GitHub Repository](https://github.com/microsoft/LLMLingua)
- [LongLLMLingua Blog Post - LlamaIndex](https://www.llamaindex.ai/blog/longllmlingua-bye-bye-to-middle-loss-and-save-on-your-rag-costs-via-prompt-compression-54b559b9ddf7)
