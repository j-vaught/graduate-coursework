# Chain-of-Verification: Reducing Hallucinations

## Main Paper: Chain-of-Verification Reduces Hallucination in Large Language Models

**Authors:** Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu, Xian Li, Asli Celikyilmaz, Jason Weston

**Title:** Chain-of-Verification Reduces Hallucination in Large Language Models

**Year:** 2023 (ArXiv submission)

**Venue:** Findings of the Association for Computational Linguistics (ACL) 2024

**ArXiv:** https://arxiv.org/abs/2309.11495

**ACL Anthology:** https://aclanthology.org/2024.findings-acl.212/

**ResearchGate:** https://www.researchgate.net/publication/384218319_Chain-of-Verification-Reduces-Hallucination_in_Large-Language-Models

**Alternative Resources:**
- Guide: https://learnprompting.org/docs/advanced/self_criticism/chain_of_verification
- Overview: https://www.gaohongnan.com/influential/cove/cove.html
- Medium Article: https://medium.com/@will.gawron/the-chain-of-verification-prompt-engineering-technique-746a64b1834b

---

## Core Concept: The Four-Step Process

### Step 1: Draft Initial Response
The model generates an initial answer to the user's query without constraints.

```
User Query: "Who won the Olympic gold medal in X sport in 2020?"
Model Draft: "[Initial unconstrained answer]"
```

**Characteristics:**
- No explicit verification instruction
- Natural generation process
- Likely includes hallucinations if knowledge is uncertain
- Baseline attempt at task

### Step 2: Plan Verification Questions
The model generates factual questions to fact-check its own draft response.

```
Drafted Answer: "[Claims made in draft]"

Verification Questions:
1. "Is [claim X] correct?"
2. "Was [fact Y] mentioned accurately?"
3. "Is [entity Z] correctly identified?"
etc.
```

**Key Aspect:**
- Model identifies testable claims
- Questions designed to catch errors
- **Independent generation** (not biased by draft)
- Thorough coverage of claims

### Step 3: Answer Verification Questions Independently
Generate answers to verification questions **without referencing the draft**.

```
Q1: Is [claim X] correct?
A1: [Answer independently]

Q2: Was [fact Y] accurate?
A2: [Answer independently]
```

**Critical Feature:**
- **Independence** from draft prevents confirmation bias
- Fresh perspective on claims
- Unbiased factuality checking
- May contradict draft without anchor

### Step 4: Generate Verified Final Response
Create final response considering verification results.

```
Verification Results:
- Claim X: [Verified/Unverified/Contradicted]
- Fact Y: [Verified/Unverified/Contradicted]

Final Response: "[Updated answer using only verified claims]"
```

**Output Quality:**
- Only includes verified or self-consistent claims
- Removes hallucinations caught in verification
- More trustworthy final answer
- Higher confidence in claims

---

## Key Results and Empirical Findings

### Hallucination Reduction

**Headline Result:**
Reduces factual hallucinations by **50-70%** across multiple tasks.

### Task-Specific Performance

#### 1. List-Based Questions (Wikidata)
- **Domain:** Factual questions with enumerated answers
- **Format:** "List all [entities] that are [property]"
- **Improvement:** 50-70% hallucination reduction
- **Example:** "List all Oscar winners for Best Picture from 2010-2020"
- **Mechanism:** Verification catches missing/incorrect entities

#### 2. Closed-Book MultiSpanQA
- **Domain:** Question answering without external documents
- **Format:** Questions requiring multiple supporting facts
- **Improvement:** 50-65% reduction
- **Example:** "Name the three founders of [company]"
- **Mechanism:** Verification verifies each name independently

#### 3. Long-Form Text Generation
- **Domain:** Open-ended generation (summaries, articles, etc.)
- **Format:** Paragraph or multiple sentences
- **Improvement:** 50-60% hallucination reduction
- **Example:** Generate biography, news article, etc.
- **Mechanism:** Breaks down paragraphs into verifiable claims

---

## Why Chain-of-Verification Works

### 1. Separates Generation from Verification
- **Problem with single pass:** Generation and verification use same context
- **CoVe solution:** Two independent model invocations
- **Benefit:** Different model states catch errors
- **Mechanism:** Stochasticity in generation prevents confirmation bias

### 2. Makes Hallucinations Explicit
- **By generating verification questions:** Model identifies testable claims
- **Highlights uncertainty:** What to verify reveals what's uncertain
- **Forces commitment:** To specific checkable facts
- **Catches vague claims:** Cannot verify vague statements

### 3. Independent Verification Without Anchor
- **Prevents confirmation bias:** Answers verification questions fresh
- **Doesn't see draft:** Can't unconsciously confirm draft
- **Fresh reasoning:** Each question answered independently
- **Possible contradiction:** Can now disagree with draft

### 4. Explicit Filtering
- **Final response:** Only includes verified information
- **Removes uncertainty:** Explicitly excludes unverified claims
- **Improves trustworthiness:** Claims stand up to questioning
- **User confidence:** Fewer hallucinations boost user trust

---

## Detailed Implementation Guidance

### Prompt Engineering for Each Step

#### Step 1: Draft Prompt
```
You are an expert [domain] assistant. Answer the following question thoroughly and accurately.

Question: [User Question]
```

#### Step 2: Verification Planning Prompt
```
Your previous answer was: [Draft]

Now, plan a set of verification questions to fact-check your answer.
These questions should:
- Cover all major claims in your answer
- Be specific and testable
- Not depend on the draft (ask as if you didn't write it)
- Identify potential sources of error

Verification questions:
1.
2.
3.
```

#### Step 3: Answer Verification Prompt
```
Answer the following verification questions. For each question, provide a clear answer based on your knowledge. Do not reference your previous answer.

Question: [Verification Q1]
Answer: [Generate independently]

Question: [Verification Q2]
Answer: [Generate independently]
```

#### Step 4: Final Response Prompt
```
Based on the following information:
Original answer: [Draft]
Verification results: [Q1 answer], [Q2 answer], ...

Generate a final verified answer that only includes claims that are consistent with the verification results. Remove any claims that were contradicted or unverified.

Final answer:
```

---

## Advantages Over Alternatives

### vs. Retrieval-Augmented Generation
- **CoVe:** Works without external documents
- **RAG:** Requires curated knowledge sources
- **CoVe advantage:** Applicable when retrieval unavailable
- **Trade-off:** CoVe relies on LLM knowledge; RAG uses external source

### vs. Fine-Tuning
- **CoVe:** Inference-time method
- **Fine-tuning:** Requires training data and computation
- **CoVe advantage:** No training necessary
- **Trade-off:** Fine-tuning can be more efficient with data

### vs. Single-Pass Verification
- **CoVe:** Two independent passes (generation + verification)
- **Single-pass:** Generate and verify in one step
- **CoVe advantage:** Independence prevents confirmation bias
- **Trade-out:** 2x inference cost

### vs. Self-Consistency
- **CoVe:** Structured verification process
- **Self-consistency:** Majority voting over multiple samples
- **CoVe advantage:** Explicit error checking
- **Self-consistency advantage:** No domain knowledge needed to formulate questions

---

## Task-Specific Applications

### 1. Fact-Checking Tasks
- **Verify:** Claim against known facts
- **Question:** "Is [claim] true?"
- **Use case:** Misinformation detection

### 2. Entity Recognition and Linking
- **Verify:** Entity names and properties
- **Question:** "Is [entity] correctly identified?"
- **Use case:** NER for critical applications

### 3. Multi-Fact Reasoning
- **Verify:** Each supporting fact in reasoning chain
- **Question:** "Is [premise X] true?"
- **Use case:** Complex QA systems

### 4. Long-Form Generation
- **Verify:** Major claims in paragraphs
- **Question:** "Is this claim accurate?"
- **Use case:** Article, biography, report generation

### 5. Creative Writing with Facts
- **Verify:** Factual claims embedded in creative text
- **Question:** "Is this factual element correct?"
- **Use case:** Educational content, historical fiction

---

## Limitations and Challenges

### 1. Computational Cost
- **2x Inference:** Generation + Verification phases
- **Multiple verification questions:** Each requires model call
- **Practical impact:** Doubles latency
- **Mitigation:** Batch verification, parallel execution

### 2. Verification Quality
- **Model Limitations:** Verification only as good as LLM knowledge
- **Circular dependency:** Can't verify using unreliable LLM
- **Unknown unknowns:** Doesn't catch facts LLM doesn't know
- **Mitigation:** Combine with retrieval when possible

### 3. Question Generation Quality
- **Incomplete questions:** May miss hallucinations
- **Biased questions:** May not challenge draft adequately
- **Format issues:** Poorly formed questions
- **Mitigation:** Iterative refinement, human feedback

### 4. Failure Modes
- **All-wrong draft:** Multiple errors verified away, others missed
- **Question cascades:** Early undetected error cascades to later questions
- **Domain-specific gaps:** Domain where LLM has weak knowledge
- **Mitigation:** Combine with other techniques

### 5. Hallucination-to-Hallucination
- **Risk:** Verification questions could hallucinate
- **Both wrong:** Unverified draft and verification agree
- **Impact:** False confidence in hallucinations
- **Mitigation:** Ensemble verification, retrieval backing

---

## Empirical Analysis

### Error Analysis from Dhuliawala et al.

**Types of Hallucinations Caught:**
1. **Entity hallucinations:** Made-up names (people, places, etc.)
2. **Relationship hallucinations:** Incorrect facts about entities
3. **Event hallucinations:** Fabricated events or dates
4. **Property hallucinations:** Wrong attributes

**Types Sometimes Missed:**
1. **Subtle contradictions:** Logically inconsistent but not obviously wrong
2. **Omissions:** Missing facts (fewer claims than should be)
3. **Correct hallucinations:** True facts not in original context

---

## Variations and Extensions

### Chain-of-Thought + Verification
Combining chain-of-thought with verification:
- CoT provides reasoning
- Verification checks each step
- More transparent and verifiable reasoning

### Self-Verification
Model checks its own output in single pass:
- Faster than CoVe (single inference)
- Less effective than CoVe (confirmation bias)
- Good starting point for filtering

### Human-in-the-Loop Verification
Include human verification loop:
- Humans verify disputed claims
- Model learns from corrections
- Appropriate for critical applications

---

## Prompt Templates for Implementation

### Template: List-Based Questions
```
Step 1 - Draft:
Generate a comprehensive list of [entities with property].

Step 2 - Verify Questions:
For each item on the list, ask: "Is this [entity] actually a [property]?"

Step 3 - Verify Answers:
Answer each verification question independently.

Step 4 - Final:
Keep only verified items.
```

### Template: Long-Form Generation
```
Step 1 - Draft:
Write a [paragraph/article] about [topic].

Step 2 - Verify Questions:
Extract each factual claim and create questions:
"Is this claim true?"

Step 3 - Verify Answers:
Answer each question independently.

Step 4 - Final:
Rewrite removing unverified claims.
```

---

## Metric and Benchmark

### Evaluation Dimensions
1. **Hallucination Reduction:** Percentage of hallucinations eliminated
2. **Answer Preservation:** How much correct information is kept
3. **User Satisfaction:** Trust in verified answers
4. **Computational Cost:** Latency and token usage

### Datasets Used in Original Work
- **Wikidata-based:** List generation tasks
- **MultiSpanQA:** Multi-fact extraction QA
- **Long-form:** Biographical, narrative generation

---

## Integration with RAG Systems

**Hybrid Approach: CoVe + RAG**
1. **Retrieve** relevant documents
2. **Draft** answer using retrieved content
3. **Plan** verification questions over draft
4. **Verify** answers using retrieval context + knowledge
5. **Generate** final verified response

**Advantages:**
- Combines retrieval grounding with verification
- Catches errors not in retrieval source
- Filters hallucinations effectively

---

## Key Takeaway for Literature Review

Chain-of-Verification is an important **inference-time mitigation** for hallucinations:
- Simple prompt-based approach (no training)
- Significant hallucination reduction (50-70%)
- Works across multiple task types
- Explicit verification process increases transparency
- Practical trade-off: 2x latency for much higher reliability
- Complements retrieval-augmented generation
- Reveals model uncertainty through questions
- Extensible to various hallucination types

