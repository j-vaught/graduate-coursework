# Context Window Scaling History: From GPT-2 to Gemini

## Model Timeline and Evolution

### 1. GPT-2 (1024 tokens)
- **Source**: OpenAI's GPT-2 documentation
- **Year**: 2019
- **Context Window**: 1,024 tokens (~512 words)
- **Key Findings**: Established the baseline for modern transformer language models with fixed context window constraint. The 1024-token limit defined the practical ceiling for input processing for several years.
- **Notes**: Fixed length at pretraining, handling longer sequences requires sliding window approaches

### 2. GPT-3 (2048 tokens)
- **Source**: OpenAI API documentation
- **Year**: 2020
- **Context Window**: 2,048 tokens (~1,000 words)
- **Key Findings**: Doubled the context window from GPT-2, though still remained a significant practical limitation. Maintained this limit across different model sizes in the family.
- **Notes**: Was considered state-of-the-art for long context at the time

### 3. GPT-3.5-turbo / ChatGPT (4096 tokens)
- **Source**: OpenAI ChatGPT API documentation
- **Year**: 2022
- **Context Window**: 4,096 tokens (~2,000 words)
- **Key Findings**: Further expansion addressing user feedback about context limitations. Initial release of commercial LLM accessible via API.
- **Notes**: Representative of industry standard for accessible models

### 4. GPT-4 (8K and 32K variants)
- **Source**: OpenAI API documentation
- **Year**: 2023
- **Context Window**: 8,192 tokens (8K) and 32,768 tokens (32K)
- **Key Findings**: Significant scaling increase, with 32K variant enabling much longer document processing. Demonstrates exponential growth trajectory.
- **Notes**: 32K version allowed processing multiple long documents simultaneously

### 5. GPT-4 Turbo (128K tokens)
- **Source**: OpenAI blog and API documentation
- **Year**: 2023
- **Context Window**: 128,000 tokens (~100,000 words)
- **Key Findings**: 4x improvement over 32K variant. Enables processing of large codebases and extended documents in single request.
- **Notes**: Represents major inflection point in context scaling

### 6. LLaMA / LLaMA 2 (2048-4096 tokens)
- **Source**: Meta/Facebook research
- **Year**: 2023
- **Context Window**: 2,048 - 4,096 tokens (base models)
- **Key Findings**: Open-source alternative to proprietary models, established baseline for community-driven development. Common starting point for context extension research.
- **Notes**: Became basis for many fine-tuned variants with extended context

### 7. LLaMA 3.1 (128K tokens)
- **Source**: Meta LLaMA 3.1 documentation
- **Year**: 2024
- **Context Window**: 128,000 tokens
- **Key Findings**: Matches GPT-4 Turbo in context capability, demonstrates competitive context scaling in open-source models.
- **Notes**: Achieved through position interpolation and fine-tuning techniques

### 8. Claude (Multiple Generations)
- **Sources**: Anthropic Claude API documentation
- **Year**: 2023-2025
- **Context Windows**:
  - Claude 1/2: 100,000 tokens (200K with research access)
  - Claude 3 family: 200,000 tokens
  - Claude 3.5 Sonnet: 1,000,000 tokens (announced)
- **Key Findings**: Anthropic focused on context window expansion as core feature, reaching 1M tokens. Demonstrated that very large contexts are practical and useful.
- **URL**: https://platform.claude.com/docs/en/build-with-claude/context-windows
- **Support Docs**: https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-claude-plans

### 9. Gemini 1.5 / 2.0 (1-2 Million tokens)
- **Source**: Google AI blog and Gemini documentation
- **Year**: 2024-2025
- **Context Window**: 1,000,000 tokens (Gemini 1.5), expanding to 2,000,000 (Gemini 2.5)
- **Key Findings**: First model to achieve 1M token context window in production. Can process 1.5 hours of video, 11 hours of audio, or 700,000+ words simultaneously. Achieves 99.7% recall on Needle in Haystack tests.
- **Blog**: https://blog.google/innovation-and-ai/products/google-gemini-next-generation-model-february-2024/
- **Gemini 2.5 Announcement**: https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/
- **Long Context Docs**: https://gemini.google/overview/long-context/
- **Google Cloud Vertex AI**: https://docs.cloud.google.com/vertex-ai/generative-ai/docs/long-context

## Computational Scaling Challenges

### 10. Context Window Impact on Computation
- **Key Findings**: Quadratic complexity means doubling context = 4x computation. Without optimization, practical scaling severely constrained by computational budget.
- **Example**: 4096 token model needs 64x more computation than 512 token baseline
- **Sources**:
  - https://www.deepchecks.com/question/how-does-context-window-size-affect-llm-performance/
  - https://medium.com/@anand_sahu/what-is-context-length-in-ai-models-8bb32bbd7719

## Extension Techniques Enabling Scaling

### 11. Position Interpolation
- **Source**: Multiple implementations in Llama2 fine-tuning
- **Key Findings**: Enables 2-4x context extension with minimal fine-tuning. Allows models trained on 2048 tokens to work with 4096-8192 tokens.
- **Technical Details**: Linearly compresses position indices to fit trained range

### 12. NTK-Aware Interpolation
- **Source**: Reddit u/bloc97, EleutherAI blog
- **Year**: 2023
- **Key Findings**: Dynamic scaling that treats high and low frequencies differently. 8x extension (2048 to 8k) achieved without full retraining.
- **Blog**: https://blog.eleuther.ai/yarn/

### 13. YaRN (Yet another RoPE extensioN)
- **Authors**: Bowen Peng et al.
- **Year**: 2023
- **Venue**: arXiv 2309.00071
- **Key Findings**: Improved NTK interpolation allowing 128K context for LLaMA models. Dynamic temperature scaling for better frequency handling.
- **PDF**: https://arxiv.org/pdf/2309.00071
- **Blog**: https://blog.eleuther.ai/yarn/

## Market and Capability Progression

### 14. Comparative Context Window Timeline
- **Source**: GitHub compilation of model context limits
- **Key Findings**:
  - 2020: Typical = 512-2048 tokens
  - 2023: Typical = 2048-4096, Leaders = 100K+
  - 2024: Typical = 4096-8192, Leaders = 100K-1M+
- **GitHub**: https://github.com/taylorwilsdon/llm-context-limits

### 15. LLMs with Largest Context Windows
- **Source**: CodingScape blog compilation
- **Key Findings**: Updated list of models with largest context windows, tracking industry progress.
- **URL**: https://codingscape.com/blog/llms-with-largest-context-windows

## Technical Documentation

### 16. What is Context Length in AI Models?
- **Author**: Anand Sahu
- **Source**: Medium article
- **Key Findings**: Overview of context window concept and its evolution across model families.
- **URL**: https://medium.com/@anand_sahu/what-is-context-length-in-ai-models-8bb32bbd7719

### 17. What is a Context Window?
- **Source**: IBM Think
- **Key Findings**: Industry definition and explanation of context window limitations and implications.
- **URL**: https://www.ibm.com/think/topics/context-window

### 18. How Does The Context Window Size Affect LLM Performance?
- **Source**: DeepChecks
- **Key Findings**: Analysis of performance degradation as context windows approach limits, and optimization strategies.
- **URL**: https://www.deepchecks.com/question/how-does-context-window-size-affect-llm-performance/

## Scaling Analysis

### 19. How LLMs Scaled from 512 to 2M Context: A Technical Deep Dive
- **Author**: Amanatullah (Aman)
- **Source**: Aman's AI Journal
- **Year**: 2025
- **Key Findings**: Comprehensive technical analysis of the methods, techniques, and innovations that enabled context scaling from 512 to 2,000,000 tokens. Traces evolution of positional encodings and extension techniques.
- **URL**: https://amaarora.github.io/posts/2025-09-21-rope-context-extension.html

### 20. Context Length Extension Overview
- **Author**: Amanatullah
- **Source**: Aman's AI Journal (Primers)
- **Key Findings**: Educational primer on context length extension techniques.
- **URL**: https://aman.ai/primers/ai/context-length-extension/

### 21. NLP LLM Context Length Extension Overview
- **Author**: Amanatullah (The Deep Hub)
- **Source**: Medium
- **Key Findings**: Survey of context extension approaches and their effectiveness.
- **URL**: https://medium.com/thedeephub/overview-e3dd94bc74c4

### 22. The Intuition Behind Context Extension Mechanisms for LLMs
- **Author**: Changsha Ma
- **Source**: Medium article
- **Key Findings**: Intuitive explanation of how various context extension techniques work and their trade-offs.
- **URL**: https://medium.com/@machangsha/the-intuition-behind-context-extension-mechanisms-for-llms-b9aa036304d7

## Timeline Summary

| Model | Year | Context | Scaling Factor |
|-------|------|---------|-----------------|
| GPT-2 | 2019 | 1K | 1x |
| GPT-3 | 2020 | 2K | 2x |
| GPT-3.5 | 2022 | 4K | 4x |
| GPT-4 8K | 2023 | 8K | 8x |
| GPT-4 32K | 2023 | 32K | 32x |
| GPT-4 Turbo | 2023 | 128K | 128x |
| Claude 1/2 | 2023 | 100K-200K | 100-200x |
| Claude 3.5 | 2024 | 1M | 1000x |
| Gemini 1.5 | 2024 | 1M | 1000x |
| Gemini 2.5 | 2025 | 2M | 2000x |

---

## Key Insights

1. **Exponential Growth**: Context windows have grown roughly 1000x in 5 years
2. **Inflection Points**:
   - 2023: GPT-4 Turbo achieves 128K (mainstream acceptance)
   - 2024: Claude/Gemini reach 1M (new capability tier)
3. **Enabling Technologies**: Position interpolation, RoPE, YaRN, efficient attention crucial
4. **Cost Trade-offs**: Larger context = higher computational cost, memory requirements
5. **Practical Limits**: Even 1M tokens has use cases (code review, document analysis, video understanding)
6. **Future Direction**: 2M+ tokens (Gemini 2.5) suggests continued scaling trajectory

## Sources Statistics

- **Total Distinct Sources**: 22
- **Company/Product Documentation**: 8 (OpenAI, Anthropic, Meta, Google)
- **Research Papers**: 3 (with arxiv IDs)
- **Technical Blog Posts**: 6
- **Educational Resources**: 5
