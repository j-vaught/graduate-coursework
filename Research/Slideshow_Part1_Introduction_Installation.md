# Agentic Coding Tools - Part 1: Introduction & Installation

## Complete Slideshow Document (40+ Slides)

---

## SECTION 1: What are Agentic Coding Tools?

---

### Slide 1: Title Slide

**Title:** Agentic Coding Tools
**Subtitle:** Empowering Developers with AI-Driven Development

**Content:**
- Part 1: Introduction & Installation
- A comprehensive guide to autonomous coding assistants
- Covering 15+ tools and frameworks
- From basic setup to advanced workflows

**Speaker Notes:**
Welcome to this comprehensive guide on agentic coding tools. This first section covers what these tools are, how they're categorized, and how to install them on your system. By the end of this session, you'll have hands-on experience setting up multiple terminal-based agents, IDE integrations, and VS Code plugins. The goal is to equip you with the knowledge to choose and implement the right tools for your development workflow.

---

### Slide 2: What Are Agentic Coding Tools?

**Title:** Understanding Agentic Coding Tools

**Content:**
- Autonomous software agents that use AI to assist with code development
- Go beyond simple code completion - they take actions
- Read files, execute commands, run tests, install dependencies
- Multi-turn conversations with context awareness
- Can plan complex tasks and execute them iteratively

**Key Characteristics:**
1. **Autonomous Action** - Execute commands, not just suggest code
2. **Context Awareness** - Understand entire codebase
3. **Tool Integration** - Work with terminals, file systems, git
4. **Iterative Problem Solving** - Refine solutions based on feedback
5. **Multi-step Reasoning** - Plan and execute complex tasks

**Speaker Notes:**
The fundamental difference between agentic tools and traditional code completion is agency. Traditional tools like GitHub Copilot suggest code snippets. Agentic tools go further - they can read your codebase, run tests, debug issues, commit changes, and manage dependencies. This represents a paradigm shift in how developers interact with AI tools. Instead of copy-pasting suggestions, you describe what you want and the agent figures out how to accomplish it, often with multiple steps and course corrections.

---

### Slide 3: The AI Agent Loop

**Title:** How Agentic Tools Work: The Loop

**Content:**

```
┌─────────────────────────────────────────────┐
│         Developer Request / Goal            │
│    "Fix the authentication bug in login"    │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│    Agent Reasons About Problem              │
│  - Analyze codebase structure               │
│  - Identify relevant files                  │
│  - Plan solution approach                   │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│    Execute Tools/Actions                    │
│  - Read files                               │
│  - Execute terminal commands                │
│  - Run tests                                │
│  - Make code changes                        │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│    Observe Feedback & Results               │
│  - Test output                              │
│  - Error messages                           │
│  - File system changes                      │
└────────────────┬────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────┐
│    Refine & Continue Loop                   │
│  - Successful? Done                         │
│  - Failed? Iterate with new approach        │
│  - Partial? Continue from where we left     │
└─────────────────────────────────────────────┘
```

**Speaker Notes:**
The agentic loop is the core concept that differentiates agentic tools. Unlike traditional IDEs where you're in control, with agentic tools you describe the goal and the agent reasons through how to achieve it. It makes observations, takes actions, observes the results, and refines the approach. This loop continues until the goal is achieved or the agent determines it cannot proceed.

---

### Slide 4: Real-World Example: Bug Fixing Flow

**Title:** Example: Fixing a Bug with an Agent

**Content:**

**Scenario:** "Fix the login endpoint - it's returning 500 errors"

**Agent's Autonomous Process:**

1. **Exploration Phase** (2-3 minutes)
   - Search codebase for login-related files
   - Examine error logs
   - Identify relevant dependencies
   - Read authentication logic

2. **Analysis Phase** (1-2 minutes)
   - Understand the problem
   - Check recent commits that might have caused it
   - Review test files

3. **Implementation Phase** (3-5 minutes)
   - Propose fixes
   - Write code changes
   - Run tests automatically

4. **Verification Phase** (2-3 minutes)
   - Execute full test suite
   - Check for regressions
   - Commit changes with git

**Result:** Bug fixed, tests passing, changes committed - all without manual intervention

**Speaker Notes:**
This is what separates agentic tools from static code completion. A traditional AI tool might suggest a one-line fix. An agentic tool actually understands the problem, navigates your codebase, writes comprehensive fixes, runs tests, and verifies everything works. The time saved isn't just in typing - it's in the entire troubleshooting and verification workflow.

---

### Slide 5: Why Use Agentic Coding Tools?

**Title:** Benefits of Agentic Coding Tools

**Content:**

**Productivity Benefits:**
- 40-60% faster development cycles for certain tasks
- Eliminates context switching (agent gathers context for you)
- Automated testing and verification
- Faster debugging (agent systematically explores issues)

**Quality Benefits:**
- Comprehensive code review (agent checks entire codebase impact)
- Automated test generation
- Consistent code style and patterns
- Better documentation

**Learning Benefits:**
- Understand how to solve problems step-by-step
- See best practices demonstrated
- Interactive feedback on approaches
- Explore alternative solutions

**Developer Experience:**
- Natural language interface
- Conversational problem solving
- Less boilerplate code writing
- Focus on high-level logic, not syntax

**Limitations to Be Aware:**
- Context window limits (can't always see entire codebase)
- Hallucination risk (agents sometimes "create" functions that don't exist)
- Cost (API calls add up)
- Learning curve (different tools have different patterns)

**Speaker Notes:**
The benefits are significant, but it's important to set realistic expectations. These tools are force multipliers, not magic wands. They excel at routine tasks like writing boilerplate, generating tests, and basic refactoring. They struggle with deep architectural decisions, security-critical code, and novel problems. The best developers will use agentic tools strategically - knowing when to let the agent take over and when to maintain manual control.

---

### Slide 6: Agentic Tools vs. Traditional Code Completion

**Title:** Comparison: Traditional vs. Agentic Tools

**Content:**

| Aspect | Traditional (GitHub Copilot) | Agentic (Claude Code, Aider) |
|--------|-----|-----|
| **Input** | Type code, get suggestions | Describe task in natural language |
| **Output** | Code snippets | Complete solutions with verification |
| **Scope** | Single file, current context | Entire codebase |
| **Actions** | Suggest code | Execute commands, modify files, run tests |
| **Verification** | Manual testing | Automatic testing and validation |
| **Iteration** | Manual refinement | Automatic refinement based on feedback |
| **Error Recovery** | You fix errors | Agent attempts fixes automatically |
| **Typical Use Case** | Writing new code | Solving problems, refactoring, debugging |
| **Learning Curve** | Low | Medium |
| **Cost Model** | Subscription/token-based | API usage or subscription |

**Speaker Notes:**
It's crucial to understand that agentic tools are not replacements for traditional completion tools - they're complementary. You might use GitHub Copilot for autocomplete while coding, then switch to Claude Code or Aider when you need to tackle a larger problem like "refactor this entire module" or "fix the failing test suite." Different tools excel at different tasks.

---

## SECTION 2: The Three Categories Overview

---

### Slide 7: Three Categories of Agentic Tools

**Title:** The Agentic Tools Ecosystem

**Content:**

```
AGENTIC TOOLS ECOSYSTEM
│
├── TERMINAL-BASED AGENTS (PRIMARY FOCUS)
│   └── Run in command line, full system access
│       ├── Claude Code (Anthropic)
│       ├── Aider (open-source)
│       ├── Codex CLI (OpenAI)
│       ├── Gemini CLI (Google)
│       ├── GitHub Copilot CLI
│       ├── OpenHands (open-source)
│       ├── Goose (open-source)
│       └── Continue CLI
│
├── AGENTIC IDEs (SPECIALIZED EDITORS)
│   └── Purpose-built editors with agents built-in
│       ├── Cursor
│       ├── Windsurf
│       └── Zed
│
└── VS CODE PLUGINS (INTEGRATED)
    └── Add agentic capabilities to VS Code
        ├── GitHub Copilot (with chat)
        ├── Cline
        ├── Continue
        └── Amazon Q
```

**Speaker Notes:**
These three categories serve different workflows. Terminal-based agents are most powerful for complex tasks and automation. Agentic IDEs provide a cohesive, optimized experience. VS Code plugins integrate agents into your existing editor. Most professional developers use a combination - terminal agents for major tasks, IDE plugins for regular development. We'll focus heavily on terminal agents in this course because they're the most flexible and powerful.

---

### Slide 8: Category 1 - Terminal-Based Agents (Overview)

**Title:** Terminal-Based Agents: The Powerhouses

**Content:**

**What Are Terminal-Based Agents?**
- Run in your terminal/command line
- Full access to your system and codebase
- Communicate via natural language in the terminal
- Can execute any command you could run manually
- Multi-turn conversations within same session

**Why They're Most Powerful:**
1. **Unrestricted Access** - No UI limitations, direct system access
2. **Scripting Integration** - Integrate into build pipelines and workflows
3. **Version Control** - Direct git integration for commits and branches
4. **Automation** - Can be incorporated into CI/CD workflows
5. **Flexibility** - Work with any language, framework, or tool

**Best For:**
- Complex multi-step tasks
- Automation and scripting
- Projects needing git integration
- Working in headless environments
- Integration into development workflows

**Trade-offs:**
- No visual IDE features
- Require terminal comfort
- Context shown in text only
- May need more explicit instructions

**Speaker Notes:**
Terminal-based agents are like having a senior developer on your team who works at the command line. They're powerful precisely because they have no restrictions - they work with your actual files, your actual tools, your actual codebase. This is why we're dedicating the most time to these tools. Once you master terminal agents, the IDE-based tools feel like simplified versions.

---

### Slide 9: Terminal Agents Deep Dive - Claude Code

**Title:** Claude Code: Anthropic's Terminal Agent

**Content:**

**Overview:**
- Developed by Anthropic
- Powers this entire training session
- Uses Claude language models (Claude 3.5 Sonnet)
- Most sophisticated agentic capabilities
- Uses MCP (Model Context Protocol) for extensions

**Key Strengths:**
- Best long-context understanding
- Excellent code analysis and refactoring
- Strong reasoning for complex problems
- Can maintain multi-hour conversations
- Integrates web search and tool use

**Best Use Cases:**
- Large refactoring projects
- Complex debugging scenarios
- Architectural discussions
- Building from specifications
- Learning and exploration

**Unique Features:**
- Model Context Protocol (MCP) support
- Anthropic Claude models (Opus 4.5, Sonnet 3.5)
- Can work in "test" mode for experimentation
- Strong safety and alignment properties

**Resource Requirements:**
- Low: Terminal + API access
- Requires API key (paid)
- No heavyweight IDE needed

**Speaker Notes:**
Claude Code is what powers this entire training. You're learning from the tool itself, so to speak. Its primary advantage is the quality of Claude's reasoning - it's exceptional at understanding nuanced problems and maintaining context over long conversations. If you're solving a truly difficult problem, Claude Code is often the first tool to reach for.

---

### Slide 10: Terminal Agents - Aider

**Title:** Aider: Open Source Powerhouse

**Content:**

**Overview:**
- Open-source (GPLv3 licensed)
- Mature, well-maintained tool
- Supports multiple LLM providers
- Specifically designed for pair programming

**Supported LLM Providers:**
- OpenAI (GPT-4, GPT-3.5)
- Anthropic Claude models
- Local models via Ollama
- Google Gemini
- Mistral, Cohere, and others

**Key Strengths:**
- Works offline with local models
- Multi-file editing with clear diffs
- Excellent git integration
- Active community and regular updates
- Cost-effective (can use cheaper models)

**Best Use Cases:**
- Pair programming workflows
- Multi-file refactoring
- When you want to stay offline
- Teams with specific LLM provider agreements
- Developers who prefer open-source tools

**Unique Features:**
- "Whole file" mode for complete rewrites
- Diff-based editing shows exact changes
- Built-in code review mechanism
- Can use local models (completely offline)

**Resource Requirements:**
- Terminal only
- API keys for remote LLMs OR local model setup
- Memory for local models (8GB+ recommended)

**Speaker Notes:**
Aider is fantastic if you value open-source software or want to work with local models. The diff-based approach is excellent for code review - you always know exactly what the agent changed. Many professional teams prefer Aider because they can run it locally without sending code to cloud APIs.

---

### Slide 11: Terminal Agents - OpenAI Codex CLI

**Title:** Codex CLI: OpenAI's Terminal Interface

**Content:**

**Overview:**
- OpenAI's official terminal tool
- Access to GPT-4 models
- Designed for command-line integration
- Good for quick tasks and automation

**Key Strengths:**
- Fast responses (GPT-4 is optimized for speed)
- Well-maintained by OpenAI
- Good for smaller, focused tasks
- Integrates with OpenAI ecosystem

**Best Use Cases:**
- Quick code generation tasks
- Command-line tool building
- Script automation
- Teams already using OpenAI APIs
- Fast feedback loops

**Limitations:**
- Less agentic than some alternatives
- Context window is fixed
- Primarily code generation, not problem solving
- Limited multi-turn reasoning

**Unique Features:**
- Direct GPT-4 access
- Fast, optimized for speed
- Good for simple tasks
- Integrates with OpenAI dashboards

**Resource Requirements:**
- Terminal access
- OpenAI API key
- OpenAI credits/paid account

**Speaker Notes:**
Codex CLI is good if speed is your priority and you're working on well-defined, smaller problems. It's not as "agentic" as some tools - it's more of a terminal-based code completion tool. But it's fast, reliable, and well-maintained.

---

### Slide 12: Terminal Agents - Gemini CLI

**Title:** Gemini CLI: Google's Entry

**Content:**

**Overview:**
- Google's official terminal interface
- Access to Gemini models (1.5 Pro, 1.5 Flash)
- Relatively new to the scene
- Good token-to-price ratio

**Key Strengths:**
- Excellent token limits (1M tokens for Gemini 1.5 Pro)
- Cost-effective pricing
- Good for long conversations
- Supports document/image input

**Best Use Cases:**
- Projects with large codebases
- Multi-hour debugging sessions
- Teams using Google Cloud
- Cost-conscious organizations
- Document-heavy workflows

**Limitations:**
- Newer, less established than competitors
- Community smaller than OpenAI/Anthropic
- Integration ecosystem developing

**Unique Features:**
- 1 million token context window
- Good multimodal support
- Google Cloud integration
- Competitive pricing

**Resource Requirements:**
- Terminal access
- Google Cloud account
- API key and credits

**Speaker Notes:**
Gemini CLI is worth considering if you're doing very long-context work. A 1 million token context window means you can feed it your entire codebase and it can reason over all of it. For large-scale refactoring or understanding massive projects, this is a huge advantage.

---

### Slide 13: Terminal Agents - Others Overview

**Title:** Other Terminal Agents (Brief Overview)

**Content:**

**GitHub Copilot CLI**
- Integrates with GitHub Copilot ecosystem
- Good for GitHub-integrated workflows
- Fewer agentic features than others
- Useful for developers already in GitHub ecosystem

**OpenHands**
- Open-source agent framework
- Supports multiple backends
- Good for research and experimentation
- More framework than finished tool

**Goose**
- Light-weight open-source agent
- Python-based, hackable
- Growing community
- Good for learning how agents work

**Continue CLI**
- Part of Continue.dev ecosystem
- VS Code-focused but has CLI
- Emerging as serious contender
- Good for teams using Continue plugin

**Speaker Notes:**
These four tools are worth monitoring but not the primary focus of this course. The first four we covered (Claude Code, Aider, Codex CLI, Gemini CLI) represent the most mature, well-maintained, and powerful options. As the agentic tools space matures, tools like OpenHands and Goose may become more prominent.

---

### Slide 14: Category 2 - Agentic IDEs

**Title:** Agentic IDEs: Built-In Intelligence

**Content:**

**What Are Agentic IDEs?**
- Purpose-built code editors with agents built-in
- No plugins or extensions needed
- Optimized user interface for agentic workflows
- Visual code editing + agent capabilities

**The Three Main Players:**

**Cursor**
- Based on VS Code, easier learning curve
- Most mature agentic IDE
- Strong IDE features + solid agent
- Best for VS Code users transitioning to agents

**Windsurf**
- Newest entrant, strong backing
- Most sophisticated agent capabilities
- Visual flow for multi-step operations
- Best for complex agentic workflows

**Zed**
- Rust-based, very fast
- Emerging agentic features
- Multi-player editing
- Best for performance and modern development

**Trade-offs of IDEs vs. Terminal Agents:**

| Feature | Terminal Agents | Agentic IDEs |
|---------|---|---|
| Full IDE features | No | Yes |
| Visual interface | No | Yes |
| Scripting/automation | Excellent | Limited |
| Learning curve | Medium | Low-Medium |
| Price | Varies | Often subscription |
| Flexibility | Very high | Medium |

**Speaker Notes:**
Agentic IDEs are fantastic for pure development workflows. If you're building features or fixing bugs in a visual environment, Cursor or Windsurf might be more comfortable than terminal agents. However, they're less suited to automation, scripting, and complex workflows. Many developers use both - terminal agents for heavy lifting, IDE plugins for everyday development.

---

### Slide 15: Category 3 - VS Code Plugins

**Title:** VS Code Plugins: Extending Your Editor

**Content:**

**What Are VS Code Agentic Plugins?**
- Extensions that add agentic capabilities to VS Code
- Keep your familiar VS Code environment
- No need to learn new editor
- Multiple options to choose from

**The Main Options:**

**GitHub Copilot (with Chat)**
- Most widely used
- Excellent code completion + chat interface
- Integrates with GitHub ecosystem
- Good IDE features support

**Cline**
- Strong agentic capabilities
- Good at multi-file changes
- Active development
- Growing community

**Continue**
- Hackable and extensible
- Works with multiple LLM providers
- Good IDE integration
- Open-source option available

**Amazon Q**
- AWS-integrated option
- Good for AWS-heavy teams
- Enterprise focus
- Built-in AWS documentation

**Trade-offs vs. Terminal Agents:**

| Aspect | Terminal Agents | VS Code Plugins |
|--------|---|---|
| IDE integration | Separate | Native |
| Visual feedback | None | Full IDE |
| CLI integration | Excellent | Limited |
| Multi-file preview | Text | Visual with syntax highlighting |
| Learning curve | Medium | Low |
| Availability | Various costs | Many free/freemium |

**Speaker Notes:**
VS Code plugins are the most accessible entry point for new users. You keep your familiar editor, just add agentic capabilities. Many developers start with a VS Code plugin, then graduate to terminal agents for more complex tasks. GitHub Copilot is the market leader because it was first and integrates well with GitHub, but Cline is gaining ground as developers discover it has more agentic features.

---

### Slide 16: Choosing Your Tool(s)

**Title:** Decision Framework: Which Tool to Use?

**Content:**

**Quick Decision Tree:**

```
What's your primary workflow?
│
├─ "I mostly code in VS Code"
│  └─> Start with GitHub Copilot or Cline plugin
│      (Easy, familiar environment)
│
├─ "I want one powerful tool for all tasks"
│  └─> Claude Code in terminal
│      (Most sophisticated agent)
│
├─ "I want to stay open-source and offline"
│  └─> Aider with local Ollama
│      (Privacy, no API keys needed)
│
├─ "I have a huge codebase (1M+ lines)"
│  └─> Gemini CLI in terminal
│      (1M token context window)
│
├─ "I want a complete IDE experience"
│  └─> Cursor or Windsurf
│      (Visual IDE with agents built-in)
│
└─ "I work with OpenAI/AWS ecosystem"
   └─> Codex CLI or Amazon Q
       (Ecosystem integration)
```

**Recommendation for This Course:**
1. Set up Claude Code (primary tool)
2. Try Aider (open-source alternative)
3. Experiment with Cursor (IDE experience)

**Speaker Notes:**
There's no single "best" tool - it depends on your priorities. Think about what matters to you: privacy, cost, ease of use, agentic capabilities, IDE features, or ecosystem integration. Most professional developers use multiple tools for different situations.

---

## SECTION 3: Terminal Agents Installation - DETAILED

---

### Slide 17: Installation Overview

**Title:** Terminal Agents Installation: Roadmap

**Content:**

**What We'll Cover:**

1. **Claude Code** (5-6 slides)
   - Prerequisites
   - Installation
   - Configuration
   - Verification
   - Troubleshooting

2. **Aider** (3-4 slides)
   - Prerequisites
   - Installation
   - Verification

3. **Codex CLI** (3-4 slides)
   - Prerequisites
   - Installation
   - Verification

4. **Gemini CLI** (3-4 slides)
   - Prerequisites
   - Installation
   - Verification

5. **Others** (1-2 slides)
   - Quick references for GitHub Copilot CLI, OpenHands, Goose

**Estimated Time:** 30-45 minutes for full setup

**Speaker Notes:**
We're going to install these tools step-by-step. Have a terminal open and follow along. Each tool has specific prerequisites - make sure you have them before starting. The good news is you can install them in any order and use them side-by-side.

---

### Slide 18: Claude Code Installation - Prerequisites

**Title:** Claude Code: Prerequisites & Requirements

**Content:**

**System Requirements:**
- macOS, Linux, or Windows (with WSL2)
- Terminal/Command line access
- Node.js 18+ (for some features)
- 100MB free disk space

**Required Accounts & Keys:**
1. **Anthropic API Account**
   - Visit: https://console.anthropic.com
   - Create free account (or log in)
   - Billing setup required (pay-as-you-go)
   - Create API key

2. **Your API Key**
   - Keep it safe (like a password)
   - Never commit to git
   - Can be stored in environment variable

**Cost Information:**
- Claude 3.5 Sonnet: $3 per 1M input tokens, $15 per 1M output tokens
- Claude Opus 4.5: $15 per 1M input tokens, $60 per 1M output tokens
- Most tasks cost $0.10-$1.00
- Free tier available for testing

**Checklist:**
- [ ] Terminal access confirmed
- [ ] Anthropic account created
- [ ] API key generated
- [ ] Billing setup configured
- [ ] Know your API key location

**Speaker Notes:**
The biggest prerequisite is the Anthropic API key. If you don't have one yet, that's step one. The API setup takes about 5 minutes. Once you have the key, keep it secret - treat it like a password. You can use free credits initially if Anthropic provides them, but eventually you'll need billing set up.

---

### Slide 19: Claude Code Installation - Installation Process

**Title:** Claude Code: Installation Steps

**Content:**

**Step 1: Install via Homebrew (macOS/Linux)**

```bash
# Update Homebrew first
brew update

# Install Claude Code
brew install claude-code

# Verify installation
claude-code --version
```

**Step 2: Alternatively, Install via npm**

```bash
# Global npm installation
npm install -g @anthropic-ai/claude

# Verify installation
claude --version
```

**Step 3: Configure API Key**

```bash
# Set API key as environment variable (temporary)
export ANTHROPIC_API_KEY="your-key-here"

# OR - Make it permanent (macOS/Linux)
# Add to ~/.bashrc or ~/.zshrc
echo 'export ANTHROPIC_API_KEY="your-key-here"' >> ~/.zshrc
source ~/.zshrc

# Windows PowerShell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "your-key-here", "User")
```

**Step 4: Test Installation**

```bash
# Start Claude Code
claude-code

# Or with specific directory
claude-code /path/to/project
```

**Speaker Notes:**
Installation is straightforward. The Homebrew method is easiest on macOS. The npm method works everywhere. The trickiest part for new users is setting the API key correctly. Make sure you're using the actual API key value, not the placeholder text. If you're unsure about your API key, log into https://console.anthropic.com to find it.

---

### Slide 20: Claude Code Installation - Verification & First Run

**Title:** Claude Code: Verification & First Run

**Content:**

**Verification Checklist:**

```bash
# 1. Check Claude Code is installed
claude-code --version
# Expected output: claude-code version X.X.X

# 2. Check API key is configured
echo $ANTHROPIC_API_KEY
# Expected output: (should show your key, not empty)

# 3. Test with a simple prompt
claude-code "echo 'Hello, Claude!'"
```

**First Run Experience:**

When you run `claude-code`, you'll see:

```
Claude Code v1.0.0
Ready for commands.

You: [waiting for input]
```

**Try These First Commands:**

```bash
# Command 1: List files in current directory
claude-code "show me the files in this directory"

# Command 2: Read a file
claude-code "read the README.md file and summarize it"

# Command 3: Create a new file
claude-code "create a hello.py file that prints 'Hello, World!'"

# Command 4: Run code
claude-code "create and run a Python script that calculates fibonacci numbers"
```

**What to Look For:**
- Agent responds with clear reasoning
- Actions appear as it executes them
- File modifications shown
- Commands execute successfully
- Feedback loop works (agent refines if needed)

**Speaker Notes:**
Your first time running Claude Code can be exciting. You're seeing an AI agent reason about your request in real-time, then execute it. Watch how it approaches the problem - you'll start to understand how to give better instructions.

---

### Slide 21: Claude Code - Troubleshooting & Tips

**Title:** Claude Code: Common Issues & Solutions

**Content:**

**Problem 1: "API key not found"**

```
Error: ANTHROPIC_API_KEY not set
```

**Solutions:**
- Verify key is set: `echo $ANTHROPIC_API_KEY`
- Check key has no leading/trailing spaces
- Restart terminal after setting key
- Use full path: `ANTHROPIC_API_KEY=xxx claude-code`

**Problem 2: "Invalid API key"**

```
Error: Invalid API key or insufficient permissions
```

**Solutions:**
- Double-check key in Anthropic console
- Ensure billing is set up
- Key might have been regenerated
- Copy fresh key from console

**Problem 3: Rate limiting / Quota exceeded**

```
Error: Rate limit exceeded
```

**Solutions:**
- Wait before next request (API rate limits exist)
- Check usage in Anthropic console
- Ensure adequate billing credits
- Consider using cheaper model option

**Problem 4: "Command not found"**

```
claude-code: command not found
```

**Solutions:**
- Verify installation: `npm list -g @anthropic-ai/claude`
- Reinstall: `npm install -g @anthropic-ai/claude`
- Check PATH: `echo $PATH`
- Use full path if needed: `/usr/local/bin/claude-code`

**Pro Tips:**
- Save API key in .env file for projects
- Use `--verbose` flag for debugging
- Check official docs: https://github.com/anthropics/claude-code
- Join Anthropic Discord for community support

**Speaker Notes:**
The most common issue is API key setup. Take your time getting this right. If you're still having issues after these steps, the Anthropic community is very helpful. Don't hesitate to ask in Discord or GitHub discussions.

---

### Slide 22: Aider Installation - Prerequisites

**Title:** Aider: Prerequisites & Setup

**Content:**

**What is Aider?**
- Open-source AI pair programming tool
- Works with multiple LLM providers
- Excellent for multi-file editing
- Community-driven development

**System Requirements:**
- Python 3.8+
- pip (Python package manager)
- Git (for repository management)
- Terminal access

**LLM Provider Options:**

1. **OpenAI (GPT-4)**
   - Requires: OpenAI API key
   - Cost: $0.03-0.06 per request
   - Best for: Balanced quality and cost

2. **Anthropic Claude**
   - Requires: Anthropic API key
   - Cost: Similar to OpenAI
   - Best for: Complex reasoning

3. **Local Models (Ollama)**
   - Requires: Ollama installed
   - Cost: Free
   - Best for: Privacy, offline work
   - Requires: 8GB+ RAM, decent CPU

4. **Other Providers**
   - Google Gemini, Mistral, Cohere, etc.
   - Various costs and capabilities

**Checklist:**
- [ ] Python 3.8+ installed
- [ ] pip available
- [ ] Git installed
- [ ] LLM provider account (choose one)
- [ ] API key available (if not using local models)

**Speaker Notes:**
Aider is more flexible than Claude Code because you can choose your LLM provider. If you want to stay offline, you can use Ollama with local models. If you want the best results, use GPT-4 from OpenAI or Claude from Anthropic.

---

### Slide 23: Aider Installation - Installation Process

**Title:** Aider: Installation Steps

**Content:**

**Step 1: Verify Python Installation**

```bash
# Check Python version (need 3.8+)
python3 --version

# If not installed, install Python 3.10+
# macOS: brew install python@3.10
# Ubuntu: sudo apt-get install python3.10
# Windows: Download from python.org
```

**Step 2: Install Aider via pip**

```bash
# Standard installation
pip install aider-chat

# Or upgrade if already installed
pip install --upgrade aider-chat

# Verify installation
aider --version
```

**Step 3: Configure LLM Provider**

```bash
# For OpenAI (GPT-4)
export OPENAI_API_KEY="your-openai-key"

# For Anthropic Claude
export ANTHROPIC_API_KEY="your-anthropic-key"

# For Ollama (local models)
# No key needed - see Slide 24

# Make persistent (add to ~/.zshrc or ~/.bashrc)
echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
```

**Step 4: Test Installation**

```bash
# Start Aider in current directory
aider

# Or with specific files
aider myfile.py anotherfile.js

# With verbose output
aider --verbose
```

**Speaker Notes:**
Installation is simple with pip. The key decision is which LLM provider to use. Most people start with OpenAI's GPT-4 because it's reliable and widely used. But if you want to try Aider without spending money, Ollama with local models is a great option.

---

### Slide 24: Aider Installation - Ollama Setup (Optional)

**Title:** Aider with Ollama: Offline Local Models

**Content:**

**Why Use Ollama?**
- Run models locally (privacy, no API keys)
- Completely free
- No internet required
- Good for learning
- Works on most laptops

**Prerequisites:**
- macOS 11.6+, Linux, or Windows
- At least 8GB RAM (16GB+ recommended)
- 20GB free disk space
- Decent CPU (M1+ Mac, Ryzen 5+, etc.)

**Step 1: Install Ollama**

```bash
# macOS
brew install ollama

# Linux
curl https://ollama.ai/install.sh | sh

# Windows
# Download from https://ollama.ai

# Verify
ollama --version
```

**Step 2: Pull a Model**

```bash
# Download Mistral (excellent quality, 7B params)
ollama pull mistral

# Or CodeLlama (specialized for coding)
ollama pull codellama

# Download takes 5-10 minutes first time
```

**Step 3: Start Ollama Server**

```bash
# In a separate terminal, keep running
ollama serve

# Or run in background
ollama serve &
```

**Step 4: Configure Aider for Ollama**

```bash
# Tell Aider to use Ollama
aider --model ollama/mistral

# Or set as default
export AIDER_LLM_MODEL="ollama/mistral"
aider
```

**Available Models for Coding:**
- mistral (good general purpose, fast)
- codellama (specialized for code)
- neural-chat (smaller, lighter)

**Speaker Notes:**
Ollama is fantastic for learning and experimentation. First run downloads the model (5-10 minutes), but subsequent runs are instant. The trade-off is local models are less powerful than GPT-4. But for many tasks, Mistral is excellent and completely free.

---

### Slide 25: Aider Verification & First Session

**Title:** Aider: Verification & First Session

**Content:**

**Verification:**

```bash
# Check installation
aider --version

# Check default model config
aider --help | grep model

# Test basic session
aider
# You should see the Aider prompt
```

**First Session Example:**

```
Aider v0.25.0
Model: gpt-4 (or your configured model)

/aider> Add a function to calculate fibonacci numbers

# Aider responds with:
# - Analysis of request
# - Code it will create/modify
# - Diff showing changes
# - Ready for your feedback
```

**Key Commands in Aider:**

```bash
# In the Aider interactive session:

/add filename.py          # Add file to session
/drop filename.py         # Remove file from session
/ls                       # List files in session
/undo                     # Undo last change
/exit                     # Exit Aider

# You can also just type naturally:
# "Refactor this function to be more efficient"
# "Fix the bug in the login code"
```

**What to Expect:**
- Aider shows diffs clearly
- You can review changes before applying
- Multi-turn conversations work naturally
- Can reference specific functions
- Excellent for pair programming feel

**Speaker Notes:**
The Aider interface feels like pair programming. You describe what you want, Aider shows you the diff, you can ask follow-up questions. The diff-based approach is excellent for code review - you're always in control.

---

### Slide 26: Codex CLI Installation - Prerequisites & Setup

**Title:** Codex CLI: Installation & Configuration

**Content:**

**About Codex CLI:**
- OpenAI's official terminal interface
- Optimized for code generation
- Integrates with OpenAI ecosystem
- Good for quick tasks

**Prerequisites:**
- Python 3.6+
- pip package manager
- OpenAI API account
- OpenAI API key

**Account Setup:**

```bash
# 1. Create OpenAI account at https://platform.openai.com
# 2. Create API key at https://platform.openai.com/api-keys
# 3. Set up billing at https://platform.openai.com/account/billing

# Pricing (pay-as-you-go):
# GPT-4: $0.03 input / $0.06 output per 1K tokens
# GPT-3.5: $0.0005 input / $0.0015 output per 1K tokens
```

**Installation Steps:**

```bash
# Install via pip
pip install openai

# Set up API key
export OPENAI_API_KEY="your-api-key-here"

# Make persistent (add to ~/.zshrc or ~/.bashrc)
echo 'export OPENAI_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
python -c "import openai; print(openai.__version__)"
```

**Configuration (Optional):**

```bash
# You can also use config file (~/.openai/credentials)
# Or pass key directly: OPENAI_API_KEY=xxx python script.py
```

**Common Issues:**
- "No module named 'openai'" → Install: `pip install openai`
- "Invalid API key" → Check key at https://platform.openai.com/api-keys
- "Insufficient quota" → Check billing at https://platform.openai.com/account/billing

**Speaker Notes:**
Codex CLI setup is straightforward. The main thing is getting the OpenAI API key configured correctly. If you're already using OpenAI services, this integrates seamlessly into your workflow.

---

### Slide 27: Codex CLI Usage Examples

**Title:** Codex CLI: First Commands

**Content:**

**Basic Usage Pattern:**

```bash
# General syntax
openai api completions.create \
  --model gpt-4 \
  --prompt "your prompt here"

# Or simpler with Chat API
openai api chat.completions.create \
  --model gpt-4 \
  --messages '[{"role":"user","content":"write hello world in python"}]'
```

**Practical Examples:**

**Example 1: Generate Python Function**

```bash
openai api chat.completions.create \
  --model gpt-4 \
  --messages '[{"role":"user","content":"Write a Python function to check if a number is prime"}]'
```

**Example 2: Explain Code**

```bash
openai api chat.completions.create \
  --model gpt-4 \
  --messages '[{"role":"user","content":"Explain this code: for i in range(10): print(i)"}]'
```

**Example 3: Generate Tests**

```bash
openai api chat.completions.create \
  --model gpt-4 \
  --messages '[{"role":"user","content":"Generate pytest test cases for a fibonacci function"}]'
```

**Creating a Wrapper Script:**

```bash
#!/bin/bash
# Save as ~/bin/codex

openai api chat.completions.create \
  --model gpt-4 \
  --temperature 0.7 \
  --messages "[{\"role\":\"user\",\"content\":\"$@\"}]"

# Usage: codex "write hello world in python"
```

**Speaker Notes:**
Codex CLI is more about code generation than agentic behavior. It's great for generating snippets quickly, but doesn't have the iterative problem-solving of Claude Code or Aider. Use it when you need fast, focused code generation.

---

### Slide 28: Gemini CLI Installation - Prerequisites

**Title:** Gemini CLI: Setup & Configuration

**Content:**

**About Gemini CLI:**
- Google's official terminal interface
- Access to Gemini 1.5 Pro/Flash models
- 1 million token context window
- Competitive pricing

**Why Choose Gemini?**
- Largest context window (1M tokens)
- Excellent for large codebase analysis
- Good price per token
- Multimodal support (images, documents)
- Google Cloud integration

**Prerequisites:**
- Python 3.8+
- pip package manager
- Google Cloud account
- Google Cloud project with Gemini API enabled

**Google Cloud Setup:**

```bash
# 1. Create Google Cloud project
# - Visit: https://console.cloud.google.com
# - Create new project
# - Enable Gemini API

# 2. Create API key
# - Go to: https://aistudio.google.com/app/apikey
# - Create new API key
# - Copy and save securely

# 3. Set environment variable
export GOOGLE_API_KEY="your-key-here"

# Make persistent
echo 'export GOOGLE_API_KEY="your-key"' >> ~/.zshrc
source ~/.zshrc

# Verify
echo $GOOGLE_API_KEY
```

**Pricing:**
- Gemini 1.5 Flash: $0.075 per 1M input / $0.30 per 1M output tokens
- Gemini 1.5 Pro: $7.50 per 1M input / $30 per 1M output tokens
- Free tier: 60 requests per minute

**Speaker Notes:**
Gemini is worth setting up if you work with large codebases. The 1 million token context is game-changing - you can fit entire projects into one conversation. Pricing is competitive and the free tier is generous for experimentation.

---

### Slide 29: Gemini CLI Installation & Usage

**Title:** Gemini CLI: Installation and First Use

**Content:**

**Installation:**

```bash
# Install Google AI Python library
pip install google-generativeai

# Verify installation
python -c "import google.generativeai as genai; print(genai.__version__)"
```

**Basic Usage:**

```bash
# Create a Python script (gemini_chat.py)
import google.generativeai as genai

# Configure with your API key
genai.configure(api_key="YOUR_API_KEY")

# Create model
model = genai.GenerativeModel("gemini-1.5-pro")

# Send message
response = model.generate_content("Write a hello world program in Python")
print(response.text)
```

**Using in Terminal:**

```bash
# Save as ~/bin/gemini
#!/usr/bin/env python3
import google.generativeai as genai
import sys
import os

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("Error: GOOGLE_API_KEY not set")
    sys.exit(1)

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content(" ".join(sys.argv[1:]))
print(response.text)

# Usage: gemini "write fibonacci in python"
```

**Multi-turn Conversation:**

```python
# For longer conversations, use chat
model = genai.GenerativeModel("gemini-1.5-pro")
chat = model.start_chat(history=[])

# First turn
response1 = chat.send_message("Explain quantum computing in simple terms")
print(response1.text)

# Follow-up turn (context maintained)
response2 = chat.send_message("Now explain superposition")
print(response2.text)
```

**Advanced: Large File Processing**

```python
# Upload large files (code, docs, etc.)
import google.generativeai as genai

file = genai.upload_file("large_codebase.txt")
model = genai.GenerativeModel("gemini-1.5-pro")
response = model.generate_content([
    "Analyze this codebase for architecture patterns:",
    file
])
```

**Speaker Notes:**
Gemini CLI is slightly more code-heavy than the others - you're writing Python scripts rather than using a pre-made CLI tool. But this flexibility is also a strength. The large context window makes it ideal for analyzing entire projects at once.

---

### Slide 30: Gemini CLI Verification & Large Context Example

**Title:** Gemini CLI: Verification & Large Context Power

**Content:**

**Verification:**

```bash
# Check API key is set
echo $GOOGLE_API_KEY

# Test basic functionality
python3 << 'EOF'
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

# Simple test
response = model.generate_content("List 5 Python best practices")
print(response.text)
EOF
```

**Real-World Example: Analyzing Large Codebase**

```python
# analyze_codebase.py
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

# Read entire project
codebase = ""
for file in ["main.py", "utils.py", "config.py", "database.py"]:
    with open(file) as f:
        codebase += f"=== {file} ===\n{f.read()}\n\n"

# Analyze with Gemini (can handle 1M tokens!)
response = model.generate_content(f"""
Analyze this codebase and provide:
1. Architecture overview
2. Potential performance issues
3. Security concerns
4. Refactoring suggestions

Codebase:
{codebase}
""")

print(response.text)
```

**Use Cases for Large Context:**
- Full codebase analysis and refactoring planning
- Multi-file bug investigation
- Architecture design discussions
- Documentation generation from code
- Test coverage analysis

**Speaker Notes:**
The 1 million token context window is Gemini's killer feature for code work. You can feed it your entire project and ask deep architectural questions. This is something no other tool can do as effectively.

---

### Slide 31: Other Terminal Agents - Quick Reference

**Title:** Other Terminal Agents: Quick Setup Guide

**Content:**

**GitHub Copilot CLI**

```bash
# Install
npm install -g @github/copilot-cli

# Setup (links to GitHub account)
copilot --setup

# Usage
copilot "generate a nodejs server"
copilot --explain "what does this command do?"
```

**Strengths:** GitHub integration, familiar to Copilot users
**Best for:** GitHub-centric workflows
**Cost:** GitHub Copilot subscription ($10/month)

---

**OpenHands**

```bash
# Install from source
git clone https://github.com/All-Hands-AI/OpenHands
cd OpenHands
pip install -e .

# Configure with API key (OpenAI or Claude)
export OPENAI_API_KEY="your-key"

# Run
python -m openhands
```

**Strengths:** Open-source, extensible framework
**Best for:** Researchers, customization needs
**Status:** Rapidly evolving

---

**Goose**

```bash
# Install
pip install goose-ai

# Configure
export ANTHROPIC_API_KEY="your-key"

# Run
python -m goose --task "refactor my code"
```

**Strengths:** Simple, hackable, Anthropic-based
**Best for:** Learning, experimentation
**Status:** Growing community

---

**Continue CLI** (from Continue.dev)

```bash
# Install as part of Continue
pip install continue

# Or use through VS Code extension (covered in next section)
```

**Strengths:** Emerging, good VS Code integration
**Best for:** VS Code users wanting CLI option
**Status:** Actively developed

**Speaker Notes:**
These four tools are worth monitoring but not essential for this course. They're either newer, more specialized, or versions of larger platforms. The first four tools (Claude Code, Aider, Codex CLI, Gemini CLI) are the main focus.

---

## SECTION 4: Agentic IDEs Installation

---

### Slide 32: Agentic IDEs Overview

**Title:** Agentic IDEs: Installation & Setup

**Content:**

**What to Expect:**
- Simplified installation (no API keys to configure manually)
- Integrated agent + editor experience
- Visual code editor with built-in AI
- Familiar VS Code-like interface

**The Three Main Options Recap:**

1. **Cursor** - Best entry point
   - Based on VS Code (most familiar)
   - Mature, stable
   - Strong agentic features

2. **Windsurf** - Most advanced
   - New but sophisticated
   - Best agentic orchestration
   - Higher price point

3. **Zed** - Highest performance
   - Rust-based, very fast
   - Emerging agentic features
   - Modern architecture

**Installation Overview by Tool:**
- Cursor: Download DMG/installer
- Windsurf: Download from website
- Zed: Download or brew install

**Time Required:** 10-15 minutes per IDE

**Speaker Notes:**
Installing agentic IDEs is much simpler than terminal agents - you mostly just download and configure your API key. The tradeoff is you're in a different editor environment, though Cursor is very similar to VS Code so the learning curve is minimal.

---

### Slide 33: Cursor Installation - macOS & Linux

**Title:** Cursor: Installation & First Launch

**Content:**

**System Requirements:**
- macOS 10.12+ OR Linux (Ubuntu 18.04+)
- 2GB RAM minimum (4GB+ recommended)
- 500MB free disk space
- API key for preferred LLM provider

**Installation - macOS:**

```bash
# Option 1: Download DMG from https://www.cursor.sh/
# Open the downloaded DMG file
# Drag Cursor to Applications folder

# Option 2: Homebrew
brew install cursor

# Verify
/Applications/Cursor.app/Contents/MacOS/Cursor --version
```

**Installation - Linux:**

```bash
# Ubuntu/Debian
wget https://download.cursor.sh/linux -O cursor.deb
sudo dpkg -i cursor.deb

# Or download AppImage
wget https://download.cursor.sh/linux/appimage
chmod +x cursor-*.AppImage
./cursor-*.AppImage
```

**First Launch:**

1. Open Cursor.app
2. You'll see welcome screen
3. Choose preferred language model:
   - GPT-4 (OpenAI)
   - Claude (Anthropic)
   - Gemini (Google)
   - Local models

4. Enter API key when prompted
5. Create/open project

**Configuration:**

- Settings: Cursor menu > Settings
- API keys: Settings > Models & API Keys
- Keybindings: Settings > Keybindings
- Theme: Settings > Theme

**Speaker Notes:**
Cursor installation is straightforward - it's basically a VS Code clone with AI integrated. If you know VS Code, you already know most of Cursor's interface. The main decision is which LLM to use - you can change it anytime in settings.

---

### Slide 34: Cursor Usage & Features

**Title:** Cursor: Key Features & Workflow

**Content:**

**Key Features:**

1. **Cmd+K Code Generation**
   - Highlight code, press Cmd+K
   - Describe changes naturally
   - Agent rewrites code automatically

2. **Cmd+L Chat Interface**
   - Side chat with full context
   - Ask questions about code
   - Multistep refactoring

3. **Tab/Autocomplete**
   - Intelligent code completion
   - Understands your codebase
   - Shows prediction intent

4. **Agent Mode**
   - Plan complex multi-file changes
   - Apply them automatically
   - Full refactoring capabilities

**Common Workflow:**

```
1. Open project in Cursor
2. Select code you want to improve
3. Press Cmd+K
4. Type: "Refactor this to use async/await"
5. Review changes
6. Accept or iterate

Or:

1. Cmd+L to open chat
2. "Help me understand this authentication flow"
3. Agent explains and shows relevant code
4. Ask follow-up questions
5. Ask agent to make specific changes
```

**Pro Tips:**

- Use `@codebase` in chat to reference entire project
- Use `@file filename.py` to focus on specific file
- Create Cursor Rules in .cursor/rules for project preferences
- Use Custom Instructions for consistent style

**Storage & Privacy:**
- Code stays on your machine
- API keys stored locally (securely)
- Conversations can be saved locally
- No code sent to Cursor server, only to your LLM provider

**Speaker Notes:**
Cursor is designed for developer comfort. If you use VS Code, you'll feel at home immediately. The Cmd+K and Cmd+L shortcuts become second nature quickly. Most developers find themselves using Cursor for routine development and terminal agents for complex multi-step tasks.

---

### Slide 35: Windsurf Installation & Features

**Title:** Windsurf: Next-Generation Agentic IDE

**Content:**

**System Requirements:**
- macOS 11+, Linux, or Windows
- 4GB RAM minimum (8GB+ recommended)
- 1GB free disk space
- API key for LLM provider

**Installation:**

```bash
# macOS via Homebrew
brew install windsurf

# Or download from https://www.windsurf.dev
# Download appropriate installer for your OS

# Linux (Ubuntu/Debian)
# Download .deb or .AppImage from website
sudo dpkg -i windsurf.deb

# Windows
# Download installer and run
```

**First Launch & Configuration:**

1. Open Windsurf
2. Select LLM provider
3. Enter API key
4. Create/open workspace

**Windsurf's Key Differentiators:**

1. **Cascade Mode**
   - Multi-file agentic orchestration
   - Plans changes across multiple files
   - Shows full diff before applying

2. **Flow Feature**
   - Visualize agent's reasoning
   - See step-by-step thought process
   - Better control over agent actions

3. **Workspace Integration**
   - Multiple files open simultaneously
   - Agent has context of entire workspace
   - Coordinated changes across files

4. **Advanced Context Window**
   - Better at understanding large projects
   - Maintains context across long sessions
   - Excellent codebase awareness

**Core Workflows:**

```
Workflow 1: "Refactor payments module"
1. Open payments folder in Windsurf
2. Ask: "Refactor the entire payments system to use dependency injection"
3. Windsurf analyzes all files
4. Shows Cascade plan for changes
5. You approve or modify plan
6. All files updated together

Workflow 2: "Add authentication"
1. Ask: "Add OAuth2 authentication to this app"
2. Windsurf creates plan
3. Shows each file change in context
4. Apply all changes atomically
```

**Speaker Notes:**
Windsurf is newer but impressive. If you want the most sophisticated agentic IDE experience, Windsurf is it. The Cascade feature for multi-file orchestration is particularly powerful. The downside is it's a bit more expensive than Cursor.

---

### Slide 36: Zed Installation & Overview

**Title:** Zed: High-Performance Agentic Editor

**Content:**

**About Zed:**
- Rust-based editor (extremely fast)
- Modern architecture
- Emerging agentic features
- Multiplayer editing support
- Lightweight and responsive

**System Requirements:**
- macOS 11+ (best experience on Apple Silicon)
- Linux support (growing)
- Windows support (in development)
- 2GB RAM minimum

**Installation:**

```bash
# macOS via Homebrew
brew install zed

# Or download from https://zed.dev
# Download DMG and run

# Linux (requires manual build currently)
git clone https://github.com/zed-industries/zed
cd zed
cargo install --path crates/zed
```

**Zed Agentic Features:**

1. **AI Chat Panel**
   - Right sidebar with AI chat
   - Context-aware code understanding
   - Inline code generation

2. **Inline Editing**
   - Request code generation inline
   - Immediate visual feedback
   - One-line to multi-block changes

3. **LLM Provider Selection**
   - Supports multiple providers
   - Easy switching between models
   - Clear token usage tracking

**Configuration:**

```
Settings JSON (~/.config/zed/settings.json):

{
  "assistant": {
    "default_model": "gpt-4",
    "openai_api_key": "your-key"
  }
}
```

**Performance Characteristics:**
- Starts in <1 second
- Syntax highlighting is instant
- Navigation is snappy
- Minimal memory usage

**Trade-offs:**
- Newer project (less mature than Cursor)
- Some features still in development
- Smaller ecosystem of extensions
- Windows support still coming

**Best Use Cases:**
- Performance-critical workflows
- Lightweight machine development
- Teams wanting modern architecture
- Learning from cutting-edge code practices

**Speaker Notes:**
Zed is worth watching. It's the fastest editor in this list and the architecture is superior. However, it's newer and less feature-complete. If speed matters to you and you're comfortable with a newer tool, Zed is excellent. For absolute stability and feature completeness, Cursor remains the safer choice.

---

### Slide 37: Comparing the Three Agentic IDEs

**Title:** Agentic IDEs: Side-by-Side Comparison

**Content:**

| Feature | Cursor | Windsurf | Zed |
|---------|--------|----------|-----|
| **Maturity** | Mature (2024) | Newer (2024) | Emerging (2024) |
| **Ease of Setup** | Very easy | Easy | Medium |
| **VS Code Familiarity** | Highest | High | Lower |
| **Multi-file Agentic** | Good | Excellent | Good |
| **Speed** | Fast | Medium | Very Fast |
| **Price** | $20/month | $30/month | Free tier available |
| **LLM Flexibility** | All major providers | All major providers | All major providers |
| **Learning Curve** | Low | Low | Medium |
| **Collaboration Features** | None | Limited | Excellent |
| **Extension Ecosystem** | Large | Growing | Growing |
| **Linux Support** | Full | Full | Partial |
| **Windows Support** | Full | Full | In development |

**Recommendation Matrix:**

**Choose Cursor if:**
- You want safest, most stable choice
- You know VS Code very well
- You want large extension ecosystem
- You're new to agentic tools

**Choose Windsurf if:**
- You want most sophisticated agentic features
- You do complex multi-file refactoring
- You want best "cascade" planning
- Budget isn't a concern

**Choose Zed if:**
- You want peak performance
- You like modern, cutting-edge tools
- You value speed and responsiveness
- You're comfortable with newer projects

**Speaker Notes:**
There's no objectively "best" choice. Most professional developers would pick Cursor because it's stable, familiar, and well-supported. But Windsurf and Zed each have compelling reasons to consider them. Many developers use multiple IDEs for different contexts.

---

## SECTION 5: VS Code Plugins Installation

---

### Slide 38: VS Code Plugins Overview

**Title:** VS Code Plugins: Adding AI to Your Existing Editor

**Content:**

**Why VS Code Plugins?**
- Keep your existing editor and configuration
- Lower barrier to entry
- Many free or freemium options
- Easier to compare multiple tools
- Familiar environment

**The Main Contenders:**

1. **GitHub Copilot** - Most popular
   - Market leader
   - GitHub integration
   - Code completion + chat
   - $10/month

2. **Cline** - Strong agentic option
   - Multi-file capabilities
   - Good agent reasoning
   - Free/freemium model
   - Growing popularity

3. **Continue** - Most extensible
   - Open-source core
   - Works with any LLM
   - Highly customizable
   - Free option available

4. **Amazon Q** - Enterprise option
   - AWS integration
   - Enterprise support
   - Free tier for individuals
   - AWS-focused features

**Installation Overview:**
- All install via VS Code Extensions marketplace
- Most take < 5 minutes to set up
- Require LLM API keys
- Work alongside normal VS Code

**Time Required:** 20-30 minutes total for setup of all four

**Speaker Notes:**
VS Code plugins are the easiest entry point into agentic tools. You don't have to learn a new editor, just add extensions. This makes them perfect for trying out different tools before committing to a terminal agent or full IDE switch.

---

### Slide 39: GitHub Copilot Installation & Setup

**Title:** GitHub Copilot: Installation & Workflow

**Content:**

**Prerequisites:**
- VS Code installed
- GitHub account
- GitHub Copilot subscription ($10/month) OR GitHub Copilot Free tier

**Installation Steps:**

1. **Install Extension**
   - Open VS Code
   - Click Extensions (Cmd+Shift+X)
   - Search "GitHub Copilot"
   - Click Install
   - Wait for installation to complete

2. **Authenticate**
   - Extension prompts to sign in to GitHub
   - Open https://github.com/login/device
   - Enter provided device code
   - Authorize VS Code
   - Return to VS Code

3. **Verify**
   - GitHub Copilot icon appears in sidebar
   - You see Copilot menu in bottom status bar

**Pricing Tiers:**

| Tier | Cost | Features |
|------|------|----------|
| Free | Free | Chat, limited completions, suggestions |
| Individual | $10/month | Unlimited completions, chat, priority |
| Business | $19/user/month | Team management, audit logs |

**Core Features:**

```
1. Code Completion (Tab key)
   - Type function signature
   - Copilot suggests implementation
   - Press Tab to accept

2. Chat Interface (Cmd+Shift+I)
   - Open chat sidebar
   - Ask questions about code
   - Multi-turn conversations
   - Can select code for context

3. Inline Comments
   - Write comment describing what code should do
   - Copilot generates implementation below
   - Excellent for TDD approach

4. Code Explanation
   - Select code
   - Right-click > Explain
   - Copilot explains functionality
```

**Key Keybindings:**

```bash
Cmd+Shift+I         # Open Copilot chat
Tab                 # Accept suggestion
Escape              # Reject suggestion
Alt+]               # Next suggestion
Alt+[               # Previous suggestion
Cmd+Up/Down         # Cycle through suggestions
```

**Configuration:**
- Settings > GitHub Copilot
- Enable/disable features
- Choose inline suggestions
- Set auto-completion behavior

**Speaker Notes:**
GitHub Copilot is the market leader because it was first and integrated deeply with GitHub. The free tier is quite generous - you get basic features without paying. Many developers use Copilot for everyday coding, then switch to more agentic tools for complex tasks.

---

### Slide 40: Cline, Continue, and Amazon Q Setup

**Title:** VS Code Plugins: Cline, Continue, and Amazon Q

**Content:**

**Cline Installation**

```
1. Open VS Code Extensions
2. Search "Cline"
3. Install Cline extension
4. Configure API key:
   - Settings > Cline > API Key
   - Paste your OpenAI, Anthropic, or other provider key
5. Click Cline icon in sidebar to start
```

**Cline Strengths:**
- Strong multi-file editing
- Excellent agentic reasoning
- Good for complex tasks
- Works with many LLM providers
- Growing community

**Continue Installation**

```
1. Open VS Code Extensions
2. Search "Continue"
3. Install Continue extension
4. Opens welcome dialog
5. Select your LLM provider:
   - OpenAI, Anthropic, Ollama, etc.
6. Enter API key
7. Create ~/continue/config.json (optional) for customization
```

**Continue Strengths:**
- Most customizable option
- Open-source core
- Excellent for VS Code power users
- Great documentation
- Can use local models via Ollama

**Amazon Q Installation**

```
1. Open VS Code Extensions
2. Search "Amazon Q"
3. Install Amazon Q extension
4. Sign in with AWS Account
5. Authorize VS Code
6. Ready to use
```

**Amazon Q Strengths:**
- AWS integration (CodeCommit, CodeGuru, etc.)
- Free tier for individual developers
- Enterprise support available
- Specialized for AWS workflows
- Good documentation

**Comparison Table:**

| Plugin | Best For | Price | LLM Flexibility | Setup Time |
|--------|----------|-------|---|---|
| **Copilot** | Everyday coding, teams | $10/mo | Limited (OpenAI) | 5 min |
| **Cline** | Complex tasks, multi-file | Free | High (any provider) | 5 min |
| **Continue** | Customization, power users | Free | Very high | 10 min |
| **Amazon Q** | AWS teams, enterprise | Free-$30/mo | Limited (AWS) | 5 min |

**Quick Start Recommendation:**

1. Install **GitHub Copilot** first (familiar, popular)
2. Try **Cline** for more agentic features
3. Experiment with **Continue** for customization
4. Use **Amazon Q** if you work with AWS

**Speaker Notes:**
By the end of these plugins, you've got a full toolkit in VS Code. Different plugins excel at different tasks. Many developers install all four and use them contextually. GitHub Copilot for daily coding, Cline for complex refactoring, Continue for highly customized workflows, Amazon Q if you're on AWS.

---

### Slide 41: Practical Setup Workflow

**Title:** Complete Setup Workflow: Everything Together

**Content:**

**Total Setup Time:** 60-90 minutes

**Recommended Installation Order:**

```
Phase 1: Terminal Agents (30-40 minutes)
├─ Claude Code (10 minutes)
├─ Aider (5 minutes)
├─ Gemini CLI or Codex CLI (10 minutes)
└─ Test each (5-10 minutes)

Phase 2: One Agentic IDE (10-15 minutes)
├─ Download & install (5 minutes)
├─ Configure API keys (3 minutes)
├─ Create test project (2 minutes)
└─ Test basic features (5 minutes)

Phase 3: VS Code Plugins (20-30 minutes)
├─ GitHub Copilot (5 minutes)
├─ Cline (5 minutes)
├─ Continue (5 minutes)
├─ Amazon Q (5 minutes)
└─ Test each (5-10 minutes)
```

**Verification Checklist:**

Terminal Agents:
- [ ] Claude Code runs and accepts prompts
- [ ] Aider creates files/modifies code successfully
- [ ] Gemini CLI or Codex CLI returns responses
- [ ] All API keys configured correctly

IDE:
- [ ] IDE launches without errors
- [ ] Chat interface responds
- [ ] Code generation works
- [ ] API key configured

VS Code Plugins:
- [ ] All 4 plugins installed in Extensions
- [ ] Each plugin shows status (connected/ready)
- [ ] Test prompt in each generates response
- [ ] Configuration saved

**Quick Diagnostics Commands:**

```bash
# Verify all tools installed
which claude-code
which aider
pip show google-generativeai
pip show openai
code --version
echo $ANTHROPIC_API_KEY
echo $OPENAI_API_KEY
echo $GOOGLE_API_KEY
```

**Troubleshooting Workflow:**

```
Tool not working?
├─ Check API key is set: echo $API_KEY
├─ Verify credentials valid (log into provider console)
├─ Check command is installed: which tool-name
├─ Reinstall if needed: pip install --upgrade tool-name
└─ Check internet connection and API rate limits
```

**Speaker Notes:**
This is ambitious - you'll have 8+ different tools set up by the end. This is intentional. You want options and familiarity with the different approaches. Most developers settle on 3-4 favorites, but having tried them all gives you perspective on which tool is best for each task.

---

### Slide 42: Key Takeaways & Next Steps

**Title:** Part 1 Summary: Introduction & Installation

**Content:**

**What You've Learned:**

1. **Agentic Tools Fundamentals**
   - What agentic tools are and how they differ from traditional AI coding tools
   - The agent loop: observe, plan, execute, refine
   - Real-world examples of agent workflows

2. **The Three Categories**
   - Terminal-based agents (most powerful)
   - Agentic IDEs (optimized editors)
   - VS Code plugins (integrated approach)

3. **Specific Tools**
   - 8+ terminal agents thoroughly covered
   - 3 agentic IDEs reviewed
   - 4 VS Code plugins explored

4. **Installation & Configuration**
   - Step-by-step setup for all major tools
   - Troubleshooting common issues
   - Verification procedures

**Tools You've Installed:**

**Terminal Agents:**
- [ ] Claude Code
- [ ] Aider
- [ ] Gemini CLI
- [ ] Codex CLI

**IDEs:**
- [ ] Cursor (recommended starting point)

**VS Code Plugins:**
- [ ] GitHub Copilot
- [ ] Cline
- [ ] Continue

**Next Steps (Part 2: Workflows & Best Practices):**

Coming up, we'll cover:
1. How to effectively prompt agentic tools
2. Multi-step problem solving workflows
3. Integration with git and CI/CD
4. When to use which tool
5. Advanced patterns and techniques

**Resources & Support:**

**Official Documentation:**
- Claude Code: https://docs.anthropic.com
- Aider: https://aider.chat/docs
- Cursor: https://docs.cursor.sh
- Windsurf: https://www.windsurf.dev/docs

**Community:**
- Anthropic Discord: https://discord.gg/anthropic
- Aider GitHub Discussions
- Cursor Discord
- Continue Slack community

**Your Challenge for Part 2:**

Try this with your installed tools:
1. Pick a small project from your GitHub
2. Ask each tool to "Identify potential bugs in this code"
3. Compare responses
4. Notice which tool was most helpful
5. Understand why

This will prepare you for strategic tool selection in Part 2.

**Speaker Notes:**
You've just installed a comprehensive toolkit. Different tools will click with different people - that's normal. Some of you will prefer terminal agents for their power. Others will love the IDE experience. Some will stick with VS Code plugins. The key is having tried them all so you can make informed decisions. In Part 2, we'll focus on how to use these tools effectively, not just how to install them. The real learning begins there.

---

## END OF PART 1

**Total Slides: 42**

**Document Complete.**

This comprehensive slideshow covers:
- 6 slides on "What are Agentic Coding Tools"
- 10 slides on "The Three Categories Overview"
- 19 slides on "Terminal Agents Installation" (detailed for Claude Code, Aider, Codex, Gemini)
- 5 slides on "Agentic IDEs Installation"
- 4 slides on "VS Code Plugins Installation"

Each slide includes:
- Slide title
- Main content with bullet points, code blocks, tables, and ASCII diagrams
- Detailed speaker notes for presenters
- Practical, immediately actionable information

The document is designed for teaching purposes with clear progression, verification steps, and troubleshooting guidance for each tool.
