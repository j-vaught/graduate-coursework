# Conversation Summarization Approaches

## Overview
Conversation summarization compresses dialogue history while preserving semantic content. It enables long-term memory by periodically summarizing older exchanges and keeping recent messages verbatim.

## Papers and Resources

### Primary Research Papers

1. **Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models**
   - Authors: [Title from search results]
   - Venue: ICLR 2025 (Published as conference paper)
   - Year: 2024
   - ID: 2308.15022
   - Key Findings:
     - Recursive summarization generates memories by processing small dialogue contexts
     - Multi-level approach: first memorize small context, then recursively produce new memory using prior memory + new context
     - Enables at least 5x more information in chat context through compression
     - Published in ICLR 2025
   - URL: https://arxiv.org/abs/2308.15022
   - Full Text: https://arxiv.org/html/2308.15022v3

2. **Beyond Static Summarization: Proactive Memory Extraction for LLM Agents**
   - Venue: arXiv (2026)
   - Year: 2026
   - ID: 2601.04463
   - Key Findings: Goes beyond static summarization by proactively extracting memories relevant to future agent tasks
   - URL: https://arxiv.org/html/2601.04463

### Implementation and Systems

3. **LLM Chat History Summarization Guide October 2025**
   - Author: Mem0.ai
   - Platform: Mem0 Blog
   - Year: 2025
   - Key Findings:
     - Contextual summarization: compress conversations older than 20 messages while keeping last 10 verbatim
     - Basic message windowing: send only last N messages (works short-term, breaks down with lost context)
     - Rolling summarization: after 5-10 turns, LLM creates summary replacing original messages
     - Vectorized memory: store interactions as embeddings, retrieve semantically similar snippets
     - Multi-level memory hierarchies: immediate working memory (current session), episodic (past interactions), semantic (general knowledge)
   - URL: https://mem0.ai/blog/llm-chat-history-summarization-guide-2025

4. **Extending Chat History through Dynamic Summarization Workflow**
   - Platform: ComfyUI LLM Party (GitHub Discussion)
   - Year: 2024
   - Key Findings: Dynamic summarization triggered when context window fills; maintains conversation flow
   - URL: https://github.com/heshengtao/comfyui_LLM_party/discussions/93

5. **Don't Let Your AI Agent Forget: Smarter Strategies for Summarizing Message History**
   - Author: Ali Ibrahim
   - Platform: Medium
   - Year: 2025
   - Key Findings:
     - Summarization is imperfect process where nuances and subtle shifts in intent lost over time
     - Different strategies for different conversation types
     - Cost implications increase with summary size
     - Trade-off between compression and detail preservation
   - URL: https://techwithibrahim.medium.com/dont-let-your-ai-agent-forget-smarter-strategies-for-summarizing-message-history-a2d5284539f1

6. **"Infinite" chat with history summarization**
   - Author: Microsoft (Surface Duo Blog)
   - Platform: Surface Duo Blog
   - Year: 2024
   - Key Findings: Practical implementation of infinite chat with periodic summarization
   - URL: https://devblogs.microsoft.com/surface-duo/android-openai-chatgpt-18/

### Advanced Architectures

7. **H-MEM: Hierarchical Memory for High-Efficiency**
   - Venue: arXiv
   - Year: 2024
   - ID: 2507.22925
   - Key Findings:
     - Four-layer memory structure: Domain, Category, Memory Trace, Episode layers
     - Layer-by-layer summarization with position indices
     - Structured retrieval from hierarchical organization
     - High efficiency through hierarchical compression
   - URL: https://www.arxiv.org/pdf/2507.22925

8. **SGMEM: SENTENCE GRAPH MEMORY FOR LONG-TERM CONVERSATIONAL AGENTS**
   - Venue: arXiv
   - Year: 2024
   - ID: 2509.21212
   - Key Findings:
     - Sentence-level organization with explicit semantic associations
     - Graph structure models relationships between conversation elements
     - Addresses memory fragmentation in long-term agents
     - Enables semantic retrieval and context reconstruction
   - URL: https://arxiv.org/pdf/2509.21212

## Key Strategies

### Message Windowing
- Simplest approach: keep last N messages in full
- Works well for short conversations
- Performance degrades as important context from earlier messages lost
- Low computational cost but limited context retention

### Rolling Summarization
- After N turns, LLM creates concise summary
- Summary replaces original messages in history
- Next summary incorporates prior summary + new context
- Prevents exponential growth of compression artifacts

### Vectorized Memory (Embedding-based)
- Store interactions as vector embeddings
- Retrieve semantically similar past conversations
- Inject only relevant snippets when needed
- More sophisticated but requires vector database

### Multi-Level Memory Hierarchies
- **Immediate Memory**: Current session, kept verbatim
- **Episodic Memory**: Important past interactions, summarized or linked
- **Semantic Memory**: General knowledge extracted over time
- Different compression rates per level based on age and relevance

### Recursive Summarization
- Small context memorization first
- Recursively produce new memory from: previous memory + new context
- Enables multi-turn summarization without cascading loss
- Suitable for extended dialogue sessions

### Hierarchical Summarization
- Layer-by-layer compression (Domain → Category → Trace → Episode)
- Position-indexed structure for retrieval
- Four-level compression with efficiency gains
- Graph-based semantic organization optional

## Performance Characteristics

### Compression Ratios
- Basic summarization: 2-5x compression
- Rolling summarization: 3-7x while maintaining coherence
- Hierarchical approaches: up to 10x with structured retrieval
- Recursive methods: 5x+ compression verified in ICLR 2025

### Information Loss
- Nuances and subtle context shifts lost during compression
- Specific details, names, and edge cases prone to omission
- Intent evolution across conversation may be flattened
- Quantified loss varies by summarization method

### Computational Cost
- One-time cost per summarization event
- Smaller cost for subsequent queries vs repeated summarization
- Rolling approach: O(window_size) per turn
- Recursive approach: O(log n) hierarchy depth with O(n) total content

## Practical Considerations

1. **Trigger Conditions**:
   - Token count thresholds (e.g., summarize when reaching 70% capacity)
   - Time-based triggers (e.g., every N turns)
   - Importance-based triggers (e.g., when certain turn counts reached)
   - Hybrid triggers combining multiple signals

2. **Summary Quality**:
   - Use specialized summarization models for consistency
   - Preserve key entities, decisions, and commitments
   - Maintain temporal ordering through summaries
   - Include confidence scores for summary completeness

3. **Integration Patterns**:
   - Mix full messages (recent) with summaries (older)
   - Use summaries as context for next-turn generation
   - Maintain summary history for multi-level retrieval
   - Track summary chain for reproducibility

4. **Monitoring and Evaluation**:
   - Measure information retention post-summarization
   - Track user satisfaction with continuity
   - Monitor for hallucinations introduced by compression
   - Validate semantic preservation through embeddings

## Open Research Questions

- Optimal summarization frequency for different dialogue types?
- How to preserve subtle contextual shifts in summaries?
- Best combination of hierarchical levels for long conversations?
- Can summarization quality be assessed without manual review?
