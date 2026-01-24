# VS Code Agentic Extensions Survey (2026)

## Executive Summary

This document provides a comprehensive analysis of major agentic AI extensions for Visual Studio Code as of January 2026. These tools represent the evolution from simple code completion to autonomous, multi-step coding agents that can plan, implement, test, and debug code with minimal human intervention.

---

## 1. GitHub Copilot (with Agent Mode)

### Overview
GitHub Copilot has evolved beyond autocomplete with the introduction of Agent Mode, transforming it into an autonomous peer programmer capable of multi-step coding tasks.

### Installation
- Available to all VS Code Insiders users (rolling out to Stable)
- Install via VS Code extensions marketplace or bundled with GitHub Copilot subscription
- Access via Copilot Edits view, select "Agent" from mode dropdown

### Key Agentic Capabilities

**Autonomous Operations**
- Determines which files to edit autonomously
- Analyzes codebase and proposes file edits across multiple files
- Executes terminal commands and tests
- Iterates to remediate issues without manual intervention

**Self-Healing**
- Monitors terminal and test output
- Responds to compile and lint errors automatically
- Auto-corrects in a loop until task completion
- Implements error remediation strategies

**Task Examples**
- Create applications from scratch
- Perform refactorings across multiple files
- Write and run tests automatically
- Migrate legacy code to modern frameworks

**Workflow**
1. Determines relevant context and files autonomously
2. Offers both code changes and terminal commands
3. Monitors correctness of edits and command output
4. Remediates issues through iterative correction

### Model Support
- Powered by OpenAI GPT models
- Multi-model support announced (expanding beyond GPT)

### Integration with VS Code
- Native integration through official Microsoft/GitHub partnership
- Deep IDE integration with Copilot Edits view
- Model Context Protocol (MCP) support
- Seamless terminal and test runner integration

### Limitations vs Standalone Tools
- Requires GitHub Copilot subscription (paid service for most users)
- Limited to Microsoft/GitHub ecosystem models primarily
- Less model flexibility compared to open-source alternatives
- Agent mode currently in preview (feature set evolving)

### Pricing
- Included with GitHub Copilot subscription
- Individual: $10/month or $100/year
- Business: $19/user/month

---

## 2. Cline

### Overview
Cline is an open-source autonomous coding agent with Plan/Act modes, MCP integration, and terminal-first workflows. Trusted by 4M+ developers worldwide with nearly 2M downloads within 6 months of release (as of Jan 2025).

### Installation
- Extension ID: `saoudrizwan.claude-dev`
- Install from VS Code Marketplace
- Configure API keys for chosen LLM provider
- Over 750K installs on marketplace

### Key Agentic Capabilities

**Plan-Then-Act Workflow**
- Plan Mode: Shows approach and walks through what's possible before execution
- Act Mode: Implements the agreed-upon plan step-by-step
- User approval gate between planning and execution

**Extensive Development Capabilities**
- Create and edit files autonomously
- Explore large projects and understand context
- Use browser for debugging and testing
- Execute terminal commands (with user permission)
- Handle complex software development tasks step-by-step

**Model Context Protocol (MCP)**
- Extend capabilities through custom tools
- Use community-made servers
- Cline can create and install tools tailored to specific workflows
- Simply ask Cline to "add a tool" and it handles everything

### Model Support
Highly flexible model support:
- Anthropic Claude (Sonnet, Opus)
- OpenAI GPT models
- Google Gemini
- AWS Bedrock
- Azure OpenAI
- GCP Vertex AI
- Cerebras and Groq
- OpenRouter
- Any OpenAI-compatible API
- Local models through LM Studio or Ollama

### Integration with VS Code
- Standalone extension with dedicated sidebar panel
- Terminal integration with command execution
- Browser automation capabilities
- File system operations (create, edit, delete files)
- Permission-based security model

### Limitations vs Standalone Tools
- Requires VS Code IDE (not a standalone CLI tool)
- Permission prompts can interrupt flow (though necessary for security)
- Depends on third-party API keys (user provides their own)
- Less integrated with GitHub-specific workflows than Copilot

### Pricing
- Open-source and free extension
- User pays only for API usage with chosen LLM provider
- No subscription or licensing fees

### Notable Recognition
- Received $32M Seed+A funding
- Compatible with VS Code, Cursor, and Windsurf
- Considered one of the most popular open-source AI coding agents

---

## 3. Continue

### Overview
Continue is the leading open-source AI code agent with three distinct operational modes (Chat, Plan, Agent) and extensive customization options.

### Installation
- Extension ID: `Continue.continue`
- Install from VS Code Marketplace or Open VSX
- Configure models and API keys
- Available as VS Code extension and CLI tool

### Key Agentic Capabilities

**Three Operational Modes**
- Chat Mode: Learning and discussion without changing code
- Plan Mode: Read-only tools for safely exploring and planning
- Agent Mode: Full autonomy with tools to modify codebase based on natural language

**Agent Mode Features**
- Automatically implement code changes
- Fix bugs autonomously
- Run commands using AI-powered decision-making
- Multi-file refactoring and large-scale modifications
- Consistency enforcement across codebase

**Background Agents & Mission Control**
- Mission Control: Single view for all cloud agents (where they run, how they're triggered, reusability)
- Background Agents: Launch in seconds with battle-tested workflows for GitHub, Sentry, Snyk, Linear
- Workflow Deployment: Deploy anywhere (local bash scripts, CI/CD, cron jobs, etc.)
- IDE-triggered workflows: Trigger from VS Code while continuing to code

### Model Support
- Highly customizable model selection
- Different models for different tasks:
  - Agentic workflows: Large reasoning models (e.g., Qwen3-235B)
  - Autocompletion: Smaller, faster models (e.g., Qwen3-Coder-30B)
  - Embeddings: Specialized embedding models (e.g., BGE-multilingual-gemma2)

### Integration with VS Code
- Native extension with chat interface
- MCP tools integration
- Customizable prompts and models
- Tool policies for controlling agent behavior
- CI/CD and automation pipeline integration
- GitHub, Sentry, Snyk, Linear integrations

### Limitations vs Standalone Tools
- Complexity can be overwhelming for beginners
- Requires configuration of multiple models for optimal performance
- Cloud agents require additional setup beyond IDE extension
- Mission Control may require separate deployment infrastructure

### Pricing
- Free for solo developers
- Team pricing: $10/user/month
- Open-source core

---

## 4. Amazon Q Developer

### Overview
Amazon Q Developer provides an agentic coding experience powered by Claude Sonnet 3.7, achieving highest scores on SWE-Bench Leaderboard and Leaderboard Lite.

### Installation
- Extension ID: `AmazonWebServices.amazon-q-vscode`
- Install from VS Code Marketplace
- Sign in with AWS Builder ID or IAM Identity Center
- Available in Visual Studio and JetBrains IDEs as well

### Key Agentic Capabilities

**Autonomous Task Execution**
- Read and write files locally in near real-time
- Run bash commands automatically
- Build code autonomously
- Natural language conversation interface

**Multi-Step Task Automation**
- Implement features autonomously
- Document code automatically
- Refactor code across multiple files
- Perform software upgrades
- Analyze existing codebase before making changes
- Map out step-by-step implementation plans
- Execute all required code changes and tests upon approval

**Direct Environment Interaction**
- Seamless local development environment interaction
- Execute bash commands directly
- Natural conversations about code
- Workspace structure understanding

**Implementation Workflow**
1. User describes feature or task
2. Q Developer analyzes existing codebase
3. Creates step-by-step implementation plan spanning multiple files
4. User reviews and approves plan
5. Executes all code changes, tests, API integrations in minutes

### Model Support
- Powered by Claude Sonnet 3.7 (latest version)
- Optimized specifically for Amazon Q Developer
- No model switching or configuration required

### Integration with VS Code
- Official AWS extension
- Deep integration with AWS services
- Local file system operations
- Terminal and command execution
- Workspace awareness and context understanding

### Limitations vs Standalone Tools
- Tied to AWS ecosystem
- Limited to Claude Sonnet 3.7 (no model choice)
- Requires AWS account and authentication
- May have AWS-specific biases in code generation
- Less flexibility than open-source alternatives

### Pricing
- Free Tier: 50 agentic chat interactions per month (perpetual)
- Pro Tier: Unlimited agentic chat (pricing varies)
- Agentic chat available at no additional cost to both tiers
- No per-token pricing displayed to users

---

## 5. Roo Code

### Overview
Roo Code is an open-source, permission-based AI coding agent with multiple specialized agent modes and full model customizability. Part of the "AI dev team" approach to coding.

### Installation
- Extension ID: `RooVeterinaryInc.roo-cline`
- Install from VS Code Marketplace
- Search "Roo Code" in Extensions view
- Configure API keys for chosen models
- Reload VS Code after installation
- Access via Roo Code icon in Activity Bar

### Key Agentic Capabilities

**Multiple Agent Modes**
- Customizable Modes: Architect, Code, and more
- Pre-defined Cloud Agent Types: Planner, Coder, etc.
- Each mode keeps models focused on specific task boundaries
- Prevents agents from overstepping their designated roles

**Autonomous Capabilities**
- Permission-based by default (asks before every action)
- Auto-Approve mode for extended autonomous operation
- Works for long periods without getting stuck
- Makes informed decisions without constant intervention
- Runs tests automatically
- Opens browser for web-related tasks
- Deep task handling beyond autocomplete

**Development Features**
- Generate code from natural language
- Refactor code with accuracy and speed
- Run tests automatically
- Control and approve file changes
- Command execution with oversight

### Model Support
- Fully model-agnostic
- Integrate any AI model:
  - OpenAI
  - Anthropic
  - Local LLMs via Ollama/LM Studio
  - Any provider of choice
- Open-source and fully customizable

### Integration with VS Code
- Dedicated panel in Activity Bar
- Seamless VS Code integration
- File system operations with permission gates
- Terminal command execution
- Browser automation capabilities

### Limitations vs Standalone Tools
- Permission prompts can slow workflow (though important for safety)
- Requires manual configuration of models and API keys
- Documentation may be less comprehensive than commercial alternatives
- Smaller community compared to GitHub Copilot

### Pricing
- Completely free and open-source
- Pay only for AI model API usage (if using paid APIs)
- No cost if using free or self-hosted models
- No subscription fees

---

## 6. Kilo Code

### Overview
Kilo Code is an all-in-one agentic engineering platform with access to 500+ AI models, parallel agent execution, and comprehensive automation features. One of the most installed agentic extensions (250K+ installs).

### Installation
- Extension ID: `kilocode.Kilo-Code`
- Install from VS Code Marketplace or OpenVSX Registry
- Find Kilo Code icon in Side Bar after installation
- Reload VS Code if prompted
- Includes $20 in free credits to start (no API key required initially)

### Key Agentic Capabilities

**Multi-Model Access**
- 500+ cutting-edge AI models available
- Control tradeoffs between latency, cost, context, and reasoning
- Models include:
  - Gemini 3 Pro
  - Claude 4.5 Sonnet & Opus
  - GPT-5
  - Many others

**Parallel Mode**
- Run multiple AI agents simultaneously
- Tackle multiple problems at once
- Increased efficiency for complex projects

**Advanced Features**
- Natural Language Code Generation: Creates files and checks its own work
- Automated Terminal Execution: Runs install and build scripts autonomously
- Browser Automation: Automates browser for UI verification and web scraping
- Error Detection: Detects terminal errors and attempts automatic fixes
- Inline Autocomplete: Context-aware code suggestions
- Automated Refactoring: Intelligent code restructuring
- Custom Modes: Planning, coding, and debugging modes

### Model Support
- Access to 500+ models from multiple providers
- No vendor lock-in
- Built-in provider with free credits
- Optional: Use your own API keys

### Integration with VS Code
- Dedicated sidebar panel
- Inline autocomplete integration
- Terminal automation
- Browser automation capabilities
- File system operations
- Error detection and remediation

### Limitations vs Standalone Tools
- Large number of models can be overwhelming
- Requires understanding of model tradeoffs for optimal use
- Less established than GitHub Copilot (newer to market)
- Documentation may be evolving

### Pricing
- $20 in free credits included to start
- API keys optional (built-in provider available)
- No commission added on top of model costs
- Pay raw token pricing from underlying providers
- Transparent pricing model

### Notable Statistics
- 250K+ installations
- #1 on OpenRouter
- 750K+ "Kilo Coders"
- 6.1 trillion tokens/month processed

---

## 7. Qodo Gen (formerly CodiumAI)

### Overview
Qodo Gen is a quality-first generative AI coding agent platform focused on code generation, unit testing, and documentation with enterprise-grade agentic workflows. First and only MCP-enabled AI coding agent for JetBrains, also supporting VS Code.

### Installation
- Extension ID: `Codium.codium`
- 751K installs on VS Code Marketplace
- Install from VS Code Marketplace
- Available for both VS Code and JetBrains IDEs

### Key Agentic Capabilities

**Agentic Workflows (Qodo Gen 1.0)**
- Autonomous agents handle coding tasks end-to-end
- Dynamically gather context
- Execute multi-step problem-solving
- 15+ specialized review agents

**Two Types of Agents**
1. Modes: Persona-driven AI agents for ongoing, context-aware conversations
   - Maintain state across interactions
   - Use MCP tools for multi-step tasks
   - Ideal for: Code review, architecture planning, iterative development

2. Workflows: Single-task AI agents with defined processes
   - Execute from start to finish
   - Perfect for repeatable or automated tasks
   - Ideal for: Bug detection, test coverage checks, documentation updates, changelog maintenance

**Model Context Protocol (MCP) Integration**
- Extensible tooling powered by Anthropic's MCP
- Seamless interoperability between AI model and enterprise tools
- Integrations include:
  - Jira
  - Git
  - APIs
  - Databases
  - Custom enterprise tools

**Example MCP Use Case**
- With Jira MCP configured: Ask "Find me a Jira ticket about creating an authentication protocol"
- Agent retrieves relevant information from Jira project directly in IDE

### Model Support
- Supports multiple AI models
- Powered by advanced models for agentic workflows
- Model selection optimized for specific task types

### Integration with VS Code
- Native IDE plugin
- Deep integration with Git
- Jira integration via MCP
- API and database connectivity
- Test generation and execution
- Documentation automation

### Limitations vs Standalone Tools
- Focus on quality and testing may be overkill for simple tasks
- Enterprise features may require additional configuration
- MCP setup required for full enterprise tool integration
- Pricing not fully transparent for enterprise features

### Pricing
- Free tier available
- Enterprise pricing for advanced features
- Team-based licensing model

### Notable Recognition
- First MCP-enabled AI coding agent for JetBrains
- 751K installations on VS Code Marketplace
- Enterprise-grade focus with quality-first approach

---

## Comparative Analysis

### Model Flexibility
1. **Most Flexible**: Cline, Roo Code, Kilo Code (500+ models)
2. **Moderate Flexibility**: Continue (customizable per task)
3. **Limited Flexibility**: GitHub Copilot, Amazon Q Developer, Qodo Gen (fixed models)

### Open Source vs Proprietary
**Open Source**: Cline, Continue, Roo Code, Kilo Code
**Proprietary**: GitHub Copilot, Amazon Q Developer, Qodo Gen

### Best for Autonomous Operations
1. **GitHub Copilot Agent Mode**: Self-healing, iterative correction
2. **Cline**: Plan-then-act with explicit approval gates
3. **Kilo Code**: Parallel agents, error auto-correction
4. **Amazon Q Developer**: Claude 3.7-powered autonomy

### Best for Enterprise Integration
1. **Qodo Gen**: MCP-enabled, Jira/Git/database integration
2. **Amazon Q Developer**: AWS ecosystem integration
3. **Continue**: CI/CD and DevOps tool integration
4. **GitHub Copilot**: GitHub-native integration

### Best for Learning/Exploration
1. **Continue**: Chat mode for learning without code changes
2. **Roo Code**: Permission-based with clear boundaries
3. **Cline**: Plan mode shows approach before execution

### Pricing Comparison (Lowest to Highest Cost)
1. **Free (Pay for APIs)**: Cline, Roo Code, Kilo Code (with free credits)
2. **Free/Freemium**: Continue (free solo, $10/user team), Amazon Q (50 interactions/month free)
3. **Subscription**: GitHub Copilot ($10-19/month), Qodo Gen (enterprise pricing)

### Installation Popularity (by installs)
1. Qodo Gen: 751K installs
2. Kilo Code: 250K+ installs
3. GitHub Copilot: Millions (bundled with GitHub)
4. Cline: 2M downloads in 6 months (4M+ users)
5. Continue: Leading open-source agent
6. Roo Code: Growing rapidly
7. Amazon Q Developer: New entrant (AWS user base)

---

## Key Trends in 2026

### 1. Model Context Protocol (MCP) Adoption
- Cline, Continue, Qodo Gen, and GitHub Copilot have adopted MCP
- Enables extensibility and enterprise tool integration
- Becoming standard for agentic extensions

### 2. Plan-Then-Act Workflows
- Separating planning from execution
- User approval gates between phases
- Reduces errors and increases trust

### 3. Multi-Agent Systems
- Kilo Code's parallel agent execution
- Continue's specialized agents for different tasks
- Roo Code's role-based agent types

### 4. Self-Healing and Error Correction
- Automatic detection of terminal errors
- Iterative correction loops
- Test-driven development automation

### 5. Background and Cloud Agents
- Continue's Mission Control for cloud agents
- Integration with CI/CD pipelines
- Asynchronous agent execution

### 6. Model Diversity
- Moving beyond single-model approaches
- 500+ models available (Kilo Code)
- Task-specific model selection

### 7. Enterprise Focus
- Qodo Gen's quality-first approach
- Amazon Q's AWS integration
- Jira, Linear, Sentry integrations

---

## Recommendations by Use Case

### For Individual Developers
**Best Choice**: Cline or Roo Code
- Free and open-source
- Flexible model support
- Strong community
- Permission-based control

### For GitHub-Centric Workflows
**Best Choice**: GitHub Copilot Agent Mode
- Native GitHub integration
- Self-healing capabilities
- Established ecosystem

### For Enterprise Teams
**Best Choice**: Qodo Gen or Continue
- MCP integration with enterprise tools
- Quality-focused workflows
- Team collaboration features
- CI/CD integration

### For AWS/Cloud-Native Development
**Best Choice**: Amazon Q Developer
- AWS ecosystem integration
- High-performance Claude 3.7
- Free tier available

### For Multi-Model Experimentation
**Best Choice**: Kilo Code or Cline
- Access to 500+ models (Kilo) or flexible model support (Cline)
- Compare different AI approaches
- No vendor lock-in

### For Learning AI-Assisted Development
**Best Choice**: Continue or Roo Code
- Clear separation of modes (Chat vs Agent)
- Safe exploration with Plan mode
- Permission-based learning

### For Maximum Autonomy
**Best Choice**: GitHub Copilot Agent Mode or Kilo Code
- Self-healing and error correction
- Parallel agent execution (Kilo)
- Minimal intervention required

---

## Limitations Compared to Standalone CLI Tools

All VS Code extensions share some limitations compared to standalone CLI tools:

### Integration Constraints
- Require VS Code IDE to be running
- Cannot operate independently of the editor
- IDE overhead affects performance

### Workflow Interruptions
- Permission prompts break flow (though necessary for security)
- IDE updates can break extensions
- Dependent on VS Code extension API changes

### Resource Usage
- Share resources with IDE
- May affect editor performance
- Memory constraints of IDE environment

### Flexibility
- Less scriptable than CLI tools
- Harder to integrate into custom automation
- Limited headless operation capabilities

### Standalone CLI Advantages
- Run in CI/CD without IDE
- Scriptable and automatable
- Lower resource overhead
- Can operate on remote servers
- Better for batch operations

---

## Future Outlook

### Expected Developments in 2026-2027

1. **Increased MCP Adoption**: More extensions will support Model Context Protocol for enterprise tool integration

2. **Multi-Agent Orchestration**: Sophisticated coordination between multiple specialized agents

3. **Improved Error Recovery**: More advanced self-healing and correction strategies

4. **Tighter IDE Integration**: Deeper integration with VS Code features (debugger, git, testing frameworks)

5. **Hybrid CLI/IDE Tools**: Extensions that work both in IDE and as standalone CLI tools

6. **Enhanced Security**: Better sandboxing and permission models for autonomous agents

7. **Cost Optimization**: Smarter model selection to reduce API costs while maintaining quality

8. **Specialized Agents**: Domain-specific agents (web development, data science, systems programming)

---

## Conclusion

The landscape of agentic AI extensions for VS Code in 2026 is diverse and rapidly evolving. The choice of extension depends heavily on specific use cases:

- **GitHub Copilot** leads in autonomy and self-healing but requires subscription
- **Cline** offers the best balance of features, flexibility, and open-source freedom
- **Continue** excels at enterprise integration and team workflows
- **Amazon Q Developer** provides excellent performance for AWS-centric development
- **Roo Code** delivers transparency and control with permission-based operations
- **Kilo Code** stands out with 500+ models and parallel agent execution
- **Qodo Gen** focuses on quality and testing with MCP-enabled enterprise integration

All tools represent significant advances over traditional autocomplete, bringing true agentic capabilities to the IDE. The trend toward Plan-Act workflows, MCP integration, and multi-agent systems suggests that these tools will continue to become more capable and autonomous while maintaining necessary human oversight.

For most individual developers, starting with Cline or Roo Code offers the best combination of capability, flexibility, and cost. Enterprise teams should evaluate Qodo Gen or Continue for their MCP integration and quality-focused features. Developers already invested in GitHub or AWS ecosystems may find Copilot Agent Mode or Amazon Q Developer to be natural choices.

---

## Sources

- [GitHub Copilot features - GitHub Docs](https://docs.github.com/en/copilot/get-started/features)
- [Get started with chat in VS Code](https://code.visualstudio.com/docs/copilot/chat/copilot-chat)
- [Introducing GitHub Copilot agent mode (preview)](https://code.visualstudio.com/blogs/2025/02/24/introducing-copilot-agent-mode)
- [GitHub Copilot coding agent](https://code.visualstudio.com/docs/copilot/copilot-coding-agent)
- [Using agents in Visual Studio Code](https://code.visualstudio.com/docs/copilot/agents/overview)
- [About GitHub Copilot coding agent - GitHub Docs](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-coding-agent)
- [Cline - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)
- [Roo Code vs Cline: Best AI Coding Agents for VS Code (2026)](https://www.qodo.ai/blog/roo-code-vs-cline/)
- [Cline - AI Coding, Open Source and Uncompromised](https://cline.bot/)
- [GitHub - cline/cline](https://github.com/cline/cline)
- [Is Cline the Best AI Coding Agent for VS Code? A Hands-On Review](https://sider.ai/blog/ai-tools/is-cline-the-best-ai-coding-agent-for-vs-code-a-hands-on-review)
- [Continue - open-source AI code agent - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=Continue.continue)
- [Quick Start - Continue](https://docs.continue.dev/ide-extensions/agent/quick-start)
- [GitHub - continuedev/continue](https://github.com/continuedev/continue)
- [Continue.dev](https://www.continue.dev/)
- [Amazon Q Developer elevates the IDE experience with new agentic coding experience](https://aws.amazon.com/blogs/aws/amazon-q-developer-elevates-the-ide-experience-with-new-agentic-coding-experience/)
- [Amazon Q Developer announces a new agentic coding experience in the IDE - AWS](https://aws.amazon.com/about-aws/whats-new/2025/05/amazon-q-developer-agentic-coding-experience-ide/)
- [Introducing an agentic coding experience in Visual Studio and JetBrains IDEs](https://aws.amazon.com/blogs/devops/introducing-an-agentic-coding-experience-in-visual-studio-and-jetbrains-ides/)
- [Amazon Q Developer](https://aws.amazon.com/q/developer/)
- [Amazon Q - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=AmazonWebServices.amazon-q-vscode)
- [Top Agentic AI Tools for VS Code, According to Installs -- Visual Studio Magazine](https://visualstudiomagazine.com/articles/2025/10/07/top-agentic-ai-tools-for-vs-code-according-to-installs.aspx)
- [Best AI Models for Agentic Vibe Coding in VS Code (January 2026) - DEV Community](https://dev.to/danishashko/best-ai-models-for-agentic-vibe-coding-in-vs-code-december-2025-3bkd)
- [Kilo Code - The best AI coding agent for VS Code and JetBrains](https://kilo.ai/)
- [Roo Code – The AI dev team that gets things done](https://roocode.com/)
- [Roo Code - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=RooVeterinaryInc.roo-cline)
- [Roo-Code: AI-Powered Autonomous Coding in VSCode](https://regolo.ai/roo-code-ai-powered-autonomous-coding-in-vscode/)
- [Installing Roo Code](https://docs.roocode.com/getting-started/installing)
- [GitHub - RooCodeInc/Roo-Code](https://github.com/RooCodeInc/Roo-Code)
- [Kilo Code: AI Coding Agent, Copilot, and Autocomplete - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=kilocode.Kilo-Code)
- [GitHub - Kilo-Org/kilocode](https://github.com/Kilo-Org/kilocode)
- [Installing Kilo Code](https://kilo.ai/docs/getting-started/installing)
- [Kilo - Move at Kilo Speed](https://kilo.ai/)
- [Kilo Code: The New Open-Source AI Coding Agent for VS Code - TechNow](https://tech-now.io/en/blogs/kilo-code-the-new-open-source-ai-coding-agent-for-vs-code)
- [Qodo: AI Code Review - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=Codium.codium)
- [Qodo | AI Agents for Code, Review & Workflows](https://www.qodo.ai/)
- [Qodo Gen 1.0: Enterprise-Grade Agentic AI Coding](https://www.qodo.ai/blog/introducing-qodo-gen-1-0-agentic-flows-for-the-enterprise/)
- [Qodo Gen | IDE plugin for AI Code Generation & Testing](https://www.qodo.ai/products/qodo-gen/)
