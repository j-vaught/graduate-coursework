# AutoCompressor: Adapting Language Models to Compress Contexts

**Authors:** Chevalier et al.

**Year:** 2023

**Venue:** Conference on Empirical Methods in Natural Language Processing (EMNLP 2023)

**Publication:** Proceedings of EMNLP 2023

**Key Concept:**
AutoCompressor is a method to adapt pre-trained language models into models capable of compressing long contexts into summary vectors, which are then accessible to the model as soft prompts.

**Architecture:**
- Adapts pre-trained models (OPT, Llama-2) for context compression
- Compresses long documents into summary vectors
- Summary vectors passed as soft prompts to the model
- Unsupervised training objective on long sequences

**Training Approach:**
- Fine-tuned on sequences of up to 30,720 tokens
- Processes long documents in segments
- Summary vectors from all previous segments used in language modeling
- Unsupervised objective for learning compression

**Key Contributions:**
- Summary vectors are good substitutes for plain-text demonstrations
- Improved perplexity on long context tasks
- Efficient compression without task-specific training

**Performance Results:**
- Significantly improves perplexity on long sequences
- Summary vectors substitute effectively for plain-text demonstrations
- Maintains semantic information in compressed representations

**Applications:**
- In-context learning with compressed task demonstrations
- Long document processing and understanding
- Context summarization for inference

**Implementation:**
- Pre-trained models available on Hugging Face
- Both OPT and Llama-2 based versions available
- Official implementation and code available

**Advantages:**
- Leverages existing pre-trained models
- Unsupervised training approach
- Effective compression without task-specific fine-tuning
- Demonstrates semantic preservation in summary vectors

**Related Models:**
- AutoCompressor-2.7b-6k (available on Hugging Face)
- OPT-based variants
- Llama-2 based variants

## References
- [Adapting Language Models to Compress Contexts - ACL Anthology](https://aclanthology.org/2023.emnlp-main.232/)
- [AutoCompressors GitHub Repository](https://github.com/princeton-nlp/AutoCompressors)
- [AutoCompressor-2.7b-6k Model Card - Hugging Face](https://huggingface.co/princeton-nlp/AutoCompressor-2.7b-6k)
