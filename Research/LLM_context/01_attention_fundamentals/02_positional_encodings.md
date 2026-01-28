# Positional Encodings: Sinusoidal, Learned, and Relative

## Foundational Work

### 1. Attention Is All You Need (Sinusoidal PE)
- **Authors**: Vaswani et al.
- **Year**: 2017
- **Venue**: NeurIPS
- **Key Findings**: Introduces sinusoidal positional encodings using sine and cosine functions of varying wavelengths. First implementation of absolute positional encoding in Transformers. Demonstrates that sinusoidal encodings allow relative position computation through dot products.
- **URL**: https://arxiv.org/abs/1706.03762

## Relative Position Representations

### 2. Self-Attention with Relative Position Representations
- **Authors**: Peter Shaw, Jakob Uszkoreit, Ashish Vaswani (Google)
- **Year**: 2018
- **Venue**: NAACL (Conference of the North American Chapter of the Association for Computational Linguistics)
- **Key Findings**: Introduces relative positional encoding that encodes pairwise distances between sequence elements instead of absolute positions. Achieves 1.3 BLEU improvement on WMT 2014 English-to-German and 0.3 BLEU on French translation. Key advantage: can generalize to sequences longer than training length.
- **URL**: https://arxiv.org/abs/1803.02155
- **PDF**: https://arxiv.org/pdf/1803.02155
- **Additional**: https://aclanthology.org/N18-2074/

### 3. Relative Positional Encoding (Study Notes)
- **Author**: Jake Tae
- **Source**: Educational blog post
- **Key Findings**: Detailed breakdown of Shaw et al. relative positional encoding mechanism, showing how it enables better length generalization compared to absolute positional encodings.
- **URL**: https://jaketae.github.io/study/relative-positional-encoding/

### 4. On Scalar Embedding of Relative Positions in Attention Models
- **Authors**: AAAI conference paper
- **Year**: 2021
- **Venue**: AAAI
- **Key Findings**: Analysis of how relative positions can be embedded as scalar values in attention computation, exploring alternatives to pairwise distance matrices.
- **URL**: https://cdn.aaai.org/ojs/17654/17654-13-21148-1-2-20210518.pdf

## Transformer-XL and Segment Recurrence

### 5. Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context
- **Authors**: Zihang Dai, Zhigang Yang, Yiming Yang, Jaime Carbonell, Quoc V. Le, Ruslan Salakhutdinov (CMU, Google)
- **Year**: 2019
- **Venue**: ACL (Association for Computational Linguistics)
- **Key Findings**: Introduces segment-level recurrence and relative positional encodings to handle longer dependencies. Can model 80-133% longer dependencies than RNNs and 291-447% longer than vanilla Transformer. Replaces absolute positions with relative encodings to avoid "temporal confusion" across segments.
- **URL**: https://arxiv.org/abs/1901.02860
- **PDF**: https://aclanthology.org/P19-1285/
- **Blog**: https://medium.com/@hassaanidrees7/exploring-the-transformer-xl-handling-long-contexts-in-text-63d31c8c9a36

### 6. Transformer-XL Relative Position Encoding (Guide)
- **Source**: APXML course material
- **Key Findings**: Comprehensive explanation of how Transformer-XL's relative positional encoding mechanism works, with practical implementation details.
- **URL**: https://apxml.com/courses/how-to-build-a-large-language-model/chapter-13-positional-encoding-variations/transformer-xl-relative-positional-encoding

## Rotary Position Embeddings (RoPE)

### 7. RoFormer: Enhanced Transformer with Rotary Position Embedding
- **Authors**: Jianlin Su et al.
- **Year**: 2021
- **Venue**: arXiv preprint (2104.09864)
- **Key Findings**: Introduces RoPE (Rotary Position Embedding) that encodes absolute position with rotation matrices while incorporating relative position dependency. Enables flexible sequence length, decaying inter-token dependency with distance, and linear self-attention with relative position encoding.
- **URL**: https://arxiv.org/abs/2104.09864
- **PDF**: https://arxiv.org/pdf/2104.09864

### 8. Understanding Rotary Position Embeddings (RoPE): A Visual Guide
- **Author**: Saeed Mehrang
- **Source**: Medium article
- **Key Findings**: Visual explanation of how RoPE works by rotating query and key vectors by angles proportional to token position. Shows clear geometric intuition behind relative position encoding through rotation.
- **URL**: https://medium.com/@saeed.mehrang/understanding-rotary-position-embeddings-rope-a-visual-guide-ef8319353ddb

### 9. Rotary Embeddings: A Relative Revolution
- **Source**: EleutherAI Blog
- **Key Findings**: Analysis of RoPE's advantages for modern language models, explaining why it became popular in models like LLaMA and other contemporary LLMs.
- **URL**: https://blog.eleuther.ai/rotary-embeddings/

### 10. Inside RoPE: Rotary Magic into Position Embeddings
- **Source**: LearnOpenCV blog
- **Key Findings**: In-depth technical exploration of RoPE mechanics and its mathematical foundation.
- **URL**: https://learnopencv.com/rope-position-embeddings/

### 11. On N-dimensional Rotary Positional Embeddings
- **Author**: Jerry (jio)
- **Source**: Technical blog post
- **Key Findings**: Extension of RoPE to multi-dimensional settings, exploring generalizations beyond 2D rotation matrices.
- **URL**: https://jerryxio.ng/posts/nd-rope/

### 12. An In-depth Exploration of Rotary Position Embedding (RoPE)
- **Source**: Aman's AI Journal Substack
- **Key Findings**: Comprehensive walkthrough of RoPE with mathematical proofs and implementation considerations.
- **URL**: https://aiexpjourney.substack.com/p/an-in-depth-exploration-of-rotary-position-embedding-rope-ac351a45c794

### 13. Rotary Position Embeddings for Long Context Length
- **Source**: MachineLearningMastery
- **Key Findings**: Practical guide showing how RoPE enables longer context lengths and improved generalization beyond training lengths.
- **URL**: https://machinelearningmastery.com/rotary-position-embeddings-for-long-context-length/

## Learned vs. Sinusoidal Comparison

### 14. Sinusoidal vs Learned Positional Embeddings
- **Source**: APXML course comparison
- **Key Findings**: Comparative analysis showing learned embeddings work well with sufficient data (BERT, GPT) while sinusoidal encodings provide better extrapolation and determinism.
- **URL**: https://apxml.com/courses/foundations-transformers-architecture/chapter-4-positional-encoding-embedding-layer/comparing-positional-encodings

### 15. Understanding Sinusoidal Positional Encoding in Transformers
- **Author**: Pranay Janupalli
- **Source**: Medium article
- **Year**: Unknown
- **Key Findings**: Detailed mathematical and intuitive explanation of why sinusoidal encodings work, including Fourier analysis perspective.
- **URL**: https://medium.com/@pranay.janupalli/understanding-sinusoidal-positional-encoding-in-transformers-26c4c161b7cc

### 16. Inside Sinusoidal Position Embeddings: A Sense of Order
- **Source**: LearnOpenCV
- **Key Findings**: Educational deep dive into the properties of sinusoidal embeddings and their geometric interpretation.
- **URL**: https://learnopencv.com/sinusoidal-position-embeddings/

### 17. A Gentle Introduction to Positional Encoding in Transformer Models, Part 1
- **Source**: MachineLearningMastery
- **Key Findings**: Introductory guide comparing absolute positional encodings, their limitations, and alternative approaches.
- **URL**: https://machinelearningmastery.com/a-gentle-introduction-to-positional-encoding-in-transformer-models-part-1/

### 18. Master Positional Encoding: Part II
- **Source**: Towards Data Science
- **Key Findings**: Advanced topics in positional encoding including hybrid approaches and recent innovations.
- **URL**: https://towardsdatascience.com/master-positional-encoding-part-ii-1cfc4d3e7375/

### 19. Positional Encoding Explained: A Deep Dive
- **Author**: Nikhil Chowdary Paleti
- **Source**: Medium (The Deep Hub)
- **Key Findings**: Comprehensive analysis of multiple positional encoding schemes and their trade-offs.
- **URL**: https://medium.com/thedeephub/positional-encoding-explained-a-deep-dive-into-transformer-pe-65cfe8cfe10b

### 20. Transformer Architecture: The Positional Encoding
- **Author**: Amirhossein Kazemnejad
- **Source**: Technical blog
- **Key Findings**: Clear mathematical derivation of sinusoidal positional encodings and their properties for relative position learning.
- **URL**: https://kazemnejad.com/blog/transformer_architecture_positional_encoding/

### 21. What is Positional Encoding?
- **Source**: IBM Think
- **Key Findings**: Industry perspective on positional encoding challenges and solutions in modern transformers.
- **URL**: https://www.ibm.com/think/topics/positional-encoding

### 22. Positional Encodings in Transformer Models
- **Source**: MachineLearningMastery
- **Key Findings**: Practical guide to implementing and choosing between different positional encoding schemes.
- **URL**: https://machinelearningmastery.com/positional-encodings-in-transformer-models/

## Other Approaches

### 23. Rethinking Positional Encoding in Language Models
- **Authors**: et al.
- **Year**: 2021
- **Venue**: ICLR
- **Key Findings**: Analysis of limitations in standard positional encodings and proposed improvements for better generalization.
- **URL**: https://openreview.net/pdf?id=09-528y2Fgf

---

## Summary Statistics

- **Total Sources Found**: 23
- **Academic Papers**: 7
- **Blog Posts/Educational**: 16
- **Core Framework Papers**: 2 (Vaswani et al., Shaw et al.)
- **Major Extensions**: 2 (Transformer-XL, RoPE)

## Evolution Timeline

1. **2017**: Sinusoidal positional encodings (Vaswani et al.)
2. **2018**: Relative position representations (Shaw et al.)
3. **2019**: Transformer-XL segment recurrence and relative PE
4. **2021**: RoPE - Rotary Position Embeddings (Su et al.)
5. **2022+**: Various extensions and refinements

## Key Insights

1. **Sinusoidal PE**: Deterministic, extrapolates to longer sequences, no learned parameters
2. **Learned PE**: Better in-distribution performance with sufficient training data
3. **Relative PE**: Superior generalization to unseen sequence lengths
4. **RoPE**: Combines benefits of rotation matrices with relative position encoding
5. **Transformer-XL**: Enables handling of longer sequences through segment recurrence
