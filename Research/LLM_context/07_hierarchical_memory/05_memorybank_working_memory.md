# MemoryBank, Working Memory Analogues, & Episodic-Semantic Distinction

## Multi-component Memory Mechanisms for LLMs

---

## 1. MemoryBank: Ebbinghaus-Inspired Long-Term Memory

### Reference
- **Title**: MemoryBank: Enhancing Large Language Models with Long-Term Memory
- **Authors**: Yu Zhong, Chundi Liu, Guo Guo, Yinan Yuan, Min Wei
- **Year**: 2024 (Published February 2024)
- **Venue**: AAAI 2024 (Thirty-Eighth AAAI Conference on AI)
- **DOI**: [10.1609/aaai.v38i17.29946](https://ojs.aaai.org/index.php/AAAI/article/view/29946)
- **ArXiv**: [2305.10250](https://arxiv.org/abs/2305.10250)
- **Application**: SiliconFriend (LLM-based AI companion)

### Motivation

LLMs suffer from **critical memory limitations** in multi-turn dialogues:
- Context window is fixed (even with 200K tokens, limits accumulate)
- Early information in conversation forgotten (primacy loss)
- User personalities and preferences quickly lost
- Unable to build genuine long-term relationships

**MemoryBank** addresses this by implementing human-inspired episodic memory with forgetting/reinforcement mechanisms.

---

## 2. Architecture: Three Modules

### 2.1 Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     CURRENT DIALOGUE                        │
│                   (User message + context)                  │
└────────────────────┬────────────────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│         MEMORY BANK SYSTEM (Three Modules)                  │
├──────────────┬──────────────┬──────────────────────────────┤
│              │              │                              │
│   RETRIEVER  │    WRITER    │         READER               │
│              │              │                              │
│ (Query bank) │ (Store/update)│ (Integrate into context)   │
│              │              │                              │
└──────────────┴──────────────┴──────────────────────────────┘
                     ↓
┌─────────────────────────────────────────────────────────────┐
│        MEMORY BANK (Episodic Memory Storage)                │
│  - User preferences, personality traits, facts             │
│  - Timestamps, importance scores, access frequency         │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 Module Details

#### **Writer Module**
- **Function**: Extract and store important information from dialogue
- **Input**: Current user message, system response
- **Operation**:
  1. Identify extractable facts/preferences
  2. Score importance of new information
  3. Update existing memory records or create new ones
  4. Apply forgetting curve decay to reduce importance of old memories
- **Output**: Updated memory bank state

**Example**:
```
User: "I'm feeling really stressed about my job.
       I work in finance but want to switch to design."

Writer extracts:
  - Memory 1: "User's profession: Finance"
  - Memory 2: "User wants to switch to design"
  - Memory 3: "User is stressed"

Applied to memory bank with importance score 8/10
```

#### **Retriever Module**
- **Function**: Find relevant memories for current dialogue
- **Input**: Current user message (query)
- **Operation**:
  1. Compute similarity between query and stored memories
  2. Retrieve top-k most relevant memories
  3. Score by relevance + recency + importance
- **Output**: Relevant memory context

**Example**:
```
User: "What did I mention last week about my career?"

Retriever searches memory bank for:
  - Memories related to "career" OR "job" OR "design"
  - Filters for memories created in past week
  - Ranks by relevance

Returns: ["User wants to switch to design", "User is stressed"]
```

#### **Reader Module**
- **Function**: Integrate retrieved memories into LLM input
- **Input**: Retrieved memories, current dialogue
- **Operation**:
  1. Summarize retrieved memories if too many
  2. Format as natural language context
  3. Append to system prompt or dialog history
  4. Present to LLM alongside current message
- **Output**: Augmented prompt with memory context

**Example**:
```
Enhanced Input to LLM:

[System Background about User]
- You are talking to a person who works in finance
- They want to switch careers to design
- They have been stressed lately
- Remember their preferences and situation

[Current User Message]
"How can I prepare for a career switch?"

[LLM generates response using background knowledge]
```

---

## 3. Memory Management: Ebbinghaus Forgetting Curve

### 3.1 Core Innovation: Implementing Human Memory Decay

**Key Insight**: Rather than infinite memory retention, implement **selective forgetting** with **reinforcement**.

### 3.2 Forgetting Curve Formula

Ebbinghaus's forgetting curve adapted for discrete memory items:

$$\text{Importance}(m, t) = I_0 \cdot e^{-\lambda t}$$

Where:
- $I_0$ = initial importance score (0-10)
- $t$ = time elapsed since last access (in update cycles)
- $\lambda$ = decay rate (controls forgetting speed)
- $\text{Importance}(m, t)$ = current importance after time $t$

### 3.3 Memory Update Mechanics

#### **Decay Without Access**
```
Memory created at t=0 with importance 8.0

Days passed:  1    3     7     14    30
Importance:  7.1  5.9   3.2   0.9   0.01

Result: Old memories naturally fade unless reinforced
```

#### **Reinforcement Through Access**
When a memory is **retrieved** (used in dialogue), its importance is **boosted**:

$$I_{\text{new}} = \min(10, I_{\text{current}} + 0.5)$$

**Effect**: Frequently relevant memories stay important; irrelevant memories naturally fade.

### 3.4 Adaptive Retention

**No explicit deletion**:
- Memories below importance threshold ignored during retrieval
- Still stored, but rarely surfaced
- Can be reactivated if relevant again

**Threshold-based filtering**:
```
Retrieved memories ranked by:
  score = importance * relevance_similarity * recency_boost

Return top-k above threshold
```

---

## 4. Working Memory in Transformers

### 4.1 Problem Statement

**Gap in literature**: While we have episodic memory solutions (MemoryBank), how do modern transformers implement **working memory**?

### Reference Research
- **TransformerFAM**: Feedback Attention is Working Memory (2024)
- **Self-Attention Limits Working Memory Capacity** (2024)
- **Memory-Augmented Transformers: A Systematic Review** (2024)

### 4.2 Transformer Components as Working Memory Analogues

| Human Cognitive Component | Transformer Analogue |
|--------------------------|----------------------|
| **Sensory Input** | Token embeddings (raw representation) |
| **Attention** | Self-attention (selection mechanism) |
| **Working Memory Capacity** | Effective context window (from attention cost) |
| **Maintenance** | Positional encoding + recurrent operations |
| **Information Binding** | Transformer layer interactions |

### 4.3 Self-Attention as Working Memory Selection

**Mechanism**:
```
1. All tokens available (like sensory buffer)
2. Query token attends to relevant positions
3. Top-k positions weighted (like attention selection)
4. Attended information forms temporary binding
5. Passed to next layer (maintenance)
```

**Working Memory Analogy**:
- **Capacity limit**: Attention head can only focus on ~4-6 items meaningfully
- **Seriality**: Processes one position at a time (Query = central executive focus)
- **Decay**: Information older in sequence less attended (primacy/recency)

### 4.4 TransformerFAM: Feedback Attention is Working Memory

**Innovation**: Add **feedback attention loops** within transformer layers to maintain internal working memory state.

**Architecture**:
```
Layer t:
  ├─ Forward attention (standard self-attention)
  ├─ Feedback from Layer t+1 (working memory refresh)
  └─ Recurrent state update (episodic binding)

Effect: Maintains longer-term associations across positions
        without explicit external memory
```

**Key Insight**: Feedback loops allow indefinite context without external cache, improving efficiency.

### 4.5 Working Memory Capacity Limits

**Empirical Finding**: Self-attention mechanism imposes working memory-like capacity limits.

**Research Result**:
- GPT-3/GPT-4 can hold ~4-7 distinct items in "active" consideration
- Attention scores gradually concentrate on few positions
- Effective working memory capacity ~7±2 (consistent with human psychology!)

**Implication**: Even with large context windows, effective working memory is limited. Need explicit memory management.

---

## 5. Episodic vs. Semantic Memory in LLMs

### 5.1 Cognitive Science Definitions

#### **Episodic Memory**
- **Content**: Specific events linked to time and place
- **Example**: "I had coffee with Alice on Tuesday at 2 PM"
- **Retrieval**: Context-dependent (cued by reminder)
- **Feeling**: Recollection (sense of re-experiencing)

#### **Semantic Memory**
- **Content**: Facts, concepts, general knowledge
- **Example**: "Paris is the capital of France"
- **Retrieval**: Automatic, context-independent
- **Feeling**: Knowing (abstract understanding)

### 5.2 Current LLM Capabilities

#### **Parametric (Implicit) Semantic Memory**
- **What**: Knowledge encoded in model weights
- **Strength**: Vast, always accessible, learned at scale
- **Weakness**: Frozen post-training, hard to update, prone to hallucination
- **Mechanism**: Distributed across layers via attention patterns

#### **Episodic Memory Gap**
- **Challenge**: LLMs historically lack true episodic memory
- **Why**: No explicit mechanism to store time-stamped events
- **Recent work**: External memory banks (MemoryBank, Generative Agents) fill this gap

### 5.3 Research on Episodic Memory in LLMs

#### Reference: "Towards Large Language Models with Human-like Episodic Memory" (2025)

**Key Findings**:

1. **Current Lack**: State-of-the-art models (GPT-4, Claude, Llama 3.1, o1-mini) struggle with episodic memory tasks
   - Multiple related events: difficulty tracking causal chains
   - Complex spatiotemporal relationships: confusion about timing
   - Person-specific memories: mixing up who said what

2. **Needed Architecture**:
   - Explicit episodic buffer (Baddeley's term)
   - Time-aware encoding (timestamps matter)
   - Context-dependent retrieval (cue-based)
   - Integration with semantic knowledge (blended memory)

3. **Proposed Solutions**:
   - External memory aligned with human episodic memory
   - Latent, unbounded storage capacity
   - Episodic memories fed to LLM alongside semantic knowledge
   - Context-aware retrieval based on current situation

### 5.4 Integration of Episodic + Semantic Memory

**Ideal Architecture**:
```
User Query: "What did Alice tell me about her job?"

1. RETRIEVAL PHASE
   Episodic Memory:
     - "Alice mentioned her job yesterday"
     - "She said she wants to switch industries"
   Semantic Memory:
     - "Alice works in finance (general fact)"
     - "Career switching is difficult (general knowledge)"

2. INTEGRATION PHASE
   Blended context sent to LLM:
   "Based on episodic memories: [Yesterday Alice said...]
    General knowledge: [Career switching typically...]
    Respond as the AI companion would..."

3. RESPONSE GENERATION
   LLM generates response using:
   - Specific episodic details (personalized)
   - General semantic knowledge (informed)
   - Relationship context (coherent)
```

---

## 6. Comparison: Different Memory Architectures

### Single vs. Multi-Component

| Aspect | Single System | Multi-Component (Episodic + Semantic) |
|--------|----------------|-------------------------------------|
| **Storage** | One mechanism | Separate systems |
| **Retrieval** | Single strategy | Context-dependent selection |
| **Decay** | Uniform | Episodic: fast; Semantic: slow |
| **Integration** | None | Explicit blending |
| **Scalability** | Capacity issue | Separated, easier scaling |
| **Interpretability** | Black box | Clear distinction |

### Parametric vs. Non-Parametric

| Aspect | Parametric (Model Weights) | Non-Parametric (External Storage) |
|--------|---------------------------|----------------------------------|
| **Update Speed** | Slow (requires retraining) | Fast (direct insertion) |
| **Capacity** | Fixed at training time | Unbounded |
| **Accuracy** | General knowledge | Specific facts |
| **Hallucination** | Possible | Retrievable truth |
| **Interpretability** | Opaque | Explicit memories |

---

## 7. Practical Implementation: SiliconFriend

### Use Case: AI Companion

**Goal**: Build an LLM-based chatbot that:
- Remembers conversations over weeks/months
- Adapts to user personality
- Maintains consistent preferences
- Provides empathetic support

### Deployment

**MemoryBank integration**:
1. **Writer**: Extracts user info after each message
   - Emotional state, preferences, goals, concerns
2. **Retriever**: Finds relevant memories before each response
   - "What does the user care about?"
   - "What have they told me before?"
3. **Reader**: Includes memories in prompt
   - "You know the user wants to switch careers..."

**Results**:
- Users report more personalized, empathetic responses
- Companion maintains conversation coherence across sessions
- Psychological dialogue data improves empathy scoring

**Cost**: ~5-15% overhead for memory operations (Writer + Retriever + Reader calls)

---

## 8. Scalability Considerations

### Memory Growth

**Problem**: After 100 conversations, thousands of memories accumulate.

**Solutions**:
1. **Importance thresholding**: Ignore low-importance memories in retrieval
2. **Summarization**: Periodically compress old memories ("Last month: user was stressed about job")
3. **Forgetting curves**: Implement stricter decay for less important items
4. **Hierarchical indexing**: Cluster memories by topic for faster retrieval

### Computational Cost

**Per message cost**:
- Retriever: O(n) similarity search (n = memory count)
  - Mitigation: Top-k early filtering
- Writer: O(1) insertion (append to memory list)
- Reader: O(k) LLM forward pass (k = context length)

**Scaling up**:
- 100 users × 100 memories × daily interactions
- ~10K memory operations/day manageable
- But real-time personalization across millions users challenging

---

## 9. Connections to Classical Memory Theory

### Ebbinghaus Curve Revival

MemoryBank **operationalizes** Ebbinghaus's ~140-year-old findings:
- Forgetting is exponential, not linear
- Reinforcement resets decay curve
- Optimal review intervals increase over time

### Baddeley's Multi-Component Model

Integration of:
- **Working memory** (in-context recent information)
- **Episodic buffer** (integrated current state)
- **Long-term memory** (MemoryBank storage)

### McClelland's Complementary Learning

- **Fast system**: Recent memories in context window (episodic)
- **Slow system**: Parameter updates (semantic knowledge)
- **Consolidation**: Periodic summarization of memories

---

## 10. Open Research Questions

1. **Optimal forgetting rate**: How quickly should memories decay?
   - Different for different user types?
   - Task-dependent?

2. **Memory consolidation**: When/how to summarize episodic → semantic?
   - Sleep-inspired consolidation phases?
   - User-initiated reflection?

3. **Episodic storage quality**: What information matters?
   - Full event descriptions vs. abstractive summaries?
   - Emotional tagging importance?

4. **Retrieval efficiency**: How to scale retrieval as memories grow?
   - Learned retrieval policies?
   - Hierarchical memory structures?

5. **Memory privacy**: What to store in user-facing memory banks?
   - Sensitive information handling?
   - User control over memories?

---

## 11. Key References & Further Reading

1. Zhong, Y., Liu, C., Guo, G., Yuan, Y., & Wei, M. (2024). MemoryBank: Enhancing Large Language Models with Long-Term Memory. In Proceedings of AAAI 2024.

2. Hwang, D., (2024). TransformerFAM: Feedback Attention is Working Memory. arXiv:2404.09173.

3. Cowan, N. (2024). Self-Attention Limits Working Memory Capacity of Transformer-Based Models. arXiv:2409.10715.

4. Ebbinghaus, H. (1885/1913). Memory: A Contribution to Experimental Psychology. Dover Publications.

5. Tulving, E. (2002). Episodic Memory: From Mind to Brain. Annual Review of Psychology, 53, 1-25.

---

## 12. Section Integration

This collection of papers shows:
- **MemoryBank**: Practical episodic memory for LLMs with human-inspired forgetting
- **Transformer WM**: How attention implements working memory-like capacity limits
- **Episodic-Semantic Distinction**: Why both systems needed, not just parametric knowledge

Together, they support the argument that **multi-component memory** (episodic + semantic + working) is essential for believable, capable LLM agents.

Next sections explore more sophisticated hierarchical architectures (SCM, HMT) and consolidation mechanisms (sleep, reflection).
