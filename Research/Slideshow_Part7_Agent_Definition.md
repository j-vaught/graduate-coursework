# Part 7: Agent Definition & Concepts
## A Comprehensive Guide to Agentic Coding Tools

---

## SECTION 1: What IS an Agent?

---

### Slide 1: Part 7 Title Slide

**Title:** Part 7: Agent Definition & Concepts

**Subtitle:** Understanding the Foundation of Agentic Coding Tools

**Content:**
```
┌─────────────────────────────────────────────┐
│                                             │
│      AGENT DEFINITION & CONCEPTS            │
│                                             │
│    Part 7 of Agentic Coding Tools Series    │
│                                             │
│  • What is an Agent?                        │
│  • Core Components                          │
│  • The ReAct Loop                           │
│  • Agent Specialization                     │
│  • Context Windows                          │
│  • Autonomy Levels                          │
│                                             │
└─────────────────────────────────────────────┘
```

**Speaker Notes:**
This part establishes the foundational concepts needed to understand agentic systems. By the end of this part, students will understand what distinguishes an agent from a traditional AI assistant, how agents work internally, and how to design agents for specific tasks. This knowledge is essential before diving into practical implementation in later parts.

---

### Slide 2: Formal Definition of an Agent

**Title:** Formal Definition: What is an Agent?

**Content:**
```
An agent is an autonomous software system that:

1. PERCEIVES its environment through sensors/tools
2. REASONS about the current state and goals
3. TAKES ACTIONS to influence the environment
4. OBSERVES the results of those actions
5. ADAPTS behavior based on feedback

Mathematical Definition:
┌────────────────────────────────────┐
│ Agent = ⟨P, S, A, δ, γ, G⟩         │
│                                    │
│ P = Perception (observations)      │
│ S = State space                    │
│ A = Action space                   │
│ δ = State transition function      │
│ γ = Goal evaluation function       │
│ G = Goal specification             │
└────────────────────────────────────┘
```

**Speaker Notes:**
This formal definition comes from classical AI theory (dating back to Russell & Norvig's work on Rational Agents). The key insight is that an agent is not just reactive—it perceives, reasons about what it perceives, takes actions based on reasoning, and then observes outcomes. In modern agentic coding tools, the "environment" is typically code, files, and APIs. The agent uses language models as its reasoning engine and tool calls as its action mechanism.

---

### Slide 3: Agent vs Traditional AI Assistant

**Title:** Agent vs Traditional AI Assistant

**Content:**
```
TRADITIONAL AI ASSISTANT          vs      AGENT

Input: User prompt              Input: User goal
  |                                |
  v                                v
┌──────────────────┐          ┌──────────────────┐
│  Process input   │          │  Assess state    │
│  Generate text   │          │  Plan actions    │
└──────────────────┘          └──────────────────┘
  |                                |
  v                                v
Output: Single response         ┌─────────────────┐
        (Done)                  │ Execute action  │
                                └─────────────────┘
                                  |
                                  v
                                ┌─────────────────┐
                                │ Observe result  │
                                └─────────────────┘
                                  |
                                  v
                                Goal met?
                                  |
                    ┌─────────────┴─────────────┐
                    v                           v
                  Yes: Done                  No: Loop
```

**Speaker Notes:**
The fundamental difference is autonomy and iteration. A traditional AI assistant is stateless—it responds to a prompt and stops. An agent is stateful and goal-directed—it operates in a loop, taking actions, observing results, and adjusting its approach based on feedback. This is why agents can tackle complex, multi-step problems that would require multiple back-and-forth interactions with a traditional assistant.

Real-world example: Asking ChatGPT to "write a Python function" returns code in one shot. Asking an agent to "debug this codebase and fix all errors" results in the agent exploring files, identifying issues, making fixes, running tests, and iterating until tests pass.

---

### Slide 4: Key Characteristic #1 - Autonomy

**Title:** Key Characteristic #1: Autonomy

**Content:**
```
AUTONOMY: The ability to make decisions and take
          actions without constant user direction

Autonomy Spectrum:
┌────────────────────────────────────────────────┐
│                                                │
│ Manual      Semi-Autonomous    Fully Autonomous│
│ (Chatbot)   (Agent)            (Rare)          │
│                                                │
│ • User     • Agent decides     • No user       │
│   provides   what to do next     input needed  │
│   each     • User confirms    • System runs    │
│   step       major actions      to completion │
│            • Limited scope                     │
│                                                │
└────────────────────────────────────────────────┘

Most practical agents operate in the
"Semi-Autonomous" zone
```

**Speaker Notes:**
True autonomy is rare in practice. Most production agents operate at semi-autonomy where they can execute a series of steps but are bounded by explicit constraints and user confirmation checkpoints. This is a design choice—it balances efficiency with safety and predictability. Students should understand that autonomy is always relative to a specific task scope. An agent might be fully autonomous within a narrow domain (e.g., "run the test suite") but require human oversight for broader tasks (e.g., "refactor the entire codebase").

---

### Slide 5: Key Characteristic #2 - Goal-Directed Behavior

**Title:** Key Characteristic #2: Goal-Directed Behavior

**Content:**
```
GOAL-DIRECTED: Agent behavior is determined by
               explicit objectives, not instructions

Non-Goal-Directed:              Goal-Directed:
"Sort this array using          "Minimize the test
the quicksort algorithm"         runtime to under 100ms"
  |                                |
  v                                v
Follow explicit steps         ┌─────────────────┐
(deterministic)               │ Analyze current │
                              │ test runtime    │
                              └─────────────────┘
                                   |
                              ┌────v─────────────┐
                              │ Identify bottleneck│
                              └─────────────────┘
                                   |
                              ┌────v─────────────┐
                              │ Try optimization │
                              └─────────────────┘
                                   |
                              ┌────v─────────────┐
                              │ Measure result   │
                              └─────────────────┘
                                   |
                        ┌──────────┴──────────┐
                        v                     v
                    Goal met?             No: try
                                          different
                                          approach
```

**Speaker Notes:**
This is what allows agents to be flexible and adaptive. When you tell an agent to "minimize response time," it can reason about multiple strategies: optimizing queries, caching results, parallelizing operations, etc. The agent chooses its approach based on what works, not what was explicitly programmed. This is fundamentally different from traditional algorithms where each step is predetermined.

---

### Slide 6: Key Characteristic #3 - Tool Use and Action

**Title:** Key Characteristic #3: Tool Use and Action

**Content:**
```
TOOL USE: Agents act on environments through
          well-defined tools/capabilities

Agent's Toolkit for Code Tasks:
┌─────────────────────────────────────────────┐
│                                             │
│ ┌──────────────┐    ┌──────────────┐      │
│ │ Read Files   │    │ Write Files   │      │
│ └──────────────┘    └──────────────┘      │
│                                             │
│ ┌──────────────┐    ┌──────────────┐      │
│ │ Run Tests    │    │ Execute Code │      │
│ └──────────────┘    └──────────────┘      │
│                                             │
│ ┌──────────────┐    ┌──────────────┐      │
│ │ Search Code  │    │ Git Ops      │      │
│ └──────────────┘    └──────────────┘      │
│                                             │
│ ┌──────────────┐    ┌──────────────┐      │
│ │ Run Linter   │    │ Deploy Code  │      │
│ └──────────────┘    └──────────────┘      │
│                                             │
└─────────────────────────────────────────────┘

Without tools: Agent can only think
With tools: Agent can think AND do
```

**Speaker Notes:**
Tools are the mechanism through which agents exert influence. They're the boundary between the agent's internal reasoning and the external world. Well-designed tools are specific ("run the Python tests in the backend folder" rather than "do something"), reliable (they work as documented), and observable (their results are clear and parseable). Tools define what's possible for an agent, so agent capability is directly limited by its toolkit.

---

### Slide 7: Brief History of Agents in AI

**Title:** History and Evolution of Agents

**Content:**
```
1956: Dartmouth Summer          → Early agent concepts
      Turing Test proposed

1980-2000: Classical AI        → STRIPS planning
           Reactive agents      Logic-based reasoning

2011: IBM Watson               → Task-specific agent
      (Jeopardy champion)

2018-2022: Foundation Models   → GPT-2, GPT-3
           emerge              First language model
                               agent experiments

2023: Agent Framework Boom     → AutoGPT, BabyAGI
      LLM Agent Papers surge   ReAct architecture
      Tool calling APIs        Claude with tool use

2024-2026: Production Agents   → Mature frameworks
           Specialized agents  -> Agentic coding tools
           Multi-agent systems → Enterprise adoption

Current: Agents are shifting from research projects
         to production infrastructure
```

**Speaker Notes:**
The key inflection point was when large language models became good enough at reasoning and instruction-following. Before LLMs, building agents required extensive programming of decision logic. Now, the reasoning is learned by the model, and we focus on providing the right tools and context. This is why agentic coding tools have become feasible only recently.

---

### Slide 8: Why Agents Matter for Coding

**Title:** Why Agents Matter for Software Development

**Content:**
```
Traditional Development Flow:
┌──────────────┐
│ Write code   │  ← Human-intensive
│ Run tests    │     One decision at a time
│ Fix errors   │
│ Repeat       │
└──────────────┘

Agentic Development Flow:
┌──────────────────────────────────────┐
│ Agent: Implement feature              │
│   ├─ Write code                      │
│   ├─ Run tests                       │
│   ├─ Fix failures                    │
│   ├─ Optimize performance            │
│   ├─ Add documentation               │
│   └─ Submit for review               │
└──────────────────────────────────────┘

Benefits:
• Parallelizable tasks (agent explores while humans plan)
• Tedious tasks automated (debugging, testing)
• 24/7 availability
• Consistent process execution
• Learns from feedback loops
```

**Speaker Notes:**
Agents are particularly valuable for software development because code is deterministic and testable. Unlike domains with ambiguous feedback, code has clear pass/fail signals from tests. An agent can reliably learn from this feedback. Additionally, many development tasks involve many small decisions that follow patterns—exactly what LLMs are good at learning. This is why we're seeing agents succeed in coding before other domains.

---

### Slide 9: Section 1 Summary

**Title:** Section 1 Summary: What IS an Agent?

**Content:**
```
KEY TAKEAWAYS:

1. Definition: An agent is an autonomous system that
   perceives, reasons, acts, and observes

2. Distinction: Unlike traditional AI, agents operate
   in iterative loops, not one-shot interactions

3. Core Characteristics:
   • AUTONOMY - Makes decisions without constant input
   • GOAL-DIRECTED - Behavior focused on objectives
   • TOOL USE - Acts through well-defined mechanisms

4. Context: Agents became practical with LLMs that
   provide reasoning capability

5. Advantage in Coding: Clear feedback (tests) and
   deterministic environment

NEXT: Understanding the internal components
      that make agents work
```

**Speaker Notes:**
Before moving to the next section, ensure students understand these foundational concepts. If they're confused about autonomy vs traditional assistance, use concrete examples from their own IDE workflows. The distinction between reactive (one-shot) and agentic (looping) is the single most important concept in this part.

---

## SECTION 2: Core Agent Components

---

### Slide 10: Core Components Overview

**Title:** Core Agent Components: The Architecture

**Content:**
```
┌─────────────────────────────────────────────────┐
│                                                 │
│              AGENT ARCHITECTURE                 │
│                                                 │
│  ┌────────────────────────────────────────┐   │
│  │        LLM (The Brain)                 │   │
│  │  • Language understanding              │   │
│  │  • Reasoning                           │   │
│  │  • Decision-making                     │   │
│  └────────────────────────────────────────┘   │
│                   ↑↓                            │
│  ┌────────────────────────────────────────┐   │
│  │    Memory/Context (The Workspace)      │   │
│  │  • Current goal                        │   │
│  │  • Previous actions                    │   │
│  │  • Observations                        │   │
│  └────────────────────────────────────────┘   │
│                   ↑↓                            │
│  ┌────────────────────────────────────────┐   │
│  │     Tools (The Hands)                  │   │
│  │  • File operations                     │   │
│  │  • Code execution                      │   │
│  │  • External APIs                       │   │
│  └────────────────────────────────────────┘   │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Speaker Notes:**
Think of an agent like a person at a desk. The LLM is their brain (thinking and reasoning). Memory/context is their workspace (what they're currently focused on and what they've already learned). Tools are their hands (how they interact with the world). Each component is essential. Remove any one and the agent breaks down. In this section, we'll deep-dive into each.

---

### Slide 11: Component #1 - The LLM (Brain) Part 1

**Title:** Component #1: The LLM - The Brain

**Content:**
```
THE LLM: Core reasoning engine of the agent

┌─────────────────────────────────────────┐
│                                         │
│  Input: [Goal + Context + Tools]       │
│           ↓                             │
│  ┌──────────────────────────────────┐  │
│  │ LLM Processes:                   │  │
│  │ • Analyzes current state         │  │
│  │ • Generates reasoning            │  │
│  │ • Plans next steps               │  │
│  │ • Selects tools to use           │  │
│  │ • Formats output                 │  │
│  └──────────────────────────────────┘  │
│           ↓                             │
│  Output: [Action + Reasoning]          │
│                                         │
└─────────────────────────────────────────┘

LLM Characteristics that Matter for Agents:
• Quality of reasoning (better models = better plans)
• Instruction-following ability
• Tool use capability (structured output)
• Consistency (reliability of decisions)
• Speed vs capability tradeoff
```

**Speaker Notes:**
The LLM is the "intelligence" in the system. Modern agents typically use frontier models (GPT-4, Claude Opus, Gemini Pro) because the quality of reasoning directly determines agent success. A smaller or weaker model might miss optimization opportunities or make poor architectural decisions. However, there's a cost-performance tradeoff: larger models are slower and more expensive. This is why many production systems use a fast model for routine decisions and a powerful model for complex reasoning.

---

### Slide 12: Component #1 - The LLM (Brain) Part 2

**Title:** Component #1: The LLM - Reasoning Capability

**Content:**
```
REASONING QUALITY AFFECTS AGENT SUCCESS

Weak Reasoning:                Strong Reasoning:
┌──────────────────┐         ┌──────────────────┐
│ Task: Fix bug in │         │ Task: Fix bug in │
│ user service     │         │ user service     │
│                  │         │                  │
│ Agent thinks:    │         │ Agent thinks:    │
│ "Run tests"      │         │ "This error      │
│ -> Tests fail    │         │  suggests wrong  │
│ "Run tests again"│         │  SQL. Let me     │
│ -> Tests fail    │         │  examine the     │
│ (repeats 5x)     │         │  query first,    │
│                  │         │  trace the data  │
│ Cost: High       │         │  flow, check     │
│ Time: Long       │         │  tests, then fix"│
│ Success: Maybe   │         │                  │
└──────────────────┘         │ Cost: Low        │
                             │ Time: Short      │
                             │ Success: Likely  │
                             └──────────────────┘

Model Selection Guidance:
┌──────────────────┬──────────────┬──────────────┐
│ Task Type        │ Model        │ Reasoning    │
├──────────────────┼──────────────┼──────────────┤
│ Routine coding   │ Claude Haiku │ Fast, Simple │
│ Complex tasks    │ Claude Opus  │ Deep reason. │
│ Creative work    │ GPT-4        │ Novel ideas  │
│ Cost-sensitive   │ Llama3       │ Adequate     │
└──────────────────┴──────────────┴──────────────┘
```

**Speaker Notes:**
This is why it's not just about "which LLM," but "which LLM for which task." A powerful model will waste money on routine file-reading tasks. A weak model will fail on complex debugging scenarios. The best production systems often use multiple models—routing simple tasks to fast models and reserving powerful models for reasoning-intensive work.

---

### Slide 13: Component #2 - Memory & Context Part 1

**Title:** Component #2: Memory & Context - The Workspace

**Content:**
```
MEMORY/CONTEXT: Everything the agent knows about
                its current task

What Lives in Memory:
┌────────────────────────────────────┐
│ GOAL                               │
│ "Implement pagination for user API"│
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ OBSERVATIONS                       │
│ • Current code structure           │
│ • Previous test results            │
│ • Errors encountered               │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ REASONING HISTORY                  │
│ • Steps already tried              │
│ • Why they failed/succeeded        │
│ • Constraints learned              │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│ PLAN                               │
│ • Next actions to try              │
│ • Fallback strategies              │
└────────────────────────────────────┘

Memory = Context window usage
More memory = More context = Better decisions
But: Context is finite and expensive
```

**Speaker Notes:**
Memory in modern LLM agents is not stored in a database—it's the prompt itself. This is both a strength and a limitation. Strength: the agent can reference any past action. Limitation: context windows are finite, so very long tasks require careful memory management. This is one reason why agents often work in phases: complete one phase, archive results to files, start fresh context with the next phase.

---

### Slide 14: Component #2 - Memory & Context Part 2

**Title:** Component #2: Memory & Context - Managing Tokens

**Content:**
```
CONTEXT WINDOW REALITIES

Typical LLM Context:
Claude Opus 4.5:    200K tokens (~150 pages)
GPT-4 Turbo:        128K tokens (~100 pages)
Claude Haiku:       200K tokens (but smaller cost)
Gemini Pro 1.5:     1M tokens (~750 pages) ⭐

Token Consumption per Task:
┌──────────────────────────┬────────────┐
│ Task Element             │ Tokens     │
├──────────────────────────┼────────────┤
│ System prompt            │ 1-2K       │
│ User goal                │ 100-500    │
│ Current file (100 lines) │ 300-500    │
│ Previous conversation    │ 1-5K       │
│ Tool results/output      │ Varies     │
│ Agent response output    │ 1-5K       │
└──────────────────────────┴────────────┘

Memory Management Strategies:
1. Summarization: "Here's what we learned..."
2. Archival: Save decisions to files
3. Forgetting: Drop old context
4. Compression: Keep key facts only
5. Phasing: Complete logical blocks separately
```

**Speaker Notes:**
This is critical for practical agents. A 200K token context might sound huge (100+ pages), but a realistic task quickly consumes it: 5K for system prompts, 5K for file contents, 10K for previous conversation, 5K for current code examination. Suddenly you're at 25K, and you still need room for new reasoning. This is why experienced agent designers think in terms of "phases" rather than "single long run." Complete phase 1, save to files, load only phase 2 context.

---

### Slide 15: Component #2 - Memory & Context Part 3

**Title:** Component #2: Context Isolation in Multi-Agent Systems

**Content:**
```
CONTEXT ISOLATION: Each agent has separate context

Multi-Agent Setup:
┌─────────────────────────────────────┐
│  COORDINATOR AGENT                  │
│  "Build this feature across services"│
│  Context: Task planning              │
└──────┬────────────────┬─────────────┘
       │                │
       v                v
┌────────────┐    ┌────────────┐
│ CODE AGENT │    │ TEST AGENT │
│ Context:   │    │ Context:   │
│ • Feature  │    │ • Test     │
│ • API spec │    │   framework│
│ • Error    │    │ • Failures │
│   fixes    │    │            │
└────────────┘    └────────────┘

Isolation Benefits:
✓ Focus (each agent focused on its task)
✓ Parallel execution (agents work simultaneously)
✓ Failure isolation (one agent's mistake doesn't
  corrupt another's memory)
✓ Resource efficiency (context waste reduced)

Isolation Challenges:
✗ Communication overhead (agents must share state)
✗ Consistency (keeping distributed state aligned)
✗ Coordination complexity
```

**Speaker Notes:**
This is an advanced pattern but increasingly common. Rather than one massive agent doing everything, decompose into specialists. The coordinator has high-level context, each specialist has focused context. When a specialist discovers something, it reports to coordinator, which may update other specialists' context. This scales much better than single-agent systems for complex projects.

---

### Slide 16: Component #3 - Tools (Actions) Part 1

**Title:** Component #3: Tools - The Hands

**Content:**
```
TOOLS: Specific, well-defined capabilities that
       agents use to interact with the world

Tool Design Principle:
        One clear responsibility per tool

┌──────────────────────────────────────────────┐
│ Well-Designed Tool:                          │
│                                              │
│ Name: read_python_file                       │
│ Input: file_path (string)                    │
│ Output: file contents (string)               │
│ Side effects: None (read-only)               │
│ Documentation: Clear parameters              │
│                                              │
│ ✓ Specific                                   │
│ ✓ Single responsibility                      │
│ ✓ Observable output                          │
│ ✓ Reliable behavior                          │
└──────────────────────────────────────────────┘

vs

┌──────────────────────────────────────────────┐
│ Poorly-Designed Tool:                        │
│                                              │
│ Name: do_stuff                               │
│ Input: command (string)                      │
│ Output: ??? (unpredictable)                  │
│ Side effects: Many (creates files, runs code)│
│                                              │
│ ✗ Too broad                                  │
│ ✗ Unclear output                             │
│ ✗ Unreliable behavior                        │
│ ✗ Difficult for agent to predict result      │
└──────────────────────────────────────────────┘

Agent capability = Quality of tools available
```

**Speaker Notes:**
Tool design is one of the most underestimated aspects of agent systems. Poor tools lead to agent confusion, failures, and hallucinations. A well-designed tool is so clear that an LLM can reliably use it without misunderstanding. This means clear names, explicit parameters, documented behavior, and predictable outputs. When designing tools for agents, think like you're writing an API that needs to be understood by an LLM that has never seen your code before.

---

### Slide 17: Component #3 - Tools Part 2

**Title:** Component #3: Tools - Common Categories

**Content:**
```
TOOL CATEGORIES FOR CODING AGENTS

┌─────────────────────────────────────────────┐
│ PERCEPTION TOOLS (Read Information)         │
│                                             │
│ • read_file / read_directory                │
│ • search_code (grep/regex)                  │
│ • list_functions / analyze_ast              │
│ • get_file_metadata                         │
│                                             │
│ -> Agent learns about the environment       │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ ACTION TOOLS (Do Things)                    │
│                                             │
│ • write_file / edit_code                    │
│ • execute_command / run_tests               │
│ • git_commit / git_push                     │
│ • create_pull_request                       │
│                                             │
│ -> Agent modifies the environment           │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ REASONING TOOLS (Process Information)       │
│                                             │
│ • analyze_code_quality                      │
│ • find_performance_bottleneck               │
│ • detect_security_issues                    │
│ • suggest_refactoring                       │
│                                             │
│ -> Agent synthesizes understanding          │
└─────────────────────────────────────────────┘

Tool Count Sweet Spot:
Too few (3-5):    Agent is paralyzed
Optimal (8-15):   Agent can accomplish tasks
Too many (50+):   Agent gets confused choosing
```

**Speaker Notes:**
The principle of tool design for agents is different from traditional API design. With humans, you want comprehensive APIs. With agents, you want highly specific tools with clear purposes. An agent given 200 tools to choose from gets paralyzed trying to decide which one to use. An agent given 10 well-named tools can quickly identify the right one. This is why successful agent frameworks often focus on small, curated toolsets rather than exposing entire APIs.

---

### Slide 18: Component #3 - Tools Part 3

**Title:** Component #3: Tools - Tool Calling Mechanism

**Content:**
```
HOW AGENTS USE TOOLS: The Tool Calling Protocol

User Request:
"Add type hints to this Python file"
      |
      v
Agent (LLM) Reasoning:
"I need to: 1) read file 2) analyze types
 3) add annotations 4) write back"
      |
      v
LLM decides to call: read_file()
      |
      v
Tool Execution Framework:
┌─────────────────────────────────────┐
│ 1. Extract tool name & parameters   │
│ 2. Validate parameters              │
│ 3. Execute tool (run actual code)   │
│ 4. Capture output                   │
│ 5. Format output back to LLM        │
└─────────────────────────────────────┘
      |
      v
Agent receives: {tool_name, result, timestamp}
      |
      v
Agent reasons about result:
"The file has function without types.
Now I'll analyze it..."
      |
      v
Agent decides next tool: analyze_code()
      |
      v
Loop continues until goal is met

This is called "Tool-Using Loop" or "Tool Calling Chain"
```

**Speaker Notes:**
This protocol is at the heart of how agents function. The LLM doesn't directly execute code—it decides what to execute and in what order. The framework handles the actual execution and reporting. This separation is important because it allows sandboxing (run tools safely), logging (see what agent did), and verification (ensure agent didn't misuse tools). Modern frameworks like Claude Code handle this automatically, but understanding the mechanism helps when debugging agent behavior.

---

### Slide 19: Component #4 - Planning Capability Part 1

**Title:** Component #4: Planning - Forward-Thinking

**Content:**
```
PLANNING CAPABILITY: How agents think ahead

Non-Planning Agent:          Planning Agent:
┌──────────────────┐        ┌──────────────────┐
│ Goal: Refactor   │        │ Goal: Refactor   │
│ codebase         │        │ codebase         │
│                  │        │                  │
│ 1. Read file     │        │ PLAN:             │
│ 2. Write changes │        │ 1. Map structure  │
│ 3. Test          │        │ 2. Identify      │
│ 4. Fails!        │        │    patterns      │
│ 5. Back to 1     │        │ 3. Draft changes  │
│ 6. Loop 5 times  │        │ 4. Write smart   │
│                  │        │ 5. Test          │
│ Cost: High       │        │ 6. Success!      │
│ Time: Long       │        │                  │
│ Iterations: Many │        │ Cost: Lower      │
└──────────────────┘        │ Time: Shorter    │
                            │ Iterations: Few  │
                            └──────────────────┘
```

**Speaker Notes:**
Planning separates good agents from bad ones. A planning agent thinks "if I change X, it will affect Y, so I should also change Y." A non-planning agent stumbles forward, making changes that create more problems. Not all LLMs plan equally well. Better models naturally produce better plans. This is another reason to use capable models for complex tasks—the planning capability difference is dramatic.

---

### Slide 20: Component #4 - Planning Capability Part 2

**Title:** Component #4: Planning - Planning Techniques

**Content:**
```
PLANNING TECHNIQUES AGENTS USE

Technique 1: Hierarchical Planning
┌──────────────────────────────┐
│ High-level goal              │
│ "Make API faster"            │
└────────┬──────────────────────┘
         │
    ┌────┴────┬──────────┬────────┐
    │          │          │        │
    v          v          v        v
 Profile  Identify   Try      Measure
 current  bottleneck approach  results
 perf     code

Technique 2: Contingency Planning
Goal: "Add database migration"
Planning:
  IF database is empty
    THEN create schema
  ELSE
    IF schema matches migration
      THEN warn user
    ELSE
      THEN create safe backup first
          then apply migration

Technique 3: Dependency Planning
┌─────────────────────────────────────┐
│ Change Backend API                  │
│   ├─ Update OpenAPI spec            │
│   ├─ Update tests                   │
│   └─ Update client library (depends │
│       on ├ tests passing)           │
│       └─ spec being updated        │
└─────────────────────────────────────┘

Good planning prevents wasted work
```

**Speaker Notes:**
Planning is learned behavior from the LLM's training. You can't force an agent to plan better—you can only help by asking for it explicitly. Prompts like "Before making changes, think about the dependencies" nudge agents toward planning. But the quality still depends on the model's reasoning ability and the task complexity.

---

### Slide 21: Section 2 Summary

**Title:** Section 2 Summary: Core Agent Components

**Content:**
```
KEY TAKEAWAYS:

1. LLM (Brain):
   • Reasoning engine of the agent
   • Better models = better decisions
   • Tradeoff: capability vs cost/speed

2. Memory/Context:
   • Everything agent knows about current task
   • Limited by context window size
   • Manage via phases, summarization, archival

3. Tools (Hands):
   • Specific, well-defined capabilities
   • Agent quality limited by tool quality
   • 8-15 tools is sweet spot
   • Protocol: LLM decides → Framework executes

4. Planning:
   • Forward-thinking about task structure
   • Prevents wasted iterations
   • Quality depends on LLM reasoning

ARCHITECTURE FORMULA:
Agent Capability = LLM Quality × Tool Design ×
                   Memory Management × Planning

NEXT: How these components work together
      in the ReAct Loop
```

**Speaker Notes:**
Before moving forward, check that students understand each component. A common mistake is thinking more tools are always better. Actually, 50 poorly-organized tools are worse than 10 excellent tools. Similarly, the biggest bang for buck is often improving tool design, not upgrading the LLM.

---

## SECTION 3: The ReAct Loop

---

### Slide 22: The ReAct Loop Overview

**Title:** The ReAct Loop: Core Agent Operating Pattern

**Content:**
```
ReAct = REAsoning + ACTing

The fundamental pattern all modern agents use:

           ┌─────────────────┐
           │    REASON       │
           │  (Think about   │
           │   situation)    │
           └────────┬────────┘
                    │
                    v
           ┌─────────────────┐
           │     ACT         │
           │  (Take action   │
           │   using tool)   │
           └────────┬────────┘
                    │
                    v
           ┌─────────────────┐
           │    OBSERVE      │
           │  (See result of │
           │   action)       │
           └────────┬────────┘
                    │
                    v
             Goal Reached?
                    │
        ┌───────────┴────────────┐
        │                        │
       YES                       NO
        │                        │
        v                        v
      END                   Loop back to
                            REASON step
```

**Speaker Notes:**
ReAct stands for "Reasoning + Acting" and was formalized in a 2023 paper by Yao et al., though the pattern existed informally before. It's deceptively simple but incredibly powerful. The genius is that reasoning and action are interleaved, not sequential. The agent doesn't plan everything upfront (which would fail for complex tasks). Instead, it reasons, acts, observes what happened, and uses that to inform the next reasoning step. This is much more human-like than traditional planning approaches.

---

### Slide 23: Slide 3 - REASON Step Deep Dive

**Title:** REASON Step: Thinking About the Situation

**Content:**
```
REASON STEP: LLM analyzes current state and
             decides next action

Input to REASON:
┌─────────────────────────────────────┐
│ Current goal:                       │
│ "Fix failing tests in auth module"  │
│                                     │
│ What we know so far:                │
│ • Test failures from previous step  │
│ • Code we've examined               │
│ • Changes we've made                │
│                                     │
│ What we still need:                 │
│ • More information? (examine code)  │
│ • To take action? (run tests)       │
│ • To change something? (edit code)  │
└─────────────────────────────────────┘

LLM's Thinking Process:
"I see test X failed with error Y.
The error looks like Z (connection refused).
That suggests the database isn't running.
I should check if database service is started.
If not running, I'll start it.
If running, I'll examine the connection string."

Output of REASON:
┌─────────────────────────────────────┐
│ Decision: What to do next           │
│ Reasoning: Why that's the right step│
│ Expected outcome: What we'll learn  │
└─────────────────────────────────────┘

This is where agents can be brilliant or terrible
depending on LLM quality
```

**Speaker Notes:**
The REASON step is pure thought—no external effects. It's the agent talking to itself. This is why you see good agents show their reasoning: "I see X, which suggests Y, so I'll do Z." Poor agents skip the reasoning: "Run test" -> failure -> "Run test again." The reasoning step is also where multi-step planning happens. A good REASON can result in "I'll run 3 tests in sequence because test A must pass before B, and B must pass before C."

---

### Slide 24: ACT Step Deep Dive

**Title:** ACT Step: Taking Action

**Content:**
```
ACT STEP: Agent executes a tool to change
          or examine the environment

Tool Call Example:
┌──────────────────────────────────────────┐
│ Reasoning decided: "Run the test suite"  │
│                                          │
│ Agent formulates tool call:              │
│ Tool: run_command                        │
│ Parameters:                              │
│   command = "pytest auth/ -v"            │
│   timeout = 30 seconds                   │
│   capture_output = true                  │
│                                          │
│ Framework executes:                      │
│ 1. Verify tool exists                    │
│ 2. Validate parameters                   │
│ 3. Execute the tool                      │
│ 4. Capture stdout/stderr                 │
│ 5. Record execution time                 │
│ 6. Return result to agent                │
└──────────────────────────────────────────┘

Types of Actions:
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ PERCEPTION   │  │   ACTION     │  │  REASONING   │
│              │  │              │  │              │
│ • Read file  │  │ • Write file │  │ • Analyze    │
│ • List items │  │ • Run code   │  │ • Compare    │
│ • Search     │  │ • Deploy     │  │ • Evaluate   │
│ • Query      │  │ • Commit     │  │              │
└──────────────┘  └──────────────┘  └──────────────┘

Action is the only step that changes the world
(everything else is thinking)
```

**Speaker Notes:**
This is where the agent actually does something. The action must be observable, repeatable, and have clear outcomes. A well-designed action is so specific that you can predict exactly what will happen. For instance, "read file X" is clear (you know which file and what you'll get). "Do some debugging" is not clear (unclear what tool will be invoked, what might happen). Bad tools lead to actions that surprise the agent, which breaks the ReAct loop.

---

### Slide 25: OBSERVE Step Deep Dive

**Title:** OBSERVE Step: Perceiving Results

**Content:**
```
OBSERVE STEP: Agent examines the outcome of
              the action just taken

Action Taken:
"Run pytest on auth module"
       |
       v
System Output:
┌────────────────────────────────────────┐
│ $ pytest auth/ -v                      │
│                                        │
│ test_login_valid_user ... PASS         │
│ test_login_invalid_user ... PASS       │
│ test_session_timeout ... FAIL          │
│   AssertionError: Session not expired  │
│                                        │
│ 2 passed, 1 failed in 2.34s            │
└────────────────────────────────────────┘

Agent's Observation:
"2 passed, 1 failed. The failure is in
test_session_timeout and the message is
'Session not expired'. This suggests the
timeout logic isn't working."

OBSERVE converts raw output into understanding

Good Observation includes:
✓ What succeeded (2 tests passed)
✓ What failed (1 test failed)
✓ Why it failed (timeout not working)
✓ What to do next (debug timeout logic)

Poor Observation:
✗ Just reports: "Tests ran"
✗ Misses details
✗ Doesn't extract next step
```

**Speaker Notes:**
The OBSERVE step is critical but often overlooked. It's not just about receiving output—it's about interpreting it correctly. A weak agent might see "1 failed" and just try running tests again. A strong agent sees "1 failed" and analyzes why, which informs the next REASON step. This is where LLM reasoning quality again matters—some models extract insights from messy output, others just repeat the output back.

---

### Slide 26: ReAct Loop Mechanics Part 1

**Title:** ReAct Loop Mechanics: Putting It Together

**Content:**
```
COMPLETE ReAct CYCLE: An Example

User Goal: "Add error handling to the API endpoint"

┌─── CYCLE 1 ────────────────────────────────────┐
│ REASON: "I need to understand current code"    │
│ ACT: read_file("api.py")                       │
│ OBSERVE: File has endpoint without try/except  │
│ Next: Need to find error cases                 │
└────────────────────────────────────────────────┘
         |
         v
┌─── CYCLE 2 ────────────────────────────────────┐
│ REASON: "Need to see existing error handlers"  │
│ ACT: search_code("except", "api/")             │
│ OBSERVE: Found 3 error handlers, similar style │
│ Next: Use same pattern for our endpoint        │
└────────────────────────────────────────────────┘
         |
         v
┌─── CYCLE 3 ────────────────────────────────────┐
│ REASON: "Now add error handling following      │
│         the established pattern"               │
│ ACT: edit_code(                                │
│   "api.py",                                    │
│   "wrap function with try/except")             │
│ OBSERVE: Code modified successfully            │
│ Next: Test the changes                         │
└────────────────────────────────────────────────┘
         |
         v
┌─── CYCLE 4 ────────────────────────────────────┐
│ REASON: "Run tests to verify error handling"   │
│ ACT: run_command("pytest api_test.py")         │
│ OBSERVE: All tests pass                        │
│ NEXT: Goal achieved!                           │
└────────────────────────────────────────────────┘
```

**Speaker Notes:**
Notice how each cycle informs the next. The agent learns something in OBSERVE that shapes what it REASONS about next. This is fundamentally different from waterfall planning. The agent doesn't need to understand the entire task upfront—it discovers what's needed as it goes. This flexibility is why ReAct is so powerful for complex, ambiguous tasks.

---

### Slide 27: ReAct Loop Mechanics Part 2

**Title:** ReAct Loop Mechanics: Why It Works

**Content:**
```
WHY ReAct IS SUPERIOR TO TRADITIONAL APPROACHES

Traditional Waterfall Planning:
┌──────────────────────────────────────────┐
│ 1. Understand all requirements           │
│ 2. Create complete plan                  │
│ 3. Execute plan steps                    │
│ 4. If step N fails → back to step 1      │
│                                          │
│ Problem: Can't predict all requirements  │
│ Result: Many failed attempts, long loops │
└──────────────────────────────────────────┘

Reactive (No Loop):
┌──────────────────────────────────────────┐
│ 1. Take next action (no planning)        │
│ 2. See result                            │
│ 3. Repeat                                │
│                                          │
│ Problem: No forward-thinking             │
│ Result: Inefficient, lots of backtracking│
└──────────────────────────────────────────┘

ReAct (Interleaved):
┌──────────────────────────────────────────┐
│ 1. Think about situation (REASON)        │
│ 2. Take one action (ACT)                 │
│ 3. Observe result (OBSERVE)              │
│ 4. Use result to inform next thought     │
│ 5. Loop                                  │
│                                          │
│ Advantage: Adaptive + thoughtful         │
│ Result: Efficient iteration              │
└──────────────────────────────────────────┘

Mathematical advantage of ReAct:
• Waterfall: O(n^2) failures (bad plan wastes many steps)
• Reactive: O(n) but with wrong steps
• ReAct: O(log n) thoughtful iteration
```

**Speaker Notes:**
This is why ReAct has become the dominant pattern. It's not about being smart at planning (that's still hard), it's about being responsive to feedback. By making one change, observing the result, and using that observation to inform the next decision, agents avoid the cascading failures of pure planning.

---

### Slide 28: ReAct vs ReWOO Patterns

**Title:** ReAct vs ReWOO: Alternative Patterns

**Content:**
```
ReWOO = REasoning WithOut Observation

ReAct Pattern:
REASON → ACT → OBSERVE → REASON → ACT → OBSERVE...
  (interleaved, responsive)

ReWOO Pattern:
┌──────────────────────────────────────┐
│ REASON Phase:                        │
│ Plan entire sequence of actions      │
│ without executing them               │
└───────────┬──────────────────────────┘
            v
┌──────────────────────────────────────┐
│ EXECUTION Phase:                     │
│ Run all actions sequentially          │
└───────────┬──────────────────────────┘
            v
┌──────────────────────────────────────┐
│ VERIFICATION Phase:                  │
│ Check if all worked                  │
└──────────────────────────────────────┘

When to Use Each:

ReAct (Interleaved):
✓ Uncertain tasks (don't know all steps)
✓ Debugging (need feedback to continue)
✓ Exploration (learning as you go)
✓ Most practical agents

ReWOO (Plan First):
✓ Well-defined tasks (steps are known)
✓ Repetitive tasks (same pattern each time)
✓ Cooperative agents (explicit handoff)
✓ Best when you can fully plan upfront

Example:
Task: "Fix the specific bug in auth.py"
      (well-defined) → Use ReWOO

Task: "Make this system 50% faster"
      (fuzzy) → Use ReAct
```

**Speaker Notes:**
ReWOO emerged as a response to concerns about ReAct's efficiency—why make decisions one step at a time when you could plan it all first? But ReWOO only works when the task is well-defined. For exploratory tasks or debugging, ReAct dominates because the agent needs feedback to decide the next step. Most production agents use ReAct because most real tasks aren't fully predictable upfront.

---

### Slide 29: Section 3 Summary

**Title:** Section 3 Summary: The ReAct Loop

**Content:**
```
KEY TAKEAWAYS:

1. ReAct Cycle: REASON → ACT → OBSERVE
   (repeat until goal achieved)

2. REASON: LLM thinks about situation
   decides what to do next

3. ACT: Agent executes a tool
   only step that changes the world

4. OBSERVE: Agent interprets results
   extracts insights for next reasoning

5. Why It Works:
   • Interleaved feedback prevents mistakes
   • One decision at a time reduces complexity
   • Responsive to environment changes
   • Doesn't require upfront complete planning

6. Alternatives:
   • ReWOO: Plan everything first (works for
     well-defined tasks)
   • Pure reactive: No thinking (inefficient)

7. ReAct is the dominant pattern because:
   Most real tasks need adaptive thinking

NEXT: How to build specialized agents
      for different coding tasks
```

**Speaker Notes:**
At this point, students should understand the operational mechanism. ReAct is the heartbeat of modern agents. Everything else (tool design, context management, etc.) is scaffolding around this core loop. When agents fail, it's often because one of these steps is broken: bad reasoning, broken tools, or misinterpretation of results.

---

## SECTION 4: Agent Specialization

---

### Slide 30: Agent Specialization Overview

**Title:** Agent Specialization: Generalists vs Specialists

**Content:**
```
AGENT SPECIALIZATION: Different agents for
                      different tasks

Generalist Agent:
┌─────────────────────────────────────┐
│ "Do whatever task is needed"        │
│                                     │
│ Can handle:                         │
│ • Coding                            │
│ • Testing                           │
│ • Deployment                        │
│ • Documentation                     │
│                                     │
│ Problems:                           │
│ • Slower (tries many approaches)    │
│ • Less accurate (generalist trades) │
│ • Context bloat (knows about all)   │
│ • Hard to debug                     │
└─────────────────────────────────────┘

Specialist Agent:
┌─────────────────────────────────────┐
│ "Write Python tests for this code"  │
│                                     │
│ Specialized for:                    │
│ • One language/framework            │
│ • One type of task                  │
│ • Known constraints                 │
│                                     │
│ Advantages:                         │
│ • Fast (fewer options to consider)  │
│ • Accurate (deep expertise)         │
│ • Lean context (only needed info)   │
│ • Easy to debug                     │
└─────────────────────────────────────┘

Modern best practice:
Use multiple specialists + coordinator
instead of one generalist
```

**Speaker Notes:**
This is a key architectural decision. Early agent systems tried to build generalists that could do anything. Production systems have discovered that specialists outperform. A test-writing specialist will outperform a general agent at writing tests because it has test-specific tools and context. The downside is coordination complexity, but that's worth the performance gains.

---

### Slide 31: Common Specialist Agent Types Part 1

**Title:** Common Specialist Types: Explorer & Coder

**Content:**
```
SPECIALIST TYPE #1: EXPLORER AGENT
Responsibility: Understand the codebase

┌────────────────────────────────────┐
│ Tools:                             │
│ • search_code (find patterns)      │
│ • analyze_structure (AST analysis) │
│ • read_file                        │
│ • list_directory                   │
│                                    │
│ Does NOT have:                     │
│ • write tools (read-only)          │
│ • execution tools                  │
│ • deployment tools                 │
│                                    │
│ Typical tasks:                     │
│ • "Map the architecture"           │
│ • "Find all database calls"        │
│ • "Identify circular dependencies" │
│ • "List all error handlers"        │
└────────────────────────────────────┘

SPECIALIST TYPE #2: CODER AGENT
Responsibility: Write and modify code

┌────────────────────────────────────┐
│ Tools:                             │
│ • read_file (understand code)      │
│ • write_file / edit_code (modify)  │
│ • search_code (find related code)  │
│ • run_command (test locally)       │
│                                    │
│ Does NOT have:                     │
│ • deployment tools                 │
│ • git push (changes stay local)    │
│ • database tools                   │
│                                    │
│ Typical tasks:                     │
│ • "Implement this feature"         │
│ • "Refactor this module"           │
│ • "Add type hints"                 │
│ • "Optimize this function"         │
└────────────────────────────────────┘
```

**Speaker Notes:**
Notice the separation of concerns. The Explorer gathers information, the Coder uses that information to make changes. Neither does everything. This prevents bugs (Coder can't accidentally push untested changes) and allows parallelization (Explorer and Coder can work simultaneously if Coder is working on different code).

---

### Slide 32: Common Specialist Agent Types Part 2

**Title:** Common Specialist Types: Reviewer & Tester

**Content:**
```
SPECIALIST TYPE #3: REVIEWER AGENT
Responsibility: Quality assurance

┌────────────────────────────────────┐
│ Tools:                             │
│ • read_code (understand changes)   │
│ • search_code (find patterns)      │
│ • analyze_performance              │
│ • check_best_practices             │
│ • lint                             │
│                                    │
│ Does NOT have:                     │
│ • write tools (read-only)          │
│ • execution tools                  │
│ • deployment tools                 │
│                                    │
│ Typical tasks:                     │
│ • "Review this code for quality"   │
│ • "Check for security issues"      │
│ • "Verify style compliance"        │
│ • "Find performance problems"      │
└────────────────────────────────────┘

SPECIALIST TYPE #4: TESTER AGENT
Responsibility: Verification and validation

┌────────────────────────────────────┐
│ Tools:                             │
│ • read_test_files                  │
│ • run_tests                        │
│ • run_command (arbitrary code)     │
│ • analyze_coverage                 │
│ • check_test_health                │
│                                    │
│ Does NOT have:                     │
│ • write code (only tests)          │
│ • deployment tools                 │
│ • git operations                   │
│                                    │
│ Typical tasks:                     │
│ • "Run the test suite"             │
│ • "Write tests for this function"  │
│ • "Find untested code paths"       │
│ • "Check if tests pass locally"    │
└────────────────────────────────────┘
```

**Speaker Notes:**
Specialists are arranged in a pipeline. Explorer → Coder → Tester → Reviewer → (Coordinator decides: push or loop back to Coder). Each specialist has exactly the tools it needs and no more. This prevents accidents (Reviewer can't modify code, only comment on it) and keeps context small (each agent only knows about its domain).

---

### Slide 33: Common Specialist Agent Types Part 3

**Title:** Common Specialist Types: Security & DevOps

**Content:**
```
SPECIALIST TYPE #5: SECURITY AGENT
Responsibility: Detect and prevent security issues

┌────────────────────────────────────┐
│ Tools:                             │
│ • analyze_security_issues          │
│ • search_code (find vulnerabilities)
│ • check_dependencies               │
│ • scan_secrets                     │
│ • read_docs (security guidelines)  │
│                                    │
│ Does NOT have:                     │
│ • write code                       │
│ • execution tools                  │
│ • deployment tools                 │
│                                    │
│ Typical tasks:                     │
│ • "Scan for SQL injection risks"   │
│ • "Check for exposed secrets"      │
│ • "Review auth implementation"     │
│ • "Audit dependencies"             │
└────────────────────────────────────┘

SPECIALIST TYPE #6: DEVOPS AGENT
Responsibility: Deployment and infrastructure

┌────────────────────────────────────┐
│ Tools:                             │
│ • deploy_service                   │
│ • configure_infrastructure         │
│ • run_health_checks                │
│ • manage_secrets                   │
│ • check_logs                       │
│                                    │
│ Does NOT have:                     │
│ • write application code           │
│ • modify tests                     │
│ • review code (different scope)    │
│                                    │
│ Typical tasks:                     │
│ • "Deploy this service"            │
│ • "Set up CI/CD pipeline"          │
│ • "Configure monitoring"           │
│ • "Rollback failed deployment"     │
└────────────────────────────────────┘

Specialist Benefits:
✓ Each has exactly the right tools
✓ No unnecessary capabilities
✓ Easy to audit (focused responsibility)
✓ Can be updated independently
```

**Speaker Notes:**
Security and DevOps specialists are particularly important. A generalist agent might accidentally push a deployment without full testing. A DevOps specialist won't deploy until explicitly told to. Similarly, a Security specialist can focus entirely on vulnerability patterns rather than also thinking about code optimization.

---

### Slide 34: When to Use Each Specialist

**Title:** Choosing the Right Specialist: Decision Tree

**Content:**
```
WHEN TO USE WHICH SPECIALIST?

Task: "Implement pagination for user API"
      |
      v
Is the codebase already understood?
    NO  → Use EXPLORER
          (map structure, find patterns)
    |
    YES → Use CODER
           (write/modify code)
           |
           v
    Does code need review?
      YES → Use REVIEWER
             (quality checks)
      |
      YES → Use TESTER
             (run tests, verify)
             |
             v
    Is there security concern?
      YES → Use SECURITY
             (vulnerability scan)
      |
      YES → Use DEVOPS
             (deploy if needed)

Visual Specialization Pipeline:
┌─────────┐  ┌─────────┐  ┌────────┐
│EXPLORER │→→│ CODER  │→→│TESTER │
└─────────┘  └─────────┘  └────────┘
                  │
                  └──→ ┌─────────┐
                      │REVIEWER │
                      └────┬────┘
                           │
                  ┌────────┼────────┐
                  v                 v
            ┌──────────┐    ┌──────────┐
            │SECURITY  │    │ DEVOPS   │
            └──────────┘    └──────────┘
```

**Speaker Notes:**
This is a practical decision tree. Not every task uses all specialists. A simple bug fix might be: Coder → Tester → done. A major refactor might be: Explorer → Coder → Reviewer → Tester → Security → done. The coordinator agent orchestrates which specialists to involve based on the task.

---

### Slide 35: Creating Custom Specialists

**Title:** Creating Custom Specialists: Design Principles

**Content:**
```
HOW TO DESIGN A SPECIALIST AGENT:

Step 1: Define Clear Responsibility
┌────────────────────────────────────────┐
│ Specialist does ONE thing really well  │
│ NOT: "Handle all database operations"  │
│ YES: "Write SQL queries for this       │
│      specific schema"                  │
└────────────────────────────────────────┘

Step 2: Specify Exact Tools
┌────────────────────────────────────────┐
│ Tool 1: read_schema (understand DB)    │
│ Tool 2: execute_query (test query)     │
│ Tool 3: suggest_optimization (improve) │
│ Tool 4: check_security (no SQL inject) │
│ Tool 5: write_migration (create schema)│
│                                        │
│ NOT: "Use all tools"                   │
│ ONLY: "Use these 5 tools"              │
└────────────────────────────────────────┘

Step 3: Create Specialized Prompt
┌────────────────────────────────────────┐
│ System prompt for SQL specialist:      │
│ "You are an expert in PostgreSQL.      │
│  Your role is to write optimal queries │
│  for this schema. You follow the       │
│  company's SQL best practices:         │
│  1. Always use prepared statements     │
│  2. Never do N+1 queries              │
│  3. Profile performance first          │
│  ..."                                  │
└────────────────────────────────────────┘

Step 4: Test Against Known Tasks
┌────────────────────────────────────────┐
│ Verify specialist works:                │
│ • "Write query for active users"       │
│ • "Optimize slow report query"         │
│ • "Fix N+1 problem"                    │
└────────────────────────────────────────┘

Key Principles:
• Narrow is better than broad
• Specialize reduces error rate
• Tools should be specific to role
• Prompts should be detailed
```

**Speaker Notes:**
The pattern is: focus the agent on one thing, give it the exact tools it needs for that thing, and prompt it to be expert in that area. This is more maintainable than trying to build one agent that does everything. When a specialist fails, you know exactly which one and can improve it. When a generalist fails, you have to debug which component went wrong.

---

### Slide 36: Section 4 Summary

**Title:** Section 4 Summary: Agent Specialization

**Content:**
```
KEY TAKEAWAYS:

1. Specialization: Multiple focused agents >
   One generalist agent

2. Common Specialists:
   • EXPLORER: Understand codebase
   • CODER: Write/modify code
   • TESTER: Verify tests pass
   • REVIEWER: Quality checks
   • SECURITY: Vulnerability detection
   • DEVOPS: Deployment/infrastructure

3. When to Use:
   Match specialist to task type
   Use pipeline: Explorer → Coder → Tester → ...

4. Design Principles:
   ✓ One clear responsibility
   ✓ Exactly the right tools
   ✓ Specialized prompts
   ✓ Testable against known tasks

5. Benefits:
   ✓ Faster (specialists don't waste time)
   ✓ Accurate (deep expertise)
   ✓ Safe (limited capabilities prevent accidents)
   ✓ Maintainable (focused responsibility)

NEXT: Understanding context windows—
      the technical foundation that
      limits all agent performance
```

**Speaker Notes:**
Specialization is a major architectural decision that separates effective agent systems from ineffective ones. Early generalist approaches were fun to try but don't scale. Modern production uses specialists. This should be the default assumption when students think about agent design.

---

## SECTION 5: Context Windows Deep Dive

---

### Slide 37: What IS a Context Window?

**Title:** Context Windows: The Technical Foundation

**Content:**
```
CONTEXT WINDOW: The amount of text (tokens)
an LLM can process in a single interaction

Visual Representation:

User Input:
"Implement pagination"
        |
        v
    ┌─────────────────────────────┐
    │   Agent's Context Window    │
    │                             │
    │ • System prompt (500 tokens)│
    │ • User request (100 tokens) │
    │ • Code files loaded (3K)    │
    │ • Previous chat history (2K)│
    │ • Tool descriptions (1.5K)  │
    │ • Agent reasoning (2K)      │
    │                             │
    │ TOTAL: 9.1K / 200K available│
    │ (4.5% of budget used)       │
    └─────────────────────────────┘
        |
        v
    Agent can continue with 190.9K tokens
    remaining before hitting limit

TOKENS: Not exactly words. Roughly:
• 1 token ≈ 0.75 words (English)
• 1 token ≈ 4 characters (average)
• 1 page of text ≈ 500-800 tokens

Window Size by Model (2026):
• Claude Haiku:      200K tokens
• Claude Opus 4.5:   200K tokens
• GPT-4 Turbo:       128K tokens
• Gemini Pro 1.5:    1,000K tokens (1M!)
```

**Speaker Notes:**
Context windows are often misunderstood as "unlimited." A 200K token window for English text is roughly 150 pages, which seems like a lot until you load an actual codebase. A single large file can easily be 5-10K tokens. Load 5 files plus conversation history plus system prompts, and you're approaching the limit. Understanding this limit is critical for effective agent design.

---

### Slide 38: Token Limits and Real Performance

**Title:** Token Limits: Theory vs Practice

**Content:**
```
THEORETICAL LIMIT vs PRACTICAL LIMIT

Theoretical (What the model can handle):
  Claude Opus: 200K tokens capacity
  = 150 pages of text
  = "Should be enough for any task"

Practical (What actually works):
  System prompt:       2K tokens (0.5 pages)
  Goal specification:  1K tokens (0.25 pages)
  Code files:          20K tokens (15 pages)
  Tool descriptions:   2K tokens (1.5 pages)
  Conversation history:10K tokens (7 pages)

  Available for work:  165K tokens

  But agent reasoning takes space:
  • Each decision:     500-2K tokens
  • Each observation:  1K-5K tokens

  With typical task: 10 decision cycles
  • Space used:       10 cycles × 3K = 30K

  Final available:    135K tokens

Reality Check:
┌────────────────────────────────────────┐
│ Practical Rule of Thumb:               │
│                                        │
│ Use no more than 50% of context window │
│ for "setup" (prompts, files, history)  │
│                                        │
│ If you're using >80%, agent will run   │
│ out of space mid-task and fail         │
└────────────────────────────────────────┘

Solution: Design agents to work within
practical limits, not theoretical limits
```

**Speaker Notes:**
This is where many agent projects fail. Engineers think "200K tokens is huge" and load everything into context. Then the agent runs out of tokens mid-task and has to be restarted, losing all progress. Good agent design assumes you'll only use 40-60% of the context window for any given task, leaving room for the agent's own reasoning and unexpected large outputs.

---

### Slide 39: Context Isolation in Multi-Agent Systems

**Title:** Context Isolation: Multi-Agent Architecture

**Content:**
```
CONTEXT ISOLATION: Separate contexts for
                   different agents

Naive Approach (PROBLEMATIC):
┌────────────────────────────────────┐
│ ONE MASSIVE CONTEXT                │
│                                    │
│ • All code files (50K tokens)      │
│ • All tools (5K tokens)            │
│ • Full conversation (20K tokens)   │
│ • All specialists can see/do all   │
│ • Total: 75K tokens consumed       │
│                                    │
│ Problems:                          │
│ ✗ Confuses specialist agents       │
│ ✗ Wastes tokens on irrelevant code │
│ ✗ All agents compete for context   │
│ ✗ Can't parallelize effectively    │
└────────────────────────────────────┘

Smart Approach (ISOLATED):
┌────────────────────────────┐
│ COORDINATOR CONTEXT        │
│ • Task overview: 1K        │
│ • Agent registry: 1K       │
└────────────────────────────┘
         |
    ┌────┴─────┬────────┐
    |          |        |
    v          v        v
┌────────┐ ┌───────┐ ┌──────────┐
│EXPLORE │ │CODER  │ │SECURITY  │
│CONTEXT │ │CONTEX │ │CONTEXT   │
│        │ │       │ │          │
│• Files │ │• Code │ │• Vulner- │
│• Search│ │• Tests│ │  ability │
│ patterns│ │• Lint│ │  scanner │
│ 2K     │ │ 3K   │ │  2.5K    │
└────────┘ └───────┘ └──────────┘

Benefits:
✓ Each agent has exactly needed context
✓ Reduced token usage overall
✓ Can parallelize (agents don't interfere)
✓ Easy to reason about (focused scope)
```

**Speaker Notes:**
This is an architectural choice that separates scalable agent systems from those that collapse. When agents have isolated contexts, they can work in parallel and don't interfere with each other. The coordinator maintains minimal context and routes tasks to appropriate specialists. This scales much better than monolithic single-agent systems.

---

### Slide 40: Gemini's 1M Token Window

**Title:** Gemini Pro 1.5: The 1 Million Token Window

**Content:**
```
GEMINI PRO 1.5: A Game Changer

Context Size Comparison:
┌──────────────────┬──────────────┐
│ Model            │ Context Size │
├──────────────────┼──────────────┤
│ GPT-4 Turbo      │ 128K         │
│ Claude Opus 4.5  │ 200K         │
│ Gemini Pro 1.5   │ 1,000K ⭐    │
│ Ratio:           │ 5-8x larger  │
└──────────────────┴──────────────┘

What 1M Tokens Means:
• ~750,000 words
• ~3,000 pages of text
• An entire codebase (reasonable size)
• Full project history
• Complete documentation
• All tests
• All examples

Practical Application:
┌──────────────────────────────────────┐
│ Could load:                          │
│ • 50 Python files (10K lines total)  │
│ • Complete test suite                │
│ • All documentation                  │
│ • Git history (last 100 commits)     │
│ • Related PRs and issues             │
│ • Still have 500K tokens left!       │
└──────────────────────────────────────┘

Implications for Agent Design:
1. Can load entire projects into context
2. Might not need isolation strategies
3. Different tradeoff calculation
4. Enables new architectural patterns

BUT: Larger context ≠ Better answers
• Reasoning capability still matters
• More tokens still cost more
• Attention may diffuse over huge contexts
• Still need to manage irrelevant info

Typical Use Case:
"Here's my entire project repo.
Fix all bugs, optimize performance,
add documentation, improve tests.
Then deploy to production."

vs

Traditional approach (multiple prompts):
"Identify bugs" → "Fix them" → "Test"
(3 separate agent runs)
```

**Speaker Notes:**
Gemini 1.5's massive context window is a paradigm shift. It's still new (as of early 2026), and we're still learning how to use it effectively. The naive approach (load everything, let the agent figure it out) doesn't work well. Even with 1M tokens, quality of token selection matters more than raw quantity. An agent with 1M tokens of irrelevant code performs worse than one with 200K tokens of carefully selected relevant code. This is a frontier of agent research right now.

---

### Slide 41: Context Management Strategies

**Title:** Managing Context: Practical Strategies

**Content:**
```
CONTEXT MANAGEMENT: How to use limited
                    context effectively

Strategy 1: Chunking (Divide into pieces)
┌──────────────────────────────────────┐
│ Task: "Refactor entire API"          │
│                                      │
│ Load only relevant file at a time:   │
│ • Cycle 1: Load user_routes.py       │
│   Refactor and test it               │
│   Save to file                       │
│ • Cycle 2: Load auth_routes.py       │
│   Refactor and test it               │
│   Save to file                       │
│ • Cycle 3: Load product_routes.py    │
│   Refactor and test it               │
│   Save to file                       │
│                                      │
│ Total: 3 cycles × 50K tokens         │
│ vs   : 1 cycle × 150K tokens         │
│                                      │
│ Advantage: Cleaner, parallelizable   │
└──────────────────────────────────────┘

Strategy 2: Summarization (Extract essence)
┌──────────────────────────────────────┐
│ Observation: "This 10K-token class   │
│ has 50 methods"                      │
│                                      │
│ Summarize for context:               │
│ "ClassX has these methods:           │
│  - __init__: initialize              │
│  - load_data: fetch from DB          │
│  - process: transform data           │
│  - save: persist to cache            │
│  See full class in file X"           │
│                                      │
│ Saves: 9K tokens                     │
│ Loss: Some detail, but preserves     │
│       agent's ability to work        │
└──────────────────────────────────────┘

Strategy 3: Phasing (Task decomposition)
┌──────────────────────────────────────┐
│ Instead of:                          │
│ "Here's the code, fix everything"   │
│                                      │
│ Phase it:                            │
│ Phase 1: "Fix critical bugs"         │
│ Phase 2: "Add type hints"            │
│ Phase 3: "Optimize performance"      │
│ Phase 4: "Add tests"                 │
│                                      │
│ Each phase: clean context,           │
│ focused goal, archived results       │
└──────────────────────────────────────┘

Strategy 4: Lazy Loading (Load on demand)
┌──────────────────────────────────────┐
│ Don't load file until needed:        │
│                                      │
│ Agent: "I need to understand         │
│        the database schema"          │
│                                      │
│ Framework: Load schema file now      │
│                                      │
│ vs                                   │
│                                      │
│ Naive: Load schema at start          │
│        (wastes tokens if unneeded)   │
└──────────────────────────────────────┘

Best Practice:
Use multiple strategies together:
1. Chunk large tasks into phases
2. Summarize large classes/files
3. Lazy load details on demand
4. Archive completed phases to files
```

**Speaker Notes:**
These aren't one-time decisions; they're design patterns that effective agent systems use throughout. A well-designed agent might process a large project by chunking it into logical components, summarizing complex parts, phasing the work, and lazy-loading details. This is why agent design is harder than prompt engineering—it requires systems thinking about resource management.

---

### Slide 42: Section 5 Summary

**Title:** Section 5 Summary: Context Windows

**Content:**
```
KEY TAKEAWAYS:

1. What is a Context Window:
   Amount of text (tokens) an LLM can
   process in one interaction

2. Token Arithmetic:
   1 token ≈ 0.75 words (English)
   1 page ≈ 500-800 tokens
   200K tokens ≈ 150 pages

3. Theoretical vs Practical:
   Theoretical: "I have 200K tokens"
   Practical: "50% for setup, 50% for work"
   Reality: Plan for 100-125K effective tokens

4. Context Isolation:
   Separate contexts for different agents
   Enables parallelization and focus
   Reduces total token consumption

5. Gemini's 1M Window:
   Game-changer for loading entire projects
   But doesn't eliminate need for strategy
   Quality of content > quantity

6. Management Strategies:
   • Chunking: Divide into manageable pieces
   • Summarization: Extract essence
   • Phasing: Decompose tasks logically
   • Lazy loading: Load on demand

PRACTICAL INSIGHT:
Best agent systems are NOT those with
largest context windows, but those that
manage context most effectively
```

**Speaker Notes:**
Context management is where art meets engineering. Naive use of large context windows often performs worse than strategic use of smaller windows. This is why experienced agent designers think about context budgeting from day one of system design.

---

## SECTION 6: Agent Autonomy Levels

---

### Slide 43: Autonomy Levels Overview

**Title:** Agent Autonomy Levels: Balancing Safety & Efficiency

**Content:**
```
AUTONOMY: How much decision-making power
does the agent have?

Why This Matters:
• Higher autonomy = faster execution
• Lower autonomy = more control/safety
• Different tasks need different levels

Autonomy Spectrum:
┌─────────────────────────────────────┐
│                                     │
│ MANUAL          SEMI-AUTO    FULL   │
│ (0%)            (50%)        (100%) │
│ ←────────────────────────────────→  │
│ Most safe      Practical     Risky  │
│ Slowest        Balanced      Fastest│
│                                     │
└─────────────────────────────────────┘

Modern Best Practice:
Most production agents operate in the
SEMI-AUTONOMOUS zone (40-70% autonomous)
```

**Speaker Notes:**
Autonomy is not a single setting but a design choice that affects the entire workflow. It's also not permanent—the same agent might operate at different autonomy levels for different tasks. Complex refactoring might need confirmation at each step, while routine formatting can be fire-and-forget.

---

### Slide 44: Autonomy Level 1 - Read-Only Mode

**Title:** Autonomy Level 1: Read-Only Mode

**Content:**
```
READ-ONLY MODE: Agent can only observe,
                not modify

Characteristics:
┌──────────────────────────────────────┐
│ • Agent has read tools                │
│ • No write tools                      │
│ • No execution tools                  │
│ • No deployment tools                 │
│ • Agent generates reports/analysis    │
│ • Humans make all decisions           │
│ • Zero risk of agent mistakes         │
└──────────────────────────────────────┘

Typical Use Cases:
┌────────────────────────────────────┐
│ • Code review/analysis              │
│ • Security audit                    │
│ • Architecture exploration          │
│ • Performance profiling             │
│ • Documentation generation          │
│ • Codebase understanding            │
└────────────────────────────────────┘

Workflow Example:
┌──────────────────────────────────────┐
│ Agent: "I've found 3 security issues:│
│        1. SQL injection in user.py   │
│        2. Hardcoded password         │
│        3. XSS vulnerability"         │
│                                      │
│ Human: Reviews findings, decides to  │
│        fix issue #1 and #2 immediately,
│        schedules #3 for later       │
└──────────────────────────────────────┘

Autonomy Level: 0%
(Agent has zero decision power,
 zero execution power)

Pros:                      Cons:
✓ Maximum safety           ✗ Slowest
✓ Easy to audit            ✗ Human dependent
✓ Low risk                 ✗ Can't scale
✓ Good for learning        ✗ Tedious for routine
```

**Speaker Notes:**
Read-only mode is the safest but least efficient. It's often the starting point when introducing agents to a team. Once the team trusts the agent's analysis, you can move to higher autonomy for routine tasks while keeping read-only for critical decisions.

---

### Slide 45: Autonomy Level 2 - Confirm Each Action

**Title:** Autonomy Level 2: Confirm-Each-Action

**Content:**
```
CONFIRM-EACH-ACTION: Agent can plan and decide,
                     but needs human approval
                     for each action

Characteristics:
┌──────────────────────────────────────┐
│ • Agent reads and understands         │
│ • Agent analyzes and plans            │
│ • Agent proposes actions              │
│ • Human approves each action          │
│ • Agent executes only approved        │
│ • Clear audit trail                   │
│ • Balances autonomy and control       │
└──────────────────────────────────────┘

Workflow Example:
┌──────────────────────────────────────┐
│ Agent: "To implement pagination, I   │
│        need to: 1) add offset/limit  │
│        params 2) modify query 3)     │
│        add tests"                    │
│                                      │
│ Human: Approves steps 1 & 2,         │
│        asks to split tests into      │
│        unit + integration            │
│                                      │
│ Agent: "Understood. Proceeding with  │
│        1, 2, then splitting tests"   │
│                                      │
│ (Each change requires approve)       │
└──────────────────────────────────────┘

Typical Use Cases:
┌────────────────────────────────────┐
│ • Important bug fixes               │
│ • Database migrations               │
│ • API changes                       │
│ • Performance optimization          │
│ • Any change affecting production   │
└────────────────────────────────────┘

Autonomy Level: ~30%
(Agent plans and decides strategy,
 humans approve each execution)

Pros:                      Cons:
✓ High safety              ✗ Slow (approval wait)
✓ Good control             ✗ Human must understand
✓ Clear audit trail        ✗ Approval becomes
✓ Prevents mistakes          bottleneck
                           ✗ Context switching
```

**Speaker Notes:**
This is the mode most enterprises start with. It gives confidence that the agent isn't doing anything unexpected while still moving faster than pure read-only. The tradeoff is that approval waits can become a bottleneck—if humans don't respond quickly, the agent stalls.

---

### Slide 46: Autonomy Level 3 - Auto-Accept with Review

**Title:** Autonomy Level 3: Auto-Accept with Review

**Content:**
```
AUTO-ACCEPT WITH REVIEW: Agent executes immediately,
                         humans review afterward

Characteristics:
┌──────────────────────────────────────┐
│ • Agent reads and understands         │
│ • Agent plans and decides             │
│ • Agent executes immediately          │
│ • System logs all actions             │
│ • Human reviews soon after            │
│ • Can rollback if issues found        │
│ • Faster execution                    │
│ • Post-hoc safety check               │
└──────────────────────────────────────┘

Workflow Example:
┌──────────────────────────────────────┐
│ Agent: "Fixing test timeout bug"     │
│ (Reads code, makes changes,          │
│  runs tests, commits)                │
│ [5 minutes pass]                     │
│                                      │
│ Human: Reviews CI/CD logs, sees:     │
│  • 47 tests run                      │
│  • All passed                        │
│  • 3 new assertions added            │
│ Human: "Looks good! ✓"               │
│                                      │
│ vs                                   │
│                                      │
│ If issues found:                     │
│ Human: "Revert this commit"          │
│ (Rollback executed)                  │
└──────────────────────────────────────┘

Typical Use Cases:
┌────────────────────────────────────┐
│ • Routine bug fixes                 │
│ • Test improvements                 │
│ • Documentation updates             │
│ • Code formatting/linting           │
│ • Internal refactoring              │
│ • Optimization tasks                │
│ • ANY task with reliable pass/fail  │
└────────────────────────────────────┘

Autonomy Level: ~70%
(Agent decides and executes,
 humans spot-check results)

Pros:                      Cons:
✓ Fast (no wait time)       ✗ Need good rollback
✓ Efficient                 ✗ Trust required
✓ No approval bottleneck    ✗ Post-hoc is slower
✓ Works for routine tasks   ✗ Some issues slip
                              through before
                              review
```

**Speaker Notes:**
This mode works best for tasks with clear success/failure signals. If a test passes, the code is good. If it fails, rollback. The key is reliable observability—you need clear metrics to know if the agent did the right thing. This is why it works great for code but less well for infrastructure where effects might be delayed.

---

### Slide 47: Autonomy Level 4 - Fire-and-Forget

**Title:** Autonomy Level 4: Fire-and-Forget

**Content:**
```
FIRE-AND-FORGET: Agent operates with minimal
                 human oversight

Characteristics:
┌──────────────────────────────────────┐
│ • Agent completely autonomous        │
│ • No human approval needed           │
│ • System logs actions                │
│ • Humans monitor from afar           │
│ • Alert if something goes wrong      │
│ • Fastest execution                  │
│ • Highest risk                       │
└──────────────────────────────────────┘

Workflow Example:
┌──────────────────────────────────────┐
│ Agent: (Internal decision loop)      │
│ "Tests failing... fixing... retesting...
│  all passing. Task complete."        │
│ (No human involvement)               │
│                                      │
│ System Monitor: Background process   │
│ "Agent completed 47 tasks today.     │
│  3 required manual intervention.     │
│  44 succeeded autonomously."         │
└──────────────────────────────────────┘

Typical Use Cases:
┌────────────────────────────────────┐
│ • Scheduled maintenance             │
│ • Log rotation                      │
│ • Cache clearing                    │
│ • Health checks                     │
│ • Routine report generation         │
│ • Automated testing (no code change)│
│ • Status updates                    │
│                                     │
│ NOT RECOMMENDED FOR:                │
│ • Production deployments            │
│ • Database changes                  │
│ • Security-related operations       │
│ • Large-scale refactoring           │
└────────────────────────────────────┘

Autonomy Level: ~95%+
(Agent has nearly complete decision power,
 humans only intervene on errors)

Pros:                      Cons:
✓ Maximum efficiency        ✗ High risk
✓ No human bottleneck       ✗ Hard to debug
✓ Scales well               ✗ Limited visibility
✓ Machines working 24/7     ✗ Requires perfection
                            ✗ Regulatory issues
```

**Speaker Notes:**
Fire-and-forget is rare in practice for important systems. It's mostly used for routine maintenance tasks where failure is acceptable. Some teams experiment with it for non-production tasks or low-risk scenarios. It's the frontier of agent autonomy but comes with significant risks that most organizations aren't ready to accept yet (2026).

---

### Slide 48: Choosing the Right Autonomy Level

**Title:** Choosing Autonomy Level: Decision Framework

**Content:**
```
DECISION TREE: Which autonomy level to use?

Start: "What task does the agent do?"
       |
       v
    Is failure safe?
    (No cascading problems?)
       |
    ┌──NO──┬──YES─┐
    |      |      |
    v      v      v
   Can we Can we clear
   roll   pass/fail?
   back?  |
    |    ┌─YES─┬─NO──┐
    |    v     v     v
    |   L3    Can we
   L2  (Auto- easily
    &  Accept) verify?
   L3       |
        ┌─YES──┬─NO──┐
        v      v     v
       L3     L2    L1
    (Fast)  (Safe) (Safest)

Autonomy Selection Guide:
┌──────────────────┬──────────────────┐
│ Task Type        │ Recommended Level│
├──────────────────┼──────────────────┤
│ Security fixes   │ L2: Confirm each │
│ Performance bugs │ L3: Auto-accept  │
│ Documentation   │ L3: Auto-accept  │
│ Tests generation │ L3: Auto-accept  │
│ Code review      │ L1: Read-only    │
│ Deployments      │ L2: Confirm each │
│ Refactoring      │ L2-L3 (depends)  │
│ Exploration      │ L1: Read-only    │
│ Maintenance      │ L4: Fire-forget  │
└──────────────────┴──────────────────┘

Key Questions:
1. What's the cost of failure?
   (Low → Higher autonomy)

2. Can we detect failure?
   (Yes → Higher autonomy)

3. Can we recover quickly?
   (Yes → Higher autonomy)

4. Do we trust the agent?
   (Yes → Higher autonomy)
```

**Speaker Notes:**
There's no universal answer—it depends entirely on the task and organization's risk tolerance. A startup might be comfortable with L3 for everything. A bank might want L2 for everything. The key is making conscious choices based on risk, not just defaulting to one level. As trust builds over time, organizations often gradually increase autonomy from L2 to L3 to L4, but only for proven patterns.

---

### Slide 49: Autonomy in Practice - Examples

**Title:** Autonomy Levels in Real-World Projects

**Content:**
```
REAL PROJECT EXAMPLE: Building a web service

Phase 1: Exploration & Design
Agent: EXPLORER AGENT (Read-Only, L1)
Task: "Map the existing architecture"
Result: Report on current structure
Autonomy: Minimal (just reads)
Why: Team needs to understand before changes

Phase 2: Implementation
Agent: CODER AGENT (Auto-Accept, L3)
Task: "Implement new API endpoint"
Result: Code written, tested locally
Autonomy: High (no approval waits)
Why: Clear success (tests pass), easy to rollback

Phase 3: Review & QA
Agent: REVIEWER AGENT (Read-Only, L1)
Task: "Code review for quality"
Result: List of issues and suggestions
Autonomy: Minimal (human makes decisions)
Why: Qualitative analysis, needs human judgment

Phase 4: Testing
Agent: TESTER AGENT (Auto-Accept, L3)
Task: "Write and run test suite"
Result: Coverage report, test results
Autonomy: High (clear pass/fail)
Why: Objective outcome, automated rollback possible

Phase 5: Deployment
Agent: DEVOPS AGENT (Confirm-Each, L2)
Task: "Deploy to staging"
Result: Asks for confirmation before deploying
Autonomy: Low-Medium
Why: High-impact decision, needs approval

Phase 6: Monitoring
Agent: MONITORING AGENT (Fire-and-Forget, L4)
Task: "Monitor health, restart if needed"
Result: Autonomous operation with alerts
Autonomy: Very High
Why: Low-risk, needs 24/7 availability

Pattern: Different agents at different levels
         in a coordinated pipeline
```

**Speaker Notes:**
This shows how autonomy decisions aren't one-time but evolve throughout the system. The same organization uses L1 for critical review decisions but L4 for routine maintenance. The art is matching autonomy to task, not picking a one-size-fits-all approach.

---

### Slide 50: Section 6 Summary

**Title:** Section 6 Summary: Agent Autonomy Levels

**Content:**
```
KEY TAKEAWAYS:

1. Autonomy Spectrum: Ranges from 0% (read-only)
   to 95%+ (fire-and-forget)

2. Four Main Levels:
   • L1 Read-Only: 0% autonomy (observe only)
   • L2 Confirm-Each: ~30% autonomy (plan & get approval)
   • L3 Auto-Accept: ~70% autonomy (execute & review)
   • L4 Fire-Forget: 95%+ autonomy (fully autonomous)

3. Choosing the Right Level:
   • Safety of failure (low safety → lower autonomy)
   • Ability to detect failure (poor detection → lower)
   • Ability to recover (hard recovery → lower)
   • Trust in agent (low trust → lower)

4. Best Practices:
   ✓ Start conservative, increase over time
   ✓ Different agents at different levels
   ✓ Match autonomy to task risk
   ✓ Build monitoring for high-autonomy tasks

5. Reality:
   • Most production agents: L2-L3 range
   • L4 rare, L1 used for exploration/review
   • Autonomy isn't permanent; adjust per task

FINAL INSIGHT:
Autonomy is not about trust in the agent's
technical capability, but about organizational
risk tolerance and task characteristics
```

**Speaker Notes:**
This section ties together all previous concepts. Students should leave understanding that every agent decision involves tradeoffs: faster vs safer, autonomous vs controlled, efficient vs explainable. The best systems make these choices deliberately, not accidentally.

---

## PART 7 CONCLUSION

---

### Slide 51: Part 7 Summary & Key Concepts

**Title:** Part 7 Complete: Agent Definition & Concepts

**Content:**
```
WHAT WE COVERED:

Section 1: What IS an Agent?
• Formal definition (perceive→reason→act→observe)
• Distinction from traditional AI assistants
• Key characteristics: autonomy, goal-directed, tool use
• Why agents matter for coding

Section 2: Core Agent Components
• LLM: The reasoning engine
• Memory/Context: The workspace (with token limits)
• Tools: The hands (interaction mechanisms)
• Planning: Forward-thinking capability

Section 3: The ReAct Loop
• REASON: Think about situation
• ACT: Execute tool
• OBSERVE: Interpret results
• Loop mechanics and why it works
• ReAct vs ReWOO patterns

Section 4: Agent Specialization
• Generalists vs Specialists (specialists win)
• Common types: Explorer, Coder, Tester, Reviewer, Security, DevOps
• Design principles for custom specialists
• Specialist pipeline architecture

Section 5: Context Windows
• What are tokens and context windows
• Theory vs practice (50% overhead rule)
• Context isolation in multi-agent systems
• Gemini's 1M token game-changer
• Management strategies: chunking, summarization, phasing

Section 6: Autonomy Levels
• Spectrum from read-only to fire-and-forget
• Four main levels (L1, L2, L3, L4)
• Decision framework for choosing level
• Real-world examples of mixing levels

FOUNDATIONAL PRINCIPLES:
1. Agents are iterative, not one-shot (ReAct loop)
2. Specialization beats generalization
3. Context is finite and expensive
4. Autonomy must match task risk
5. Tools determine capability
```

**Speaker Notes:**
Recap all major themes. Students should leave this part with a solid understanding of what agents are, how they work internally, and how to design them effectively. The next part will show how to build and deploy these systems.

---

### Slide 52: Connections to Future Parts

**Title:** Preparation for Upcoming Parts

**Content:**
```
WHERE WE GO FROM HERE:

Concepts in Part 7          Applied in Future Parts
│                           │
├─ Agent definition    →    Part 8: Building your first agent
├─ ReAct loop          →    Part 9: Agent implementation patterns
├─ Tool design         →    Part 10: Creating custom tools
├─ Specialization      →    Part 11: Multi-agent systems
├─ Context management  →    Part 12: Scaling agents
├─ Autonomy levels     →    Part 13: Safety & constraints
└─ LLM selection       →    Part 14: Advanced techniques

PART 8 PREVIEW:
You'll implement your first agent using these
concepts. You'll create:
• A simple Explorer agent (read-only)
• A Coder agent (with guardrails)
• A coordinator to orchestrate them

PART 9 PREVIEW:
Common patterns you'll see:
• Sequential pipeline (A→B→C)
• Parallel execution (A|B parallel, then C)
• Feedback loops (A→B→A for refinement)
• Branching (different paths based on results)

PART 10 PREVIEW:
You'll design tools by:
• Identifying what agents need to do
• Creating specific, reliable tools
• Testing tools with agents
• Iterating on tool design

PART 11 PREVIEW:
You'll build:
• Communication between agents
• Shared state management
• Conflict resolution
• Emergent behavior
```

**Speaker Notes:**
This frames Part 7 as foundational knowledge that will be applied immediately. Students should feel that they now have the conceptual vocabulary and mental models they need, and the next parts show the practical implementation. This is the transition from "theory of agents" to "engineering agents."

---

### Slide 53: Key Takeaways & Reflection

**Title:** Key Takeaways: What You Now Understand

**Content:**
```
BY THE END OF PART 7, YOU CAN EXPLAIN:

Conceptual Understanding:
□ What an agent is (not just a chatbot)
□ How agents differ from traditional AI
□ Why ReAct loop works better than planning
□ When to use specialists vs generalists
□ Why context windows matter practically
□ How to choose appropriate autonomy levels

Technical Understanding:
□ LLM as reasoning engine
□ Memory as context window budget
□ Tools as action mechanisms
□ Planning as forward-thinking
□ Token accounting and management
□ Tool calling protocol

Design Understanding:
□ How to architect multi-agent systems
□ Trade-offs between autonomy and safety
□ Context isolation for scalability
□ Specialization patterns
□ Token budgeting strategies

Practical Judgment:
□ When to use which specialist
□ How much autonomy for which task
□ How to design effective tools
□ How to manage context effectively
□ How to debug agent behavior

SELF-CHECK QUESTIONS:

1. Explain to a non-technical person what
   an agent is and why it's different from ChatGPT.

2. Walk through a ReAct loop for "fix this bug"
   - what happens in each step?

3. Design a specialist agent for writing unit tests.
   What tools would it have? What would it NOT have?

4. You have a 200K token context. A project needs
   30K tokens. How would you manage this?

5. A task could be done by the agent at L2 or L3.
   What questions would you ask to decide?

If you can answer these, you understand Part 7.
```

**Speaker Notes:**
These self-check questions are the real learning objectives. Students don't need to memorize definitions—they need to be able to reason about agent design using these concepts. Frame this as the real goal: can you use these ideas to solve problems?

---

### Slide 54: Common Misconceptions to Avoid

**Title:** Common Misconceptions & Clarifications

**Content:**
```
MISCONCEPTION #1:
"More tools = better agent"

REALITY:
10-15 well-designed tools > 50 random tools
Agents get confused with too many options
Tool quality > tool quantity

MISCONCEPTION #2:
"Larger context window = better agent"

REALITY:
200K context used wisely > 1M context poorly used
Relevant tokens > total tokens
Context management skill matters more than size

MISCONCEPTION #3:
"Agents always pick the best approach"

REALITY:
Agents use LLM reasoning (probabilistic, not perfect)
May converge on local optima, not global
May miss creative solutions
Still need human oversight

MISCONCEPTION #4:
"Agents should be as autonomous as possible"

REALITY:
Autonomy should match task risk
High autonomy for low-risk, reversible tasks
Low autonomy for high-risk, irreversible tasks
Most tasks benefit from medium autonomy

MISCONCEPTION #5:
"One agent can do all coding tasks"

REALITY:
Specialization beats generalization
Different tasks need different approaches
Multi-agent systems outperform monolithic agents

MISCONCEPTION #6:
"Planning upfront is better than ReAct"

REALITY:
ReAct adapts to unexpected findings
Planning fails on ambiguous/complex tasks
ReAct+human feedback > planning alone

MISCONCEPTION #7:
"Agent ability = LLM ability"

REALITY:
Agent ability = LLM ability × Tool quality ×
                Context management × Design

Bad tools can cripple a capable LLM
Good tools can amplify a modest LLM
```

**Speaker Notes:**
Addressing misconceptions explicitly helps students avoid pitfalls their peers made. These come from common patterns seen in early agent projects that failed to meet expectations.

---

### Slide 55: Resources for Further Learning

**Title:** Learning Resources & Exploration

**Content:**
```
KEY PAPERS (Academic Foundation):

"ReAct: Synergizing Reasoning and Acting
 in Language Models" (Yao et al., 2023)
→ The paper that formalized ReAct pattern

"AutoGPT, BabyAGI, etc."
→ Early agent systems (2023)

"Language Models as Zero-Shot Planners"
→ How LLMs approach planning

"Specialization vs Generalization in AI"
→ Why specialists outperform generalists


FRAMEWORKS & TOOLS:

Claude Code (Anthropic, 2024+)
→ Production agent framework

AutoGPT
→ Open-source agent implementation

LangChain / LlamaIndex
→ Agent libraries with tool support

CrewAI
→ Multi-agent orchestration


BLOGS & ARTICLES:

Anthropic Research Blog
→ Latest on agent architectures

OpenAI Research
→ Development of agent capabilities

Hugging Face Blog
→ Open-source agent tools


HANDS-ON EXPERIMENTS:

Build your own agent:
1. Pick an LLM (Claude, GPT-4, etc.)
2. Design 5-10 tools
3. Write system prompt
4. Test ReAct loop manually
5. Iterate based on results

Explore existing agents:
1. Try Claude Code on real task
2. Observe how it plans vs executes
3. Understand why it made specific tool choices
4. Think about how you'd design it differently


COMMUNITIES:

Discord: AI/Agent focused communities
Reddit: r/agents, r/MachineLearning
Twitter: Follow researchers and practitioners
Slack: Company/university channels
```

**Speaker Notes:**
Give students entry points for deeper learning. Some will want to study the theory, others want to build immediately. Provide resources for both paths. The key is showing that this isn't magic—there's solid research behind these concepts, and students can dive deeper if interested.

---

### Slide 56: Final Reflection & Next Steps

**Title:** Closing Reflection: You Now Understand Agents

**Content:**
```
JOURNEY SO FAR:

Started with: "What even is an agent?"
Discovered: Agents are iterative loops with
            reasoning + action + observation

Started with: "How does it work internally?"
Discovered: LLM thinks, tools act, memory holds context
            Autonomy tradeoffs drive design

Started with: "How do I build one?"
Discovered: Specialization, careful tool design,
            context management, autonomy choices

NOW YOU CAN:

✓ Explain agents to others (conceptually)
✓ Distinguish agents from ChatGPT
✓ Design specialist agents for tasks
✓ Reason about autonomy levels
✓ Plan context budgeting
✓ Understand ReAct vs other patterns
✓ Debug why agents fail
✓ Make architectural decisions

NEXT: PART 8 - BUILDING YOUR FIRST AGENT

You'll take these concepts and:
1. Build a real agent (with code)
2. Define actual tools
3. Run ReAct loop with real LLM
4. Debug when it doesn't work
5. Iterate to improve

This theory becomes practice.

QUESTION TO CARRY FORWARD:
"For MY use case, what would be the
ideal agent architecture?"

Think about it as you review Part 7.
You'll implement your answer in Part 8.
```

**Speaker Notes:**
End on a forward-looking note. Students should leave this part feeling competent to discuss agents and ready to implement them. The gap between theory and practice is closed in Part 8.

---

## APPENDIX: Reference Materials

---

### Appendix A: Glossary

**Title:** Appendix A: Terminology Reference

**Content:**
```
AGENT GLOSSARY:

Agent: Autonomous system perceiving environment,
       reasoning about goals, taking actions, observing
       results, adapting behavior

Autonomy: Degree of independent decision-making power
          (0% = read-only, 95%+ = fire-and-forget)

Context Window: Amount of text (tokens) an LLM can
                process in single interaction

LLM: Large Language Model (GPT-4, Claude, Gemini, etc.)
     The reasoning engine of an agent

Memory: Agent's knowledge of current task, previous
        actions, observations (stored in context)

ReAct: Pattern of interleaved reasoning and acting
       (REASON→ACT→OBSERVE loop)

ReWOO: Alternative to ReAct where agent plans all
       actions before executing any

Specialist Agent: Agent designed for specific task type
                 (coder, tester, reviewer, etc.)

Generalist Agent: Agent designed to handle many task types
                 (less effective in practice)

Token: Smallest unit of text for LLMs
       ~1 token ≈ 0.75 words (English)

Tool: Well-defined capability agent uses to act
      (read file, write code, run test, etc.)

Tool Calling: Protocol where LLM decides what tool to
              use, framework executes it

Reasoning: LLM thinking about situation, planning next
          step (happens internally, no external effect)

Acting: Agent executing a tool (only step changing world)

Observing: Agent interpreting results of action and
          extracting insights

Context Isolation: Separate memory/context for different
                   agents to prevent interference

Chunking: Breaking large task into manageable pieces,
         each with separate context

Summarization: Reducing large text to key concepts,
              preserving understanding while saving tokens

Phasing: Decomposing task into logical sequential stages

Lazy Loading: Loading information only when agent needs it,
             not loading everything upfront
```

**Speaker Notes:**
This glossary can be printed or referenced throughout the course. Students will encounter these terms repeatedly in future parts and should have definitions available.

---

### Appendix B: Quick Reference - Autonomy Levels

**Title:** Appendix B: Autonomy Levels Quick Reference

**Content:**
```
AUTONOMY LEVELS QUICK REFERENCE TABLE:

┌────────┬──────────────┬──────────────┬──────────┐
│Level   │Name          │Autonomy %    │Best For  │
├────────┼──────────────┼──────────────┼──────────┤
│L1      │Read-Only     │0%            │Analysis  │
│        │              │              │Reviews   │
│        │              │              │Security  │
│        │              │              │audits    │
├────────┼──────────────┼──────────────┼──────────┤
│L2      │Confirm-Each  │~30%          │Important │
│        │              │              │decisions │
│        │              │              │DB schema │
│        │              │              │changes   │
├────────┼──────────────┼──────────────┼──────────┤
│L3      │Auto-Accept   │~70%          │Routine   │
│        │              │              │bugs      │
│        │              │              │Tests     │
│        │              │              │Docs      │
├────────┼──────────────┼──────────────┼──────────┤
│L4      │Fire-Forget   │95%+          │Maintenance
│        │              │              │Monitoring│
│        │              │              │Logging   │
└────────┴──────────────┴──────────────┴──────────┘

Decision Quick-Check:
Is failure acceptable?           YES→ Higher autonomy
Can we detect failure quickly?   YES→ Higher autonomy
Can we recover easily?           YES→ Higher autonomy
Does team trust agent?           YES→ Higher autonomy
Is this production-critical?     YES→ Lower autonomy
```

**Speaker Notes:**
This table can be laminated or bookmarked for quick reference during design decisions.

---

### Appendix C: Specialist Agent Comparison Chart

**Title:** Appendix C: Specialist Agents Comparison

**Content:**
```
SPECIALIST AGENTS: QUICK COMPARISON

                 EXPLORER  CODER   TESTER  REVIEWER  SECURITY  DEVOPS
┌────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼──────────┐
│Primary Task    │Understand│Modify  │Verify  │Quality  │Threats  │Deploy    │
│                │         │Code    │Tests   │Check    │Analysis │          │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼──────────┤
│Can Read?       │✓        │✓       │✓       │✓       │✓       │✓        │
│Can Write Code? │         │✓       │Limited │         │        │✓ (config)│
│Can Execute?    │         │Local   │✓       │         │         │✓        │
│Can Deploy?     │         │        │        │         │         │✓        │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼──────────┤
│Key Tools       │Search   │Write   │Run     │Analyze  │Scan    │Deploy   │
│                │Analyze  │Edit    │Tests   │Lint     │Check   │Monitor  │
│                │Map      │Git ops │Analyze │Review   │Audit   │Health   │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼──────────┤
│Autonomy Level  │L1       │L2-L3   │L3      │L1       │L1-L2   │L2-L4    │
│                │(Read)   │(Medium)│(High)  │(Read)   │(Low)   │(Var)    │
├────────────────┼─────────┼─────────┼─────────┼─────────┼─────────┼──────────┤
│Typical Tasks   │"Map     │"Impl.  │"Run    │"Review  │"Scan   │"Deploy" │
│                │structure"│feature"│tests"  │PR"      │vulns"  │"Rollback│
│                │"Find    │"Refact"│"Write  │"Suggest │"Audit  │"Monitor"│
│                │patterns"│"Optimize
" │tests"  │improve" │deps"   │"Health" │
└────────────────┴─────────┴─────────┴─────────┴─────────┴─────────┴──────────┘

Typical Pipeline Order:
EXPLORER → CODER → TESTER → REVIEWER → SECURITY → DEVOPS
(Understand)→(Change)→(Verify)→(Quality)→(Safety)→(Deploy)
```

**Speaker Notes:**
This visual comparison helps students quickly understand which specialist to use and what capabilities they have.

---

## END OF PART 7

**Final Notes for Instructors:**

This 56-slide comprehensive guide covers all aspects of agent definition and concepts. Each section can stand alone for reference, or be taught sequentially. The tone balances academic rigor with practical application. Students should complete with strong conceptual foundations ready for implementation in Part 8.

Key learning outcomes verified:
- Students can explain what agents are
- Students understand ReAct loop mechanics
- Students can design specialist agents
- Students understand context management
- Students can reason about autonomy tradeoffs
- Students understand why these patterns work

Estimated teaching time: 4-6 hours (depending on interactive discussion)
```

**Speaker Notes:**
Wrap up with confidence that this part provides complete conceptual foundation. Students who master these slides will find Part 8 implementation much easier because they'll understand the "why" behind each design decision.

---

**End of Slideshow Document**

