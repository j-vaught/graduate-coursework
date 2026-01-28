# Self-Consistency in Language Models

## Main Paper: Self-Consistency Improves Chain of Thought Reasoning in Language Models

**Authors:** Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc V. Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery

**Title:** Self-Consistency Improves Chain of Thought Reasoning in Language Models

**Year:** 2023

**Venue:** International Conference on Learning Representations (ICLR) 2023

**ArXiv:** https://arxiv.org/abs/2203.11171

**OpenReview:** https://openreview.net/forum?id=1PL1NIMMrw

**ICLR Slides:** https://iclr.cc/media/iclr-2023/Slides/11718.pdf

**PDF Reference:** https://www.cs.toronto.edu/~cmaddis/courses/csc2541_w25/presentations/self-consistency.pdf

**DBLP:** https://dblp.org/rec/conf/iclr/0002WSLCNCZ23.html

**GitHub Implementation:** https://github.com/dj-sorry/self_consistency

---

## Core Concept and Motivation

### The Intuition Behind Self-Consistency

**Key Insight:** Complex reasoning problems typically admit **multiple distinct reasoning paths** that all lead to the **same unique correct answer**.

**Example:**
- Math problem: Solvable via addition-then-division OR division-then-multiplication
- Logic puzzle: Multiple logical progressions lead to identical conclusion
- Physics problem: Different problem-solving strategies converge

### Why This Matters
- Single greedy decoding is suboptimal for complex reasoning
- Models can reach correct answer through various intermediate steps
- Diversity of paths increases robustness

---

## Method: Replacing Greedy Decoding

### Standard Approach (Baseline)
```
Chain-of-Thought Prompting:
Q: [Question]
A: [Generate single path] → [Single answer]
```
- Takes greedy decoding path
- Single reasoning chain shown
- Vulnerable to local mistakes

### Self-Consistency Approach
```
Self-Consistency:
Q: [Question]
A: [Sample K diverse paths] → [Marginal over paths] → [Consensus answer]

Steps:
1. Generate K different reasoning chains (k=5-40 typical)
2. Extract answer from each chain independently
3. Select most consistent answer by marginalization
4. Report majority answer or highest confidence

Implementation:
- Use temperature sampling (T > 0) for diversity
- Multiple independent samples from model
- Ensemble aggregation at output level
```

---

## Key Results

### Benchmark Performance Improvements

All results use **Self-Consistency** vs. baseline **Chain-of-Thought with greedy decoding**:

| Benchmark | Baseline CoT | Self-Consistency | Improvement |
|-----------|-------------|------------------|------------|
| GSM8K | 40.4% | 58.3% | +17.9% |
| SVAMP | 60.7% | 71.7% | +11.0% |
| AQuA | 50.0% | 62.2% | +12.2% |
| StrategyQA | 61.3% | 67.7% | +6.4% |
| ARC-challenge | 77.7% | 81.6% | +3.9% |

**Key Observation:** Larger improvements on harder benchmarks (GSM8K, AQuA)

### Analysis by Task Difficulty
- **Harder tasks:** Larger self-consistency gains (15-20%)
- **Easier tasks:** Smaller gains (3-5%)
- **Complex reasoning:** Biggest benefit
- **Simple tasks:** Marginal improvements

---

## Detailed Methodology

### Sampling Strategy

**1. Generation Phase:**
- Temperature T = 0.7-1.0 (higher than greedy T=0)
- K samples per question (typical K=5-40)
- Independent sampling for diversity
- Complete reasoning chains generated

**2. Extraction Phase:**
- Parse final answer from each chain
- Robust extraction to handle format variations
- Handle multiple answer formats (numbers, text, etc.)

**3. Aggregation Phase:**
- **Majority Voting:** Most frequent answer wins
- **Confidence Scoring:** Weight by sampling probability
- **Weighted Aggregation:** Assign weights based on likelihood

**4. Final Answer:**
- Report majority consensus answer
- Include confidence score
- Handling ties gracefully

---

## Why Self-Consistency Works

### Theoretical Insights

**1. Error Correction Through Diversity**
- Individual chains may have reasoning errors
- Multiple paths reduce error probability
- Correct reasoning path likely to be shared

**2. Robustness to Intermediate Steps**
- CoT vulnerable to early mistakes cascading
- Self-consistency averages over intermediate variations
- Final answer more stable across paths

**3. Uncertainty Reduction**
- Single path may be coincidentally correct
- Multiple convergent paths = higher confidence
- Consensus implies genuine understanding

**4. Ensemble Benefit**
- Each sampling = different model instantiation (due to stochasticity)
- Combining diverse models reduces variance
- Standard ensemble benefits apply

### Information-Theoretic Perspective
- Sampling explores model's answer distribution
- Mode of distribution = most likely answer
- Marginalization improves generalization

---

## Comparison with Alternatives

### vs. Self-Verification
- Self-consistency: Aggregate multiple attempts
- Self-verification: Check and correct single attempt
- Self-consistency: More effective empirically

### vs. Fine-Tuning Chain-of-Thought
- Self-consistency: No training required
- Fine-tuning: Requires labeled data and resources
- Self-consistency: Drop-in improvement at inference

### vs. Model Scaling
- Self-consistency: K×cost (K samples)
- Larger models: Higher base cost
- Self-consistency: Cheaper than training larger model

### vs. Ensemble with Different Models
- Self-consistency: Single model, multiple samples
- Multi-model ensemble: Multiple models, single sample each
- Self-consistency: More practical and cost-effective

---

## Computational Considerations

### Cost-Benefit Analysis

**Cost:** K times inference cost (K = 5-40)
- Single inference: 1x cost
- 5-sample self-consistency: 5x cost
- But: Accuracy improvement often 10-20%

**Benefit:** Significant accuracy gains
- Effective accuracy improvement per token cost
- More efficient than larger models
- Practical for production systems

**Optimal K Selection:**
- K=5: Good balance for most tasks
- K=10-20: Maximum utility for complex reasoning
- K>40: Diminishing returns usually
- Task-dependent selection recommended

---

## Implementation Details

### Prompt Engineering for Self-Consistency

**Effective Practices:**
1. Use clear chain-of-thought prompts
2. Include reasoning examples
3. Let model show full work
4. Explicitly request step-by-step thinking

**Example Prompt:**
```
Let's think step by step.

Q: [Question]
A: Let me work through this step by step:
Step 1: [reason]
Step 2: [reason]
Therefore, the answer is [answer].
```

### Extraction and Parsing

**Robust Answer Extraction:**
- Look for explicit "answer:" markers
- Parse numeric/categorical answers
- Handle multiple answer formats
- Normalize for comparison (lowercase, trim, etc.)

**Handling Malformed Outputs:**
- Skip unparseable chains
- Use partial matching
- Fallback to string similarity

---

## Extensions and Related Work

### Universal Self-Consistency (Recent Extension)

**Paper:** Universal Self-Consistency for Large Language Models

**URL:** https://openreview.net/pdf?id=LjsjHF7nAN

**Contribution:**
- Extends self-consistency beyond reasoning tasks
- Applicable to diverse task types
- Improved consistency measurement
- Task-agnostic approach

---

## S2AF: Self-Check Framework

**Title:** S2AF: An action framework to self-check the Understanding Self-Consistency of Large Language Models

**URL:** https://www.sciencedirect.com/science/article/abs/pii/S0893608025002448

**Key Idea:**
- Active self-checking during reasoning
- Integrated confidence assessment
- Continuous verification during generation

---

## Applications Beyond Reasoning

### Hallucination Reduction
- Self-consistency provides confidence measure
- Low agreement = potential hallucination flag
- Multiple paths expose factual inconsistencies

### Factuality Improvement
- Different reasoning paths may verify facts
- Convergent paths = factually consistent
- Divergent paths = uncertainty about facts

### Knowledge-Grounded Tasks
- Multiple retrieval-based reasoning paths
- Consensus from different evidence sources
- Improved grounding through consistency checking

### Dialogue Systems
- Multiple response paths for same query
- Consistency ensures coherent dialogue
- Prevents contradictory responses

---

## Limitations and Challenges

### 1. Computational Cost
- K×inference cost is significant
- Not practical for latency-critical applications
- Cost-accuracy trade-off analysis needed

### 2. Tied Answers Problem
- Multiple tied answers: How to break tie?
- Arbitrary majority method may fail
- Need better aggregation for equal votes

### 3. Format Sensitivity
- Correct reasoning but wrong format = miscounting
- Requires robust answer extraction
- Task-specific parsing challenges

### 4. Long-Form Generation
- Works best for discrete answers
- Less clear for long-form text generation
- Measuring consistency is harder

### 5. Inherent Limitation
- Can't improve beyond maximum accuracy of any path
- If all K paths are wrong, self-consistency fails
- Model capability ceiling not overcome

---

## Empirical Patterns from Research

### Sample Size (K) Effect
- K=1: Baseline
- K=5: 80-90% of gains
- K=10: 90-95% of gains
- K=20+: Diminishing returns

### Task Dependency
- **Arithmetic:** High gains (15-20%)
- **Logic:** Medium gains (8-12%)
- **Common sense:** Low gains (3-7%)
- Task complexity drives benefit size

### Model Size Relationship
- Larger models: Consistent improvements
- Small models: Larger relative gains
- All model sizes benefit

### Temperature Parameter
- T too low (< 0.5): Low diversity, minimal gains
- T = 0.7-1.0: Optimal diversity-quality balance
- T too high (> 1.5): Quality degradation

---

## Best Practices for Implementation

1. **Baseline CoT First:**
   - Ensure quality chain-of-thought prompts
   - Self-consistency works best with good CoT

2. **Optimize K:**
   - Start with K=5
   - Measure accuracy/cost trade-off
   - Task-specific tuning

3. **Extract Carefully:**
   - Design robust answer extraction
   - Handle edge cases explicitly
   - Validate on dev set

4. **Balance Cost:**
   - Consider latency constraints
   - Monitor token usage
   - A/B test benefits vs. cost

5. **Combine with Other Techniques:**
   - Works with few-shot learning
   - Compatible with ensemble methods
   - Can improve other decoding strategies

---

## Key Takeaway for Literature Review

Self-consistency represents an important **inference-time improvement** for reasoning tasks:
- Simple to implement (no training)
- Significant accuracy gains (10-20% typical)
- Works across models and tasks
- Demonstrates power of sampling and aggregation
- Practical trade-off between accuracy and cost
- Reveals model uncertainty through disagreement
- Applicable to hallucination detection and confidence estimation

