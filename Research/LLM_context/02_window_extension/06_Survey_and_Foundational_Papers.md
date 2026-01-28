# Survey Papers and Foundational Work on Context Extension

## 1. Beyond the Limits: A Survey of Techniques to Extend Context Length
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** IJCAI 2024
**ArXiv ID:** 2402.02244
**Title:** Beyond the Limits: A Survey of Techniques to Extend the Context Length in Large Language Models
**URL:** https://arxiv.org/html/2402.02244v3

**Key Findings:**
Comprehensive survey organizing context extension techniques into five categories: length extrapolation (positional scaling methods), attention approximation (sparse/efficient mechanisms), attention-free transformers, model compression, and hardware-aware transformers. Covers the What, Why, and How of each approach with unified taxonomy for understanding the landscape of long-context LLM research and practical implementation considerations.

---

## 2. Awesome LLM Long-Context Modeling
**Authors:** Xnhyacinth et al.
**Year:** 2024
**Venue:** GitHub curated repository
**Status:** Community-maintained collection
**URL:** https://github.com/Xnhyacinth/Awesome-LLM-Long-Context-Modeling

**Key Findings:**
Curated list of must-read papers and blogs on LLM-based long-context modeling with detailed categorization by method type (position encoding, attention mechanisms, training strategies). Includes implementation links, model releases, and benchmarks, providing practical resource for researchers implementing context extension techniques.

---

## 3. How LLMs Scaled from 512 to 2M Context: A Technical Deep Dive
**Authors:** Amaar Agarwal
**Year:** 2025
**Venue:** Blog post (technical analysis)
**Status:** Comprehensive technical analysis
**URL:** https://amaarora.github.io/posts/2025-09-21-rope-context-extension.html

**Key Findings:**
Technical deep dive tracing evolution of RoPE scaling methods from 512-token baseline to 2M-token contexts, explaining mathematical foundations of Position Interpolation, NTK-aware scaling, YaRN, and advanced variants. Provides intuitive explanations of frequency domain dynamics and practical implementation details for understanding modern scaling approaches.

---

## 4. A Survey from the Perspective of Positional Encoding
**Authors:** Multiple researchers
**Year:** 2024
**Venue:** EMNLP 2024 Findings
**ArXiv ID:** Not directly cited but related
**Status:** Positional encoding-focused survey
**URL:** https://aclanthology.org/2024.findings-emnlp.582.pdf

**Key Findings:**
Focuses specifically on positional encoding approaches to context extension, analyzing fundamental tradeoffs between different encoding strategies (sinusoidal, learned, relative bias, rotary). Provides theoretical analysis of why certain encoding approaches enable better extrapolation and length generalization.

---

## 5. Constructing Transformers For Longer Sequences with Sparse Attention Methods
**Authors:** Google Research
**Year:** 2020
**Venue:** Google AI Blog
**Status:** Industry perspective/tutorial
**URL:** https://research.google/blog/constructing-transformers-for-longer-sequences-with-sparse-attention-methods/

**Key Findings:**
Google Research blog post synthesizing sparse attention approaches (Reformer, Longformer, BigBird) for long-sequence processing, explaining design principles and tradeoffs. Provides practical guidance for practitioners choosing between different approximation strategies based on task and hardware requirements.

---

## 6. Extending the RoPE: EleutherAI Blog
**Authors:** EleutherAI community
**Year:** 2023
**Venue:** EleutherAI Blog
**Status:** Community technical resource
**URL:** https://blog.eleuther.ai/yarn/

**Key Findings:**
Detailed technical blog explaining RoPE extension methods (NTK-aware, dynamic scaling, YaRN) with mathematical intuitions and practical guidance. Serves as community resource for understanding why RoPE scaling works and how different variants compare, widely referenced in implementation discussions.

---

## 7. Rotary Embeddings: A Relative Revolution
**Authors:** EleutherAI
**Year:** 2021
**Venue:** EleutherAI Blog
**Status:** Foundational explanation
**URL:** https://blog.eleuther.ai/rotary-embeddings/

**Key Findings:**
Foundational blog explaining rotary position embeddings (RoPE) from first principles, why they're superior to absolute and sinusoidal positions, and how they enable the relative position structure needed for extrapolation. Essential background for understanding why RoPE became dominant in modern LLMs (LLaMA, Mistral, Gemma).

---

## 8. ALiBi Deep Dive: Interpolation vs. Extrapolation
**Authors:** SambaNova
**Year:** 2022
**Venue:** SambaNova Blog
**Status:** Industry analysis
**URL:** https://sambanova.ai/blog/alibi-interpolation-vs-extrapolation

**Key Findings:**
Detailed comparison of ALiBi's extrapolation approach vs RoPE interpolation methods, explaining fundamental tradeoffs and why ALiBi excels at length extrapolation. Provides industry perspective on positional encoding design choices and practical considerations for model architects.

---

## 9. Inside RoPE: Rotary Magic into Position Embeddings
**Authors:** LearnOpenCV
**Year:** 2024
**Venue:** LearnOpenCV Blog
**Status:** Educational technical content
**URL:** https://learnopencv.com/rope-position-embeddings/

**Key Findings:**
Comprehensive educational explanation of RoPE mechanics with visualizations, walking through mathematics of rotary embeddings and how frequency components enable position encoding. Serves as pedagogical resource for understanding the foundations upon which all RoPE scaling methods build.

---

## 10. Context Rot: How Increasing Input Tokens Impacts LLM Performance
**Authors:** Chroma Research
**Year:** 2024
**Venue:** Chroma Research Blog
**Status:** Research findings
**URL:** https://research.trychroma.com/context-rot

**Key Findings:**
Empirical study showing performance degradation patterns as context length increases ("context rot"), analyzing why longer contexts sometimes hurt performance. Highlights importance of proper training and evaluation methodology when extending context windows, informing better evaluation practices.

---

## 11. The Transformer Family Version 2.0
**Authors:** Lil'Log (Lilian Weng)
**Year:** 2023
**Venue:** Lil'Log Blog
**Status:** Comprehensive transformer survey
**URL:** https://lilianweng.livejournal.com/posts/2023-01-27-the-transformer-family-v2/

**Key Findings:**
Comprehensive review of transformer variants including long-context approaches (Reformer, Longformer, BigBird, etc.), providing unified perspective on efficiency improvements and architectural innovations. Includes context extension methods within broader transformer landscape.

---

## 12. Demystifying Sparse Attention: A Comprehensive Guide
**Authors:** Vishal Singh (Medium)
**Year:** 2024
**Venue:** Medium
**Status:** Educational guide
**URL:** https://medium.com/@vishal09vns/sparse-attention-dad17691478c

**Key Findings:**
Educational guide demystifying sparse attention mechanisms, explaining common patterns and tradeoffs between different sparsity patterns. Helps practitioners understand when and why to choose specific sparse attention strategies for their applications.

---

## 13. Positional Embeddings in Transformers: A Math Guide to RoPE & ALiBi
**Authors:** Multiple contributors (Towards Data Science)
**Year:** 2024
**Venue:** Towards Data Science
**Status:** Educational technical content
**URL:** https://towardsdatascience.com/positional-embeddings-in-transformers-a-math-guide-to-rope-alibi/

**Key Findings:**
Mathematical explanation of RoPE and ALiBi with equations and intuitive explanations, helping readers understand positional encoding design principles. Compares approaches and explains why certain designs enable better extrapolation.

---

## Key Survey Takeaways

### Five Main Categories of Context Extension
1. **Length Extrapolation:** Positional scaling (PI, NTK-aware, YaRN, CLEX, LongRoPE)
2. **Attention Approximation:** Sparse/efficient attention (BigBird, Longformer, Ring Attention, Flash Attention)
3. **Attention-Free:** Alternative architectures (SSMs, etc.)
4. **Model Compression:** Quantization and pruning for long context
5. **Hardware-Aware:** Distributed training and inference strategies

### Timeline of Major Milestones

- **2020:** Reformer (LSH attention), Longformer (sliding window), BigBird (sparse patterns)
- **2021:** RoFormer (RoPE introduction), Rotary Embeddings paper
- **2022:** ALiBi, Flash Attention
- **2023:** Position Interpolation, NTK-aware scaling, YaRN, Ring Attention, StreamingLLM
- **2024:** LongRoPE (2M tokens), CLEX, E²-LLM, Landmark Attention, Distributed training methods
- **2025:** ComRoPE, SkyLadder (scheduling), continued advances

---

## Implementation Resources

- **EleutherAI:** Foundational technical understanding and implementations
- **HuggingFace:** Model hosting with context-extended variants
- **GitHub Awesome Lists:** Community-curated implementations and papers
- **ICLR/NeurIPS:** Peer-reviewed advances in long-context LLMs
- **ArXiv:** Preprints of latest context extension research

---

## References

- Main Survey: https://arxiv.org/html/2402.02244v3
- Awesome LLM Long-Context: https://github.com/Xnhyacinth/Awesome-LLM-Long-Context-Modeling
- EleutherAI Blog: https://blog.eleuther.ai/
- All Paths Lead to Transformers: https://amaarora.github.io/
