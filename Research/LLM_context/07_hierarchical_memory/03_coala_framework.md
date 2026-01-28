# CoALA: Cognitive Architectures for Language Agents

## A Unifying Framework for LLM-Based Agents

---

## 1. Overview and Motivation

### Reference
- **Title**: Cognitive Architectures for Language Agents
- **Authors**: Theodore Sumers, Shunyu Yao, Karthik Narasimhan, Thomas L. Griffiths
- **Year**: 2023
- **Venue**: Published in TMLR (Transactions on Machine Learning Research), February 2024
- **ArXiv**: [2309.02427](https://arxiv.org/abs/2309.02427)
- **GitHub**: [awesome-language-agents repository](https://github.com/ysymyth/awesome-language-agents)

### Motivation

Recent advances in augmenting LLMs with external resources (internet, knowledge bases) and internal control structures (chain-of-thought, planning) have created a diverse landscape of language agents. However, **no systematic framework existed** to:
- Organize and categorize existing agents
- Understand design dimensions and tradeoffs
- Identify gaps and future research directions
- Connect to classical AI and cognitive science

**CoALA provides this unifying lens**, drawing inspiration from decades of cognitive architecture research (e.g., ACT-R, SOAR, CLARION).

---

## 2. Core Framework: Three Organizational Dimensions

### Dimension 1: Information Storage (Memory Architecture)

CoALA distinguishes **hierarchical memory components** inspired by human cognition:

#### **Working Memory**
- **Capacity**: Limited, task-dependent
- **Duration**: Short-term maintenance
- **Accessibility**: Immediately available to current processing
- **Composition**: Current state, recent observations, active goals
- **Function**: Supports ongoing reasoning, decision-making, planning
- **Implementation in LLMs**: Context window, in-context prompt, attention mechanism

#### **Long-Term Memory** (Three Subtypes)

1. **Procedural Memory**
   - **Content**: Skills, strategies, behavioral routines
   - **Encoding**: Conditional action mappings ("if condition, then action")
   - **Accessibility**: Implicit, automatic execution
   - **LLM analog**: Model parameters encoding procedures via gradient descent
   - **Example**: Learned patterns for tool use, reasoning steps

2. **Semantic Memory**
   - **Content**: Facts, concepts, general knowledge
   - **Encoding**: Declarative knowledge representations
   - **Accessibility**: Explicit retrieval, conceptual relationships
   - **LLM analog**: Learned embeddings and transformer parameters encoding factual knowledge
   - **Example**: Facts about the world, entity relationships, domain knowledge

3. **Episodic Memory**
   - **Content**: Specific events, experiences, contexts
   - **Encoding**: Event-specific representations with spatiotemporal grounding
   - **Accessibility**: Retrieval given contextual cues
   - **LLM analog**: External memory banks, retrieved examples, past dialogues
   - **Example**: Previous conversations, successful task solutions, specific agent observations

#### **Memory Architecture Diagram**

```
┌─────────────────────────────────────────────┐
│         WORKING MEMORY (In-context)         │
│  - Current state, observations, goals       │
└─────────────────────────────────────────────┘
           ↓ (retrieval) ↑ (storage)
┌─────────────────────────────────────────────┐
│        LONG-TERM MEMORY                     │
├─────────────────┬──────────────┬────────────┤
│  Procedural     │  Semantic    │  Episodic  │
│  (skills,       │  (facts,     │  (events,  │
│   strategies)   │   concepts)  │   contexts)│
└─────────────────┴──────────────┴────────────┘
```

### Dimension 2: Action Space (Interaction Capabilities)

CoALA divides agent actions into two categories:

#### **External Actions**
- **Grounding**: Directly affect the external environment or virtual world
- **Examples**:
  - API calls (web search, calculator, code execution)
  - Querying external databases
  - Robot/simulator control
  - Generating final outputs
- **Purpose**: Obtain information or change world state
- **Role**: Bridge between agent reasoning and external grounding

#### **Internal Actions**
- **Cognition**: Operate on internal representations (memory and reasoning)
- **Subcategories**:
  1. **Reasoning**: Transforming current beliefs/goals
     - Chain-of-thought generation
     - Decomposition of complex goals
     - Hypothesis generation
  2. **Retrieval**: Accessing information from long-term memory
     - Semantic search
     - Episodic memory lookup
     - Factual knowledge retrieval
  3. **Learning**: Updating long-term memory
     - Storing new facts (knowledge updates)
     - Refining strategies (procedural updates)
     - Recording experiences (episodic storage)

#### **Action Space Examples**

| Task | External Actions | Internal Actions |
|------|------------------|------------------|
| Question Answering | Search, calculate | Retrieve facts, reason |
| Code Generation | Run/test code | Decompose task, retrieve examples |
| Dialogue | Output response | Reflect on previous turns, update memory |
| Planning | Execute actions | Plan, reason about effects |

### Dimension 3: Decision-Making Procedure

CoALA models agent decision-making as an **interactive loop** with planning and execution:

#### **Planning Phase**
1. **Perception**: Observe current state (environment, working memory)
2. **Goal activation**: Determine what to pursue
3. **Deliberation**: Plan next action(s)
   - Evaluate which action (internal or external) to take
   - Consider information needs, reasoning depth, world changes
   - Utilize heuristics or learned policies

#### **Execution Phase**
1. **Act**: Execute chosen action
   - If internal: reasoning, retrieval, or learning
   - If external: call API, interact with environment
2. **Observe**: Process action results
3. **Update working memory**: Incorporate observations

#### **Loop Structure**

```
┌─────────────────────────────────────────────┐
│     OBSERVATION (Environment/State)         │
└────────────────────┬────────────────────────┘
                     ↓
┌─────────────────────────────────────────────┐
│  PLANNING: Which action next? (deliberation)│
└────────────────────┬────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│ EXECUTION: Internal/External Action          │
├──────────────────────────────────────────────┤
│ [Reasoning/Retrieval/Learning] | [API/Tool] │
└────────────────────┬─────────────────────────┘
                     ↓
┌──────────────────────────────────────────────┐
│  UPDATE: New observations, update WM, repeat │
└──────────────────────────────────────────────┘
```

#### **Decision-Making Strategies**

1. **Reactive**: Immediate action based on current observation (no planning)
2. **Deliberative**: Explicit planning phase before action
3. **Hybrid**: Combination of reactive fast decisions and deliberative planning
4. **Learned**: Action selection via learned policy (RL-based)
5. **Heuristic-based**: Predefined strategies (e.g., "if uncertain, search")

---

## 3. CoALA Applied: Example Agent Architectures

### Example 1: ReAct Agent (Yao et al., 2023)

Maps to CoALA as follows:

**Memory**:
- Working memory: Thought, action trajectory, current observation
- Semantic memory: Model parameters with world knowledge
- Episodic memory: None explicit

**Actions**:
- External: Tool use (search, calculator, QA systems)
- Internal: Reasoning (generate "Thought" via language model)

**Decision-Making**:
- Reactive loop: Observe → Think → Act → Observe...
- No explicit planning; action selection driven by reasoning

### Example 2: SayCan (Ahn et al., 2022)

Maps to CoALA as follows:

**Memory**:
- Working memory: Current task, object states, goal
- Semantic memory: Learned affordances and skills
- Episodic memory: Past trajectories (optionally)

**Actions**:
- External: Robot actions (pick, place, open)
- Internal: Reasoning about feasibility, learning from feedback

**Decision-Making**:
- Deliberative: Plan sequence of skills, then execute
- Hierarchical: High-level language reasoning → skill instantiation

### Example 3: Generative Agents (Park et al., 2023)

Maps to CoALA as follows:

**Memory**:
- Working memory: Current activity/plan, observations
- Semantic memory: World state, entity knowledge
- Episodic memory: Memory stream (rich, timestamped experiences)

**Actions**:
- External: Navigate environment, interact with objects
- Internal: Reflection on experiences, planning daily activities, learning from environment

**Decision-Making**:
- Deliberative: Plan day → execute + observe → reflect
- Hierarchical: Long-term goals → daily plans → hourly actions

---

## 4. Key Advantages of the CoALA Framework

### 1. **Unification**
- Provides common vocabulary for disparate agent architectures
- Enables systematic comparison across approaches
- Connects modern LLM agents to classical AI architectures

### 2. **Actionability**
- Identifies design dimensions (memory, actions, decision-making)
- Suggests improvements to existing agents
- Guides development of new agent capabilities

### 3. **Research Guidance**
- Highlights underexplored combinations (e.g., episodic memory + planning)
- Suggests scalability challenges
- Identifies missing capabilities (e.g., most agents lack procedural learning)

### 4. **Interpretability**
- Makes agent design choices explicit
- Clarifies what memory systems agents actually use
- Separates conceptual architecture from implementation details

---

## 5. Memory Architecture Deep Dive

### Working Memory in Language Agents

**In-context information** (current prompt/context window):
- Immediate task specification
- Previous conversation history
- Current observations
- Relevant retrieved examples
- Reasoning traces (chain-of-thought)

**Capacity constraints**:
- Token limit of LLM (4K-200K depending on model)
- Attention cost grows quadratically with sequence length
- Design question: What to prioritize in limited context?

### Semantic Memory in Language Agents

**Parametric Knowledge**:
- Learned during pretraining
- Fixed after training (unless fine-tuned)
- Distributed across parameters
- Accessed implicitly via forward pass

**Non-parametric Knowledge**:
- External databases (Wikipedia, knowledge graphs)
- Retrieved when relevant to task
- Explicit, interpretable
- Scalable to unbounded knowledge

### Episodic Memory in Language Agents

**Implementations**:
1. **Conversation history** (implicit episodic memory for dialogue)
2. **Experience buffers** for RL agents
3. **Memory banks** (e.g., Generative Agents' memory stream)
4. **Vector databases** (retrieval-augmented generation)

**Design questions**:
- How to represent episodes? (text, embeddings, structured)
- What triggers storage? (all events, or selective?)
- How to retrieve? (similarity, recency, importance)
- How to limit growth? (summarization, forgetting)

---

## 6. Emergent Research Directions from CoALA

### 1. **Procedural Memory & Skill Learning**
- How can agents learn and consolidate procedures?
- What's the role of gradient descent vs. explicit learning?
- Can language models develop stable "behavioral routines"?

### 2. **Episodic Memory Integration**
- How to build rich episodic memory for language agents?
- Role of emotion/importance signals in memory formation
- Integration with semantic and procedural memories

### 3. **Metacognition & Self-Monitoring**
- How should agents decide when to plan vs. react?
- What are good intrinsic signals for confidence/uncertainty?
- How to implement effective attention allocation?

### 4. **Scalability of Memory**
- How to scale episodic memory without unbounded growth?
- Abstracting and consolidating experiences (like sleep)
- Efficient retrieval from massive episodic stores

### 5. **Cross-Task Transfer**
- How do language agents generalize procedures across tasks?
- Role of semantic memory in enabling transfer
- Continual learning without catastrophic forgetting

---

## 7. Implementation Considerations

### Practical Design Choices

| Component | Decision | Implication |
|-----------|----------|-------------|
| WM | Implicit (in prompt) vs. Explicit | Transparency vs. efficiency |
| Semantic | Parametric only vs. + retrieval | Scalability vs. knowledge freshness |
| Episodic | None vs. limited vs. unbounded | Computational cost vs. learning |
| Actions | Predefined tools vs. learned | Interpretability vs. flexibility |
| Planning | None vs. heuristic vs. learned | Simplicity vs. optimality |

### Optimization Tradeoffs

1. **Memory size vs. retrieval accuracy**
   - Larger memory → more information available, harder to find relevant
   - Lossy compression → faster retrieval, lost information

2. **Planning depth vs. execution efficiency**
   - Deep planning → better strategies, slower
   - Shallow/reactive → fast, potentially suboptimal

3. **Episodic growth vs. storage costs**
   - Rich episodic memory → better learning, unbounded growth
   - Compression/forgetting → bounded storage, potential knowledge loss

---

## 8. Critical Reception and Extensions

### Strengths
- First comprehensive framework bridging LLM agents and classical cognitive architectures
- Clear conceptual dimensions enable systematic research
- Retrospectively organizes 100+ papers on language agents
- Connects to decades of cognitive science and AI research

### Limitations and Open Questions
- **Implementation gap**: Framework is conceptual; how to instantiate each component?
- **Learning mechanisms unclear**: How do agents acquire procedural and semantic knowledge?
- **Scaling challenges**: How to scale memory systems to realistic task complexity?
- **Integration mechanisms**: How do memory systems interact and trade off resources?
- **Evaluation**: Lack of standardized metrics for memory quality and agent capability

### Extensions and Follow-up Work

1. **Episodic Memory Focus**: Recent work emphasizes episodic memory importance (see next section: Generative Agents)
2. **Continual Learning**: Adaptation of CoALA for agents learning across many tasks
3. **Reasoning & Planning**: Integration with latest reasoning/planning research (e.g., chain-of-thought, tree-of-thought)
4. **Multimodal Extensions**: Application to agents handling vision, audio, text jointly

---

## 9. Key References & Further Reading

1. Sumers, T., Yao, S., Narasimhan, K., & Griffiths, T. L. (2023). Cognitive Architectures for Language Agents. TMLR (Transactions on Machine Learning Research).

2. Yao, S., Yu, D., Zhao, J., Shao, I., Hong, S., Wang, H., ... & Zhou, D. (2023). ReAct: Synergizing Reasoning and Acting in Language Models. ICLR 2023.

3. Ahn, M., Brohan, A., Brown, N., Chebotar, Y., Cortes, O., David, B., ... & Xu, P. (2022). Do As I Can, Not As I Say: Grounding Language in Robotic Affordances. arXiv:2204.01691.

4. Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative Agents: Interactive Simulacra of Human Behavior. UIST 2023.

---

## 10. Connection to Broader Section

CoALA provides the **conceptual framework** for this entire section on hierarchical memory. It identifies:
- What memory systems we should build (working, semantic, procedural, episodic)
- What actions they should support (reasoning, retrieval, learning)
- How they should interact (via planning-execution loops)

Subsequent papers operationalize CoALA's vision with specific implementations, empirical results, and neurobiological inspiration.
