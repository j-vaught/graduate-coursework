# Human vs. LLM Memory & Cognitive-Science-Inspired Architectures

## Comparative Analysis and Integrated Cognitive Designs

---

## 1. Comparative Memory Analysis: Human vs. LLM

### Reference Papers
- **"Judgments of Learning Distinguish Humans from Large Language Models in Predicting Memory"** (Nature Scientific Reports, 2025)
- **"Large Language Models and Cognitive Science: A Comprehensive Review of Similarities, Differences, and Challenges"** (2024)
- **"From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs"** (2024)
- **"Analyzing Memory Effects in Large Language Models through the Lens of Cognitive Psychology"** (2024)

---

## 2. Structural Similarities

### Multi-Component Architecture

Both humans and LLMs exhibit **multi-component memory systems**:

| Memory Type | Humans | LLMs |
|-------------|--------|------|
| **Working Memory** | ~3-7 items capacity | Attention window (context-dependent) |
| **Short-term Storage** | ~20-30 seconds duration | In-context, implicit (fed to forward pass) |
| **Long-term Storage** | Unlimited (lifetime) | Model parameters (~fixed at inference) |
| **Encoding** | Multimodal (visual, auditory, semantic) | Distributed embeddings (abstract) |
| **Retrieval** | Associative (cue-dependent) | Attention-based (similarity-weighted) |

### Primacy and Recency Effects

**Both humans and LLMs demonstrate**:
- **Primacy effect**: Items early in sequence remembered better
- **Recency effect**: Most recent items recalled better
- **Serial position curve**: U-shaped retention pattern

**Human mechanism**: Separate encoding processes (rehearsal for primacy, active maintenance for recency)

**LLM mechanism**: Attention allocation (position embeddings, token positioning in context)

### False Memories

**Both exhibit "false memories"**:
- Humans: Misremember related words that weren't shown (Deese-Roediger-McDermott paradigm)
- LLMs: Generate hallucinated information semantically related to context (semantic contamination)

---

## 3. Critical Differences

### 3.1 Selectivity and Emotional Significance

#### **Human Memory** (Highly Selective)
- Emotionally salient events remembered better
- Danger, surprise, novel stimuli preferentially encoded
- Evolutionary advantage: Survival-critical information prioritized
- Mechanism: Amygdala tags emotion, boosting hippocampal encoding

**Example**:
```
Human at party:
  Remembers: Dramatic breakup conversation (high emotion)
  Forgets: Background music, neutral conversations

Emotional tagging makes some memories stick despite irrelevance
```

#### **LLM Memory** (Non-Selective)
- All tokens treated with equal computational resources (in principle)
- No inherent emotional weighting
- Learns patterns from training data frequency, not salience
- No biological equivalent of amygdala-hippocampus interaction

**Consequence**: LLMs may over-remember trivial details, under-remember functionally important information.

### 3.2 Adaptive Forgetting Mechanisms

#### **Human Forgetting** (Adaptive)
- Serves multiple functions:
  1. **Cognitive economy**: Prevents overload
  2. **Interference reduction**: Old knowledge doesn't interfere with new
  3. **Contextual relevance**: Old, irrelevant information discarded
  4. **Abstraction**: Specific episodes consolidated into generalizable knowledge

- Forgetting rate **sensitive to importance**:
  - Critical information: Slow forgetting (via spaced retrieval)
  - Irrelevant details: Fast forgetting (Ebbinghaus curve)

**Example**:
```
Human after job training (first week):
  Day 1: Remembers 100% of procedures
  Day 7: Remembers ~25%
  Day 30: Remembers ~15%

But: Critical safety procedures retained
     Irrelevant background trivia forgotten
```

#### **LLM Forgetting** (Non-Adaptive)
- No explicit forgetting mechanism during inference
- "Forgetting" occurs via:
  1. **Context window limitation**: Information pushed out as new tokens arrive
  2. **Retrieval failure**: Information present in parameters but not activated
  3. **Interference**: New learned knowledge can overwrite old (catastrophic forgetting)

- No built-in mechanism to prioritize based on importance

### 3.3 Conceptual Organization and Consistency

#### **Human Concepts** (Stable, Coherent)
- Conceptual structure relatively fixed across contexts
- Word "dog" activates consistent features (animal, loyal, furry)
- Conceptual relations stable across cultures and languages
- Example: "Robin" → prototypically BIRD (features: wings, fly, nest)

#### **LLM Concepts** (Context-Dependent, Variable)
- Conceptual structure varies based on task/prompt
- Word embeddings change based on surrounding tokens
- Concept drift across different prompting strategies
- Example: Same word generates different activations in different sentences

**Implication**: Humans have **conceptual stability**; LLMs have **contextual plasticity** (adaptability but less coherence).

### 3.4 Metacognition and Confidence Judgment

#### **Human Metacognition** (Calibrated)
- Judgments of Learning (JoL): Predict whether something was learned
- Confidence judgments correlate with actual recall accuracy
- Can monitor own learning in real-time
- Useful for study strategy: Know when to review vs. move forward

#### **LLM Metacognition** (Uncalibrated)
**Empirical finding (Nature Scientific Reports 2025)**:

| Model | JoL-Recall Correlation |
|-------|------------------------|
| Humans | r = 0.68 (strong) |
| GPT-3.5 | r = 0.12 (none) |
| GPT-4 | r = 0.15 (none) |
| Claude 3 | r = 0.18 (none) |

**Implication**: LLMs **cannot** assess their own memory reliability. Confident wrong answers vs. uncertain but correct answers indistinguishable by model.

---

## 4. Memory Effect Parallels and Divergences

### 4.1 Effects Both Show

#### **Primacy & Recency**
Both humans and LLMs remember:
- First items in sequence (primacy)
- Last items in sequence (recency)
- Middle items forgotten (serial position U-shape)

#### **False Memory/Hallucination**
Both generate false information:
- Humans: Remember related words that weren't shown
- LLMs: Generate plausible but untrue facts

### 4.2 Effects Only Humans Show

#### **Spacing Effect** (Not Inherent to LLMs)
- Humans: Spaced practice beats massed practice
- LLMs: No inherent preference (depends on training algorithm)
- But can be trained to mimic via prompt manipulation

#### **Testing Effect**
- Humans: Retrieval practice (testing) superior to passive study
- LLMs: No clear analogous effect (tokens equally weighted in context)

#### **Encoding Specificity**
- Humans: Memory retrieval benefits from encoding-retrieval match
- LLMs: Less clear encoding-specificity; embeddings more abstract

### 4.3 Effects Only LLMs Show

#### **Prompt Sensitivity**
- How question phrased dramatically affects retrieval (humans more robust)
- "What is 2+2?" vs. "Compute 2+2:" different responses possible
- No human equivalent of prompt-response sensitivity

#### **Context Window Truncation**
- Artificial capacity limit from context window size
- Humans don't have discrete context window
- Long-term memory accessible via cues, not token count

---

## 5. Cognitive-Science-Inspired LLM Architectures

### 5.1 Cognitive Workspace Hypothesis

#### Reference
- **Title**: Cognitive Workspace: Active Memory Management for LLMs
- **Year**: 2024
- **Theoretical Foundation**: Global Workspace Theory (Baars, 1988)

#### Theory

**Global Workspace Theory** (neuroscience):
- Limited-capacity workspace for conscious access
- Cognitive processes compete for workspace access
- Winning processes broadcast to other cognitive modules
- Explains attention, executive function, consciousness metaphorically

#### Implementation in LLMs

```
Cognitive Workspace for LLMs:

┌────────────────────────────────────────────┐
│         WORKSPACE (Limited Capacity)       │
│  - Current task goal                       │
│  - Recent observations                     │
│  - Retrieved relevant knowledge            │
│  - Active reasoning trace                  │
│  (Capacity: ~1K-4K tokens)                 │
└────────────────────────────────────────────┘
         ↓ (broadcast)
┌────────────────────────────────────────────┐
│   COGNITIVE MODULES (Parallel Processing)  │
│  - Reading module (comprehension)          │
│  - Planning module (goal generation)       │
│  - Memory module (storage/retrieval)       │
│  - Execution module (action)               │
└────────────────────────────────────────────┘
```

#### Key Operations

1. **Workspace Population**
   - Determine what information is task-relevant
   - Select from memory what to bring into workspace
   - Based on current goal and observations

2. **Conscious Processing** (Metaphorical)
   - All modules see workspace contents
   - Implicit coordination without explicit communication

3. **Workspace Update**
   - As attention shifts, workspace cleared and refilled
   - Prevents overload, enforces bottleneck

#### Advantage

Mimics human attention limitations in a principled way:
- Humans can't multi-task perfectly (workspace competition)
- LLMs similarly bottlenecked by workspace capacity
- Theory-driven rather than ad-hoc

### 5.2 Cognitive LLMs: Integrating Cognitive Architectures

#### References
- **"Cognitive LLMs: Toward Human-Like Artificial Intelligence by Integrating Cognitive Architectures and Large Language Models for Manufacturing Decision-Making"** (2025)
- **Hybrid approach**: Cognitive architecture (ACT-R-like) + LLM

#### Integration Strategy

```
Classical Cognitive Architecture:
  ├─ Symbolic production rules (if-then)
  ├─ Working memory buffers
  ├─ Declarative knowledge base
  └─ Procedural learning mechanisms

Combined with LLM:
  ├─ LLM as encoder/decoder for natural language
  ├─ LLM for flexible reasoning
  ├─ Symbolic layer for structured knowledge
  └─ Hybrid execution: symbolic rules + LLM inference
```

#### Mechanism

1. **Extract decision-making process** from cognitive architecture
2. **Encode as latent representations** (embeddings)
3. **Inject into LLM adapter layers** (via LoRA)
4. **Fine-tune** for downstream tasks

#### Benefits

- **Interpretability**: Symbolic rules explicit
- **Knowledge transfer**: Cognitive model structure → LLM inductive bias
- **Reliability**: Constrain LLM outputs via symbolic rules
- **Explainability**: Reason through cognitive model decisions

### 5.3 Multiple Memory Systems for Agents

#### Reference
- **"Multiple Memory Systems for Enhancing the Long-term Memory of Agent"** (2024)

#### Architecture

Inspired by **multiple memory systems in cognitive psychology**:

```
COGNITIVE PSYCHOLOGY INSPIRATION:
  Declarative Memory
    ├─ Episodic (events)
    └─ Semantic (facts)
  Procedural Memory (skills)
  Implicit Memory (habits)

AGENT IMPLEMENTATION:
  Episodic Memory
    ├─ Events with timestamps, locations
    ├─ Natural language descriptions
    └─ Retrieval: similarity + temporal context

  Semantic Memory
    ├─ Structured facts (knowledge graphs)
    ├─ Concepts and relations
    └─ Retrieval: conceptual similarity

  Procedural Memory
    ├─ Learned skills and strategies
    ├─ Action sequences
    └─ Retrieval: automatic execution

  Implicit Memory
    ├─ Habits, preferences (soft constraints)
    ├─ Learned associations
    └─ Unconscious influence on behavior
```

#### Principles

1. **Encoding Specificity**: Information encoded and retrieved via same modality
   - Episodic: Retrieved via context/event cues
   - Semantic: Retrieved via conceptual cues
   - Procedural: Retrieved via task/action cues

2. **Levels of Processing**: Deeper processing (semantic) stronger retention
   - Shallow: Surface features (words) → weak memory
   - Deep: Meaning integration → strong memory

3. **Transfer-Appropriate Processing**: Retrieval benefit when test matches encoding
   - Test similar to encoding context → better performance

#### Benefits

- **Flexibility**: Different memory types for different needs
- **Efficiency**: Specialized retrieval for each type
- **Naturalness**: Aligns with human cognitive structure
- **Scalability**: Modularity enables independent scaling

---

## 6. Comparative Table: Human vs. LLM Memory Features

| Feature | Human | LLM | Gap |
|---------|-------|-----|-----|
| **Selectivity** | High (emotion-based) | Low (uniform) | LLMs need affective tagging |
| **Forgetting** | Adaptive (importance-weighted) | Non-adaptive (context-limited) | LLMs need importance scoring |
| **Conceptual Stability** | High (robust across tasks) | Low (context-variable) | LLMs drift more |
| **Metacognition** | Strong (calibrated confidence) | Weak (overconfident/underconfident) | LLMs need confidence calibration |
| **Episodic Memory** | Rich (detailed, time-bound) | Absent (parametric only) | LLMs need explicit episodic buffers |
| **Semantic Memory** | Rich (conceptual networks) | Rich (distributed) | LLMs have different organization |
| **Procedural Memory** | Clear (skills vs. knowledge) | Unclear (learned in parameters) | LLMs need explicit skill learning |
| **Implicit Memory** | Present (habits, priming) | Present (hidden in embeddings) | LLMs need to surface implicitness |
| **Working Memory Capacity** | ~7±2 items | ~4-7 positions (empirically) | Surprisingly similar! |
| **Context Integration** | Multimodal | Unimodal (text) | LLMs need multimodal memory |

---

## 7. Implications for LLM Design

### Based on Human-LLM Differences

1. **Emotional/Importance Tagging**
   - Humans use amygdala-hippocampal interaction to tag important memories
   - LLMs could implement explicit importance scoring (MemoryBank, Generative Agents)

2. **Adaptive Forgetting**
   - Implement Ebbinghaus curve with reinforcement (as in MemoryBank)
   - Prioritize important information in retrievals

3. **Stability Mechanisms**
   - Constrain embeddings to reduce context-dependence
   - Implement consistency checks across prompts
   - Use regularization to stabilize conceptual structure

4. **Metacognitive Calibration**
   - Teach LLMs to assess confidence accurately
   - Output uncertainty estimates alongside predictions
   - Train on calibration objectives

5. **Episodic Memory Structures**
   - Implement explicit episodic buffers (Baddeley's concept)
   - Time-stamp all memories
   - Maintain spatiotemporal context
   - Enable cue-based retrieval (not just semantic similarity)

---

## 8. Recent Cognitive Architectures for LLMs

### 8.1 CAIM: Cognitive AI Memory Framework

#### Innovation
- Integrates multiple memory systems from cognitive science
- Designed for long-term human-AI interaction
- Focuses on personalization and preference learning

#### Architecture
```
EPISODIC MEMORY: Interaction history
  - All user messages and AI responses
  - Timestamps and context
  - User goals and intents

SEMANTIC MEMORY: Learned user model
  - Preferences (inferred from interactions)
  - Values and priorities
  - Knowledge about user's domain

PROCEDURAL MEMORY: Learned interaction patterns
  - Effective ways to help this user
  - Communication style preferences
  - Routine tasks and workflows

IMPLICIT MEMORY: Habits and associations
  - Unconscious preferences
  - Learned associations
  - Soft constraints on behavior
```

### 8.2 Memory-of-Thought (MoT)

#### Innovation
- LLM explicitly saves and retrieves "thoughts"
- Two-phase learning: Pre-thinking, then recalling

#### Process
```
Phase 1: PRE-THINKING
  When encountering question, LLM generates reasoning
  If confidence high: Save thought to memory
  Format: "Question: ... Answer: ... Reasoning: ..."

Phase 2: RECALLING
  On new question: Query memory for similar past "thoughts"
  Retrieve high-confidence solutions
  Use as guide for current reasoning

Result: LLM learns from its own good reasoning
        Similar to human reflection and consolidation
```

### 8.3 Dyna-Think: Planning with Internal World Model

#### Innovation
- Combine planning, reasoning, and world simulation
- Internal simulation without external tool calls

#### Architecture
```
1. WORLD MODEL (Learned)
   - Dynamics model of task domain
   - Predicts state transitions

2. PLANNING (Offline)
   - Use world model to simulate alternatives
   - No actual execution, just mental simulation
   - Find good policy/strategy

3. REASONING (Online)
   - Actual task execution
   - Guided by planned strategy
   - Adapt based on real outcomes

Analogy: Human planning (think ahead) + execution (act)
```

---

## 9. Neuro-Symbolic Integration: The Future?

### Motivation

Neither pure symbolic (rule-based) nor pure neural (LLM) sufficient:
- **Symbolic**: Interpretable but brittle, doesn't scale to complex domains
- **Neural**: Flexible but opaque, may hallucinate or be inconsistent

### Hybrid Approach

```
SYMBOLIC LAYER (Knowledge, Rules)
  ├─ Facts: "Paris is in France"
  ├─ Rules: "If X is city in Y, then X ⊆ Y"
  ├─ Constraints: "Patient history immutable"
  └─ Reasoning: Logical inference
       ↓ ↑
       ↓ ↑ (Grounding)
       ↓ ↑
NEURAL LAYER (LLM, Embeddings)
  ├─ Understanding: Language comprehension
  ├─ Generation: Natural responses
  ├─ Retrieval: Memory access
  └─ Learning: Pattern discovery
```

### Benefits

1. **Grounding**: Symbolic facts keep neural outputs grounded
2. **Interpretability**: Symbolic rules explain neural decisions
3. **Flexibility**: Neural learning discovers new patterns
4. **Reliability**: Constraints prevent hallucinations
5. **Learning**: Both symbolic facts updated and neural weights updated

---

## 10. Open Questions and Future Directions

### Fundamental Questions

1. **Consciousness-like processing**: Do LLMs need explicit workspace/global workspace?
2. **Emotional tagging**: Is explicit importance scoring sufficient substitute for emotion?
3. **Sleep consolidation**: Would periodic offline processing improve LLM learning?
4. **Social learning**: How do LLMs learn from collective human experience?
5. **Developmental trajectory**: Can LLMs develop memory gradually (infant→adult-like)?

### Practical Challenges

1. **Scaling episodic memory**: Handle years of interaction data
2. **Efficient retrieval**: Finding relevant memories in billions of stored episodes
3. **Privacy**: What to store and access control
4. **Multimodal memory**: Beyond text to images, audio, sensory
5. **Continual learning**: Update knowledge without catastrophic forgetting

---

## 11. Key References & Further Reading

1. Cowan, N. (2024). Judgments of Learning Distinguish Humans from Large Language Models in Predicting Memory. Nature Scientific Reports, 15, 6753.

2. Arrieta, A., et al. (2024). Large Language Models and Cognitive Science: A Comprehensive Review of Similarities, Differences, and Challenges. arXiv:2409.02387.

3. Geng, S., et al. (2024). From Human Memory to AI Memory: A Survey on Memory Mechanisms in the Era of LLMs. arXiv:2504.15965.

4. Wu, S., Oltramari, A., Francis, J., Giles, C. L., Ritter, F. E. (2025). Cognitive LLMs: Toward Human-Like Artificial Intelligence. Proceedings of the Manufacturing Informatics, 31(2), XX-XX.

5. Baars, B. J. (1988). A Cognitive Theory of Consciousness. Cambridge University Press.

6. Barsalou, L. W. (1999). Perceptual Symbol Systems. Behavioral and Brain Sciences, 22(4), 577-660.

---

## 12. Integration with Full Section 7

This final paper collection completes the hierarchical memory section by:

1. **Showing what's needed**: Identifying gaps between human and LLM memory
2. **Proposing solutions**: Cognitive architectures that address those gaps
3. **Connecting theory to practice**: Multiple papers demonstrating specific implementations
4. **Looking forward**: Open research directions grounded in cognitive science

Together with the previous papers (CoALA, Generative Agents, MemoryBank, Catastrophic Forgetting, Sleep/HMT), this section provides:

- **Theoretical foundation** (Atkinson-Shiffrin, Baddeley, Consolidation)
- **Framework** (CoALA organizing memory dimensions)
- **Empirical demonstration** (Generative Agents showing memory works)
- **Practical systems** (MemoryBank, SCM, HMT for real implementations)
- **Learning theory** (Catastrophic forgetting, LoRA, replay solutions)
- **Biology-inspired mechanisms** (Sleep consolidation, hierarchical organization)
- **Comparative analysis** (Human vs. LLM strengths/weaknesses)
- **Integrated architectures** (Cognitive workspace, multiple memory systems, neuro-symbolic)

This comprehensive coverage establishes that **hierarchical, human-inspired memory is essential for capable, coherent, long-context LLM agents**.
