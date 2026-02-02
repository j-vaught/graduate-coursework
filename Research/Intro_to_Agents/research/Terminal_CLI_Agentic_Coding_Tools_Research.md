# Terminal/CLI-Based Agentic Coding Tools: Comprehensive Research Summary

**Research Date**: January 2026
**Primary Focus**: Claude Code CLI and competing terminal-based AI coding agents

---

## Table of Contents

1. [Overview & Market Landscape](#overview--market-landscape)
2. [Claude Code CLI (Primary Focus)](#claude-code-cli-primary-focus)
3. [Aider](#aider)
4. [OpenHands](#openhands)
5. [Codex CLI (OpenAI)](#codex-cli-openai)
6. [GitHub Copilot CLI](#github-copilot-cli)
7. [Gemini CLI (Google)](#gemini-cli-google)
8. [Continue CLI](#continue-cli)
9. [Cursor CLI](#cursor-cli)
10. [Cline](#cline)
11. [Goose](#goose)
12. [Devin CLI (Cognition Labs)](#devin-cli-cognition-labs)
13. [Benchmarks & Performance Comparison](#benchmarks--performance-comparison)
14. [Best Practices & Workflows](#best-practices--workflows)
15. [Context Management & Token Optimization](#context-management--token-optimization)
16. [Key Trends in 2026](#key-trends-in-2026)

---

## Overview & Market Landscape

### What Are Agentic CLI Coding Tools?

Agentic CLI tools are AI-powered command-line agents that go beyond simple autocomplete, actively planning and executing multi-step tasks while managing files, running commands, and handling Git history directly within the terminal. CLI coding agents in 2026 represent a shift from suggestion-based assistance to truly agentic workflows that plan, act, and adapt while staying rooted in the terminal.

### Market Position

Developer consensus has largely settled on one point: there is no single "best" AI coding agent in isolation, as developers evaluate based on where they want leverage: speed and flow inside the editor, control and reliability on large codebases, or greater autonomy higher up the stack. Most CLI coding agents in 2026 are open-source or low-cost, democratizing access to advanced AI-assisted development.

---

## Claude Code CLI (Primary Focus)

### Overview

Claude Code is an agentic coding tool developed by Anthropic that lives in your terminal, understands your codebase, and helps you code faster by executing routine tasks, explaining complex code, and handling git workflows—all through natural language commands. Originally built to support developer productivity at Anthropic, it has become far more than a coding tool, being used for deep research, video creation, and note-taking, among countless other non-coding applications.

### Installation and Setup

#### Native Binary Installation (Recommended)
```bash
# macOS/Linux
curl -fsSL https://claude.ai/install.sh | bash

# Windows
irm https://claude.ai/install.ps1 | iex
```

#### NPM Installation (Deprecated but Available)
```bash
# Global installation
npm install -g @anthropic-ai/claude-code

# Migration from npm to native
claude install
```

#### Requirements
- Node.js 18+ (for npm installation)
- Minimum 4GB RAM recommended
- Active internet connection
- Anthropic API key (from Anthropic Console)
- Claude subscription (Pro, Max, Teams, or Enterprise) or Claude Console account

**Note**: NPM installation is deprecated. Anthropic recommends using the native binary installation to avoid package manager conflicts.

### Key Commands and Workflows

#### Planning vs Execution Modes
Claude Code's greatest superpower is its workflow: first, it plans, then it acts. Without research and planning steps, Claude tends to jump straight to coding a solution, but asking Claude to research and plan first significantly improves performance for problems requiring deeper thinking upfront.

#### Command Structure
- Natural language interface - describe what you want to accomplish
- Slash commands for specific operations (stored in `.claude/commands` folder)
- Custom commands can be created as Markdown files and checked into git for team access

### Agent/Task Spawning Capabilities

#### Built-in Subagents

Claude Code includes several specialized subagents, each running in its own context window with custom system prompts, specific tool access, and independent permissions:

1. **Explore Subagent**: Fast, read-only agent optimized for searching and analyzing codebases, used for file discovery, code search, and codebase exploration (powered by Haiku)
2. **Plan Subagent**: Used for codebase research when in plan mode and Claude needs to understand your codebase
3. **General-Purpose Subagent**: Used for complex research, multi-step operations, and code modifications

#### Custom Subagents
You can create custom subagents with specialized prompts and tool access tailored to specific tasks or workflows.

### Multi-Agent and Parallelization Features

#### Parallel Task Execution
Claude Code supports running multiple subagents in parallel. You can launch parallel tasks with prompts like: "Explore the codebase using 4 tasks in parallel. Each agent should explore different directories."

#### Constraints and Limitations
- **Parallelism Cap**: The parallelism level is capped at 10 agents
- **Batch Execution**: When providing a parallelism level, Claude Code executes tasks in parallel but in batches, waiting until all tasks in the current batch complete before starting the next batch
- **No Nested Subagents**: Subagents cannot spawn other subagents, preventing infinite nesting while still gathering necessary context

#### Swarming (2026 Enhancement)
Anthropic engineers mentioned plans to enhance "Swarming" (orchestrated multi-agent execution) in 2026. Familiarizing yourself with parallel execution patterns now will prepare developers for these enhanced capabilities.

### Planning Modes vs Execution Modes

#### Plan Mode
- Claude automatically uses the Explore Subagent when researching in Plan Mode
- Haiku-powered specialist efficiently searches your codebase while saving context tokens
- Automatic delegation happens when you need comprehensive code exploration

#### Execution Mode
- Direct file editing, terminal command execution
- Git workflow management (commits, branches, PRs)
- Automatic testing and linting integration

### Context and Codebase Understanding

#### Context Management Strategies
- **Sub-agents**: Isolate specific research or exploration tasks
- **Scratchpad**: Temporary workspace for intermediate computations
- **Compaction**: Automatic compression of conversation history when approaching token limits
- **Explore Subagent**: Offloads codebase analysis to save main conversation context

#### Codebase Analysis
- Understands large and complex codebases in a single session
- Maintains relationships between files and dependencies
- Provides architectural discussions and deep debugging support
- Supports careful refactoring across multiple files

### Strengths and Use Cases

- Advanced reasoning capabilities
- Excellent for understanding intent and explaining why a particular solution makes sense
- Handles complex multi-file operations
- Strong at research-plan-implement workflows
- Integrates seamlessly with Git workflows
- Performs spectacularly well for virtually any task

### Model Information

- Powered by Claude Opus 4.5 (model ID: claude-opus-4-5-20251101) and Sonnet 4.5
- Latest version as of January 2026: 2.1.12
- Receives regular updates with new features and improvements

---

## Aider

### Overview

Aider is an open-source AI pair programming tool that operates directly from your terminal, working seamlessly with your existing git repositories without requiring any IDE plugins or browser tabs. It's a Git-first CLI coding agent designed for developers who live inside version control.

### Installation and Setup

```bash
# Recommended installation (creates isolated environment)
python -m pip install aider-install
aider-install

# Alternative: Using uv
python -m pip install uv
uv tool install --force --python python3.12 --with pip aider-chat@latest

# Docker
docker pull paulgauthier/aider

# Basic usage
cd /path/to/your/codebase
aider --model deepseek --api-key deepseek=<key>
aider --model sonnet --api-key anthropic=<key>
```

#### Requirements
- Python 3.12+ (aider-install will install if needed)
- Git repository
- API key for chosen LLM provider

### Key Commands and Workflows

#### Chat Modes
Switch between different modes using slash commands:
- `/code` - Code editing mode (default)
- `/architect` - High-level planning mode with two-model approach
- `/ask` - Discussion mode without file editing
- `/help` - Help mode
- `/chat-mode <mode>` - Switch to any mode

#### Recommended Workflow
Bounce back and forth between `/ask` and `/code` modes:
1. Use ask mode to discuss what you want to do and get suggestions
2. Switch to code mode to have aider start editing your files

### Agent/Task Spawning Capabilities

#### Architect Mode
In architect mode, aider sends requests to two models:
1. **Main Model (Architect)**: Proposes solutions at a high level (excellent with OpenAI o1 models)
2. **Editor Model**: Turns the architect's proposal into specific file editing instructions (e.g., GPT-4o or Sonnet)

This two-stage approach pairs models that are strong at reasoning but less capable at editing with models that excel at code manipulation.

#### Shortcuts
- `--architect`: Launch directly in architect mode
- `--auto-accept-architect`: Enable/disable automatic acceptance of architect changes (default is True)

**Note**: No explicit "lazy mode" exists. References to "lazy coding" refer to a historical problem with GPT-4 Turbo eliding code sections, not a feature.

### Multi-Agent and Parallelization Features

Aider primarily operates as a single-agent system with the architect/editor split being the main form of task delegation. While it doesn't have explicit multi-agent parallelization like Claude Code's subagents, the architect mode provides a form of specialized task delegation.

### Planning Modes vs Execution Modes

#### Planning (Architect Mode)
- High-level solution design
- Reasoning-focused models (o1, o3-mini) excel here
- Produces implementation plans

#### Execution (Code Mode)
- Direct file editing with specific edit formats
- Automatic git commits with descriptive messages
- Integration with linters and test suites

### Context and Codebase Understanding

#### Repository Map (Repo-Map)
Aider's key innovation for codebase understanding:

- **Concise Map**: Creates a map of your whole git repository including the most important classes and functions with their types and call signatures
- **Graph Ranking Algorithm**: Analyzes the full repo map using a graph where each source file is a node and edges connect files with dependencies
- **Smart Selection**: Identifies and maps the portions most relevant to the current chat state, optimizing what fits into the active token budget
- **Tree-sitter Based**: Uses tree-sitter (not ctags) to build the repository map, providing better accuracy

This helps aider:
- Understand code it's editing and how it relates to other parts
- Write new code that respects and utilizes existing libraries, modules, and abstractions
- Work well in larger projects with multi-file refactoring

### Strengths and Use Cases

- **Git Integration**: Automatic commits with sensible commit messages
- **Multi-file Coordination**: Makes coordinated changes across multiple files
- **Language Support**: Works with most popular programming languages (Python, JavaScript, Rust, Ruby, Go, C++, PHP, HTML, CSS, and dozens more)
- **LLM Flexibility**: Works best with Claude 3.7 Sonnet, DeepSeek R1 & Chat V3, OpenAI o1, o3-mini & GPT-4o, but can connect to almost any LLM
- **Local Models**: Supports local models via Ollama for privacy-focused workflows
- **Testing Integration**: Automatically lint and test code every time changes are made; can fix problems detected by linters and test suites
- **Multimodal**: Add images and web pages to chat for visual context, screenshots, reference docs
- **Voice Commands**: Speak directly to Aider to request features, tests, or bug fixes

### Additional Features

- **Edit Formats**: Multiple edit format strategies optimized for different models
- **YAML Configuration**: Extensive configuration via `.aider.conf.yml` files
- **Version Control**: Easy to diff, manage, and undo AI changes using familiar git tools

---

## OpenHands

### Overview

OpenHands (formerly OpenDevin) is a fully open-source platform that uses AI agents to act like a developer. The platform recently announced the OpenHands CLI, bringing the full power of OpenHands development agents directly from the command line with no Docker required.

### Installation and Setup

```bash
# Requires Python 3.12 or 3.13
# No Docker or web interface needed for CLI

# Installation details available from OpenHands documentation
```

#### Requirements
- Python 3.12 or 3.13
- No Docker required for CLI (unlike web version)
- LLM API key (supports multiple providers)

### Key Commands and Workflows

OpenHands CLI provides the easiest way to start using OpenHands development agents, with common capabilities including:
- Creating and modifying files
- Fixing bugs
- Refactoring code
- Running tests or linters directly from the terminal

You can give tasks to OpenHands agents using a website, command line, or by writing scripts.

### Agent/Task Spawning Capabilities

#### Sub-Agent Delegation
OpenHands enables parallel task execution by delegating work to multiple sub-agents that run independently and return consolidated results. Agent delegation allows a main agent to spawn multiple sub-agents for parallel processing.

#### AgentDelegateAction
OpenHands uses a special action type called `AgentDelegateAction`, which enables an agent to delegate a specific subtask to another agent.

### Multi-Agent and Parallelization Features

#### Hierarchical Agent Coordination
- The SDK supports hierarchical agent coordination through a delegation tool
- Sub-agents operate as independent conversations that inherit the parent's model configuration and workspace context
- Enables structured parallelism and isolation without any changes to the core SDK

#### Multi-Agent System Features
- Hierarchical agent structures where agents can delegate subtasks to other agents
- Built-in delegation primitives
- Standardized vocabulary for agent roles and capabilities
- Each sub-agent runs independently with its own conversation context
- Main agent consolidates and processes results from sub-agents

### Planning Modes vs Execution Modes

OpenHands agents use a reason and act (ReAct) loop to complete complex use cases. The platform supports different agent types that can be specialized for planning or execution tasks.

### Context and Codebase Understanding

- Agents have access to full codebase context
- Sub-agents inherit parent's workspace context
- Can change code, run computer commands, find and fix bugs, and write documentation
- Built on a modular SDK architecture (OpenHands Software Agent SDK)

### Strengths and Use Cases

- **Open Source**: Fully open source under Apache 2.0-style license, no vendor lock-in
- **Model Agnostic**: Can use Claude, GPT, or any other LLM
- **Multi-Platform**: Available as CLI, web interface, and SDK for custom integrations
- **Research-Backed**: Published as a conference paper at ICLR 2025
- **Toad Integration**: Sponsor of Toad development (universal terminal interface for AI agents), included as recommended agent in Toad's agent store

### Integration with Ecosystem

OpenHands partners with Toad (a universal terminal interface for AI agents) and is included as a recommended agent in Toad's agent store, showing strong ecosystem integration.

---

## Codex CLI (OpenAI)

### Overview

Codex CLI is OpenAI's coding agent that runs locally from your terminal. It can read, change, and run code on your machine in the selected directory. Built in Rust for speed and efficiency, it's open source and included in ChatGPT Plus, Pro, Business, Enterprise, and Edu subscriptions.

### Installation and Setup

```bash
# NPM installation
npm i -g @openai/codex

# Homebrew installation
brew install --cask codex
```

#### Requirements
- ChatGPT Plus, Pro, Business, Enterprise, or Edu subscription
- Node.js (for npm installation)

### Key Commands and Workflows

#### Model Selection
- `/model` - Switch between GPT-5-Codex and GPT-5, or adjust reasoning levels
- Default model support includes GPT-5-Codex, GPT-5, and reasoning models (o1, o3-mini, o4-mini)

#### Interactive Terminal UI
Codex launches into a full-screen terminal UI that can:
- Read your repository
- Make edits
- Run commands as you iterate together

### Agent/Task Spawning Capabilities

#### Agent Collaboration (2026 Enhancement)
Collaboration tools gained richer agent control:
- `spawn_agent`: Accepts an agent role preset for specialized tasks
- `send_input`: Can optionally interrupt a running agent before delivering the message
- Represents significant progress in multi-agent capabilities within Codex

#### Agent Skills
Codex now supports agent skills: reusable bundles of instructions that help Codex reliably complete specific tasks:
- Available in both Codex CLI and IDE extensions
- Can be invoked explicitly by typing `$skill-name`
- Can be selected automatically by Codex
- `$create-plan` skill is experimental and needs to be installed

### Multi-Agent and Parallelization Features

While specific multi-agent parallelization features are not as extensive as Claude Code or OpenHands, the agent collaboration enhancements in 2026 show movement toward richer multi-agent capabilities.

### Planning Modes vs Execution Modes

#### Read-Only Mode (Planning/Consulting)
- Keeps Codex in a consultative mode where it can browse files
- Won't make changes or run commands until you approve a plan
- Switch using `/approvals` command
- Recommended for planning or consulting without making changes

#### Approval Modes
Different levels of control over Codex's actions:
- **Read-Only**: Browse and plan without changes
- **Standard**: Confirm before executing changes
- **Full Access**: Work across your machine including network access without asking (use sparingly, only with trusted repos)

#### Exec Subcommand (Non-Interactive)
```bash
# Automate workflows or wire Codex into existing scripts
codex exec "task description"
```
Runs Codex non-interactively, piping the final plan and results back to stdout.

### Context and Codebase Understanding

- Reads and understands repository structure
- Can access and comprehend documentation
- Reasoning engine for complex problem-solving
- Long-term planning capability

### Strengths and Use Cases

#### Key Features
- **Model Context Protocol (MCP)**: Give Codex access to additional third-party tools and context
- **Web Search**: Search the web and get up-to-date information for tasks
- **Code Review**: Separate Codex agent reviews code before commit or push
- **Cloud Tasks**: Launch Codex Cloud task, choose environments, and apply resulting diffs without leaving terminal
- **Terminal Integration**: Watch commands being executed and view output logs

#### Recent Launch Impact
Launched in December 2025/January 2026 as a lightweight open-source coding agent that brings the power of models like o3 and o4-mini into local workflows, making it easy to pair with them to complete tasks faster.

---

## GitHub Copilot CLI

### Overview

GitHub Copilot CLI brings the power of Copilot coding agent directly to your terminal, allowing you to work locally and synchronously with an AI agent that understands your code and GitHub context.

### Installation and Setup

```bash
# NPM installation
npm install -g @github/copilot

# Authenticate using existing GitHub credentials
```

#### Requirements
- GitHub account
- GitHub Copilot subscription
- Supports macOS, Linux, and Windows (via WSL)

### Key Commands and Workflows

#### Model Selection
- `/model` - Choose from available models
- Default: Claude Sonnet 4.5
- Options include Claude Sonnet 4 and GPT-5

#### Context Management Commands
- `/compact` - Manual compression of conversation history
- `/context` - Visualize current token usage
- `--resume` - Tab completion to cycle through sessions
- `/cwd` - Change working directory (with tab completion)
- `/add-dir` - Add directory to context (with tab completion)

#### Specialized Agent Delegation
Copilot automatically delegates to four custom agents:
1. **Explore Agent**: Codebase analysis without cluttering main conversation context
2. **Task Agent**: Runs commands with brief summaries
3. **Plan Agent**: Creates complex implementation plans
4. **Code-Review Agent**: Evaluates modifications

### Agent/Task Spawning Capabilities

GitHub Copilot CLI's specialized custom agents represent automatic task delegation. When you ask Copilot to perform certain tasks, it automatically delegates to the appropriate specialized agent based on the request type.

### Multi-Agent and Parallelization Features

The four specialized agents work independently, with Copilot acting as an orchestrator that delegates tasks to the appropriate agent. While not explicitly parallel in user control, the system internally manages which agent handles which task.

### Planning Modes vs Execution Modes

#### Plan Agent
Dedicated agent for creating complex implementation plans before execution.

#### Execution
Task agent handles command execution with summaries, while code changes are managed by the main Copilot agent or delegated to appropriate specialists.

### Context and Codebase Understanding

#### Auto-Compaction
When approaching 95% of the token limit, Copilot automatically compresses conversation history, preventing context overflow that would otherwise terminate sessions.

#### Context Visualization
The `/context` command lets you visualize current token usage, helping you understand how much context window is remaining.

#### Session Management
The `--resume` flag with tab completion allows cycling through previous sessions, maintaining continuity across work sessions.

### Strengths and Use Cases

#### Recent Updates (January 2026)
- **Intra-line Syntax Highlighting**: Shows exactly what changed, integrates with Git's configured pager
- **Web Fetch Tool**: Retrieves content from URLs as markdown, with URL access controlled through `~/.copilot/config` with `allowed_urls` and `denied_urls` patterns
- **Enhanced Tab Completion**: Autocompletes paths in `/cwd` and `/add-dir`
- **Reasoning Visibility**: Ctrl+T toggles model reasoning visibility in supported models

#### Integration Benefits
- Deep GitHub integration (understands GitHub context)
- Automatic agent specialization
- Professional support through GitHub
- Regular updates and improvements

---

## Gemini CLI (Google)

### Overview

Gemini CLI is Google's open-source AI agent that brings the power of Gemini directly into your terminal. It's fully open source under the Apache 2.0 license, allowing developers to inspect the code and contribute to the project.

### Installation and Setup

```bash
# Installation details from Google documentation
# Requires Python 3.12 or 3.13
```

#### Requirements
- Python 3.12 or 3.13
- Google account (personal account provides free tier)

### Key Commands and Workflows

#### ReAct Loop
Gemini CLI uses a reason and act (ReAct) loop with built-in tools and local or remote MCP servers to complete complex use cases like:
- Fixing bugs
- Creating new features
- Improving test coverage

### Agent/Task Spawning Capabilities

Gemini CLI operates primarily as a single agent with access to multiple tools rather than spawning multiple sub-agents. The tool delegation happens through the ReAct loop framework.

### Multi-Agent and Parallelization Features

Limited explicit multi-agent features compared to Claude Code or OpenHands. Focus is on single-agent operation with rich tool access.

### Planning Modes vs Execution Modes

#### ReAct Framework
Combines reasoning and action in an iterative loop:
1. Reason about the task
2. Act using available tools
3. Observe results
4. Iterate until task completion

### Context and Codebase Understanding

#### Massive Context Window
- Access to Gemini 3 models with **1 million token context window**
- Gemini 2.5 Pro available on free tier with personal Google account
- Enables understanding of very large codebases in a single session

#### Built-in Tools
- Google Search grounding for up-to-date information
- File operations
- Shell commands
- Web fetching
- MCP (Model Context Protocol) support for custom integrations

### Strengths and Use Cases

#### Free Tier Access
- 60 requests/min
- 1,000 requests/day
- Access to Gemini 2.5 Pro with 1M token context window
- Free with personal Google account

#### Performance
Gemini 3 Flash achieves 78% SWE-bench Verified score for agentic coding, demonstrating strong real-world coding capabilities.

#### Recent Updates (January 2026)
- Gemini 3 Flash now available in Gemini CLI
- Supports high-frequency workflows common to terminal-based work
- Updates to release notes, improvements to keybindings, various feature additions

#### Developer Experience
- Designed for developers who live in the command line
- Open source allows inspection and contribution
- MCP support enables custom integrations
- No vendor lock-in

---

## Continue CLI

### Overview

Continue is an open-source CLI that can be used in Headless mode to run async cloud agents or TUI mode as an in-sync coding agent. It provides developers with a powerful, programmable interface for building and interacting with asynchronous coding agents from the terminal.

### Installation and Setup

```bash
# NPM installation
npm i -g @continuedev/cli

# Interactive mode for complex tasks
cn

# Headless mode for automation
cn -p "Generate a conventional commit name for the current git changes"
```

### Key Commands and Workflows

#### Dual Operating Modes

1. **Interactive TUI Mode (`cn`)**
   - Full-screen terminal interface
   - Complex task handling
   - Real-time collaboration with agent

2. **Headless Mode (`cn -p "prompt"`)**
   - Non-interactive automation
   - Scriptable workflows
   - Pipe outputs to other commands

#### Mission Control Integration
The CLI provides the same workflows as Mission Control with pure terminal power, allowing you to:
- Iterate fast
- Pipe outputs
- Script everything

### Agent/Task Spawning Capabilities

#### Async Cloud Agents
Async Cloud Agents allow you to perform multiple AI-driven code-related operations concurrently without blocking your main workflow. Think of them as intelligent background workers that can handle complex tasks while you focus on other priorities.

This enables true parallel work where you can:
- Define a task
- Leave the LLM to execute in the background
- Start a new task immediately

### Multi-Agent and Parallelization Features

#### Concurrent Operations
Continue CLI's async cloud agents enable running multiple coding operations in parallel:
- Background task execution
- Non-blocking workflows
- Multiple concurrent agents working on different tasks

### Planning Modes vs Execution Modes

Continue CLI operates with both planning and execution capabilities integrated into its async agent framework, though not as explicitly separated as Claude Code's plan mode.

### Context and Codebase Understanding

#### Permissions and Safety
Continue CLI implements a granular permission system with sensible defaults:
- **Read-only tools**: Automatically allowed
- **Write operations**: Require confirmation
- **Terminal commands**: Require confirmation

This ensures safety while maintaining productivity.

### Strengths and Use Cases

#### Automation and Scripting
- Scriptable interface for building custom workflows
- Pipe outputs to integrate with existing scripts
- Automate repetitive tasks
- Non-interactive mode for CI/CD integration

#### Flexibility
- Same workflows as Mission Control GUI
- Pure terminal operation
- No context switching between tools

#### Beyond the Editor
Continue CLI can be used to automate everything beyond just coding tasks, making it a general-purpose automation tool powered by AI.

---

## Cursor CLI

### Overview

Cursor CLI brings the powerful Composer agent capabilities from Cursor's editor directly to the command line. Announced on January 16, 2026, it represents Cursor's expansion beyond the editor interface.

### Installation and Setup

Details available from Cursor's official documentation as of the January 16, 2026 release.

### Key Commands and Workflows

#### Agent Modes
- **Plan Mode** (`/plan` or `--mode=plan`): Design your approach before coding
  - Cursor asks clarifying questions to refine your plan
  - Pre-coding design and architecture discussions
- **Ask Mode**: Conversational interaction without immediate code changes

#### Cloud Handoff
- Background task execution
- Continue tasks in the cloud while you work on other things locally

#### MCP Integration
- One-click MCP authentication
- Access to Model Context Protocol servers

### Agent/Task Spawning Capabilities

#### Composer Agent in CLI
Agent mode gives Composer more autonomy, allowing it to:
- Pull context automatically
- Run terminal commands (with permission)
- Edit code across multiple files
- Use semantic search
- Grep strings across codebase

### Multi-Agent and Parallelization Features

While not explicitly multi-agent in the same way as Claude Code's subagents, Cursor CLI supports:
- Cloud handoff for background tasks
- Plan mode for separated planning phase
- Integration with MCP servers for extended capabilities

### Planning Modes vs Execution Modes

#### Plan Mode
- Dedicated planning phase before execution
- Clarifying questions to refine approach
- Design-first workflow

#### Execution Mode
- Agent autonomy with tool access
- Terminal command execution
- File editing and semantic search
- Active code modification

### Context and Codebase Understanding

Cursor CLI inherits Composer's powerful context understanding:
- Semantic search across codebase
- String grep capabilities
- Multiple file awareness
- Codebase-wide refactoring support

### Strengths and Use Cases

#### Flexibility
- Run agents in any terminal or script
- Not limited to editor environment
- Integration with existing CLI workflows

#### Background Tasks
Cloud handoff enables long-running tasks to continue while you focus on other work, improving productivity for time-intensive operations.

#### CLI + Editor Integration
Seamless handoff between terminal and editor environments, letting you use the best tool for each task.

---

## Cline

### Overview

Cline is an open-source, autonomous AI coding agent that utilizes a flexible LLM backend to plan and execute complex, multi-step software development tasks. It operates across three platforms: VS Code extension (primary), CLI tool, and JetBrains plugin.

### Installation and Setup

Cline is available as:
- **VS Code Extension**: Primary interface (Visual Studio Marketplace)
- **CLI Tool**: For terminal-based workflows and automation
- **JetBrains Plugin**: For IntelliJ-based IDEs

### Key Commands and Workflows

#### Client-Server Architecture
Cline operates through a client-server architecture:
- **Cline Core**: Runs as a standalone service
- **CLI**: Acts as a scriptable interface for managing tasks, instances, and agent interactions
- **Multiple Frontends**: CLI, VSCode, JetBrains can attach to the same Cline Core instance

This enables seamless task handoff between environments.

### Agent/Task Spawning Capabilities

#### Autonomous Agent Features
Cline can:
- Create and edit files
- Explore large projects
- Use the browser for web-related tasks
- Execute terminal commands (after permission is granted)

#### Browser Integration
For web development tasks, Cline can:
- Launch sites in a headless browser
- Click, type, scroll
- Capture screenshots and console logs
- Debug front-end issues

### Multi-Agent and Parallelization Features

#### CLI for Parallel Execution
The CLI is designed for both interactive use and automation, making it ideal for:
- CI/CD pipelines
- Parallel task execution
- Terminal-based workflows
- Background job management

#### Multiple Instance Support
Multiple frontends can attach to the same Cline Core instance, enabling distributed development workflows across different interfaces.

### Planning Modes vs Execution Modes

Cline handles complex tasks step-by-step thanks to Claude Sonnet's agentic coding capabilities, integrating planning and execution in its autonomous workflow.

### Context and Codebase Understanding

- Large project exploration capabilities
- File and directory navigation
- Code search and analysis
- Terminal output monitoring
- Browser-based debugging for web projects

### Strengths and Use Cases

#### Multi-Platform Support
- VS Code (primary)
- CLI (automation and terminal workflows)
- JetBrains (IntelliJ, PyCharm, WebStorm, etc.)

#### Flexibility
- Flexible LLM backend (not locked to single provider)
- Permission-based operation
- Autonomous task execution
- Integration with multiple development environments

#### CI/CD Integration
CLI design makes it ideal for continuous integration and deployment pipelines, enabling automated code generation and testing as part of build processes.

---

## Goose

### Overview

Goose is an on-machine AI agent capable of automating complex development tasks from start to finish. It goes beyond code suggestions to build entire projects from scratch, write and execute code, debug failures, orchestrate workflows, and interact with external APIs autonomously. Created by Block (formerly Square), Goose was contributed to the Linux Foundation's Agentic AI Foundation (AAIF) in December 2025.

### Installation and Setup

Available as both desktop app and CLI:
- Desktop application for GUI workflows
- CLI for terminal integration and automation

### Key Commands and Workflows

#### Two Operating Modes

1. **Full REPL Mode**
   - Chat back and forth like other CLI coding agents
   - Interactive conversation with the agent

2. **Terminal Integration**
   - `@goose "do this"` - Ambient assistance
   - Quick one-off commands without entering full REPL

#### Automation Scripts
```bash
# One-liner task execution
goose run -t "your instructions here"

# Instructions from file
goose run -i instructions.md
```

#### macOS Scheduling
On macOS, you can use crontab for scheduling recurrent scripts, automating Goose to activate repeatedly (e.g., with Docker Model Runner).

### Agent/Task Spawning Capabilities

Goose operates primarily as a single autonomous agent with extensive tool access rather than spawning multiple sub-agents. The focus is on the agent's ability to orchestrate complex workflows using available tools.

### Multi-Agent and Parallelization Features

Limited explicit multi-agent features. Goose focuses on being a powerful single agent with extensive capabilities rather than coordinating multiple agents.

### Planning Modes vs Execution Modes

Goose integrates planning and execution in its autonomous workflow, capable of:
- Building plans autonomously
- Configuring required tools
- Executing multi-step workflows
- Debugging and adapting when failures occur

### Context and Codebase Understanding

#### Development Environment
Goose operates with its own:
- Command line interface (CLI)
- Code editor
- Browser for documentation access
- Reasoning engine for problem-solving
- Long-term planning capability

#### Model Context Protocol (MCP)
One of Goose's biggest strengths is its support for the Model Context Protocol (MCP)—a standard backed by Anthropic and others to let models talk to tools and data in a structured way. This enables rich integration with external tools and data sources.

### Strengths and Use Cases

#### Model Flexibility
- Supports over 25 LLM providers
- Commercial services (OpenAI, Anthropic, etc.)
- Cloud platforms (AWS Bedrock, Google Vertex AI, etc.)
- Local models (Ollama, LM Studio, etc.)
- Multi-model configuration to optimize performance and cost

#### MCP Integration
Seamless integration with MCP servers enables Goose to access structured tools and data, extending its capabilities beyond basic coding tasks.

#### Open Source Governance
Contributed to the Linux Foundation's Agentic AI Foundation (AAIF) alongside Anthropic's MCP and OpenAI's AGENTS.md, ensuring the project's future is shaped by the community under neutral governance.

#### Versatility
Can be used for:
- Building entire projects from scratch
- Writing and executing code
- Debugging failures
- Orchestrating complex workflows
- Interacting with external APIs
- Research and analysis tasks

#### Desktop + CLI
Available in both desktop app and CLI forms, accommodating different workflow preferences and use cases.

---

## Devin CLI (Cognition Labs)

### Overview

Devin AI is created by Cognition Labs and is considered part of a trend surrounding the advent of autonomous AI agents that can take direct action to solve problems. It's positioned as an AI software engineer that can operate autonomously.

### Installation and Setup

Devin operates primarily as a web-based service with CLI integration capabilities. As of January 2026, Devin is being integrated into enterprise workflows (e.g., Infosys, Goldman Sachs).

### Key Commands and Workflows

#### Terminal Interface
Devin builds a plan and configures required tools using its own command line interface (CLI), code editor, and browser. The interface looks something like a cross between ChatGPT and a Unix terminal—half natural language and half code.

#### Monitoring
Devin's terminal allows you to:
- Watch commands being executed
- View output logs
- Monitor agent progress

### Agent/Task Spawning Capabilities

#### API and Integration
Devin provides an accessible API, and other agents can be integrated into custom workflows via CLI commands. The platform supports CLI scripts for agents, with examples including scripts to pull information about tickets from issue trackers.

### Multi-Agent and Parallelization Features

While Devin itself is a single autonomous agent, it can be integrated with other agents through its API and CLI commands, enabling multi-agent workflows at the orchestration level.

### Planning Modes vs Execution Modes

Devin operates with integrated planning and execution:
- Builds comprehensive plans
- Configures required tools
- Executes autonomously
- Adapts when encountering failures

### Context and Codebase Understanding

#### Autonomous Development Environment
Devin operates with its own:
- CLI
- Code editor
- Browser for documentation access
- Reasoning engine
- Long-term planning capability

It can access, read, and comprehend documentation using its reasoning engine.

### Strengths and Use Cases

#### Enterprise Integration
Recent developments include:
- Integration into Infosys internal engineering teams (after six months of use showing significant improvement in engineering quality and efficiency)
- Goldman Sachs using Devin as "Employee #1" in their "Hybrid Workforce"
- Infosys and Cognition strategic collaboration announced in 2026

#### Devin Review (January 2026)
An AI-enabled code review tool developed by Cognition, introduced in January 2026, extending Devin's capabilities into the code review domain.

#### Autonomous Operation
Devin can:
- Take direct action to solve problems
- Build entire features autonomously
- Operate with minimal human oversight
- Integrate with existing development workflows

#### Dual Interface
- Web interface for interactive work
- CLI tools for automation and integration

---

## Benchmarks & Performance Comparison

### Key Benchmarks for CLI Coding Agents (2026)

#### Terminal-Bench 2.0 (New Standard)

**Overview**
Launched in May 2025 through a collaboration with Stanford and the Laude Institute. Terminal-Bench evaluates whether AI agents can operate inside a real, sandboxed command-line environment.

**What It Measures**
Unlike one-shot patch-generation benchmarks, Terminal-Bench measures an agent's ability to:
- Plan across multi-step workflows
- Execute commands and scripts
- Recover from errors
- Navigate the filesystem under realistic constraints
- Compile code
- Configure environments
- Run tools

**Agents Evaluated**
The benchmark evaluates:
- Three popular command-line agents: Claude Code, Codex CLI, and Gemini CLI
- Three open-source software engineering agents: OpenHands, Mini-SWE-Agent, and Terminus 2

**Results (Early January 2026)**
Top performers:
- Droid + GPT-5.2
- Codex CLI + GPT-5.2

**Significance**
Terminal-Bench 2.0 is the new standard for CLI/terminal task fitness, providing a more realistic evaluation of agent capabilities in actual terminal environments.

#### SWE-bench Verified

**Overview**
A human-validated section of the SWE-bench dataset released by OpenAI in August 2024, consisting of 500 high-quality test cases.

**Performance Levels**
- Most top models score over 70% on the verified version
- Gemini 3 Flash achieves 78% SWE-bench Verified score

**What It Tests**
Real-world software engineering tasks from actual GitHub issues and pull requests, testing an agent's ability to:
- Understand problem descriptions
- Navigate codebases
- Implement solutions
- Pass existing test suites

#### SWE-bench Pro

**Overview**
A more challenging version of SWE-bench designed to test frontier model capabilities.

**Performance (2026)**
Best-performing models:
- OpenAI GPT-5: 23.3%
- Claude Opus 4.1: 23.1%

This demonstrates that even top models struggle with the most challenging real-world software engineering tasks, showing significant room for improvement.

#### Model Performance Insights

**Closed-Source vs Open-Source**
There is a clear trend that closed-source models perform better on SWE-bench than open-source models, with the exception of Qwen Max Instruct.

**Tool Usage Patterns**
Claude Sonnet 4 shows a more balanced approach with:
- Moderate usage across all tool categories
- Approximately 9,000-10,000 default tools
- Fewer search operations
- Indicates a more targeted problem-solving methodology

### Recommendations for Evaluation

**For CLI/Terminal Fitness**
Use Terminal-Bench 2.0 as the primary benchmark.

**For Software Engineering Capabilities**
Lead with SWE-bench Verified/Pro for comprehensive evaluation of coding abilities.

**Practical Considerations**
Benchmarks provide useful comparisons, but real-world performance depends on:
- Specific use cases
- Codebase characteristics
- Developer workflow integration
- Team collaboration needs
- Cost and availability

---

## Best Practices & Workflows

### Research-Plan-Implement Workflow

**The Problem**
Without research and planning steps, Claude (and other agents) tend to jump straight to coding a solution.

**The Solution**
Asking Claude to research and plan first significantly improves performance for problems requiring deeper thinking upfront.

**Implementation**
1. **Research**: Explore codebase, understand requirements, identify dependencies
2. **Plan**: Design architecture, identify approach, consider edge cases
3. **Implement**: Write code based on plan
4. **Review/Test**: Verify functionality, run tests, check for issues

### Plan-Act-Reflect Framework

**Purpose**
Helps your AI coding agent think before it codes, preventing runaway logic and improving collaboration between human and agent.

**Phases**
1. **Plan**: Define what needs to be done and how
2. **Act**: Execute the plan with code changes
3. **Reflect**: Review results, identify issues, iterate

### Specific Instructions

**Impact on Performance**
Claude Code's success rate improves significantly with more specific instructions, especially on first attempts. Clear directions upfront reduce the need for course corrections later.

**Best Practices**
- Be explicit about requirements
- Specify constraints and edge cases
- Provide context about codebase architecture
- Mention testing requirements upfront
- Clarify expected behavior

### Test-Driven Development (TDD)

**Why It Works with AI Agents**
Test-driven development becomes even more powerful with agentic coding. Asking Claude to write tests based on expected input/output pairs provides:
- Clear success criteria
- Automatic validation
- Regression protection
- Documentation of expected behavior

**Implementation**
1. Ask agent to write tests first
2. Provide expected input/output pairs
3. Have agent implement code to pass tests
4. Run tests automatically after changes

### Version Control Best Practices

**Why It Matters**
AI coding agents can move fast—but version control ensures you maintain order.

**Strong Git Practices**
- **Commit small, logical changes often**: Makes review easier, rollback safer
- **Review every change**: Don't blindly accept agent modifications
- **Use descriptive commit messages**: Many agents auto-generate good messages
- **Branch strategically**: Use feature branches for agent-driven work
- **Keep work transparent**: Easy to review and understand changes

### Start Small and Review

**Recommended Approach**
1. Pick one agent and integrate it into an existing Git workflow
2. Review every change it makes
3. Run tests after each modification
4. Treat the agent as a collaborator rather than an authority
5. Gradually expand usage as you build trust

### Custom Commands and Templates

**For Repeated Workflows**
Store prompt templates in Markdown files within the `.claude/commands` folder (for Claude Code), which:
- Become available through the slash commands menu
- Can be checked into git for team access
- Ensure consistency across team members
- Reduce typing for common tasks

**Example Use Cases**
- Code review prompts
- Testing templates
- Documentation generation
- Refactoring patterns

### Parallel Subagent Patterns

#### Research & Literature Review
Run these in parallel when exploring a new topic or codebase:
- **Explore agent**: Search codebase for relevant implementations
- **WebSearch agent**: Find papers, docs, or existing solutions
- **Plan agent**: Identify architecture and design patterns

#### Data Processing & Experiments
- Process multiple datasets simultaneously
- Run parameter sweeps in parallel
- Compare different algorithms/approaches side-by-side

#### Code Analysis & Debugging
- **Agent 1**: Trace data flow through the system
- **Agent 2**: Search for similar patterns/bugs in codebase
- **Agent 3**: Check documentation and tests for expected behavior

#### Build & Test Parallelization
- Run tests while building documentation
- Lint/format while running unit tests
- Build multiple targets simultaneously

### Subagent Best Practices

1. **Independence**: Only parallelize tasks with no dependencies between them
2. **Specificity**: Give each agent a clear, focused objective
3. **Background tasks**: Use `run_in_background: true` for long-running tasks (builds, large searches)
4. **Explicit parallel request**: Say "run in parallel" or "simultaneously" to trigger parallel execution
5. **Collect and synthesize**: After parallel agents complete, synthesize findings into actionable insights

### 2026 Workflow Trends

**Parallel Running**
More apps will support parallel running as a workflow in 2026, allowing developers to:
- Define a task
- Leave an LLM to execute it in the background
- Start a new task immediately

**Async Agents**
Continue CLI and other tools support async cloud agents that work in the background while you focus on other priorities.

**Trust and Reliability**
2026 will be about securing ground for Agentic CLI tools—developers need to be convinced that available products can be trusted to support their workflows over time.

---

## Context Management & Token Optimization

### The Context Window Challenge

**Advertised vs Actual Performance**
Even as modern AI assistants leverage models with context windows ranging from 128,000 tokens to over 1 million tokens (Cursor's Max Mode with Gemini 3 Pro), most models break much earlier than advertised. A model claiming 200k tokens typically becomes unreliable around 130k, with sudden performance drops rather than gradual degradation.

**Why It Matters**
Larger windows do not eliminate the need for disciplined context management. Effective agentic systems must treat context the way operating systems treat memory and CPU cycles: as finite resources to be budgeted, compacted, and intelligently paged.

### Auto-Compaction

#### GitHub Copilot CLI
When approaching 95% of the token limit, Copilot automatically compresses conversation history, preventing context overflow that would otherwise terminate sessions.

**Manual Controls**
- `/compact` - Manual compression of conversation history
- `/context` - Visualize current token usage
- `--resume` - Tab completion to cycle through sessions

#### Benefits
- Prevents session termination
- Maintains continuity of work
- Transparent to user
- Preserves important context while removing redundancy

### Specialized Agents for Context Optimization

#### Explore Agent (Claude Code, GitHub Copilot)
An Explore agent enables codebase analysis without cluttering the main conversation context. Key benefits:
- **Read-only**: Won't accidentally modify code
- **Efficient**: Often uses smaller models (e.g., Haiku)
- **Isolated**: Runs in separate context window
- **Targeted**: Focused on search and exploration

#### Sub-Agents for Context Isolation

**Claude Code Subagents**
Each subagent runs in its own context window with:
- Custom system prompt
- Specific tool access
- Independent permissions
- Isolated token budget

**OpenHands Sub-Agent Delegation**
Sub-agents operate as independent conversations that:
- Inherit parent's model configuration
- Maintain separate workspace context
- Enable structured parallelism
- Prevent context pollution

### Context Engineering Techniques

#### Scratchpad Usage
Sub-agents can use scratchpads for:
- Temporary workspace for intermediate computations
- Notes that don't pollute main conversation
- Calculation staging areas
- Scratch work isolation

#### Repository Maps (Aider)
Aider's repo-map approach:
- Creates concise map of entire git repository
- Includes most important classes and functions with types and signatures
- Uses graph ranking algorithm to identify relevant portions
- Optimizes what fits into active token budget
- Updates relevance based on current chat state

Benefits:
- Understand relationships without loading full files
- Smart selection of relevant context
- Scalable to large codebases
- Dynamic adaptation to conversation

### Token Optimization Strategies

#### 1. Lazy Loading
Don't load entire codebase upfront:
- Load files on-demand as needed
- Use repo maps for overview
- Pull full file content only when modifying

#### 2. Strategic Compaction
- Compress older conversation history
- Preserve critical context (goals, constraints, decisions)
- Remove redundant exchanges

#### 3. Tool-Based Offloading
Use tools instead of loading content into context:
- File search tools instead of loading directories
- Grep for specific patterns instead of reading files
- Execute commands and return only results

#### 4. Hierarchical Context
- Main agent maintains high-level context
- Sub-agents handle detail-level work
- Results summarized back to main agent

### Model-Specific Context Features

#### Gemini CLI - 1M Token Context Window
Gemini 2.5 Pro and Gemini 3 models offer:
- 1 million token context window
- Ability to load extremely large codebases
- Reduced need for context management tricks
- Free tier access with personal Google account

**Caveat**: Even with 1M tokens, performance typically degrades before limit is reached.

### Industry Trends (2026)

**Context as a Resource**
Looking ahead to 2026, developers are gravitating toward tools that deliver more per token:
- Better context management
- Fewer retries needed
- Stronger first passes
- Less iteration to reach goals

**Disciplined Management Required**
The trend is toward treating context like operating systems treat memory:
- Budget allocation
- Intelligent paging
- Compaction strategies
- Priority-based retention

### Best Practices Summary

1. **Monitor Context Usage**: Use tools like `/context` to visualize token consumption
2. **Use Specialized Agents**: Offload searches and exploration to dedicated agents
3. **Enable Auto-Compaction**: Let tools automatically manage context limits
4. **Structure Information Hierarchically**: Main agent coordinates, sub-agents handle details
5. **Choose Models Wisely**: Balance context window size with model capabilities
6. **Load Lazily**: Don't front-load entire codebase, fetch on-demand
7. **Compress History**: Periodically compact conversation history while preserving key decisions
8. **Use Repository Maps**: Leverage tools like Aider's repo-map for overview without full file loading

---

## Key Trends in 2026

### 1. Shift from Suggestion to Autonomy

**Historical Context**
Early AI coding tools focused on autocomplete and suggestions (GitHub Copilot 2021-2023).

**2026 Reality**
Agentic coding—where AI doesn't just suggest code but autonomously plans, executes, debugs, and iterates across your entire codebase—has crossed from research prototype to daily driver for thousands of developers.

**Impact**
CLI coding agents in 2026 represent a shift from suggestion-based assistance to truly agentic workflows that plan, act, and adapt while staying rooted in the terminal.

### 2. Multi-Agent Orchestration

**Current State**
Most advanced CLI tools now support some form of multi-agent coordination:
- Claude Code: Subagents with parallelization (up to 10 parallel)
- OpenHands: Hierarchical agent delegation
- GitHub Copilot: Specialized custom agents (Explore, Task, Plan, Code-Review)
- Codex CLI: Agent collaboration with spawn_agent and send_input

**Swarming (2026 Enhancement)**
Anthropic engineers mentioned plans to enhance "Swarming" (orchestrated multi-agent execution) in 2026, representing the next evolution in agent coordination.

**Why It Matters**
Complex software tasks benefit from specialization—having dedicated agents for exploration, planning, implementation, and review mirrors human team structures.

### 3. Parallel Execution Becomes Standard

**Trend**
More apps will support parallel running as a workflow in 2026, allowing developers to:
- Define a task and leave an LLM to execute in the background
- Start a new task immediately
- Run multiple research/exploration tasks simultaneously
- Process multiple datasets in parallel

**Examples**
- Continue CLI: Async cloud agents
- Claude Code: Parallel subagent spawning
- Cursor CLI: Cloud handoff for background tasks

### 4. Model Context Protocol (MCP) Adoption

**What is MCP?**
A standard backed by Anthropic and others to let models talk to tools and data in a structured way.

**Tools Supporting MCP**
- Goose: "One of Goose's biggest strengths"
- Gemini CLI: Built-in MCP support for custom integrations
- Codex CLI: Model Context Protocol for third-party tools
- Cursor CLI: One-click MCP authentication

**Impact**
MCP enables rich integration with external tools and data sources, standardizing how agents access capabilities beyond basic coding.

**Governance**
Contributed to the Linux Foundation's Agentic AI Foundation (AAIF) alongside Anthropic's MCP and OpenAI's AGENTS.md.

### 5. Open Source Dominance

**2026 Landscape**
Most CLI coding agents are open-source or low-cost:
- Aider: Fully open source
- OpenHands: Fully open source (Apache 2.0-style license)
- Gemini CLI: Open source (Apache 2.0)
- Goose: Open source (contributed to Linux Foundation AAIF)
- Codex CLI: Open source (built in Rust)
- Cline: Open source

**Benefits**
- No vendor lock-in
- Community contribution
- Transparency and trust
- Customization and extension

**Governance Models**
Notable: Goose's contribution to Linux Foundation's Agentic AI Foundation ensures neutral governance and community-driven development.

### 6. Context Window Arms Race

**Current State**
- Gemini 3: 1 million tokens
- Claude models: 200k tokens
- GPT models: Varying by version

**Reality Check**
Most models break much earlier than advertised—a model claiming 200k tokens typically becomes unreliable around 130k.

**2026 Focus**
Rather than just larger windows, emphasis is on:
- Better context management
- Auto-compaction
- Specialized agents to offload context
- Repository maps and semantic indexing
- Intelligent token budgeting

### 7. Benchmark Evolution

**Traditional Benchmarks**
SWE-bench and variants focused on one-shot patch generation.

**New Standard**
Terminal-Bench 2.0 (launched May 2025) evaluates:
- Multi-step workflows
- Planning and recovery
- Real command-line operation
- Filesystem navigation
- Environment configuration

**Why It Matters**
Better benchmarks drive better tools—Terminal-Bench 2.0 measures what actually matters for CLI agent effectiveness.

### 8. Trust and Reliability Focus

**2026 Priority**
"2026 will be about securing ground for Agentic CLI tools—developers need to be convinced that available products can be trusted to support their workflows over time."

**Factors**
- Consistent performance
- Reliable updates
- Strong governance (open source, foundations)
- Security and privacy
- Enterprise adoption (Infosys, Goldman Sachs using Devin)

### 9. Specialized Agents for Specific Tasks

**Pattern**
Rather than single general-purpose agent, tools are moving toward:
- Explore agents for codebase analysis
- Plan agents for architecture and design
- Task agents for command execution
- Code-review agents for evaluation
- Architect models + editor models (Aider)

**Benefits**
- Optimization for specific tasks
- Smaller, faster models for simple tasks
- Advanced reasoning models for complex planning
- Cost optimization
- Performance improvement

### 10. Terminal-First Development

**Philosophy**
Tools designed for developers who live in the command line, not just IDE-first tools with CLI added.

**Examples**
- Gemini CLI: "Designed for developers who live in the command line"
- Aider: "Git-first CLI coding agent"
- Goose: "Terminal-first AI agent"

**Benefits**
- Fits existing workflows
- Scriptable and automatable
- CI/CD integration
- No context switching
- Full control

### 11. Reasoning Models Integration

**Trend**
Integration with advanced reasoning models:
- OpenAI o1, o3-mini, o4-mini
- Claude Opus 4.5
- GPT-5, GPT-5-Codex

**Architect Mode Example**
Aider's architect mode pairs reasoning-strong models (o1) with editing-capable models (GPT-4o, Sonnet):
- Architect reasons about solution
- Editor implements specific changes

**Impact**
Better planning and problem-solving before code generation, leading to fewer iterations and higher quality solutions.

### 12. Free and Freemium Tiers

**Accessibility**
Many tools offer generous free tiers:
- Gemini CLI: Free with personal Google account (60 req/min, 1000/day)
- Aider: Open source, free (pay only for LLM API)
- OpenHands: Open source
- Continue CLI: Open source

**Impact**
Democratizes access to advanced AI coding assistance, allowing individual developers and small teams to benefit without significant financial investment.

---

## Sources

### Claude Code CLI
- [GitHub - anthropics/claude-code](https://github.com/anthropics/claude-code)
- [Claude Code - AI coding agent for terminal & IDE](https://claude.com/product/claude-code)
- [Claude Code overview - Claude Code Docs](https://code.claude.com/docs/en/overview)
- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Create custom subagents - Claude Code Docs](https://code.claude.com/docs/en/sub-agents)
- [How to Use Claude Code Subagents to Parallelize Development](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/)
- [Multi-agent parallel coding with Claude Code Subagents](https://medium.com/@codecentrevibe/claude-code-multi-agent-parallel-coding-83271c4675fa)
- [Set up Claude Code - Claude Code Docs](https://code.claude.com/docs/en/setup)
- [@anthropic-ai/claude-code - npm](https://www.npmjs.com/package/@anthropic-ai/claude-code)

### Aider
- [Aider - AI Pair Programming in Your Terminal](https://aider.chat/)
- [GitHub - Aider-AI/aider](https://github.com/Aider-AI/aider)
- [Chat modes | aider](https://aider.chat/docs/usage/modes.html)
- [Repository map | aider](https://aider.chat/docs/repomap.html)
- [Installation | aider](https://aider.chat/docs/install.html)
- [Getting Started with Aider: AI-Powered Coding from the Terminal](https://blog.openreplay.com/getting-started-aider-ai-coding-terminal/)

### OpenHands
- [The OpenHands CLI: AI-Powered Development in Your Terminal](https://openhands.dev/blog/the-openhands-cli-ai-powered-development-in-your-terminal)
- [GitHub - OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)
- [OpenHands | The Open Platform for Cloud Coding Agents](https://openhands.dev/)
- [Sub-Agent Delegation - OpenHands Docs](https://docs.openhands.dev/sdk/guides/agent-delegation)
- [The OpenHands Software Agent SDK](https://arxiv.org/html/2511.03690v1)

### Codex CLI (OpenAI)
- [Codex CLI](https://developers.openai.com/codex/cli/)
- [GitHub - openai/codex](https://github.com/openai/codex)
- [Codex CLI features](https://developers.openai.com/codex/cli/features/)
- [Quickstart](https://developers.openai.com/codex/quickstart/)
- [Codex CLI Safe Planning Guide](https://smartscope.blog/en/generative-ai/chatgpt/codex-plan-mode-complete-guide/)

### GitHub Copilot CLI
- [GitHub - github/copilot-cli](https://github.com/github/copilot-cli)
- [GitHub Copilot CLI: Enhanced agents, context management](https://github.blog/changelog/2026-01-14-github-copilot-cli-enhanced-agents-context-management-and-new-ways-to-install/)
- [Using GitHub Copilot CLI - GitHub Docs](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-cli)
- [About GitHub Copilot CLI - GitHub Docs](https://docs.github.com/en/copilot/concepts/agents/about-copilot-cli)

### Gemini CLI (Google)
- [GitHub - google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)
- [Gemini CLI | Gemini Code Assist](https://developers.google.com/gemini-code-assist/docs/gemini-cli)
- [Google announces Gemini CLI: your open-source AI agent](https://blog.google/technology/developers/introducing-gemini-cli-open-source-ai-agent/)
- [Gemini 3 Flash is now available in Gemini CLI](https://developers.googleblog.com/gemini-3-flash-is-now-available-in-gemini-cli/)

### Continue CLI
- [GitHub - continuedev/continue](https://github.com/continuedev/continue)
- [Building Cloud Agents with Continue CLI](https://blog.continue.dev/building-async-agents-with-continue-cli/)
- [Beyond the Editor: Using Continue CLI](https://blog.continue.dev/beyond-the-editor-how-im-using-continue-cli-to-automate-everything/)

### Cursor CLI
- [Cursor CLI (Jan 16, 2026): CLI Agent Modes](https://forum.cursor.com/t/cursor-cli-jan-16-2026-cli-agent-modes-and-cloud-handoff/149171)
- [Features · Cursor](https://cursor.com/features)
- [Modes | Cursor Docs](https://cursor.com/docs/agent/modes)

### Cline
- [GitHub - cline/cline](https://github.com/cline/cline)
- [Cline - AI Coding, Open Source and Uncompromised](https://cline.bot/)
- [CLI Reference - Cline](https://docs.cline.bot/cline-cli/cli-reference)

### Goose
- [GitHub - block/goose](https://github.com/block/goose)
- [Quickstart | goose](https://block.github.io/goose/docs/quickstart/)
- [Goose: The Terminal-First AI Agent](https://dev.to/james_miller_8dc58a89cb9e/goose-the-terminal-first-ai-agent-that-actually-gets-work-done-g5e)
- [What Makes Goose Different](https://dev.to/nickytonline/what-makes-goose-different-from-other-ai-coding-agents-2edc)

### Devin CLI
- [Introducing Devin - Devin Docs](https://docs.devin.ai/)
- [Cognition](https://cognition.ai/)
- [Coding Agents 101](https://devin.ai/agents101)

### Benchmarks & Comparisons
- [Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks](https://arxiv.org/html/2601.11868)
- [SWE-bench](https://www.vals.ai/benchmarks/swebench)
- [8 benchmarks shaping the next generation of AI agents](https://ainativedev.io/news/8-benchmarks-shaping-the-next-generation-of-ai-agents)
- [Introducing SWE-bench Verified](https://openai.com/index/introducing-swe-bench-verified/)
- [Agentic CLI Tools Compared: Claude Code vs Cline vs Aider](https://research.aimultiple.com/agentic-cli/)
- [Top 5 CLI Coding Agents in 2026](https://dev.to/lightningdev123/top-5-cli-coding-agents-in-2026-3pia)
- [Best AI Coding Agents for 2026: Real-World Developer Reviews](https://www.faros.ai/blog/best-ai-coding-agents-2026)

### Best Practices & Context Management
- [Claude Code: Best practices for agentic coding](https://www.anthropic.com/engineering/claude-code-best-practices)
- [Building With AI Coding Agents: Best Practices](https://medium.com/@elisheba.t.anderson/building-with-ai-coding-agents-best-practices-for-agent-workflows-be1d7095901b)
- [GitHub Copilot CLI Gains Specialized Agents](https://winbuzzer.com/2026/01/16/github-copilot-cli-gains-specialized-agents-parallel-execution-and-smarter-context-management-xcxwbn/)
- [Context Window Management: Strategies for Long-Context AI Agents](https://www.getmaxim.ai/articles/context-window-management-strategies-for-long-context-ai-agents-and-chatbots/)
- [5 Key Trends Shaping Agentic Development in 2026](https://thenewstack.io/5-key-trends-shaping-agentic-development-in-2026/)
