# Multi-Agent Architectures and Parallelization for Terminal-Based Coding Agents

A comprehensive guide covering Claude Code's Task tool, hierarchical agent workflows, parallelization strategies, and best practices for multi-tier agent orchestration in CLI environments.

---

## Table of Contents

1. [Claude Code's Task Tool and Subagent System](#claude-codes-task-tool-and-subagent-system)
2. [Hierarchical Agent Workflows](#hierarchical-agent-workflows)
3. [Planning → Building → Task Decomposition Patterns](#planning--building--task-decomposition-patterns)
4. [Parallelization Strategies](#parallelization-strategies)
5. [Agent Orchestration in CLI Environments](#agent-orchestration-in-cli-environments)
6. [Multi-Tier Agent Architectures](#multi-tier-agent-architectures)
7. [Best Practices for Multi-Agent Work](#best-practices-for-multi-agent-work)
8. [Practical Implementation Patterns](#practical-implementation-patterns)

---

## Claude Code's Task Tool and Subagent System

### Core Concepts

**Task Tool Overview**
- The Task tool spawns **ephemeral Claude workers** - temporary contractors who show up for one specific job, then vanish
- Each Task gets its own **200k context window**, completely isolated from everything else
- Tasks enable parallelization by running up to **10 concurrent operations** simultaneously
- Operations are queued beyond the 10-agent limit and executed in batches

**Context Isolation Benefits**
- Each subagent has its own context window, providing additional context capacity for large codebases
- Subagent work doesn't bloat the main conversation context
- When complete, subagents return a summary (not full context) to the orchestrator
- Prevents a single AI agent from exhausting its context window on complex multi-stage tasks
- **Important limitation**: Both Tasks and subagents start with ~20,000 tokens of context loading before actual work begins

### Task vs Subagent Distinction

**Tasks** (Ephemeral Workers)
- Best for parallel search operations
- One-time, isolated jobs
- Examples: searching without a target ("Find all database connections" across 1,000 files), reading 50 config files to build a dependency map, analyzing competitor codebases without contamination

**Subagents** (Persistent Specialists)
- Persistent expertise with their own context
- Longer-running, specialized work
- Examples: code reviewer, security scanner, test coverage analyzer
- Can be orchestrated to work simultaneously on different aspects of the same problem

### Capabilities and Limitations

**Strengths**
- Dramatically speeds up complex workflows through parallelization
- During code review, can run style-checker, security-scanner, and test-coverage subagents simultaneously
- Reduces review time from minutes to seconds
- Provides compartmentalized expertise with role-based specialization

**Limitations**
- Critical details like stack traces can be lost in context summarization
- Only 10 concurrent operations cap the parallelism level
- Each agent starts with ~20k token overhead before actual work
- Claude Code uses subagents conservatively by default - **must be explicit in prompts to maximize parallelization**

### Practical Usage Patterns

**When to Use Tasks**
1. Searching without a specific target across many files
2. Parallel reads of multiple configuration files
3. Context isolation when analyzing external codebases
4. Truly one-off work that won't need follow-up

**When to Use Subagents**
1. Complex multi-step features requiring different expertise
2. Code review with multiple specialized reviewers
3. Performance optimization across different components
4. Systematic refactoring with different focus areas

**Maximizing Parallelization**
To maximize subagent usage, provide Claude with **explicit steps** including:
- Details about which steps will be delegated to subagents
- Clear task boundaries and dependencies
- Expected outputs from each subagent
- How results will be synthesized

---

## Hierarchical Agent Workflows

### Three-Layer Architecture

**1. Strategy Layer**
- High-level goal interpretation
- Overall approach determination
- Resource allocation decisions
- Dynamic replanning based on results

**2. Planning Layer**
- Task decomposition into manageable subtasks
- Dependency identification
- Sequence determination (what runs in parallel vs sequential)
- Resource and tool assignment

**3. Execution Layer**
- Actual implementation work
- Tool usage and API calls
- File operations and code modifications
- Results reporting back to planning layer

### Hierarchical Multi-Agent Systems (HMAS)

**Tree-Like Structure**
- **Leader agent** at the root node interprets user objectives
- Formulates high-level plan
- Assigns work to specialized sub-agents
- Coordinates information flow between layers

**AgentOrchestra Framework**
- **Planning Agent**: Central orchestrator for high-level reasoning, task decomposition, and adaptive planning
- **Specialized Sub-Agents**: Domain-specific agents equipped with specialized tools
- Systematically decomposes complex, long-horizon tasks into manageable subtasks
- Mirrors how humans manage intricate projects

### Workflow Phases

**1. Planning Phase**
- Orchestrator creates structured task breakdown
- Identifies dependencies and parallelization opportunities
- Allocates resources and determines agent assignments

**2. Delegation Phase**
- Subtasks assigned to specialist agents
- Context provisioning (only necessary information)
- Clear success criteria establishment

**3. Execution Phase**
- Sub-agents perform work independently
- Parallel execution where possible
- Progress monitoring by orchestrator

**4. Synthesis Phase**
- Orchestrator aggregates outputs from multiple agents
- Resolves conflicts between agent outputs
- Creates unified result

**5. Iteration Phase**
- Dynamic replanning based on results
- Feedback loops for refinement
- Adaptive course correction

---

## Planning → Building → Task Decomposition Patterns

### Task Decomposition Strategies

**Hierarchical Task Decomposition**
- Breaks down large objectives into multiple levels of abstraction
- Ranges from high-level phases down to granular, actionable steps
- Mirrors how humans manage intricate projects
- Reduces cognitive load on the LLM
- Improves reasoning and minimizes hallucinations

**Static vs Dynamic Decomposition**
- **Static**: Decomposition happens during implementation planning
  - Use when the solution is known
  - Optimizes for faster execution
  - Requires upfront certainty
- **Dynamic**: Decomposition happens during execution
  - Use when the solution is unclear
  - Accepts higher cost for better discovery
  - Supports iterative learning and exploration

### Core Decomposition Patterns

**1. Plan & Solve Pattern**
- Agent autonomously breaks down complex tasks
- Creates series of smaller, simpler tasks
- Leads to better results by reducing cognitive load
- Systematic approach to problem-solving

**2. PEER Pattern** (Plan, Execute, Express, Review)
- **Plan**: Create structured approach
- **Execute**: Implement the solution
- **Express**: Format output professionally
- **Review**: Quality check and refinement
- Each iteration refines output based on all four phases

**3. ReWOO Pattern**
- Enforces strict **plan → execute → synthesize** separation
- Small, explicit graph where each node returns typed result
- Deterministic flow of results downstream
- Plan-Guided ReAct Worker performs local loop for each step
- Does not reorder steps or call tools outside the plan

### Dependency Analysis

**During Planning Phase**
- Identify which steps must be completed sequentially
- Determine which steps can run in parallel
- Consider required resources, tools, or information for each step
- Map data flow between tasks
- Only begin execution after structured plan is complete

**Adaptive Delegation Based on Complexity**
- **Simple modifications/bug fixes**: High autonomy to coder agent
- **Medium tasks**: Iterative decomposition with checkpoints
- **Large tasks**: Strong oversight with frequent synthesis

---

## Parallelization Strategies

### Parallel Execution Patterns

**Container-Based Isolation**
- Spawn multiple containers for isolated agent work
- Provide container-use as MCP server to agents
- Agents spawn containers independently
- Merge remote agent work back to main branch
- Developed by former Docker founder for optimized workflow

**ParallelAgent Workflow**
- Executes sub-agents concurrently
- Dramatically speeds up workflows with independent tasks
- Examples:
  - Content workflow: 6:10 → 3:56 (36% speed-up)
  - Code review: style + security + coverage simultaneously
  - Testing: unit tests + integration tests + linting in parallel

### Parallelization Strategies by Use Case

**1. Research & Literature Review** (Parallel)
- **Agent 1**: Explore codebase for relevant implementations
- **Agent 2**: WebSearch for papers, docs, existing solutions
- **Agent 3**: Identify architecture and design patterns

**2. Data Processing & Experiments** (Parallel)
- Process multiple datasets simultaneously
- Run parameter sweeps in parallel
- Compare different algorithms/approaches side-by-side

**3. Code Analysis & Debugging** (Parallel)
- **Agent 1**: Trace data flow through system
- **Agent 2**: Search for similar patterns/bugs in codebase
- **Agent 3**: Check documentation and tests for expected behavior

**4. Build & Test Parallelization** (Parallel)
- Run tests while building documentation
- Lint/format while running unit tests
- Build multiple targets simultaneously

**5. Content Generation** (Parallel)
- **Agent 1**: Draft content
- **Agent 2**: Fact-check
- **Agent 3**: Generate examples
- **Orchestrator**: Coordinates tasks, merges results, resolves conflicts

### Performance Gains

**Benchmarks**
- Content workflow: ~37% faster with similar quality
- Code review: Minutes → seconds with parallel specialist agents
- Higher throughput through parallel execution
- Reliability through shard retries
- Role-based specialization improves quality
- Tighter context control per agent

**Trade-offs**
- Multi-agent systems outperformed single agents by **90.2%** (Anthropic research)
- But consumed **15× more tokens**
- Coordination overhead increases with more agents
- Communication requires clear protocols
- Debugging more challenging (interaction problems vs individual agent errors)

### Parallelization Best Practices

**1. Independence Requirements**
- Only parallelize tasks with no dependencies
- Ensure agents can work without waiting for other agent outputs
- Map data dependencies before parallelization

**2. Specificity**
- Give each agent a clear, focused objective
- Define success criteria explicitly
- Limit scope to prevent overlap

**3. Background Tasks**
- Use `run_in_background: true` for long-running tasks
- Examples: builds, large file searches, comprehensive tests
- Orchestrator can continue other work while background tasks execute

**4. Explicit Parallel Requests**
- Say "run in parallel" or "simultaneously" in prompts
- Be explicit about which tasks should run concurrently
- Provide clear boundaries between parallel workstreams

**5. Collect and Synthesize**
- After parallel agents complete, synthesize findings
- Create unified, actionable insights
- Resolve conflicts between agent outputs
- Present coherent results to user

---

## Agent Orchestration in CLI Environments

### CLI-Specific Orchestration Tools

**CLI Agent Orchestrator (CAO)**
- Open source multi-agent orchestration framework
- Transforms developer work with AI-powered CLI tools (Amazon Q CLI, Claude Code)
- Creates hierarchical orchestration system
- Multiple specialized CLI AI agents work together under intelligent supervision

**Architecture**
- Operates entirely within local environment
- All agent communications through local tmux sessions
- Uses MCP (Model Context Protocol) servers for tool integration
- Strong privacy and security - no data leaves local machine

### Orchestrator-Workers Pattern

**Orchestrator Responsibilities**
- Explicitly defines what knowledge artifacts subagents must return
- Reuses and synthesizes artifacts across future tasks
- Dispatches multiple explorer and coder agents
- Maintains adaptive delegation based on task complexity
- Session monitoring shows reasoning, not just actions

**Worker Agents**
- **Explorer Agents**: Gather information, search codebases, analyze patterns
- **Coder Agents**: Implement changes, write code, run tests
- **Specialist Agents**: Security, performance, style enforcement, etc.
- Report back to orchestrator with structured findings

### CLI Best Practices

**1. Configuration Files**
- Always start projects with `AGENTS.md` or `CLAUDE.md` files
- Include: test instructions, core files, code styling, guidelines
- Agents retrieve this information to guide operations
- Update regularly as project evolves

**2. Task Management**
- Define clear, scoped tasks
- Supply just enough context (avoid overload)
- Use discipline: specific prompts, not vague requests
- Group similar work together for batch review

**3. Security and Permissions**
- Maintain local-only execution
- Control file system access carefully
- Review agent actions before applying
- Use sandboxed environments for untrusted code

**4. Session Monitoring**
- Review session logs for agent reasoning
- Identify misunderstandings before they become PRs
- Improve future prompts based on logs
- Track resource usage and performance

### Popular CLI Coding Tools

**Comparison of Agentic CLI Tools**
- **Claude Code**: Strong multi-agent orchestration, 200k context per agent
- **Aider**: Lightweight, fast for simple edits
- **Codex CLI**: OpenAI-backed, good for completion
- **Gemini CLI**: Google's offering, strong at search integration
- **Warp**: Terminal-native AI with context-aware suggestions

**Common Features**
- Task delegation and automation
- Parallel execution support
- Context management
- MCP server integration
- Git workflow integration

---

## Multi-Tier Agent Architectures

### Three-Tier Framework Architecture

**Foundation Tier**
- Establishes tool orchestration
- Transparency in reasoning and decision-making
- Data lifecycle patterns (acquisition → processing → storage → cleanup)
- Core capabilities: file I/O, git operations, bash execution, web access

**Workflow Tier**
- Delivers automation through five core patterns:
  1. **Prompt Chaining**: Sequential task execution
  2. **Routing**: Dynamic task assignment based on content
  3. **Parallelization**: Concurrent execution of independent tasks
  4. **Evaluator-Optimizer**: Iterative refinement with quality checks
  5. **Orchestrator-Workers**: Hierarchical task coordination

**Autonomous Tier**
- Agents determine their own approaches dynamically
- Tool usage selection based on context
- Adaptive planning and replanning
- Self-correction and learning from results

### Enterprise Multi-Agent Systems

**Coordinated Architecture**
- Central orchestration layer coordinates multi-tenant systems
- Foundation for ecosystem of specialized agents
- Multiple AI agents collaborate through central API orchestrator
- Process automation runs organizational tasks automatically

**Production-Ready Systems**
- 108 specialized AI agents
- 15 multi-agent workflow orchestrators
- 129 agent skills
- 72 development tools organized into 72 focused, single-purpose plugins

### MAAD Framework (Multi-Agent Architecture Design)

**Purpose**
- Automates software architecture design process
- Agents simulate human roles in traditional architecture design
- Roles: developer, architect, project manager, code reviewer, security specialist, tester

**Benefits**
- Multi-agent systems often outperform single-agent systems
- Specialized expertise for each architectural concern
- Parallel evaluation of design alternatives
- Comprehensive coverage of architectural requirements

### Microsoft Agent Framework

**Architecture Components**
- Defines agent and orchestration behavior
- Deployed in Azure Container Apps
- Uses Azure AI services for LLM integration
- Multiple-agent workflow automation solution

**Orchestration Patterns**
- Single-agent: One agent handles entire workflow
- Multi-agent: Specialized agents collaborate on complex tasks
- Hierarchical: Leader coordinates team of specialist agents
- Networked: Peer-to-peer agent communication and collaboration

---

## Best Practices for Multi-Agent Work

### Phased Approach with Subagents

**1. Research Phase**
- Explore codebase
- Understand requirements
- Identify dependencies
- Search for existing solutions
- Review documentation and tests

**2. Implementation Phase**
- Write code based on research findings
- Make changes systematically
- Follow established patterns
- Test incrementally

**3. Review/Testing Phase**
- Run tests (unit, integration, e2e)
- Verify functionality
- Check for issues and edge cases
- Performance validation

**4. Cleanup Phase**
- Refactor if needed
- Ensure code quality standards
- Final verification
- Documentation updates

### Context Management

**Efficient Context Provisioning**
- Pass only necessary context to each agent
- Keep context size manageable to prevent overload
- Remove unnecessary data when no longer needed
- Use context isolation to prevent contamination

**Context Window Strategy**
- Each subagent: 200k tokens
- But ~20k overhead before actual work
- Main conversation: separate context pool
- Summaries returned, not full context

### Agent Specialization

**Create Focused Agents**
- Specialized prompts for specific domains
- Specific tools per agent type
- Clear success criteria
- Single responsibility principle

**Common Specialist Roles**
- **Research Agent**: Information gathering, documentation review
- **Coding Agent**: Implementation, refactoring, bug fixes
- **Data Analysis Agent**: Performance metrics, profiling, optimization
- **Security Agent**: Vulnerability scanning, security best practices
- **Test Agent**: Test generation, coverage analysis, validation
- **Review Agent**: Code quality, style enforcement, best practices

### Coordination Strategies

**State Management**
- **Centralized**: Orchestrator maintains all state (simpler, single point of failure)
- **Distributed**: Each agent maintains own state (more resilient, harder to coordinate)
- **Hybrid**: Critical state centralized, execution state distributed (balanced approach)

**Communication Protocols**
- Define clear interfaces between agents
- Structured data formats (JSON, typed objects)
- Error handling and retry logic
- Timeout management for long-running agents

### Incremental Complexity

**Start Simple**
- Begin with single-agent workflow
- Add one specialist at a time
- Validate each agent's performance before adding more
- Monitor token usage and costs

**Scale Gradually**
- Two agents: Planner + Executor
- Three agents: Planner + Executor + Reviewer
- Four+ agents: Add specialists as needed
- Don't over-architect initially

### Supervision Strategy

**Supervised Mode** (Active Oversight)
- Watch agents in real-time
- Steer decisions when needed
- Verify outputs before accepting
- Best for: Critical changes, unfamiliar domains, building trust

**Autonomous Mode** (Fire-and-Forget)
- Let agents complete work independently
- Review results afterward
- Minimal intervention
- Best for: Well-understood tasks, established patterns, trusted agents

**Progression**
- Start with supervised mode
- Build trust through successful executions
- Gradually shift to autonomous mode
- Maintain supervision for critical operations

### Debugging Multi-Agent Systems

**Common Issues**
- Agent interaction problems (not individual agent errors)
- Context synchronization issues
- Conflicting outputs from parallel agents
- Coordination overhead and delays

**Debugging Strategies**
- Review session logs for reasoning traces
- Isolate agents to test individually
- Check communication between agents
- Validate orchestrator's decision-making
- Monitor token usage per agent

---

## Practical Implementation Patterns

### Pattern 1: Code Review Multi-Agent

**Agents**
1. **Security Auditor**: Scans for vulnerabilities, checks dependencies
2. **Style Enforcer**: Validates formatting, naming conventions, code style
3. **Performance Analyst**: Identifies bottlenecks, suggests optimizations
4. **Test Coverage**: Analyzes test completeness, suggests additional tests
5. **Synthesizer**: Combines feedback into cohesive review comment

**Workflow**
- Parallel execution of all 4 specialist agents
- Each returns structured findings
- Synthesizer creates unified, actionable review
- Timing: Minutes → seconds

### Pattern 2: Feature Implementation Multi-Agent

**Phase 1: Research** (Parallel)
- **Agent A**: Search codebase for similar implementations
- **Agent B**: Review documentation and best practices
- **Agent C**: Identify required dependencies and tools

**Phase 2: Planning** (Sequential)
- Orchestrator synthesizes research findings
- Creates implementation plan with subtasks
- Identifies which subtasks can be parallelized

**Phase 3: Implementation** (Parallel)
- **Agent 1**: Implement core logic
- **Agent 2**: Write tests
- **Agent 3**: Update documentation

**Phase 4: Integration** (Sequential)
- Orchestrator combines implementations
- Runs integration tests
- Fixes conflicts and issues

### Pattern 3: Performance Optimization Multi-Agent

**Parallel Analysis**
1. **Profiling Agent**: Runs performance profiler, identifies hotspots
2. **Memory Agent**: Analyzes memory usage, identifies leaks
3. **Algorithm Agent**: Reviews algorithmic complexity, suggests improvements
4. **Database Agent**: Analyzes queries, suggests indexes and optimizations

**Sequential Optimization**
- Orchestrator prioritizes issues by impact
- Assigns optimization tasks to coder agent
- Runs benchmarks after each optimization
- Validates no regressions

### Pattern 4: Bug Investigation Multi-Agent

**Parallel Investigation**
1. **Flow Tracer**: Traces data flow through system to error point
2. **Pattern Searcher**: Searches codebase for similar bugs and fixes
3. **Documentation Checker**: Reviews docs and tests for expected behavior
4. **Dependency Analyzer**: Checks for known issues in dependencies

**Synthesis and Fix**
- Orchestrator combines findings
- Identifies root cause
- Generates fix implementation
- Creates test to prevent regression

### Pattern 5: Documentation Generation Multi-Agent

**Parallel Generation**
1. **Code Analyzer**: Extracts structure, interfaces, key functions
2. **Example Generator**: Creates usage examples and code snippets
3. **API Documenter**: Documents public APIs with parameters and returns
4. **Tutorial Writer**: Creates getting-started guides

**Sequential Polish**
- Orchestrator organizes documentation sections
- Ensures consistency in tone and style
- Links between related sections
- Final review and formatting

### Pattern 6: Test Suite Generation

**Parallel Test Generation**
1. **Unit Test Agent**: Creates unit tests for individual functions
2. **Integration Test Agent**: Tests component interactions
3. **Edge Case Agent**: Identifies and tests edge cases
4. **E2E Test Agent**: Creates end-to-end user scenarios

**Sequential Validation**
- Run all tests to verify they pass
- Check coverage metrics
- Identify gaps
- Refine tests based on results

---

## Advanced Patterns and Considerations

### Dynamic Replanning

**When to Replan**
- Unexpected errors during execution
- Resource constraints encountered
- Better approach discovered mid-execution
- User requirements change

**Replanning Process**
1. Pause current execution
2. Analyze what worked and what didn't
3. Create revised plan
4. Resume with new approach
5. Learn from the iteration

### Agent Handoffs

**Seamless Transitions**
- Agent A completes its work
- Packages results in structured format
- Hands off to Agent B with clear context
- Agent B continues without redundant work

**Handoff Best Practices**
- Define clear handoff points
- Use structured data formats
- Include metadata (confidence scores, warnings, caveats)
- Maintain traceability

### Quality Assurance Loops

**Evaluator-Optimizer Pattern**
1. **Executor Agent**: Implements solution
2. **Evaluator Agent**: Assesses quality against criteria
3. **Optimizer Agent**: Refines based on evaluation
4. Iterate until quality threshold met

**Benefits**
- Automated quality improvement
- Reduces human review burden
- Systematic refinement process
- Measurable quality metrics

### Resource Management

**Token Budget Management**
- Monitor token usage per agent
- Set budgets for exploratory vs execution work
- Kill runaway agents consuming excessive tokens
- Optimize prompts to reduce token overhead

**Time Management**
- Set timeouts for each agent
- Prioritize critical path work
- Background long-running tasks
- Fail fast on blocked tasks

---

## Key Takeaways

### Critical Success Factors

1. **Be Explicit**: Claude Code uses subagents conservatively - explicitly request parallel execution
2. **Context Isolation**: Leverage 200k context per agent for large codebases
3. **Appropriate Parallelization**: Only parallelize truly independent tasks
4. **Clear Interfaces**: Define what each agent should return and in what format
5. **Start Simple**: Build trust with simple patterns before scaling to complex orchestration

### When Multi-Agent Shines

- Complex, multi-faceted problems requiring diverse expertise
- Large codebases exceeding single agent context limits
- Tasks with clear parallelization opportunities
- Time-sensitive work benefiting from concurrent execution
- Quality-critical work requiring multiple specialist reviews

### When to Avoid Multi-Agent

- Simple, straightforward tasks
- When coordination overhead exceeds benefits
- Token budgets are constrained
- Tasks are highly sequential with tight dependencies
- Single agent can handle within context limits

### The Future of Terminal-Based Multi-Agent Systems

**2026 Trends**
- Coordinated groups of AI agents working across planning, creation, quality checks
- Container-based isolation for safer parallel execution
- Workflows moving from rigid sequence to flexible parallelism
- Teams coordinating labor across multi-agent parallel workflows
- Transformation of AI into collaborative teams for complex applications

**Emerging Capabilities**
- More sophisticated orchestration patterns
- Better context management and handoffs
- Improved debugging and observability
- Lower coordination overhead
- More efficient token usage

---

## Sources

### Claude Code Specific
- [How to Use Claude Code Subagents to Parallelize Development](https://zachwills.net/how-to-use-claude-code-subagents-to-parallelize-development/)
- [ClaudeLog - Claude Code Docs, Guides, Tutorials & Best Practices](https://claudelog.com/mechanics/task-agent-tools/)
- [Multi-agent parallel coding with Claude Code Subagents](https://medium.com/@codecentrevibe/claude-code-multi-agent-parallel-coding-83271c4675fa)
- [Claude Code - When to use task tool vs subagents](https://amitkoth.com/claude-code-task-tool-vs-subagents/)
- [How to Use Claude Code Sub-Agents for Parallel Work](https://timdietrich.me/blog/claude-code-parallel-subagents/)
- [How Claude Code works - Official Docs](https://code.claude.com/docs/en/how-claude-code-works)
- [What is the Task Tool in Claude Code](https://claudelog.com/faqs/what-is-task-tool-in-claude-code/)
- [How to run Claude Code in parallel](https://ona.com/stories/parallelize-claude-code)

### Hierarchical Workflows
- [AgentOrchestra: A Hierarchical Multi-Agent Framework](https://arxiv.org/html/2506.12508v1)
- [Prompt Strategies for Hierarchical Task Decomposition](https://apxml.com/courses/prompt-engineering-agentic-workflows/chapter-4-prompts-agent-planning-task-management/prompt-strategies-hierarchical-tasks)
- [Building Multi-Agent Architectures](https://medium.com/@akankshasinha247/building-multi-agent-architectures-orchestrating-intelligent-agent-systems-46700e50250b)
- [What is AI Agent Planning?](https://www.ibm.com/think/topics/ai-agent-planning)
- [LLM Agent Task Decomposition Strategies](https://apxml.com/courses/agentic-llm-memory-architectures/chapter-4-complex-planning-tool-integration/task-decomposition-strategies)
- [Hierarchical Multi-Agent Systems: Concepts and Operational Considerations](https://overcoffee.medium.com/hierarchical-multi-agent-systems-concepts-and-operational-considerations-e06fff0bea8c)

### CLI Orchestration
- [CLI Agent Orchestrator: Transforming Developer CLI Tools](https://aws.amazon.com/blogs/opensource/introducing-cli-agent-orchestrator-transforming-developer-cli-tools-into-a-multi-agent-powerhouse/)
- [Compare the Top 5 Agentic CLI Coding Tools](https://getstream.io/blog/agentic-cli-tools/)
- [Top 10 Open-Source CLI Coding Agents](https://dev.to/forgecode/top-10-open-source-cli-coding-agents-you-should-be-using-in-2025-with-links-244m)
- [Multi-agent coding system - GitHub](https://github.com/Danau5tin/multi-agent-coding-system)
- [How to orchestrate agents using mission control](https://github.blog/ai-and-ml/github-copilot/how-to-orchestrate-agents-using-mission-control/)
- [Agentic CLI Tools Compared](https://research.aimultiple.com/agentic-cli/)

### Parallelization Strategies
- [AI Coding 2026: Managing Multi-Agent Parallel Workflows](https://www.geeky-gadgets.com/manage-ai-agents-like-a-senior-engineer/)
- [5 Key Trends Shaping Agentic Development in 2026](https://thenewstack.io/5-key-trends-shaping-agentic-development-in-2026/)
- [Parallel agents - Agent Development Kit](https://google.github.io/adk-docs/agents/workflow-agents/parallel-agents/)
- [2026: From AI Pilots to Parallel Agent Workflows](https://www.smartcat.com/blog/from-pilots-to-parallel-agent-workflows/)
- [Parallelizing AI Coding Agents](https://ainativedev.io/news/how-to-parallelize-ai-coding-agents)
- [Multi-Agent Parallel Workflow: From Coder to Conductor](https://jiahaoxiang2000.github.io/blog/tools/multi-agent-parallel)
- [Multi-Agent Parallel Execution](https://skywork.ai/blog/agent/multi-agent-parallel-execution-running-multiple-ai-agents-simultaneously/)
- [Developer's guide to multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/)

### Orchestration Patterns
- [Microsoft Agent Framework Workflows Orchestrations](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/overview)
- [AI Agent Orchestration Patterns - Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
- [Customize agent workflows with Strands Agents](https://aws.amazon.com/blogs/machine-learning/customize-agent-workflows-with-advanced-orchestration-techniques-using-strands-agents/)
- [Orchestrator-Workers Workflow](https://javaaidev.com/docs/agentic-patterns/patterns/orchestrator-workers-workflow/)
- [Top 10+ Agentic Orchestration Frameworks & Tools in 2026](https://research.aimultiple.com/agentic-orchestration/)
- [Agent Orchestration Patterns with Dynamiq](https://www.getdynamiq.ai/post/agent-orchestration-patterns-in-multi-agent-systems-linear-and-adaptive-approaches-with-dynamiq)
- [AI Agent Orchestration: How To Coordinate Multiple AI Agents](https://botpress.com/blog/ai-agent-orchestration)
- [Orchestrating Multi-Agent Intelligence: MCP-Driven Patterns](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/orchestrating-multi-agent-intelligence-mcp-driven-patterns-in-agent-framework/4462150)

### Multi-Agent Workflows
- [Multi-agent system: Frameworks & step-by-step tutorial](https://blog.n8n.io/multi-agent-systems/)
- [Top AI Agentic Workflow Patterns](https://blog.bytebytego.com/p/top-ai-agentic-workflow-patterns)
- [Four-Phase Workflow | Agentic Coding](https://agenticoding.ai/docs/methodology/lesson-3-high-level-methodology)
- [Multi-Agent Workflows: A Practical Guide](https://medium.com/@kanerika/multi-agent-workflows-a-practical-guide-to-design-tools-and-deployment-3b0a2c46e389)
- [AI Agentic Workflows: Tutorial & Best Practices](https://fme.safe.com/guides/ai-agent-architecture/ai-agentic-workflows/)
- [How to Build Your First Agentic Workflow](https://caylent.com/blog/how-to-build-your-first-agentic-workflow)
- [A Coding Guide to Build Intelligent Multi-Agent Systems with the PEER Pattern](https://www.marktechpost.com/2025/08/02/a-coding-guide-to-build-intelligent-multi-agent-systems-with-the-peer-pattern/)

### Multi-Tier Architectures
- [Designing Multi-Agent Intelligence - Microsoft](https://developer.microsoft.com/blog/designing-multi-agent-intelligence)
- [Intelligent automation and multi-agent orchestration - GitHub](https://github.com/wshobson/agents)
- [AI Agent Architecture: Tutorial and Best Practices](https://www.patronus.ai/ai-agent-development/ai-agent-architecture)
- [Build a Multiple-Agent Workflow Automation Solution - Azure](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/idea/multiple-agent-workflow-automation)
- [What Is Agentic AI Architecture?](https://zencoder.ai/blog/what-is-agentic-ai-architecture)
- [Knowledge-Based Multi-Agent Framework for Automated Software Architecture Design](https://arxiv.org/abs/2503.20536)
- [Single-agent and multi-agent architectures - Microsoft](https://learn.microsoft.com/en-us/dynamics365/guidance/resources/contact-center-multi-agent-architecture-design)
- [Top 9 AI Agent Frameworks as of January 2026](https://www.shakudo.io/blog/top-9-ai-agent-frameworks)
