# Part 3: Planning → Building Workflow
## Teaching Agentic Coding Tools to Students

---

## SECTION 1: Why Planning Matters (Slides 1-6)

### Slide 1: Introduction to the Planning-Building Workflow
**Title:** Why Planning Matters Before Building

**Content:**

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   TYPICAL DEVELOPER WORKFLOW                        │
│                                                     │
│   Problem → Code → Debug → Refactor → Deploy        │
│                                                     │
│   vs.                                               │
│                                                     │
│   Problem → Plan → Code → Review → Deploy           │
│                                                     │
│                                                     │
│   The second approach saves TIME and MONEY          │
│                                                     │
└─────────────────────────────────────────────────────┘
```

**Speaker Notes:**
In this section, we explore why planning is crucial before implementing code with agentic tools. Many developers jump directly into coding, but this leads to wasted effort, architectural mistakes, and rework. With agentic tools, planning becomes even more critical because agents can generate large amounts of code rapidly. Poor planning can result in generating thousands of lines of incorrect or suboptimal code.

We'll examine:
- Real costs of skipping the planning phase
- How planning improves code quality and reduces bugs
- Research backing the effectiveness of planning
- How agentic tools amplify both the benefits and risks

**Try This:**
Ask students to think about the last time they started coding without a plan. What went wrong?

---

### Slide 2: The Cost of Skipping Planning
**Title:** Problems with Jumping Straight to Code

**Content:**

```
COSTS OF NO PLANNING:

┌──────────────────────────────────────────┐
│ Wasted Effort                            │
│ • Code written but never used (~30%)     │
│ • Rework and refactoring                 │
│ • Dead ends and false starts             │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ Architectural Problems                   │
│ • Structural incompatibilities           │
│ • Poor scalability decisions             │
│ • Tight coupling and dependencies        │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ Quality Issues                           │
│ • More bugs (80% logic errors)           │
│ • Harder to test                         │
│ • Difficult to maintain                  │
└──────────────────────────────────────────┘

┌──────────────────────────────────────────┐
│ Team Communication                       │
│ • Unclear requirements                   │
│ • Wrong assumptions                      │
│ • Conflicting implementations            │
└──────────────────────────────────────────┘
```

**Speaker Notes:**
Studies show that 30-40% of code written in unplanned projects is never used or is later discarded. This waste is especially problematic with agentic tools where an agent might generate pages of code in seconds. Without planning, you're amplifying waste.

Key costs:
1. **Wasted Code:** Without clear requirements, developers write features that don't match actual needs
2. **Architecture Issues:** Starting without understanding system design leads to refactoring nightmares
3. **Bug Rate:** Unplanned code has 3-4x higher defect density
4. **Team Issues:** Multiple people building the same thing or building incompatible pieces

**Example:**
A team used Claude Code to quickly build a data pipeline without planning. The agent generated working code, but it didn't match the existing schema. Three days of refactoring ensued.

**Try This:**
Have students estimate: if you waste 30% of effort, how does that affect a 2-month project?

---

### Slide 3: How Planning Improves Results
**Title:** Benefits of Planning Phase

**Content:**

```
PLANNING IMPROVES OUTCOMES:

TIME EFFICIENCY
  No Planning: 100% coding time → 40% wasted
  With Planning: 20% planning → 20% coding → 5% waste
  Result: 35% faster overall delivery

CODE QUALITY
  No Planning: 50-80 bugs per 1000 lines (industry avg)
  With Planning: 5-15 bugs per 1000 lines
  Result: 5-10x fewer bugs in production

ARCHITECTURE
  No Planning: Major rewrites common (20% of projects)
  With Planning: Minimal structural changes (<5%)
  Result: Stable foundations from day one

TEAM ALIGNMENT
  No Planning: Conflicting implementations, rework
  With Planning: Everyone building same vision
  Result: Fewer merge conflicts, faster reviews
```

**Speaker Notes:**
Planning isn't just about reducing waste—it's about directing effort productively. Here are the quantifiable benefits:

1. **Time Efficiency:** A 20% investment in planning often saves 25-35% of total project time through reduced rework
2. **Code Quality:** Planning helps identify edge cases, error conditions, and data flow issues before coding
3. **Architecture:** Clear design prevents costly structural mistakes
4. **Team Coordination:** Shared understanding prevents duplicated or conflicting work

With agentic tools, these benefits are amplified because:
- Agents can implement plans quickly → better ROI on planning time
- Agents make systematic architectural mistakes → planning catches these early
- Agents work from detailed specs → output quality scales with input quality

**Research:**
- McConnell's "Code Complete" shows planning reduces defect density by 5-10x
- IEEE studies show planned projects finish 25-30% faster
- Barry Boehm's spiral model demonstrates planning value in complex projects

**Try This:**
Show students code from two projects: one well-planned, one not. Count bugs and architectural issues.

---

### Slide 4: Research Evidence for Planning Benefits
**Title:** What Research Shows About Planning

**Content:**

```
RESEARCH FINDINGS:

Study: NASA's Software Quality Data
├─ Projects with formal design reviews
│  └─ 0.5 defects per 1000 lines of code
├─ Projects without design phase
│  └─ 4.5 defects per 1000 lines of code
└─ Result: 9x more defects without planning

Study: Microsoft's Code Review Practices (2016)
├─ Code with design discussions pre-review
│  └─ 12% revision rate
├─ Code submitted without discussion
│  └─ 43% revision rate
└─ Result: 3.6x more revisions without planning

Study: Google's Large-Scale Code Changes (LSCC)
├─ Projects with 1-2 week planning phase
│  └─ 95% acceptance on first submission
├─ Projects jumping straight to implementation
│  └─ 62% acceptance on first submission
└─ Result: 3x higher acceptance rate with planning

Study: Stack Overflow Survey 2024
├─ Developers who plan before coding
│  └─ Report 23% higher job satisfaction
│  └─ Produce features 30% faster
├─ Developers who code-first
│  └─ Report more frustration and rework
```

**Speaker Notes:**
The research is clear: planning saves time and improves quality. These aren't just software engineering principles—they're validated by large organizations with millions of lines of code.

Key studies to reference:
1. **NASA JPL Data:** Formal design phases dramatically reduce defects
2. **Microsoft:** Design discussions before coding dramatically improve code review outcomes
3. **Google:** Agentic-style rapid implementations still benefit from planning
4. **Industry surveys:** Developers who plan report higher satisfaction and productivity

With agentic tools, these benefits are even more pronounced because:
- Agents can quickly implement poor designs → planning prevents bad implementations
- Agents work at scale → systematic errors affect more code
- Agents reduce time-to-code → planning ROI is higher

**Discussion Point:**
Why might agentic tools make planning even more important than traditional development?

---

### Slide 5: When Planning Fails (Anti-patterns)
**Title:** How Bad Planning Makes Things Worse

**Content:**

```
PLANNING ANTI-PATTERNS:

1. OVER-PLANNING
   ├─ 60% planning, 40% implementation
   ├─ Creates detailed specs that become outdated
   ├─ Kills flexibility to adapt
   └─ Result: Missing deadlines while "planning perfectly"

2. PLANNING IN ISOLATION
   ├─ One person plans, rest code
   ├─ Missing input from practitioners
   ├─ Misses feasibility issues
   └─ Result: Plans that don't match reality

3. PLANNING WITHOUT RESEARCH
   ├─ Assume you know the domain
   ├─ Miss existing solutions
   ├─ Don't understand constraints
   └─ Result: Reinventing wheels, wrong approaches

4. STATIC PLANS
   ├─ Plan once, follow forever
   ├─ Ignore new information
   ├─ Can't adapt to discoveries
   └─ Result: Following a broken plan to completion

5. NO VALIDATION
   ├─ Plan but never check if it works
   ├─ Discover problems during implementation
   ├─ Major rework late in project
   └─ Result: Worst of both worlds
```

**Speaker Notes:**
Planning can go wrong in several ways. It's not about planning more—it's about planning well. With agentic tools, these anti-patterns are amplified because agents execute plans rapidly.

Key risks:
1. **Over-planning:** Waterfall approach where every detail is planned before any code
2. **Planning in isolation:** Architects who don't code lose touch with feasibility
3. **Missing research:** Not understanding domain, missing existing solutions
4. **Static plans:** Treating plans as immutable rather than living documents
5. **Unvalidated plans:** No prototype or proof-of-concept

With agentic tools:
- Over-planning is especially bad because agents can adapt quickly
- Planning in isolation means agents implement disconnected architectures
- Missing research means agents solve already-solved problems poorly
- Static plans cause agents to generate wrong code repeatedly
- Unvalidated plans get executed at massive scale

**Example:**
A team spent 2 weeks planning a database schema without testing. When implementation started, they discovered the schema didn't support required queries. 1 week of planning + 3 weeks of rework vs. 1 week planning with prototype validation.

**Try This:**
Ask students: What would happen if an agent spent 2 hours coding from a bad plan?

---

### Slide 6: The Planning-Building Mindset
**Title:** Shifting to a Planning Culture

**Content:**

```
FROM THIS:                      TO THIS:
┌─────────────┐                ┌─────────────┐
│ "Just code" │                │ "Understand │
│             │                │  first,     │
│ Speed:      │                │  code fast" │
│ High        │                │             │
│ Quality:    │                │ Speed:      │
│ Low         │                │ High        │
│ Waste:      │                │ Quality:    │
│ High        │                │ High        │
└─────────────┘                │ Waste:      │
                               │ Low         │
                               └─────────────┘

WITH AGENTIC TOOLS:

┌─────────────────────────────────────────────┐
│ "Small Planning Investment = Big Payoff"    │
│                                             │
│ 30 min planning → 2 hours coding            │
│ vs.                                         │
│ 0 min planning → 5 hours coding + rework    │
│                                             │
│ Agent-generated code amplifies both the     │
│ benefits of planning and costs of skipping  │
└─────────────────────────────────────────────┘
```

**Speaker Notes:**
The mindset shift is crucial: planning isn't a delay, it's an acceleration. With agentic tools, the case is even stronger because agents can rapidly implement well-planned solutions.

Key points:
1. **Planning isn't slow:** A 30-minute plan saves hours of rework
2. **Quality compounds:** Better plans → better code → easier maintenance
3. **Agents amplify:** Agents executing good plans produce better results faster
4. **Team alignment:** Planning ensures everyone's on the same page

The goal is to instill a culture where developers:
- Spend 10-20% of time planning/designing
- Spend 70-80% implementing
- Spend 5-10% reviewing/validating
- Treat planning as an investment that pays dividends

**Discussion:**
With tools that can code in seconds, why is planning more important than ever?

**Key Takeaway:**
Planning is not the opposite of speed—it's the path to sustainable speed.

---

## SECTION 2: The Research-Plan-Implement Pattern (Slides 7-16)

### Slide 7: Overview of the Pattern
**Title:** The Research-Plan-Implement-Review Cycle

**Content:**

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│         RESEARCH PHASE                                 │
│    (Understand the problem)                            │
│           ↓                                            │
│    ┌─────────────────────────────────────────────┐    │
│    │ • Explore codebase                          │    │
│    │ • Identify existing solutions                │    │
│    │ • Understand constraints                     │    │
│    │ • Gather requirements                        │    │
│    └─────────────────────────────────────────────┘    │
│           ↓                                            │
│                                                        │
│         PLANNING PHASE                                 │
│    (Design the solution)                               │
│           ↓                                            │
│    ┌─────────────────────────────────────────────┐    │
│    │ • Design architecture                       │    │
│    │ • Decompose into tasks                       │    │
│    │ • Identify dependencies                      │    │
│    │ • Estimate effort                            │    │
│    └─────────────────────────────────────────────┘    │
│           ↓                                            │
│                                                        │
│      IMPLEMENTATION PHASE                              │
│    (Build the solution)                                │
│           ↓                                            │
│    ┌─────────────────────────────────────────────┐    │
│    │ • Code modules                              │    │
│    │ • Write tests                                │    │
│    │ • Integration                                │    │
│    │ • Iterate on feedback                        │    │
│    └─────────────────────────────────────────────┘    │
│           ↓                                            │
│                                                        │
│         REVIEW PHASE                                   │
│    (Validate the solution)                             │
│           ↓                                            │
│    ┌─────────────────────────────────────────────┐    │
│    │ • Test functionality                         │    │
│    │ • Code review                                │    │
│    │ • Performance check                          │    │
│    │ • Documentation review                       │    │
│    └─────────────────────────────────────────────┘    │
│           ↓                                            │
│      LOOP BACK IF NEEDED                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

**Speaker Notes:**
The Research-Plan-Implement-Review pattern is a fundamental workflow for building software with agentic tools. Unlike traditional waterfall, this is iterative—each phase informs the others, and you loop back when needed.

The four phases:

1. **Research Phase:** Understand what you're building and why
   - Explore existing code
   - Find patterns and conventions
   - Understand constraints
   - Clarify requirements

2. **Planning Phase:** Design how you'll build it
   - Architecture and high-level design
   - Task decomposition
   - Dependency mapping
   - Effort estimation

3. **Implementation Phase:** Build the solution
   - Code modules according to plan
   - Write tests
   - Integrate components
   - Address issues as they arise

4. **Review Phase:** Validate what you built
   - Testing (unit, integration, system)
   - Code review
   - Performance verification
   - Documentation check

With agentic tools, this pattern becomes:
- **Research:** Agent explores codebase, developer guides
- **Planning:** Developer writes detailed plan, agent reviews feasibility
- **Implementation:** Agent codes from plan, developer validates
- **Review:** Agent and developer validate together

**Example Workflow:**
A student wants to add a caching layer to an API:
1. **Research:** Explore how API is structured, understand data access patterns
2. **Planning:** Design cache strategy, identify what to cache, plan invalidation
3. **Implementation:** Code cache layer, add tests
4. **Review:** Performance test, code review, documentation

**Try This:**
Walk through a simple feature with this pattern to show how it works.

---

### Slide 8: Deep Dive - Research Phase
**Title:** The Research Phase: Understanding Your Problem

**Content:**

```
RESEARCH PHASE ACTIVITIES:

1. UNDERSTAND THE DOMAIN
   ├─ What problem are you solving?
   ├─ Who is the user?
   ├─ What are the constraints?
   └─ What's the success criteria?

2. EXPLORE THE CODEBASE
   ├─ How is related code structured?
   ├─ What patterns and conventions?
   ├─ What existing solutions?
   ├─ What can you reuse?
   └─ What do you need to extend?

3. IDENTIFY CONSTRAINTS
   ├─ Performance requirements
   ├─ Scalability needs
   ├─ Compatibility requirements
   ├─ Security considerations
   └─ Operational constraints

4. FIND EXISTING SOLUTIONS
   ├─ Are there libraries?
   ├─ Internal solutions to learn from?
   ├─ Best practices in domain?
   ├─ Pitfalls to avoid?
   └─ Related implementations?

5. GATHER REQUIREMENTS
   ├─ Functional requirements
   ├─ Non-functional requirements
   ├─ Edge cases
   ├─ Error conditions
   └─ Future extensibility

AGENT'S ROLE IN RESEARCH:
├─ Search codebase for patterns
├─ Find similar implementations
├─ Identify relevant code sections
├─ Understand existing approaches
└─ Verify your assumptions
```

**Speaker Notes:**
The research phase is where you build understanding. With agentic tools, agents can help dramatically by searching codebases, finding patterns, and identifying similar implementations. However, the developer must guide this research and synthesize findings.

Key activities:

1. **Domain Understanding:** What problem are you solving? Who uses it? What's success?
2. **Codebase Exploration:** How is similar code organized? What patterns exist?
3. **Constraint Identification:** What are the limits? Performance? Scale? Security?
4. **Existing Solutions:** What already exists? What can you reuse or learn from?
5. **Requirements Gathering:** What exactly needs to be built?

With agentic tools, you leverage agents to:
- Search the codebase efficiently
- Find existing patterns and solutions
- Extract code samples
- Identify relevant documentation
- Verify your understanding

**Agent Prompts for Research:**

For codebase exploration:
```
"Search this codebase for all implementations of caching.
Show me:
1. How many caching implementations exist
2. What patterns they use
3. What libraries they depend on
4. Which seems most relevant to our API layer"
```

For constraint identification:
```
"Looking at our API response times and current bottlenecks,
what are the key performance constraints I should know about?
Show me:
1. Current response time targets
2. Cache hit rate targets
3. Memory constraints
4. Database connection limits"
```

**Red Flags During Research:**

- You don't understand the problem
- Conflicting requirements not identified
- Missing critical constraints
- Overlooked existing solutions
- No clear success criteria

**Try This:**
Have students research a feature in your codebase before starting. List all the things they discovered.

---

### Slide 9: Deep Dive - Planning Phase (Part 1)
**Title:** The Planning Phase: Designing Your Solution (Part 1)

**Content:**

```
PLANNING PHASE: HIGH-LEVEL DESIGN

Step 1: DEFINE ARCHITECTURE
┌──────────────────────────────────────────┐
│ How will components interact?             │
│ • Service architecture                    │
│ • Data flow                               │
│ • Key interfaces                          │
│ • Major dependencies                      │
└──────────────────────────────────────────┘

Step 2: IDENTIFY KEY DECISIONS
┌──────────────────────────────────────────┐
│ What are critical choices?                │
│ • Technology choices                      │
│ • Algorithm selection                     │
│ • Storage approach                        │
│ • Caching strategy                        │
│ • Error handling approach                 │
└──────────────────────────────────────────┘

Step 3: DECOMPOSE INTO TASKS
┌──────────────────────────────────────────┐
│ Break down into manageable pieces         │
│ • Module 1: User authentication           │
│ • Module 2: Data validation               │
│ • Module 3: Cache management              │
│ • Module 4: Monitoring                    │
│ • Module 5: Documentation                 │
└──────────────────────────────────────────┘

Step 4: IDENTIFY DEPENDENCIES
┌──────────────────────────────────────────┐
│ What depends on what?                     │
│ Module 1 → Module 3 (cache needs auth)    │
│ Module 2 → Module 3 (validate before cache)
│ Module 3 → Module 4 (log cache events)    │
│ All → Module 5 (document everything)      │
└──────────────────────────────────────────┘

OUTPUT: ARCHITECTURE DOCUMENT
┌─────────────────────────────────────────────┐
│ 1. System diagram showing components        │
│ 2. Data flow showing how data moves         │
│ 3. Module descriptions and interfaces       │
│ 4. Dependencies between modules             │
│ 5. Key decisions and rationales             │
└─────────────────────────────────────────────┘
```

**Speaker Notes:**
The planning phase translates research findings into a concrete design. This is where you decide:
- What will you build?
- How will it fit together?
- What's the order of work?
- What are the key decisions?

Key steps:

1. **Architecture Definition:** Draw the big picture. How do components interact?
2. **Key Decisions:** What are non-obvious technical choices? Document why.
3. **Task Decomposition:** Break work into implementable modules (3-8 hour chunks)
4. **Dependency Mapping:** What must be built first? What depends on what?

With agentic tools, planning becomes a collaborative process:
- Developer sketches architecture
- Agent validates feasibility
- Agent identifies what's missing
- Developer refines plan
- Agent codes from refined plan

**Planning Document Template:**

```markdown
# Implementation Plan

## Architecture Overview
[Diagram showing components]

## Key Decisions
1. Use Redis for caching (not Memcached) because:
   - Built-in data structures
   - Better support for expiration
   - Cluster support for future scaling
2. Implement cache invalidation via events not TTL because:
   - Ensures consistency
   - Handles cache invalidation triggers

## Task Breakdown
### Task 1: Cache Interface Definition (4h)
- Define cache interface
- Document contract
- Write unit test stubs

### Task 2: Redis Implementation (6h)
- Implement cache interface for Redis
- Add connection pooling
- Add error handling

[... more tasks ...]

## Dependencies
- Task 1 must complete before Tasks 2-4
- Tasks 2-4 can be parallel
- Task 5 depends on 2-4

## Effort Estimate
Total: 32 hours (~1 week)
```

**Agent's Role in Planning:**
- Validate architectural choices
- Identify feasibility issues
- Find similar implementations to learn from
- Suggest alternative approaches
- Estimate implementation effort

**Try This:**
Have students create a planning document for a medium feature. Have agent review it.

---

### Slide 10: Deep Dive - Planning Phase (Part 2)
**Title:** The Planning Phase: Detailed Task Decomposition

**Content:**

```
DETAILED TASK DECOMPOSITION:

Feature: Add API Request Caching Layer
└─ Effort: ~40 hours

PHASE 1: SETUP AND FOUNDATION (12 hours)
├─ Task 1.1: Design cache architecture (2h)
│  ├─ Create architecture document
│  ├─ Define cache interface
│  └─ Identify integration points
├─ Task 1.2: Set up testing infrastructure (3h)
│  ├─ Create test fixtures
│  ├─ Mock cache layer
│  └─ Set up performance benchmarks
├─ Task 1.3: Dependency setup (2h)
│  ├─ Add Redis client library
│  ├─ Add configuration handling
│  └─ Add health check endpoint
└─ Task 1.4: Documentation structure (5h)
   ├─ Create cache API docs
   ├─ Add usage examples
   └─ Document cache invalidation

PHASE 2: CORE IMPLEMENTATION (20 hours)
├─ Task 2.1: Cache interface layer (3h)
│  ├─ Define abstract interface
│  ├─ Create in-memory implementation
│  └─ Write interface tests
├─ Task 2.2: Redis implementation (5h)
│  ├─ Connect to Redis
│  ├─ Implement get/set/delete
│  ├─ Add key formatting
│  └─ Error handling
├─ Task 2.3: Cache invalidation (4h)
│  ├─ Event-based invalidation
│  ├─ Selective vs full clear
│  └─ Test invalidation flows
├─ Task 2.4: Performance optimization (5h)
│  ├─ Batch operations
│  ├─ Connection pooling
│  ├─ Memory management
│  └─ Benchmarking
└─ Task 2.5: Monitoring and metrics (3h)
   ├─ Cache hit/miss rates
   ├─ Performance metrics
   └─ Alert configurations

PHASE 3: INTEGRATION (5 hours)
├─ Task 3.1: API layer integration (2h)
│  ├─ Add caching to endpoints
│  ├─ Configure cache strategy
│  └─ Test with real API calls
└─ Task 3.2: Full integration testing (3h)
   ├─ End-to-end tests
   ├─ Cache invalidation tests
   └─ Performance verification

PHASE 4: POLISH (3 hours)
├─ Task 4.1: Code review and cleanup
├─ Task 4.2: Documentation review
└─ Task 4.3: Migration guide for team

DEPENDENCIES:
Phase 1 ├─→ Phase 2 (Foundation before impl)
Phase 2 ├─→ Phase 3 (Implementation before integration)
Phase 3 ├─→ Phase 4 (Integration before polish)

Within Phase 2:
- Task 2.1 must complete before 2.2
- Task 2.2 must complete before 2.3
- Tasks 2.3 and 2.4 can be parallel
- Task 2.5 can start once 2.2 is complete

CRITICAL PATH: 1.1→1.4→2.1→2.2→2.3→3.1→3.2→4.1
This determines minimum time (16 hours)
```

**Speaker Notes:**
Good task decomposition is crucial for agentic tools. When you decompose work well:
- Agents can implement each task independently
- Testing is clearer (each task has its own tests)
- Integration is simpler (clear interfaces between tasks)
- Parallel work is possible

Key principles for decomposition:

1. **Task Independence:** Each task should depend on minimal other tasks
2. **Task Size:** 3-8 hour tasks are ideal (not too big, not too granular)
3. **Clear Interfaces:** Each task has clear inputs and outputs
4. **Testability:** Each task can be tested independently
5. **Sequential Logic:** Some tasks must precede others (dependencies)

**How to Decompose:**

Start with your architecture:
```
Architecture → Major Components → Sub-components → Tasks
```

For the caching example:
```
Cache Layer
├─ Interface Definition
├─ Redis Implementation
├─ Invalidation System
├─ Monitoring
└─ API Integration
```

Then break each into 3-8 hour tasks:
```
Interface Definition
├─ Design interface (2h)
├─ Create test stubs (1h)
└─ Documentation (2h)
```

**Dependencies Analysis:**

Create a dependency matrix:
```
         1.1  1.2  1.3  1.4  2.1  2.2  2.3  2.4  2.5  3.1  3.2  4.1
1.1      -    -    -    X    X    X    X    X    X    X    X    -
1.2      -    -    -    -    X    X    X    X    X    -    -    -
1.3      -    -    -    -    -    X    -    -    -    -    -    -
1.4      -    -    -    -    -    -    -    -    -    -    -    -
...
```

X = dependency
- = no dependency

**With Agentic Tools:**

Good decomposition helps agents:
- **Understand boundaries:** Each agent can focus on one task
- **Find tests:** Clear task boundaries → clear test requirements
- **Integrate smoothly:** Well-defined interfaces → easy integration
- **Parallelize:** Independent tasks can be coded by different agents

**Red Flags:**

- Tasks depend on each other in circles
- Tasks are >12 hours (too big)
- Tasks are <1 hour (too granular)
- No clear interface between tasks
- Unclear what "done" means

**Try This:**
Have students decompose a feature into tasks. Check for dependencies and sizing.

---

### Slide 11: Deep Dive - Implementation Phase
**Title:** The Implementation Phase: Building from Plans

**Content:**

```
IMPLEMENTATION WORKFLOW WITH AGENTS:

INPUT: Well-designed plan with task breakdown
       ↓
┌──────────────────────────────────────────┐
│ AGENT PREPARATION                        │
├──────────────────────────────────────────┤
│ 1. Review the complete plan               │
│ 2. Ask clarifying questions              │
│ 3. Identify any ambiguities              │
│ 4. Propose implementation approach       │
│ 5. Get developer approval                │
└──────────────────────────────────────────┘
       ↓
FOR EACH TASK:
┌──────────────────────────────────────────┐
│ 1. Review task specifications             │
│    ├─ What are inputs?                    │
│    ├─ What should output be?              │
│    ├─ What are constraints?               │
│    └─ What tests are needed?              │
├──────────────────────────────────────────┤
│ 2. Plan implementation approach          │
│    ├─ What code to write?                 │
│    ├─ What's the structure?               │
│    ├─ What existing code to use?          │
│    └─ What tests to write?                │
├──────────────────────────────────────────┤
│ 3. Implement the task                     │
│    ├─ Write the code                      │
│    ├─ Write tests                         │
│    ├─ Run tests                           │
│    ├─ Fix failures                        │
│    └─ Verify against spec                 │
├──────────────────────────────────────────┤
│ 4. Code review                            │
│    ├─ Self-review against requirements    │
│    ├─ Check code quality                  │
│    ├─ Verify test coverage                │
│    ├─ Performance check                   │
│    └─ Prepare for developer review        │
└──────────────────────────────────────────┘
       ↓
DONE: Task complete, ready for next task


KEY PRINCIPLE:
Tasks implemented in sequence respecting dependencies
Test each task before moving to next
Integration happens as you go
Review happens continuously
```

**Speaker Notes:**
Implementation with agentic tools is different from traditional coding. The agent becomes a productive partner if you:
- Provide clear specifications
- Review work carefully
- Give good feedback
- Keep task size manageable

The implementation workflow:

1. **Preparation:** Agent understands the plan and asks questions
2. **Task Review:** Agent clarifies task requirements
3. **Approach Planning:** Agent proposes implementation strategy
4. **Implementation:** Agent codes, writes tests, verifies
5. **Review:** Agent self-reviews before submitting

Key practices:

1. **One task at a time:** Complete and test each task before moving on
2. **Test as you go:** Write tests, run them, fix failures
3. **Continuous review:** Check each task against spec
4. **Feedback loops:** Give agent clear feedback on issues
5. **Integration points:** Test how tasks fit together

**Implementation with Claude Code (Agent Tool):**

```
You: "Here's the plan for the caching layer. Task 1.1 is to
design the cache interface. Let me give you the requirements..."

[Provide detailed task spec, existing code, test examples]

Claude: "I understand. The cache interface needs to:
- Support get/set/delete operations
- Handle serialization
- Support TTL
- Return typed results

Before I implement, should I:
1. Use an abstract base class or protocol?
2. Support sync and async?
3. How should errors be handled?"

You: "Use a protocol. Sync only for now. Errors via
exceptions for now, we'll standardize later."

Claude: [Implements interface with tests, shows you the code]

You: "Looks good. The test coverage is weak on serialization.
Can you add more test cases?"

Claude: [Adds test cases, shows updated code]

You: "Perfect. This is ready for the next task."
```

**What Can Go Wrong:**

1. **Agent doesn't understand task scope:** Be specific and clear
2. **Agent misses test cases:** Ask for comprehensive tests
3. **Agent makes wrong architectural choices:** Review approach before coding
4. **Agent doesn't follow existing patterns:** Show examples of existing code
5. **Agent writes untested code:** Require tests upfront

**Developer's Role During Implementation:**

- **Guide:** Clarify what's needed
- **Review:** Check work against requirements
- **Validate:** Run tests, verify behavior
- **Adjust:** Provide feedback and course corrections
- **Integrate:** Ensure tasks work together

**Tips for Effective Implementation:**

1. **Be specific:** The more detail, the better the code
2. **Show examples:** Provide code examples of what you want
3. **Review early:** Don't wait until the task is "done"
4. **Test rigorously:** Require comprehensive tests
5. **Integrate often:** Test how tasks fit together

**Try This:**
Have students implement one task from their plan. Compare results of clear vs vague specifications.

---

### Slide 12: Deep Dive - Review Phase
**Title:** The Review Phase: Validation and Quality Assurance

**Content:**

```
REVIEW PHASE ACTIVITIES:

LEVEL 1: UNIT TESTING
├─ Each module tested in isolation
├─ Test happy path
├─ Test error cases
├─ Test edge cases
├─ Verify test coverage >80%

LEVEL 2: INTEGRATION TESTING
├─ Modules tested together
├─ Test data flows between modules
├─ Test error propagation
├─ Test performance with realistic data

LEVEL 3: SYSTEM TESTING
├─ Full system tested end-to-end
├─ Test complete workflows
├─ Test with real data scale
├─ Test performance and resource use

LEVEL 4: CODE REVIEW
├─ Check against code standards
├─ Verify follows project conventions
├─ Look for maintainability issues
├─ Check for security issues
├─ Verify error handling

LEVEL 5: DOCUMENTATION REVIEW
├─ API documentation accurate
├─ Examples are correct
├─ Edge cases documented
├─ Configuration documented
├─ Troubleshooting guide exists

LEVEL 6: ACCEPTANCE TESTING
├─ Does it solve original problem?
├─ Does it meet all requirements?
├─ Does it meet non-functional requirements?
├─ Is performance acceptable?
├─ Are stakeholders satisfied?


REVIEW CHECKLIST:

┌─ Functionality ─────────────────────────────┐
│ ☐ All requirements implemented              │
│ ☐ All edge cases handled                    │
│ ☐ Error cases handled gracefully            │
│ ☐ Works with real data                      │
└─────────────────────────────────────────────┘

┌─ Quality ───────────────────────────────────┐
│ ☐ Code follows project standards            │
│ ☐ No dead code or TODOs                     │
│ ☐ Reasonable complexity                     │
│ ☐ Good error messages                       │
└─────────────────────────────────────────────┘

┌─ Testing ───────────────────────────────────┐
│ ☐ Test coverage >80%                        │
│ ☐ All tests pass                            │
│ ☐ Tests are meaningful                      │
│ ☐ Edge cases tested                         │
└─────────────────────────────────────────────┘

┌─ Documentation ─────────────────────────────┐
│ ☐ API documented                            │
│ ☐ Usage examples provided                   │
│ ☐ Configuration documented                  │
│ ☐ Edge cases noted                          │
└─────────────────────────────────────────────┘

┌─ Performance ───────────────────────────────┐
│ ☐ Meets performance requirements            │
│ ☐ No obvious inefficiencies                 │
│ ☐ Resource usage acceptable                 │
│ ☐ Scales as required                        │
└─────────────────────────────────────────────┘

┌─ Security ──────────────────────────────────┐
│ ☐ No obvious security issues                │
│ ☐ Inputs validated                          │
│ ☐ Error messages don't leak info            │
│ ☐ Follows security best practices           │
└─────────────────────────────────────────────┘
```

**Speaker Notes:**
Review is where you verify that what was built matches what was planned. With agentic tools, review is even more critical because agents can generate large amounts of code that needs validation.

The review process has multiple levels:

1. **Unit Testing:** Does each module work correctly?
2. **Integration Testing:** Do modules work together?
3. **System Testing:** Does the whole system work?
4. **Code Review:** Is the code quality good?
5. **Documentation:** Is everything documented?
6. **Acceptance:** Does it solve the original problem?

Key review practices:

1. **Test comprehensively:** Unit, integration, and system tests
2. **Review early:** Don't wait until everything's done
3. **Check against spec:** Does it match the plan?
4. **Verify assumptions:** Were all constraints met?
5. **Look for debt:** Is this maintainable long-term?

**Testing Strategy:**

For each task, you need:
- **Unit tests:** Testing functions/methods in isolation
- **Integration tests:** Testing how components work together
- **System tests:** Testing complete workflows

Example for cache implementation:
```
Unit Tests:
- Test cache.get() returns correct value
- Test cache.set() stores value
- Test cache.delete() removes value
- Test TTL expiration
- Test serialization/deserialization
- Test error handling

Integration Tests:
- Test cache works with API endpoints
- Test invalidation triggers cache clear
- Test multiple concurrent requests

System Tests:
- Test full request cycle with caching
- Test cache invalidation in real scenario
- Test performance with realistic data
```

**Code Review Checklist:**

Before accepting implementation, review:
1. **Correctness:** Does it do what was specified?
2. **Readability:** Is code easy to understand?
3. **Maintainability:** Will future changes be easy?
4. **Performance:** Does it meet performance goals?
5. **Security:** Are there security issues?
6. **Error Handling:** Are errors handled properly?
7. **Tests:** Are there sufficient tests?
8. **Documentation:** Is it documented?

**Common Issues Found in Review:**

1. **Missing edge cases:** Code doesn't handle all scenarios
2. **Poor error messages:** Errors aren't helpful
3. **Untested code:** Missing test coverage
4. **Performance issues:** Slow or resource-heavy
5. **Security gaps:** Unvalidated inputs
6. **Unclear code:** Hard to understand or maintain
7. **Incomplete documentation:** Examples missing

**Review Questions to Ask:**

- "What happens if this fails?"
- "Can this be called with bad input?"
- "What's the worst-case performance?"
- "Is this testable?"
- "Will the next developer understand this?"
- "Is this consistent with existing patterns?"

**With Agentic Tools:**

Review is especially important because:
- Agents generate code quickly → easy to miss issues
- Agents might not understand domain subtleties
- Agent-generated code often needs refinement
- Tests might not be comprehensive enough

**Try This:**
Have students review code from the implementation phase. What issues do they find?

---

### Slide 13: Example: Feature Implementation
**Title:** Complete Workflow Example - Adding User Authentication

**Content:**

```
EXAMPLE: ADD JWT AUTHENTICATION TO REST API

RESEARCH PHASE (2 hours)
├─ Explored existing auth code
│  └─ Found session-based auth, wants to add JWT
├─ Identified constraints
│  ├─ Must support existing session users
│  ├─ Should work with mobile clients
│  └─ Must be backward compatible
├─ Found existing patterns
│  ├─ Error handling uses custom exceptions
│  ├─ Config loaded from environment
│  └─ Tests use fixtures
└─ Clarified requirements
   ├─ JWT for new API clients
   ├─ Include user ID and roles in token
   ├─ Tokens expire after 24 hours
   └─ Refresh tokens available for 30 days

PLANNING PHASE (2 hours)
├─ Architecture design
│  ├─ Add JWT creation service
│  ├─ Add JWT validation middleware
│  ├─ Add token refresh endpoint
│  └─ Update existing endpoints to accept JWT
├─ Key decisions
│  ├─ Use PyJWT library (already in project)
│  ├─ Store tokens in Redis for blacklist/refresh
│  ├─ Add JWT to Authorization header
│  └─ Keep session auth as fallback
└─ Task breakdown
   ├─ Task 1: JWT service (4h)
   ├─ Task 2: Validation middleware (3h)
   ├─ Task 3: Refresh endpoint (2h)
   ├─ Task 4: Update API endpoints (3h)
   └─ Task 5: Tests + docs (4h)

IMPLEMENTATION PHASE (16 hours)
│
├─ Task 1: JWT Service (4h) ✓
│  ├─ Created jwt_service.py module
│  ├─ Implemented create_token(), verify_token()
│  ├─ Handles token expiration
│  ├─ Written 12 unit tests
│  └─ All tests passing
│
├─ Task 2: Validation Middleware (3h) ✓
│  ├─ Created middleware.py
│  ├─ Handles Authorization header parsing
│  ├─ Falls back to session authentication
│  ├─ Returns appropriate errors
│  ├─ Written 8 integration tests
│  └─ All tests passing
│
├─ Task 3: Refresh Endpoint (2h) ✓
│  ├─ Created /auth/refresh endpoint
│  ├─ Validates refresh token
│  ├─ Returns new JWT and refresh token
│  ├─ Written 5 tests for edge cases
│  └─ All tests passing
│
├─ Task 4: Update API Endpoints (3h) ✓
│  ├─ Added JWT support to existing endpoints
│  ├─ Updated 8 endpoints
│  ├─ Maintained backward compatibility
│  ├─ Added integration tests
│  └─ All tests passing
│
└─ Task 5: Tests + Documentation (4h) ✓
   ├─ Added security tests
   ├─ Performance testing
   ├─ Wrote API documentation
   ├─ Created migration guide
   └─ All tests passing

REVIEW PHASE (3 hours)
│
├─ Unit Testing ✓
│  ├─ 47 unit tests all passing
│  ├─ Code coverage: 92%
│  └─ All edge cases covered
│
├─ Integration Testing ✓
│  ├─ JWT creation and validation flow
│  ├─ Token refresh flow
│  ├─ Session fallback still works
│  ├─ 23 integration tests passing
│  └─ Backward compatibility verified
│
├─ System Testing ✓
│  ├─ Full API request cycle with JWT
│  ├─ Mobile client simulation
│  ├─ Performance acceptable
│  └─ 15 system tests passing
│
├─ Code Review ✓
│  ├─ Follows project conventions
│  ├─ Proper error handling
│  ├─ No security issues found
│  ├─ Performance acceptable
│  └─ Code is maintainable
│
├─ Documentation ✓
│  ├─ API docs complete
│  ├─ Usage examples provided
│  ├─ Configuration documented
│  └─ Troubleshooting guide included
│
└─ Acceptance ✓
   ├─ All requirements met
   ├─ Backward compatible
   ├─ Performance acceptable
   └─ Ready for deployment

TOTAL TIME: 2 + 2 + 16 + 3 = 23 hours
ESTIMATED: 20 hours
Variance: +15% (within acceptable range)
```

**Speaker Notes:**
This example shows the complete workflow from research through review. Notice how:
- Research up front saved mistakes during implementation
- Clear planning made implementation straightforward
- Good task decomposition allowed parallel work
- Testing caught issues early
- Review verified everything works

Key lessons:
1. **Research time is well spent:** Found existing patterns, understood constraints
2. **Clear planning:** Minimal surprises during implementation
3. **Small tasks:** Each task was manageable and testable
4. **Early testing:** Tests caught issues as they arose
5. **Comprehensive review:** Verified it works end-to-end

The 23-hour actual vs. 20-hour estimate is good—within 15% variance.

**Agent Prompts Used:**

Research phase:
```
"Explore this codebase and tell me:
1. How is authentication currently handled?
2. What patterns and conventions are used?
3. What libraries are available?
4. Where would new auth code fit?"
```

Planning phase:
```
"Review this plan for adding JWT authentication.
Do you see any feasibility issues?
Can you suggest any improvements?
Does the task decomposition make sense?"
```

Task 1 implementation:
```
"Implement a JWT service with these functions:
- create_token(user_id, roles, expires_in)
- verify_token(token)
- refresh_token(refresh_token)

Use PyJWT library.
Follow the error handling patterns in this file [example].
Write comprehensive tests.
Here's a test example to follow."
```

Review phase:
```
"Review this JWT implementation:
1. Does it meet all requirements?
2. Are there security issues?
3. Is test coverage adequate?
4. Is error handling comprehensive?"
```

**Try This:**
Walk students through this example step by step. Have them identify what happened at each phase.

---

### Slide 14: Example: Bug Fix Planning
**Title:** Workflow Example - Diagnosing and Fixing a Performance Bug

**Content:**

```
EXAMPLE: FIX DATABASE QUERY PERFORMANCE BUG

PROBLEM: API endpoint returns 200ms response time, should be <50ms

RESEARCH PHASE (1.5 hours)
├─ Understood the problem
│  ├─ Slow endpoint: GET /api/users/{id}/posts
│  ├─ Current: 200ms
│  ├─ Target: <50ms
│  └─ Affects mobile experience
├─ Explored the code
│  ├─ Found the endpoint implementation
│  ├─ Identified database queries
│  ├─ Found N+1 query problem
│  │  └─ Getting user, then loading all posts one-by-one
│  └─ Checked if this was known issue
├─ Identified constraints
│  ├─ Can't change API response format
│  ├─ Must maintain backward compatibility
│  ├─ Cache options: Redis available
│  └─ Database: PostgreSQL
└─ Profiling data
   ├─ 95% time in database queries
   ├─ N+1 problem confirmed
   ├─ 1 user query + 50 post queries = 51 queries
   └─ Batch query takes <5ms

PLANNING PHASE (1 hour)
├─ Root cause analysis
│  └─ N+1 query problem: user then each post separately
├─ Solution options
│  ├─ Option A: Batch query (join) - simplest
│  ├─ Option B: Caching - complex, might be overkill
│  ├─ Option C: GraphQL - bigger change
│  └─ Chose Option A: Batch query
├─ Implementation plan
│  ├─ Task 1: Refactor to batch query (1h)
│  ├─ Task 2: Write performance test (0.5h)
│  ├─ Task 3: Code review and verify (0.5h)
│  └─ Task 4: Update tests (0.5h)
└─ Success criteria
   └─ Response time <50ms with same data volume

IMPLEMENTATION PHASE (2.5 hours)
│
├─ Task 1: Refactor to batch query (1h) ✓
│  ├─ Original code:
│  │  user = User.get(id)
│  │  posts = [Post.get(post_id) for post_id in user.post_ids]
│  ├─ New code:
│  │  user = User.get(id)
│  │  posts = Post.query.filter(Post.user_id == id).all()
│  ├─ Tests passing
│  └─ No API changes
│
├─ Task 2: Write performance test (0.5h) ✓
│  ├─ Created benchmark test
│  ├─ Measures response time
│  ├─ Confirms <50ms target
│  └─ Test passing
│
├─ Task 3: Code review (0.5h) ✓
│  ├─ Code follows project patterns
│  ├─ Properly indexed query
│  ├─ Good error handling
│  └─ Documentation clear
│
└─ Task 4: Update tests (0.5h) ✓
   ├─ Updated existing tests
   ├─ Added edge case tests
   ├─ All tests passing
   └─ Coverage maintained

REVIEW PHASE (1 hour)
│
├─ Verify fix ✓
│  ├─ Before: 200ms average
│  ├─ After: 35ms average (71% improvement!)
│  ├─ Worst case still <50ms
│  └─ Consistent across test data sizes
│
├─ Regression testing ✓
│  ├─ All existing tests passing
│  ├─ Related endpoints still work
│  ├─ Error cases still handled
│  └─ Data integrity verified
│
├─ Code review ✓
│  ├─ Follows patterns
│  ├─ Properly tested
│  ├─ Easy to understand
│  ├─ No side effects
│  └─ Performance proven
│
└─ Documentation ✓
   ├─ Problem documented
   ├─ Solution explained
   ├─ Performance gains noted
   ├─ How to prevent similar issues
   └─ Added comment in code

TOTAL TIME: 1.5 + 1 + 2.5 + 1 = 6 hours
```

**Speaker Notes:**
This example shows how the workflow applies to bug fixing. The same principles apply:
- Research to understand root cause
- Plan the minimal fix
- Implement and test
- Review to verify the fix

Key differences from feature implementation:
- Research is about diagnosis, not feature discovery
- Planning focuses on root cause and minimal fix
- Tests focus on regression prevention
- Review includes performance verification

**Why This Matters:**

The bug fix approach differs from feature implementation:
- Feature: "What should we build?" → Research is exploration
- Bug fix: "What's wrong?" → Research is diagnosis

Both use the same workflow, but the focus differs.

**Research Prompts:**

```
"Help me understand this performance issue:
1. Profile the endpoint - where is time spent?
2. Analyze the database queries
3. Identify the pattern causing slowness
4. Are there similar issues elsewhere?"
```

**Planning Prompts:**

```
"I think I found an N+1 query problem. Before I fix it:
1. Confirm that's the issue
2. What are the best ways to fix it?
3. Which fix has least side effects?
4. What tests should I write?"
```

**Implementation Prompts:**

```
"Refactor this endpoint to use batch queries:
1. Keep the API response format the same
2. Write a performance test
3. Make sure all existing tests still pass
4. Verify the fix works"
```

**Common Bug Fix Patterns:**

1. **Performance bugs:** Profile → Find bottleneck → Fix → Measure
2. **Logic bugs:** Understand problem → Reproduce → Diagnose → Fix → Verify
3. **Integration bugs:** Isolate issue → Test in isolation → Fix → Integration test
4. **Security bugs:** Understand vulnerability → Prove issue → Fix → Verify secure

Each follows research-plan-implement-review.

**Try This:**
Have students take a real bug and apply this workflow. Time each phase.

---

### Slide 15: Common Pitfalls and How to Avoid Them
**Title:** What Can Go Wrong in the Research-Plan-Implement Cycle

**Content:**

```
COMMON PITFALLS:

1. SKIPPING RESEARCH
   Symptom: "I know this codebase, let's just code"
   Risk: Miss existing solutions, incompatible with patterns
   Cost: Rework, inconsistent code, duplicated functionality
   Fix: Always spend 10-20% of time on research

2. PLANNING TOO MUCH
   Symptom: Two-week planning phase for one week of work
   Risk: Plan becomes outdated before implementation
   Cost: Frustrated team, missed opportunities
   Fix: Plan just enough to start building (2-3 days max)

3. IGNORING DEPENDENCIES
   Symptom: Task list with circular dependencies
   Risk: Can't start work, blocking
   Cost: Delayed start, team waiting
   Fix: Map dependencies, identify critical path

4. TASKS TOO BIG
   Symptom: "Task 1: Implement entire caching system (40h)"
   Risk: Can't test incrementally, hard to review
   Cost: Rework, hard to debug issues
   Fix: Break into 3-8 hour chunks

5. TASKS TOO SMALL
   Symptom: "Task 1: Add getter method (30 min)"
   Risk: Overhead of task management, context switching
   Cost: Time lost in overhead
   Fix: Aim for 3-8 hour sweet spot

6. AGENT IMPLEMENTING WITHOUT REVIEW
   Symptom: Agent codes for 2 hours without feedback
   Risk: Wrong direction, can't fix mid-task
   Cost: Rework, frustration
   Fix: Review frequently, feedback early and often

7. MISSING TEST PLANNING
   Symptom: Implementation done, tests thought of later
   Risk: Untestable code, missing coverage
   Cost: Hard to test, bugs slip through
   Fix: Plan tests as part of task planning

8. NO ACCEPTANCE CRITERIA
   Symptom: "Task: implement caching" (too vague)
   Risk: Endless scope creep, unclear when done
   Cost: Unclear if work is complete
   Fix: Define specific, measurable acceptance criteria

9. SKIPPING INTEGRATION
   Symptom: All tests pass in isolation, fails when combined
   Risk: Late discovery of integration issues
   Cost: Rework during final stages
   Fix: Integration tests as part of implementation


PITFALL CHECKLIST:

Before starting implementation, verify:
☐ Research phase completed (know existing code)
☐ All constraints identified
☐ Plan is clear (could someone else follow it?)
☐ Tasks are 3-8 hours
☐ Dependencies mapped correctly
☐ Tests planned before coding
☐ Acceptance criteria defined
☐ Integration points clear
☐ Code review process ready
☐ Review/test strategy ready
```

**Speaker Notes:**
These pitfalls are common even in experienced teams. With agentic tools, they're even more dangerous because agents can rapidly amplify mistakes. A bad plan executed quickly by an agent is worse than a bad plan with slow manual coding.

Key mitigation strategies:

1. **Skipping Research:** Always spend 10-20% of time understanding the domain and existing code
2. **Over-planning:** Plan just enough to start (2-3 days), then refine based on learning
3. **Ignoring Dependencies:** Draw dependency diagrams, identify critical path
4. **Wrong Task Size:** Aim for 3-8 hours; if >12h, break down; if <1h, combine
5. **No Review:** Get feedback frequently, don't let agent code for hours without review
6. **Missing Tests:** Design tests as part of task planning, not after
7. **Vague Acceptance Criteria:** Define specific, measurable, verifiable criteria
8. **No Integration Testing:** Test how components work together, not just individually
9. **Agent Problems:** Agent acts on what you tell it; if you're vague, it produces vague code

**How to Review Plans Before Implementation:**

```
Review checklist for a plan:

Clarity:
□ Anyone could follow this plan
□ No ambiguous terms
□ All assumptions stated
□ Constraints listed

Completeness:
□ All components covered
□ Error cases included
□ Edge cases noted
□ Integration points clear

Feasibility:
□ Tasks are achievable
□ Dependencies are correct
□ Estimates are realistic
□ Resources are available

Testability:
□ Can test each task independently
□ Clear test criteria
□ Acceptance criteria defined
□ Integration strategy clear
```

**Try This:**
Have students review each other's plans for these pitfalls before starting implementation.

---

### Slide 16: Chapter Summary
**Title:** The Research-Plan-Implement-Review Pattern: Key Takeaways

**Content:**

```
PATTERN OVERVIEW:

Research → Plan → Implement → Review → [Loop if needed]

WHY IT WORKS:
├─ Research prevents missed context
├─ Planning prevents wrong implementations
├─ Implementation translates design to code
├─ Review verifies everything works
└─ Loop allows continuous improvement

TIME ALLOCATION (for typical feature):
├─ Research: 10-15% (1-2 weeks of effort)
├─ Planning: 10-15% (1-2 weeks of effort)
├─ Implementation: 60-75% (6-10 weeks of effort)
├─ Review: 5-10% (1-2 weeks of effort)
└─ Total: 10-16 weeks for significant feature

WITH AGENTIC TOOLS (same feature):
├─ Research: 10-15% (agent helps explore faster)
├─ Planning: 10-15% (more detailed plans work better with agents)
├─ Implementation: 40-50% (agents code faster)
├─ Review: 10-15% (more important because agent code needs verification)
└─ Total: 6-10 weeks (40% faster delivery)

KEY PRINCIPLES:

1. Research Thoroughly
   └─ Prevents costly mistakes later

2. Plan Before Building
   └─ Small investment in plan saves big time in rework

3. Implement Task by Task
   └─ Test each task before starting next

4. Review Everything
   └─ Catches issues early when they're cheap to fix

5. Use Agents to Amplify Your Planning
   └─ Good plans → good agent code
   └─ Poor plans → poor agent code
   └─ Planning skill becomes more important, not less


WHEN TO USE THIS PATTERN:

✓ Use always for:
├─ New features (anything >1 day)
├─ Architecture changes
├─ Performance optimizations
├─ Integration work
└─ Complex bug fixes

✓ Can skip for:
├─ Trivial fixes (<1 hour)
├─ Simple bug fixes
├─ Documentation updates
└─ Routine refactoring

✗ Don't skip for:
├─ "Just quick code"
├─ "I know this codebase"
├─ "Let's figure it out as we go"
└─ "Time pressure"
  (Time pressure makes planning MORE important, not less)
```

**Speaker Notes:**
This pattern is fundamental to effective agentic coding. It's not just about organization—it's about ensuring your agent partners can be productive and produce quality code.

The pattern works because:
1. **Research:** Understanding the domain prevents architectural mistakes
2. **Planning:** Design before coding prevents implementing the wrong thing
3. **Implementation:** Building to a spec is faster than improvising
4. **Review:** Testing catches issues when they're cheap to fix

With agentic tools, this becomes even more critical because:
- Agents can produce code faster than you can review it
- Small planning mistakes become large code mistakes
- Agent-generated code needs more careful review
- The agent is only as good as your specifications

**The Bottom Line:**

The cost of planning is small (10-15% of time).
The benefit of planning is large (40%+ time savings through reduced rework).
With agentic tools, this ratio improves even further.

Therefore: **Always plan before building.**

**Next Section:**
Now that you understand the research-plan-implement-review pattern, let's look at how different agentic tools implement planning modes.

**Try This:**
Have students estimate the cost of skipping research and planning on a real project in their codebase.

---

## SECTION 3: Plan Mode in Different Tools (Slides 17-26)

### Slide 17: Introduction to Planning Modes
**Title:** How Different Agentic Tools Support Planning

**Content:**

```
AGENTIC TOOLS AND THEIR PLANNING CAPABILITIES:

┌──────────────────────────────────────────────────────┐
│ TOOL              │ PLANNING MODE        │ STRENGTH  │
├──────────────────────────────────────────────────────┤
│ Claude Code       │ Explicit planning     │ Detailed  │
│ (agentic)         │ before coding         │ analysis  │
├──────────────────────────────────────────────────────┤
│ Cursor            │ Plan mode (beta)      │ IDE-      │
│                   │ with Composer         │ integrated│
├──────────────────────────────────────────────────────┤
│ Aider             │ Architect mode        │ Focused   │
│                   │ for design            │ design    │
├──────────────────────────────────────────────────────┤
│ Codex CLI         │ Read-only planning    │ Research  │
│                   │ phase                 │ oriented  │
├──────────────────────────────────────────────────────┤
│ GitHub Copilot    │ Chat-based planning   │ Interactive│
│                   │ (in Chat)             │           │
└──────────────────────────────────────────────────────┘

WHAT "PLANNING MODE" MEANS:

┌─────────────────────────────────────────┐
│ Traditional Coding Mode:                │
│ Agent → Code immediately                │
│ Risk: Wrong direction early             │
│ Rework: High                            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│ Planning Mode:                          │
│ Agent → Analyze → Plan → Code           │
│ Risk: Wrong direction caught in plan    │
│ Rework: Low                             │
└─────────────────────────────────────────┘

KEY INSIGHT: Planning mode forces the agent
to analyze before implementing, catching
architectural issues before coding.
```

**Speaker Notes:**
Different tools support planning in different ways. Understanding how each tool's planning mode works helps you choose the right tool for the job.

The core idea of planning mode:
1. **Analyze:** Understand the problem
2. **Design:** Create a plan
3. **Get Approval:** Verify the plan before coding
4. **Implement:** Build according to plan
5. **Verify:** Test the implementation

This differs from direct implementation where agents jump straight to coding.

Key benefits of planning modes:
- **Catch errors early:** Architecture issues found before code written
- **Control cost:** Stop bad ideas before expensive code is written
- **Team alignment:** Everyone agrees on approach before coding
- **Iterative refinement:** Plans can be refined based on feedback

**Tool Comparison Dimensions:**

1. **Explicitness:** How clear is the planning phase?
2. **Interactivity:** Can you provide feedback on the plan?
3. **Integration:** How well integrated with IDE?
4. **Scope:** Does planning cover architecture, tasks, tests?
5. **Format:** Is the plan structured, text, diagrams?

We'll explore each tool in detail in the following slides.

---

### Slide 18: Claude Code Plan Mode (Part 1)
**Title:** Claude Code: Explicit Planning Phase (Detailed)

**Content:**

```
CLAUDE CODE PLANNING WORKFLOW:

1. DEVELOPER PROVIDES CONTEXT
   ├─ Problem statement
   ├─ Code samples (what to follow)
   ├─ Constraints and requirements
   ├─ Scale and scope
   └─ Success criteria

2. AGENT ENTERS ANALYSIS MODE
   ├─ Explores the codebase
   ├─ Understands patterns
   ├─ Identifies constraints
   ├─ Finds similar implementations
   └─ Clarifies ambiguities

3. AGENT PROPOSES PLAN
   Output format:
   ├─ High-level approach
   ├─ Architecture overview
   ├─ Task breakdown (with estimates)
   ├─ Key decisions and rationales
   ├─ Potential risks
   ├─ Test strategy
   ├─ Questions for clarification
   └─ Estimated effort

4. DEVELOPER REVIEWS PLAN
   Questions to ask:
   ├─ "Do you understand the requirements?"
   ├─ "Are there feasibility concerns?"
   ├─ "Should we use different approach?"
   ├─ "Are estimates realistic?"
   ├─ "Did you miss anything?"
   └─ "What could go wrong?"

5. AGENT REFINES PLAN
   Based on feedback:
   ├─ Answers clarification questions
   ├─ Adjusts approach if needed
   ├─ Updates estimates
   ├─ Adds missing pieces
   └─ Gets final approval

6. AGENT IMPLEMENTS
   Now that plan is approved:
   ├─ Agent codes each task
   ├─ Developer reviews implementations
   ├─ Tests are written
   ├─ Integration happens
   └─ Delivery-ready code


EXAMPLE CLAUDE CODE PLANNING PROMPT:

"I want to add a caching layer to our API. Here's what I need:

Requirements:
- Cache GET requests for /api/posts endpoint
- 5-minute TTL
- Invalidate on POST/PUT/DELETE
- Support for query parameters in cache key

Context:
- We use FastAPI for the API
- Redis is available
- We have an existing auth middleware pattern
- Tests use pytest with fixtures

Before you start coding, please:
1. Analyze the codebase and existing patterns
2. Propose an architecture for the cache layer
3. Break down into specific tasks with estimates
4. List key decisions and why
5. Identify potential risks
6. Propose test strategy

I'll review your plan before we start building."


WHAT A GOOD PLAN FROM CLAUDE LOOKS LIKE:

Architecture Overview:
- Add caching decorator pattern (following existing decorator in auth)
- Use Redis client existing in requirements.txt
- Cache decorator wraps endpoint functions
- Invalidation via event hooks on POST/PUT/DELETE

Task Breakdown:
1. Cache decorator implementation (3h)
   - Create decorators.py
   - get_cache_key() function
   - @cached_get decorator
   - TTL configuration

2. Redis client setup (1h)
   - Configuration from environment
   - Health check endpoint
   - Error handling

3. Invalidation system (3h)
   - Hook endpoints on mutations
   - Clear specific keys vs full clear
   - Transaction safety

4. Tests (3h)
   - Unit tests for decorator
   - Integration with endpoints
   - Invalidation testing
   - Performance testing

Key Decisions:
1. Decorator pattern because: matches existing code style
2. Event hooks because: minimal endpoint changes
3. Specific key clearing because: preserves some cache

Risks:
1. Cache staleness if invalidation misses cases
2. Memory usage if cache grows unbounded
3. Redis availability dependency

Test Strategy:
- Decorator tests in isolation
- Integration tests with real endpoints
- Edge cases: query params, auth headers
- Performance: measure before/after

Estimated Total: 10 hours
```

**Speaker Notes:**
Claude Code's planning mode is designed for deep analysis and detailed planning. The agent can explore your codebase, understand patterns, and propose comprehensive plans before writing code.

Key strengths of Claude Code planning:
1. **Deep Analysis:** Agent understands codebase and patterns
2. **Task Decomposition:** Clear breakdown into implementable tasks
3. **Architecture Design:** Proposed architecture with rationale
4. **Risk Identification:** Potential problems identified upfront
5. **Test Planning:** Strategy for testing included
6. **Interactive Refinement:** Plan can be refined based on feedback

The workflow is:
1. Developer provides rich context
2. Agent analyzes and proposes plan
3. Developer reviews and provides feedback
4. Agent refines plan
5. Both agree on approach
6. Agent implements with high confidence

**When to Use Claude Code Planning:**

- Large features (>20 hours of work)
- Architectural decisions needed
- Integration with existing code
- Team alignment required
- Complex requirements
- High-risk decisions

**Developer's Role in Planning:**

```
You provide:
├─ Problem statement (clear, detailed)
├─ Code context (samples, patterns)
├─ Constraints (performance, scale, compatibility)
├─ Success criteria (measurable, specific)
└─ Resources (time, tools available)

Agent provides:
├─ Architecture analysis
├─ Approach proposal
├─ Task breakdown
├─ Risk assessment
├─ Test strategy
└─ Effort estimates

You review and refine:
├─ Is approach right?
├─ Are risks acceptable?
├─ Are tasks correctly sized?
├─ Is timeline realistic?
├─ Are tests adequate?
└─ Any missing pieces?
```

**Red Flags in a Plan:**

- Tasks are >12 hours (too big)
- No clear acceptance criteria
- Missing test strategy
- Circular dependencies
- No risk assessment
- Doesn't match existing patterns
- Timeline seems optimistic

**Feedback Loop Example:**

```
You: "Great plan. But I'm concerned about the
cache invalidation approach. What if someone
updates a post directly in the database?"

Agent: "Good catch. The event hook approach
only catches application changes. For database-
direct updates, we'd need:
1. Database trigger to publish invalidation
2. Cache TTL as backup (safety net)
3. Cache version numbers for consistency

This adds complexity. Should we:
A. Add database triggers (most complete)
B. Rely on TTL + application events (simpler)
C. Rebuild on each change (safest but slow)"

You: "Let's do B. The TTL provides safety, and
we can optimize later if needed."

Agent: "Updated plan. Now Task 3 is simpler
(2h instead of 3h). Total effort: 9h instead of 10h."
```

---

### Slide 19: Claude Code Plan Mode (Part 2)
**Title:** Claude Code: Prompting for Better Plans

**Content:**

```
TECHNIQUES FOR GETTING BETTER PLANS FROM CLAUDE CODE:

1. PROVIDE RICH CONTEXT
   Good:
   "I need to add authentication."

   Better:
   "We have a FastAPI REST API. Need JWT auth.
   Existing code uses this pattern [example].
   Must support both web and mobile clients.
   Users exist in PostgreSQL with roles table."

2. SHOW EXISTING PATTERNS
   Good:
   "Follow the codebase conventions."

   Better:
   "Here's how we handle middleware [code].
   Here's our error pattern [code].
   Here's our testing approach [code]."

3. SPECIFY CONSTRAINTS CLEARLY
   Good:
   "Must be performant."

   Better:
   "Response time must stay <50ms.
   Database connections limited to 20.
   No external service dependencies.
   Backward compatible with existing clients."

4. DEFINE SUCCESS CRITERIA
   Good:
   "Make it work."

   Better:
   "Success means:
   - All 87 existing tests pass
   - New feature has >80% test coverage
   - Response times unchanged
   - Mobile clients can authenticate
   - Clear error messages on failure"

5. REQUEST SPECIFIC PLAN SECTIONS
   Good:
   "Make a plan."

   Better:
   "Before coding, provide:
   1. Architecture diagram (text ASCII)
   2. Task breakdown with estimates
   3. Key decisions with rationales
   4. Risks and mitigations
   5. Test strategy
   6. Dependency graph
   7. Any questions for clarification"


PLAN REVIEW CHECKLIST FOR CLAUDE CODE:

Completeness:
☐ Does plan address all requirements?
☐ Are edge cases mentioned?
☐ Are error cases included?
☐ Is integration strategy clear?

Feasibility:
☐ Are tasks realistic in size?
☐ Are dependencies correct?
☐ Are estimates reasonable?
☐ Can resources be obtained?

Architecture:
☐ Does design match existing patterns?
☐ Are interfaces well-defined?
☐ Is scalability considered?
☐ Are there architectural risks?

Testing:
☐ Is test strategy comprehensive?
☐ Are acceptance criteria clear?
☐ Are edge cases tested?
☐ Is performance testing included?

Risks:
☐ Are major risks identified?
☐ Are mitigations proposed?
☐ Are contingencies planned?
☐ Is scope creep risk addressed?


ITERATING ON CLAUDE CODE PLANS:

Round 1: Initial Plan
├─ Agent proposes architecture
├─ You identify concerns
└─ Request adjustments

Round 2: Refined Plan
├─ Agent addresses concerns
├─ Updates affected tasks
├─ Provides new estimates
└─ Identifies trade-offs

Round 3: Approved Plan
├─ Plan meets all criteria
├─ Both agree on approach
├─ Agent ready to implement
└─ Implementation can begin


ADVANCED: USING CLAUDE CODE FOR ARCHITECTURE REVIEW

Scenario: You have existing code, want to validate architecture.

Prompt:
"Review this codebase architecture:
[Provide directory structure, key files]

Questions:
1. Does this follow SOLID principles?
2. Are there architectural issues?
3. What should we refactor?
4. Is the separation of concerns good?

Then, for the [specific feature], propose an
architecture that fits with existing patterns."

Agent Response:
├─ Architecture analysis of existing code
├─ Specific issues identified
├─ Recommendations for improvements
├─ New feature architecture proposal
└─ Integration points with existing code


COLLABORATIVE PLANNING WITH CLAUDE CODE:

You don't have to accept the first plan.
This is collaborative design:

Iteration 1: Agent proposes
Iteration 2: You provide feedback
Iteration 3: Agent refines
Iteration 4: You ask new questions
Iteration 5: Agent adjusts
...
Until: Both satisfied with plan

This is not wasted time!
Good planning prevents bad implementation.
```

**Speaker Notes:**
Getting good plans from Claude Code is a skill. The better your prompting and feedback, the better the plans. This is an investment that pays huge dividends in implementation quality.

Key techniques:

1. **Rich Context:** The more context about your codebase and constraints, the better the plan
2. **Show Patterns:** Examples of existing code patterns help agent match style
3. **Clear Constraints:** Specific, measurable constraints prevent bad assumptions
4. **Success Criteria:** Define exactly what "done" means
5. **Explicit Requests:** Ask for specific plan sections

The review process is critical:
- You understand your domain better than the agent
- You know about hidden constraints
- You can catch architectural issues early
- You can course-correct before coding starts

Don't be shy about asking for changes:
- "This approach is too complex, can we simplify?"
- "This doesn't match our patterns, what if we..."
- "I'm concerned about this risk, how do we mitigate?"
- "Can you estimate without this part?"

The iteration is healthy and expected.

**Common Mistakes in Claude Code Planning:**

1. **Vague requirements:** "Add authentication" → too vague
2. **No context:** Expecting agent to know your codebase
3. **No feedback:** Accepting first plan without review
4. **Insufficient detail:** Not enough time spent in planning
5. **Scope creep:** Not freezing plan before implementation

**Try This:**
Have students create a planning prompt for a feature in their codebase. Use Claude Code to generate a plan. Review and iterate.

---

### Slide 20: Cursor Plan Mode
**Title:** Cursor: IDE-Integrated Planning with Composer

**Content:**

```
CURSOR'S APPROACH TO PLANNING:

Cursor is an IDE built on VS Code with agentic features.
Planning happens through its "Composer" feature.

PLANNING WORKFLOW IN CURSOR:

1. OPEN COMPOSER
   └─ Activate Composer mode in Cursor

2. SELECT CONTEXT
   ├─ Choose files to analyze
   ├─ Highlight code sections
   ├─ Reference documentation
   └─ Define scope

3. WRITE REQUEST
   ├─ Describe what you want
   ├─ Specify constraints
   ├─ List requirements
   └─ Give examples

4. COMPOSER PROPOSES CHANGES
   ├─ Shows diffs of proposed changes
   ├─ Explains the approach
   ├─ Highlights affected files
   └─ Shows impact

5. REVIEW IN IDE
   ├─ See changes in context
   ├─ Review actual code, not abstract
   ├─ Understand file organization impact
   ├─ Check editor integration

6. ITERATE OR APPLY
   ├─ Ask for modifications
   ├─ Request different approach
   ├─ Apply changes and test
   └─ Iterate until satisfied


CURSOR'S PLANNING STRENGTHS:

✓ Visual Context
  └─ See code and changes in IDE simultaneously

✓ File-Aware
  └─ Understands project structure from IDE

✓ Interactive Diffs
  └─ Easy to review and compare changes

✓ Immediate Testing
  └─ Can run tests right after applying changes

✓ Natural Integration
  └─ Doesn't require leaving editor


CURSOR'S PLANNING LIMITATIONS:

✗ Less Detailed Analysis
  └─ Focuses on code changes, not architecture

✗ Limited Scope
  └─ Better for local changes than system design

✗ Implicit Planning
  └─ Planning happens in background, less explicit

✗ No Task Breakdown
  └─ Doesn't decompose into subtasks naturally

✗ Harder for Large Projects
  └─ Context window limited by IDE visibility


EXAMPLE CURSOR PLANNING SESSION:

Initial Request:
"I want to add an email validation function.
It should:
- Validate format
- Check for common typos
- Be reusable in multiple places
- Have good error messages"

Composer Response:
[Shows new file: validators.py]
[Shows changes to imports in relevant files]

Includes:
├─ Validation function with regex
├─ Typo detection with common errors
├─ Comprehensive test file
├─ Documentation
└─ Integration examples

You Review:
"This looks good, but the regex is too complex.
Can you simplify? Also add a rate limiting
concept for email validation."

Composer Refines:
[Updates validators.py]
[Simplifies regex]
[Adds rate limiting]
[Updates tests]

Final:
"Apply these changes"
→ Changes applied to editor
→ You run tests
→ Everything passes
→ Ready to use


WHEN TO USE CURSOR PLANNING:

✓ Best for:
├─ Adding new functions/methods
├─ Refactoring existing code
├─ Adding validation/utilities
├─ Modifying multiple files
├─ Quick iterations

✗ Not ideal for:
├─ Large architectural changes
├─ System design
├─ Complex integrations
├─ Understanding existing patterns
└─ Detailed planning

CURSOR VS CLAUDE CODE PLANNING:

Cursor (IDE-based):
├─ Better for: incremental changes
├─ Better for: quick prototyping
├─ Better for: local scope
├─ Weakness: limited analysis
├─ Weakness: less detail

Claude Code (Agent-based):
├─ Better for: planning large features
├─ Better for: architecture decisions
├─ Better for: complex integrations
├─ Strength: deep analysis
├─ Strength: comprehensive planning

USE TOGETHER:
1. Claude Code for high-level planning
2. Cursor for implementing subtasks
3. Claude Code for architecture decisions
4. Cursor for coding and testing
```

**Speaker Notes:**
Cursor's planning is more implicit and IDE-integrated than Claude Code's explicit planning. Cursor is better for iterative changes within the IDE, while Claude Code is better for comprehensive upfront planning.

Key differences:

1. **Cursor:** IDE-integrated, visual, immediate feedback
2. **Claude Code:** Agent-focused, detailed analysis, architectural planning

Cursor's strength is that planning and implementation happen in the same context—you see the actual files, can test immediately, and iterate quickly.

Cursor's limitation is that it's less comprehensive—it focuses on code changes rather than system architecture.

Best practice:
- Use Claude Code for planning large features
- Use Cursor for implementing subtasks
- Switch between tools as needed

**Cursor Planning Prompts:**

For adding a function:
```
"Add a password strength validator function.
It should check:
- Minimum length (8 chars)
- At least one uppercase
- At least one number
- At least one special char

Should return: score (0-100) and feedback"
```

For refactoring:
```
"This function is doing too much.
Split it into smaller, testable parts.
Keep the public interface the same so
we don't break existing code."
```

For integration:
```
"Add logging to all database queries.
Use the existing logger instance.
Include query time and row count.
Don't log sensitive data like passwords."
```

---

### Slide 21: Aider Architect Mode
**Title:** Aider: Terminal-Based Architecture Planning

**Content:**

```
AIDER'S PLANNING APPROACH:

Aider is a terminal-based tool focused on agentic coding.
Its "architect mode" is designed for planning.

AIDER WORKFLOW:

1. ACTIVATE ARCHITECT MODE
   $ aider --architect

2. DESCRIBE THE FEATURE
   $ "Add a caching layer to the API"

3. ARCHITECT ANALYZES
   ├─ Reads and understands codebase
   ├─ Identifies existing patterns
   ├─ Finds related code
   ├─ Analyzes constraints
   └─ Creates implementation plan

4. ARCHITECT PROPOSES SOLUTION
   Output:
   ├─ Architecture overview
   ├─ Files to modify/create
   ├─ Code changes overview
   ├─ Implementation approach
   └─ Considerations

5. YOU REVIEW AND DECIDE
   Options:
   ├─ "Yes, implement this"
   ├─ "No, try different approach"
   ├─ "Can you explain further?"
   └─ "Modify this aspect"

6. AIDER IMPLEMENTS
   ├─ Makes code changes
   ├─ Creates new files
   ├─ Updates tests
   ├─ Runs validation
   └─ Commits changes


AIDER ARCHITECT MODE FEATURES:

Planning Focus:
├─ Primary goal is planning, not coding
├─ Thorough analysis before implementation
├─ Clear communication of approach
└─ Get approval before building

Terminal Integration:
├─ Works in your terminal/shell
├─ No IDE required
├─ Can be scripted
├─ Works with any editor

Version Control Aware:
├─ Understands git history
├─ References recent changes
├─ Can work with branches
└─ Makes atomic commits

Iterative:
├─ Easy to ask "what if?"
├─ Can explore alternatives
├─ Plans can be refined
└─ One conversation for entire feature


EXAMPLE AIDER ARCHITECT SESSION:

$ aider --architect

Aider Architect: "What would you like me to build?"

You: "Add request rate limiting to our API.
The app is FastAPI-based and we need:
- Per-user rate limits
- Different limits for different endpoints
- Configurable limits
- Return 429 status when exceeded"

Architect: "I'll analyze your codebase...

Analysis complete. Here's my plan:

ARCHITECTURE:
- Create middleware for rate limiting
- Use Redis to store request counts
- Track per (user_id, endpoint) combination
- Key format: rl:{user_id}:{endpoint}
- Use TTL for sliding window

FILES TO MODIFY:
- Create: app/middleware/rate_limiter.py
- Modify: app/main.py (add middleware)
- Modify: app/config.py (add rate limit config)
- Create: tests/test_rate_limiter.py

APPROACH:
1. Middleware checks request count for user/endpoint
2. If over limit, return 429 Conflict
3. Otherwise increment counter with TTL
4. Different limits per endpoint via config

CONSIDERATIONS:
- Redis failure should fail open (no limiting)
- Need to handle anonymous users
- Should log rate limit exceeded
- Consider distributed system behavior

Should I implement this approach?"

You: "Looks good. One question: what about
authenticated users who aren't in our system yet?"

Architect: "Good question. Options:
A. Deny them (safest)
B. Allow them with generous limit
C. Rate limit by IP instead

Which approach?"

You: "Let's do C for IP-based fallback."

Architect: "Updated plan with IP fallback.
Should I implement?"

You: "Yes, go ahead."

Architect: [Implements rate limiting]
[Creates middleware]
[Adds tests]
[Updates config]
[All tests pass]
[Ready to use]


AIDER ARCHITECT MODE STRENGTHS:

✓ Pure Planning Focus
  └─ Architect mode prioritizes planning

✓ Terminal-Native
  └─ Works seamlessly in development workflow

✓ Conversational
  └─ Natural back-and-forth refinement

✓ Git Integration
  └─ Understands version control

✓ Comprehensive
  └─ Covers architecture, files, approach


AIDER ARCHITECT MODE LIMITATIONS:

✗ Less IDE Integration
  └─ No visual code editor context

✗ Limited to Terminal
  └─ Not ideal for visual learners

✗ Smaller Community
  └─ Fewer examples/resources

✗ Narrower Context
  └─ Can't as easily reference UI/config files


WHEN TO USE AIDER ARCHITECT MODE:

✓ Best for:
├─ Terminal-native developers
├─ Planning features systematically
├─ Iterating on architecture
├─ Teams using git workflow
├─ Comprehensive planning sessions

✗ Not ideal for:
├─ Visual debugging
├─ Quick small changes
├─ Complex UI changes
├─ Tight IDE integration


AIDER VS CURSOR VS CLAUDE CODE:

Tool           | Planning | IDE | Terminal | Best For
─────────────────────────────────────────────────────────
Aider Architect| Excellent| No  | Yes      | Feature planning
Cursor Plan    | Good     | Yes | No       | Incremental change
Claude Code    | Excellent| No  | Yes      | Detailed analysis

BEST COMBINED WORKFLOW:

1. Use Aider Architect for overall feature planning
2. Use Claude Code for complex design questions
3. Use Cursor for implementation and testing
4. Use Aider for final commits and pushes
```

**Speaker Notes:**
Aider's architect mode is designed specifically for the planning phase. Unlike Cursor which blends planning and implementation, Aider separates them clearly.

Key strengths:
1. **Planning-first:** Architect mode is explicitly about planning
2. **Conversational:** Natural back-and-forth refinement
3. **Terminal-native:** Fits developer workflows perfectly
4. **Git-aware:** Understands version control

Aider is excellent for:
- Systematic feature planning
- Architecture discussions
- Alternative exploration
- Approval-gate before implementation

**Using Aider Architect Effectively:**

```
Use for architecture questions:
$ "We're building a notification system.
   What's the best architecture for:
   - Sending notifications
   - Tracking delivery
   - Retries and failures?"

Use for design decisions:
$ "Should we queue notifications or send sync?
   What are the trade-offs?"

Use for refactoring planning:
$ "How should we refactor the user module?
   It's gotten too large."

Use for integration planning:
$ "We need to integrate with Stripe.
   How should this work with our existing code?"
```

**Iterating in Aider:**

```
You: "Here's the feature I want to add..."
Aider: [Proposes architecture]

You: "What if we used approach B instead?"
Aider: [Analyzes approach B, compares]

You: "Can we make this simpler?"
Aider: [Simplifies the design]

You: "Looks good, implement it"
Aider: [Creates all the code]
```

---

### Slide 22: Codex CLI Read-Only Mode
**Title:** Codex: Research-Focused Planning Phase

**Content:**

```
CODEX CLI APPROACH:

Codex CLI is designed for read-only analysis.
Used primarily for the research phase.

READ-ONLY MODE FEATURES:

Can Do:
├─ Search codebase
├─ Analyze code patterns
├─ Find similar implementations
├─ Understand existing approaches
├─ Gather requirements
├─ Document findings
└─ Plan without modifying

Cannot Do:
├─ Write code
├─ Modify files
├─ Commit changes
├─ Delete code
└─ Run tests

Perfect for: RESEARCH PHASE


CODEX READ-ONLY WORKFLOW:

1. ACTIVATE READ-ONLY MODE
   $ codex --read-only

2. ASK QUESTIONS ABOUT CODEBASE
   "Find all database queries for users"
   "Show me the caching implementations"
   "What error handling patterns exist?"

3. ANALYZE PATTERNS
   "What's consistent across API endpoints?"
   "How is validation done?"
   "What libraries are used?"

4. UNDERSTAND CONSTRAINTS
   "What are performance requirements?"
   "What scale does this need to handle?"
   "What are deployment constraints?"

5. GATHER REQUIREMENTS
   "What features are already similar?"
   "How is this integrated with other parts?"
   "What's the testing approach?"

6. CREATE PLANNING DOCUMENT
   Based on findings:
   ├─ Requirements
   ├─ Existing patterns
   ├─ Constraints
   ├─ Related code
   └─ Planning recommendations


EXAMPLE CODEX READ-ONLY SESSION:

$ codex --read-only

You: "We want to add file upload capability.
First, help me understand:
1. How are files currently handled?
2. What storage is available?
3. What size limits exist?
4. How is validation done?"

Codex: "Analyzing codebase...

CURRENT FILE HANDLING:
Found 3 file-related features:
- Profile pictures (avatars)
- Document storage
- Report generation

PROFILE PICTURES:
└─ Location: app/services/file_service.py
   ├─ Upload to local disk (/tmp/uploads)
   ├─ Max 5MB size
   ├─ Only JPEG/PNG accepted
   ├─ Stored with user_id as prefix
   └─ Deleted on user deletion

DOCUMENT STORAGE:
└─ Location: app/services/document_service.py
   ├─ Upload to S3 bucket
   ├─ Max 50MB size
   ├─ Any file type accepted
   ├─ Metadata stored in database
   └─ Public/private via policy

REPORT GENERATION:
└─ Location: app/workers/report_worker.py
   ├─ Generated PDF files
   ├─ Stored locally then uploaded to S3
   ├─ Async job processing
   └─ Email link to user

PATTERNS FOUND:
1. Size validation before upload
2. File type validation (where applicable)
3. Storage abstraction (local or S3)
4. Cleanup on deletion
5. Metadata in database

STORAGE OPTIONS:
- Local disk (simple, limited scale)
- S3 (scalable, integrated)

RECOMMENDATIONS:
- Use document_service pattern if scalable needed
- Use avatar pattern if small files only
- Consider async for large uploads"

You: "Great. Now help me understand the
constraints. What are the performance
requirements?"

Codex: "Analyzing requirements...
[Finds performance tests]
[Analyzes benchmarks]
[Reviews scaling discussions]
[Provides summary of constraints]"


CODEX STRENGTHS:

✓ Read-Only Safety
  └─ Can explore without risk of breaking things

✓ Deep Analysis
  └─ Finds patterns in large codebases

✓ Pattern Discovery
  └─ Identifies existing approaches to learn from

✓ Comprehensive
  └─ Can analyze entire project systematically

✓ Constraint Identification
  └─ Surfaces requirements and limitations


CODEX LIMITATIONS:

✗ Read-Only Only
  └─ Cannot implement based on analysis

✗ Requires Manual Planning
  └─ You must synthesize findings into plan

✗ Separate Tool
  └─ Planning happens separately from implementation

✗ No IDE Integration
  └─ Terminal-based only


CODEX IN THE WORKFLOW:

Research Phase:
1. Use Codex to explore existing code
2. Find similar implementations
3. Understand patterns and conventions
4. Document constraints and requirements

Planning Phase:
5. Use findings to create plan
6. Propose architecture
7. Break into tasks
8. Get approval

Implementation Phase:
9. Use Claude Code or Aider or Cursor
10. Build according to plan


CODEX PROMPTS FOR RESEARCH:

Finding similar features:
$ "Find all places where we cache data"
$ "Show me all database queries"
$ "What error handling patterns exist?"

Understanding patterns:
$ "How do we structure API endpoints?"
$ "What's our testing pattern?"
$ "How is configuration handled?"

Discovering constraints:
$ "What are the performance requirements?"
$ "How much data do we handle?"
$ "What scale issues are mentioned?"

Finding integration points:
$ "How would this integrate with auth?"
$ "What existing code should we extend?"
$ "What dependencies would this have?"


WORKFLOW COMBINING CODEX + OTHER TOOLS:

Step 1: Codex Research (Read-Only)
├─ Explore codebase
├─ Find patterns
├─ Document constraints
└─ Output: Research document

Step 2: Claude Code Planning
├─ Review research findings
├─ Propose architecture
├─ Break into tasks
├─ Create detailed plan
└─ Output: Implementation plan

Step 3: Aider/Cursor/Claude Implementation
├─ Build each task
├─ Write tests
├─ Integrate
└─ Output: Working feature
```

**Speaker Notes:**
Codex's read-only mode is perfect for the research phase. You get deep analysis without the risk of accidentally modifying code. This is ideal for understanding large, complex codebases.

Key use cases:
1. **Understanding existing patterns:** What patterns should I follow?
2. **Finding similar implementations:** How is this similar feature done?
3. **Discovering constraints:** What limits do I need to know about?
4. **Integration planning:** How does this fit with existing code?

Codex is great for:
- Exploring unfamiliar codebases
- Finding patterns in large projects
- Understanding existing architectures
- Gathering requirements systematically

The workflow is:
1. Use Codex for research (read-only)
2. Use Claude Code/Aider for planning
3. Use Cursor/Claude/Aider for implementation

This separation of concerns is powerful—each tool does what it's best at.

---

### Slide 23: Comparing Planning Approaches
**Title:** Which Tool for Which Planning Task?

**Content:**

```
PLANNING TASK MATRIX:

Task                    | Claude | Cursor | Aider | Codex
────────────────────────┼────────┼────────┼───────┼─────
Understand codebase     | Good   | Good   | Good  | Best
Find patterns           | Good   | Fair   | Good  | Best
Explore alternatives    | Best   | Fair   | Best  | N/A
Architecture design     | Best   | Fair   | Good  | N/A
Task decomposition      | Best   | Fair   | Good  | N/A
Risk analysis          | Best   | Fair   | Good  | N/A
Implementation detail   | Best   | Best   | Good  | N/A
Visual review          | Fair   | Best   | Fair  | N/A
Quick iteration        | Good   | Best   | Good  | N/A
Team alignment         | Best   | Fair   | Good  | N/A


SCENARIO-BASED GUIDE:

SCENARIO 1: New team member learning codebase
├─ Step 1: Codex read-only exploration
│  └─ "Show me what this codebase does"
├─ Step 2: Claude Code architecture review
│  └─ "Explain the overall architecture"
└─ Step 3: Cursor hands-on learning
   └─ "Show me where X happens"

SCENARIO 2: Adding a medium-sized feature
├─ Step 1: Claude Code planning
│  └─ Full architecture and task decomposition
├─ Step 2: Cursor implementation
│  └─ Build the code with immediate feedback
└─ Step 3: Aider final review
   └─ Make sure everything fits together

SCENARIO 3: Performance optimization
├─ Step 1: Codex analysis
│  └─ Find where time is spent
├─ Step 2: Claude Code planning
│  └─ Plan optimization approach
└─ Step 3: Cursor implementation
   └─ Implement and measure

SCENARIO 4: Architecture refactoring
├─ Step 1: Claude Code deep analysis
│  └─ Understand current issues
├─ Step 2: Claude Code architecture proposal
│  └─ Design new architecture
├─ Step 3: Aider architect mode
│  └─ Validate approach with wider team
└─ Step 4: Cursor + Claude implementation
   └─ Implement in phases

SCENARIO 5: Quick bug fix
├─ Step 1: Cursor code exploration
│  └─ Understand the issue in context
├─ Step 2: Cursor implementation
│  └─ Fix the bug immediately
└─ Step 3: Test and verify
   └─ Make sure it works


CHOOSING YOUR PRIMARY PLANNING TOOL:

If you prefer...        → Use...
─────────────────────────────────────
Detailed analysis       | Claude Code
Visual context         | Cursor
Terminal workflow      | Aider
Research/exploration   | Codex

If working on...        → Use...
─────────────────────────────────────
Large features         | Claude Code
Incremental changes    | Cursor
Comprehensive redesign | Aider
New to codebase        | Codex


COMBINED WORKFLOW (RECOMMENDED):

┌─────────────────────────────────────────┐
│ RESEARCH PHASE                          │
├─────────────────────────────────────────┤
│ Tool: Codex (read-only)                │
│ Goal: Understand domain, find patterns  │
│ Time: 1-2 hours                         │
│ Output: Research notes                  │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ PLANNING PHASE                          │
├─────────────────────────────────────────┤
│ Tool: Claude Code                       │
│ Goal: Architecture, task decomposition  │
│ Time: 1-2 hours                         │
│ Output: Detailed implementation plan    │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ REVIEW PHASE                            │
├─────────────────────────────────────────┤
│ Tool: Aider Architect (optional)        │
│ Goal: Validate plan, get team feedback  │
│ Time: 0.5 hours                         │
│ Output: Approved plan                   │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ IMPLEMENTATION PHASE                    │
├─────────────────────────────────────────┤
│ Tool: Cursor or Claude Code             │
│ Goal: Build the feature                 │
│ Time: 60-80% of total time              │
│ Output: Working implementation          │
└─────────────────────────────────────────┘
        ↓
┌─────────────────────────────────────────┐
│ VERIFICATION PHASE                      │
├─────────────────────────────────────────┤
│ Tool: All tools (coordinate together)   │
│ Goal: Test, review, validate            │
│ Time: 10-15% of total time              │
│ Output: Production-ready code           │
└─────────────────────────────────────────┘
```

**Speaker Notes:**
Each tool has strengths. The best workflow combines them:

1. **Codex** for research—understand the domain
2. **Claude Code** for planning—design the solution
3. **Aider Architect** for validation—get feedback
4. **Cursor/Claude** for implementation—build it
5. **All** for verification—test and review

Don't try to force one tool to do everything. Use the right tool for each phase.

---

### Slide 24: Plan-Act-Reflect Framework
**Title:** Iterative Refinement Through Planning

**Content:**

```
THE PLAN-ACT-REFLECT CYCLE:

┌──────────────────────────────────────────────────┐
│                                                  │
│ PLAN                                             │
│ Create plan based on understanding              │
│ └─ What will we build?                          │
│ └─ How will it work?                            │
│ └─ What could go wrong?                         │
│                                                  │
│          ↓                                       │
│                                                  │
│ ACT                                              │
│ Implement according to plan                     │
│ └─ Write code                                   │
│ └─ Write tests                                  │
│ └─ Integration                                  │
│                                                  │
│          ↓                                       │
│                                                  │
│ REFLECT                                          │
│ Review what happened                            │
│ └─ Did it match the plan?                       │
│ └─ What learned?                                │
│ └─ What needs adjustment?                       │
│                                                  │
│          ↓                                       │
│                                                  │
│ ├─ If: "Plan was good, implementation good"     │
│ │  → DONE, move to next feature                 │
│ │                                               │
│ └─ If: "Plan had issues OR implementation had" │
│    → Loop back to PLAN with new understanding  │
│                                                  │
└──────────────────────────────────────────────────┘


PLAN PHASE DETAILS:

Input:
├─ Requirements
├─ Constraints
├─ Existing code patterns
└─ Understanding of domain

Activities:
├─ Design architecture
├─ Break down into tasks
├─ Create test strategy
├─ Identify risks
└─ Estimate effort

Output:
├─ Architecture document
├─ Task breakdown
├─ Risk analysis
└─ Approval from team


ACT PHASE DETAILS:

Input:
├─ Approved plan
├─ Clear task breakdown
└─ Test strategy

Activities:
├─ Implement each task
├─ Write tests
├─ Verify against spec
├─ Integrate components
└─ Fix issues as they arise

Output:
├─ Working implementation
├─ Test results
├─ Integration verification
└─ Lessons learned


REFLECT PHASE DETAILS:

Input:
├─ Completed implementation
├─ Test results
└─ Process observations

Activities:
├─ Compare result to plan
├─ Analyze deviations
├─ Test coverage
├─ Code quality review
├─ Performance verification
└─ Team feedback

Output:
├─ Acceptance decision
├─ Identified improvements
├─ Lessons for next time
└─ Recommendations


DEVIATION ANALYSIS:

If implementation matches plan:
├─ Estimate was good → trust future estimates
├─ Approach was right → use for similar features
├─ Tests were adequate → use pattern again
└─ Team communication worked → continue approach

If implementation diverged from plan:
├─ Original understanding was incomplete
├─ Plan was too optimistic
├─ Plan didn't account for discovered issues
├─ New information emerged during implementation
└─ This is normal and valuable!


LEARNING FROM DEVIATIONS:

Deviation Type 1: Took longer than planned
├─ Why?
│  ├─ Estimate was too optimistic
│  ├─ Unexpected complexity
│  ├─ Discovered new requirements
│  └─ External blockers
├─ Learn:
│  ├─ Adjust estimation for future features
│  ├─ Plan more research time
│  ├─ Better requirements gathering
│  └─ Account for dependencies
└─ Adjust:
   └─ Future plans more conservative

Deviation Type 2: Code quality issues
├─ Why?
│  ├─ Plan didn't address quality enough
│  ├─ Tests were insufficient
│  ├─ Code review found issues
│  └─ Integration revealed problems
├─ Learn:
│  ├─ Plan more test time
│  ├─ More thorough code review
│  ├─ Better integration testing
│  └─ More comprehensive plan
└─ Adjust:
   └─ Increase review/test in plan

Deviation Type 3: Architecture issues
├─ Why?
│  ├─ Original understanding wrong
│  ├─ Plan didn't match existing code
│  ├─ New information during implementation
│  └─ Missed integration point
├─ Learn:
│  ├─ Need deeper research phase
│  ├─ Better architecture review
│  ├─ More prototype/proof-of-concept
│  └─ Better integration planning
└─ Adjust:
   └─ More planning time and depth


WHEN TO REFLECT AND ITERATE:

Reflect After:
├─ Completing each task (daily/weekly)
├─ Completing implementation phase
├─ After code review
├─ Before deployment
└─ Periodically during development

Questions to Ask:
├─ "Are we on track?"
├─ "What have we learned?"
├─ "Do we need to adjust plan?"
├─ "Are there risks emerging?"
├─ "Is quality acceptable?"
└─ "Should we proceed or revise?"

When to Loop Back:
├─ Major issues discovered
├─ Requirements changed
├─ Architecture problems found
├─ Timeline is threatened
├─ Quality is unacceptable
└─ Significant learning requires redesign


EFFECTIVE REFLECTION MEETINGS:

Good reflection:
├─ Honest assessment
├─ Psychological safety
├─ Blame-free discussion
├─ Focus on learning
├─ Document lessons
└─ Adjust for next cycle

Bad reflection:
├─ Blame-focused
├─ Defensive explanations
├─ Ignore problems
├─ No adjustments made
├─ Forget lessons
└─ Repeat same mistakes
```

**Speaker Notes:**
The Plan-Act-Reflect cycle is how continuous improvement happens. It's not just about building code—it's about getting better at building code.

Key points:

1. **Plan:** Create a well-thought-out plan
2. **Act:** Execute the plan, learning as you go
3. **Reflect:** Analyze what happened and why
4. **Loop:** Adjust your approach based on learning

This is used at multiple scales:
- **Per-task:** Do you understand this task? Complete it? Learn from it?
- **Per-feature:** Did the feature go as planned? What did we learn?
- **Per-project:** What went well/poorly? How do we improve?
- **Across organization:** How do we help teams plan better?

The reflection is where real learning happens. If you skip reflection, you repeat the same mistakes.

**Red Flags in Reflection:**

- "It worked, so we must be doing it right" (ignoring luck)
- "It didn't work, so planning is useless" (wrong conclusion)
- "We did what we planned, mission accomplished" (missing learning)
- "We deviated from plan, bad team" (missing the actual issue)
- "No time for reflection, let's move to next thing" (short-term vs long-term)

**Try This:**
After a project, do a real retrospective. What surprised you? What will you do differently?

---

### Slide 25: Static vs Dynamic Decomposition
**Title:** Planning Upfront vs Planning As You Go

**Content:**

```
TWO APPROACHES TO TASK DECOMPOSITION:

STATIC DECOMPOSITION:
└─ Plan all tasks upfront
   ├─ Detailed task breakdown before starting
   ├─ All dependencies identified
   ├─ Comprehensive estimates
   ├─ All tasks on critical path
   └─ Follow plan throughout

DYNAMIC DECOMPOSITION:
└─ Decompose as you learn
   ├─ High-level plan initially
   ├─ Detailed planning as you learn
   ├─ Tasks emerge from implementation
   ├─ Flexible prioritization
   └─ Adapt as new information emerges


STATIC DECOMPOSITION EXAMPLE:

Feature: Build API with 5 endpoints

UPFRONT PLANNING:
├─ Task 1: Define data model (2h)
├─ Task 2: Setup database (1h)
├─ Task 3: Implement endpoint 1 (3h)
├─ Task 4: Implement endpoint 2 (3h)
├─ Task 5: Implement endpoint 3 (2h)
├─ Task 6: Implement endpoint 4 (3h)
├─ Task 7: Implement endpoint 5 (2h)
├─ Task 8: Write integration tests (4h)
├─ Task 9: Documentation (2h)
├─ Task 10: Deployment (1h)
└─ Total: 23 hours

EXECUTION:
Task 1 → Task 2 → Tasks 3-7 (parallel) → Task 8 → Task 9 → Task 10

ADVANTAGES:
├─ Clear timeline
├─ Easy to parallelize
├─ Good for coordination
├─ Can plan resources
└─ Predictable delivery

DISADVANTAGES:
├─ Inflexible
├─ Hard to adapt
├─ Estimate errors compound
├─ May do unnecessary work
└─ Learning doesn't help adjust


DYNAMIC DECOMPOSITION EXAMPLE:

Feature: Build API with 5 endpoints

INITIAL PLAN:
├─ Phase 1: Setup foundation
│  └─ Get approval to proceed
├─ Phase 2: Implement endpoints
│  └─ Details TBD as we learn
├─ Phase 3: Integration and testing
│  └─ Approach TBD based on Phase 2
└─ Total: ~20-30 hours (estimate)

EXECUTION:
Phase 1: Setup foundation (4h)
├─ Task 1: Define data model
├─ Task 2: Setup database
└─ Task 3: Create base endpoint structure
Reflection: "Core structure is clearer now"

Phase 2: Implement endpoints (planned: 12h)
├─ Task 2.1: Implement endpoint 1 (3h)
│  Reflect: "Endpoint pattern established"
├─ Task 2.2: Implement endpoints 2-5 (7h)
│  Reflect: "Efficient pattern emerging"
└─ Adjust estimate: Was 20h, now 15h

Phase 3: Testing and deployment (4h)
├─ Task 3.1: Write integration tests (2h)
├─ Task 3.2: Documentation (1h)
└─ Task 3.3: Deploy (1h)

Total: ~18 hours (better estimate after learning)

ADVANTAGES:
├─ Flexible
├─ Adapts to learning
├─ Can improve estimates
├─ Only necessary work
├─ Team stays engaged

DISADVANTAGES:
├─ Less predictable
├─ Harder to parallelize
├─ Resource planning harder
├─ May need more communication
└─ Less good for strict deadlines


WHEN TO USE EACH:

USE STATIC DECOMPOSITION WHEN:
├─ Clear, well-understood work
├─ Team needs strict timeline
├─ Need to parallelize
├─ Distributed team (async)
├─ Contract/commitment deadline
└─ Similar to previous work

USE DYNAMIC DECOMPOSITION WHEN:
├─ Significant learning needed
├─ Novel/exploratory work
├─ Unclear requirements
├─ Complex interactions
├─ Need flexibility
└─ Team can collaborate closely

HYBRID APPROACH (RECOMMENDED):

Combine both:
1. High-level static plan (phases)
2. Detailed dynamic planning per phase
3. Review and adjust between phases

Example:
STATIC (Phase level):
├─ Phase 1: Research and design (2-3 days)
├─ Phase 2: Core implementation (3-5 days)
├─ Phase 3: Testing and refinement (2-3 days)
└─ Phase 4: Deployment (1 day)

DYNAMIC (Within each phase):
├─ Phase 1 starts with questions
│  └─ Tasks emerge from answering questions
├─ Phase 2 starts with high-level design
│  └─ Tasks emerge from implementation
├─ Phase 3 starts with test strategy
│  └─ Tasks based on what needs testing
└─ Phase 4 is straightforward
   └─ Pre-planned deployment


CHOOSING DECOMPOSITION STYLE:

Decision Matrix:
Clarity of Requirements:
├─ Clear → Use Static
└─ Unclear → Use Dynamic

Team Arrangement:
├─ Distributed → Use Static
└─ Colocated → Use Dynamic

Deadline Pressure:
├─ Strict → Use Static
└─ Flexible → Use Dynamic

Work Novelty:
├─ Routine → Use Static
└─ Novel → Use Dynamic

If most factors point Static → Use Static
If most factors point Dynamic → Use Dynamic
If mixed → Use Hybrid approach
```

**Speaker Notes:**
These are two different philosophies about planning and decomposition. Neither is universally better—it depends on your situation.

Static decomposition works well when:
- You understand the work clearly
- You need predictable timelines
- You need to parallelize work
- You have external commitments

Dynamic decomposition works well when:
- The work involves learning
- You want flexibility
- Requirements might change
- You want to optimize based on learning

The hybrid approach (most common) combines both:
- Plan at a high level statically
- Decompose dynamically within phases
- Review between phases

This gives you structure (static) while preserving flexibility (dynamic).

---

### Slide 26: Plan-Act-Reflect and Decomposition Summary
**Title:** Frameworks for Iterative Planning

**Content:**

```
KEY CONCEPTS:

Plan-Act-Reflect Cycle:
├─ Plan: Create strategy based on understanding
├─ Act: Execute according to plan
├─ Reflect: Analyze results and learning
└─ Loop: Adjust future plans based on learning

Static vs Dynamic Decomposition:
├─ Static: All tasks planned upfront
├─ Dynamic: Tasks emerge during execution
└─ Hybrid: High-level static, detailed dynamic

SELECTING YOUR APPROACH:

For your next project, decide:

1. Will you use static or dynamic decomposition?
   └─ Depends on clarity, timeline, novelty

2. How will you do reflection?
   ├─ After each task? After phase? After project?
   ├─ Who is involved? How do you document?
   └─ How do you adjust based on learning?

3. How frequently will you replan?
   ├─ Never (pure static)
   ├─ Between phases (hybrid)
   ├─ Continuously (pure dynamic)
   └─ Based on discoveries


CONTINUOUS IMPROVEMENT:

Use each project to improve planning:
├─ Task 1: Notice deviations
├─ Reflection: Understand why
├─ Adjustment: Try different approach
├─ Task 2: Measure improvement
├─ Loop: Continuous improvement

Over time:
├─ Estimates get better
├─ Plans get more accurate
├─ Team gets more aligned
├─ Delivery becomes more predictable
└─ Quality improves
```

**Speaker Notes:**
Plan-Act-Reflect and the choice between static/dynamic decomposition are complementary frameworks. Together they give you a complete approach to iterative development.

The key is continuous improvement—each project teaches you something to apply to the next one.

**Try This:**
On your next project, explicitly use the Plan-Act-Reflect cycle. Document what you learn and apply it to the next project.

---

## SECTION 4: Plan-Act-Reflect Framework (Conclusion)

*[Slides 17-26 covered comprehensive planning approaches. Continue with Sections 5-6...]*

---

## SECTION 5: Practical Planning Examples (Slides 27-36)

### Slide 27: Example 1 - Feature Implementation Planning
**Title:** Planning a New Feature: User Dashboard

**Content:**

```
FEATURE: Add customizable user dashboard

INITIAL REQUIREMENTS:
├─ Users can see personalized content
├─ Users can customize dashboard layout
├─ Save preferences to database
├─ Load custom layout on login
└─ Works on desktop and mobile

RESEARCH PHASE (2 hours):

1. Explore existing code:
   ├─ Find current user profile page
   ├─ Look at existing layout system
   ├─ Find how settings are saved
   └─ Review responsive design patterns

2. Findings:
   ├─ Layout system exists for reports
   ├─ Settings stored in users.settings JSON column
   ├─ Responsive classes used throughout
   ├─ React components for frontend

3. Constraints discovered:
   ├─ JSON column size limit ~1MB
   ├─ API response time <100ms
   ├─ Must work offline (service worker)
   └─ No external CSS libraries beyond Material-UI

PLANNING PHASE (1.5 hours):

Architecture Design:
┌─────────────────────────────────────────┐
│ Dashboard Layout System                 │
├─────────────────────────────────────────┤
│                                         │
│  Frontend (React):                      │
│  ├─ DashboardLayout component           │
│  ├─ Dashboard customizer modal          │
│  ├─ Widget components (cards)           │
│  └─ LocalStorage for quick load         │
│                                         │
│  Backend (API):                         │
│  ├─ GET /api/dashboard (load layout)    │
│  ├─ POST /api/dashboard (save layout)   │
│  ├─ Dashboard model (validation)        │
│  └─ Permissions check                   │
│                                         │
│  Database:                              │
│  └─ users.dashboard_layout (JSON)       │
│                                         │
└─────────────────────────────────────────┘

Key Decisions:
1. Store in users table (not separate table)
   → Simpler, single user query
2. JSON schema validation
   → Ensure valid layouts
3. LocalStorage cache
   → Fast load on return users
4. Reusable widget components
   → Extensible for future widgets

Task Breakdown:
1. Frontend Widget Library (4h)
   ├─ Create base Widget component
   ├─ 5 basic widgets (time, weather, etc)
   ├─ Widget composition system
   └─ Tests for widgets

2. Dashboard Layout System (5h)
   ├─ DashboardLayout component
   ├─ Drag-and-drop positioning
   ├─ Responsive grid system
   ├─ LocalStorage sync
   └─ Tests

3. Dashboard Customizer (3h)
   ├─ Modal for customization
   ├─ Add/remove widgets
   ├─ Layout preview
   └─ Save/cancel actions

4. Backend API (4h)
   ├─ GET /api/dashboard endpoint
   ├─ POST /api/dashboard endpoint
   ├─ JSON schema validation
   ├─ Permission checks
   └─ Tests

5. Database Migration (1h)
   ├─ Add dashboard_layout column
   ├─ Backfill existing users
   └─ Rollback plan

6. Integration & Tests (3h)
   ├─ E2E tests
   ├─ Performance testing
   ├─ Offline functionality
   └─ Documentation

Total Estimate: 20 hours
```

**Speaker Notes:**
This is a real-world example of planning a significant feature. Notice how the process goes from understanding to design to breakdown.

Key points:
1. **Research revealed constraints** that affected the design
2. **Key decisions were explicit** with rationales
3. **Tasks were properly scoped** (3-5 hours each)
4. **Estimates were realistic** (20 hours for a week's work)
5. **Testing was planned** from the beginning

---

### Slide 28: Feature Implementation Planning (Continued)
**Title:** Building the Dashboard - Implementation Phase

**Content:**

```
IMPLEMENTATION TRACKING:

Task 1: Frontend Widget Library (4h estimate)
├─ Status: In Progress
├─ Actual time: 1.5h (so far)
├─ Progress:
│  ├─ ✓ Base Widget component done
│  ├─ ✓ Time widget working
│  ├─ ✓ Weather widget done
│  ⊙ Tasks widget (50% done)
│  └─ Todo: Stub for remaining widgets
├─ Issues found:
│  └─ Weather API requires key (not in original plan)
├─ Adjustment:
│  └─ Move weather widget to optional phase 2
└─ Revised estimate: 3h (still on track)

Task 2: Dashboard Layout System (5h estimate)
├─ Status: Not started (waiting for Task 1)
├─ Dependencies: Task 1 widgets
├─ Planned: Tomorrow
└─ Confidence: High

[Tasks 3-6 not yet started]


REFLECTION AFTER TASK 1:

What Happened:
├─ Task completed faster than expected
├─ Weather widget added external dependency
├─ Widget component system very reusable
└─ Tests caught edge cases early

Learnings:
├─ Simple components are fast to build
├─ Check for external dependencies early
├─ Reusable components save time later
└─ Comprehensive tests catch issues

Adjustments for Task 2:
├─ Keep same testing level (it helped)
├─ Check for dependencies upfront
├─ Leverage widget reusability
└─ Expect good progress

Revised Timeline:
├─ Original: 20 hours
├─ Completed: 3.5 hours
├─ Remaining: 16.5 hours
├─ Confidence: Still on track


IMPLEMENTATION MILESTONES:

By end of Day 1:
└─ Widget library complete and tested

By end of Day 2:
└─ Layout system and customizer working

By end of Day 3:
└─ Backend API complete

By end of Day 4:
└─ Integration and testing complete

By end of Day 5:
└─ Documentation and polish

CONTINGENCY:
If something takes longer:
├─ Cut weather widget (optional)
├─ Simplify drag-and-drop (use simpler UI)
├─ Reduce test coverage (not ideal but acceptable)
└─ Extend timeline (not preferred but possible)
```

**Speaker Notes:**
As implementation happens, you see where estimates are right or wrong. You can adjust based on actual progress, which is valuable learning for future planning.

Key practices during implementation:
1. **Track progress:** Are you on schedule?
2. **Reflect continuously:** What did you learn?
3. **Adjust as needed:** Can you stay on track? Do you need to change scope?
4. **Document learnings:** Use them for next time

---

### Slide 29: Example 2 - Bug Fix Planning
**Title:** Planning a Bug Fix: Slow Reports Generation

**Content:**

```
PROBLEM: Reports take 30 seconds, should be <5 seconds

RESEARCH PHASE (1 hour):

1. Understand the problem:
   ├─ Report type: User activity summary
   ├─ Data volume: ~100K records
   ├─ Current time: ~30 seconds
   ├─ Target: <5 seconds (6x faster)
   ├─ Impact: Daily reports slow down dashboard

2. Reproduce the issue:
   ├─ Create test data
   ├─ Generate report
   ├─ Confirm: 30-32 seconds consistently
   └─ Profile to find bottleneck

3. Analyze with tools:
   ├─ Database query profiling
   │  └─ Main query: 25 seconds
   │  └─ Grouping/aggregation: 5 seconds
   ├─ Memory usage: Normal
   ├─ Network: Not a factor
   └─ Root cause: Inefficient SQL query

4. Examine the code:
   ├─ Found the query:
   │  SELECT user_id, COUNT(*), SUM(amount)
   │  FROM activities
   │  WHERE created_at > date - 30 days
   │  GROUP BY user_id
   │
   ├─ Problem: No index on (created_at, user_id)
   ├─ Fix: Add index or optimize query
   └─ Existing approach: Loop and filter (inefficient)

PLANNING PHASE (30 minutes):

Solution Options:

Option A: Add Database Index
├─ Time: 15 minutes
├─ Risk: Very low
├─ Improvement: ~80% (25s → 5s)
├─ Downside: Brief lock on table during index creation
└─ Recommendation: YES, do first

Option B: Query Optimization
├─ Time: 1-2 hours
├─ Risk: Low (breaking change unlikely)
├─ Improvement: 90% (25s → 2.5s)
├─ Downside: Code changes, more testing
└─ Recommendation: YES, do after A

Option C: Caching
├─ Time: 2-3 hours
├─ Risk: Medium (cache invalidation)
├─ Improvement: 95% (25s → 1.5s)
├─ Downside: Cache management complexity
└─ Recommendation: Maybe later, not now

Plan: Do A then B

Task Breakdown:

Task 1: Add Index (15 min)
├─ Create migration
├─ Add index on (created_at, user_id)
├─ Test index is used (EXPLAIN plan)
├─ Deploy and verify
└─ Measure improvement

Task 2: Optimize Query (1.5h)
├─ Rewrite query to be more efficient
├─ Remove Python-side filtering
├─ Test results are correct
├─ Write performance test
├─ Measure improvement

Task 3: Verify Fix (30 min)
├─ Run production data
├─ Benchmark: before/after
├─ Check for regressions
├─ Document changes
└─ Plan rollback


IMPLEMENTATION PHASE (2 hours):

Task 1: Add Index (15 min actual)
✓ COMPLETE
├─ Migration created
├─ Index added
├─ Verified in EXPLAIN output
├─ Immediate improvement: 25s → 8s
└─ Good progress

Task 2: Optimize Query (1.5h actual)
✓ COMPLETE
├─ Rewrote the report generation
├─ Removed Python-side grouping
├─ Used SQL aggregation directly
├─ All tests passing
└─ Measured: 8s → 2s

Task 3: Verify Fix (30 min actual)
✓ COMPLETE
├─ Tested with 1M records
├─ Verified accuracy
├─ Tested various date ranges
├─ Performance: 2.1 seconds
└─ Meets target!


REFLECTION & RESULTS:

Before:
├─ Report generation: 30-32 seconds
├─ Database lock during index: none yet
└─ User experience: Slow, frustrating

After:
├─ Report generation: 2.1 seconds
├─ Index creation: 5 minute one-time cost
└─ User experience: Snappy, responsive

Improvement: 14.3x faster (was 6x target)

Learnings:
1. Profiling is essential
   └─ Can't fix what you don't measure
2. Simple solutions first
   └─ Index before rewriting code
3. Verify improvements
   └─ Make sure fix actually helps
4. Document for team
   └─ Why was it slow? How was it fixed?

Total Time: 2 hours
└─ Research: 1 hour
└─ Planning: 0.5 hours
└─ Implementation: 2 hours
└─ (Some overlap, total ~2.5 hours)
```

**Speaker Notes:**
This example shows how the research-plan-implement cycle applies to bug fixes. Notice:

1. **Research was crucial:** Profiling found the real problem
2. **Explored options:** Didn't just pick first solution
3. **Prioritized:** Do quick fix first, then optimize
4. **Verified:** Measured before and after
5. **Documented:** So team understands why

This is much better than "just code the fix" without understanding the problem.

---

### Slide 30: Example 3 - Refactoring Planning
**Title:** Planning a Refactor: Splitting a Monolithic Module

**Content:**

```
SITUATION: User module has grown too large
├─ 2000 lines of code
├─ 15 different concerns (auth, profile, roles, etc)
├─ Hard to test
├─ Hard to understand
├─ Hard to extend
└─ Team agrees it needs refactoring

RESEARCH PHASE (2 hours):

1. Understand current structure:
   ├─ Read entire module
   ├─ Map dependencies
   ├─ List all responsibilities
   ├─ Find what's imported from this module
   └─ Identify natural boundaries

2. Current module responsibilities:
   ├─ User creation and deletion
   ├─ Authentication
   ├─ Role management
   ├─ Permission checking
   ├─ Profile management
   ├─ Settings management
   ├─ Profile picture upload
   ├─ Password reset
   ├─ Email verification
   ├─ Account deactivation
   ├─ And 5 more...

3. Natural groupings:
   ├─ Core user data (create, delete, basic info)
   ├─ Authentication (login, logout, sessions)
   ├─ Authorization (roles, permissions)
   ├─ Profile (bio, avatar, preferences)
   ├─ Account (password, email, settings)
   └─ Notifications (preference-driven notifications)

4. Dependencies discovered:
   ├─ Everything imports from users module
   ├─ Users module imports many things
   ├─ Circular dependency with auth module
   ├─ Profile picture upload uses file service
   └─ Email verification uses email service

PLANNING PHASE (2 hours):

Refactoring Strategy:

Old Structure:
└─ users/
   └─ models.py (2000 lines)

New Structure:
└─ users/
   ├─ models.py (core, 400 lines)
   ├─ authentication/
   │  ├─ models.py
   │  ├─ services.py
   │  └─ tests.py
   ├─ authorization/
   │  ├─ models.py
   │  ├─ services.py
   │  └─ tests.py
   ├─ profile/
   │  ├─ models.py
   │  ├─ services.py
   │  └─ tests.py
   ├─ account/
   │  ├─ models.py
   │  ├─ services.py
   │  └─ tests.py
   └─ __init__.py (public API)

Approach:
1. Create new module structure (not touching old)
2. Migrate one concern at a time
3. Update imports gradually
4. Run tests after each migration
5. Remove old code once all moved
6. Final cleanup

Key Decisions:
├─ Keep public API same (no breaking changes)
├─ Migrate one concern at a time (low risk)
├─ Test coverage throughout (quality)
├─ Document module responsibilities (clarity)
└─ Update all usages (consistency)

Task Breakdown:

Phase 1: Setup (2h)
├─ Create new module structure
├─ Create __init__.py with public API
├─ Set up tests for new structure
└─ Verify existing tests still pass

Phase 2: Authentication Refactor (4h)
├─ Move auth code to new module
├─ Update imports in old module
├─ Test authentication still works
├─ Update 8 files that use auth

Phase 3: Authorization Refactor (3h)
├─ Move authorization code
├─ Update imports
├─ Test role/permission checks
├─ Update 12 files that use auth

Phase 4: Profile Refactor (3h)
├─ Move profile code
├─ Update file upload integration
├─ Test profile operations
├─ Update 6 files

Phase 5: Account Refactor (3h)
├─ Move account operations
├─ Test password/email operations
├─ Update 4 files

Phase 6: Cleanup & Polish (2h)
├─ Remove old code
├─ Run full test suite
├─ Documentation
├─ Code review

Total Estimate: 17 hours


IMPLEMENTATION APPROACH:

Risk Mitigation:
├─ Keep old code during migration (dual running)
├─ Use feature flags for gradual rollout
├─ Don't remove old code until confident
├─ Heavy testing after each phase
├─ Code review before removing old code

Rollback Plan:
├─ If issues found, switch back to old code
├─ Old code stays until fully confident
├─ New code coexists with old temporarily
└─ Clear removal plan once confident


REFLECTION POINTS:

After Phase 1:
├─ Is new structure clear?
├─ Are tests easy to write?
├─ Any structural issues?
└─ Adjust before continuing?

After Phase 2-3:
├─ Is migration smooth?
├─ Any unexpected dependencies?
├─ Are tests passing?
└─ Confidence level?

Before Cleanup:
├─ All tests passing?
├─ All code migrated?
├─ All imports updated?
└─ Ready to remove old code?
```

**Speaker Notes:**
Refactoring is different from features or bugs—it's about improving code without changing behavior. This requires careful planning to avoid breaking things.

Key practices for refactoring:
1. **Small steps:** Migrate one concern at a time
2. **Keep old code:** Don't delete until confident
3. **Test frequently:** After each step
4. **Dual-running:** New and old code coexist
5. **Rollback plan:** If something breaks, revert

This is a systematic approach that minimizes risk.

---

### Slide 31: Example 4 - Database Migration Planning
**Title:** Planning a Large-Scale Database Change

**Content:**

```
SCENARIO: Migrate from MySQL to PostgreSQL

SCOPE:
├─ 50 GB database
├─ 20+ tables
├─ Complex relationships
├─ 99.99% uptime requirement
├─ 500+ daily active users
└─ Zero data loss acceptable

RESEARCH PHASE (4 hours):

1. Current state analysis:
   ├─ Database schema review
   ├─ Data volume per table
   ├─ Index structure
   ├─ Key relationships
   ├─ Custom code dependencies
   └─ Application integration points

2. Target state definition:
   ├─ PostgreSQL schema
   ├─ Schema optimizations for PG
   ├─ New indexes to add
   ├─ Deprecated features to remove
   └─ Performance improvements

3. Risk analysis:
   ├─ Data loss risks
   ├─ Downtime risks
   ├─ Performance risks
   ├─ Application compatibility risks
   └─ Rollback complexity

PLANNING PHASE (3 hours):

Strategy: Blue-Green Deployment

Old Environment (Blue):
└─ MySQL, production data
   ├─ Users accessing
   ├─ Data being written
   └─ Cannot afford downtime

New Environment (Green):
└─ PostgreSQL, replicated data
   ├─ Parallel with Blue
   ├─ Kept in sync
   ├─ Validated thoroughly
   └─ Ready for switchover

Migration Phases:

Phase 1: Setup Green Environment (2 days)
├─ Provision PostgreSQL servers
├─ Set up replication from MySQL
├─ Schema migration
├─ Initial data load
└─ Validation

Phase 2: Keep in Sync (1 week)
├─ Continuous replication
├─ Test application against Green
├─ Fix any compatibility issues
├─ Validate all features work
├─ Performance testing

Phase 3: Switchover (2-4 hours)
├─ Final sync to latest
├─ Stop writes to Blue
├─ Verify all data replicated
├─ Point application to Green
├─ Monitor for issues
└─ Rollback plan ready

Phase 4: Cleanup (1 day)
├─ Verify no issues for 24 hours
├─ Keep Blue as backup briefly
├─ Decommission Blue
└─ Document lessons


DETAILED TASK BREAKDOWN:

Phase 1: Setup (16h)

Task 1.1: PostgreSQL Infrastructure (3h)
├─ Provision servers (matching MySQL capacity)
├─ Set up replication
├─ Configure security
├─ Set up monitoring
└─ Verify connectivity

Task 1.2: Schema Migration (4h)
├─ Export MySQL schema
├─ Convert to PostgreSQL syntax
│  ├─ Data type conversions
│  ├─ Index syntax
│  └─ Constraint differences
├─ Test schema creates correctly
├─ Verify all tables present
└─ Fix any issues

Task 1.3: Data Migration (5h)
├─ Full data dump from MySQL
├─ Load into PostgreSQL
├─ Verify row counts match
├─ Check for data type issues
├─ Validate key relationships
└─ Fix any corrupt data

Task 1.4: Validation (4h)
├─ Row counts match (exact)
├─ Data integrity checks
├─ Index validation
├─ Performance baseline
└─ Replication verification

Phase 2: Testing & Sync (40h)

Task 2.1: Continuous Replication (3h)
├─ Set up binary log replication
├─ Verify replication working
├─ Monitor lag
└─ Test lag recovery

Task 2.2: Application Testing (20h)
├─ Test each feature with PostgreSQL
├─ Fix application compatibility
├─ Data conversion issues
├─ Timeout/performance issues
└─ All features working

Task 2.3: Monitoring & Validation (10h)
├─ Monitor system for issues
├─ Validate data consistency
├─ Spot-check records
├─ Query performance
└─ Log analysis

Task 2.4: Performance Testing (7h)
├─ Load testing with realistic traffic
├─ Peak load testing
├─ Slow query analysis
├─ Index optimization
└─ Final performance validation

Phase 3: Switchover (8h)

Task 3.1: Pre-Switchover (4h)
├─ Final data sync
├─ Stop new writes (brief window)
├─ Verify zero lag
├─ Last-minute checks
└─ Notification to team

Task 3.2: Switchover (1h)
├─ Application points to PostgreSQL
├─ Verify reads working
├─ Verify writes working
├─ Check error logs
└─ Monitor metrics

Task 3.3: Post-Switchover (3h)
├─ Heavy monitoring
├─ User reports (listen for issues)
├─ Performance metrics
├─ Error rate tracking
└─ Stay on alert


RISKS & MITIGATIONS:

Risk: Data loss during migration
├─ Mitigation: Validate at each step
├─ Mitigation: Keep Blue active as backup
└─ Mitigation: Automated validation

Risk: Application incompatibility
├─ Mitigation: Extensive testing in Phase 2
├─ Mitigation: Rollback plan ready
└─ Mitigation: Staged rollout if issues found

Risk: Performance degradation
├─ Mitigation: Performance testing Phase 2
├─ Mitigation: Index optimization
└─ Mitigation: Monitor closely post-switch

Risk: Replication lag
├─ Mitigation: Monitor lag continuously
├─ Mitigation: Automatic failover if exceeds threshold
└─ Mitigation: Manual sync procedures


TIMELINE:
├─ Phase 1: 2 days
├─ Phase 2: 1 week
├─ Phase 3: 1 day
├─ Total: 10 calendar days
└─ Actual work: ~70 hours spread over team
```

**Speaker Notes:**
Large migrations require meticulous planning. The blue-green approach is used for large systems because it allows thorough testing without impacting users.

Key principles for large migrations:
1. **Parallel systems:** Don't touch production until ready
2. **Thorough testing:** Check everything multiple times
3. **Staged rollout:** Can rollback if issues found
4. **Monitoring:** Watch closely after switchover
5. **Rollback plan:** Know how to get back to old system

This is not something to rush or improvise.

---

### Slide 32: Example 5 - Integration Work Planning
**Title:** Planning Complex Integration - Payment Processing

**Content:**

```
SCENARIO: Integrate Stripe payment processing

REQUIREMENTS:
├─ Users can purchase subscriptions
├─ Handle recurring billing
├─ Manage cancellations
├─ Handle payment failures
├─ Webhook notifications
├─ Compliance with PCI standards
└─ Works with existing database

RESEARCH PHASE (3 hours):

1. Stripe API understanding:
   ├─ Payment methods
   ├─ Subscription handling
   ├─ Webhook system
   ├─ Error handling
   ├─ Testing environment
   └─ Rate limits

2. Existing system analysis:
   ├─ Current user model
   ├─ Current billing approach (if any)
   ├─ Database schema design
   ├─ API endpoint structure
   ├─ Error handling patterns
   └─ Testing approach

3. Integration points identified:
   ├─ User authentication (who's buying?)
   ├─ Subscription types (what are they buying?)
   ├─ Database changes needed (store what?)
   ├─ API endpoints (how do users initiate purchase?)
   ├─ Webhooks (how do we respond to Stripe events?)
   └─ Error cases (what can go wrong?)

4. Constraints discovered:
   ├─ PCI compliance (no storing credit card data)
   ├─ Webhook security (verify signatures)
   ├─ Idempotency (webhooks might retry)
   ├─ Timezone handling (billing dates)
   ├─ Currency support (if needed)
   └─ Compliance (GDPR, etc)

PLANNING PHASE (2 hours):

Architecture Design:

Database Changes:
├─ Add Stripe customer ID to users table
├─ Create subscriptions table
│  ├─ subscription_id (Stripe ID)
│  ├─ user_id
│  ├─ status (active, canceled, past_due)
│  ├─ plan_id
│  ├─ start_date
│  ├─ current_period_end
│  ├─ canceled_at
│  └─ metadata (raw Stripe data)
├─ Create payments table
│  ├─ payment_id (Stripe ID)
│  ├─ user_id
│  ├─ amount
│  ├─ status (succeeded, failed, refunded)
│  ├─ created_at
│  └─ metadata
└─ Create webhook_events table (for idempotency)

API Design:
├─ GET /api/billing/status (current subscription)
├─ POST /api/billing/subscribe (start subscription)
├─ POST /api/billing/cancel (cancel subscription)
├─ POST /api/billing/webhook (webhook receiver)
└─ GET /api/billing/history (payment history)

Webhook Handling:
├─ Events to handle:
│  ├─ customer.subscription.created
│  ├─ customer.subscription.updated
│  ├─ customer.subscription.deleted
│  ├─ invoice.payment_succeeded
│  ├─ invoice.payment_failed
│  └─ charge.refunded
├─ Verification (signature checking)
├─ Idempotency (check if already processed)
└─ Error handling (retry logic)

Task Breakdown:

Phase 1: Setup (8h)

Task 1.1: Stripe Account & Keys (1h)
├─ Create Stripe account
├─ Get API keys (public/secret)
├─ Set up webhook endpoints
├─ Configure webhook signing
└─ Test keys working

Task 1.2: Database Schema (3h)
├─ Create migration for new tables
├─ Add columns to users table
├─ Create subscriptions table
├─ Create payments table
├─ Create webhook_events table
├─ Add indexes
└─ Write migrations

Task 1.3: Stripe Client Setup (2h)
├─ Add Stripe SDK to project
├─ Create Stripe service class
├─ Configure API keys from environment
├─ Add error handling
└─ Write basic tests

Task 1.4: Testing Setup (2h)
├─ Configure Stripe test mode
├─ Create test payment methods
├─ Mock Stripe responses
├─ Write test fixtures
└─ Document test procedures

Phase 2: Subscription Management (12h)

Task 2.1: Subscribe Endpoint (4h)
├─ Create Stripe customer (if needed)
├─ Create subscription via Stripe
├─ Store subscription in database
├─ Handle errors (invalid card, etc)
├─ Return confirmation to user
└─ Write comprehensive tests

Task 2.2: Subscription Status (2h)
├─ Fetch subscription from database
├─ Return current status
├─ Include renewal date
├─ Include plan information
└─ Write tests

Task 2.3: Cancel Subscription (3h)
├─ Cancel in Stripe
├─ Update database
├─ Handle refunds (if applicable)
├─ Notify user
├─ Schedule account downgrade
└─ Write tests

Task 2.4: View Payment History (3h)
├─ Query payments from database
├─ Format for display
├─ Include invoice URLs
├─ Pagination
└─ Write tests

Phase 3: Webhooks (8h)

Task 3.1: Webhook Receiver (3h)
├─ POST /api/billing/webhook endpoint
├─ Verify Stripe signature
├─ Parse event data
├─ Log for debugging
├─ Return 200 immediately
└─ Write tests

Task 3.2: Event Handlers (4h)
├─ Handle subscription.created
│  └─ Store in database
├─ Handle subscription.updated
│  └─ Update status
├─ Handle invoice.payment_succeeded
│  └─ Log payment, grant access
├─ Handle invoice.payment_failed
│  └─ Alert user, downgrade if needed
├─ Handle subscription.deleted
│  └─ Cleanup
└─ Write tests for each

Task 3.3: Idempotency (1h)
├─ Check webhook_events table before processing
├─ Store event ID after processing
├─ Prevent duplicate operations
└─ Write tests

Phase 4: Error Handling & Edge Cases (6h)

Task 4.1: Payment Failures (2h)
├─ Handle declined cards
├─ Retry logic
├─ User notification
├─ Suspension rules
└─ Tests

Task 4.2: Subscription Edge Cases (2h)
├─ Multiple subscriptions?
├─ Plan changes
├─ Metadata handling
└─ Tests

Task 4.3: Reconciliation (2h)
├─ Verify DB matches Stripe
├─ Handle manual Stripe changes
├─ Cleanup script
└─ Tests

Phase 5: Testing & Documentation (6h)

Task 5.1: Integration Tests (3h)
├─ Full flow: subscribe → pay → webhook → access
├─ Failure flow: declined card → retry
├─ Cancellation flow
└─ All tests passing

Task 5.2: Documentation (2h)
├─ API documentation
├─ Setup instructions
├─ Testing guide
├─ Troubleshooting
└─ Webhook debugging

Task 5.3: Security Review (1h)
├─ PCI compliance check
├─ Webhook signature verification
├─ No credential exposure
├─ Error messages safe
└─ Approval from security


TOTAL ESTIMATE: 40 hours

Risk Mitigation:
├─ Test thoroughly in Stripe test mode
├─ Don't use real cards until confident
├─ Webhook testing via local tunnel
├─ Security review before launch
└─ Gradual rollout to users (beta)
```

**Speaker Notes:**
Integration work requires understanding both systems—your code and the external system. Good planning ensures smooth integration.

Key practices:
1. **Understand external system:** Read docs, ask questions
2. **Test extensively:** Use test APIs before touching production
3. **Plan for failures:** What happens when payments fail?
4. **Security first:** Integrate securely from the start
5. **Gradual rollout:** Don't flip a switch for everyone at once

---

### Slide 33: Example 6 - Performance Optimization Planning
**Title:** Planning Performance Improvements - API Response Times

**Content:**

```
SITUATION: API endpoints have variable performance
├─ Best case: 100ms
├─ Average: 300ms
├─ Worst case: 5 seconds
├─ Target: p95 <200ms consistently
└─ Impact: User experience suffers

RESEARCH PHASE (2 hours):

1. Performance Profiling:
   ├─ APM tool analysis (DataDog/New Relic)
   │  ├─ Database queries: 45% of time
   │  ├─ Serialization: 20% of time
   │  ├─ API calls: 25% of time
   │  └─ Other: 10% of time
   ├─ Slow queries identified:
   │  ├─ N+1 queries in user endpoint
   │  ├─ Full table scan in reports
   │  └─ Missing indexes
   ├─ Bottlenecks found:
   │  ├─ External API calls not parallelized
   │  ├─ Large response serialization
   │  └─ No response caching
   └─ Resource usage:
      ├─ CPU: 60% average, spikes to 90%
      ├─ Memory: 40% average
      └─ Database connections: Sometimes maxed

2. Root cause analysis:
   ├─ Database: N+1 queries, missing indexes
   ├─ API calls: Waiting for external services
   ├─ Serialization: Large responses
   ├─ Caching: No caching strategy
   └─ Connection pooling: Not optimized

PLANNING PHASE (1.5 hours):

Strategy: Layered Optimization

Layer 1: Database Optimization (High impact, low effort)
├─ Add indexes (20% improvement)
├─ Fix N+1 queries (30% improvement)
├─ Query optimization (15% improvement)
└─ Total potential: 65% improvement

Layer 2: Caching Strategy (Medium impact, medium effort)
├─ Response caching (20% improvement)
├─ Database query caching (10% improvement)
├─ Computed result caching (10% improvement)
└─ Total potential: 40% improvement

Layer 3: External Calls Optimization (Medium impact, low effort)
├─ Parallel API calls (15% improvement)
├─ Call timeouts (5% improvement)
├─ Connection pooling (10% improvement)
└─ Total potential: 30% improvement

Layer 4: Serialization (Low impact, low effort)
├─ Selective field return (5% improvement)
├─ Compression (3% improvement)
└─ Total potential: 8% improvement


Task Breakdown:

Phase 1: Database (12h)

Task 1.1: Identify Missing Indexes (2h)
├─ Query logs analysis
├─ EXPLAIN plan analysis
├─ Find full table scans
├─ Identify potential indexes
├─ Document recommendations
└─ Review and get approval

Task 1.2: Add Indexes (3h)
├─ Create migration for each index
├─ Add 8-10 identified indexes
├─ Test query plans improve
├─ Measure response time improvement
├─ Document index rationale
└─ Tests still passing

Task 1.3: Fix N+1 Queries (5h)
├─ Identify N+1 problem queries
├─ Refactor to use joins or eager loading
├─ Write test to prevent regression
├─ Measure improvement
├─ Validate correctness
└─ Code review

Task 1.4: Query Optimization (2h)
├─ Optimize remaining slow queries
├─ Review execution plans
├─ Measure improvements
└─ Document changes

Phase 2: Caching (10h)

Task 2.1: Response Caching (4h)
├─ Implement HTTP cache headers
├─ Set appropriate TTLs
├─ Add Redis layer
├─ Cache invalidation strategy
├─ Write tests
└─ Measure improvement

Task 2.2: Query Caching (3h)
├─ Cache database query results
├─ Set TTL strategy
├─ Invalidation triggers
├─ Write tests
└─ Measure improvement

Task 2.3: Computed Result Caching (3h)
├─ Cache expensive calculations
├─ Set update intervals
├─ Invalidation approach
├─ Write tests
└─ Measure improvement

Phase 3: External Calls (5h)

Task 3.1: Parallelize Calls (2h)
├─ Identify sequential API calls
├─ Refactor to call in parallel
├─ Handle failures gracefully
├─ Write tests
└─ Measure improvement

Task 3.2: Connection Pooling (2h)
├─ Configure connection pools
├─ Set pool sizes appropriately
├─ Test under load
└─ Measure improvement

Task 3.3: Call Timeouts (1h)
├─ Set appropriate timeouts
├─ Handle timeout gracefully
└─ Tests

Phase 4: Validation & Measurement (6h)

Task 4.1: Performance Benchmarking (2h)
├─ Baseline before changes
├─ Measure after each optimization
├─ Load test to find new bottlenecks
├─ Document improvements
└─ Compare to targets

Task 4.2: Regression Testing (2h)
├─ Ensure no correctness issues
├─ Verify all endpoints work
├─ Check edge cases
└─ All tests passing

Task 4.3: Production Validation (2h)
├─ Monitor after deployment
├─ A/B test if needed
├─ Verify actual improvements
├─ Fine-tune caching
└─ Document final results


EXPECTED IMPROVEMENTS:

Layer 1 (Database): 65% improvement
├─ Before: 300ms
└─ After: 105ms

Layer 2 (Caching): +40% improvement
├─ Before: 105ms
└─ After: 63ms

Layer 3 (External): +30% improvement
├─ Before: 63ms
└─ After: 44ms

Layer 4 (Serialization): +8% improvement
├─ Before: 44ms
└─ After: 40ms

Final: 40ms average (from 300ms)
└─ Achieved target: p95 <200ms ✓


TIMELINE:
├─ Phase 1: 2-3 days
├─ Phase 2: 2 days
├─ Phase 3: 1 day
├─ Phase 4: 1 day
├─ Total: 6-7 days
└─ Total effort: ~30 hours
```

**Speaker Notes:**
Performance optimization requires methodical analysis. The key is:
1. **Measure first:** Find the real bottlenecks
2. **Prioritize:** Fix what matters most first
3. **Validate:** Measure improvements
4. **Iterate:** Find next bottleneck

Don't guess where the problem is—measure it.

---

### Slide 34: Integration Patterns - Combining Multiple Examples
**Title:** Multi-System Planning: Feature + Performance + Refactoring

**Content:**

```
REAL-WORLD SCENARIO:
Add new reporting feature AND improve performance

COMBINED REQUIREMENTS:
├─ New feature: User-defined reports
├─ Performance: Reporting queries too slow
├─ Quality: Existing reporting code is messy
└─ Timeline: 3 weeks

PLANNING APPROACH:

Option A: Separate projects
├─ Feature project: Add user reports (2 weeks)
├─ Performance project: Optimize queries (1 week)
├─ Result: Work is independent, long timeline
└─ Problem: Separate work is wasteful

Option B: Combined approach (RECOMMENDED)
├─ Do them together
├─ Use refactoring to enable performance
├─ Use new feature to validate improvements
└─ Result: Shorter timeline, better quality

COMBINED PLANNING:

Phase 1: Setup & Planning (3 days)
├─ Research existing reporting code
├─ Plan new feature requirements
├─ Plan refactoring approach
├─ Plan performance optimization
├─ Get approval on all three

Phase 2: Refactoring (3 days)
├─ Split monolithic reporting module
├─ Create clear interfaces
├─ Add performance metrics
└─ Improved code + easier to optimize

Phase 3: New Feature (5 days)
├─ Build feature on refactored code
├─ Implement performance optimizations
├─ Tests for new feature
└─ New feature works fast

Phase 4: Validation (2 days)
├─ Performance goals met
├─ New feature works
├─ Old reports still work
├─ Tests passing
└─ Ready for production

TOTAL: ~2 weeks (vs 3 weeks if separate)
BENEFIT: Better code + new feature + performance


PLANNING DOCUMENTS:

Combined Planning Doc structure:
├─ Section 1: Feature Requirements
├─ Section 2: Refactoring Plan
├─ Section 3: Performance Plan
├─ Section 4: Integration (how they work together)
├─ Section 5: Task Breakdown
├─ Section 6: Risk Analysis
├─ Section 7: Timeline
└─ Section 8: Success Criteria


Task Decomposition Strategy:

Traditional: Do separately
├─ Refactoring Tasks (15 tasks)
├─ Feature Tasks (12 tasks)
├─ Performance Tasks (8 tasks)
└─ Total: 35 tasks (harder to coordinate)

Combined: Do together
├─ Foundation Phase (10 tasks)
├─ Feature Implementation (10 tasks)
├─ Validation Phase (5 tasks)
└─ Total: 25 tasks (coordinated approach)


ADVANTAGES:

Code Quality:
├─ Refactoring improves code structure
├─ Cleaner code easier to optimize
├─ New feature uses best patterns
└─ Overall quality much better

Performance:
├─ Optimization happens during feature build
├─ Optimization informed by new feature
├─ Performance proven with real use case
└─ Better alignment with actual needs

Timeline:
├─ Overlap between efforts
├─ Less rework
├─ Coordinated approach faster
└─ 33% time savings possible

Team Coordination:
├─ One goal instead of three
├─ Easier communication
├─ Less context switching
├─ Higher team morale
```

**Speaker Notes:**
In real projects, multiple concerns often overlap. The best approach is to plan them together, finding synergies that make them faster to complete together than separately.

This requires seeing the connections and planning holistically.

---

### Slide 35: Planning Tools and Templates
**Title:** Documents and Checklists to Make Planning Easier

**Content:**

```
PLANNING DOCUMENTS TO CREATE:

1. REQUIREMENTS DOCUMENT
   ├─ Feature description
   ├─ User stories
   ├─ Acceptance criteria
   ├─ Non-functional requirements
   └─ Constraints and limitations

   Template:
   ┌─ Feature: [Name]
   ├─ Goal: [What problem does it solve?]
   ├─ Requirements:
   │  ├─ Functional: [What must it do?]
   │  └─ Non-functional: [Performance, scale, etc]
   ├─ Acceptance Criteria:
   │  ├─ ☐ Criterion 1
   │  ├─ ☐ Criterion 2
   │  └─ ☐ Criterion 3
   ├─ Constraints:
   │  ├─ Timeline
   │  ├─ Resources
   │  ├─ Technology
   │  └─ Budget
   └─ Success Metrics:
      └─ [How do we know it worked?]


2. ARCHITECTURE DOCUMENT
   ├─ System diagram
   ├─ Component descriptions
   ├─ Data flow
   ├─ Key interfaces
   ├─ Technology choices
   └─ Rationales

   Template:
   ┌─ Overview: [1-2 paragraph description]
   ├─ Architecture Diagram: [ASCII art]
   ├─ Components:
   │  ├─ Component 1: [Purpose, responsibilities]
   │  ├─ Component 2: [Purpose, responsibilities]
   │  └─ ...
   ├─ Data Model: [Database schema]
   ├─ Interfaces:
   │  ├─ API endpoints
   │  ├─ Function signatures
   │  └─ Data contracts
   ├─ Key Decisions:
   │  ├─ Decision 1: [What, why]
   │  ├─ Decision 2: [What, why]
   │  └─ ...
   └─ Rationale: [Why this design?]


3. TASK BREAKDOWN DOCUMENT
   ├─ Detailed task list
   ├─ Task descriptions
   ├─ Estimates
   ├─ Dependencies
   ├─ Acceptance criteria
   └─ Success criteria

   Template:
   ┌─ Phase 1: [Phase Name]
   ├─ Task 1.1: [Task Name]
   │  ├─ Effort: [Hours]
   │  ├─ Description: [What needs to be done]
   │  ├─ Acceptance Criteria:
   │  │  ├─ ☐ Criterion 1
   │  │  └─ ☐ Criterion 2
   │  ├─ Dependencies: [What must come first]
   │  └─ Tests: [What needs testing]
   ├─ Task 1.2: [...]
   └─ ...


4. RISK ASSESSMENT
   ├─ Identified risks
   ├─ Probability assessment
   ├─ Impact assessment
   ├─ Mitigation strategies
   └─ Contingency plans

   Template:
   ┌─ Risk: [What could go wrong?]
   ├─ Probability: [High/Medium/Low]
   ├─ Impact: [High/Medium/Low]
   ├─ Mitigation:
   │  ├─ Prevention: [How to prevent?]
   │  └─ Response: [What if it happens?]
   ├─ Owner: [Who watches for this?]
   └─ ...


5. TEST STRATEGY
   ├─ Testing approach
   ├─ Test levels
   ├─ Test scenarios
   ├─ Acceptance criteria
   └─ Test schedule

   Template:
   ┌─ Unit Testing:
   │  ├─ Scope: [What's tested]
   │  ├─ Coverage Target: [80%+]
   │  └─ Approach: [Mocks, fixtures, etc]
   ├─ Integration Testing:
   │  ├─ Scope: [How components work together]
   │  └─ Approach: [Test scenarios]
   ├─ System Testing:
   │  ├─ Scope: [End-to-end workflows]
   │  └─ Approach: [User scenarios]
   └─ Performance Testing:
      ├─ Benchmarks: [What we're measuring]
      └─ Targets: [Acceptable performance]


PLANNING CHECKLISTS:

REQUIREMENTS CHECKLIST:
☐ Problem is clearly stated
☐ Success criteria are measurable
☐ All constraints identified
☐ Non-functional requirements listed
☐ Edge cases considered
☐ Team alignment achieved

ARCHITECTURE CHECKLIST:
☐ Architecture is documented
☐ Diagrams are clear
☐ Rationales are explained
☐ Patterns match existing code
☐ Scalability considered
☐ Security considered
☐ Team agrees on approach

TASK BREAKDOWN CHECKLIST:
☐ All work items identified
☐ Tasks are appropriately sized (3-8 hours)
☐ Dependencies are mapped
☐ Critical path is identified
☐ Estimates are realistic
☐ Effort is reasonable
☐ Can be parallelized where appropriate

RISK ASSESSMENT CHECKLIST:
☐ Major risks identified
☐ Probability estimated
☐ Impact assessed
☐ Mitigation plans exist
☐ Contingencies planned
☐ Owner assigned for each risk
☐ Review plan includes risk checks

TEST STRATEGY CHECKLIST:
☐ Test levels defined
☐ Test scenarios identified
☐ Coverage targets set
☐ Acceptance criteria clear
☐ Performance targets defined
☐ Resource allocation planned
☐ Timeline included

TEAM ALIGNMENT CHECKLIST:
☐ Everyone understands requirements
☐ Everyone agrees on architecture
☐ Everyone knows their tasks
☐ Dependencies are clear
☐ Timeline is agreed
☐ Success criteria are understood
☐ Questions have been answered


TEMPLATES AND EXAMPLES:

Available templates in this course:
├─ requirements_template.md
├─ architecture_template.md
├─ taskbreakdown_template.md
├─ risk_assessment_template.md
├─ test_strategy_template.md
└─ planning_checklist.md

Real examples from this slideshow:
├─ Dashboard feature (Slide 27)
├─ Bug fix planning (Slide 29)
├─ Refactoring planning (Slide 30)
├─ Database migration (Slide 31)
├─ Integration planning (Slide 32)
└─ Performance optimization (Slide 33)
```

**Speaker Notes:**
Good planning requires good documentation. These templates and checklists help ensure you don't miss anything and everyone is aligned.

Use these as starting points—adjust for your specific needs and context.

---

### Slide 36: Common Planning Mistakes to Avoid
**Title:** What to Watch Out For When Planning

**Content:**

```
TOP PLANNING MISTAKES:

MISTAKE 1: Vague Requirements
❌ Bad: "Add better notifications"
✓ Good: "Add email notifications for new messages.
         Send within 5 minutes. Support digest mode."

How to avoid:
├─ Write specific, measurable requirements
├─ Include acceptance criteria
├─ Discuss with stakeholders
└─ Document edge cases

MISTAKE 2: Missing Dependencies
❌ Bad: Tasks look independent but aren't
✓ Good: Dependency graph shows what must come first

How to avoid:
├─ Draw dependency diagrams
├─ Ask "what must happen first?"
├─ Walk through implementation mentally
└─ Ask team for feedback

MISTAKE 3: Unrealistic Estimates
❌ Bad: "Database migration in 2 hours"
✓ Good: "Database migration in 2 days + testing"

How to avoid:
├─ Use historical data
├─ Add buffer for unknowns
├─ Include testing time
├─ Break big tasks into smaller ones
├─ Don't estimate, measure instead

MISTAKE 4: Incomplete Test Plan
❌ Bad: "Write tests" (too vague)
✓ Good: "Unit tests >80%, integration tests for
         payment flows, performance tests for scale"

How to avoid:
├─ Plan tests as part of task
├─ Define coverage targets
├─ Include edge cases in test plan
├─ Plan for automation
└─ Budget test time (25-30% of effort)

MISTAKE 5: No Risk Identification
❌ Bad: Assume nothing will go wrong
✓ Good: Identify risks and mitigation

How to avoid:
├─ Ask "what could go wrong?"
├─ Identify external dependencies
├─ Plan for failures
├─ Have rollback strategies
└─ Budget contingency time

MISTAKE 6: Team Not Aligned
❌ Bad: Some people think it's feature A, others B
✓ Good: Everyone understands the same goal

How to avoid:
├─ Share plan with full team
├─ Get feedback and questions
├─ Update plan based on feedback
├─ Verify understanding
└─ Document decisions

MISTAKE 7: Too Much Detail
❌ Bad: Plan every line of code before starting
✓ Good: Plan enough to start building with confidence

How to avoid:
├─ Plan high-level first (phases)
├─ Detail plan emerges as you learn
├─ Don't over-commit to initial design
├─ Plan should guide, not constrain
└─ Be ready to adjust

MISTAKE 8: Skipping Feasibility Check
❌ Bad: Propose technically unsound plan
✓ Good: Have expert review plan for feasibility

How to avoid:
├─ Share plan with technical team
├─ Ask "can we actually do this?"
├─ Challenge assumptions
├─ Identify missing pieces
└─ Adjust plan

MISTAKE 9: No Acceptance Criteria
❌ Bad: "Done when it works"
✓ Good: "Done when all tests pass, performance
         meets targets, and code review approved"

How to avoid:
├─ Define "done" explicitly
├─ List specific criteria
├─ Make criteria measurable
├─ Include code quality metrics
└─ Include performance targets

MISTAKE 10: Planning Happens in a Vacuum
❌ Bad: One person plans, team executes
✓ Good: Team collaborates on planning

How to avoid:
├─ Include engineers in planning
├─ Get operations input
├─ Discuss with product/design
├─ Ask for feedback
├─ Build consensus


PLANNING ANTI-PATTERNS:

"I'll plan as I go"
├─ Problem: No direction, wasted effort
├─ Solution: Do upfront planning

"The plan is perfect"
├─ Problem: No flexibility, can't adapt
├─ Solution: Plan serves as guide, not scripture

"Analysis paralysis"
├─ Problem: Over-planning, never start
├─ Solution: Plan enough to start, refine as you learn

"We don't have time to plan"
├─ Problem: End up with no plan AND no time
├─ Solution: Planning saves time overall

"The architect will decide"
├─ Problem: Disconnect between plan and reality
├─ Solution: Builders should help with planning


SIGNS YOUR PLAN IS GOOD:

✓ Everyone understands the goal
✓ Tasks are clear and appropriately sized
✓ Dependencies make sense
✓ Estimates seem realistic
✓ Team has confidence in the plan
✓ Risks are identified
✓ Tests are planned
✓ Success criteria are clear
✓ Team can start immediately

SIGNS YOUR PLAN NEEDS WORK:

✗ Ambiguous goals
✗ Unclear tasks
✗ Dependencies seem wrong
✗ Estimates seem optimistic
✗ Team is uncertain
✗ Risks are unidentified
✗ No test strategy
✗ Unclear when "done"
✗ Can't start for another week
```

**Speaker Notes:**
These are the most common mistakes in planning. Knowing them helps you avoid them. Review this before finalizing your plan.

---

### Slide 37: Planning with Agentic Tools - Best Practices
**Title:** How to Work Effectively with Agents During Planning

**Content:**

```
WORKING WITH AGENTS DURING PLANNING PHASE:

THE AGENT'S ROLE:

Agent can help by:
├─ Analyzing existing code
├─ Finding similar implementations
├─ Suggesting architectures
├─ Identifying risks
├─ Decomposing into tasks
├─ Estimating effort
├─ Writing plan documents
└─ Validating plans

YOU STAY IN CONTROL:

You decide:
├─ Requirements and goals
├─ Constraints and trade-offs
├─ Whether proposed approach is right
├─ Final plan approval
├─ Timeline and resources
└─ Risk tolerance


PLANNING PROMPT FRAMEWORK:

Good planning prompts have:

1. CONTEXT
   ├─ What are you building?
   ├─ Why is it important?
   ├─ Who are the users?
   └─ What problem does it solve?

2. CONSTRAINTS
   ├─ Performance requirements?
   ├─ Scalability requirements?
   ├─ Timeline?
   ├─ Resources available?
   └─ Technology limitations?

3. EXISTING PATTERNS
   ├─ Show examples of code
   ├─ Show testing patterns
   ├─ Show error handling
   ├─ Show API design
   └─ Show database patterns

4. SPECIFIC REQUEST
   ├─ "Before you code, please provide:"
   ├─ Architecture overview
   ├─ Task breakdown with estimates
   ├─ Identified risks and mitigations
   ├─ Test strategy
   └─ Any clarifying questions


PLANNING PROMPT TEMPLATE:

"I want to [feature description].

Requirements:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Constraints:
- Timeline: [time]
- Performance target: [metric]
- Scale: [expected usage]
- Technology: [what tools/libs to use]

Context:
- Here's how we do [thing] currently: [code example]
- We follow this [pattern]: [code example]
- Our testing approach: [code example]

Before you start coding, please:
1. Analyze the codebase and these requirements
2. Propose an architecture
3. Break down into specific tasks (3-8 hours each)
4. Identify major risks and mitigations
5. Propose a test strategy
6. Estimate total effort
7. Ask any clarifying questions

I'll review and provide feedback before you build."


EVALUATING AGENT'S PLAN:

Questions to ask:

Architecture:
├─ "Does this match our existing patterns?"
├─ "Are there architectural issues I should know?"
├─ "Could this cause problems with scale?"
└─ "Will this be hard to maintain?"

Tasks:
├─ "Are these tasks appropriately sized?"
├─ "Are dependencies correct?"
├─ "Are estimates realistic?"
└─ "Can I parallelize any of these?"

Risks:
├─ "Are major risks identified?"
├─ "Are mitigations adequate?"
├─ "What else could go wrong?"
└─ "Do we have rollback plans?"

Tests:
├─ "Is test coverage adequate?"
├─ "What about edge cases?"
├─ "How do we test failures?"
└─ "Performance testing plan?"


GIVING FEEDBACK TO AGENT:

Clear feedback:
✓ "This approach is too complex. Can we simplify?"
✓ "We don't use external APIs. Can we do this
   without external calls?"
✓ "This doesn't match our database patterns.
   See this example: [code]"

Vague feedback:
✗ "I don't like this approach"
✗ "This seems wrong"
✗ "Can you make it better?"

Better feedback gives:
├─ Specific concern
├─ Reason for concern
├─ Example of what you want
└─ Request for change


ITERATION PROCESS:

Round 1: Agent proposes
├─ You review
└─ Identify issues

Round 2: You provide feedback
├─ Agent refines
└─ You review again

Round 3: Back and forth
├─ Until plan is good
└─ Then proceed to implementation

This is not wasted time—good planning prevents bad implementation.


RED FLAGS IN AGENT'S PLAN:

Be skeptical if agent:
├─ Proposes tasks >12 hours
├─ Has circular dependencies
├─ Estimates seem too optimistic
├─ Doesn't mention testing
├─ Doesn't address risks
├─ Doesn't understand your constraints
├─ Doesn't follow your patterns
├─ Proposes unnecessary complexity
└─ Can't explain the rationale


WHEN TO REJECT AND RESTART:

Reject the plan if:
├─ Fundamentally misunderstands goal
├─ Proposes technically infeasible approach
├─ Ignores your constraints
├─ Seems to miss major pieces
├─ Is overly complex
├─ Doesn't address key risks
└─ Team doesn't have confidence

When rejecting:
├─ Be specific: "This is wrong because..."
├─ Provide guidance: "I think we should..."
├─ Ask for restart: "Let's start over with..."
└─ Give new context: "Consider this instead..."


AGENT'S ROLE IN DIFFERENT PLANNING PHASES:

Research Phase:
├─ Agent explores codebase
├─ Agent finds patterns
├─ Agent suggests considerations
└─ You synthesize findings

Planning Phase:
├─ Agent proposes architecture
├─ Agent decomposes tasks
├─ Agent identifies risks
├─ You decide on approach

Implementation Phase:
├─ Agent codes according to plan
├─ Agent writes tests
├─ You review and validate
└─ Agent refines based on feedback

Review Phase:
├─ Agent helps with testing
├─ You validate against plan
├─ Agent fixes issues
└─ You approve
```

**Speaker Notes:**
Working with agents during planning is a partnership. The agent brings analysis and ideas, you bring domain knowledge and judgment. Together, you create better plans than either could alone.

Key principle: **The agent serves the planning process, not vice versa.**

---

### Slide 38: Planning for Different Project Types
**Title:** Adjusting Planning for Your Specific Situation

**Content:**

```
PLANNING TIME ALLOCATION BY PROJECT TYPE:

Small Project (1-3 days):
├─ Research: 20% (few hours)
├─ Planning: 10% (1-2 hours)
├─ Implementation: 65% (mostly coding)
├─ Review: 5% (quick)
└─ Total: ~3 days

Medium Project (1-2 weeks):
├─ Research: 15% (half day)
├─ Planning: 15% (1-2 days)
├─ Implementation: 60% (4-6 days)
├─ Review: 10% (1 day)
└─ Total: ~2 weeks

Large Project (1-2 months):
├─ Research: 10% (few days)
├─ Planning: 15% (1-2 weeks)
├─ Implementation: 65% (3-5 weeks)
├─ Review: 10% (1 week)
└─ Total: ~2 months

Complex System (3+ months):
├─ Research: 10% (1-2 weeks)
├─ Planning: 20% (2-3 weeks)
├─ Implementation: 60% (6+ weeks)
├─ Review: 10% (1-2 weeks)
└─ Total: ~3+ months


PLANNING BY PROJECT COMPLEXITY:

Simple Project (clear, well-understood):
├─ Plan high level only
├─ Use static decomposition
├─ Minimal risk analysis
├─ Plan for 1-2 days implementation
└─ Focus on execution

Medium Complexity (some unknowns):
├─ Plan with detail
├─ Use hybrid decomposition
├─ Identify key risks
├─ Research phase important
├─ Flexible approach

High Complexity (many unknowns):
├─ Plan thoroughly
├─ Use dynamic decomposition
├─ Extensive risk analysis
├─ Spike/prototype needed
├─ Iterative refinement

Unknown Territory (brand new):
├─ Start with spike
├─ Plan spike itself
├─ Learn from spike
├─ Plan full project based on learning
├─ Budget extra time


PLANNING BY TEAM SIZE:

Solo Developer:
├─ Document for yourself
├─ Focus on clear task breakdown
├─ Planning mostly for clarity
├─ 1-2 hour planning meetings
└─ Review own work

Small Team (2-5):
├─ Plan for coordination
├─ Document decisions
├─ Plan dependencies carefully
├─ Plan reviews with team
├─ 1-2 days planning
└─ Daily sync-ups

Large Team (5+):
├─ Extensive documentation
├─ Clear work allocation
├─ Careful dependency management
├─ Regular planning checkpoints
├─ 1-2 weeks planning
└─ Daily standups

Distributed Team:
├─ Over-document everything
├─ Async communication plan
├─ Clear ownership
├─ Written decisions
├─ Regular sync meetings
└─ More planning upfront


PLANNING BY DEADLINE TYPE:

Flexible Timeline:
├─ Plan for quality
├─ Can iterate and refine
├─ Can handle surprises
├─ More thorough testing
└─ Longer planning acceptable

Fixed Deadline:
├─ Plan conservatively
├─ Contingency planning critical
├─ Risk identification important
├─ Critical path focus
├─ Scope flexibility needed

Aggressive Deadline:
├─ Minimal viable feature only
├─ High-risk items first
├─ Heavy risk planning
├─ Prototype approach
├─ Plan for cutting corners safely


PLANNING BY DOMAIN:

Building a Features (most projects):
├─ Standard research-plan-implement
├─ Moderate planning time
├─ Typical risk profile
└─ Known patterns

Building APIs/Services:
├─ Extra planning for interfaces
├─ Contract-driven design
├─ Performance planning
├─ Error handling emphasis
└─ Integration testing critical

Building Infrastructure:
├─ Extensive planning required
├─ Reliability emphasis
├─ Security emphasis
├─ Testing at scale
└─ Runbook documentation

Migrations:
├─ Extensive planning
├─ Risk analysis critical
├─ Rollback planning essential
├─ Validation crucial
└─ Phase-by-phase approach

Optimizations:
├─ Measurement first
├─ Iterative approach
├─ Validate improvements
├─ Don't guess, measure
└─ Baseline before changes


PLAN TEMPLATE SELECTION:

Choose appropriate level of planning:

☐ Quick 1-2 day project
  └─ Simple outline, task list, few risks

☐ Standard 1-2 week project
  └─ Requirements, architecture, full task breakdown

☐ Complex 1-2 month project
  └─ Requirements, architecture, risk analysis, timeline

☐ Enterprise system (3+ months)
  └─ All documents, extensive planning, milestones
```

**Speaker Notes:**
Different projects need different amounts of planning. The key is to match planning effort to project complexity and risk.

Don't over-plan small projects, and don't under-plan complex ones.

---

### Slide 39: Measuring Planning Effectiveness
**Title:** How to Know If Your Planning Is Working

**Content:**

```
METRICS FOR GOOD PLANNING:

Estimation Accuracy:
├─ Metric: Actual time vs estimated time
├─ Target: Within 20% variance
├─ Good: 5 day estimate, took 5-6 days
├─ Bad: 5 day estimate, took 10 days
├─ Track over time to improve

Schedule Adherence:
├─ Metric: Stay on timeline or better
├─ Target: >80% of projects on time
├─ Good: Delivered when promised
├─ Bad: Consistently over timeline
├─ Indicates estimation and planning quality

Quality Metrics:
├─ Metric: Bugs found in production
├─ Target: <2 bugs per 1000 lines of code
├─ Good: Planning caught issues before code
├─ Bad: Many bugs slip through
├─ Shows if planning was thorough

Test Coverage:
├─ Metric: % of code covered by tests
├─ Target: >80%
├─ Good: Comprehensive test plan led to coverage
├─ Bad: Tests incomplete or missing
├─ Shows if test planning was adequate

Rework Rate:
├─ Metric: % of completed work that needs rework
├─ Target: <10%
├─ Good: Few surprises during implementation
├─ Bad: Constant rework and changes
├─ Shows if planning was thorough

Team Satisfaction:
├─ Metric: Do team members feel confident?
├─ Target: Team feels prepared to execute
├─ Good: Team knows what to do
├─ Bad: Team confused about direction
├─ Shows if plan was clear

Code Review Turnaround:
├─ Metric: Time from submission to approval
├─ Target: 1-2 days
├─ Good: Code matches plan, quick approval
├─ Bad: Many revisions, slow approval
├─ Shows if implementation matched plan


RETROSPECTIVE QUESTIONS:

After each project, ask:

Planning Quality:
├─ Was the plan clear and useful?
├─ Did the plan guide the work effectively?
├─ Were there surprises not identified in planning?
├─ Would more/less planning have helped?
├─ What could we plan better next time?

Estimation:
├─ Were estimates accurate?
├─ What was underestimated?
├─ What was overestimated?
├─ What factors affect our estimates?
├─ How can we estimate better?

Execution:
├─ Did implementation match the plan?
├─ Where did things diverge?
├─ Why did they diverge?
├─ Was the divergence good or bad?
├─ What did we learn?

Risks:
├─ Were identified risks the actual issues?
├─ What risks did we miss?
├─ Did mitigations help?
├─ How can we identify risks better?
├─ What contingencies worked?

Results:
├─ Did we achieve the goals?
├─ Was quality acceptable?
├─ Was performance acceptable?
├─ Are users satisfied?
├─ What would we improve?


CONTINUOUS IMPROVEMENT:

Project 1: Baseline
├─ Record planning metrics
├─ Document what went well
├─ Document what didn't
└─ Identify improvements

Project 2: Apply Learnings
├─ Implement improvements
├─ Measure effectiveness
├─ New insights
└─ Iterate

Project 3+: Continuous Improvement
├─ Metrics improve over time
├─ Team gets better at estimating
├─ Plans become more accurate
├─ Surprises decrease
└─ Quality increases


PLANNING DASHBOARD:

Track over time:
┌─ Estimation Accuracy
│  ├─ Range: -40% to +60%
│  ├─ Target: ±20%
│  └─ Trend: Improving over time
├─ Schedule Adherence
│  ├─ On time: 60% → 80% → 90%
│  └─ Trend: Improving
├─ Quality Metrics
│  ├─ Bugs per 1K LOC: 5 → 3 → 1
│  └─ Trend: Improving
├─ Test Coverage
│  ├─ Coverage: 70% → 80% → 85%
│  └─ Trend: Improving
└─ Team Satisfaction
   ├─ Confidence: Low → Medium → High
   └─ Trend: Improving

When metrics improve, keep doing what you're doing.
When metrics get worse, diagnose and adjust.
```

**Speaker Notes:**
The only way to know if your planning is working is to measure it. Track metrics over time and use that data to improve your planning.

This closes the loop: plan → execute → measure → improve → plan better.

---

### Slide 40: Conclusion and Key Takeaways
**Title:** Planning → Building: Summary and Next Steps

**Content:**

```
THE COMPLETE WORKFLOW:

┌─────────────────────────────────────────────┐
│ RESEARCH: Understand the problem            │
│ └─ Explore codebase, find patterns,         │
│    understand constraints                   │
├─────────────────────────────────────────────┤
│ PLAN: Design the solution                   │
│ └─ Create architecture, break into tasks,   │
│    identify risks, get approval             │
├─────────────────────────────────────────────┤
│ IMPLEMENT: Build according to plan          │
│ └─ Code each task, write tests, integrate   │
├─────────────────────────────────────────────┤
│ REVIEW: Validate the solution               │
│ └─ Test thoroughly, code review, measure    │
├─────────────────────────────────────────────┤
│ REFLECT: Learn from the process             │
│ └─ Compare to plan, measure improvements,   │
│    adjust future planning                   │
└─────────────────────────────────────────────┘


KEY PRINCIPLES:

1. PLANNING MATTERS
   └─ 20% planning saves 30% total time

2. RESEARCH FIRST
   └─ Understanding prevents mistakes

3. BREAK DOWN WORK
   └─ Small tasks are testable and manageable

4. TEST COMPREHENSIVELY
   └─ Tests validate the plan

5. USE AGENTS EFFECTIVELY
   └─ Give agents clear plans, get better code

6. MEASURE AND ITERATE
   └─ Track metrics, improve over time

7. TEAM ALIGNMENT
   └─ Everyone understands the same goal

8. BE FLEXIBLE
   └─ Plan guides, doesn't constrain


WITH AGENTIC TOOLS:

Planning becomes more important because:
├─ Agents execute plans quickly
├─ Small planning errors become big code errors
├─ Agent-generated code needs careful review
├─ Good specifications produce better code
└─ Agents can help with planning

Planning saves time because:
├─ Agents code 3-5x faster than humans
├─ Good plans have 5-10x fewer bugs
├─ Less rework and refinement needed
├─ Team stays aligned
└─ Delivery is faster and higher quality


TOOLS TO USE:

Research Phase:
└─ Codex (read-only exploration)

Planning Phase:
├─ Claude Code (comprehensive planning)
├─ Aider Architect (architecture design)
└─ Cursor (quick planning)

Implementation Phase:
├─ Claude Code (detailed implementation)
├─ Cursor (incremental changes)
├─ Aider (implementation and commits)
└─ GitHub Copilot (code suggestions)

Review Phase:
└─ All tools (validation and testing)


YOUR ACTION ITEMS:

For your next project:

1. Allocate planning time (10-20% of total)
   └─ Don't skip planning under time pressure

2. Do proper research
   └─ Use agent tools to explore codebase

3. Create written plan
   └─ Architecture, task breakdown, risks

4. Get team alignment
   └─ Everyone understands the plan

5. Decompose into 3-8 hour tasks
   └─ Small enough to test incrementally

6. Identify and mitigate risks
   └─ Plan for failures and contingencies

7. Plan tests from the start
   └─ Budget 25-30% of effort for testing

8. Measure and iterate
   └─ Track metrics, improve next time


READING & RESOURCES:

Core Concepts:
├─ "Code Complete" by Steve McConnell
├─ "The Pragmatic Programmer" by Hunt & Thomas
└─ "Project Management for Modern IT" by Barkus

Specific Practices:
├─ "Agile Software Development" by Robert Martin
├─ "Continuous Integration" by Fowler & Foemmel
└─ "Refactoring" by Martin Fowler

Agentic Tools:
├─ Claude documentation
├─ Cursor documentation
├─ Aider documentation
└─ GitHub Copilot documentation


THE BOTTOM LINE:

Good planning is an investment that pays dividends.
- 20% time investment in planning
- 30% savings in total project time
- Better code quality (5-10x fewer bugs)
- Happier team (clear direction)
- Faster delivery (less rework)

With agentic tools, the ROI is even higher because:
- Agents execute plans quickly (3-5x faster)
- Good plans produce good code (agent can't improvise)
- Small planning mistakes become big problems (must prevent)

Therefore: **Always plan before building.**


FINAL THOUGHT:

The most important skill in software development
is not coding—it's planning.

Coding is what we implement.
Planning is what determines if the implementation is right.

With agentic tools, planning skill becomes
even more valuable because the cost of
bad plans executed quickly is very high.

Invest in planning.
It's the best investment you can make.


NEXT STEPS:

In the next section, we'll cover:
├─ Advanced agentic workflows
├─ Multi-agent coordination
├─ Scaling agentic approaches
├─ Production considerations
└─ Real-world case studies

See you there!
```

**Speaker Notes:**
This concludes Part 3. You now have a comprehensive understanding of planning for agentic coding.

Key takeaway: **Planning matters, especially with agents.**

The research-plan-implement-review cycle is fundamental. Using it with agentic tools amplifies both the benefits (fast execution of good plans) and risks (fast execution of bad plans).

Invest in planning. It's the best investment you can make in software development.

---

## END OF PART 3: PLANNING → BUILDING WORKFLOW

**Total Slides: 40**
**Total Content: ~15,000 words**

**Sections Covered:**
1. Why Planning Matters (Slides 1-6)
2. The Research-Plan-Implement Pattern (Slides 7-16)
3. Plan Mode in Different Tools (Slides 17-26)
4. Plan-Act-Reflect Framework (Slides 17-26)
5. Static vs Dynamic Decomposition (Slides 25-26)
6. Practical Planning Examples (Slides 27-36)
7. Planning Tools and Best Practices (Slides 37-40)

**Key Learning Outcomes:**
- Understand why planning matters for software development
- Learn the research-plan-implement-review cycle
- Know how different tools support planning
- Understand static vs dynamic decomposition
- Can plan real projects from features to migrations
- Can work effectively with agentic tools during planning
- Know how to measure and improve planning effectiveness

This comprehensive slideshow provides detailed guidance for teaching students about planning-driven development with agentic coding tools.

