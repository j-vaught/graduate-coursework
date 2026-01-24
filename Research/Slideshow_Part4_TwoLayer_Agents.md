# Part 4: Two-Layer Agent Work
## Teaching Agentic Coding Tools - Comprehensive Slideshow (40 slides)

---

## SECTION 1: Introduction to Two-Layer Pattern (5-6 slides)

### Slide 1: Title Slide - Two-Layer Agent Architecture
**Slide Title:** Two-Layer Agent Architecture: Orchestration and Specialization

**Visual Content:**
```
┌─────────────────────────────────────────┐
│                                         │
│      ORCHESTRATOR AGENT (Main)          │
│      ─────────────────────────          │
│   • Plans complex work                  │
│   • Breaks into tasks                   │
│   • Coordinates workers                 │
│   • Synthesizes results                 │
│                                         │
│  ↓        ↓        ↓        ↓           │
│                                         │
│  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐      │
│  │Task1│ │Task2│ │Task3│ │Task4│      │
│  │Worker│ │Worker│ │Worker│ │Worker│      │
│  └─────┘ └─────┘ └─────┘ └─────┘      │
│  (Parallel Execution)                  │
│                                         │
└─────────────────────────────────────────┘
```

**Main Content:**
- Modern agentic coding involves two distinct layers
- **Orchestrator Layer:** Thinks strategically, plans work, delegates
- **Worker Layer:** Executes specific tasks, reports results
- This pattern enables scaling, specialization, and parallel execution
- Mirrors how humans tackle complex projects

**Speaker Notes:**
The two-layer pattern is fundamental to effective agentic coding at scale. Instead of one agent trying to do everything, we separate concerns: one agent orchestrates and plans, while specialized workers execute discrete tasks. This allows for better resource utilization, clearer separation of concerns, and the ability to run multiple workers in parallel. Think of it like a project manager coordinating specialized team members rather than one person trying to do all the work.

**Key Concept:** Separation of concerns through orchestration-worker division

---

### Slide 2: What is Orchestration?
**Slide Title:** Orchestration: The Art of Coordinating Agents

**Visual Content:**
```
ORCHESTRATOR RESPONSIBILITIES:

┌──────────────────────────────────────┐
│  1. PLANNING                         │
│     Decompose goals into tasks       │
│     ├─ Analyze requirements          │
│     ├─ Identify dependencies         │
│     └─ Create execution order        │
│                                      │
│  2. TASK DISTRIBUTION                │
│     Route work to appropriate agents │
│     ├─ Skill matching                │
│     ├─ Load balancing                │
│     └─ Priority ordering             │
│                                      │
│  3. COORDINATION                     │
│     Manage concurrent execution      │
│     ├─ Parallel spawning             │
│     ├─ Dependency tracking           │
│     └─ Timeout handling              │
│                                      │
│  4. SYNTHESIS                        │
│     Aggregate and interpret results  │
│     ├─ Combine outputs               │
│     ├─ Verify quality                │
│     └─ Decision making               │
└──────────────────────────────────────┘
```

**Main Content:**
- Orchestration is the coordination layer that manages multiple agents
- Decides WHAT work needs to be done and WHO should do it
- Not about doing the work itself, but directing it
- Requires understanding:
  - Problem decomposition
  - Agent capabilities
  - Dependency management
  - Result integration

**Speaker Notes:**
Orchestration is a meta-level activity. The orchestrator doesn't implement features or debug code—it decides which agents should. It's like a conductor in an orchestra: the conductor doesn't play the instruments but coordinates when each section plays. An effective orchestrator understands the capabilities of its workers, can break complex problems into manageable pieces, and knows how to integrate their results into a coherent whole.

**Key Concept:** Orchestration = Strategic thinking about work distribution

---

### Slide 3: Main Agent vs Worker Agents
**Slide Title:** Roles in the Two-Layer System

**Visual Content:**
```
┌─────────────────────────────────────────────────────────┐
│ MAIN AGENT (Orchestrator)      │ WORKER AGENTS           │
├─────────────────────────────────────────────────────────┤
│                                 │                        │
│ Responsibilities:               │ Responsibilities:      │
│ • Receives user request         │ • Receive task desc    │
│ • Analyzes scope                │ • Execute work         │
│ • Creates plan                  │ • Report results       │
│ • Spawns tasks/workers          │ • Handle errors        │
│ • Waits for results             │ • Stay focused         │
│ • Makes decisions               │                        │
│ • Synthesizes output            │ Constraints:           │
│                                 │ • ~200K token limit    │
│ Scope:                          │ • Single task focus    │
│ • System-wide view              │ • Report-driven        │
│ • Long-lived                    │ • Isolated context     │
│ • Strategic thinking            │                        │
│                                 │ Advantages:            │
│ Token Budget:                   │ • No context bloat     │
│ • Full context available        │ • Fast execution       │
│                                 │ • Specialization       │
│                                 │ • Parallel work        │
│                                 │                        │
└─────────────────────────────────────────────────────────┘
```

**Main Content:**
- **Main Agent (Orchestrator):** Maintains system-wide perspective, makes strategic decisions
- **Worker Agents:** Focused specialists, execute one task at a time
- Different token budgets, responsibilities, and lifespans
- Workers are ephemeral; orchestrator is persistent
- Workers report back; orchestrator decides next steps

**Speaker Notes:**
The distinction between main and worker agents is crucial. Main agents are like project managers—they have the big picture and make strategic decisions. Workers are like specialized contractors—they do specific work and report results. This separation allows main agents to maintain detailed context about the overall project while workers stay focused and efficient without context bloat. Workers have limited token budgets (around 200K), so they need to be task-focused, while main agents have full access to context.

**Key Concept:** Different layers = different responsibilities and constraints

---

### Slide 4: Why Split Work into Tasks?
**Slide Title:** Benefits of Task Decomposition

**Visual Content:**
```
PROBLEM: Single Agent Attempting Everything
┌─────────────────────────────────────────────────┐
│                                                 │
│  • Context bloat (token limits)                │
│  • Loss of focus (too many concerns)           │
│  • Sequential execution (slow)                 │
│  • Hard to isolate failures                    │
│  • Cannot parallelize                          │
│  • Reduced effectiveness                       │
│                                                 │
└─────────────────────────────────────────────────┘

SOLUTION: Orchestrator + Task Workers
┌─────────────────────────────────────────────────┐
│                                                 │
│  ✓ Clear token boundaries                      │
│  ✓ Task focus (one thing well)                 │
│  ✓ Parallel execution                          │
│  ✓ Isolated failure handling                   │
│  ✓ Easy to retry failed tasks                  │
│  ✓ Better result quality                       │
│  ✓ Scalability                                 │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Main Content:**
- **Context Efficiency:** Workers have limited token budgets; staying focused preserves tokens
- **Parallelization:** Multiple workers can execute simultaneously
- **Focus:** Each worker concentrates on one task, improving quality
- **Resilience:** Failed tasks can be retried without affecting others
- **Scalability:** Easy to add more workers as complexity grows
- **Debugging:** Failures are isolated to specific tasks
- **Performance:** Parallel > sequential for multi-hour projects

**Speaker Notes:**
The main reason to split work is efficiency and parallelization. When a project takes hours or involves hundreds of files, splitting it among workers lets them run in parallel, dramatically reducing total time. Additionally, focused tasks produce better results because the worker isn't juggling multiple concerns. Workers with limited token budgets work better with focused tasks—they don't waste tokens on context about unrelated parts of the project. If one task fails, only that worker retries, not the entire system.

**Key Concept:** Task splitting enables parallelization and focus

---

### Slide 5: Real-World Analogy
**Slide Title:** Two-Layer Pattern in Familiar Contexts

**Visual Content:**
```
ANALOGY 1: Construction Project
┌──────────────────────────────────────┐
│  Project Manager (Orchestrator)      │
│  • Reads blueprint                   │
│  • Creates schedule                  │
│  • Hires contractors                 │
│  • Coordinates teams                 │
│  • Verifies progress                 │
│                                      │
│  ↓ ↓ ↓ ↓ (Parallel work)             │
│                                      │
│  Electricians │ Plumbers │ Framers   │
│  (Workers)                           │
└──────────────────────────────────────┘

ANALOGY 2: Magazine Production
┌──────────────────────────────────────┐
│  Editor-in-Chief (Orchestrator)      │
│  • Plans issue layout                │
│  • Assigns articles                  │
│  • Gathers submissions               │
│  • Reviews quality                   │
│                                      │
│  ↓ ↓ ↓ ↓ (Parallel work)             │
│                                      │
│  Writers │ Designers │ Fact-checkers │
│  (Workers)                           │
└──────────────────────────────────────┘
```

**Main Content:**
- **Construction:** Project manager orchestrates electricians, plumbers, framers (workers)
- **Magazine:** Editor-in-Chief orchestrates writers, designers, fact-checkers (workers)
- **Software Development:** Tech lead orchestrates backend devs, frontend devs, QA (workers)
- **Code AI:** Orchestrator agent → specialist worker agents
- Pattern is timeless and proven at scale

**Speaker Notes:**
This pattern isn't new—it's how humans organize complex work. A construction project can't have one person doing everything; a project manager coordinates specialists. Each specialist stays in their lane, doesn't need to know about other specialties, and can work in parallel with others. The same logic applies to agentic coding. An orchestrator handles planning and coordination while workers focus on specific tasks. This division of labor is what makes complex projects manageable.

**Key Concept:** Time-tested pattern from human organization

---

### Slide 6: When to Use Two-Layer Pattern (Decision Guide)
**Slide Title:** When Should You Use Two-Layer Architecture?

**Visual Content:**
```
DECISION TREE:

Is your task complex?
├─ NO  → Single agent sufficient ✓
│
└─ YES → Does it decompose naturally?
    ├─ NO  → Single agent or loop-based
    │
    └─ YES → Needs parallelization?
        ├─ NO  → Maybe sequential
        │
        └─ YES → Use Two-Layer!
                 ✓ Orchestrator + Workers

USE TWO-LAYER WHEN:
✓ Task naturally breaks into 3+ subtasks
✓ Subtasks are independent
✓ Total work > 2-3 hours
✓ Subtasks need specialization
✓ Parallelization saves time
✓ Context would exceed reasonable limits
```

**Main Content:**
- **Use Two-Layer for:**
  - Large codebases (many files to analyze)
  - Multi-phase tasks (research → design → build → test)
  - Specialized subtasks (backend vs frontend)
  - Long-running projects (breaking into time-bounded chunks)
  - Independent parallel work (code review, testing)

- **Avoid Two-Layer for:**
  - Simple, quick tasks (< 1 hour)
  - Tasks with heavy dependencies
  - Problems requiring constant decision-making
  - When context is minimal

**Speaker Notes:**
Two-layer architecture adds complexity, so use it judiciously. Simple tasks don't benefit—overhead outweighs gains. You need tasks that are independent enough to parallelize, substantial enough to benefit from focus, and ideally numerous enough that parallelization saves significant time. Rule of thumb: if the orchestrator's plan would take multiple hours and breaks naturally into 3+ independent pieces, consider two-layer. If it's a quick operation or requires constant back-and-forth, stick with a single agent or a simple loop.

**Key Concept:** Two-layer adds value for complex, parallelizable work

---

## SECTION 2: The Orchestrator-Worker Model (8-10 slides)

### Slide 7: Orchestrator Responsibilities Deep Dive
**Slide Title:** The Orchestrator: Strategic Decision-Maker

**Visual Content:**
```
ORCHESTRATOR WORKFLOW:

┌─────────────────────────────────────────────────┐
│                                                 │
│  1. UNDERSTAND                                  │
│     └─ Parse user request → identify scope     │
│                                                 │
│  2. PLAN                                        │
│     └─ Break into atomic tasks                 │
│        • Identify dependencies                 │
│        • Create execution order                │
│        • Allocate resources                    │
│                                                 │
│  3. SPAWN                                       │
│     └─ Create worker agents for each task     │
│        • Provide clear instructions            │
│        • Set success criteria                  │
│        • Define context boundaries             │
│                                                 │
│  4. WAIT                                        │
│     └─ Collect results as workers complete    │
│        • Handle timeouts                       │
│        • Detect partial failures               │
│        • Track progress                        │
│                                                 │
│  5. SYNTHESIZE                                  │
│     └─ Combine results into final answer      │
│        • Validate quality                      │
│        • Make final decisions                  │
│        • Format output                         │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Main Content:**
- **Understanding:** Orchestrator analyzes the user's request and determines scope
- **Planning:** Decomposes into discrete, independent tasks with clear outputs
- **Spawning:** Creates appropriate number of workers with focused instructions
- **Waiting:** Manages concurrent execution, handles failures, tracks progress
- **Synthesis:** Combines worker outputs into coherent final result

**Speaker Notes:**
Think of the orchestrator as a strategic leader. It doesn't implement features or fix bugs—it decides what needs to be done and who should do it. A good orchestrator asks: "What are the independent pieces of work? What's the minimum information each worker needs? How do I validate their results?" The orchestrator should be efficient with its thinking—spend tokens on planning, not execution.

**Key Concept:** Orchestrator = Plan → Delegate → Integrate

---

### Slide 8: Worker Responsibilities
**Slide Title:** Worker Agents: Focused Executors

**Visual Content:**
```
WORKER LIFECYCLE:

Receive Task
    ↓
┌─────────────────────────────────────┐
│ 1. UNDERSTAND TASK                  │
│    • Read instruction carefully     │
│    • Identify success criteria      │
│    • Note context boundaries        │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 2. EXECUTE WORK                     │
│    • Use provided context           │
│    • Stay in scope                  │
│    • Solve the specific problem     │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 3. VALIDATE RESULT                  │
│    • Check against success criteria │
│    • Verify completeness            │
│    • Self-test if possible          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│ 4. REPORT                           │
│    • Summarize findings             │
│    • Explain decisions              │
│    • Highlight issues               │
└─────────────────────────────────────┘
    ↓
Return to Orchestrator
```

**Main Content:**
- **Receive:** Worker gets task instruction, context, and success criteria
- **Execute:** Performs focused work without worrying about other tasks
- **Validate:** Checks result meets criteria before reporting
- **Report:** Provides clear summary of what was done and any issues
- **Key Principle:** Workers stay in scope—don't try to solve everything

**Speaker Notes:**
A good worker agent is disciplined. It receives a task with clear boundaries and stays within them. It doesn't try to be clever or expand the scope. If the task is "review these 5 functions for bugs," it reviews those 5 functions, not the entire codebase. Workers should be efficient: use tokens to solve the assigned problem, validate the solution, and report clearly. If something is out of scope, workers should note it but not attempt to solve it—that's the orchestrator's job.

**Key Concept:** Worker = Focused execution, clear reporting

---

### Slide 9: Communication Between Layers (Passing Context)
**Slide Title:** How Information Flows Between Layers

**Visual Content:**
```
ORCHESTRATOR → WORKER (Task Assignment)

Orchestrator sends to Worker:
┌─────────────────────────────────────┐
│ 1. TASK DEFINITION                  │
│    "Review code in files X, Y, Z    │
│     for security vulnerabilities"   │
│                                     │
│ 2. RELEVANT CONTEXT                 │
│    • File contents                  │
│    • Existing issues/reports        │
│    • Success criteria               │
│                                     │
│ 3. CONSTRAINTS                      │
│    • Scope boundaries               │
│    • Token limits                   │
│    • Deadline/timeout               │
│                                     │
│ 4. OUTPUT FORMAT                    │
│    "Return findings as JSON with   │
│     line numbers and severity"      │
└─────────────────────────────────────┘


WORKER → ORCHESTRATOR (Result Return)

Worker returns to Orchestrator:
┌─────────────────────────────────────┐
│ 1. OUTCOME STATUS                   │
│    • Success/Failure/PartialSuccess │
│                                     │
│ 2. KEY FINDINGS                     │
│    • Results of work                │
│    • Metrics/statistics             │
│    • Notable issues                 │
│                                     │
│ 3. CONFIDENCE LEVEL                 │
│    • High/Medium/Low confidence     │
│    • Edge cases encountered         │
│    • Assumptions made               │
│                                     │
│ 4. RECOMMENDATIONS                  │
│    • Next steps                     │
│    • Alternative approaches         │
│    • Resources needed               │
└─────────────────────────────────────┘
```

**Main Content:**
- **Downward Flow (O→W):** Clear, focused task definition with sufficient context
- **Upward Flow (W→O):** Structured results with status, findings, and confidence
- **Information Design:** Provide workers with exactly what they need, nothing more
- **Result Format:** Ask workers to structure results for easy synthesis
- **Feedback Loop:** Orchestrator interprets results and decides on next steps

**Speaker Notes:**
The communication between layers must be precise and efficient. When the orchestrator spawns a worker, it should include all necessary context—if the worker needs to review security in specific files, provide those files. Don't force the worker to search for context. Conversely, workers should structure their results clearly. Instead of prose rambling, ask for structured output: JSON with findings, status codes, confidence levels. This makes synthesis much easier. Think of it like API contracts: clear input specification and output schema.

**Key Concept:** Information flows must be precise and well-structured

---

### Slide 10: Result Synthesis
**Slide Title:** Combining Worker Results Into Final Output

**Visual Content:**
```
Multiple Workers Reporting Results:

Worker 1 (Backend Review)
└─ Found 3 bugs
   ├─ Critical: SQL injection
   ├─ Medium: Missing validation
   └─ Low: Performance issue

Worker 2 (Frontend Review)
└─ Found 2 bugs
   ├─ Medium: XSS vulnerability
   └─ Low: UI inconsistency

Worker 3 (Security Audit)
└─ Found 4 issues
   ├─ Critical: Authentication bypass
   ├─ High: Unencrypted data
   ├─ Medium: Weak password policy
   └─ Low: Missing logging


ORCHESTRATOR SYNTHESIZES:

┌─────────────────────────────────────┐
│ SYNTHESIS TASKS:                    │
│                                     │
│ 1. AGGREGATE                        │
│    Combine all findings into one    │
│    list (4 critical, 3 medium, etc) │
│                                     │
│ 2. DEDUPLICATE                      │
│    Remove if multiple workers       │
│    found same issue                 │
│                                     │
│ 3. PRIORITIZE                       │
│    Sort by severity and impact      │
│                                     │
│ 4. VALIDATE                         │
│    Check consistency, flag          │
│    contradictions                   │
│                                     │
│ 5. CONTEXTUALIZE                    │
│    Add explanations, next steps     │
│                                     │
│ 6. FORMAT OUTPUT                    │
│    Present to user in clear format  │
└─────────────────────────────────────┘
```

**Main Content:**
- **Aggregation:** Combine all worker outputs into single view
- **Deduplication:** Merge equivalent findings from multiple workers
- **Prioritization:** Order results by importance (severity, urgency)
- **Validation:** Check for contradictions or missing pieces
- **Contextualization:** Add orchestrator's perspective and recommendations
- **Formatting:** Present to user in most useful form (report, JSON, UI)

**Speaker Notes:**
Synthesis is where the orchestrator adds value beyond just running workers. A good orchestrator doesn't just dump worker results; it integrates them intelligently. If two workers found the same issue, report it once with combined evidence. If workers disagree (e.g., one says feature is feasible, another says it's not), the orchestrator investigates and decides. The synthesized output should be more valuable than any single worker's output—that's the orchestrator's job.

**Key Concept:** Synthesis = Integration + Analysis + Decision-Making

---

### Slide 11: Dependency Management
**Slide Title:** Handling Task Dependencies

**Visual Content:**
```
DEPENDENCY PATTERNS:

Pattern 1: PARALLEL (No Dependencies)
┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐
│Task 1 │  │Task 2 │  │Task 3 │  │Task 4 │
└───────┘  └───────┘  └───────┘  └───────┘
   ║         ║         ║         ║
   └─────────┴─────────┴─────────┘
        (All run simultaneously)


Pattern 2: LINEAR (Sequential)
┌────────┐
│Task 1  │ (requires file structure)
└────────┘
    ↓
┌────────┐
│Task 2  │ (requires Task 1 output)
└────────┘
    ↓
┌────────┐
│Task 3  │ (requires Task 2 output)
└────────┘


Pattern 3: TREE (Some Parallelism)
        ┌───────────┐
        │ Analyze   │
        └─────┬─────┘
         ↓    ↓    ↓
       ┌──┐ ┌──┐ ┌──┐
       │T1│ │T2│ │T3│ (parallel)
       └──┘ └──┘ └──┘
         ↓    ↓    ↓
        └─────┬─────┘
        ┌─────────────┐
        │  Synthesize │
        └─────────────┘
```

**Main Content:**
- **Independent Tasks:** Can run in parallel, maximum efficiency
- **Sequential Tasks:** One depends on output of previous; must order them
- **Hybrid:** Mix of parallel and sequential (most common)
- **Dependency Resolution:**
  - Identify dependencies early in planning
  - Run independent tasks in parallel
  - Only serialize when necessary
  - Use results from completed tasks to inform later ones

**Speaker Notes:**
Understanding dependencies is crucial for effective orchestration. Parallel tasks run simultaneously and save time; sequential tasks must run in order. Good orchestrators identify parallelizable work and exploit it. For example, when reviewing code, you can run multiple workers reviewing different files in parallel. But you might need one worker to understand architecture first, then have others review components. Identify these patterns during planning so you schedule work efficiently.

**Key Concept:** Identify parallelizable work early

---

### Slide 12: Error Handling and Recovery
**Slide Title:** Managing Failures in the Two-Layer System

**Visual Content:**
```
ERROR SCENARIOS:

Scenario 1: Single Task Fails
┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐
│Task 1│  │Task 2│  │Task 3│  │Task 4│
│  ✓   │  │  ✗   │  │  ✓   │  │  ✓   │
└──────┘  └──────┘  └──────┘  └──────┘

Orchestrator Actions:
├─ Retry Task 2 with modified prompt
├─ If still fails: collect other results
├─ Note partial failure in synthesis
└─ Recommend manual review of Task 2


Scenario 2: Worker Timeout
┌──────────────────────────────────────┐
│ Worker doesn't respond in time       │
│ (e.g., 30+ mins on complex task)     │
│                                      │
│ Orchestrator Actions:                │
│ ├─ Detect timeout (max 10 workers)  │
│ ├─ Flag as timeout in results        │
│ ├─ Can retry with simpler task       │
│ └─ Collect results from other tasks  │
└──────────────────────────────────────┘


Scenario 3: Multiple Failures
┌──────┐  ┌──────┐  ┌──────┐
│Task 1│  │Task 2│  │Task 3│
│  ✗   │  │  ✗   │  │  ✗   │
└──────┘  └──────┘  └──────┘

Orchestrator Actions:
├─ Recognize systemic issue
├─ Re-examine task definitions
├─ Simplify/redesign tasks
├─ Retry with better prompts
└─ May revert to single-agent approach
```

**Main Content:**
- **Single Task Failure:** Retry that task or collect other results
- **Timeout Handling:** Worker taking too long; may terminate and retry
- **Partial Failure:** Some workers succeed, some fail; use successful results
- **Systemic Failure:** All workers failing; indicates task design problem
- **Recovery Strategies:**
  - Retry with simpler prompt
  - Add more context/guidance
  - Break task into smaller pieces
  - Fallback to single-agent approach

**Speaker Notes:**
Two-layer systems must handle failures gracefully. A single worker's failure shouldn't crash the entire operation. Orchestrator should detect timeouts, retries, and partial results, then decide: keep going with available results, retry the failed task, or consolidate to single-agent. If most tasks fail, it signals the plan is flawed—redesign rather than brute force. Good error handling is what makes two-layer systems robust and reliable in production.

**Key Concept:** Failures are isolated; orchestrator adapts

---

## SECTION 3: Task vs Subagent Distinction (6-8 slides)

### Slide 13: Tasks vs Subagents
**Slide Title:** Two Ways to Delegate Work

**Visual Content:**
```
COMPARISON MATRIX:

┌──────────────────┬────────────────┬──────────────────┐
│ Aspect           │ TASKS          │ SUBAGENTS        │
├──────────────────┼────────────────┼──────────────────┤
│ Lifetime         │ Ephemeral      │ Persistent       │
│                  │ One-off job    │ Exists throughout│
│                  │                │ task sequence    │
├──────────────────┼────────────────┼──────────────────┤
│ Token Budget     │ ~200K per task │ Fresh budget     │
│                  │ No carryover   │ per interaction  │
├──────────────────┼────────────────┼──────────────────┤
│ State            │ Stateless      │ Maintains state  │
│                  │ No memory      │ Remembers context│
│                  │ between calls  │ and decisions    │
├──────────────────┼────────────────┼──────────────────┤
│ Initialization   │ Quick          │ Slower (setup)   │
│ Cost             │ Minimal        │ More overhead    │
├──────────────────┼────────────────┼──────────────────┤
│ Ideal For        │ Isolated work  │ Iterative work   │
│                  │ One execution  │ Multiple turns   │
├──────────────────┼────────────────┼──────────────────┤
│ Concurrency      │ Up to 10       │ Typically 1-3    │
│ Limit            │ simultaneous   │ sequential       │
└──────────────────┴────────────────┴──────────────────┘
```

**Main Content:**
- **Tasks:** Lightweight, stateless workers for specific jobs
  - Run once, report results, disappear
  - Can run many in parallel (up to 10)
  - No shared state between task instances

- **Subagents:** Persistent specialists with memory
  - Exist for duration of task sequence
  - Maintain context and state
  - Fewer simultaneous instances
  - Better for iterative/collaborative work

**Speaker Notes:**
This distinction is often confused, so let's be clear. In Claude Code, there are two delegation mechanisms. Tasks are for one-off work—"review this file," "generate documentation," "run these tests." Fire them up, get results, they're done. Subagents are for ongoing collaboration—you might spawn a subagent to be your "documentation specialist" who helps with multiple doc-related tasks throughout a session. Tasks are stateless; subagents remember previous interactions. For most orchestrator-worker patterns, tasks are what you want—simpler, faster, more parallelizable.

**Key Concept:** Tasks = Stateless one-offs; Subagents = Persistent specialists

---

### Slide 14: Task Characteristics and Use Cases
**Slide Title:** Tasks: Lightweight, Stateless Execution

**Visual Content:**
```
TASK LIFECYCLE:

Orchestrator: "Spawn Task"
                ↓
        ┌───────────────┐
        │ Initialize    │ (< 1 second)
        │ Fresh context │
        │ 200K budget   │
        └───────────────┘
                ↓
        ┌───────────────┐
        │ Execute work  │ (seconds to mins)
        │ Use provided  │
        │ context only  │
        └───────────────┘
                ↓
        ┌───────────────┐
        │ Report result │ (instant)
        │ Clean termination
        └───────────────┘


IDEAL TASK CHARACTERISTICS:

✓ Self-contained work
✓ Clear input → output mapping
✓ No dependency on previous tasks
✓ Can be parallelized
✓ Execution < 5 minutes
✓ Result is final (no back-and-forth)
✓ Multiple workers can do same task
✓ Task can be retried independently
```

**Main Content:**
- **Best For:**
  - Analyzing individual files or functions
  - Running tests on specific modules
  - Generating documentation sections
  - Code reviews of focused scope
  - Data processing on subsets
  - Parallel experiments

- **Key Advantage:** Freshly initialized for each task means no context bloat
- **Constraint:** ~200K tokens per task; keep focused to stay within limits
- **Execution Model:** Fire many simultaneously (up to 10); fast, parallel

**Speaker Notes:**
Tasks are your go-to for distributed work. They're lightweight—minimal overhead to spawn, quick to start. They have fresh token budgets, so you never worry about one task's context affecting another. The trade-off is they have no memory; each task is isolated. This is actually an advantage for parallelization because tasks don't interfere with each other. If you're reviewing 20 files, spawn 10 tasks, review 2 files each, run in parallel. Each task uses a fresh context, completes independently, reports results.

**Key Concept:** Tasks are optimized for parallelization

---

### Slide 15: Subagent Characteristics and Use Cases
**Slide Title:** Subagents: Persistent, Stateful Partners

**Visual Content:**
```
SUBAGENT LIFECYCLE:

Orchestrator: "Spawn Subagent"
        ↓
    ┌────────────────────┐
    │ Initialize         │ (slower, more setup)
    │ Specialized role   │
    │ Fresh context      │
    │ 200K budget/turn   │
    └────────────────────┘
        ↓
    ┌────────────────────┐
    │ Turn 1: Work       │
    │ Learns context,    │
    │ makes decisions    │
    └────────────────────┘
        ↓
    ┌────────────────────┐
    │ Turn 2: Continue   │
    │ Remembers Turn 1   │
    │ Builds on progress │
    └────────────────────┘
        ↓
    ┌────────────────────┐
    │ Turn N: Finalize   │
    │ Full context       │
    │ aware of all work  │
    └────────────────────┘
        ↓
    Clean termination


IDEAL SUBAGENT CHARACTERISTICS:

✓ Iterative problem solving
✓ Multi-turn interactions
✓ Specialist role (architect, writer, etc)
✓ Benefits from context accumulation
✓ Makes decisions that inform later work
✓ Provides guidance across tasks
✓ Needs to understand broader context
```

**Main Content:**
- **Best For:**
  - Architecture design (multiple refinements)
  - Writing/documentation (iterative feedback)
  - Complex debugging (gather context, then solve)
  - Feature implementation (plan → build → test cycles)
  - Specialist roles (backend architect, security reviewer)

- **Key Advantage:** Remembers prior interactions, builds sophisticated understanding
- **Cost:** Each turn uses fresh 200K budget, but initialization overhead
- **Execution Model:** Typically 1-3 sequential subagents; back-and-forth interaction

**Speaker Notes:**
Subagents are for more involved collaboration. If your work requires multiple turns—"let's design this architecture, now implement it, now test it"—subagents are better. Each turn gets fresh context, but the subagent remembers previous turns and builds on them. This is valuable for complex work where understanding grows iteratively. The cost is you can't parallelize subagents as easily (you typically use a few, not ten). Use subagents for specialists whose job is complex or requires oversight; use tasks for worker bees that do isolated jobs.

**Key Concept:** Subagents are for iterative, multi-turn collaboration

---

### Slide 16: When to Use Tasks vs Subagents
**Slide Title:** Decision Tree: Tasks or Subagents?

**Visual Content:**
```
DECISION LOGIC:

Is work naturally parallelizable?
├─ YES (e.g., review 10 files)
│  └─ Use TASKS
│     • Spawn multiple tasks
│     • Run in parallel
│     • Collect results
│
└─ NO, requires back-and-forth
    Is it iterative?
    ├─ NO (one execution, complex or not)
    │  └─ Use TASK
    │     • Single focused task
    │     • Report result
    │
    └─ YES (multiple turns needed)
        └─ Use SUBAGENT
           • Initialize once
           • Multiple interactions
           • Builds context


QUICK REFERENCE:

TASK               │ SUBAGENT
─────────────────────────────────────
Code review       │ Code architect
Test file X       │ Integrate & test
Review security   │ Design protocol
Analyze data      │ Data strategy
Generate docs     │ Doc specialist
─────────────────────────────────────
```

**Main Content:**
- **Choose Task if:**
  - Work can be parallelized (many similar jobs)
  - Single execution gets the job done
  - Result doesn't need refinement/iteration
  - Multiple workers can work independently
  - Speed is critical

- **Choose Subagent if:**
  - Work requires refinement iterations
  - Specialist role needing context growth
  - Multiple related decisions to make
  - Guidance/oversight throughout project
  - Quality matters more than speed

**Speaker Notes:**
The practical guide: parallelizable work = tasks. Iterative work = subagents. A code review task might spawn 5 tasks to review different functions in parallel. An architecture design might spawn 1 subagent you interact with multiple times. In most orchestrator patterns, you'll use tasks for workers—it's simpler, faster, more scalable. Save subagents for when you really need persistent state and iterative refinement.

**Key Concept:** Parallelizable = Tasks; Iterative = Subagents

---

### Slide 17: Example: Task-Based Worker Pattern
**Slide Title:** Practical Example: Task-Based Code Review

**Visual Content:**
```
SCENARIO: Review 8 functions for bugs

ORCHESTRATOR DECISION:
"This is parallelizable. Use tasks."

SPAWNING PHASE:
Task 1: Review func_auth()
Task 2: Review func_parse()
Task 3: Review func_query()
Task 4: Review func_format()
Task 5: Review func_validate()
Task 6: Review func_cache()
Task 7: Review func_hash()
Task 8: Review func_log()

(All 8 spawn in parallel)

EXECUTION (runs simultaneously):
Time 0:    [T1][T2][T3][T4][T5][T6][T7][T8]
           ↓   ↓   ↓   ↓   ↓   ↓   ↓   ↓
           (each finds 1-3 bugs)
Time 2min: [T1✓][T2✓][T3✓][T4✓][T5✓][T6✓][T7✓][T8✓]

RESULTS RETURN:
T1: Found 2 bugs
T2: Found 1 bug
T3: Found 3 bugs
T4: Found 0 bugs
T5: Found 1 bug
T6: Found 2 bugs
T7: Found 1 bug
T8: Found 0 bugs

ORCHESTRATOR SYNTHESIZES:
├─ 10 total bugs found
├─ Aggregate by severity
├─ Create prioritized report
└─ Return to user
```

**Main Content:**
- **Parallelization Efficiency:** 8 tasks × 2 min each = 2 min total (vs 16 min sequential)
- **Task Design:** Each task is self-contained, needs function code only
- **Result Handling:** Aggregate findings, deduplicate, prioritize
- **Scalability:** Can handle 20+ functions by increasing parallel tasks
- **Failure Resilience:** One task failure doesn't affect others

**Speaker Notes:**
This exemplifies the task pattern. You have a set of similar, independent jobs. Divide them among tasks and run in parallel. The orchestrator's job is minimal—send work out, collect results, synthesize. This is where two-layer shines: what would take 16 minutes sequentially takes 2 minutes with parallel tasks. For large codebases, this scales beautifully.

**Key Concept:** Tasks enable parallelization that dramatically reduces time

---

### Slide 18: Example: Subagent-Based Specialist Pattern
**Slide Title:** Practical Example: Iterative Architecture Design

**Visual Content:**
```
SCENARIO: Design system architecture for new feature

ORCHESTRATOR DECISION:
"Complex, iterative. Use subagent."

SUBAGENT INITIALIZED:
Role: "Architecture Specialist"
Expertise: System design, scalability, patterns

TURN 1 - INITIAL DESIGN:
User: "We need a real-time notification system.
       Expect 1M users, 100K concurrent."
Subagent: (designs architecture)
Result: Proposes microservices approach
        ├─ Notification service (handles queueing)
        ├─ WebSocket gateway (handles connections)
        └─ Analytics service (tracks delivery)

TURN 2 - REFINEMENT:
User: "Can it handle 10M events/sec?"
Subagent: (recalls Turn 1 design, refines)
Result: "Kafka for buffering, recommends Redis cache,
         adjusts thread counts"

TURN 3 - VALIDATION:
User: "What about disaster recovery?"
Subagent: (understands full design, adds DR layer)
Result: "Multi-region replication, failover strategy"

TURN 4 - IMPLEMENTATION GUIDE:
User: "How do we build this?"
Subagent: (knows full context, provides implementation steps)
Result: Detailed step-by-step build plan

Subagent terminates with full context of all decisions.
```

**Main Content:**
- **Iterative Refinement:** Each turn builds on previous understanding
- **Context Growth:** Subagent accumulates knowledge across turns
- **Specialist Role:** Deep expertise in architecture applied consistently
- **Decision Continuity:** All decisions connected and coherent
- **Output:** Comprehensive design from multiple perspectives

**Speaker Notes:**
This shows subagents shine. The specialist accumulates context across turns, understands constraints, refines design iteratively. You can't easily parallelize this—it requires sequential interaction. A task can't do this as well because each task is fresh; you'd lose context between design iterations. The subagent remembers "we chose Kafka for buffering," so when asked about disaster recovery, it integrates that into the solution. This is specialist-level work that benefits from memory.

**Key Concept:** Subagents excel at iterative specialization

---

## SECTION 4: Claude Code Task Tool Deep Dive (10-12 slides)

### Slide 19: Claude Code Task Tool Overview
**Slide Title:** The Task Tool: Spawning Worker Agents

**Visual Content:**
```
CLAUDE CODE TASK TOOL:

What it is:
├─ Built-in command for spawning parallel agents
├─ Terminal-based, integrated into Claude Code
├─ Handles context isolation and management
└─ Manages constraints and execution

Syntax:
task: "instruction" [options]

Example:
task: "Review the authentication module for security issues"
      --context="src/auth.py"
      --timeout=300
      --name="auth-review"

Key Features:
├─ Parallel execution (up to 10 concurrent)
├─ Automatic context isolation
├─ Result collection and buffering
├─ Timeout management
├─ Structured output format
└─ Integration with main agent
```

**Main Content:**
- **Purpose:** Spawn lightweight worker agents for parallelizable work
- **Syntax:** `task: "instruction"` with optional parameters
- **Concurrency:** Up to 10 tasks run simultaneously
- **Context:** Each task gets ~200K tokens, isolated from other tasks
- **Results:** Automatically collected and returned to orchestrator
- **Integration:** Native to Claude Code, minimal overhead

**Speaker Notes:**
The task tool is Claude Code's built-in mechanism for the worker layer. You don't need external infrastructure or APIs; it's part of the language model itself. When you spawn a task, Claude Code creates a fresh context window with your instruction and any provided context. The task executes independently, reports results, and disappears. Up to 10 can run simultaneously, so you get parallelization for free. This is what makes two-layer patterns practical in Claude Code.

**Key Concept:** Task tool = Built-in parallelization mechanism

---

### Slide 20: Task Syntax and Parameters
**Slide Title:** Task Tool Parameters and Options

**Visual Content:**
```
COMPLETE TASK SYNTAX:

task: "Primary instruction for the worker"
  --name="task-identifier"
  --context="file or block to provide"
  --timeout=300
  --output-format="json|text|markdown"
  --priority="low|normal|high"

PARAMETER BREAKDOWN:

Instruction (Required):
  What you want the task to do
  Example: "Review this code for security issues"

Name (Optional):
  Identifier for tracking
  Useful when running many tasks

Context (Optional):
  File(s) or content to provide
  Can be glob patterns: "src/**/*.py"
  Automatically read and included
  Stays within 200K budget

Timeout (Optional):
  Max seconds to wait (default: varies)
  Typical: 120-600 seconds
  If exceeded: task terminates, report timeout

Output Format (Optional):
  json: Structured output (recommended)
  text: Plain text response
  markdown: Formatted markdown

Priority (Optional):
  low: Background tasks
  normal: Standard execution
  high: Rush priority


FULL EXAMPLE:

task: "Identify security vulnerabilities in these functions"
  --name="security-audit-auth"
  --context="src/auth/*.py"
  --timeout=300
  --output-format="json"
  --priority="high"
```

**Main Content:**
- **Instruction:** Core task definition (e.g., "write unit tests")
- **Name:** Label for identifying task in logs/results
- **Context:** Specific files/content to provide; respects 200K limit
- **Timeout:** How long to wait before killing task
- **Output Format:** How to structure results (JSON recommended)
- **Priority:** When to execute relative to other tasks

**Speaker Notes:**
The most important parameters are instruction (what to do) and context (what to operate on). You want to provide just enough context so the task can succeed without wasting tokens. If the task is "review src/auth.py," provide just that file. Don't provide the entire codebase. Use glob patterns for multiple files. Output format should usually be JSON for easy synthesis by the orchestrator. Timeout prevents endless waiting—set it appropriately for task complexity.

**Key Concept:** Parameters control task scope, context, and execution

---

### Slide 21: Spawning Multiple Tasks (Parallelization)
**Slide Title:** Running Tasks in Parallel

**Visual Content:**
```
SEQUENTIAL SPAWNING:

Main Agent:
  task: "Review file1.js"
    [waits for completion: ~2 min]
  task: "Review file2.js"
    [waits for completion: ~2 min]
  task: "Review file3.js"
    [waits for completion: ~2 min]
  task: "Review file4.js"
    [waits for completion: ~2 min]

Total time: ~8 minutes


PARALLEL SPAWNING (Correct):

Main Agent spawns all at once:
  task: "Review file1.js" --name="t1"
  task: "Review file2.js" --name="t2"
  task: "Review file3.js" --name="t3"
  task: "Review file4.js" --name="t4"

All tasks execute simultaneously.
Main agent waits for all to complete.

Total time: ~2 minutes (4x faster!)


PRACTICAL PATTERN:

# Prepare task list
tasks_to_run = [
  ("Review auth module", "src/auth.py"),
  ("Review payment module", "src/payment.py"),
  ("Review database module", "src/db.py"),
  ("Review API module", "src/api.py"),
]

# Spawn all tasks
for instruction, context in tasks_to_run:
  task: instruction
    --context=context
    --name=f"review-{Path(context).stem}"

# Orchestrator waits and collects all results
# Then synthesizes findings
```

**Main Content:**
- **Sequential:** Task completes → Next task starts (slow, no parallelization)
- **Parallel:** All tasks spawn, run simultaneously, orchestrator waits for all
- **Constraint:** Maximum 10 concurrent tasks
- **Efficiency:** N similar tasks take ~1/N the time with parallelization
- **Resource Management:** Stay under 10; if > 10, batch them

**Speaker Notes:**
Parallel spawning is where you get huge efficiency gains. Don't spawn tasks one by one and wait for each. Prepare your list, spawn them all at once, then wait for batch completion. A review task taking 2 minutes × 10 files = 20 minutes sequentially, but just 2 minutes in parallel. This is why two-layer patterns are so valuable for big jobs. Use naming to track which task is which in your results.

**Key Concept:** Spawn all tasks upfront for maximum parallelization

---

### Slide 22: Context Isolation (200K Per Task)
**Slide Title:** Token Budget and Context Isolation

**Visual Content:**
```
CONTEXT ISOLATION:

┌──────────────────────────────────────┐
│  Main Agent                          │
│  Token Budget: Full (no hard limit)  │
│  Can maintain large context          │
│  Uses tokens to orchestrate          │
└──────────────────────────────────────┘
                 ↓
    ┌────────────┬────────────┬────────────┐
    ↓            ↓            ↓            ↓
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ Task 1  │ │ Task 2  │ │ Task 3  │ │ Task 4  │
│~200K    │ │~200K    │ │~200K    │ │~200K    │
│tokens   │ │tokens   │ │tokens   │ │tokens   │
│each     │ │each     │ │each     │ │each     │
└─────────┘ └─────────┘ └─────────┘ └─────────┘
(Isolated)  (Isolated)  (Isolated)  (Isolated)
(Fresh)     (Fresh)     (Fresh)     (Fresh)


BUDGET MANAGEMENT:

Task 1 Budget: 200K tokens
├─ Instruction: ~0.1K
├─ Context (provided files): ~50K
├─ Working space (thinking): ~149K
└─ Output: ~0.9K

If context > 200K:
├─ Automatic truncation (may drop data!)
├─ Or: Claude warns and task fails
├─ Solution: Reduce context or split task

CONTEXT PROVISION:

Good:
  task: "Review auth.py for bugs"
    --context="src/auth.py"  [5K]
  ✓ Leaves plenty of budget for thinking

Bad:
  task: "Review auth module"
    --context="src/**/*.py"  [500K]
  ✗ Exceeds budget, will fail or truncate

Better:
  task: "Review auth.py"
    --context="src/auth.py"  [5K]
  task: "Review api.py"
    --context="src/api.py"  [4K]
  ✓ Split work, each within budget
```

**Main Content:**
- **Per-Task Limit:** ~200K tokens per task (context + working budget)
- **Context Sharing:** Don't repeat large context across many tasks
- **Efficiency Strategy:** Provide minimum necessary context per task
- **Failure Handling:** Task fails if context exceeds budget; reduce or split
- **Main Agent:** No hard limit; can maintain orchestration context

**Speaker Notes:**
Understanding context isolation is critical. Each task is fresh with ~200K tokens. If you provide 100K tokens of context to a task, it has ~100K left for thinking and output. If your codebase is huge, you can't give it all to every task—split the work instead. The orchestrator is different; it maintains the big picture and orchestration context across all workers. But workers should stay focused. This is why tasks are efficient—each task is right-sized for its job, no wasted context on irrelevant code.

**Key Concept:** Each task gets ~200K; be efficient with context

---

### Slide 23: Constraints: Maximum 10 Concurrent Tasks
**Slide Title:** Concurrency Limits and Batching

**Visual Content:**
```
CONCURRENCY CONSTRAINT:

Maximum concurrent tasks: 10

Scenario 1: Exactly 10 Tasks (Optimal)
task1 ─┐
task2 ─┤
task3 ─┤
task4 ─┤
task5 ─┼─ All run simultaneously
task6 ─┤
task7 ─┤
task8 ─┤
task9 ─┤
task10─┘

Scenario 2: More than 10 Tasks (Must Batch)
task1 ──┐
task2  ─┤
...    ─┤ Batch 1: Run simultaneously
task10─┘
[Wait for batch to complete]

task11─┐
task12─┤
...   ─┤ Batch 2: Run simultaneously
task20─┘
[Wait for batch to complete]

Example:
Need to review 50 functions?
├─ Batch 1: Functions 1-10 (2 min)
├─ Batch 2: Functions 11-20 (2 min)
├─ Batch 3: Functions 21-30 (2 min)
├─ Batch 4: Functions 31-40 (2 min)
└─ Batch 5: Functions 41-50 (2 min)
Total: 10 min (sequential batches, but each batch parallel)


BATCHING PATTERN:

def orchestrate_reviews(files):
  all_results = []

  # Batch size: 10
  for batch_start in range(0, len(files), 10):
    batch = files[batch_start:batch_start+10]

    # Spawn 10 tasks for this batch
    batch_results = []
    for file in batch:
      result = task: f"Review {file}"
        --context=file
      batch_results.append(result)

    all_results.extend(batch_results)
    # Batch 1 completes, move to Batch 2

  return all_results
```

**Main Content:**
- **Hard Limit:** 10 concurrent tasks maximum
- **Less is OK:** Can run 1-10 tasks; benefits scale with parallelization
- **More Than 10:** Must batch into groups of ≤ 10
- **Batching Overhead:** Sequential batches are slower than single parallel set
- **Optimization:** Size batches to maximize parallelization

**Speaker Notes:**
The 10-task limit is a practical constraint from the infrastructure. You can spawn 10 tasks and let them run in parallel; if you need 25 tasks, you batch into three groups. Each batch runs in parallel, but batches execute sequentially. For 25 tasks of 2 minutes each: single parallel take 2 minutes, three sequential batches take 6 minutes. You still get value, but less than if you could parallelize all 25. Design your tasks to stay under 10 when possible.

**Key Concept:** Batch large jobs into groups of ≤ 10 tasks

---

### Slide 24: Result Collection and Processing
**Slide Title:** Handling Task Results

**Visual Content:**
```
RESULT LIFECYCLE:

Spawn all tasks
        ↓
Tasks execute in parallel
        ↓
Results accumulate as tasks complete
(not necessarily in spawn order)
        ↓
Orchestrator receives all results
        ↓
Process results


RESULT STRUCTURE:

Each task returns:
{
  "task_id": "t1",
  "status": "success|timeout|error",
  "output": "actual result",
  "execution_time": 45,  // seconds
  "tokens_used": 12500,
  "warnings": []
}

Processing Pattern:
┌────────────────────────────────────┐
│ Collect all results                │
├────────────────────────────────────┤
│ for each result:                   │
│   if status == "success":          │
│     aggregate_output(result)       │
│   elif status == "timeout":        │
│     handle_timeout(result)         │
│     maybe retry                    │
│   elif status == "error":          │
│     handle_error(result)           │
│     maybe retry or skip            │
│                                    │
│ After processing all results:      │
│   deduplicate findings             │
│   prioritize by importance         │
│   format final report              │
└────────────────────────────────────┘


ERROR SCENARIOS:

Success:
  task_1: Found 3 bugs ✓
  task_2: Found 1 bug ✓
  task_3: Found 2 bugs ✓
  → All results used

Partial Success:
  task_1: Found 3 bugs ✓
  task_2: Timeout ✗
  task_3: Found 2 bugs ✓
  → Use 1 & 3, flag 2 as incomplete

All Failed:
  task_1: Error ✗
  task_2: Error ✗
  task_3: Error ✗
  → Likely flawed task design; retry or redesign
```

**Main Content:**
- **Result Format:** Each task returns status, output, execution time, tokens used
- **Success Status:** `success`, `timeout`, or `error`
- **Collection:** Results arrive asynchronously; collect all before processing
- **Processing:** Aggregate successes, handle failures gracefully
- **Partial Failure:** Use available results, note what failed
- **Synthesis:** Combine results into final output

**Speaker Notes:**
Tasks don't return in spawn order—they arrive as each completes. Collect all results before synthesis. Check status for each: success means process normally, timeout means task ran too long (maybe retry with simpler task), error means something went wrong (check error details). A well-designed orchestrator can handle partial failures—if 8 of 10 tasks succeed, synthesize those 8 results and note that 2 timed out. This makes the system robust.

**Key Concept:** Collect all results, handle failures gracefully

---

### Slide 25: Practical Example: Claude Code Task Usage
**Slide Title:** Real Code Example: Spawning and Processing Tasks

**Visual Content:**
```
ORCHESTRATOR CODE EXAMPLE:

Main Agent:
"""
I need to review 8 functions in auth.py for security issues.

Let me spawn 4 parallel review tasks:
"""

task: "Review functions get_user_token and
       validate_token for security issues.
       Focus on: injection attacks, token
       validation weaknesses, timing attacks."
  --context="src/auth.py:50-100"
  --name="auth-tokens"
  --timeout=300
  --output-format="json"

task: "Review functions hash_password and
       verify_password for security issues.
       Focus on: weak hashing, timing
       vulnerabilities, salt handling."
  --context="src/auth.py:200-250"
  --name="auth-password"
  --timeout=300
  --output-format="json"

task: "Review function authenticate_user for
       security issues. Focus on: SQL injection,
       rate limiting, session handling."
  --context="src/auth.py:300-350"
  --name="auth-main"
  --timeout=300
  --output-format="json"

task: "Review function is_admin_token for
       security issues. Focus on: authorization
       bypass, token forgery, privilege escalation."
  --context="src/auth.py:400-450"
  --name="auth-admin"
  --timeout=300
  --output-format="json"

[Tasks run in parallel for ~3 minutes]

Results received:
- auth-tokens: 2 issues found (1 critical)
- auth-password: 1 issue found (medium)
- auth-main: 3 issues found (2 critical)
- auth-admin: 0 issues found

Synthesis:
Aggregated 6 security issues across 8 functions.
Prioritized by severity:
1. SQL injection in authenticate_user (CRITICAL)
2. Token validation weakness in get_user_token (CRITICAL)
3. Timing attack in verify_password (MEDIUM)
... etc
```

**Main Content:**
- **Task Preparation:** Identify 4 independent code review tasks
- **Context Provision:** Give each task only the relevant lines
- **Naming:** Use descriptive names for tracking (`auth-tokens`, etc.)
- **Parallelization:** Spawn all 4 at once
- **Result Handling:** Process JSON output from all tasks
- **Synthesis:** Aggregate findings, prioritize, report to user

**Speaker Notes:**
This is real, practical usage. The orchestrator decides: "I have 8 functions to review. I can parallelize this. Let me break into 4 pairs and spawn 4 tasks." Each task gets just the code it needs, with clear instructions. They run in parallel (~3 min vs 12 min sequential). The orchestrator collects results, synthesizes findings (deduplicates, prioritizes), and returns a comprehensive report. This is how you leverage the task tool effectively.

**Key Concept:** Well-designed tasks provide massive efficiency gains

---

### Slide 26: Batch Execution Behavior
**Slide Title:** How Batch Task Execution Works

**Visual Content:**
```
BATCH EXECUTION MODEL:

When Main Agent Spawns 5 Tasks:

t=0s
  Spawn task_1 -> Ready
  Spawn task_2 -> Ready
  Spawn task_3 -> Ready
  Spawn task_4 -> Ready
  Spawn task_5 -> Ready

t=1s - 2min
  [All 5 execute in parallel]
  task_1 ███████████ (2 min)
  task_2 █████ (1 min)
  task_3 ███████████████ (2.5 min)
  task_4 ████ (0.5 min)
  task_5 ██████████ (1.5 min)

t=2.5min
  task_4 completes ✓
  Main agent does NOT wait; continues scheduling

t=1.5min
  task_2 completes ✓
  Main agent continues...

t=1.5min
  task_5 completes ✓
  Main agent continues...

t=2min
  task_1 completes ✓
  Main agent continues...

t=2.5min
  task_3 completes ✓
  All tasks done!

[Orchestrator collects all results and processes]


ORCHESTRATOR WAITS FOR:

Option 1: Wait for all tasks
  orchestrator: [spawns tasks] [waits] [gets all results]
  → Blocks until every task complete
  → Gets all results at once

Option 2: Process results as they arrive
  orchestrator: [spawns tasks]
               [asynchronously collects results]
               [processes partial results]
  → Can start synthesis before all complete
  → More complex but faster feedback

Most common: Option 1
(Orchestrator waits for all, then processes batch)
```

**Main Content:**
- **Parallel Execution:** Tasks run simultaneously, not in spawn order
- **Completion Order:** Tasks complete as they finish; fastest first
- **Orchestrator Wait:** Main agent waits for all tasks or specific threshold
- **Result Collection:** Asynchronous; results arrive as tasks complete
- **Processing:** Can process all at once or as batches arrive
- **Practical Pattern:** Spawn all → Wait for all → Synthesize → Return

**Speaker Notes:**
Task execution is genuinely parallel. When you spawn 5 tasks at t=0, they all run simultaneously, each in its own context. They don't wait for each other; fastest finishes first. The orchestrator typically waits until all are done, collects results, then processes. This is the blocking model—simple and predictable. More advanced patterns let you process results as they arrive, but that adds complexity. For teaching purposes, the blocking model is clearer: spawn, wait, process, return.

**Key Concept:** Tasks run parallel; orchestrator collects all results

---

## SECTION 5: Two-Layer Patterns in Other Tools (5-6 slides)

### Slide 27: Aider's Architect/Editor Model
**Slide Title:** Two-Layer Pattern in Aider

**Visual Content:**
```
AIDER ARCHITECTURE (Pair Programming AI):

┌─────────────────────────────────────┐
│        User/Main Agent              │
│        (Controls flow)              │
└─────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│      ARCHITECT LAYER                 │
│  • Analyzes codebase                 │
│  • Decides what needs changing      │
│  • Creates plan                     │
│  • Specifies files to modify        │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│       EDITOR LAYER                   │
│  • Receives architect's plan         │
│  • Modifies specified files          │
│  • Generates/updates code            │
│  • Runs tests                        │
└──────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│   Return modified code to user      │
└─────────────────────────────────────┘

ANALOGY TO CLAUDE CODE:
Architect = Orchestrator (planning)
Editor    = Task Worker (execution)

Both use Claude LLM, but for different purposes
```

**Main Content:**
- **Architect Role:** Analyzes codebase, plans changes, decides approach
- **Editor Role:** Implements changes specified by architect
- **Separation:** Thinking (architect) vs. doing (editor)
- **Workflow:** User → Architect → Editor → Back to User
- **Benefits:** Clear separation, iterative refinement possible
- **Comparison:** Similar to orchestrator-worker but tightly coupled to user

**Speaker Notes:**
Aider demonstrates the pattern in pair programming context. The architect "thinks" about what needs to change; the editor "does" the changes. This is two-layer applied to code modification. Claude Code's pattern is similar but more flexible—orchestrator is you (the main agent), workers are tasks. Aider's architect-editor is more automated; they decide together. Both show that breaking into layers improves results and clarity.

**Key Concept:** Two-layer pattern appears across different tools

---

### Slide 28: OpenHands Delegation Model
**Slide Title:** Delegation Pattern in OpenHands

**Visual Content:**
```
OPENHANDS ARCHITECTURE (Autonomous Agent Framework):

┌──────────────────────────────────────┐
│      Main Agent (Controller)         │
│  • Receives task from user           │
│  • Plans approach                    │
│  • Delegates to tool agents          │
│  • Verifies results                  │
└──────────────────────────────────────┘
              ↓ ↓ ↓ ↓
    ┌─────────┴──┴───────┬──────────┐
    ↓                    ↓          ↓
┌────────┐          ┌────────┐  ┌────────┐
│ Code   │          │ Shell  │  │Search  │
│Analyst │          │Command │  │Expert  │
│Agent   │          │Agent   │  │Agent   │
└────────┘          └────────┘  └────────┘

Responsibilities:
Code Analyst:  Understands code, suggests changes
Shell Command: Executes CLI commands, reads output
Search Expert: Finds relevant code, docs, solutions

Each agent is specialist, handles one domain.
Main agent orchestrates specialists.
```

**Main Content:**
- **Specialist Agents:** Each agent handles specific domain (code, shell, search)
- **Main Controller:** Routes tasks to appropriate specialists
- **Delegation:** Instead of one agent doing everything, delegate to experts
- **Result Integration:** Controller combines specialist outputs
- **Scalability:** New specialists can be added without changing core

**Speaker Notes:**
OpenHands shows a scaling pattern where you add multiple specialist agents. The controller's job is to route work: "This is a code problem, send to Code Analyst. This needs a shell command, send to Shell Command Agent." This is orchestrator-worker at scale. The key insight: specialists are more effective than generalists. One agent trying to code and run shell commands and search docs is less effective than three agents each expert in their domain.

**Key Concept:** Specialist agents through delegation improve quality

---

### Slide 29: GitHub Copilot's Four-Agent Pattern
**Slide Title:** Copilot's Internal Agent Architecture

**Visual Content:**
```
GITHUB COPILOT ARCHITECTURE (Inferred from Public Info):

User Request (e.g., "Write a function to sort an array")
              ↓
┌──────────────────────────────────────┐
│    1. INTENT CLASSIFIER              │
│    (What is user asking?)            │
│    • Code generation?                │
│    • Code review?                    │
│    • Testing?                        │
│    • Documentation?                  │
└──────────────────────────────────────┘
              ↓
              ├─→ Code Generation Path
              ├─→ Code Review Path
              ├─→ Testing Path
              └─→ Documentation Path
              ↓
┌──────────────────────────────────────┐
│  2. CONTEXT GATHERER                 │
│  (What information is needed?)       │
│  • Codebase analysis                 │
│  • File history                      │
│  • Similar patterns                  │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│  3. SPECIALIST GENERATOR             │
│  (Path-specific handler)             │
│  • Language-specific expert          │
│  • Framework-specific expert         │
│  • Style-specific expert             │
└──────────────────────────────────────┘
              ↓
┌──────────────────────────────────────┐
│  4. QUALITY VALIDATOR                │
│  (Does output meet standards?)       │
│  • Syntax check                      │
│  • Style compliance                  │
│  • Performance check                 │
└──────────────────────────────────────┘
              ↓
Return to user
```

**Main Content:**
- **Intent Classifier:** Understands what user wants
- **Context Gatherer:** Collects relevant codebase information
- **Specialist Generator:** Uses appropriate expert for task type
- **Quality Validator:** Ensures output meets quality standards
- **Pipeline:** Specialized agents at each step
- **Result:** Higher quality than monolithic approach

**Speaker Notes:**
Copilot uses a four-agent pipeline (simplified; actual implementation likely more complex). Each agent has specific responsibility: understand intent, gather context, generate solution, validate quality. This pipeline approach shows how two-layer thinking scales. Rather than one agent solving the whole problem, you have specialists at each stage. The first agent routes the work to the right path; subsequent agents handle their part. This is orchestrator thinking applied internally.

**Key Concept:** Pipeline architecture chains specialists sequentially

---

### Slide 30: Pattern Recognition Across Tools
**Slide Title:** Common Two-Layer Patterns in AI Tools

**Visual Content:**
```
RECURRING PATTERN ACROSS TOOLS:

┌────────────────────────────────────────┐
│  All Tool Layers:                      │
│                                        │
│  Orchestration Layer:                  │
│  • Plans work                          │
│  • Routes to workers                   │
│  • Makes decisions                     │
│  • Synthesizes results                 │
│                                        │
│  ↓ ↓ ↓ (Delegation)                    │
│                                        │
│  Worker/Specialist Layer:              │
│  • Executes focused task               │
│  • Reports results                     │
│  • Stays in scope                      │
│  • Specializes in domain               │
└────────────────────────────────────────┘

Why This Pattern Appears Everywhere:
✓ Separation of concerns (thinking vs. doing)
✓ Efficiency (specialists better than generalists)
✓ Scalability (easy to add more workers)
✓ Resilience (failure in one worker doesn't crash system)
✓ Parallelization (workers can run simultaneously)


Tool Comparison:

Claude Code     │ Main agent       │ Tasks (ephemeral)
                │ Orchestrates     │ Parallel workers

Aider           │ Architect        │ Editor
                │ Plans changes    │ Implements changes

OpenHands       │ Controller       │ Multiple specialists
                │ Routes work      │ Agents in domains

Copilot         │ Intent classifier→ Specialist pipeline
                │ Routes requests  │ Multi-stage processing
```

**Main Content:**
- **Universal Pattern:** Two-layer appears in diverse tools (AI and non-AI)
- **Naming Varies:** Orchestrator/worker, architect/editor, controller/specialist
- **Core Function:** Thinking layer + doing layer
- **Benefits:** Apply everywhere there's complex work
- **Implementation:** Varies but principle is constant

**Speaker Notes:**
This pattern is so fundamental that it appears across different tools and approaches. Claude Code implements it with explicit tasks. Aider builds it into pair programming. OpenHands uses specialist delegation. Copilot uses pipeline routing. Same principle, different implementations. When you design agent systems, recognize this pattern and apply it consciously. You'll get better results than trying to do everything in one agent.

**Key Concept:** Universal pattern, multiple implementations

---

## SECTION 6: Practical Examples (8-10 slides)

### Slide 31: Example 1: Code Review with Multiple Specialists
**Slide Title:** Practical Example: Multi-Specialist Code Review

**Visual Content:**
```
SCENARIO: Review new backend API module (50 functions)

User Request:
"Please review src/api.py for:
 - Security issues
 - Performance problems
 - Code quality/style
 - Test coverage"

ORCHESTRATOR PLAN:

1. Identify 4 review concerns
2. Spawn 4 parallel review tasks
   - Task 1: Security specialist
   - Task 2: Performance specialist
   - Task 3: Quality specialist
   - Task 4: Testing specialist
3. Collect results
4. Synthesize findings
5. Prioritize recommendations

EXECUTION:

Main Agent spawns:

task: "Review api.py for SECURITY issues.
       Look for: SQL injection, auth bypass,
       data validation, API vulnerabilities"
  --context="src/api.py"
  --name="security-review"
  --timeout=300

task: "Review api.py for PERFORMANCE issues.
       Look for: slow queries, N+1 problems,
       memory leaks, inefficient algorithms"
  --context="src/api.py"
  --name="perf-review"
  --timeout=300

task: "Review api.py for CODE QUALITY.
       Look for: style violations, poor naming,
       duplication, maintainability, documentation"
  --context="src/api.py"
  --name="quality-review"
  --timeout=300

task: "Review api.py for TEST COVERAGE.
       Look for: missing tests, edge cases,
       error handling, mock usage"
  --context="src/api.py"
  --name="testing-review"
  --timeout=300

[Tasks run in parallel: ~3 minutes]

RESULTS:

Security Review:
  ✓ Found 3 critical SQL injection risks
  ✓ Found 1 authentication bypass
  ✓ Data validation weak in 2 endpoints

Performance Review:
  ✓ Found N+1 query problem in get_users()
  ✓ Found inefficient sorting in list_items()
  ✓ Memory issue with large file uploads

Code Quality Review:
  ✓ 15 naming violations
  ✓ 5 duplicated blocks
  ✓ Missing docstrings (8 functions)

Testing Review:
  ✓ Error path untested (3 functions)
  ✓ Edge case: empty input not tested
  ✓ Mock objects incomplete

SYNTHESIS:

Critical Issues (Fix First):
  1. SQL injection in get_user_by_id (SECURITY)
  2. SQL injection in search_items (SECURITY)
  3. Authentication bypass in admin_endpoint (SECURITY)
  4. N+1 queries in get_users (PERFORMANCE)

High Priority (Fix Soon):
  5. Memory leak in file upload
  6. Error paths untested
  7. Missing docstrings in public API

Medium Priority (Fix Before Release):
  8. Code style violations
  9. Test coverage gaps
  10. Naming inconsistencies

EFFICIENCY:
Sequential: 4 reviews × 3 min = 12 minutes
Parallel:   ~3 minutes
Speedup:    4x faster!
```

**Main Content:**
- **Specialization:** Each task handles one review domain
- **Parallelization:** 4 experts work simultaneously on same code
- **Comprehensive:** Covers security, performance, quality, testing
- **Synthesis:** Combines all findings into prioritized report
- **Efficiency:** 4x faster than sequential reviews
- **Quality:** Specialized review better than generalist review

**Speaker Notes:**
This exemplifies the two-layer pattern in practice. Instead of asking one agent to review for security, performance, quality, and testing (spreading its focus), you spawn four specialists who each concentrate on their domain. They work in parallel, each returning findings. The orchestrator synthesizes into one comprehensive report, prioritized by importance. This is both faster and higher quality than serial reviews. Real software teams use this pattern—code reviews involve security, performance, quality, and testing specialists.

**Key Concept:** Specialization through parallelization

---

### Slide 32: Example 2: Feature Implementation Breakdown
**Slide Title:** Practical Example: Building a Complex Feature

**Visual Content:**
```
FEATURE REQUEST:
"Implement real-time notification system with:
 - Web socket connections
 - Message queue for buffering
 - Database persistence
 - User preferences
 - Delivery confirmation"

ORCHESTRATOR ANALYSIS:

This is complex, requires:
1. Understanding existing architecture
2. Designing notification system
3. Implementing 5 components in parallel
4. Integration testing
5. Documentation

Sequential would take days.
Two-layer can parallelize components.

EXECUTION PLAN:

Phase 1: RESEARCH & DESIGN (Subagent - architect)
  Subagent: "Review our architecture.
            Design notification system that integrates."
  Result: Detailed design doc with component specs

Phase 2: COMPONENT BUILD (Tasks - workers in parallel)
  task: "Implement WebSocket connection handler"
  task: "Implement message queue (Kafka interface)"
  task: "Implement database persistence layer"
  task: "Implement user preferences service"
  task: "Implement delivery confirmation"

  [5 tasks run in parallel: ~45 minutes]

Phase 3: INTEGRATION (Task)
  task: "Integrate all 5 components,
         write integration tests"
  Result: Fully functional system

Phase 4: TESTING & DOCS (Tasks in parallel)
  task: "Write unit tests for all components"
  task: "Write API documentation"
  task: "Write deployment guide"

  [3 tasks parallel: ~20 minutes]

TIMELINE:

Sequential (one person):
├─ Research & design: 2 hours
├─ Component 1: 1 hour
├─ Component 2: 1 hour
├─ Component 3: 1 hour
├─ Component 4: 1 hour
├─ Component 5: 1 hour
├─ Integration: 1 hour
├─ Testing: 1 hour
├─ Docs: 1 hour
└─ Total: 10 hours

Two-Layer Orchestration:
├─ Research & design: 2 hours (subagent)
├─ Components 1-5 parallel: 1 hour (5 tasks)
├─ Integration: 1 hour (task)
├─ Testing, Docs, API parallel: 30 min (3 tasks)
└─ Total: ~5 hours (50% faster!)

Plus quality improvement from specialization.
```

**Main Content:**
- **Research Phase:** Architect designs overall approach
- **Build Phase:** Workers implement components in parallel
- **Integration Phase:** Verify components work together
- **Testing Phase:** Parallel testing, documentation
- **Time Savings:** ~50% reduction through parallelization
- **Quality:** Specialized workers → better implementation

**Speaker Notes:**
This shows how two-layer scales to significant features. The orchestrator doesn't build everything; it plans, then delegates to specialists. The architect designs; workers build components in parallel; testing and docs happen simultaneously. This mirrors real team dynamics: one architect, multiple developers building components, testers and writers working in parallel. AI agents can do the same. The key is identifying parallelizable work and exploiting it.

**Key Concept:** Large features split into parallelizable components

---

### Slide 33: Example 3: Bug Investigation Pattern
**Slide Title:** Practical Example: Distributed Bug Investigation

**Visual Content:**
```
SCENARIO: Production bug with unclear root cause
"System crashes when processing large payloads"

ORCHESTRATOR STRATEGY:

1. Gather all information about the issue
2. Spawn investigation tasks for different angles
3. Collect findings
4. Correlate to find root cause

INVESTIGATION TASKS:

task: "Analyze error logs from last 24h.
       Look for patterns before crashes.
       Identify stack traces, error messages."
  --context="logs/error_2024-01-15.log"
  --name="log-analysis"

task: "Review code that processes payloads.
       Look for: buffer overflows, memory leaks,
       inefficient parsing, size limits."
  --context="src/payload_processor.py"
  --name="code-review"

task: "Check infrastructure metrics (CPU, memory,
       disk). Look for spikes correlating with crashes."
  --context="infrastructure/metrics_recent.json"
  --name="metrics-analysis"

task: "Review recent changes (git log).
       Look for commits that might cause crashes
       when processing large payloads."
  --context="git log --oneline -50"
  --name="recent-changes"

task: "Research known issues with large payloads
       in dependencies. Check version compatibility."
  --context="requirements.txt, CHANGELOG.md"
  --name="dependency-check"

[5 tasks run in parallel: ~4 minutes]

FINDINGS:

Log Analysis:
  • Crashes start at 14:30 today
  • Stack trace shows memory allocation failure
  • Last 50 crashes all similar pattern

Code Review:
  • Payload parser allocates full payload to memory
  • No streaming; entire file loaded at once
  • Size limit check missing

Metrics Analysis:
  • Memory usage spikes to 100% before crash
  • Correlates exactly with crash times
  • CPU fine; disk fine

Recent Changes:
  • Commit abc123: "Optimize payload parser for speed"
  • Removed streaming code
  • Added batch processing

Dependency Check:
  • Memory library updated yesterday
  • New version has different allocation behavior
  • Known issue in version 2.1.x

ROOT CAUSE IDENTIFIED:

Recent optimization removed streaming → full payload to memory
+ New dependency version with different allocation
= Out of memory when payload > available memory

Solution:
  Either revert to streaming, or revert dependency,
  or add size limits

EFFICIENCY:
Sequential investigation: ~2 hours
Parallel investigation: ~10 minutes + analysis
Time saved: 90%!
```

**Main Content:**
- **Multi-Angle Investigation:** Different tasks look at different clues
- **Parallel Data Collection:** Analyze logs, code, metrics, changes simultaneously
- **Correlation:** Combine findings to identify root cause
- **Efficiency:** Dramatically faster than sequential investigation
- **Confidence:** Multiple converging lines of evidence

**Speaker Notes:**
Debugging often involves gathering information from multiple angles. Rather than sequentially: analyze logs, then review code, then check metrics, then review changes (hours of time), parallelize: five workers investigate different angles simultaneously (minutes). They each bring their findings; orchestrator correlates and identifies root cause. This pattern is used by incident response teams—different people investigate different angles in parallel. AI agents can do the same, faster and with consistency.

**Key Concept:** Parallel investigation converges on root cause quickly

---

### Slide 34: Example 4: Documentation Generation
**Slide Title:** Practical Example: Generating Comprehensive Documentation

**Visual Content:**
```
SCENARIO: Codebase has 100+ functions; minimal documentation
Need comprehensive docs quickly

USER REQUEST:
"Generate documentation for the payment module.
 Include API reference, examples, integration guide."

ORCHESTRATOR PLAN:

Payment module structure:
├─ charge_card()       [process payment]
├─ refund_charge()     [handle refund]
├─ update_card()       [card management]
├─ create_customer()   [customer setup]
├─ list_charges()      [query charges]
├─ webhook_handler()   [receive events]
├─ validate_card()     [card validation]
├─ apply_coupon()      [discount handling]

DECOMPOSITION:

Break documentation into tasks:

task: "Generate API reference for these functions:
       charge_card, refund_charge, update_card.
       Include: parameters, return values, errors,
       examples. Format as markdown."
  --context="src/payment.py:50-150"
  --name="api-ref-1"

task: "Generate API reference for these functions:
       create_customer, list_charges, webhook_handler.
       Include: parameters, return values, errors,
       examples. Format as markdown."
  --context="src/payment.py:200-300"
  --name="api-ref-2"

task: "Generate API reference for these functions:
       validate_card, apply_coupon.
       Include: parameters, return values, errors,
       examples. Format as markdown."
  --context="src/payment.py:350-400"
  --name="api-ref-3"

task: "Write integration guide showing how to:
       1. Initialize payment module
       2. Charge a card (with error handling)
       3. Handle webhooks
       4. Test locally
       Include code examples, best practices."
  --context="src/payment.py, examples/"
  --name="integration-guide"

task: "Write troubleshooting guide covering:
       • Common errors and solutions
       • Debug techniques
       • Rate limits and quotas
       • Test mode vs production"
  --context="src/payment.py, tests/"
  --name="troubleshooting"

[5 tasks run in parallel: ~8 minutes]

RESULTS COMPILATION:

Combined output:
├─ API Reference (3 task outputs merged)
├─ Integration Guide
├─ Troubleshooting Guide
└─ Example: Complete payment flow

DOCUMENTATION STRUCTURE:

# Payment Module Documentation

## Quick Start
[From integration guide]

## API Reference
### Charge Card
[From api-ref-1]
### Refund Charge
[From api-ref-1]
... etc (all functions from 3 parallel tasks)

## Integration Guide
[From integration-guide task]

## Troubleshooting
[From troubleshooting task]

## Examples
[Complete examples]

EFFICIENCY:
Sequential doc generation: 2-3 hours
Parallel doc generation: ~10 minutes
Quality: Specialized writers per task
```

**Main Content:**
- **Decomposition:** Break docs into independent sections
- **Parallelization:** Multiple writers work on different sections
- **Specialization:** Each task focused on specific doc type
- **Compilation:** Orchestrator assembles into coherent documentation
- **Efficiency:** 12-15x faster than sequential writing
- **Quality:** Specialized tasks produce better docs

**Speaker Notes:**
Documentation often requires explaining different aspects: API reference, integration guide, examples, troubleshooting. Rather than one person or agent writing everything sequentially, spawn workers for each section. They work in parallel, return results, you assemble into comprehensive documentation. This scales beautifully—10 functions to document? One worker. 100 functions? Parallelize into 5-10 workers. Each worker documents a section, returns polished markdown. Orchestrator combines and formats.

**Key Concept:** Documentation parallelizes by section or functionality

---

### Slide 35: Example 5: Batch Testing and Validation
**Slide Title:** Practical Example: Parallel Testing Strategy

**Visual Content:**
```
SCENARIO: New release with 50 test suites
Need to verify all tests pass, identify failures

USER REQUEST:
"Run all test suites. Report results with summary."

CHALLENGE:
50 test suites × 2 min each = 100 minutes sequential
But many tests are independent (no shared state)

TWO-LAYER SOLUTION:

Batch 1: Run tests for different modules (10 parallel)

task: "Run tests for authentication module.
       Report: pass/fail, coverage, slow tests."
  --context="tests/test_auth.py, src/auth.py"
  --name="test-batch-1-auth"

task: "Run tests for payment module."
  --context="tests/test_payment.py, src/payment.py"
  --name="test-batch-1-payment"

task: "Run tests for api module."
  --context="tests/test_api.py, src/api.py"
  --name="test-batch-1-api"

... [7 more tasks, 10 total in batch 1] ...

[Batch 1 runs in parallel: ~3 minutes for all 10]

Batch 2: Run remaining 10 suites
[Another 3 minutes]

... Batches continue until all 50 complete ...

RESULTS COLLECTION:

Batch 1 Results (10 suites):
├─ auth: 47 pass, 2 fail (test_2fa_timeout, test_recovery_codes)
├─ payment: 52 pass, 0 fail
├─ api: 89 pass, 1 fail (test_rate_limit_edge_case)
├─ user: 33 pass, 0 fail
├─ email: 18 pass, 0 fail
├─ cache: 25 pass, 0 fail
├─ storage: 41 pass, 1 fail (test_concurrent_write)
├─ analytics: 29 pass, 0 fail
├─ logger: 15 pass, 0 fail
└─ utils: 44 pass, 0 fail

Batch 2 Results (10 suites):
[Similar breakdown]

... All batches ...

SYNTHESIS:

Total:
├─ Suites run: 50
├─ Tests passed: 2843
├─ Tests failed: 8
├─ Coverage: 87% (average)
├─ Slow tests: 12 (> 1 sec each)

FAILURES (Need investigation):
1. test_2fa_timeout (auth) - timeout too short?
2. test_recovery_codes (auth) - logic error?
3. test_rate_limit_edge_case (api) - boundary condition?
4. test_concurrent_write (storage) - race condition?
[Remaining 4]

RECOMMENDATIONS:
├─ Fix 4 critical failures before release
├─ Investigate 12 slow tests for optimization
├─ Good coverage (87%); target 90%

TIMELINE:
Sequential: 50 suites × 2 min = 100 min
Parallel:   5 batches × 3 min = 15 min + overhead
Speedup:    ~6-7x faster!

With orchestrator spending 2 min to analyze results,
total time: ~17 minutes for 50 suites (vs 100+ min)
```

**Main Content:**
- **Batch Strategy:** Divide tests into parallelizable batches
- **Parallel Execution:** Up to 10 test suites simultaneously
- **Sequential Batching:** Process batches sequentially due to 10-task limit
- **Result Synthesis:** Aggregate results, identify failures
- **Efficiency:** ~6-7x faster than sequential testing
- **Quality Checks:** Coverage, slow tests, failure analysis

**Speaker Notes:**
Testing is perfect for parallelization because tests are typically independent. You can run 10 test suites in parallel, collect results, run 10 more. This is realistic for real projects with many test suites. The orchestrator's job is minimal: send work in batches, collect results, synthesize into report. This pattern is what CI/CD systems do—they parallelize test execution across multiple machines. With AI agents, you do the same thing in software.

**Key Concept:** Batch parallelization scales linear workloads

---

### Slide 36: Best Practices for Two-Layer Design
**Slide Title:** Design Principles for Orchestrator-Worker Systems

**Visual Content:**
```
ORCHESTRATOR BEST PRACTICES:

1. PLAN THOROUGHLY
   ├─ Understand problem completely
   ├─ Identify parallelizable work
   ├─ Break into independent tasks
   └─ Size tasks appropriately

2. PROVIDE CONTEXT EFFICIENTLY
   ├─ Give workers exactly what they need
   ├─ Don't over-provide context
   ├─ Use file/line boundaries
   └─ Respect 200K budget

3. WRITE CLEAR INSTRUCTIONS
   ├─ Specific, detailed task descriptions
   ├─ Include success criteria
   ├─ Note important constraints
   └─ Ask for structured output

4. HANDLE FAILURES GRACEFULLY
   ├─ Expect some workers to fail
   ├─ Use available partial results
   ├─ Retry with modified approach
   └─ Know when to give up and redesign


WORKER BEST PRACTICES:

1. UNDERSTAND SCOPE
   ├─ Read instructions carefully
   ├─ Stay focused on assigned task
   ├─ Don't expand scope
   └─ Ask if unclear (indirectly)

2. USE PROVIDED CONTEXT
   ├─ Rely on provided files/context
   ├─ Don't try to access external info
   ├─ Stay within token budget
   └─ Be efficient with tokens

3. VALIDATE OUTPUT
   ├─ Check result meets criteria
   ├─ Self-test if possible
   ├─ Note edge cases
   └─ Report confidence level

4. REPORT CLEARLY
   ├─ Structure findings
   ├─ Be concise and specific
   ├─ Highlight important issues
   └─ Explain reasoning


SYSTEM DESIGN PRINCIPLES:

┌────────────────────────────────────────┐
│ PRINCIPLE 1: Specialization            │
│ Workers focus on specific domains      │
│ Better results than generalists        │
│                                        │
│ PRINCIPLE 2: Independence              │
│ Tasks should be independent            │
│ Enables parallelization                │
│                                        │
│ PRINCIPLE 3: Isolation                 │
│ Workers don't interfere                │
│ Failures are contained                 │
│                                        │
│ PRINCIPLE 4: Clarity                   │
│ Instructions and context clear         │
│ Results structured and unambiguous     │
│                                        │
│ PRINCIPLE 5: Efficiency                │
│ No wasted context or communication     │
│ Right-sized tasks and batches          │
└────────────────────────────────────────┘
```

**Main Content:**
- **Orchestrator:** Plan well, communicate clearly, handle failures
- **Workers:** Understand scope, stay focused, report structured results
- **System:** Design for specialization, independence, isolation, clarity, efficiency
- **Key Tension:** Parallelization gains vs. overhead of spawning/managing tasks
- **Right-Sizing:** Don't over-engineer simple problems; use two-layer for complex work

**Speaker Notes:**
Good two-layer design requires discipline on both sides. Orchestrators must plan thoroughly; vague instructions lead to poor results. Workers must stay focused; scope creep reduces effectiveness. The system should minimize communication overhead while maximizing parallelization. Not every problem needs two-layer—simple tasks handled better by single agent. But when you have complex, parallelizable work, these principles apply.

**Key Concept:** Specialization, independence, clarity drive success

---

### Slide 37: Common Pitfalls and How to Avoid Them
**Slide Title:** Mistakes in Two-Layer Design

**Visual Content:**
```
PITFALL 1: Over-Parallelization
Problem:
  "Let me parallelize EVERYTHING!"
  Spawn 100 tasks for simple problem
  Overhead outweighs gains

Solution:
  ├─ Use two-layer only for complex work (3+ tasks)
  ├─ Measure: Is speedup worth complexity?
  ├─ For < 2-3 items, single agent better
  └─ Rule: Task > 30 seconds work before parallelizing

Example:
  Bad:  5 files to review → spawn 5 tasks, coordinate
  Good: 5 files to review → one agent reviews all
        50 files to review → spawn 10 tasks (5 per batch)


PITFALL 2: Poor Task Definition
Problem:
  "Do something smart with this code" (vague)
  Worker doesn't know what "smart" means
  Returns unusable results

Solution:
  ├─ Write specific, measurable instructions
  ├─ Include success criteria
  ├─ Provide examples if helpful
  └─ Ask for structured output format

Example:
  Bad:  "Review this code"
  Good: "Review for security issues. Check for:
         SQL injection, XSS, auth bypass, data leaks.
         Return findings as JSON with line numbers."


PITFALL 3: Context Bloat
Problem:
  "I'll provide the entire codebase to each worker"
  Context exceeds 200K; task fails or truncates
  Workers can't focus with so much irrelevant context

Solution:
  ├─ Provide only relevant context
  ├─ Use file/line boundaries
  ├─ Remove unrelated code
  ├─ Respect 200K budget
  └─ If more context needed, redesign task

Example:
  Bad:  All 500 files of codebase to review auth.py
  Good: Just src/auth.py to review auth.py


PITFALL 4: Task Dependency Not Handled
Problem:
  "Task B needs output from Task A"
  Spawn both in parallel
  Task B fails or produces wrong results

Solution:
  ├─ Identify dependencies early
  ├─ Serialize dependent tasks
  ├─ Or pass Task A result to Task B explicitly
  └─ Design tasks to be independent when possible

Example:
  Bad:  Parallelize "design API" and "implement API"
  Good: Seq: Design API (subagent) → Implement (tasks)


PITFALL 5: Ignoring Failure Modes
Problem:
  "All workers will succeed"
  One worker fails; no fallback
  Overall result incomplete

Solution:
  ├─ Expect failures; plan for them
  ├─ Use partial results when possible
  ├─ Retry failed tasks with modifications
  ├─ Synthesize what succeeded
  └─ Flag incomplete/failed tasks clearly


PITFALL 6: Spawning Too Many Tasks
Problem:
  "I'll spawn 50 tasks! Parallelization!"
  Only 10 concurrent allowed
  Creates complex batching logic
  No benefit vs. single agent for small count

Solution:
  ├─ Limit to 10 or fewer tasks
  ├─ If need more: batch sequentially
  ├─ Evaluate: is batching worth it?
  ├─ Single agent often better for < 20 items
  └─ Two-layer for 50+
```

**Main Content:**
- **Over-Parallelization:** Don't parallelize trivial work
- **Poor Definitions:** Clear, specific instructions essential
- **Context Bloat:** Provide only what workers need
- **Unhandled Dependencies:** Identify dependencies early
- **Ignoring Failures:** Plan for partial failures
- **Too Many Tasks:** Respect 10-task limit; batch if needed

**Speaker Notes:**
These are real mistakes teams make. Over-parallelizing simple work adds complexity without benefit. Vague instructions produce vague results. Providing massive context wastes tokens and confuses workers. Parallelizing dependent tasks breaks causality. Not handling failures leads to incomplete results. Trying to spawn 50 tasks at once violates system constraints. Learn these pitfalls; design systems to avoid them. The goal is elegance, not complexity.

**Key Concept:** Avoid over-engineering; match design to problem

---

### Slide 38: Measuring Success: Metrics for Two-Layer Systems
**Slide Title:** How to Evaluate Orchestrator-Worker Performance

**Visual Content:**
```
KEY METRICS:

1. TIME EFFICIENCY
   Metric: Total execution time
   ├─ Compare: Sequential vs. parallel
   ├─ Formula: (Sequential time) / (Parallel time)
   ├─ Goal: 3-8x speedup for well-parallelized work
   └─ Good speedup indicates effective decomposition

   Example:
   └─ Sequential: 20 minutes
      Parallel:   5 minutes (+ 1 min overhead)
      Speedup:    3.3x ✓

2. QUALITY IMPROVEMENT
   Metric: Result quality vs. single agent
   ├─ Does specialization improve results?
   ├─ Fewer errors/bugs found?
   ├─ Better structured output?
   ├─ More comprehensive coverage?
   └─ Goal: 20-40% quality improvement

   Example:
   └─ Single agent code review: 8 bugs found
      Specialist review: 12 bugs found
      Improvement: 50% ✓

3. COST EFFICIENCY
   Metric: Token consumption
   ├─ Tokens used per work unit
   ├─ Overhead of orchestration
   ├─ Compare: Sequential token cost vs parallel
   └─ Goal: Similar or lower total tokens

   Example:
   └─ Single agent: 80K tokens for review
      Orchestrator + 4 workers: 60K tokens
      Savings: 25% ✓

4. FAILURE RECOVERY
   Metric: Robustness
   ├─ % of workers failing
   ├─ Ability to continue with partial results
   ├─ Retry success rate
   ├─ Overall system reliability
   └─ Goal: > 90% success rate

   Example:
   └─ 10 workers; 1 fails; system recovers
      Success rate: 90% ✓

5. SCALABILITY
   Metric: Performance with scale
   ├─ How time increases with problem size
   ├─ Linear scaling (ideal)
   ├─ Sublinear scaling (good)
   ├─ Superlinear scaling (poor)
   └─ Goal: Sublinear or linear

   Example:
   └─ 10 files: 3 min
      20 files: 5 min (not 6 min)
      30 files: 7 min (not 9 min)
      Sublinear due to parallelization ✓

EVALUATION FRAMEWORK:

┌─────────────────────────────────────┐
│ Assess two-layer design:            │
│                                     │
│ Time speedup > 2x? ✓ Continue      │
│ Time speedup < 1.5x? ✗ Redesign   │
│                                     │
│ Quality improvement > 20%? ✓ Keep  │
│ Quality same/worse? ✗ Rethink      │
│                                     │
│ Token efficiency? ✓ Proceed        │
│ Token overhead? ✗ Optimize         │
│                                     │
│ Failure < 5%? ✓ Robust             │
│ Failure > 10%? ✗ Unreliable       │
│                                     │
│ If most checks pass: Good design   │
│ If many fail: Reconsider approach  │
└─────────────────────────────────────┘
```

**Main Content:**
- **Time Efficiency:** Measure speedup; 2-8x is typical
- **Quality:** Specialization often improves results 20-40%
- **Cost:** Total tokens for parallel should be ≤ sequential
- **Reliability:** Failure rate should be < 5-10%
- **Scalability:** Should scale sublinearly with parallelization
- **Decision:** Use metrics to justify two-layer complexity

**Speaker Notes:**
Don't implement two-layer just because it's "cool." Measure its impact. Is it actually faster? Are results better? Is it worth the complexity? Use these metrics to evaluate. If speedup > 2x and quality is good, it's justified. If speedup < 1.5x, you might be over-engineering. Measure failure rates—if more than 10% of workers fail, something is wrong with task design. Use scalability tests: does adding more items/files increase time linearly or sublinearly? Good parallelization should scale sublinearly.

**Key Concept:** Measure impact; use data to justify design

---

### Slide 39: Evolution: From Single-Agent to Two-Layer
**Slide Title:** When and How to Transition to Two-Layer

**Visual Content:**
```
TYPICAL PROJECT EVOLUTION:

Stage 1: SIMPLE PROBLEM
Size: < 1 hour of work
├─ Single agent sufficient
├─ No parallelization benefit
├─ Overhead of coordination > gains
Example: "Fix this bug"

Stage 2: GROWING PROBLEM
Size: 2-4 hours of work
├─ Still single agent, but
├─ Consider if naturally decomposes
├─ Measure: would tasks save time?
Example: "Review these 10 functions"

Stage 3: COMPLEX PROBLEM
Size: 4+ hours of work
├─ Natural decomposition exists
├─ Multiple independent pieces
├─ Parallelization would help
├─ TWO-LAYER is now beneficial
Example: "Build this feature with 5 components"

Stage 4: SCALED PROBLEM
Size: Days of work; many components
├─ Two-layer is essential
├─ Multiple levels of orchestration
├─ Batching and careful resource management
Example: "Full system redesign with 20+ tasks"


TRANSITION INDICATORS:

When to move from single-agent to two-layer:

Green Light (Go to two-layer):
├─ ✓ Project takes 3+ hours
├─ ✓ Work naturally breaks into 3+ independent pieces
├─ ✓ Pieces could be parallelized
├─ ✓ Each piece is 30+ minutes of work
├─ ✓ Team has capacity to manage complexity
├─ ✓ Quality or speed is critical

Yellow Light (Maybe two-layer):
├─ ? Project is 2-3 hours
├─ ? Decomposition is possible but not natural
├─ ? Slight parallelization benefit possible
├─ ? Marginal decision; try both

Red Light (Stick with single-agent):
├─ ✗ Project < 1 hour
├─ ✗ Doesn't decompose naturally
├─ ✗ High interdependencies
├─ ✗ Small number of items (< 3-5)
├─ ✗ Coordination overhead > parallelization gains

TRANSITION PROCESS:

1. Start with single agent
   └─ Simpler, easier to understand
      Build initial solution

2. Profile and measure
   └─ How long did it take?
      Which parts took longest?

3. Identify parallelizable work
   └─ Can any parts run independently?
      How many tasks would that be?

4. Estimate speedup
   └─ Sequential time / N parallel tasks
      Plus overhead (20-30%)

5. Decide
   └─ If speedup > 1.5x: Migrate to two-layer
      If speedup < 1.5x: Keep single-agent

6. Implement two-layer
   └─ Design orchestrator
      Identify tasks
      Test with small batch
      Gradually scale
```

**Main Content:**
- **Simple Problems:** Single-agent is best
- **Growing Problems:** Consider two-layer but not required
- **Complex Problems:** Two-layer becomes essential
- **Scaled Problems:** Two-layer is necessary
- **Transition Triggers:** Time > 3 hours, 3+ pieces, parallelizable
- **Process:** Start simple, measure, decompose, redesign if benefits justify

**Speaker Notes:**
Don't over-engineer from the start. Begin with a single agent. If it takes 30 minutes and works well, you're done. If it takes 2 hours and you identify parallelizable work, consider two-layer. If it takes 5+ hours and naturally decomposes, two-layer is the right choice. The transition should be driven by data, not preconceptions. Measure the single-agent approach, identify bottlenecks, then redesign to parallelize those bottlenecks. This evolutionary approach ensures you're always using the simplest design that solves the problem.

**Key Concept:** Evolve from simple to complex as needed

---

### Slide 40: Summary and Key Takeaways
**Slide Title:** Two-Layer Agent Architecture - Summary

**Visual Content:**
```
CORE CONCEPT:
┌─────────────────────────────────────────────┐
│  Orchestrator-Worker Pattern                │
│  ├─ Orchestrator: Plans, delegates, decides │
│  ├─ Workers: Execute, report, specialize   │
│  └─ Together: Solve complex problems fast   │
└─────────────────────────────────────────────┘

KEY BENEFITS:
✓ Parallelization (3-8x speedup)
✓ Specialization (20-40% quality improvement)
✓ Scalability (easy to add workers)
✓ Resilience (failures isolated)
✓ Clarity (separation of concerns)

WHEN TO USE:
✓ Complex work decomposing into pieces
✓ 3+ independent tasks
✓ Total work > 2-3 hours
✓ Parallelization saves significant time

IMPLEMENTATION IN CLAUDE CODE:
├─ Main agent = Orchestrator
├─ task: "..." = Worker spawning
├─ Up to 10 concurrent tasks
├─ ~200K tokens per task
├─ Automatic context isolation
└─ Native parallelization

PATTERN ACROSS TOOLS:
├─ Aider: Architect/Editor
├─ OpenHands: Controller/Specialists
├─ Copilot: Pipeline stages
├─ Real teams: Managers/Workers
└─ Universal pattern proven at scale

DESIGN PRINCIPLES:
1. Specialization → Better quality
2. Independence → Parallelizable
3. Isolation → Resilient
4. Clarity → Effective
5. Efficiency → Right-sized

PRACTICAL EXAMPLES:
├─ Multi-specialist code review
├─ Parallel feature implementation
├─ Distributed bug investigation
├─ Parallel documentation generation
├─ Batch testing strategy

BEST PRACTICES:
├─ Plan thoroughly
├─ Provide context efficiently
├─ Write clear instructions
├─ Handle failures gracefully
├─ Measure to evaluate


COMMON MISTAKES TO AVOID:
├─ Over-parallelizing simple work
├─ Poor task definitions
├─ Context bloat
├─ Unhandled dependencies
├─ Ignoring failures
├─ Exceeding 10-task limit


DECISION FRAMEWORK:

Is work naturally parallelizable?
├─ YES, and 3+ pieces, and > 2 hrs
│  └─ Use two-layer architecture ✓
│
└─ NO, or < 3 pieces, or < 1 hour
   └─ Single agent better ✓


FINAL THOUGHTS:

Two-layer architecture is powerful but not a
universal solution. Use it when it provides
genuine benefits:
- Significant time savings through parallelization
- Quality improvements through specialization
- Scalability for large problems
- Resilience against individual failures

For simple, quick tasks: stick with single agent
For complex, parallelizable work: leverage two-layer

The pattern appears across AI tools and human
organizations because it fundamentally works.
Mastering it unlocks the next level of agent
effectiveness.

Key insight: Think like a manager, not a worker.
Instead of trying to do everything yourself,
plan the work and delegate to specialists.
That's when agentic systems become truly powerful.
```

**Main Content:**
- **Core:** Orchestrator delegates to workers; specialization + parallelization
- **Benefits:** 3-8x speedup, 20-40% quality improvement, scalability, resilience
- **When:** Complex, parallelizable work, 3+ pieces, 2+ hours
- **Implementation:** Claude Code task tool, ~200K tokens per task, up to 10 concurrent
- **Universal:** Pattern appears in diverse tools and human organizations
- **Key Principle:** Specialization and delegation drive results

**Speaker Notes:**
Two-layer architecture is one of the most powerful patterns for agentic coding. It transforms agents from generalists trying to do everything into specialized teams that parallelize work and dramatically improve results. The pattern is proven—it appears in Aider, OpenHands, Copilot, and every major organization. In Claude Code, you implement it with the task tool. Master this pattern and you can tackle projects that would be impossible for a single agent. But use it judiciously—simpler designs are often better for simpler problems. The art is knowing when to apply which approach.

**Key Concept:** Two-layer: Powerful pattern, use when justified by benefits

