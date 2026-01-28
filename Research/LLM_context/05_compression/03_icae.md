# ICAE: In-Context Autoencoder for Context Compression

**Authors:** Ge et al.

**Year:** 2024

**Venue:** International Conference on Learning Representations (ICLR 2024)

**arXiv ID:** 2307.06945

**Publication Date:** July 2023 (arXiv), ICLR 2024 (conference)

**Key Concept:**
The In-context Autoencoder (ICAE) leverages the power of a large language model (LLM) to compress a long context into short compact memory slots that can be directly conditioned on by the LLM for various purposes.

**Architecture:**
Two-module design:
1. **Encoder Module:** Learnable encoder adapted with LoRA from an LLM
   - Compresses long context into limited number of memory slots
   - Parameter-efficient adaptation using Low-Rank Adaptation
2. **Decoder Module:** Fixed target LLM
   - Conditions on memory slots for various purposes
   - Generates outputs based on compressed representations

**Training Approach:**
1. **Pretraining Phase:**
   - Uses both autoencoding and language modeling objectives
   - Trained on massive text data
   - Generates memory slots accurately representing original context

2. **Fine-tuning Phase:**
   - Fine-tuned on instruction data
   - Produces desirable responses to various prompts
   - Task-specific optimization

**Performance Metrics:**
- Lightweight implementation with fewer than 1% additional parameters
- Achieves 4× context compression based on Llama
- Improved latency during inference
- Reduced GPU memory cost during inference

**Advantages:**
- Minimal parameter overhead (< 1%)
- Effective compression ratio (4×)
- Both autoencoding and language modeling objectives
- Maintains semantic information in memory slots
- Efficient inference with reduced latency and memory

**Applications:**
- Long document processing
- In-context learning with compressed context
- Question answering on long texts
- Summarization with compressed context

**Availability:**
- Code and models available at GitHub repository
- Implementation details provided
- Compatible with Llama-based models

## References
- [In-context Autoencoder for Context Compression in a Large Language Model - arXiv](https://arxiv.org/abs/2307.06945)
- [ICAE GitHub Repository](https://github.com/getao/icae)
- [Published as conference paper at ICLR 2024](https://proceedings.iclr.cc/paper_files/paper/2024/file/0b276510ec2d3f6613a8b60c41ff0438-Paper-Conference.pdf)
- [Paper Page - Hugging Face](https://huggingface.co/papers/2307.06945)
