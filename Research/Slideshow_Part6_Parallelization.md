# Part 6: Parallelization with Agents
## A Comprehensive Guide to Agentic Coding Tools

---

## Section 1: Why Parallelization (5-6 slides)

---

### Slide 1: The Power of Parallel Execution
**Title:** Why Parallelization Matters in Agentic Coding

**Main Content:**
- **36% Performance Improvement**: Sequential task execution takes 10 minutes; parallel execution completes in 6.4 minutes
- **90% Quality Improvement**: Multiple agents working simultaneously on related problems cross-verify and catch errors
- **Real-world impact**: A codebase analysis that would take 1 hour sequentially completes in 17 minutes with parallel agents
- **Scalability**: Process more tasks without proportional time increase

**Visual Example:**
```
Sequential:  [Agent 1] [Agent 2] [Agent 3] = 10 min
Parallel:    [Agent 1, Agent 2, Agent 3] (concurrent) = 6.4 min

Speedup: 1.56x faster execution
```

**Speaker Notes:**
Parallelization is one of the most impactful techniques in agentic coding. When tasks are independent, running them simultaneously saves substantial wall-clock time. Emphasize that this isn't just about speed—multiple concurrent agents can validate each other's work, improving overall quality. The 36% improvement metric comes from real-world usage patterns where tasks that could run in parallel were instead run sequentially.

**Student Prompt Template:**
```
Run these tasks in parallel:
1. [Task A description]
2. [Task B description]
3. [Task C description]

After completion, compare and synthesize the results.
```

---

### Slide 2: Performance Gains Across Task Types

**Title:** Real Performance Metrics by Task Category

**Main Content:**
- **Research phase tasks**: 40-50% faster execution
  - Literature review + codebase exploration simultaneously
  - Example: Finding relevant papers while exploring implementations = 8 min instead of 15 min

- **Code analysis tasks**: 35-45% faster execution
  - Trace data flow + search for patterns + check docs in parallel
  - Example: Debugging a complex issue in 12 minutes vs 20 minutes sequentially

- **Data processing tasks**: 60-70% faster execution
  - Multiple parameter sweeps running simultaneously
  - Example: 10 experiments in parallel = complete in 5 minutes instead of 45 minutes

- **Build & test**: 30-40% faster execution
  - Linting + testing + documentation building simultaneously
  - Example: Full CI pipeline in 3 minutes instead of 5 minutes

**Speaker Notes:**
Different task categories see different speedup ratios. Data processing tasks see the highest improvements (60-70%) because they're most parallelizable. Code analysis sees moderate improvements (35-45%) because some work depends on outputs of previous work. Build pipelines see 30-40% improvements. Help students understand why—data processing tasks have minimal synchronization points, while code analysis often requires sequential refinement.

**Student Prompt Template:**
```
I need to optimize a [data processing/code analysis/build] pipeline.
Run these components in parallel:
- Component A: [description]
- Component B: [description]

Measure execution time and report the speedup.
```

---

### Slide 3: The 90% Quality Improvement Story

**Title:** How Parallelization Improves Code Quality

**Main Content:**
- **Multiple perspectives**: Different agents approach the same problem from different angles
  - Agent 1 focuses on performance
  - Agent 2 focuses on readability
  - Agent 3 focuses on maintainability
  - Consensus emerges on the best solution

- **Cross-validation**:
  - If 2 out of 3 agents suggest the same fix, it's likely correct
  - If results diverge, agents can investigate why
  - Reduces hallucination impact through consensus

- **Coverage improvement**:
  - Agent A tests functionality
  - Agent B tests edge cases
  - Agent C tests performance characteristics
  - Combined: 90% more test coverage

- **Real example**:
  ```
  Sequential single agent: Tests basic functionality only
  Three parallel agents: Test basic + edge cases + performance + security
  Result: 90% improvement in test coverage and reliability
  ```

**Speaker Notes:**
This is a key insight that students often miss—parallelization isn't just about speed, it's about quality. When you have multiple agents working on the same problem simultaneously, you get natural fault-tolerance through consensus. If all three agents suggest the same solution, you can have high confidence it's correct. If they diverge, that's a signal to investigate further. This is similar to how scientific consensus works—multiple independent observations converge on truth.

**Student Prompt Template:**
```
To improve code quality, have three agents independently:
1. [Agent A task]
2. [Agent B task]
3. [Agent C task]

Then synthesize: "Where do your recommendations align? Where do they differ?
What does the consensus suggest?"
```

---

### Slide 4: When Parallel Beats Sequential

**Title:** Decision Matrix: Parallel vs Sequential Execution

**Main Content:**
- **Use Parallel When:**
  - Tasks have NO data dependencies (Agent A's output not needed for Agent B)
  - Total execution time of sequential would exceed 10 minutes
  - Multiple perspectives would improve solution quality
  - You have budget for increased token consumption
  - Synchronization points are minimal

- **Use Sequential When:**
  - Task B requires output from Task A
  - Sequential execution is under 5 minutes total
  - Token budget is constrained
  - Tasks are tightly coupled
  - Single agent has sufficient expertise

**Decision Tree:**
```
Do the tasks have data dependencies?
├─ YES → Sequential (Agent A, then Agent B)
└─ NO → Can they benefit from parallel?
    ├─ NO → Sequential (simpler, fewer tokens)
    └─ YES → Is total time > 10 min?
        ├─ NO → Either approach works
        └─ YES → Parallel (justified by speedup)
```

**Speaker Notes:**
Students need a clear mental model for when to parallelize. The key question is independence. If Task B depends on Task A's output, you must run them sequentially. If they're independent, you have a choice. The decision depends on whether the time savings and quality improvements justify the token usage overhead. For small tasks (under 5 minutes total), the overhead might exceed benefits. For large tasks (over 10 minutes), parallelization almost always wins.

**Student Prompt Template:**
```
Before paralleling these tasks, verify independence:
1. Can [Task B] be completed without [Task A]'s output? (YES/NO)
2. Is the sequential time > 10 minutes? (YES/NO)
3. Would different perspectives improve the solution? (YES/NO)

If all are YES, proceed with parallelization.
```

---

### Slide 5: The 15x Token Usage Trade-off

**Title:** Understanding the Token Cost of Parallelization

**Main Content:**
- **Token multiplication factor**: Running N agents in parallel ≈ N × baseline token cost
  - 1 agent: 10,000 tokens
  - 3 parallel agents: ~30,000 tokens
  - 5 parallel agents: ~50,000 tokens

- **Why tokens multiply**:
  - Each agent receives the full context (duplicated)
  - Each agent performs independent reasoning (not shared)
  - Results are deduplicated, but thinking isn't
  - System prompts and instructions are repeated

- **Cost vs Benefit Analysis**:
  ```
  Task duration: 20 minutes sequential
  Parallelization speedup: 3x faster (6.7 minutes)
  Time saved: 13.3 minutes
  Token cost: 3x baseline

  Worth it if: Time value > token cost
  For research/debugging: Usually YES
  For routine tasks: Maybe NO
  ```

- **Mitigation strategies**:
  - Use smaller models for parallel tasks
  - Compress context for parallel agents
  - Parallelize only the critical path
  - Batch multiple results into one query

**Speaker Notes:**
This is crucial: parallelization isn't "free." You pay for it in tokens. Three parallel agents cost roughly 3 times as many tokens as one agent. Students need to understand this trade-off consciously. For research-heavy tasks where human time is expensive (debugging, literature review, architecture design), the token cost is justified. For routine tasks where you'd pay the same tokens sequentially anyway, the justification is weaker. Teach students to measure both wall-clock time and token consumption.

**Student Prompt Template:**
```
Before running N parallel agents, estimate:
1. Baseline token cost for 1 agent: [estimate]
2. Expected speedup: [multiple]
3. Time value of speedup: [minutes saved × hourly cost]
4. Token cost: ~[baseline × N]

Decision: Parallelize if [time value] > [token cost]
```

---

### Slide 6: Integration with Your Workflow

**Title:** Parallelization in Your Development Process

**Main Content:**
- **Research phase**: Parallelize heavily
  - Explore codebase + search literature + identify patterns (all simultaneously)
  - Justification: Long phase, complex synthesis, token cost low relative to time

- **Implementation phase**: Parallelize selectively
  - Parallelize independent modules
  - Sequential for integrated components
  - Justification: Tight integration requires sequencing

- **Review/Testing phase**: Parallelize moderately
  - Different test suites in parallel
  - Different linting/formatting rules simultaneously
  - Justification: Tests are independent

- **Cleanup phase**: Sequential only
  - Refactoring must be done carefully
  - Single agent maintains consistency

**Workflow Integration Example:**
```
Research Phase (PARALLEL)
├─ Agent 1: Explore codebase structure
├─ Agent 2: Search for related implementations
└─ Agent 3: Find best practices & documentation

Implementation Phase (SEQUENTIAL with parallel modules)
├─ Agent 1: Implement Module A
├─ Agent 2: Implement Module B (parallel to A)
├─ Agent 3: Implement Module C (parallel to A & B)
└─ Agent 4: Integration (sequential after A, B, C)

Review/Testing Phase (PARALLEL)
├─ Agent 1: Unit tests
├─ Agent 2: Integration tests
├─ Agent 3: Performance tests

Cleanup Phase (SEQUENTIAL)
└─ Agent 1: Refactoring & final review
```

**Speaker Notes:**
Help students see how parallelization fits into their overall workflow. Not every phase benefits equally. Research benefits heavily—you want multiple perspectives gathering information simultaneously. Implementation is more mixed—independent modules can be parallel, but integration must be sequential. Testing is highly parallelizable. Refactoring must be sequential for consistency.

**Student Prompt Template:**
```
For my [project type], parallelize the [phase name]:
1. Identify independent components
2. Assign each to a parallel agent
3. Define synchronization point
4. Estimate token cost vs time benefit
5. Proceed if justified
```

---

## Section 2: Parallelization Fundamentals (6-8 slides)

---

### Slide 7: Independent vs Dependent Tasks

**Title:** The Foundation of Parallelization: Task Independence

**Main Content:**
- **Independent tasks**: Can run in any order, produce same result
  - Agent A: "Analyze function performance"
  - Agent B: "Check code style compliance"
  - Agent C: "Review security implications"
  - Running in order ABC, CAB, or BCA produces same overall result

- **Dependent tasks**: B requires A's output
  - Agent A: "Parse the data file" → produces `parsed_data`
  - Agent B: "Analyze parsed_data" → requires output from A
  - Must run sequentially: A first, then B

- **Partially dependent tasks**: B needs some of A's output
  - Agent A: "Find bugs in code" (produces bug list)
  - Agent B: "Refactor code" (needs original code + bug info)
  - Both need original context, so they can run in parallel
  - Agent A focuses on finding issues
  - Agent B focuses on structure improvements
  - Results are combined for final refactoring

**Dependency Graph Examples:**
```
INDEPENDENT (all parallel):
Task A ─┐
Task B ─┼─→ [Combine] → Result
Task C ─┘

LINEAR DEPENDENT:
Task A → Task B → Task C → [Combine] → Result

MIXED (some parallel):
Task A ──┐
Task B ──┼─→ Task D → [Combine] → Result
Task C ──┘
```

**Speaker Notes:**
This is the foundational concept. Students must understand dependency before attempting parallelization. Use real examples from their domain. The key insight is that in a dependency graph, you can parallelize tasks at the same "level" (with no edges between them). This often requires careful problem decomposition.

**Student Prompt Template:**
```
Before parallelizing, map task dependencies:

1. Task A: [description] → produces [output]
2. Task B: [description] → requires [input from A?]
3. Task C: [description] → requires [input from A/B?]

Dependency Graph:
[Draw or describe edges]

Parallel groups:
- Parallel group 1: [tasks without inter-dependencies]
- Parallel group 2: [tasks that need group 1 output]
```

---

### Slide 8: Data Dependencies and Flow

**Title:** Tracking Information Flow in Parallel Tasks

**Main Content:**
- **Zero-dependency data**:
  - Each agent gets the full input context
  - No communication between agents
  - Example: "Analyze this code for performance, security, and readability" (3 parallel agents, each sees full code)

- **Partial-dependency data**:
  - Agent A produces intermediate result
  - Agent B and C use intermediate result AND original input
  - Cannot parallelize A with B and C
  - Can parallelize B with C after A completes
  ```
  Phase 1: A (gets original input)
  Phase 2: B and C in parallel (each gets A's output + original input)
  ```

- **Full-dependency data**:
  - A → B → C → D (pipeline)
  - No parallelization possible
  - Must execute sequentially
  - Token usage is 1x baseline

- **Data flow documentation**:
  ```
  Agent A Input: raw_data.json
  Agent A Output: parsed_data.json

  Agent B Input: parsed_data.json + analysis_requirements.txt
  Agent B Output: performance_metrics.json

  Agent C Input: parsed_data.json + analysis_requirements.txt
  Agent C Output: security_findings.json

  Final Synthesis Input: performance_metrics.json + security_findings.json
  ```

**Speaker Notes:**
Teach students to explicitly track what data flows where. This prevents subtle bugs where one agent needs output from another but they're scheduled in parallel. The key is being explicit about inputs and outputs. When documenting parallel tasks, always specify what each agent receives and produces.

**Student Prompt Template:**
```
Document the data flow for these parallel tasks:

Agent 1 - [Name]
├─ Input: [data/files needed]
├─ Process: [what it does]
└─ Output: [files produced]

Agent 2 - [Name]
├─ Input: [data/files needed]
├─ Process: [what it does]
└─ Output: [files produced]

Dependency analysis:
- Can these agents run in parallel? (check for circular dependencies)
- Do they need each other's outputs? (YES/NO)
```

---

### Slide 9: Synchronization Points

**Title:** Coordinating Parallel Agents with Synchronization

**Main Content:**
- **Explicit synchronization**: "After all agents complete, perform synthesis"
  ```
  PARALLEL PHASE:
  [Agent 1] [Agent 2] [Agent 3]
      ↓        ↓        ↓
  SYNCHRONIZATION BARRIER
      ↓        ↓        ↓
  SYNTHESIS PHASE:
  [Agent 4: Combine results]
  ```

- **Synchronization points in practice**:
  - Research phase: "Gather all agents' findings, then synthesize"
  - Implementation phase: "Module A and B complete, then integrate"
  - Testing phase: "All test results complete, then generate report"

- **Types of synchronization**:
  - **Full barrier**: Wait for ALL agents before proceeding
  - **Partial barrier**: Wait for ANY N agents (useful for redundancy)
  - **Timeout barrier**: Wait up to 5 minutes, then proceed with results so far

- **Implicit synchronization**:
  - Tool system forces synchronization (agent must complete before next step)
  - You can't access partial results until agent completes

**Example with Synchronization:**
```
Request parallel phase:
"Run these 3 agents in parallel: [A], [B], [C]"

[Wait for all to complete]

Synchronization point reached automatically

Next request:
"Here are the results from the 3 agents:
[Agent A output]
[Agent B output]
[Agent C output]

Now synthesize them..."
```

**Speaker Notes:**
Synchronization points are implicit in most agentic tools—you must wait for all parallel agents to complete before the next step. But you can be strategic about where you place synchronization. Some workflows use multiple parallel phases with synchronization between them. Help students visualize this as a timeline.

**Student Prompt Template:**
```
My parallel workflow:

Phase 1 (parallel):
- Agent 1: [task]
- Agent 2: [task]
- Agent 3: [task]

Synchronization barrier (wait for all)

Phase 2 (sequential synthesis):
- Agent 4: Combine outputs from agents 1-3 and [synthesis logic]

Phase 3 (parallel):
- Agent 5: [task with synthesis result]
- Agent 6: [task with synthesis result]

Synchronization barrier (wait for all)

Phase 4 (final):
- Generate final output
```

---

### Slide 10: Batch Execution and Agent Lifecycle

**Title:** How Agents are Spawned and Managed

**Main Content:**
- **Agent lifecycle in parallel**:
  ```
  [Spawn Agent 1] ─→ [Process] ─→ [Collect Output] ─→ [Destroy Agent 1]
  [Spawn Agent 2] ─→ [Process] ─→ [Collect Output] ─→ [Destroy Agent 2]
  [Spawn Agent 3] ─→ [Process] ─→ [Collect Output] ─→ [Destroy Agent 3]

  (All stages happen concurrently)
  ```

- **Batch execution characteristics**:
  - All agents receive FULL context (no state sharing)
  - Agents don't communicate with each other
  - Each agent has isolated working directory
  - Results are collected sequentially (one per agent)
  - Memory is reclaimed after each agent completes

- **Maximum parallelism**:
  - Most tools: 10 concurrent agents max
  - Claude Code: 10 concurrent agents
  - Cursor: 8 concurrent agents
  - Continue CLI: Unlimited (with rate limiting)

- **Resource implications**:
  - 10 concurrent agents = 10x memory usage
  - Each agent uses separate token counter
  - Network requests are concurrent
  - Processing is truly parallel (not threaded)

**Batch Execution Timeline:**
```
Time 0:     Spawn Phase
            [A][B][C][D][E] all spawned

Time 1-T:   Execution Phase
            [A running...][B running...][C running...][D running...][E running...]

Time T:     Completion Phase
            A completes: output collected
            B completes: output collected
            C completes: output collected
            D completes: output collected
            E completes: output collected

Time T+:    Results available for synthesis
```

**Speaker Notes:**
Emphasize that agents are truly spawned concurrently, not just queued. Each agent starts immediately in its own isolated environment. This is important for understanding performance characteristics. If each agent takes 2 minutes, 10 parallel agents take 2 minutes total (not 20 minutes). Help students understand the resource requirements—10 parallel agents is resource-intensive.

**Student Prompt Template:**
```
For my parallel execution:
1. How many agents will I spawn? [N]
2. Expected time per agent: [T] minutes
3. Total parallel execution time: ~[T] minutes
4. Token per agent: ~[tokens]
5. Total tokens for all agents: ~[N × tokens]

Check: Is N ≤ 10? (yes, proceed / no, batch into multiple rounds)
```

---

### Slide 11: Dealing with Failures in Parallel Execution

**Title:** Error Handling and Fault Tolerance

**Main Content:**
- **Single agent failure modes**:
  - Agent timeout: (rare, usually 30-60 min limit)
  - Agent crash: (can happen if OOM)
  - Invalid output: (agent produces malformed results)
  - Partial failure: (completes some tasks, fails on others)

- **Failure recovery strategies**:
  - **Consensus-based**: If 2 of 3 agents succeed, use majority
    ```
    Agent A: Success ✓
    Agent B: Success ✓
    Agent C: Timeout ✗

    Use results from A & B, they agree
    ```

  - **Redundancy**: Run tasks with more agents than needed
    ```
    Critical task: Run on 5 agents
    Accept result if 4+ agree
    Handles 1 failure gracefully
    ```

  - **Fallback**: Have sequential backup
    ```
    Try parallel: 3 agents with 5 min timeout
    If all fail or timeout: Sequential retry with 1 agent
    ```

- **Detecting failures**:
  - Check for empty outputs
  - Look for error messages in results
  - Compare outputs for consistency
  - Flag anomalies in results

**Error Handling Pattern:**
```
Request parallel execution
↓
[Wait with timeout]
↓
Collect results:
├─ All successful → Proceed
├─ Some successful → Check consensus
│  ├─ Majority agree → Use consensus
│  └─ No majority → Fallback to sequential
└─ All failed → Fallback to sequential
```

**Speaker Notes:**
Teach students that parallelization increases complexity in failure modes. One agent failure in a 3-agent parallel run is a 33% failure rate. This is usually acceptable if you have consensus logic. Teach the redundancy principle: critical tasks should run on more agents than strictly needed, allowing you to handle failures gracefully.

**Student Prompt Template:**
```
Error handling strategy for parallel tasks:

Critical level: [LOW/MEDIUM/HIGH]

If LOW (not critical):
  "Run these in parallel, use results from first successful completion"

If MEDIUM (somewhat critical):
  "Run these in parallel (2 agents), use result if they agree"

If HIGH (very critical):
  "Run these in parallel (3 agents), use result if 2+ agents agree.
   If not, retry with different approach/agent."
```

---

## Section 3: Parallel Patterns by Use Case (12-15 slides)

---

### Slide 12: Pattern 1 - Research & Literature Review (Part A)

**Title:** The Parallel Research Pattern

**Main Content:**
- **Pattern goal**: Gather information from multiple angles simultaneously

- **Three-agent research breakdown**:
  - **Agent 1 - Codebase Explorer**:
    - Task: "Explore the codebase structure"
    - Searches for: File organization, module boundaries, key implementations
    - Produces: Codebase map and relevant file locations

  - **Agent 2 - Literature Searcher**:
    - Task: "Search for papers, documentation, and best practices"
    - Searches for: Academic papers, official docs, tutorials
    - Produces: Bibliography and key concepts to consider

  - **Agent 3 - Pattern Identifier**:
    - Task: "Find similar implementations in the codebase"
    - Searches for: Design patterns used, similar solved problems
    - Produces: List of precedents to learn from

- **Synchronization**: All three agents complete, then synthesis agent combines results

**Example workflow**:
```
Research Task: "How should we implement authentication?"

PARALLEL PHASE:
[Agent 1: Explore existing auth in codebase]
[Agent 2: Search for modern auth best practices]
[Agent 3: Find similar auth implementations in open source]

SYNTHESIS PHASE (sequential):
[Agent 4: Combine findings and recommend approach]
```

**Token allocation**:
- Per-agent: ~2,000-3,000 tokens
- Total: ~9,000 tokens (3 agents)
- Sequential alternative: ~3,000 tokens (1 agent, but lower quality)
- Trade-off: +6,000 tokens for better research quality and consensus

**Speaker Notes:**
The research pattern is one of the most effective parallelization patterns. Students often waste time researching sequentially when they could parallelize. The key insight is that research has no dependencies—you can explore code, search literature, and find patterns all at the same time. The synthesis happens only after all information is gathered. This is analogous to how humans research: reading multiple sources in parallel, then synthesizing.

**Student Prompt Template:**
```
To research [topic], run these agents in parallel:

Agent 1 - Codebase Explorer:
"Explore the [project name] codebase structure. Find all files related to [topic].
Describe the existing implementation."

Agent 2 - Literature Searcher:
"Search for papers, documentation, and best practices about [topic].
Focus on [specific area]. Find at least 3 authoritative sources."

Agent 3 - Pattern Identifier:
"Find similar implementations to [topic] in open source projects.
Identify common patterns and anti-patterns."

Then: "Synthesize these three reports into a comprehensive research summary."
```

---

### Slide 13: Pattern 1 - Research & Literature Review (Part B)

**Title:** Advanced Research Patterns

**Main Content:**
- **Multi-layer research** (5+ agents):
  ```
  Layer 1 (Parallel):
  - Agent 1: Search academic papers
  - Agent 2: Search GitHub implementations
  - Agent 3: Search documentation

  Sync Point

  Layer 2 (Parallel):
  - Agent 4: Analyze found papers for key concepts
  - Agent 5: Analyze found code for patterns
  - Agent 6: Analyze docs for best practices

  Sync Point

  Layer 3 (Sequential):
  - Agent 7: Generate comprehensive report
  ```

- **Redundant searches for critical topics**:
  - If finding specific info is critical, have 2 agents search
  - Different search strategies might find different results
  - Combine to ensure comprehensive coverage

- **Iterative research**:
  - Phase 1: Broad parallel search
  - Synthesis: "What should we explore deeper?"
  - Phase 2: Focused parallel research on gaps
  - Final synthesis: Complete picture

- **Research pattern metrics**:
  - Quality improvement: 70-85% (due to multiple perspectives)
  - Time improvement: 40-50% (speedup from parallelization)
  - Total research time: 8 min parallel vs 15 min sequential

**Speaker Notes:**
Show students how the research pattern can be layered. Basic research is 3 agents in parallel. Advanced research might be 6+ agents across 2-3 layers. The key is thinking of research as having phases, where each phase can be parallelized. This is more efficient than having one super-agent try to do all research simultaneously.

**Student Prompt Template:**
```
Multi-layer research for [complex topic]:

PHASE 1 - Broad Parallel Search:
Agent 1: "Search for [aspect A] research and implementations"
Agent 2: "Search for [aspect B] research and implementations"
Agent 3: "Search for [aspect C] research and implementations"

After Phase 1, I'll ask: "Based on these findings, what are the 3 biggest
knowledge gaps we should investigate further?"

PHASE 2 - Focused Parallel Investigation:
Agent 4-6: Investigate the identified gaps

PHASE 3 - Synthesis:
"Combine all findings into a research report with recommendations"
```

---

### Slide 14: Pattern 2 - Data Processing & Experiments

**Title:** Parallel Data Processing and Parameter Sweeps

**Main Content:**
- **Pattern goal**: Process data or run experiments with different parameters simultaneously

- **Parameter sweep example**:
  ```
  Sequential:
  Agent 1: Experiment with learning_rate=0.001 (5 min)
  Agent 2: Experiment with learning_rate=0.01 (5 min)
  Agent 3: Experiment with learning_rate=0.1 (5 min)
  Total: 15 minutes, 3x tokens

  Parallel:
  Agent 1: Experiment with learning_rate=0.001 (5 min)
  Agent 2: Experiment with learning_rate=0.01 (5 min)
  Agent 3: Experiment with learning_rate=0.1 (5 min)
  Total: 5 minutes, 3x tokens

  Speedup: 3x faster, same token cost
  ```

- **Data processing tasks**:
  - **Dataset A & B analysis**: Split dataset work
  - **Format conversion**: Convert different formats in parallel
  - **Cleaning & validation**: Different validation approaches simultaneously
  - **Feature engineering**: Different feature sets in parallel

- **Experimental design**:
  - Control variable: Keep constant across agents
  - Test variable: Each agent tests different value
  - Example: All agents test same code, different input configurations

**Parallel Experiment Pattern:**
```
Experiment Task: Find optimal learning rate

Agent A: learning_rate=0.0001
├─ Train model
├─ Evaluate on test set
└─ Report accuracy + convergence time

Agent B: learning_rate=0.001
├─ Train model
├─ Evaluate on test set
└─ Report accuracy + convergence time

Agent C: learning_rate=0.01
├─ Train model
├─ Evaluate on test set
└─ Report accuracy + convergence time

[Sync]

Synthesis: Compare results, identify optimal learning rate
```

**Speaker Notes:**
This is where parallelization gives the biggest benefits—70-80% speedup for data processing. Students should recognize that any task with multiple independent runs or parameter values is a candidate for parallelization. The key constraint is that each run must be independent (no dependencies between parameter values).

**Student Prompt Template:**
```
Parallel experiment for [variable name]:

Base configuration: [constant parameters]

Agent 1: Run experiment with [variable]=[value A]
├─ Load [dataset]
├─ Configure [parameter]=[value A]
├─ Execute [experiment]
└─ Report [metrics: metric1, metric2, ...]

Agent 2: Run experiment with [variable]=[value B]
├─ Load [dataset]
├─ Configure [parameter]=[value B]
├─ Execute [experiment]
└─ Report [metrics: metric1, metric2, ...]

Agent 3: Run experiment with [variable]=[value C]
[same structure]

After all complete: "Compare the three results and identify the optimal value."
```

---

### Slide 15: Pattern 3 - Code Analysis & Debugging

**Title:** Parallel Code Review and Debugging

**Main Content:**
- **Pattern goal**: Analyze code from multiple perspectives simultaneously for bugs, style, and performance

- **Three-agent code review**:
  ```
  Agent 1 - Correctness Reviewer:
  "Review this code for logical errors, edge cases, off-by-one errors."

  Agent 2 - Style/Maintainability Reviewer:
  "Review this code for readability, naming conventions, structure."

  Agent 3 - Performance Reviewer:
  "Review this code for performance, memory usage, algorithmic efficiency."
  ```

- **Debugging pattern**:
  ```
  Agent 1: Trace data flow through the buggy code
  Agent 2: Search codebase for similar bugs and how they were fixed
  Agent 3: Review related tests to understand intended behavior

  [Sync]

  Agent 4: Integrate findings and propose fix
  ```

- **Static analysis tasks**:
  - **Agent 1**: Check for security vulnerabilities
  - **Agent 2**: Check for performance issues
  - **Agent 3**: Check for maintainability issues
  - **Agent 4**: Check for concurrency issues

- **Real bug finding example**:
  ```
  Code: for i in range(len(list)-1): list[i+1] = list[i]

  Agent 1 (Correctness): "This has a logical error—it overwrites before copying"
  Agent 2 (Style): "Using enumerate() would be clearer"
  Agent 3 (Performance): "This is O(n) memory for O(n) time, could be optimized"

  Consensus: Bug exists, fix needed
  ```

**Speaker Notes:**
Code analysis is highly parallelizable because reviewers look for different things. A performance reviewer focuses on different aspects than a security reviewer. Running them in parallel saves time and catches more issues. Emphasize that consensus matters—if all three agents agree there's a bug, it's almost certainly real.

**Student Prompt Template:**
```
Parallel code analysis for [function/module]:

Agent 1 - Correctness Reviewer:
"Review this code for logical errors, edge cases, boundary conditions:
[code snippet]

Produce a list of potential bugs with severity levels."

Agent 2 - Style & Maintainability Reviewer:
"Review this code for readability and maintainability:
[code snippet]

Suggest improvements to naming, structure, and documentation."

Agent 3 - Performance Reviewer:
"Review this code for performance and resource usage:
[code snippet]

Identify algorithmic improvements and resource bottlenecks."

Synthesis: "Combine these three reviews. What's the consensus on the main issues?"
```

---

### Slide 16: Pattern 4 - Build & Test Parallelization

**Title:** Concurrent Build and Test Execution

**Main Content:**
- **Pattern goal**: Execute independent build tasks simultaneously

- **Build pipeline parallelization**:
  ```
  Sequential:
  [Lint] → [Unit Tests] → [Integration Tests] → [Build] → [Docs]
  Total: 20 minutes

  Parallel:
  [Lint] ──┐
  [Unit Tests] ─┼─→ [Integration Tests] → [Build]
  [Format]──┘
                              └─→ [Docs] (parallel to Build)
  Total: 8 minutes
  ```

- **Independent test suites**:
  - Unit tests (fast, 2 min)
  - Integration tests (medium, 3 min)
  - Performance tests (medium, 3 min)
  - Security tests (medium, 4 min)
  - All can run in parallel: total 4 min instead of 12 min

- **Build parallelization**:
  - Compile module A + B + C in parallel (not sequentially)
  - Generate docs + run tests simultaneously
  - Check formatting while running type-checking

- **Post-test phases**:
  - Code coverage report (after all tests)
  - Performance regression analysis (after performance tests)
  - Documentation generation (parallel to tests)
  - Deployment (after all checks pass)

**Build Timeline Example:**
```
Sequential approach:
[Lint] (1m) → [Unit] (2m) → [Integration] (3m) → [Build] (2m) → [Docs] (2m)
TOTAL: 10 minutes

Parallel approach:
[Lint] (1m) ──────┐
[Unit] (2m) ──────┼→ [Integration] (3m) ──┐
[Format] (1m)─────┘                        ├→ [Build] (2m)
[Type-check] (1m)─────┐                    │
[Security] (2m)───────┼──→ [Post-checks]───┤
                       │    └──→ [Docs] (2m)
TOTAL: 5 minutes

Speedup: 2x faster
```

**Speaker Notes:**
Many students don't realize how much build time can be parallelized. Modern CI/CD systems do this automatically, but understanding it conceptually helps when designing custom build pipelines. The key is identifying which tasks are truly independent and which have implicit dependencies (e.g., you must lint before build for consistent output).

**Student Prompt Template:**
```
Parallelize the build pipeline:

Current sequential steps:
1. Lint (2 min)
2. Type-check (1 min)
3. Format (1 min)
4. Unit tests (3 min)
5. Integration tests (4 min)
6. Build (2 min)
7. Generate docs (2 min)

Parallel groups:
Group 1 (early, parallel): Lint, Type-check, Format
├─ Time: 2 min (longest)

Group 2 (after group 1): Unit tests, Integration tests
├─ Can they run parallel? [Yes, independent]
├─ Time: 4 min (longest)

Group 3 (after group 2): Build + Docs parallel
├─ Time: 2 min

TOTAL PARALLEL: 8 min (vs 17 min sequential)
```

---

### Slide 17: Pattern 5 - Content Generation and Analysis

**Title:** Parallel Content Creation and Writing

**Main Content:**
- **Pattern goal**: Generate different content pieces or analyze text from multiple angles simultaneously

- **Multi-format generation**:
  ```
  Write a report, then simultaneously generate:
  Agent 1: Executive summary (1 page)
  Agent 2: Technical details (5 pages)
  Agent 3: Appendix with code samples (3 pages)

  Total: 3-4 min parallel vs 6-8 min sequential
  ```

- **Document review pattern**:
  ```
  Agent 1: Grammar, spelling, punctuation check
  Agent 2: Technical accuracy review
  Agent 3: Clarity and readability review
  Agent 4: Style consistency review

  All parallel, then synthesize feedback
  ```

- **Content variants**:
  - Generate documentation for different audiences
    - Agent A: For beginners
    - Agent B: For advanced users
    - Agent C: API reference
  - All parallel, combine into single docs site

- **Blog post or article writing**:
  ```
  Given topic: "Best practices for parallel processing"

  Agent 1: Write introduction section
  Agent 2: Write technical section
  Agent 3: Write examples section

  [Sync]

  Agent 4: Combine sections, check flow, edit for consistency
  ```

**Content Pipeline Example:**
```
Input: Research findings about distributed systems

Parallel content generation:
├─ Agent 1: Write 2-page executive summary
├─ Agent 2: Write 10-page technical whitepaper
├─ Agent 3: Write 5-page beginner's guide
└─ Agent 4: Create FAQ document

[Sync]

Post-processing (sequential):
└─ Agent 5: Review all content for consistency, combine into one document
```

**Speaker Notes:**
Content generation is a practical parallelization pattern that students can use immediately. If you need multiple content pieces from the same source material, generate them in parallel. The key is that the content pieces are independent—a beginner's guide doesn't depend on a technical whitepaper output.

**Student Prompt Template:**
```
Parallel content generation for [topic]:

Source material: [description or file]

Agent 1: Generate [content type 1]
└─ Audience: [target audience]
└─ Length: [page count]
└─ Focus: [key points]

Agent 2: Generate [content type 2]
└─ Audience: [target audience]
└─ Length: [page count]
└─ Focus: [key points]

Agent 3: Generate [content type 3]
└─ Audience: [target audience]
└─ Length: [page count]
└─ Focus: [key points]

[After all complete]

"Combine the three content pieces. Remove redundancy while preserving unique
perspective from each piece."
```

---

## Section 4: Claude Code Parallelization Deep Dive (8-10 slides)

---

### Slide 18: Explicit Parallel Request Syntax in Claude Code

**Title:** How to Write Parallel Requests in Claude Code

**Main Content:**
- **The magic keywords**: "in parallel", "simultaneously", "concurrently"
  - Any of these triggers parallel execution
  - Placement: Should be explicit at start of task description
  - Effect: Changes execution from sequential to parallel

- **Basic syntax**:
  ```
  "Run these tasks in parallel:
  1. [Task A description]
  2. [Task B description]
  3. [Task C description]

  After completion, [synthesis instructions]"
  ```

- **Implicit vs explicit**:
  - Implicit: "Explore the code, search for papers, find patterns"
    (Claude may or may not parallelize)
  - Explicit: "Run these in parallel: 1) explore code 2) search papers 3) find patterns"
    (Claude will parallelize)

- **Request structure**:
  ```
  "Run [N] agents in parallel:

  Agent 1 - [Role]:
  [Task description]
  [Specific instructions]
  [Expected output]

  Agent 2 - [Role]:
  [Task description]
  [Specific instructions]
  [Expected output]

  ...

  After all agents complete, [synthesis/consolidation instructions]"
  ```

- **Common phrasing**:
  - "Run in parallel"
  - "Simultaneously"
  - "Concurrently"
  - "At the same time"
  - "All at once"
  - "Do X while doing Y while doing Z"

**Good vs Poor Parallel Requests:**
```
POOR:
"Explore the code. Search for papers. Find patterns."
(Ambiguous—might not parallelize)

GOOD:
"Run three agents in parallel:
1. Explore the codebase structure
2. Search for relevant papers
3. Find similar implementations

Then combine findings."

BEST:
"Run these agents in parallel:

Agent 1 - Codebase Explorer:
Explore [project] codebase. Find all files related to [topic].
Report structure and key implementations.

Agent 2 - Literature Searcher:
Search for papers about [topic]. Find at least 3 sources.
Report findings and key concepts.

Agent 3 - Pattern Finder:
Find similar implementations in open source.
Report common patterns and best practices.

After all complete: Synthesize findings into a research report."
```

**Speaker Notes:**
Emphasize that explicitness matters. If you want parallelization, say it explicitly. Claude Code will respect the explicit request and spawn multiple agents. The more detailed you are about what each agent should do, the better the results. Use clear role names and specific instructions for each agent.

**Student Prompt Template:**
```
To parallelize your requests in Claude Code, use this template:

"Run [N] agents in parallel:

Agent 1 - [Specific Role Name]:
Objective: [What should this agent accomplish?]
Task: [Specific task description]
Focus on: [Key aspects]
Produce: [Expected output type]

Agent 2 - [Specific Role Name]:
Objective: [What should this agent accomplish?]
Task: [Specific task description]
Focus on: [Key aspects]
Produce: [Expected output type]

[Repeat for each agent]

After all agents complete:
[How should outputs be combined/synthesized?]"
```

---

### Slide 19: Maximum Concurrent Agents in Claude Code

**Title:** Scaling Limits and Resource Management

**Main Content:**
- **Maximum parallel agents**: 10 concurrent
  - This is a hard limit in Claude Code
  - Attempting to spawn 11 agents will error or queue
  - Best practice: Stay under 10 for reliability

- **Recommended maximums by use case**:
  - **Research tasks**: 3-5 agents (optimal quality)
  - **Data processing**: 5-10 agents (processing power limited by dataset)
  - **Code analysis**: 3-4 agents (reviewing same code)
  - **Build/testing**: 5-8 agents (I/O limited)

- **Beyond 10 agents—batching strategy**:
  ```
  Naive approach (fails):
  "Run 15 agents in parallel" → ERROR (exceeds 10)

  Correct approach:
  Batch 1: "Run agents 1-10 in parallel"
  [Wait for results]
  Batch 2: "Run agents 11-15 in parallel"
  [Wait for results]
  [Synthesize all results]
  ```

- **Memory and resource implications**:
  - 1 agent: ~500MB memory + context
  - 5 agents: ~2.5GB memory
  - 10 agents: ~5GB memory
  - System impact: Very high for 10 agents
  - Best practice: Use 3-5 agents for stability

- **Token implications at scale**:
  ```
  Task requiring 5,000 tokens with 1 agent

  3 agents: ~15,000 tokens total
  5 agents: ~25,000 tokens total
  10 agents: ~50,000 tokens total

  Rule of thumb: N agents ≈ N × baseline tokens
  ```

**Resource Usage by Agent Count:**
```
Agents | Memory | Tokens | Execution | Recommended
   1   |  500MB | 5k     |    5 min  | Always safe
   3   | 1.5GB  | 15k    |    5 min  | Good quality
   5   | 2.5GB  | 25k    |    5 min  | Balanced
   8   | 4.0GB  | 40k    |    5 min  | High resource
  10   | 5.0GB  | 50k    |    5 min  | Very high
```

**Speaker Notes:**
Teach students to think about resource constraints. More agents isn't always better. For most tasks, 3-5 agents is optimal (quality + resources + token cost). When you need more parallelism, batch into multiple rounds. Explain the batching strategy so they can scale beyond 10.

**Student Prompt Template:**
```
For my parallel task with [N] agents:

If N ≤ 10:
  "Run these [N] agents in parallel: [list agents]"

If N > 10:
  "Run these agents in parallel (BATCH 1):
  1. [agents 1-10]

  [Wait for results]

  Then run BATCH 2:
  2. [agents 11-N]

  [Wait for results]

  Finally: [synthesize all results from both batches]"
```

---

### Slide 20: Batch Execution Behavior and Guarantees

**Title:** What Happens During Parallel Execution

**Main Content:**
- **Execution guarantees**:
  - All agents start at approximately the same time (within milliseconds)
  - No inter-agent communication (each agent is isolated)
  - Output is collected only after agent completes
  - Agents cannot block each other

- **Timing characteristics**:
  ```
  If fastest agent takes 1 minute
  If slowest agent takes 5 minutes
  Total parallel time: ~5 minutes (slowest agent time)

  Not: 1 + 2 + 3 + 4 + 5 = 15 minutes (sequential)
  But: max(1, 2, 3, 4, 5) = 5 minutes (parallel)
  ```

- **Output collection**:
  - Results are presented in execution order
  - Usually: Fast agents finish first, appear first
  - System waits for slowest agent before considering batch complete
  - You cannot access partial results

- **Failure modes**:
  - If 1 agent fails, others continue (not blocked)
  - You get results from agents that succeeded
  - You must handle missing results in synthesis
  - No automatic retry of failed agents

- **State isolation**:
  ```
  Agent 1 creates file.txt
  Agent 2 doesn't see file.txt
  Agent 3 doesn't see file.txt

  Each agent has isolated working directory
  Files created by agents are lost after completion
  (unless explicitly returned as output)
  ```

**Batch Execution Flow:**
```
INPUT: Parallel request with N agents

SPAWN PHASE (milliseconds):
[Agent 1 starts] [Agent 2 starts] [Agent 3 starts] ... [Agent N starts]

EXECUTION PHASE:
[Agent 1 running...      ] (2 min)
[Agent 2 running...          ] (3 min)
[Agent 3 running...                ] (5 min)
[Agent 4 running... ] (1 min)

COLLECTION PHASE:
Agent 4 completes first (1 min) - output collected
Agent 1 completes (2 min) - output collected
Agent 2 completes (3 min) - output collected
Agent 3 completes (5 min) - output collected (now all done)

OUTPUT PHASE:
All 4 results available for synthesis
(Slowest agent determines total time: 5 min)
```

**Speaker Notes:**
This is important for student understanding: parallel execution time is determined by the slowest agent, not the sum. If you have agents that vary widely in execution time, consider whether you can rebalance work. For example, if one agent takes 2 minutes and another takes 10 minutes, they're not equally balanced. Help students think about workload distribution.

**Student Prompt Template:**
```
To understand execution timing:

My parallel tasks:
- Agent 1: [task] - estimated [N] min
- Agent 2: [task] - estimated [M] min
- Agent 3: [task] - estimated [K] min

Sequential time: [N + M + K] = [total] min
Parallel time: max([N], [M], [K]) = [total] min
Speedup: [sequential time] / [parallel time] = [factor]x

Expected parallel execution: ~[max time] minutes
```

---

### Slide 21: The run_in_background Parameter

**Title:** Background Execution for Long-Running Tasks

**Main Content:**
- **Background execution concept**:
  - Specify `run_in_background: true` for tasks that take > 5 minutes
  - Agent runs in background, you can do other work
  - Results retrieved asynchronously later
  - Useful for batch processing, large experiments

- **When to use run_in_background**:
  - Long data processing (> 10 minutes)
  - Extensive experimentation with many parameters
  - Building large projects
  - Running full test suites
  - Anything else you don't need immediately

- **When NOT to use**:
  - Tasks under 5 minutes (just wait)
  - Tasks you need for next step (blocks on retrieval anyway)
  - Interactive debugging (need immediate feedback)

- **Syntax**:
  ```
  "Run this agent in the background:

  Agent 1 - Long Processing Task:
  [description]
  [instructions]
  run_in_background: true

  [Other work happens here while agent runs]

  Task Complete: 'Retrieve results from Agent 1 background execution'"
  ```

- **Practical pattern**:
  ```
  Main flow:
  ├─ Start Agent 1 (long task) in background
  ├─ While Agent 1 runs:
  │  ├─ Agent 2: Quick analysis
  │  ├─ Agent 3: Documentation
  │  └─ Agent 4: Testing
  ├─ [Agent 1 completes in background]
  └─ Synthesis: Combine all results
  ```

**Background Execution Timeline:**
```
Sequential approach:
[Agent 1: Long task, 15 min] → [Agent 2: 5 min] → [Agent 3: 5 min]
TOTAL: 25 min (blocked waiting for Agent 1)

Background approach:
[Agent 1: Long task starts in background]
[Meanwhile, Agent 2 runs: 5 min]
[Meanwhile, Agent 3 runs: 5 min]
[Agent 1 still running... 10 min into its 15 min task]
[After Agents 2-3: Check Agent 1 status]
[Agent 1 completes: 15 min]
[Synthesis: 2 min]
TOTAL: 17 min (parallelized Agent 1 with Agents 2-3)
```

**Speaker Notes:**
Background execution is underutilized by students. It's perfect for starting long-running tasks and then doing other work. The key insight is that while one agent processes data, others can review code, write documentation, or run tests. This is how you get maximum utilization of your time and tokens.

**Student Prompt Template:**
```
For tasks with different durations:

Quick setup phase (parallel, ~3 min):
Agent 1: [quick task]
Agent 2: [quick task]

Long processing (background):
Agent 3: [long task - 10+ min]
run_in_background: true

While Agent 3 runs (parallel, ~5 min):
Agent 4: [medium task]
Agent 5: [medium task]

Final synthesis (after Agent 3 completes):
Agent 6: Combine all results including background Agent 3

Total time: ~5 + 10 = 15 min (vs 3 + 10 + 5 + 2 = 20 min sequential)
```

---

### Slide 22: Practical Prompt Templates for Parallelization

**Title:** Ready-to-Use Prompt Templates

**Main Content:**
- **Template 1: Basic 3-Agent Research**
  ```
  "Run these 3 agents in parallel:

  Agent 1 - Codebase Researcher:
  Explore [project name] and find all code related to [topic].

  Agent 2 - Literature Researcher:
  Search for papers and documentation about [topic].

  Agent 3 - Pattern Researcher:
  Find similar implementations in open source.

  After all complete, synthesize into a research report."
  ```

- **Template 2: Code Review Panel**
  ```
  "Review this code from 3 perspectives:

  Agent 1 - Correctness Reviewer:
  Look for logical errors, edge cases, off-by-one errors.

  Agent 2 - Style Reviewer:
  Look for readability, naming, structure issues.

  Agent 3 - Performance Reviewer:
  Look for efficiency, memory, algorithmic improvements.

  Consensus: What issues do 2+ reviewers agree on?"
  ```

- **Template 3: Parallel Experimentation**
  ```
  "Run these experiments in parallel with [base configuration]:

  Agent 1: Test with [variable]=[value1]
  Agent 2: Test with [variable]=[value2]
  Agent 3: Test with [variable]=[value3]

  Each should report: [metrics to measure]

  After all, compare and identify optimal [variable]."
  ```

- **Template 4: Multi-Format Documentation**
  ```
  "Generate documentation in 3 formats:

  Agent 1: Executive summary (1-2 pages, non-technical)
  Agent 2: Technical documentation (5-10 pages, detailed)
  Agent 3: API reference (comprehensive function list)

  Then combine into integrated documentation package."
  ```

- **Template 5: Parallel Data Processing**
  ```
  "Process these datasets in parallel:

  Agent 1: Clean and validate dataset A
  Agent 2: Clean and validate dataset B
  Agent 3: Clean and validate dataset C

  Each should report: [quality metrics]

  After all, combine into merged dataset."
  ```

**Speaker Notes:**
Give students these templates to copy and adapt. These are tested patterns that work well. The key is that students should have templates to start from rather than inventing from scratch. Show how each template follows the principles: explicit parallel request, clear role names, specific instructions for each agent, and synthesis step.

**Student Prompt Template:**
```
Adapt a template for your use case:

Template: [choose 1-5 above]
Customizations:
- Replace [topic] with: [your topic]
- Replace [variable] with: [your variable]
- Replace [value1/2/3] with: [your values]
- Agents: [adjust number if needed]

Full customized prompt:
[Copy template and apply replacements]
```

---

## Section 5: Parallelization in Other Tools (5-6 slides)

---

### Slide 23: Parallelization in Cursor

**Title:** How Cursor Implements Parallel Agents

**Main Content:**
- **Cursor's approach**: Built-in support for up to 8 parallel agents
  - Simpler than Claude Code (no syntax, happens automatically)
  - Triggered by phrases like "run in parallel" or "simultaneously"
  - Can spawn up to 8 agents without explicit batching

- **Syntax in Cursor**:
  ```
  "Do these in parallel:
  - [Task 1]
  - [Task 2]
  - [Task 3]"
  ```
  Cursor automatically spawns agents

- **Strengths**:
  - Simpler to use (less verbose syntax)
  - Built into IDE, integrated workflow
  - Automatic parallel detection
  - Visual feedback on parallel execution

- **Limitations**:
  - Only 8 agents max (vs Claude Code's 10)
  - Less control over agent specialization
  - Less flexible for complex workflows
  - No run_in_background parameter

- **Comparison with Claude Code**:
  | Feature | Claude Code | Cursor |
  |---------|------------|--------|
  | Max agents | 10 | 8 |
  | Explicit syntax | Yes (required) | No (automatic) |
  | Terminal integration | Native | Through IDE |
  | Flexibility | High | Medium |
  | Learning curve | Steeper | Shallower |

**Speaker Notes:**
Cursor is a GUI-based IDE that integrates AI agents. It's different from Claude Code's CLI-based approach. Students should understand that different tools have different strengths. Cursor's automatic parallelization is convenient but less explicit. Claude Code requires explicit syntax but gives more control.

**Student Prompt Template:**
```
In Cursor, parallel requests are simpler:

Instead of detailed roles:
"Run these in parallel:
1. [Task A]
2. [Task B]
3. [Task C]"

Cursor will:
1. Detect "parallel" keyword
2. Spawn agents automatically
3. Execute concurrently
4. Aggregate results

No need for role names or detailed instructions (though they help).
```

---

### Slide 24: Parallelization in Continue CLI

**Title:** Continue CLI's Async Agent Architecture

**Main Content:**
- **Continue CLI approach**: Asynchronous agent execution
  - Different from strict sync/parallel model
  - Agents can be spawned asynchronously (fire and forget)
  - Results collected whenever available
  - No hard limit on concurrent agents (rate limited)

- **Async execution model**:
  ```
  Spawn Agent 1 (async)
  Spawn Agent 2 (async)
  Spawn Agent 3 (async)
  [Agents run independently, don't block main thread]
  Main process continues
  [Check for results when needed]
  ```

- **Benefits**:
  - Highly scalable (unlimited agents conceptually)
  - Non-blocking execution
  - Efficient resource usage
  - Natural for distributed work

- **Challenges**:
  - Results come back at unpredictable times
  - Need to handle partial results
  - Synchronization is explicit (not implicit)
  - More complex for beginners

- **Syntax in Continue**:
  ```
  async {
    agent1.start(task1)
    agent2.start(task2)
    agent3.start(task3)

    results = [
      agent1.await(),
      agent2.await(),
      agent3.await()
    ]
  }
  ```

**Async Execution Timeline:**
```
Continue CLI (async):
[Agent 1 spawned]
[Agent 2 spawned]
[Agent 3 spawned]
[Main process continues immediately]
[Check for results in background]
[Results available as agents complete]

Can potentially run 50+ agents (with rate limiting)
Not blocked by slowest agent conceptually
Requires explicit synchronization points
```

**Speaker Notes:**
Continue CLI's async model is different—more like traditional parallel programming with threads. Students familiar with async/await will recognize the pattern. It's more flexible than strict parallel execution but requires more careful handling of synchronization and result aggregation.

**Student Prompt Template:**
```
For Continue CLI async execution:

"Spawn these agents asynchronously:

async {
  // Start agents without waiting
  task1 = agent1.start('[task A description]')
  task2 = agent2.start('[task B description]')
  task3 = agent3.start('[task C description]')

  // Other work can happen here

  // Wait for results when needed
  results = [
    task1.await(),
    task2.await(),
    task3.await()
  ]

  // Process results
  synthesize(results)
}"
```

---

### Slide 25: Container-Based Isolation and Resource Management

**Title:** How Tools Isolate Parallel Agents

**Main Content:**
- **Isolation mechanisms**:
  - Each agent runs in isolated process (or container)
  - No shared memory between agents
  - No file system sharing (unless explicitly passed)
  - No environment variable sharing
  - Clean state for each agent

- **Benefits of isolation**:
  - Agents can't interfere with each other
  - Failures don't cascade
  - Clean, predictable environments
  - Better error handling
  - Security boundaries

- **Implementation approaches**:
  - **Process isolation**: Separate OS processes (fastest)
  - **Container isolation**: Docker/OCI containers (more heavyweight)
  - **Virtual machine**: Full VM per agent (most isolated, slowest)
  - Most tools use process isolation for speed

- **Information passing**:
  - Between isolated agents: Only through explicit output
  - No shared variables or mutable state
  - Results serialized/deserialized between agents
  - Context window sent fresh to each agent

- **Resource limits per agent**:
  ```
  Memory: ~500MB per agent
  CPU: 1 core per agent (more if available)
  Time: 30-60 minute timeout per agent
  Tokens: Independent counter per agent
  Files: ~100MB workspace per agent
  ```

**Isolation Architecture:**
```
Main Process
├─ Agent 1 [Isolated Process]
│  ├─ Working directory
│  ├─ Memory space
│  └─ File system view
├─ Agent 2 [Isolated Process]
│  ├─ Working directory
│  ├─ Memory space
│  └─ File system view
├─ Agent 3 [Isolated Process]
│  ├─ Working directory
│  ├─ Memory space
│  └─ File system view
└─ Result Aggregator
   ├─ Collects output from all agents
   └─ Passes to synthesis step
```

**Speaker Notes:**
Isolation is what makes parallelization safe. Students should understand that agents can't interfere with each other because they run in isolated environments. This is both a feature (safety) and a limitation (can't share mutable state easily). Emphasize that sharing information between agents requires explicitly returning results.

**Student Prompt Template:**
```
To understand isolation in your parallel execution:

Agent 1:
├─ Gets: [input context]
├─ Uses: Isolated working directory and memory
├─ Creates: Files, variables, state (isolated)
└─ Returns: Explicit output only

Agent 2:
├─ Gets: [input context]
├─ Uses: Isolated working directory and memory
├─ Creates: Files, variables, state (isolated)
└─ Returns: Explicit output only

Synthesis Agent:
├─ Gets: Output from Agent 1 + Agent 2
├─ Cannot access: Agent 1/2 working directories or memory
└─ Uses: Only explicit outputs returned by each agent
```

---

## Section 6: Best Practices (6-8 slides)

---

### Slide 26: Independence Requirements for Parallelization

**Title:** When Tasks CAN Run in Parallel

**Main Content:**
- **True independence test**:
  ```
  Can Task B be completed without Task A's output?
  If YES → Can parallelize
  If NO → Must sequence (B depends on A)
  ```

- **Independent task checklist**:
  - [ ] Task A's output is NOT required by Task B
  - [ ] Task B's output is NOT required by Task A
  - [ ] Both tasks don't modify the same files
  - [ ] Order of execution doesn't matter
  - [ ] Results can be combined without conflicts
  - All TRUE → Can parallelize

- **Common parallelization mistakes**:
  ```
  MISTAKE: Trying to parallelize sequential dependencies

  "Parse data in parallel"
  Agent 1: Read file → Parse JSON
  Agent 2: Process parsed_data (but Agent 1 hasn't produced it!)

  CORRECT: Sequence explicitly
  Agent 1: "Read and parse data. Output parsed_data.json"
  [Wait for Agent 1]
  Agent 2: "Load parsed_data.json and process it"
  ```

- **Partial parallelization**:
  ```
  Phases that can parallelize:
  ├─ Phase 1: Independent read operations (all parallel)
  ├─ [Sync point: combine data]
  ├─ Phase 2: Independent analyses (all parallel)
  ├─ [Sync point: aggregate findings]
  └─ Phase 3: Sequential synthesis (must be sequential)
  ```

**Independence Verification Flowchart:**
```
Considering parallelizing Task A and Task B?

Does Task A output go into Task B input?
├─ YES → SEQUENTIAL (B depends on A)
└─ NO → Continue

Does Task B output go into Task A input?
├─ YES → SEQUENTIAL (A depends on B)
└─ NO → Continue

Do they modify the same file?
├─ YES → SEQUENTIAL (conflict)
└─ NO → Continue

Is there any other dependency?
├─ YES → SEQUENTIAL (unknown dependency)
└─ NO → PARALLELIZE! (truly independent)
```

**Speaker Notes:**
This is critical: improper parallelization (parallelizing dependent tasks) is a common error. Help students develop the habit of explicitly checking independence before parallelizing. Use the checklist approach to make it systematic rather than relying on intuition.

**Student Prompt Template:**
```
Independence check before parallelizing:

Task A: [description]
└─ Produces: [output type]

Task B: [description]
└─ Produces: [output type]

Dependency analysis:
1. Does A's output go into B? YES/NO
2. Does B's output go into A? YES/NO
3. Do they modify same files? YES/NO
4. Any other dependencies? YES/NO

Decision:
If all NO → PARALLELIZE
If any YES → SEQUENTIAL, order as [A → B] or [B → A]
```

---

### Slide 27: Specificity for Each Agent

**Title:** Clear Roles and Instructions

**Main Content:**
- **Good role naming**:
  ```
  VAGUE:
  - Agent 1, Agent 2, Agent 3 (meaningless)

  SPECIFIC:
  - Agent 1 - Correctness Reviewer
  - Agent 2 - Performance Analyzer
  - Agent 3 - Security Auditor
  ```

- **Clear task instructions**:
  ```
  VAGUE:
  "Analyze this code"
  (Too open-ended, agent might miss important aspects)

  SPECIFIC:
  "Review this code for security vulnerabilities.
  Look for SQL injection, buffer overflows, privilege escalation.
  Provide specific code locations and severity levels."
  ```

- **Expected output specification**:
  ```
  VAGUE:
  "Find bugs" → Agent produces long rambling report

  SPECIFIC:
  "Find bugs. Format as JSON with:
  {
    'bugs': [
      {'line': N, 'severity': 'HIGH/MEDIUM/LOW', 'description': '...'}
    ]
  }"
  → Agent produces structured, parseable output
  ```

- **Context provision**:
  - Be explicit about what each agent should focus on
  - Provide background information needed
  - Specify constraints or requirements
  - Example: "Focus on edge cases only, ignore happy path"

**Specificity Improvement Examples:**
```
CODE REVIEW EXAMPLE:

VAGUE:
"Review this code"

SPECIFIC:
"Review this implementation of quicksort for correctness.
Focus on:
1. Edge cases: empty arrays, single element, duplicates
2. Off-by-one errors in partition
3. Base case handling
4. Time/space complexity
Report each finding as: [LINE] [SEVERITY] [DESCRIPTION]"

RESULT: Specific agent produces precise, actionable findings
```

**Speaker Notes:**
Quality of parallel execution depends on specificity. Vague instructions lead to vague outputs that are hard to synthesize. Specific instructions lead to focused outputs that complement each other well. This is especially important when multiple agents work on the same problem from different angles.

**Student Prompt Template:**
```
To improve agent specificity:

Instead of:
"Agent 1: Analyze [topic]"

Write:
"Agent 1 - [Specific Role]:
Analyze [topic] specifically for [aspect].
Focus on: [key areas]
Consider: [important factors]
Report findings as: [format specification]
Output format: [JSON/CSV/structured format]"

Check: Is each agent's role and task completely clear?
If you handed this to a junior developer, could they do it?
```

---

### Slide 28: Background Task Usage Patterns

**Title:** When and How to Use run_in_background

**Main Content:**
- **Selection criteria**:
  ```
  If task takes > 8 minutes:
    └─ Consider run_in_background: true
  If task takes 5-8 minutes:
    └─ Maybe background (depends on what else you're doing)
  If task takes < 5 minutes:
    └─ Just wait, don't background
  ```

- **Pattern 1: Long processing + Quick analysis**
  ```
  Start long task in background:
  Agent 1: [Long processing task]
  run_in_background: true

  While Agent 1 runs, do quick work:
  Agent 2: [Quick analysis of results so far]
  Agent 3: [Prepare for synthesis]

  Then: Retrieve Agent 1 results and synthesize
  ```

- **Pattern 2: Multiple batches**
  ```
  Batch 1 (background):
  Agents 1-5: [Long tasks]
  run_in_background: true

  Batch 2 (meanwhile):
  Agents 6-8: [Other work]

  Synthesis (after both complete):
  Agent 9: Combine all results
  ```

- **Pattern 3: Progressive refinement**
  ```
  Phase 1: Start initial analysis in background
  Phase 2 (while Phase 1 runs): Quick review and planning
  Phase 3 (after Phase 1): Detailed deep-dive
  ```

**Background Execution Best Practices:**
```
DO:
✓ Start long-running tasks in background
✓ Do other work while waiting
✓ Check status periodically
✓ Plan synthesis phase in advance

DON'T:
✗ Use background for small tasks (< 5 min)
✗ Forget to retrieve background task results
✗ Start too many background tasks (memory)
✗ Wait for background tasks immediately (defeats purpose)
```

**Speaker Notes:**
Background execution is a time optimization technique. The principle is simple: start long work, do other work meanwhile, retrieve results later. Students often forget to use this, running long tasks synchronously when they could be running them in the background. Show concrete examples of how much time can be saved.

**Student Prompt Template:**
```
To use background execution effectively:

Analyze your workflow:
- Task A duration: [minutes]
- Task B duration: [minutes]
- Task C duration: [minutes]

If max(A,B,C) > 8 minutes:
  "Start Task [longest] in background
  run_in_background: true

  While it runs, do Tasks [others]:
  Agent 2: [Task B]
  Agent 3: [Task C]

  Then retrieve background results and synthesize"

Time saved: [sequential time] - [parallel time] = [saved] min
```

---

### Slide 29: Collecting and Synthesizing Results

**Title:** How to Combine Parallel Outputs

**Main Content:**
- **Synthesis approaches**:
  ```
  MERGE: Combine results into single output
  "All findings merged into one report"

  CONSENSUS: Look for agreement among agents
  "Where do 2+ agents agree? That's strong signal."

  COMPARE: Highlight differences
  "Where do agents disagree? That signals uncertainty."

  RANK: Order results by importance
  "Highest priority findings from all agents"
  ```

- **Synthesis templates**:
  ```
  Template 1: Merge findings
  "Combine the security findings from Agents 1-3.
  Remove duplicates. Sort by severity. Produce unified list."

  Template 2: Consensus analysis
  "These are findings from 3 agents.
  Which findings do 2+ agents agree on?
  Which are outliers?"

  Template 3: Comprehensive report
  "Synthesize the 3 agent outputs into a single comprehensive
  report with section for each aspect."
  ```

- **Handling contradictions**:
  ```
  If Agent 1 says: "This is a performance issue"
  If Agent 2 says: "This is not an issue"

  Action:
  "Agents 1 and 2 disagree about [issue].
  Agent 1 reasons: [reasoning]
  Agent 2 reasons: [reasoning]
  Who is more likely correct? Why?"
  ```

- **Deduplication**:
  ```
  Agent 1 finds: [Issue A, Issue B, Issue C]
  Agent 2 finds: [Issue B, Issue D]
  Agent 3 finds: [Issue A, Issue C, Issue E]

  Deduplicated: [Issue A, Issue B, Issue C, Issue D, Issue E]
  (remove exact duplicates while preserving unique findings)
  ```

**Synthesis Process Flow:**
```
Parallel Results Collection:
├─ Agent 1 output: [findings 1-5]
├─ Agent 2 output: [findings 3, 6-8]
├─ Agent 3 output: [findings 1, 4, 9-10]

Deduplication:
└─ Unique findings: [1-10]

Categorization:
├─ Security: [1, 6, 9]
├─ Performance: [2, 7]
└─ Style: [3, 4, 5, 8, 10]

Ranking:
├─ HIGH: [1, 6]
├─ MEDIUM: [2, 7, 9]
└─ LOW: [3, 4, 5, 8, 10]

Final Report:
HIGH severity findings, categorized, all unique findings included
```

**Speaker Notes:**
Synthesis is where the true value of parallelization emerges. Multiple agents provide different perspectives, and combining these perspectives intelligently produces better results than any single agent. Teach students to be intentional about synthesis strategy rather than just concatenating outputs.

**Student Prompt Template:**
```
To synthesize parallel results:

"Here are outputs from [N] agents:

Agent 1: [findings/results summary]
Agent 2: [findings/results summary]
Agent 3: [findings/results summary]

Please synthesize:
1. Deduplicate: Remove exact duplicates
2. Analyze consensus: Where do 2+ agents agree?
3. Identify outliers: Which findings are unique?
4. Rank: What's most important?
5. Format: Present as [JSON/report/list/other]

Final output should: [synthesis goal]"
```

---

### Slide 30: Monitoring Token Usage in Parallel Execution

**Title:** Token Economics of Parallelization

**Main Content:**
- **Token cost model**:
  ```
  Single agent task:
  Input tokens: 2,000
  Output tokens: 1,000
  Total: 3,000 tokens

  Same task with 3 parallel agents:
  Input tokens: 2,000 × 3 = 6,000 (duplicated context)
  Output tokens: 1,000 × 3 = 3,000
  Total: 9,000 tokens

  Cost multiplier: 3x tokens
  Time benefit: ~50% faster
  ```

- **Cost-benefit analysis**:
  ```
  Token cost: 9,000 - 3,000 = 6,000 extra tokens
  Time saving: 10 min → 5 min = 5 minutes saved

  Is 6,000 tokens worth 5 minutes?
  Depends on:
  - Your token budget
  - Value of 5 minutes of your time
  - Quality improvement from multiple perspectives
  ```

- **Monitoring strategies**:
  - Track tokens before and after parallelization
  - Calculate actual speedup achieved
  - Measure quality improvement (bug-finding, coverage)
  - Compare cost/benefit over time

- **Optimization techniques**:
  ```
  To reduce token cost of parallelization:

  1. Context compression:
     "Here's the essential info: [compressed context]"

  2. Focus narrowing:
     "Focus only on [specific aspect], ignore other details"

  3. Smaller models:
     Use Haiku for parallel tasks, Opus for synthesis

  4. Deduplication:
     "Don't repeat findings from other agents"
  ```

- **Token budgeting**:
  ```
  Monthly budget: 1,000,000 tokens

  Parallelization decision matrix:
  If 1 agent: 10,000 tokens, 20 min
  If 3 agents: 30,000 tokens, 8 min
  Speedup: 2.5x faster, 3x tokens

  Budget impact: 30,000 / 1,000,000 = 3% of monthly budget
  Worth it? Usually YES for 2.5x speedup
  ```

**Token Usage Visualization:**
```
Cost vs Time Trade-off

Parallel Cost: 30,000 tokens
│
│     ○ Parallel (high cost, low time)
│    ╱│
│   ╱ │ ← Better if time > cost
│  ╱  │
│ ╱   │
├─────┼────────→ Time (minutes)
│     │
│     ○ Sequential (low cost, high time)
│
Total Token Cost (thousands)
```

**Speaker Notes:**
Help students develop token awareness. Parallelization isn't free, and students should consciously make the trade-off decision. For most research and debugging tasks, the trade-off is favorable. For routine tasks or when token budget is tight, sequential might be better. Teach the mental model: more tokens for less time.

**Student Prompt Template:**
```
Token cost analysis for parallelization:

Task: [description]

Sequential approach:
- Agents: 1
- Tokens per agent: ~[estimate]
- Time: ~[minutes]
- Total tokens: ~[estimate]

Parallel approach (N agents):
- Agents: [N]
- Tokens per agent: ~[estimate] (may be less if context compressed)
- Time: ~[estimate]
- Total tokens: ~[estimate]

Cost-benefit:
- Token increase: [parallel] - [sequential] = [delta]
- Time decrease: [sequential] - [parallel] = [saved] min
- Quality improvement: [describe expected]

Decision: Parallelize if [time value + quality value] > [token cost]
```

---

### Slide 31: Debugging Parallel Execution

**Title:** Finding and Fixing Problems in Parallel Tasks

**Main Content:**
- **Common parallel execution issues**:
  1. **One agent fails, others succeed**
    - Check: Did you expect consensus?
    - Fix: Use fallback to sequential or re-run single agent

  2. **Results are inconsistent**
    - Check: Are agents receiving identical context?
    - Fix: Verify input is same for all agents

  3. **Timeout on slowest agent**
    - Check: Can work be rebalanced?
    - Fix: Move some work from slow to fast agents

  4. **Synthesis can't handle outputs**
    - Check: Did agents output in expected format?
    - Fix: Specify output format in agent instructions

  5. **Quality is worse than sequential**
    - Check: Are instructions too vague?
    - Fix: Make instructions more specific per agent

- **Debugging workflow**:
  ```
  Step 1: Run parallel version, note results
  Step 2: Run sequential version of same work
  Step 3: Compare outputs
    - Are they similar? (parallelization works)
    - Are they different? (something wrong)
  Step 4: Identify which agent produced wrong output
  Step 5: Re-run that agent with improved instructions
  ```

- **Logging and monitoring**:
  ```
  For each agent, log:
  - Start time and end time
  - Tokens used
  - Output size
  - Any error messages
  - Quality metrics if applicable

  Compare across agents to identify outliers
  ```

- **Validation checklist**:
  - [ ] All agents completed successfully
  - [ ] Outputs are in expected format
  - [ ] Outputs are non-empty and meaningful
  - [ ] Synthesis step produces valid result
  - [ ] Result quality matches or exceeds sequential
  - [ ] Token cost is justified by time saving

**Debugging Decision Tree:**
```
Parallel execution failed or produced poor results?

Did all agents complete?
├─ NO: Agent timeout or crash
│  └─ Split work differently or re-run failed agent
└─ YES: All completed, continue

Are outputs in expected format?
├─ NO: Agents didn't follow format instructions
│  └─ Re-run with clearer output format specification
└─ YES: Continue

Is synthesis step failing?
├─ YES: Outputs don't match synthesis expectations
│  └─ Check if agents actually answered the right question
└─ NO: Continue

Is quality worse than sequential?
├─ YES: Parallelization isn't helping
│  └─ Agents might be conflicting; use sequential instead
└─ NO: Success!

Compare parallel tokens vs sequential tokens:
├─ Parallel much more expensive?
│  └─ Consider compression or sequential for cost savings
└─ Tokens acceptable?
   └─ Parallelization is working!
```

**Speaker Notes:**
Debugging parallel execution is different from debugging sequential code. The key insight is comparison: parallel execution often makes sense only when compared to sequential. Show students how to systematically debug by isolating which agent is problematic and fixing just that one.

**Student Prompt Template:**
```
Debugging parallel execution:

Symptom: [describe what went wrong]

Diagnosis steps:
1. Re-run sequentially: [run same work with 1 agent]
2. Compare outputs: [sequential output] vs [parallel outputs]
3. Identify problematic agent: [which agent output differs?]
4. Analyze agent instructions: [does Agent X instructions match output?]

Hypothesis: [what went wrong?]

Fix: [specific change to instructions or approach]

Re-run parallel with fix and verify quality improvement
```

---

### Slide 32: Integration with Your Development Process

**Title:** Making Parallelization Part of Your Workflow

**Main Content:**
- **When to introduce parallelization**:
  - Early in projects: Research phase (highly parallelizable)
  - Middle: Implementation (some parallelization)
  - Late: Testing and refinement (moderate parallelization)

- **Project phases and parallelization intensity**:
  ```
  Research Phase: ████████████ (heavy parallelization)
  Design Phase: ████████░░░░ (moderate parallelization)
  Implementation: ████░░░░░░░░ (light-moderate parallelization)
  Testing: ██████░░░░░░ (moderate parallelization)
  Refinement: ██░░░░░░░░░░ (light parallelization)
  ```

- **Parallelization checklist for each task**:
  ```
  Before starting any task, ask:
  1. Can this be decomposed into independent subtasks?
  2. Will parallelization save meaningful time?
  3. Do I have token budget for parallelization?
  4. Would multiple perspectives improve quality?

  If 3+ answers are YES: Parallelize
  If 2 or fewer: Consider sequential
  ```

- **Documentation and planning**:
  - Document which tasks you parallelize and why
  - Track token cost vs time saved
  - Build library of working patterns
  - Share successful patterns with team

**Workflow Integration Example:**
```
Project: Implement new feature

Research Phase (HEAVILY PARALLEL):
├─ 3 agents: code exploration, literature search, pattern finding
├─ Tokens: ~25,000
├─ Time: 10 min (vs 25 min sequential)
└─ Value: High quality research, consensus on approach

Design Phase (MODERATE PARALLEL):
├─ 2 agents: architecture design, feasibility analysis
├─ Tokens: ~15,000
├─ Time: 8 min (vs 12 min sequential)
└─ Value: Two perspectives on design

Implementation Phase (LIGHT PARALLEL):
├─ Sequential mostly (tight dependencies)
├─ Parallel where possible (independent modules)
├─ Tokens: ~30,000 (similar to sequential)
├─ Time: 15 min (vs 18 min sequential)
└─ Value: Modest time saving, less quality impact

Testing Phase (MODERATE PARALLEL):
├─ 3 agents: unit tests, integration tests, perf tests
├─ Tokens: ~20,000
├─ Time: 5 min (vs 15 min sequential)
└─ Value: High parallelizability, significant speedup

TOTAL:
Parallel: 38 min total time, ~90,000 tokens
Sequential: 70 min total time, ~50,000 tokens
Trade-off: 45% faster, 1.8x tokens
```

**Speaker Notes:**
Help students see parallelization as integrated into their overall development process, not as a separate technique. As they build experience, they'll naturally recognize parallelizable opportunities. The key is being intentional about the decision rather than defaulting to sequential.

**Student Prompt Template:**
```
Planning parallelization for your project:

Project: [name]
Timeline: [duration]

For each phase, analyze:
Phase: [name]
├─ Duration: [minutes]
├─ Can decompose into independent subtasks? YES/NO
├─ If YES, how many subtasks? [N]
├─ Estimated parallel time: [N × longest subtask]
├─ Time saved: [sequential] - [parallel] = [saved]
├─ Token cost multiplier: [N]
└─ Decision: [PARALLELIZE / SEQUENTIAL]

Build parallelization plan covering all phases
```

---

## Advanced Considerations and Edge Cases

---

### Slide 33: Handling Large-Scale Parallelization

**Title:** Scaling Beyond 10 Agents

**Main Content:**
- **When you need more than 10 agents**:
  - Large experiments with many parameter values
  - Big data processing with multiple datasets
  - Comprehensive code analysis across large codebases
  - Extensive testing suite with many test categories

- **Batching strategy**:
  ```
  Need 25 agents? Use 3 batches:

  Batch 1: Agents 1-10
  [Wait for completion]
  [Aggregate results]

  Batch 2: Agents 11-20
  [Wait for completion]
  [Aggregate results]

  Batch 3: Agents 21-25
  [Wait for completion]
  [Aggregate results]

  Final synthesis: Combine all batch results
  ```

- **Batch management**:
  - Track results per batch
  - Number batches clearly (Batch 1, Batch 2, etc.)
  - Aggregate before next batch
  - Final synthesis combines all batches

- **Resource considerations**:
  - Running 10 concurrent agents is resource-intensive
  - Space agents across batches rather than cramming 20 into 2 batches
  - Each batch completes cleanly before next starts
  - Memory is fully freed between batches

- **Latency optimization**:
  ```
  Slow (sequential batches):
  [Batch 1: 5 min] [Batch 2: 5 min] [Batch 3: 5 min] [Synthesis: 2 min]
  TOTAL: 17 min

  Fast (parallel where possible):
  [Batch 1: 5 min] [Batch 2: 5 min, start background]
  [Then immediately start Batch 3 while Batch 2 runs]
  [Synthesis: 2 min]
  TOTAL: ~12 min

  Note: Only possible if Batch 3 doesn't depend on Batch 2
  ```

**Large-Scale Experiment Batching:**
```
Experiment: Test 30 different model configurations

Naive approach (fails):
"Run 30 agents in parallel" → ERROR (exceeds limit of 10)

Correct approach:

BATCH 1 (Agents 1-10):
- Agent 1: Config set A parameters (A1-A10)
- Agent 2: Config set B parameters (B1-B10)
- ...
- Agent 10: Config set J parameters (J1-J10)

[Collect results]

BATCH 2 (Agents 11-20):
- Agent 11: Config set K parameters (K1-K10)
- ...
- Agent 20: Config set T parameters (T1-T10)

[Collect results]

BATCH 3 (Agents 21-30):
- Agent 21: Config set U parameters (U1-U10)
- ...
- Agent 30: Config set (complete set of 30 configs)

[Collect results]

Final: Aggregate all 30 results and compare
```

**Speaker Notes:**
Large-scale parallelization requires thinking in batches. The key insight is that you can batch sequentially (one batch after another) or batch intelligently (overlap where possible). Teaching batching strategy empowers students to scale beyond the 10-agent limit naturally.

**Student Prompt Template:**
```
For more than 10 parallel tasks:

Total tasks: [N]
Max concurrent agents: 10

Batch size strategy:
- If tasks are dependent: Sequential batches [recommended]
- If tasks are independent: Can overlap batches

Batch plan:
Batch 1 (agents 1-10): [task description] [time: ~T1]
Batch 2 (agents 11-20): [task description] [time: ~T2]
[Continue batching]

Total time: Sum of batch times = [T1 + T2 + ...] minutes
(No parallelism between batches unless tasks permit)

Aggregation strategy:
[How to combine results from all batches]
```

---

### Slide 34: Error Recovery and Fault Tolerance

**Title:** Advanced Error Handling in Parallel Systems

**Main Content:**
- **Fault tolerance levels**:
  ```
  Level 1 (NONE): One agent fails → Entire task fails
  Level 2 (PARTIAL): One agent fails → Use results from others
  Level 3 (FULL): One agent fails → Retry or use backup
  ```

- **Redundancy pattern**:
  ```
  For critical task, run on N agents:

  N=1: No tolerance, fails if agent has issue
  N=2: Can continue if 1 agent agrees
  N=3: Can continue even if 1 agent fails
  N=5: Can tolerate up to 2 agent failures

  Rule: Need ceil((F+1)*2) agents to tolerate F failures
  ```

- **Consensus-based recovery**:
  ```
  Task results from 5 agents:
  ✓ Agent 1: Result A
  ✓ Agent 2: Result A
  ✗ Agent 3: Timeout
  ✓ Agent 4: Result A
  ✓ Agent 5: Result A

  Action: 4/5 agree on Result A
  Decision: Use Result A (1 failure acceptable)
  ```

- **Adaptive retry**:
  ```
  If critical agent fails:
  1. Log the failure
  2. Retry same agent with same input
  3. If fails again, retry with different instructions
  4. If still fails, mark as unrecoverable
  ```

- **Fallback strategies**:
  ```
  Parallel approach fails (timeout, crash):
  ├─ Fallback 1: Retry parallel with timeout extension
  ├─ Fallback 2: Run sequential version
  ├─ Fallback 3: Use last known good results
  ├─ Fallback 4: Manual intervention
  └─ Fallback 5: Skip this task, continue with others
  ```

**Fault Tolerance Decision Tree:**
```
Task criticality assessment:

Is failure acceptable?
├─ YES (low importance):
│  └─ Run 1 agent, fallback to sequential
├─ NO (medium importance):
│  └─ Run 2-3 agents, require consensus
└─ CRITICAL (cannot fail):
   └─ Run 5 agents, tolerate 2 failures

For each level, implement appropriate retry/fallback logic
```

**Speaker Notes:**
Fault tolerance is important when running production workflows. Research tasks can be more tolerant of failures. Production systems need higher reliability. Help students think about what "failure" means for their task and plan appropriately.

**Student Prompt Template:**
```
Fault tolerance planning for [task]:

Task importance: [LOW/MEDIUM/HIGH/CRITICAL]

Failure modes:
1. [Agent timeout]
2. [Agent crash]
3. [Invalid output]

For each failure mode:
├─ Probability: [estimate]
├─ Impact: [describe impact]
└─ Response: [recovery action]

Fault tolerance level to implement:
├─ LOW: Single agent, no redundancy
├─ MEDIUM: 2-3 agents, majority vote
├─ HIGH: 5 agents, tolerate 2 failures

Fallback chain:
1. [Primary: parallel with redundancy]
2. [Fallback: sequential single agent]
3. [Fallback: manual review]
4. [Fallback: skip and continue]
```

---

### Slide 35: Performance Profiling and Optimization

**Title:** Measuring and Optimizing Parallel Execution

**Main Content:**
- **Key metrics to track**:
  - **Wall-clock time**: Total elapsed time
  - **Token usage**: Total tokens consumed
  - **Cost-per-minute-saved**: Tokens / time_saved
  - **Quality score**: Bugs found, coverage, etc.
  - **Agent utilization**: What % of max concurrent agents used

- **Profiling template**:
  ```
  Task: [name]
  Date: [date]

  Sequential execution:
  - Time: [minutes]
  - Tokens: [count]
  - Quality score: [score]

  Parallel execution (N agents):
  - Time: [minutes]
  - Tokens: [count]
  - Quality score: [score]

  Metrics:
  - Speedup: [sequential_time / parallel_time]x
  - Token multiplier: [parallel_tokens / sequential_tokens]x
  - Cost per minute saved: [extra_tokens / time_saved]
  - Quality improvement: [quality_improvement]%
  ```

- **Optimization opportunities**:
  - **Reduce context size**: Compress input for parallel agents
  - **Change agent model**: Use Haiku for parallel, Opus for synthesis
  - **Rebalance work**: If one agent takes much longer, reassign work
  - **Adjust agent count**: Maybe 3 agents better than 5?

- **Profiling over time**:
  ```
  Track parallelization effectiveness across projects:

  Project 1: Speedup 1.5x, tokens 2.0x
  Project 2: Speedup 2.1x, tokens 2.8x
  Project 3: Speedup 1.2x, tokens 1.5x

  Patterns: Which types of tasks parallelize best?
  Answer: Data processing (2.1x) > Code analysis (1.5x) > Writing (1.2x)
  ```

- **ROI calculation**:
  ```
  Time saved: [minutes]
  Hourly rate: $[rate]
  Value of time saved: [minutes] / 60 * [rate] = $[value]

  Extra tokens: [count]
  Token cost: $[cost per million]
  Token cost: [count] / 1,000,000 * [cost per million] = $[token_cost]

  Net ROI: [value] - [token_cost] = $[net]
  Positive: Parallelization was worth it
  ```

**Performance Dashboard:**
```
Parallelization Effectiveness Over Time

                   Speedup (factor)
                   2.0x ┐
                        │     ✓ ✓
                   1.5x ├─────●────
                        │   ●   ●
                   1.0x └────────────
                        Project 1-5

          Tokens × (0-5 range)
                   5.0x ┐
                        │
                   3.0x ├───●───────
                        │     ● ●
                   1.0x └──●─────●──
                        Project 1-5

         ROI Positive?
                        ✓ ✓ ✓ ✓ ✗
                        1 2 3 4 5
```

**Speaker Notes:**
Encourage students to profile their parallelization efforts. This data drives future decisions. Over time, they'll see patterns: which task types parallelize well, which don't. This empirical data is more valuable than general guidelines.

**Student Prompt Template:**
```
Profile your parallelization effort:

Task: [name]

BASELINE (sequential):
- Time: [measure]
- Tokens: [measure]
- Quality: [measure]

PARALLEL (N agents):
- Time: [measure]
- Tokens: [measure]
- Quality: [measure]

Analysis:
- Speedup: [calculate]
- Token cost: [calculate]
- Cost per minute saved: [calculate]
- Quality improvement: [calculate]
- Was parallelization worth it? YES/NO

If NO, identify:
- What could be improved?
- Would different N help?
- Is this task type bad for parallelization?
```

---

## Conclusion and Summary

---

### Slide 36: Key Takeaways

**Title:** Essential Concepts for Parallelization

**Main Content:**
1. **Independence is Everything**
   - Parallelize only truly independent tasks
   - If B needs A's output, must run sequentially
   - Always verify before attempting parallelization

2. **Explicit is Better**
   - Use clear "run in parallel" language
   - Give each agent a specific role and instructions
   - Specify expected output format
   - Clarity compounds across agents

3. **Cost-Benefit Analysis**
   - Parallelization isn't free (3x tokens for 3 agents)
   - Worth it when time saved > token cost
   - Different tasks have different ROI
   - Profile your parallelization to learn patterns

4. **Synchronization Matters**
   - Implicit sync barriers after parallel phases
   - Plan synthesis step carefully
   - Multiple perspectives improve quality through consensus
   - Deduplication of results is important step

5. **Scale Pragmatically**
   - 3-5 parallel agents is usually optimal
   - Use batching for larger tasks (beyond 10)
   - More agents = exponentially higher resource use
   - Sometimes sequential is better

6. **Integration with Workflow**
   - Research: Heavily parallelize (3-5 agents)
   - Implementation: Selectively parallelize (independent modules)
   - Testing: Moderately parallelize (independent test suites)
   - Refactoring: Sequential only (consistency critical)

**Speaker Notes:**
Review these key takeaways. Students should internalize that parallelization is a tool to be used judiciously, not applied everywhere. The decision to parallelize should be based on task analysis, not habit. Emphasize that learning to recognize parallelizable patterns comes with experience.

---

### Slide 37: Common Pitfalls and How to Avoid Them

**Title:** Mistakes to Watch For

**Main Content:**
- **Pitfall 1: Parallelizing dependent tasks**
  ```
  ✗ WRONG: "Parse data in parallel with processing"
           (Processing depends on parsing output)
  ✓ CORRECT: "Parse first, then process in parallel with analysis"
  ```

- **Pitfall 2: Vague agent instructions**
  ```
  ✗ WRONG: Agent 1: "Analyze code"
  ✓ CORRECT: Agent 1 - Security Auditor: "Look for SQL injection,
             buffer overflows, privilege escalation"
  ```

- **Pitfall 3: Ignoring token cost**
  ```
  ✗ WRONG: Always parallelize for speed
  ✓ CORRECT: Parallelize only if token cost < time value
  ```

- **Pitfall 4: No synthesis plan**
  ```
  ✗ WRONG: Run 3 agents in parallel, no plan for combining results
  ✓ CORRECT: Plan synthesis step explicitly
  ```

- **Pitfall 5: Expecting perfect consensus**
  ```
  ✗ WRONG: Assume all agents will produce identical results
  ✓ CORRECT: Expect differences, look for patterns and majority view
  ```

- **Pitfall 6: Overloading agents**
  ```
  ✗ WRONG: Agent 1: "Do [10 unrelated tasks]"
  ✓ CORRECT: Agent 1: "Do [specific focused task]"
  ```

- **Pitfall 7: Not validating results**
  ```
  ✗ WRONG: Accept parallel results without checking
  ✓ CORRECT: Validate outputs, compare to sequential baseline
  ```

- **Pitfall 8: Memory/resource exhaustion**
  ```
  ✗ WRONG: Attempt 20 parallel agents on system with 4GB RAM
  ✓ CORRECT: Monitor resources, stick to 3-5 agents for stability
  ```

**Avoidance Strategies:**
```
Before parallelizing, run through checklist:
☐ Tasks are truly independent (no data dependencies)
☐ Time savings justify token cost
☐ Each agent has focused, specific role
☐ Expected outputs are well-defined
☐ Synthesis strategy is planned
☐ System has resources for N parallel agents
☐ Results will be validated
☐ If only 1-2 are true, reconsider parallelization
```

**Speaker Notes:**
These are the mistakes I see repeatedly. Help students internalize the checklist and develop a habit of going through it before parallelizing. Most parallelization failures come from one of these pitfalls.

---

### Slide 38: When Parallelization Doesn't Help

**Title:** Sequential Execution is Sometimes Better

**Main Content:**
- **Refactoring and code cleanup**:
  - Must be sequential for consistency
  - Multiple agents might introduce conflicts
  - Single agent maintains coherent style

- **Tight architectural integration**:
  - Implementation of tightly coupled modules
  - Each module depends on previous
  - No independent subtasks

- **Quick tasks (< 5 minutes)**:
  - Overhead of parallelization > time saved
  - Better to just run sequentially
  - Token cost not justified

- **Highly uncertain domains**:
  - When you don't know what you're looking for
  - Sequential exploration more efficient
  - Can adapt based on findings
  - Parallel agents might explore irrelevant directions

- **Token-budget limited projects**:
  - Every token counts
  - Parallelization multiplies token usage
  - Sequential single agent more efficient
  - Accept longer time for lower cost

- **Single-expert domains**:
  - When you need one specific expert
  - Multiple agents add noise
  - Expert single agent better
  - Example: Highly specialized language syntax

**Decision Matrix: Sequential vs Parallel**

```
                  Sequential | Parallel
Execution time    Longer     | Shorter
Token cost        Lower      | Higher
Parallelizability Low        | High
Dependency        High       | Low
Quality need      Consistency| Thoroughness
Budget sensitivity High      | Low
Expertise req.    Specific   | Broad

Choose SEQUENTIAL if: High dependency, tight budget, consistency critical
Choose PARALLEL if: Independent tasks, ample budget, thoroughness desired
```

**Speaker Notes:**
Balance the teaching—parallelization is powerful but not always right. Sometimes sequential is better. Help students develop the judgment to recognize which approach fits their situation. The best engineers know when NOT to parallelize as well as when TO parallelize.

---

### Slide 39: Building Your Parallelization Intuition

**Title:** Developing Skill with Experience

**Main Content:**
- **Start simple**:
  - Master 3-agent patterns first (research, review, analysis)
  - Avoid complex 10-agent batching initially
  - Build intuition gradually

- **Document everything**:
  - Write down tasks you parallelize
  - Record outcomes (time, tokens, quality)
  - Build personal knowledge base
  - Refer back to what worked

- **Experiment systematically**:
  - Try parallelizing a task
  - Compare to sequential baseline
  - Document the difference
  - Adjust approach based on results

- **Pattern recognition**:
  - Notice patterns in parallelizable tasks
  - Build library of working prompts
  - Adapt patterns to new contexts
  - Share patterns with others

- **Mentorship and learning**:
  - Learn from others' parallelization patterns
  - Share your findings
  - Discuss edge cases
  - Build community knowledge

- **Continuous improvement**:
  ```
  Cycle:
  Try → Measure → Learn → Apply → Repeat

  Session 1: Try parallelization, it works 60%
  Session 2: Apply lessons, it works 75%
  Session 3: Refine patterns, it works 85%
  Session 4+: Expert level (90%+ success rate)
  ```

**Development Path:**
```
Beginner (Sessions 1-5):
└─ Understand basic 3-agent patterns
  └─ Success with simple research/review tasks
    └─ Token-aware but not optimized

Intermediate (Sessions 6-20):
└─ Parallelize moderate complexity (6-8 agents)
  └─ Use batching for larger problems
    └─ Token optimization for cost efficiency

Advanced (Sessions 20+):
└─ Recognize parallelizable patterns instantly
  └─ Optimize for specific use cases
    └─ Build custom parallel patterns
      └─ Mentor others on parallelization
```

**Speaker Notes:**
Emphasize that skill development takes time and practice. Nobody becomes proficient with parallelization in one session. Each project teaches lessons. Over a semester/year of projects, students will develop strong intuition. Encourage them to document their learning and refer back to it.

---

### Slide 40: Next Steps and Further Learning

**Title:** Your Path Forward with Parallelization

**Main Content:**
- **Immediate next steps**:
  1. Identify a task in your current project suitable for parallelization
  2. Write the parallel request using templates from Slide 22
  3. Run it and measure results (time, tokens, quality)
  4. Document what you learned
  5. Apply the lesson to similar tasks

- **Short-term goals (next 2-3 weeks)**:
  - Master the 3-agent research pattern
  - Master the 3-agent code review pattern
  - Use parallelization in at least 5 distinct tasks
  - Build a personal template library
  - Track token cost vs time saved for each

- **Medium-term goals (next 1-2 months)**:
  - Recognize parallelizable patterns automatically
  - Implement complex patterns (6-8 agents, batching)
  - Optimize for your specific workflow
  - Mentor teammates on parallelization
  - Measure ROI systematically

- **Long-term goals (ongoing)**:
  - Become expert in parallelization patterns
  - Apply to increasingly complex problems
  - Develop domain-specific patterns
  - Contribute to agentic tool improvements
  - Teach others what you've learned

- **Resources for continued learning**:
  - Study parallel patterns in research and production
  - Review documentation of parallelization tools
  - Experiment with advanced patterns
  - Join communities discussing agentic AI
  - Read papers on multi-agent systems

- **Questions to explore**:
  ```
  What types of tasks parallelize best in your domain?
  What's the optimal team size for your work? (3, 5, 8?)
  How do you measure quality improvements from parallelization?
  What are the edge cases in your field?
  How could parallelization change the way you work?
  ```

**Progressive Skill Building:**
```
Session 1: Understand concepts, run first parallel task
├─ Resources: This slideshow, basic templates
└─ Goal: Run one successful parallel task

Sessions 2-5: Apply to multiple tasks
├─ Resources: Template library, documentation
└─ Goal: 5 successful parallel executions

Sessions 6+: Master and optimize
├─ Resources: Own experience, community patterns
└─ Goal: Expert proficiency, mentoring others
```

**Speaker Notes:**
End on an optimistic note. Parallelization is a learnable skill. Students who apply these concepts consistently will quickly become proficient. The key is starting simple, documenting results, and building gradually. Encourage them to reach out with questions as they learn and to share their discoveries with classmates.

---

## Appendix: Quick Reference Guides

---

### Appendix A: Parallel Request Templates (Quick Reference)

**Title:** Ready-to-Use Templates

**Content:**
```
TEMPLATE 1: THREE-AGENT RESEARCH
"Run these 3 agents in parallel:

Agent 1 - Codebase Explorer:
Explore [PROJECT] codebase for [TOPIC].

Agent 2 - Literature Researcher:
Search academic papers and docs for [TOPIC].

Agent 3 - Pattern Identifier:
Find similar implementations for [TOPIC].

After completion, synthesize into research report."

---

TEMPLATE 2: CODE REVIEW PANEL
"Review this code from 3 angles:

Agent 1 - Correctness: Check logic, edge cases, errors.
Agent 2 - Style: Check readability, naming, structure.
Agent 3 - Performance: Check efficiency, resources, algorithms.

After all agents, identify issues 2+ reviewers agree on."

---

TEMPLATE 3: PARALLEL EXPERIMENTS
"Run these experiments in parallel:

Agent 1: [PARAMETER=VALUE1] → Report [METRICS]
Agent 2: [PARAMETER=VALUE2] → Report [METRICS]
Agent 3: [PARAMETER=VALUE3] → Report [METRICS]

After completion, compare and identify optimal."

---

TEMPLATE 4: DOCUMENTATION GENERATION
"Generate documentation in 3 formats:

Agent 1: Executive summary (1-2 pages)
Agent 2: Technical guide (5-10 pages)
Agent 3: API reference (comprehensive)

After completion, combine into single document."

---

TEMPLATE 5: PARALLEL DATA PROCESSING
"Process datasets in parallel:

Agent 1: Clean and validate DATASET_A → Report quality
Agent 2: Clean and validate DATASET_B → Report quality
Agent 3: Clean and validate DATASET_C → Report quality

After completion, merge into unified dataset."
```

---

### Appendix B: Troubleshooting Guide

**Title:** Common Problems and Solutions

**Content:**
```
PROBLEM: One agent times out while others complete
CAUSE: Unbalanced workload distribution
FIX: Redistribute work more evenly across agents

PROBLEM: Results are contradictory
CAUSE: Agents interpreted task differently
FIX: Make instructions more specific, add examples

PROBLEM: Synthesis can't combine outputs
CAUSE: Output format not specified
FIX: Specify exactly what format each agent should use

PROBLEM: Quality is worse than single agent
CAUSE: Vague instructions leading to unfocused work
FIX: Give each agent specific, focused role

PROBLEM: Token cost is too high
CAUSE: Too many agents or redundant context
FIX: Reduce agent count or compress context

PROBLEM: Parallelization slower than sequential
CAUSE: Overhead exceeds time savings
FIX: Use sequential for small tasks (< 5 min)

PROBLEM: Some agents produce empty output
CAUSE: Agent failed silently or misunderstood task
FIX: Make task requirements explicit, add validation

PROBLEM: Results are inconsistent across runs
CAUSE: Non-deterministic agent behavior
FIX: Seed random processes, specify constraints
```

---

### Appendix C: Metric Calculation Formulas

**Title:** Quantifying Parallelization Benefits

**Content:**
```
SPEEDUP = Sequential_Time / Parallel_Time
          (Higher is better, minimum 1.0)

TOKEN_MULTIPLIER = Parallel_Tokens / Sequential_Tokens
                  (Lower is better, minimum 1.0)

COST_PER_MINUTE = (Parallel_Tokens - Sequential_Tokens) / Time_Saved
                 (Lower is better)

QUALITY_IMPROVEMENT = (Parallel_Quality - Sequential_Quality) / Sequential_Quality × 100%
                     (Higher is better)

ROI = Time_Value - Token_Cost
      (Positive is good)
      where:
      Time_Value = Minutes_Saved / 60 × Hourly_Rate
      Token_Cost = Extra_Tokens / 1,000,000 × Cost_Per_Million

EFFICIENCY = Speedup / Token_Multiplier
            (Higher means better speedup for token cost)

PARALLELIZATION_WORTH_IT_IF:
  (Speedup > 1.3) AND (Token_Multiplier < 3)
  OR Quality_Improvement > 20%
```

---

### Appendix D: Decision Flowchart

**Title:** Should I Parallelize This Task?

```
START: Considering task for parallelization

┌─ Can task be decomposed into independent subtasks?
│  ├─ NO → Use SEQUENTIAL (no parallelization possible)
│  └─ YES → Continue
│
├─ Can I specify what each subtask does?
│  ├─ NO → Use SEQUENTIAL (too vague)
│  └─ YES → Continue
│
├─ Will parallel execution save >= 3 minutes?
│  ├─ NO → Use SEQUENTIAL (overhead not justified)
│  └─ YES → Continue
│
├─ Do I have token budget for N× multiplier?
│  ├─ NO → Use SEQUENTIAL (budget constrained)
│  └─ YES → Continue
│
├─ Would multiple perspectives improve quality?
│  ├─ NO → Use SEQUENTIAL (single expert sufficient)
│  └─ YES → Continue
│
└─ PARALLELIZE with N agents

    ├─ If N ≤ 10: Direct parallel request
    ├─ If 10 < N ≤ 30: Batch into 2-3 rounds
    └─ If N > 30: Consider if parallelization is right approach
```

---

**End of Slideshow**

---

## Document Metadata

**Title:** Part 6: Parallelization with Agents - Complete Educational Slideshow

**Purpose:** Comprehensive teaching material for agentic coding students

**Slides:** 40 main slides + 4 appendix sections

**Topics Covered:**
- Performance benefits and trade-offs
- Parallelization fundamentals
- Practical patterns by use case
- Claude Code implementation details
- Comparison with other tools
- Best practices and common pitfalls
- Advanced techniques

**Audience:** Students learning agentic coding tools

**Estimated Teaching Time:** 2-3 hours of classroom material (with discussion)

**Last Updated:** January 2026

---
