# Agentic Coding Tools: A Student Guide
## Slideshow Outline

---

# Part 1: Introduction & Installation

## Slide 1: What Are Agentic Coding Tools?
- Beyond autocomplete: AI that **plans, executes, debugs, and iterates**
- Three categories:
  - **Terminal-based agents** (CLI tools) ← Main Focus
  - **Agentic IDEs** (standalone editors)
  - **VS Code plugins** (extensions)
- Shift from suggestion-based → truly autonomous workflows

## Slide 2: The Three Categories Overview

### Terminal-Based Agents (Primary Focus)
| Tool | Provider | Key Feature |
|------|----------|-------------|
| Claude Code | Anthropic | Multi-agent parallelization (up to 10) |
| Aider | Open Source | Git-first, architect/editor modes |
| Codex CLI | OpenAI | Reasoning models (o1, o3-mini) |
| Gemini CLI | Google | 1M token context, free tier |
| GitHub Copilot CLI | GitHub | 4 specialized agents |

### Agentic IDEs
| Tool | Key Feature |
|------|-------------|
| Cursor | 8 parallel agents, background agents |
| Windsurf | Cascade engine, best value ($15/mo) |
| Zed | Privacy-focused, bring-your-own-key |

### VS Code Plugins
| Tool | Key Feature |
|------|-------------|
| GitHub Copilot | Agent mode, self-healing |
| Cline | Open source, 500+ models |
| Continue | MCP integration, free |

---

# Part 2: Installation Procedures

## Slide 3: Terminal-Based Agents Installation

### Claude Code CLI (Recommended)
```bash
# macOS/Linux (Native - Recommended)
curl -fsSL https://claude.ai/install.sh | bash

# Windows PowerShell
irm https://claude.ai/install.ps1 | iex

# Requirements: Node.js 18+, Claude subscription
```

### Aider
```bash
# Recommended installation
python -m pip install aider-install
aider-install

# Usage
cd /path/to/your/codebase
aider --model sonnet --api-key anthropic=<key>
```

### Gemini CLI
```bash
# Free with Google account
# 60 req/min, 1000/day, 1M token context
# Installation from Google documentation
```

### Codex CLI
```bash
npm i -g @openai/codex
# or
brew install --cask codex
```

## Slide 4: Agentic IDEs Installation

### Cursor
- Download from cursor.com
- macOS: Drag to Applications
- Windows: Run installer
- Linux: AppImage (make executable)

### Windsurf
- Download from windsurf.com
- Import VS Code settings
- Sign in to Codeium account

## Slide 5: VS Code Plugins Installation

### GitHub Copilot
1. Open Extensions (`Ctrl/Cmd+Shift+X`)
2. Search "GitHub Copilot"
3. Install and authenticate with GitHub

### Cline
1. Extensions → Search "Cline"
2. Install → Configure API provider
3. Click robot icon in Activity Bar

### Continue
1. Extensions → Search "Continue"
2. Install → Configure model provider
3. Free for solo developers

---

# Part 3: Basic Usage

## Slide 6: Core Capabilities Overview
1. **Code Generation & Editing**
2. **File Management**
3. **Writing & Documentation**
4. **Codebase Research/Search**
5. **Online Research**
6. **Git Workflows**

## Slide 7: Code Generation & Editing

### Terminal Agents (Claude Code example)
```
> Create a function that validates email addresses
> Refactor this class to use dependency injection
> Fix the bug in the authentication middleware
```

### IDEs (Cursor example)
- `Ctrl+K` - Targeted AI edits
- `Tab` - Autocomplete
- Composer for multi-file refactoring

### VS Code (Copilot)
- Natural language comments trigger generation
- Agent mode for autonomous multi-file edits

## Slide 8: File Management

### Terminal Agents
- Read, create, edit, delete files via natural language
- Automatic Git integration (commits, branches)
- Custom commands stored in `.claude/commands/`

### IDEs
- Multi-file operations with codebase understanding
- Automatic commit message generation
- Branch management

### VS Code Plugins
- Permission-based file operations
- Integrated with VS Code file system

## Slide 9: Writing & Documentation

### Capabilities
- Generate documentation from code
- Create README files
- Write inline comments
- Generate API documentation

### Example (Claude Code)
```
> Document all public methods in src/api/
> Create a getting-started guide for this project
> Explain what this function does and add a docstring
```

## Slide 10: Codebase Research & Search

### Terminal Agents
- Semantic search across entire codebase
- Understand architecture and relationships
- Map dependencies automatically

### Example Queries
```
> How does authentication work in this codebase?
> Find all API endpoints that access the database
> What components depend on the UserService?
```

### Aider's Repository Map
- Graph-based analysis of codebase structure
- Identifies most relevant files for current task
- Optimizes context window usage

## Slide 11: Online Research

### Built-in Capabilities
- Web search for documentation
- Fetch content from URLs
- Research solutions to problems

### MCP Integration (Model Context Protocol)
- Connect to external tools and data sources
- Supported by: Claude Code, Codex CLI, Cursor CLI, Goose

### Example
```
> Search for the latest React 19 migration guide
> Find best practices for PostgreSQL indexing
```

## Slide 12: Git Workflows

### Automatic Integration
- Stage and commit changes
- Generate descriptive commit messages
- Create branches and PRs
- Review changes before applying

### Example (Claude Code)
```
> Commit these changes with a descriptive message
> Create a PR for this feature branch
> Show me what changed in the last 3 commits
```

---

# Part 4: Planning → Building Workflow

## Slide 13: The Research-Plan-Implement Pattern

### The Problem
Without planning steps, agents jump straight to coding → often wrong approach

### The Solution: Three Phases
```
1. RESEARCH → Understand the problem
2. PLAN → Design the solution
3. IMPLEMENT → Write the code
```

### Why It Works
- Reduces hallucinations
- Catches issues early
- Produces better solutions
- Matches how humans work

## Slide 14: Plan Mode in Action

### Claude Code Plan Mode
```
> /plan Implement user authentication with JWT
```
Agent will:
1. Explore codebase for existing auth patterns
2. Identify dependencies needed
3. Design architecture
4. Present plan for approval
5. Execute only after confirmation

### Cursor Plan Mode
```
/plan  or  --mode=plan
```
- Asks clarifying questions
- Designs approach before coding

## Slide 15: The Plan-Act-Reflect Framework

```
┌─────────┐
│  PLAN   │ ← Define what needs to be done
└────┬────┘
     ↓
┌─────────┐
│   ACT   │ ← Execute the plan
└────┬────┘
     ↓
┌─────────┐
│ REFLECT │ ← Review results, iterate
└────┬────┘
     ↓
  (Loop back to PLAN if needed)
```

### Benefits
- Prevents runaway logic
- Improves collaboration
- Catches errors early

## Slide 16: Static vs Dynamic Decomposition

### Static Decomposition
- Plan everything upfront
- Use when: Solution is known
- Pro: Faster execution
- Con: Requires certainty

### Dynamic Decomposition
- Plan as you go
- Use when: Solution is unclear
- Pro: Better discovery
- Con: Higher token cost

### Recommendation
Start with planning, switch to dynamic for exploration tasks

---

# Part 5: Two-Layer Agent Work

## Slide 17: The Two-Layer Pattern

```
┌─────────────────────────────────────┐
│         ORCHESTRATOR AGENT          │
│   (Plans, coordinates, synthesizes) │
└─────────────────┬───────────────────┘
                  │
         ┌────────┴────────┐
         ↓                 ↓
┌─────────────┐     ┌─────────────┐
│   TASK 1    │     │   TASK 2    │
│ (Subagent)  │     │ (Subagent)  │
└─────────────┘     └─────────────┘
```

### Workflow
1. **Plan** - Orchestrator breaks down the problem
2. **Build** - Orchestrator assigns subtasks
3. **Split into Tasks** - Subagents execute independently
4. **Synthesize** - Orchestrator combines results

## Slide 18: Task vs Subagent Distinction

### Tasks (Ephemeral Workers)
- One-time, isolated jobs
- Best for: Parallel search, reading many files
- Example: "Search all 1,000 files for database connections"

### Subagents (Persistent Specialists)
- Specialized expertise
- Longer-running work
- Example: Security scanner, code reviewer, test analyzer

## Slide 19: Practical Example - Code Review

### Traditional Single-Agent
```
> Review this PR for issues
```
Takes: ~5 minutes, limited perspective

### Two-Layer Multi-Agent
```
> Review this PR using parallel specialist agents
```

**Orchestrator spawns:**
- Security Auditor → Checks vulnerabilities
- Style Enforcer → Validates formatting
- Performance Analyst → Finds bottlenecks
- Test Coverage → Analyzes test completeness

**Result:** Minutes → Seconds, comprehensive review

## Slide 20: Claude Code Task Tool Syntax

```
Prompt: "Run 4 agents in parallel to explore
different directories of the codebase"
```

### What Happens
1. Claude spawns 4 subagents
2. Each gets 200k context window
3. They run simultaneously
4. Results summarized back to main agent

### Constraints
- Max 10 concurrent agents
- ~20k token overhead per agent
- Must be **explicit** about parallelization

---

# Part 6: Multi-Tier Agent Architecture

## Slide 21: Three-Tier Agent Hierarchy

```
┌─────────────────────────────────────┐
│          STRATEGY LAYER             │
│   (High-level goals, replanning)    │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│          PLANNING LAYER             │
│ (Task decomposition, dependencies)  │
└─────────────────┬───────────────────┘
                  ↓
┌─────────────────────────────────────┐
│         EXECUTION LAYER             │
│   (Implementation, tool usage)      │
└─────────────────────────────────────┘
```

## Slide 22: Specialized Agents in the Hierarchy

### GitHub Copilot CLI's Four Agents
1. **Explore Agent** - Codebase analysis
2. **Task Agent** - Command execution
3. **Plan Agent** - Implementation planning
4. **Code-Review Agent** - Modification evaluation

### Aider's Architect/Editor Model
1. **Architect** (Reasoning model - o1) → High-level solution
2. **Editor** (Fast model - Sonnet) → Specific file edits

## Slide 23: Agents Calling Agents

### OpenHands Hierarchical Delegation
```
Main Agent
    │
    ├──→ SubAgent A (inherits workspace)
    │         │
    │         └──→ SubAgent A1
    │
    └──→ SubAgent B (independent context)
```

### Key Points
- Sub-agents inherit parent's model configuration
- Each has independent conversation context
- Results consolidated by parent
- Enables structured parallelism

## Slide 24: Five-Phase Workflow

```
1. PLANNING      → Orchestrator creates task breakdown
        ↓
2. DELEGATION    → Assign tasks to specialist agents
        ↓
3. EXECUTION     → Sub-agents work independently
        ↓
4. SYNTHESIS     → Combine and resolve conflicts
        ↓
5. ITERATION     → Dynamic replanning if needed
```

## Slide 25: Claude Code Subagent Limitation

### Important: No Nested Subagents
```
Main Agent
    │
    └──→ SubAgent (can NOT spawn more agents)
```

**Why?** Prevents infinite nesting, maintains control

**Workaround:** Use orchestrator pattern with explicit task delegation

---

# Part 7: Parallelization with Agents

## Slide 26: Why Parallelization Matters

### Performance Gains
- Content workflow: **36% faster** (6:10 → 3:56)
- Code review: **Minutes → Seconds**
- Quality: **90.2% improvement** over single agent

### Trade-off
- 15× more tokens consumed
- Coordination overhead
- More complex debugging

## Slide 27: Parallelization Patterns

### Pattern 1: Research & Literature Review
```
PARALLEL:
├── Agent 1: Explore codebase implementations
├── Agent 2: WebSearch for papers/docs
└── Agent 3: Identify design patterns
```

### Pattern 2: Code Analysis & Debugging
```
PARALLEL:
├── Agent 1: Trace data flow
├── Agent 2: Search for similar bugs
└── Agent 3: Check docs and tests
```

### Pattern 3: Build & Test
```
PARALLEL:
├── Tests running
├── Documentation building
└── Linting/formatting
```

## Slide 28: Explicit Parallel Requests

### Claude Code Requires Explicit Instructions
```
# DON'T
> Explore the codebase

# DO
> Run 4 agents IN PARALLEL to explore:
  - Agent 1: src/api directory
  - Agent 2: src/components directory
  - Agent 3: src/utils directory
  - Agent 4: tests directory
```

### Key Phrases
- "Run in parallel"
- "Simultaneously"
- "Concurrently"
- "At the same time"

## Slide 29: Background Tasks

### `run_in_background: true`
```
Use for:
- Long-running builds
- Large file searches
- Comprehensive test suites
- API documentation generation
```

### Benefits
- Orchestrator continues other work
- No blocking on slow tasks
- Better resource utilization

## Slide 30: Parallelization Best Practices

1. **Independence** - Only parallelize tasks with NO dependencies
2. **Specificity** - Give each agent a clear, focused objective
3. **Background tasks** - Use for long-running operations
4. **Explicit requests** - Say "run in parallel" explicitly
5. **Collect and synthesize** - Combine results after completion
6. **Monitor token usage** - Parallelization is expensive

---

# Part 8: Agent Definition

## Slide 31: What IS an Agent?

### Definition
An **agent** is an AI system that:
- **Plans** its approach to a problem
- **Acts** using tools and APIs
- **Observes** results
- **Adapts** based on feedback
- Operates with **autonomy** toward a goal

### vs Traditional AI Assistants
| Traditional | Agentic |
|-------------|---------|
| Responds to prompts | Pursues goals |
| Single turn | Multi-turn loops |
| No tool use | Uses tools |
| No memory | Maintains context |

## Slide 32: Core Agent Components

```
┌─────────────────────────────────────┐
│              AGENT                  │
├─────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  │
│  │    LLM      │  │   MEMORY     │  │
│  │  (Brain)    │  │  (Context)   │  │
│  └─────────────┘  └──────────────┘  │
│  ┌─────────────┐  ┌──────────────┐  │
│  │   TOOLS     │  │  PLANNING    │  │
│  │ (Actions)   │  │  (Strategy)  │  │
│  └─────────────┘  └──────────────┘  │
└─────────────────────────────────────┘
```

### Components
- **LLM** - The reasoning engine
- **Memory** - Context window + persistent storage
- **Tools** - File I/O, bash, web, APIs
- **Planning** - Task decomposition and strategy

## Slide 33: The ReAct Loop

```
┌──────────────────────────────────────┐
│                                      │
│   ┌─────────┐                        │
│   │ REASON  │ ← Think about the task │
│   └────┬────┘                        │
│        ↓                             │
│   ┌─────────┐                        │
│   │   ACT   │ ← Use a tool           │
│   └────┬────┘                        │
│        ↓                             │
│   ┌─────────┐                        │
│   │ OBSERVE │ ← See the result       │
│   └────┬────┘                        │
│        │                             │
│        └──────────→ (Loop)           │
│                                      │
└──────────────────────────────────────┘
```

Used by: Gemini CLI, OpenHands, most agentic tools

## Slide 34: Agent Specialization

### Generalist vs Specialist Agents

**Generalist**
- Handles any task
- Broader context needed
- Lower specific expertise

**Specialist**
- Focused on one domain
- Smaller, optimized prompts
- Higher expertise in domain

### Common Specialist Types
- **Explorer** - Codebase analysis (often uses smaller, faster models)
- **Coder** - Implementation
- **Reviewer** - Quality checks
- **Tester** - Test generation
- **Security** - Vulnerability scanning

## Slide 35: Agent Context Windows

### Claude Code Context Architecture
```
Main Agent: 200k tokens
    │
    ├── SubAgent 1: 200k tokens (isolated)
    ├── SubAgent 2: 200k tokens (isolated)
    └── SubAgent 3: 200k tokens (isolated)
```

### Key Points
- Each agent has **independent** context
- ~20k token overhead before work begins
- Results **summarized** back (not full context)
- Enables handling of massive codebases

### Gemini CLI
- **1 million token** context window
- Can load extremely large codebases
- Free tier with Google account

## Slide 36: Agent Autonomy Levels

### Spectrum of Control
```
LOW AUTONOMY ←────────────────────→ HIGH AUTONOMY
     │                                    │
Read-Only    Confirm    Auto-Accept    Fire-and-
 Mode        Each         with          Forget
             Action      Review
```

### Claude Code Modes
- **Plan Mode** - Research and design only
- **Auto Mode** - Execute without confirmation

### Codex CLI Approval Modes
- **Read-Only** - Browse only, no changes
- **Standard** - Confirm before executing
- **Full Access** - Work without asking

---

# Part 9: Summary & Best Practices

## Slide 37: Tool Selection Guide

### Choose Terminal Agents When:
- You live in the command line
- Need maximum control
- Want scriptable automation
- Prefer text-based interaction

### Choose Agentic IDEs When:
- Visual feedback is important
- GUI-based workflow preferred
- Want integrated debugging
- Need real-time collaboration

### Choose VS Code Plugins When:
- Already use VS Code
- Want lightweight integration
- Don't need full autonomy
- Budget-conscious

## Slide 38: Key Takeaways

1. **Planning beats jumping to code** - Research → Plan → Implement
2. **Multi-agent beats single agent** - Specialize for better results
3. **Parallelization is powerful** - But requires explicit instructions
4. **Context is finite** - Use subagents to isolate and expand
5. **Start simple, scale gradually** - Build trust before autonomy

## Slide 39: Recommended Workflow

```
1. Start with single agent
        ↓
2. Add planning phase
        ↓
3. Introduce one specialist
        ↓
4. Validate performance
        ↓
5. Add more specialists
        ↓
6. Enable parallelization
        ↓
7. Scale to multi-tier
```

## Slide 40: Resources & Further Learning

### Documentation
- Claude Code: code.claude.com/docs
- Aider: aider.chat
- Cursor: cursor.com/docs
- Gemini CLI: developers.google.com/gemini-code-assist

### Key Concepts to Explore
- Model Context Protocol (MCP)
- ReAct and ReWOO patterns
- PEER pattern (Plan, Execute, Express, Review)
- Hierarchical Multi-Agent Systems (HMAS)

---

# Appendix: Quick Reference

## Terminal Agent Commands

### Claude Code
```bash
claude                    # Start interactive
claude "task"            # One-shot task
/plan                    # Enter plan mode
Ctrl+B                   # Background subagent
/compact                 # Compress context
```

### Aider
```bash
aider                    # Start in repo
/code                    # Code editing mode
/architect               # Planning mode
/ask                     # Discussion mode
```

### Codex CLI
```bash
codex                    # Interactive mode
codex exec "task"        # Non-interactive
/model                   # Switch models
/approvals               # Change approval level
```

## Parallelization Prompt Templates

### Research Pattern
```
Run the following agents IN PARALLEL:
1. Search codebase for [pattern]
2. Find documentation about [topic]
3. Identify existing implementations of [feature]
```

### Code Review Pattern
```
Run these specialist agents SIMULTANEOUSLY:
1. Security auditor: check for vulnerabilities
2. Style enforcer: validate formatting
3. Performance analyst: identify bottlenecks
4. Test coverage: analyze test completeness
```

### Feature Implementation Pattern
```
Execute these phases:
PARALLEL PHASE 1 (Research):
- Agent A: Search for similar implementations
- Agent B: Review documentation
- Agent C: Identify dependencies

SEQUENTIAL PHASE 2 (Planning):
- Synthesize findings and create plan

PARALLEL PHASE 3 (Implementation):
- Agent 1: Core logic
- Agent 2: Tests
- Agent 3: Documentation
```
