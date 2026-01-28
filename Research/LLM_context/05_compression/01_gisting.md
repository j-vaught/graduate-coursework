# Gisting Approaches to Context Compression

## Gisting: Learning to Compress Prompts with Gist Tokens

**Authors:** Mu et al.

**Year:** 2023

**Venue:** Advances in Neural Information Processing Systems (NeurIPS)

**Key Concept:**
Gisting is a simple approach to context compression that uses "gist tokens," which forces the model to condense input information into dedicated token activations by introducing a representational bottleneck in the attention mask. This generates a context-specific "tuning prefix" in a single forward pass.

**Key Features:**
- Implementation requires only new vocabulary token embeddings and an attention mask modification
- Easily integrable with existing frameworks and systems
- Context-specific tuning prefix generated in single forward pass
- Requires minimal modifications to existing models

**Advantages:**
- Simple approach requiring only attention mask modification
- Straightforward integration with existing systems
- Minimal overhead in terms of parameters

**Limitations:**
- Performance degrades rapidly when compressing longer contexts
- Does not effectively scale even to contexts of 100s of tokens
- Limited to compressing short prompts (task instructions before input texts)
- Does not address the real issue of long contexts in modern LLMs

**Performance Characteristics:**
- Effective for short-form context compression
- Rapid degradation for longer sequences
- Not suitable for contemporary long context requirements

**Applications:**
- Task instruction compression
- Short prompt optimization
- Model fine-tuning with compressed prompts

## References
- [Long Context In-Context Compression by Getting to the Gist of Gisting](https://arxiv.org/html/2504.08934v1)
- [Learning to Compress Prompts with Gist Tokens - NeurIPS 2023](https://arxiv.org/abs/2504.08934)
