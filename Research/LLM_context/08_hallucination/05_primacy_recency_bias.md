# Primacy and Recency Biases in LLMs

## Overview: Positional Biases in Language Models

LLMs exhibit strong **serial position effects** paralleling human cognitive biases:
- **Primacy Effect:** Items presented first are preferentially recalled/selected
- **Recency Effect:** Items presented last are preferentially recalled/selected
- **Combined Effect:** Creates U-shaped performance curve (see Lost in the Middle)

---

## Recent Empirical Research

### 1. Exploiting Primacy Effect To Improve Large Language Models

**Authors:** Bianca Raimondi and team

**Title:** Exploiting Primacy Effect To Improve Large Language Models

**Year:** 2025

**ArXiv:** https://arxiv.org/abs/2507.13949

**PDF:** https://arxiv.org/pdf/2507.13949

**Key Findings:**
- Primacy effect is systematic and exploitable
- GPT models exhibit strong primacy bias
- Leveraging primacy bias can improve performance
- Effect magnitude varies by task and model

**Specific Results:**
- Primacy bias influences 10.12% of decisions (averaged across models)
- Effect amplified for multiple-choice questions
- Larger models show reduced but persistent bias
- Bias predictable and can be strategically used

---

### 2. Serial Position Effects of Large Language Models

**Title:** Serial Position Effects of Large Language Models

**ArXiv:** https://arxiv.org/abs/2406.15981

**Year:** 2024

**Key Findings:**
- Extensive empirical confirmation of serial position effects
- Both primacy and recency effects confirmed
- Effects vary by task type
- Interaction with prompt structure

**Methodological Contribution:**
- Systematic evaluation framework
- Quantification of position bias magnitude
- Task-specific analysis

---

### 3. Recency Bias in LLM-Based Reranking

**Title:** Do Large Language Models Favor Recent Content? A Study on Recency Bias in LLM-Based Reranking

**ArXiv:** https://arxiv.org/abs/2509.11353

**Year:** 2025

**Full Text:** https://arxiv.org/html/2509.11353v1

**Key Findings:**
- Recency effect in ranking/reranking tasks
- "Fresh" passages consistently promoted
- Effect tested across 7+ LLM models
- Larger models attenuate but don't eliminate effect

**Empirical Results:**
- Models consistently rank last items higher
- Effect appears in list reranking tasks
- Affects information retrieval pipeline quality
- Challenges retrieval-augmented generation systems

---

### 4. The Hidden Position Bias in LLMs

**Source:** Medium article exploring position bias

**URL:** https://medium.com/@lyx_62906/the-hidden-position-bias-in-llms-why-your-ai-might-fail-when-it-s-asked-to-choose-26d59516f6ee

**Key Concepts:**
- Position bias affects choice/selection tasks
- Particularly problematic for multiple-choice QA
- Can cause model failures despite capability
- Often overlooked in evaluation

---

## Multiple Choice Questions and Option Order

### Critical Vulnerability

**Scenario:** Multiple choice assessment where option order affects outcome
- Option A is correct when presented first: High accuracy
- Same option D is correct when presented last: High accuracy
- Same option B is correct when presented second: Lower accuracy

### Research Evidence

**Finding:** GPT models show consistent option position preference
- Models favor options at extremes
- Middle options have lower selection rate
- Effect controls for actual semantic understanding

### Implications
- Unfair evaluation of LLMs on choice tasks
- Hidden performance limitations
- Confounded assessment results

---

## Primacy Effects in Detail

### Characteristics
1. **First Item Advantage**
   - Information presented first has disproportionate influence
   - Attention weights favor beginning of context
   - Cumulative effect across reasoning

2. **Direction Dependence**
   - Reading left-to-right biases leftmost (first) information
   - Affects both prompts and retrieved content

3. **Task Generality**
   - Multiple-choice questions: Strong effect
   - Free generation: Moderate effect
   - Reasoning tasks: Variable effect

### Magnitude
- **Typical Effect Size:** 5-15% performance difference
- **Extreme Cases:** Up to 25%+ degradation
- **Model Dependent:** Varies by size and training

### Interaction with Context Length
- Increases with longer context
- More pronounced when information scattered
- Cumulative effect across documents

---

## Recency Effects in Detail

### Characteristics
1. **Last Item Advantage**
   - Information presented last gets priority
   - Particularly strong in ranking tasks
   - Affects decision-making recency

2. **Buffer Effect**
   - Recent tokens in context have high attention
   - Working memory-like mechanism
   - Position relative to end matters more than absolute position

3. **Sequence Position Interaction**
   - Combined primacy + recency = U-curve
   - Valleys in middle positions
   - Asymmetric for different task types

### Magnitude
- **Ranking Tasks:** 10-20% effect typical
- **Choice Tasks:** 5-15% effect
- **Larger Models:** Effect attenuates but persists

### Empirical Evidence from Multiple Studies
- Consistent across GPT-3, GPT-3.5, GPT-4 (older versions)
- Observed in Claude, Llama, Falcon, PaLM
- Effect not size-dependent (large models still biased)

---

## Psychological Parallel: Cognitive Bias Induction

### Paper: Quantifying Cognitive Bias Induction in LLM-Generated Content

**URL:** https://openreview.net/pdf?id=jnd8pFD4GL

**Finding:** LLMs can induce cognitive biases in user reasoning through:
- Primacy/recency effects in generation
- Repetition of biased information at positions of influence
- Compounding effects across generations

---

## Psychology Comparison: Do Primacy Effects in LLMs Mirror Human Cognition?

### Paper: On Psychology of AI – Does Primacy Effect Affect ChatGPT and Other LLMs?

**URL:** https://arxiv.org/html/2504.20444v1

**Key Questions:**
- Are LLM biases algorithmic or cognitive parallels?
- Mechanisms fundamentally different from human memory?
- Can we apply human cognitive science insights?

**Findings:**
- Superficial similarities to human primacy effect
- Different underlying mechanisms (attention vs. working memory)
- Both lead to similar behavioral patterns
- Different mitigation strategies may be needed

---

## Practical Implications and Applications

### 1. Prompt Engineering Strategies

**To Reduce Primacy Bias:**
- Put critical information at beginning and end
- Repeat key facts multiple times
- Use explicit emphasis markers

**To Exploit Primacy Bias (When Favorable):**
- Place desired information first
- Use position strategically in demonstrations
- Lead with correct answers in few-shot

### 2. Few-Shot Demonstrations

**Primacy Effect on In-Context Learning:**
- First examples set implicit task understanding
- Format of initial examples particularly influential
- Label distribution in examples matters more at boundaries

**Optimal Strategy:**
- Carefully order examples
- Place canonical examples at boundaries
- Vary positions across evaluation

### 3. Multiple-Choice Question Design

**Bias Mitigation:**
- Randomize option positions across questions
- Use explicit position-independent format
- Verify answer distribution across positions

**Assessment Implications:**
- Don't rely on single presentation order
- Test position robustness
- Report performance by option position

### 4. Ranking and Reranking Tasks

**For RAG Systems:**
- Recency bias affects document ranking
- Last documents may be over-weighted
- Early documents may be under-weighted
- Consider position normalization

**Recommended Approach:**
- Randomize retrieval result ordering
- Use multiple evaluation permutations
- Account for position in reranking algorithms

---

## Mitigation Strategies

### 1. Position-Aware Prompting
```
"Consider all the following options equally:
Option A: ...
Option B: ...
Option C: ...
Do not favor options based on their position."
```

### 2. Reordering Strategies
- **Multiple Evaluations:** Test same information in different positions
- **Random Permutation:** Eliminate positional advantage
- **Counterbalancing:** Test all positions for critical comparisons

### 3. Architectural Solutions
- Modified positional encodings
- Position-aware attention mechanisms
- Debiasing during training

### 4. Post-Processing Correction
- Collect predictions across position variations
- Aggregate results to remove bias
- Weighted averaging based on position

---

## Task-Specific Position Bias Patterns

### Open-Domain Question Answering
- Primacy effect: First retrieved document over-weighted
- Recency effect: Last answer in multi-step reasoning preferred
- Combined: Non-linear performance vs. rank position

### Ranking/Reranking
- Strong recency: Last item consistently highest ranked
- Weak primacy: First item slightly over-ranked
- Middle items: Systematically undervalued

### Multiple-Choice Selection
- Balanced primacy + recency: Both A and D favored
- Option B/C: Lower selection rates
- Effect independent of semantic content

### Information Retrieval
- Document order in results affects selection
- Earlier mentions in documents are weighted more
- Position in document affects citation probability

### Dialogue/Conversation
- Recent utterances: Higher weight in responses
- Earlier context: Fades over conversation
- Primacy of speaker identity maintained

---

## Interaction with Context Length

### Short Contexts (< 1000 tokens)
- Position effects moderate
- All content relatively accessible
- Primacy/recency more balanced

### Medium Contexts (1000-10K tokens)
- Position effects pronounced
- Lost-in-the-middle effect visible
- Clear U-shaped curve

### Long Contexts (> 10K tokens)
- Extreme position effects
- Middle content increasingly inaccessible
- Recency may dominate over primacy

---

## Quantitative Patterns Across Studies

### Typical Quantified Effects
- **Primacy Advantage:** +5-10% over middle position
- **Recency Advantage:** +8-15% over middle position
- **Position Variance:** Total range 15-25% across positions

### Model Size Relationship
- Larger models: Slightly reduced bias
- Never eliminated: Present in all tested models
- Effect increases with context length

### Task Type Influence
- Ranking: Recency > Primacy
- Selection: Primacy ≥ Recency
- Generation: Primacy slightly favored
- Reasoning: Variable by subtask

---

## Research Questions and Future Directions

1. **Mechanistic Understanding**
   - Why do transformers exhibit these biases?
   - Role of positional encodings vs. attention?
   - Trainable or fundamental limitation?

2. **Model-Specific Investigation**
   - Do different architectures show same patterns?
   - Vision transformers and multimodal models?
   - Specialized long-context models?

3. **Mitigation Effectiveness**
   - Which strategies work best?
   - Trade-offs with other performance metrics?
   - Scalability of solutions?

4. **Application-Specific Optimization**
   - Task-optimal position strategies?
   - Domain-specific bias patterns?
   - Multi-task debiasing approaches?

---

## Key Takeaway for Literature Review

Position bias (primacy/recency effects) is:
- **Pervasive:** Present across all LLMs tested
- **Significant:** Causes measurable performance degradation
- **Predictable:** Systematic and quantifiable
- **Mitigatable:** Various strategies show promise
- **Critical for Practice:** Must account for in evaluation and deployment

