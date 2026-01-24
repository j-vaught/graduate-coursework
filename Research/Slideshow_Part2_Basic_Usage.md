# Part 2: Basic Usage - Agentic Coding Tools
## A Comprehensive Guide for Students

---

## TABLE OF CONTENTS
1. Core Capabilities Overview (Slides 1-4)
2. Code Generation & Editing (Slides 5-14)
3. File Management (Slides 15-20)
4. Writing & Documentation (Slides 21-26)
5. Codebase Research & Search (Slides 27-36)
6. Online Research (Slides 37-40)
7. Git Workflows (Slides 41-46)

---

# SECTION 1: CORE CAPABILITIES OVERVIEW

---

## Slide 1: What Are Agentic Coding Tools?

### Main Content

Agentic coding tools are AI-powered assistants that understand and interact with your development environment autonomously. Unlike traditional code completion, these tools:

- Execute terminal commands directly
- Read and modify entire files
- Navigate your codebase structure
- Research solutions independently
- Commit changes to version control
- Reason about complex problems iteratively

### Key Distinction

**Traditional Code Completion**: Single suggestion → You accept or reject

**Agentic Tools**: Multi-step reasoning → Tool executes plan → Iterative refinement

### Speaker Notes

Emphasize that agentic tools represent a paradigm shift. They're not just smarter autocomplete—they're collaborative agents that can reason about your project holistically. This is particularly powerful for tasks that involve multiple steps or require understanding project context.

---

## Slide 2: Categories of Agentic Tools

### Main Content

#### Terminal-Based Agents
- Claude Code (this tool, built-in)
- Aider
- GitHub Copilot CLI
- Command-line focused, scriptable

#### IDE/Editor Plugins
- Cursor (AI-first IDE)
- Windsurf
- VS Code extensions
- Real-time as you work

#### Web-Based Interfaces
- Claude.ai
- ChatGPT
- GitHub Copilot Chat
- Browser-based access

### Positioning

Terminal agents are most powerful for:
- Automated workflows
- Complex multi-file refactoring
- Codebase analysis
- CI/CD pipeline integration

### Speaker Notes

Each category has strengths. Terminal agents excel at repeatability and automation. IDE plugins excel at real-time feedback. Discuss how students might use them in combination—IDE for interactive development, terminal agent for complex refactoring tasks.

---

## Slide 3: The Agent Reasoning Loop

### Main Content

```
┌─────────────────────────────────────────────┐
│ 1. UNDERSTAND: Parse user request          │
│    - Identify goals                         │
│    - Assess complexity                      │
│    - Determine dependencies                 │
└──────────────┬──────────────────────────────┘
               │
┌──────────────v──────────────────────────────┐
│ 2. EXPLORE: Investigate project context    │
│    - Search codebase                        │
│    - Read relevant files                    │
│    - Map dependencies                       │
└──────────────┬──────────────────────────────┘
               │
┌──────────────v──────────────────────────────┐
│ 3. PLAN: Determine execution strategy      │
│    - Break into subtasks                    │
│    - Order operations                       │
│    - Identify tests needed                  │
└──────────────┬──────────────────────────────┘
               │
┌──────────────v──────────────────────────────┐
│ 4. EXECUTE: Perform operations             │
│    - Modify files                           │
│    - Run commands                           │
│    - Generate artifacts                     │
└──────────────┬──────────────────────────────┘
               │
┌──────────────v──────────────────────────────┐
│ 5. VERIFY: Check results                   │
│    - Run tests                              │
│    - Validate output                        │
│    - Identify issues                        │
└──────────────┬──────────────────────────────┘
               │
              NO ◄──── Issues Found?
               │              │
              YES             │
               │◄──────────────┘
               │
┌──────────────v──────────────────────────────┐
│ 6. REFINE: Fix problems                    │
│    - Adjust approach                        │
│    - Try alternatives                       │
│    - Iterate until success                  │
└─────────────────────────────────────────────┘
```

### Speaker Notes

This loop is fundamental to understanding how agentic tools work. They're not executing blindly—they explore, understand, plan, then execute. This is why they're so powerful but also why clear requests matter. The better the initial request, the more efficiently the agent can loop through to completion.

---

## Slide 4: Core Capabilities at a Glance

### Main Content

| Capability | Terminal Agents | IDE Plugins | Description |
|-----------|-----------------|-------------|-------------|
| Code Generation | Excellent | Excellent | Create files and functions from scratch |
| Multi-File Editing | Excellent | Good | Modify multiple files in one operation |
| Codebase Search | Excellent | Excellent | Find patterns and understand architecture |
| Terminal Execution | Excellent | Limited | Run commands and see output in real-time |
| Git Operations | Excellent | Good | Commit, branch, PR automation |
| Documentation | Excellent | Good | Generate docs, comments, README |
| Testing | Excellent | Good | Write and run test suites |
| Real-Time Feedback | Limited | Excellent | Immediate suggestions as you type |
| Debugging | Good | Excellent | Step through and identify issues |
| Large Refactoring | Excellent | Good | Project-wide code changes |

### Speaker Notes

Terminal agents excel when you need automation and can batch operations. IDE plugins excel when you want immediate feedback. Most professional developers use both—IDE plugin during development, terminal agent for larger tasks. This complementary approach is the sweet spot for productivity.

---

# SECTION 2: CODE GENERATION & EDITING

---

## Slide 5: Code Generation Fundamentals

### Main Content

Code generation with agentic tools involves:

1. **Natural Language Specification**: Describe what you want
2. **Context Analysis**: Tool reads relevant files
3. **Pattern Recognition**: Tool identifies similar code in project
4. **Generation**: Tool creates code matching project style
5. **Integration**: Tool places code in correct location
6. **Validation**: Tool checks for errors and adjusts

### Example Request

```
"Create a Python class called DatabaseConnection that:
- Connects to PostgreSQL using psycopg2
- Implements context manager methods (__enter__, __exit__)
- Has methods for query execution and transaction management
- Includes proper error handling
- Follows the same style as our existing database module"
```

### What the Agent Does

```bash
# Search for existing database patterns
grep -r "class.*Connection" src/

# Read the existing database module to understand style
cat src/database/existing_connection.py

# Generate the new class
# (creates file with proper formatting, error handling, docstrings)

# Validate against project patterns
# (checks for consistency with existing code)
```

### Speaker Notes

The power here is that the agent learns your project's conventions automatically. It's not generating generic code—it's generating code that matches your specific style and patterns. This is why context is crucial: the more relevant code the agent can see, the better the generated code quality.

---

## Slide 6: Terminal Agent Example - Claude Code

### Main Content

**Claude Code** is the native terminal agent in this environment.

#### Basic Command Structure

```bash
# Start Claude Code with optional context
claude code /path/to/project

# Common operations within Claude Code
"Create a React component called UserProfile"
"Add error handling to the database module"
"Generate unit tests for the authentication system"
"Refactor this function for better readability"
```

#### Real Example: Creating a Python API Endpoint

```bash
# Start Claude Code pointing to your project
claude code /workspace/api-project

# Request
> "Create a FastAPI endpoint that accepts POST requests at /api/users with
>  name and email, validates input using Pydantic, stores in database,
>  returns created user with ID, includes error handling for duplicates"

# Claude Code will:
# 1. Examine existing FastAPI route patterns
# 2. Check the Pydantic model structure
# 3. Understand database schema from existing code
# 4. Generate endpoint matching project style
# 5. Add proper error handling and status codes
# 6. Run validation to ensure it integrates correctly
```

### Speaker Notes

Claude Code is unique because it runs directly in your terminal context. This means it can chain operations automatically. You can ask it to create a file, then test it, then refactor it—all in one session without context switching.

---

## Slide 7: Terminal Agent Example - Aider

### Main Content

**Aider** is a powerful terminal-based AI pair programmer focused on code editing.

#### Installation & Setup

```bash
# Install via pip
pip install aider-chat

# Start Aider with specific files
aider src/main.py src/utils.py

# Or let Aider find files
aider --auto-lint
```

#### Interactive Terminal Interface

```
aider> "Add JWT authentication to the login endpoint"
aider> "The imported 'User' model isn't used, remove it"
aider> "Refactor this duplicated code into a helper function"
aider> "Run tests and fix any failures"
```

#### Real Example: Multi-File Refactoring

```bash
# Start Aider in project directory
cd /workspace/project && aider

# Aider maintains context of all open files
# You can refer to them by name

aider> "Update the User model to add an email_verified field"

# Aider reads the User model file
# Identifies all places it's used
# Updates model, migrations, and related code
# Runs tests to verify changes

aider> "Fix any migration conflicts"
# Aider analyzes error output and fixes issues
```

#### Key Aider Features

```bash
# Mark files for editing (with /add)
aider> "/add src/models.py src/views.py"

# Ask Aider to write tests
aider> "Write tests for the authentication module"

# Get diff before accepting changes
aider> "Show me the changes you'll make"

# Commit working changes
aider> "/commit 'Add JWT authentication'"
```

### Speaker Notes

Aider is particularly good for conversational code editing. You can have a back-and-forth dialogue about what you want, and Aider maintains context across multiple changes. The `/add` command is powerful—it tells Aider exactly which files to focus on, making it more efficient.

---

## Slide 8: Terminal Agent Example - GitHub Copilot CLI

### Main Content

**GitHub Copilot CLI** extends GitHub Copilot to the terminal.

#### Installation

```bash
# Requires GitHub CLI and Copilot subscription
gh extension install github/gh-copilot

# Verify installation
gh copilot --version
```

#### Command Explanation

```bash
# Get explanation for commands
gh copilot explain "find . -name '*.py' -type f -exec grep -l 'TODO' {} \;"

# Output:
# This command finds all Python files in the current directory
# and its subdirectories, then searches for files containing 'TODO'
```

#### Suggest Command

```bash
# Ask Copilot to suggest a command
gh copilot suggest "show git log for last 10 commits in one line"

# Suggested output:
# git log --oneline -10
#
# Accept (y) / Reject (n) / Edit (e)?
```

#### Code Explanation

```bash
# Explain existing code
gh copilot explain "jq '.data | map(select(.active == true)) | sort_by(.date)'"

# Copilot explains what jq does with the data
```

### Real Workflow Example

```bash
# You need a complex command
gh copilot suggest "compress all files in src/ older than 30 days"

# Copilot suggests:
find src/ -type f -mtime +30 -exec gzip {} \;

# You accept and run it
# Later you need to understand what you ran
gh copilot explain "find src/ -type f -mtime +30 -exec gzip {} \;"
```

### Speaker Notes

While GitHub Copilot CLI is less autonomous than Claude Code or Aider, it's excellent for learning. You can ask it to explain complex commands, breaking the barrier for students unfamiliar with command-line tools. It's also integrated directly into GitHub's ecosystem, making it natural if you're already using GitHub.

---

## Slide 9: IDE Agent Example - Cursor

### Main Content

**Cursor** is an IDE built from the ground up with AI-first design.

#### Key Features for Code Generation

```
┌─ CURSOR IDE ─────────────────────────────────────┐
│                                                   │
│  CMD + K: Generate code inline                   │
│  │ Write description, get generated code        │
│  │ Can reference files with @file syntax        │
│  │                                               │
│  CMD + L: Generate longer code blocks            │
│  │ For complex functions and components          │
│  │ Multi-file aware                              │
│  │                                               │
│  CMD + Shift + L: Generate terminal commands    │
│  │ Useful for npm/git commands                   │
│  │                                               │
│  Codebase Context: CMD + Enter                   │
│  │ References entire project in requests         │
│  │ Learns your coding style automatically        │
│  │                                               │
│  @ Rules: Define custom guidelines              │
│  │ "Always use async/await"                      │
│  │ "Use TypeScript strict mode"                  │
│  │ "Follow React hooks best practices"           │
│                                                   │
└───────────────────────────────────────────────────┘
```

#### Real Example: Generate React Component

```
File: App.tsx
User presses CMD + K and types:

"Create a TodoList component that:
- Displays items from a todos array
- Has add/delete buttons for each item
- Uses React hooks (useState, useEffect)
- Fetches todos on mount from /api/todos
- Shows loading state while fetching
- Uses Tailwind CSS for styling"

Cursor generates:

import { useState, useEffect } from 'react';

export function TodoList() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/todos')
      .then(res => res.json())
      .then(data => {
        setTodos(data);
        setLoading(false);
      });
  }, []);

  const deleteTodo = (id) => {
    setTodos(todos.filter(t => t.id !== id));
  };

  if (loading) return <div>Loading...</div>;

  return (
    <ul className="space-y-2">
      {todos.map(todo => (
        <li key={todo.id} className="flex justify-between">
          <span>{todo.title}</span>
          <button onClick={() => deleteTodo(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}
```

#### Cursor's Learning Feature

Cursor learns your coding patterns:
- If you always use certain imports, Cursor includes them
- If you have a specific error handling pattern, Cursor replicates it
- If you prefer functional over class components, Cursor respects that
- The longer you use it on a project, the better it understands your style

### Speaker Notes

Cursor bridges IDE and agent. You get the real-time feedback of an IDE with the reasoning of an agent. The @ syntax is particularly powerful—@file lets you reference specific files, and Cursor understands context from them. Cursor is excellent for rapid prototyping and learning new frameworks.

---

## Slide 10: IDE Agent Example - Windsurf

### Main Content

**Windsurf** (from Codeium) is another AI-native IDE with different emphasis.

#### Cascade Feature (Unique to Windsurf)

```
Cascade is Windsurf's multi-agent system:

┌─────────────────────────────────────────────┐
│ Multi-Agent Planning                         │
│                                              │
│ Your request: "Implement real-time          │
│ notifications system"                        │
│                                              │
│ Agent 1: Architecture Analyzer               │
│ → Reviews codebase structure                │
│ → Identifies patterns                       │
│ → Suggests integration points               │
│                                              │
│ Agent 2: Code Generator                      │
│ → Generates notification service            │
│ → Creates WebSocket handler                 │
│ → Updates UI components                     │
│                                              │
│ Agent 3: Test Generator                      │
│ → Writes unit tests                         │
│ → Creates integration tests                 │
│ → Validates implementation                  │
│                                              │
│ Result: Complete feature implementation     │
│ with architecture, code, and tests          │
└─────────────────────────────────────────────┘
```

#### Windsurf Command Palette

```
CMD + Shift + P (or Ctrl + Shift + P)

Actions:
- Generate unit test for file
- Create documentation
- Refactor selected code
- Explain code to me
- Add TypeScript types
- Optimize performance
- Generate API endpoint
```

#### Real Example: Add Authentication

```
Open authentication module
CMD + Shift + P → "Add OAuth2 support"

Windsurf's Cascade:
1. Analyzes existing auth patterns
2. Identifies all files needing updates
3. Generates OAuth2 provider setup
4. Updates login flow
5. Creates tests
6. Generates documentation

All automatically, with your approval at key checkpoints.
```

### Speaker Notes

Windsurf's Cascade is particularly interesting because it explicitly uses multiple agents with different specializations. This is different from other tools—most tools use a single agent that reasons about everything. Windsurf's multi-agent approach can be more efficient for complex tasks but may be slower for simple ones.

---

## Slide 11: Multi-File Editing - Terminal Agent Example

### Main Content

This is where terminal agents truly excel—editing multiple interdependent files in one operation.

#### Scenario: Rename Database Column

```bash
# Traditional approach (painful):
# 1. Update database schema
# 2. Create migration
# 3. Update ORM models
# 4. Update all queries referencing the column
# 5. Update tests
# 6. Update documentation
# 7. Debug any remaining issues

# With terminal agent (one operation):
aider

aider> "Rename the database column 'user_name' to 'username'
>       everywhere in the codebase. Update migrations,
>       models, queries, tests, and any API documentation."

# Aider automatically:
# - Finds all references to user_name
# - Updates database schema files
# - Updates ORM model definitions
# - Updates all query files
# - Updates test fixtures
# - Updates documentation
# - Runs tests to verify nothing broke
```

#### Real Example Output

```bash
aider> "Rename 'user_name' to 'username' everywhere"

Searching for all references to 'user_name'...
Found 47 occurrences in:
  - database/migrations/
  - models/user.py
  - queries/user_queries.py
  - tests/test_user.py
  - tests/fixtures/users.py
  - docs/api.md
  - src/api/handlers.py

Updating files...
[1/6] database/migrations/001_add_username_field.py
[2/6] models/user.py
[3/6] queries/user_queries.py
[4/6] tests/test_user.py
[5/6] tests/fixtures/users.py
[6/6] docs/api.md

Running tests to verify changes...
✓ All tests passing
✓ No new linting errors

Changes ready to commit. Review? (y/n)
```

#### Multi-File Orchestration Pattern

```python
# What the agent understands implicitly:

# 1. Dependency tracking
#    If file A imports from file B, changing B might affect A
#    Agent tracks this automatically

# 2. Pattern consistency
#    If the same code pattern appears in 10 files,
#    Agent updates all 10 consistently

# 3. Side effects
#    If changing a function signature requires updating
#    all callers, agent finds and updates them

# 4. Testing
#    After changes, agent runs relevant tests
#    If tests fail, agent analyzes and fixes issues
```

### Speaker Notes

This is what separates agentic tools from traditional code editors. A traditional refactoring tool might find and replace strings. An agentic tool understands the semantic meaning of changes and updates dependent code accordingly. This is particularly powerful for large refactorings that would normally take hours.

---

## Slide 12: Advanced Refactoring - Terminal Agent Example

### Main Content

Terminal agents can perform complex refactorings that would be extremely time-consuming manually.

#### Example 1: Extract Duplicated Logic

```python
# Before: Duplicated validation code in multiple places

# In user_service.py
def create_user(email, name, password):
    if not email or '@' not in email:
        raise ValueError("Invalid email")
    if len(name) < 2:
        raise ValueError("Name too short")
    if len(password) < 8:
        raise ValueError("Password too weak")
    # ... rest of logic

# In admin_service.py (same validation code repeated)
def create_admin(email, name, password):
    if not email or '@' not in email:
        raise ValueError("Invalid email")
    if len(name) < 2:
        raise ValueError("Name too short")
    if len(password) < 8:
        raise ValueError("Password too weak")
    # ... rest of logic
```

#### Agent Request

```bash
claude code /workspace/project

"Extract the validation logic from create_user and create_admin
into a reusable validator module. Create validation functions for
each field type, update both functions to use them, and add unit
tests for the validators."
```

#### What Agent Does

```bash
# 1. Identifies duplicated validation logic
# 2. Creates validators/validation.py with functions:
#    - validate_email()
#    - validate_name()
#    - validate_password()

# 3. Updates user_service.py:
#    from validators import validate_email, validate_name, validate_password
#
#    def create_user(email, name, password):
#        validate_email(email)
#        validate_name(name)
#        validate_password(password)
#        # ... rest of logic

# 4. Updates admin_service.py similarly

# 5. Generates test file with comprehensive test cases

# 6. Runs tests to verify refactoring worked
```

#### Example 2: Function Signature Update

```bash
"Update the get_user function signature from:
  get_user(user_id) -> dict

To:
  get_user(user_id: int, include_posts: bool = False) -> User

Update all 23 call sites, add type hints throughout,
and create tests for the new include_posts parameter."
```

#### Another Complex Pattern: Async/Await Migration

```bash
"Convert all database query functions from synchronous
to async/await pattern. Update all calling code.
Keep backward compatibility where possible with adapter
functions. Add type hints. Ensure tests still pass."
```

The agent will:
- Identify all database query functions
- Convert each to async
- Find all 100+ call sites
- Update them to use await
- Create adapter functions for gradual migration
- Update tests
- Validate everything still works

### Speaker Notes

These are the tasks that make agentic tools worth using. Manually, the database query conversion would take a developer 2-3 days. With an agentic tool, it's 10 minutes of setup and verification. The agent doesn't just find-and-replace—it understands the semantic meaning and updates everything that depends on the change.

---

## Slide 13: VS Code Plugin Example - GitHub Copilot

### Main Content

**GitHub Copilot** is the most popular AI coding assistant in VS Code.

#### Installation

```bash
# Install the Copilot extension from VS Code marketplace
# Sign in with your GitHub account
# Requires GitHub Copilot subscription
```

#### In-Line Completion

```python
# Start typing, Copilot suggests:

def calculate_average(numbers):
    # Copilot suggests:
    return sum(numbers) / len(numbers)

# Press Tab to accept, Escape to reject

def format_user_data(user):
    # Copilot suggests:
    return {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at.isoformat()
    }
```

#### Copilot Chat (CMD + Shift + I)

```
/explain - Explain what the selected code does
/doc - Generate documentation for the function
/fix - Identify and fix bugs in selected code
/generate - Generate code from description
/test - Generate unit tests for code

Example:

// Select a function, press CMD + Shift + I
// Type: /test

// Copilot generates:

describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid email', async () => {
      const user = await userService.createUser({
        email: 'test@example.com',
        name: 'Test User'
      });
      expect(user.id).toBeDefined();
      expect(user.email).toBe('test@example.com');
    });
  });
});
```

#### Context-Aware Suggestions

```typescript
// Copilot learns from your code style

// If your file has these patterns:
const users = await db.query('SELECT * FROM users');
const posts = await db.query('SELECT * FROM posts');

// Later, when you type:
const comments = await db.query(
  // Copilot suggests: 'SELECT * FROM comments'
)
```

### Speaker Notes

Copilot is excellent for real-time assistance while you're actively coding. It learns your patterns quickly and makes suggestions that match your style. The Chat interface extends this to more complex tasks. It's less powerful than dedicated terminal agents but requires less context-switching during development.

---

## Slide 14: Choosing the Right Tool for Code Generation

### Main Content

Decision matrix for different code generation tasks:

```
TASK                          BEST TOOL              WHY
────────────────────────────────────────────────────────────
Single function generation    Copilot (IDE)          Real-time, low friction
                              Cursor (CMD+K)

Component/module generation   Cursor                 Multiple file context
                              Windsurf

Multi-file refactoring        Aider                  Designed for this
                              Claude Code

Learning new framework        Cursor                 Immediate feedback
                              GitHub Copilot

Understanding existing code   Copilot Chat           In-editor explanation
                              Claude Code

Batch automation              Claude Code            Scriptable, repeatable
                              Terminal agents

Architecture design           Claude Code            Reason about patterns
                              Windsurf Cascade
```

#### Guidelines

1. **For Interactive Work**: Use IDE plugins (Cursor, Copilot)
   - Immediate feedback
   - Less context-switching
   - Good for prototyping

2. **For Complex Refactoring**: Use Terminal Agents (Aider, Claude Code)
   - Multi-file aware
   - Can chain operations
   - Good for systematic changes

3. **For Learning**: Use IDE with Chat (Cursor, Copilot)
   - Explanations built-in
   - Can ask questions iteratively
   - Stay in editor context

4. **For Automation**: Use Terminal Agents
   - Can be scripted
   - Good for CI/CD
   - Repeatable

### Speaker Notes

Most productive developers use multiple tools in combination. They might use Cursor during development for rapid iteration, then use Claude Code or Aider for larger refactoring tasks. The tools complement each other rather than competing. Students should experiment with multiple tools to find their preferred workflow.

---

# SECTION 3: FILE MANAGEMENT

---

## Slide 15: File Operations - Core Patterns

### Main Content

Agentic tools can completely automate file management through reading, creating, and editing files.

#### The File Operations Loop

```
┌─────────────────────────────────────┐
│ 1. SEARCH: Find relevant files      │
│    grep, glob patterns, semantic    │
│    search                           │
└──────────────┬──────────────────────┘
               │
┌──────────────v──────────────────────┐
│ 2. READ: Load file contents         │
│    Understand structure and context │
└──────────────┬──────────────────────┘
               │
┌──────────────v──────────────────────┐
│ 3. EDIT: Modify files               │
│    Add, remove, change code         │
│    Maintain formatting              │
└──────────────┬──────────────────────┘
               │
┌──────────────v──────────────────────┐
│ 4. WRITE: Save changes              │
│    Preserve permissions             │
│    Update timestamps                │
└──────────────┬──────────────────────┘
               │
┌──────────────v──────────────────────┐
│ 5. VALIDATE: Check results          │
│    Verify syntax                    │
│    Run linters                      │
│    Execute tests                    │
└─────────────────────────────────────┘
```

#### Creating Files - Example

```bash
claude code /workspace/project

"Create a Python module for configuration management with:
- ConfigManager class
- Support for loading from YAML files
- Environment variable override capability
- Type hints and docstrings
- Example configuration file"
```

#### Reading Files - Example

```bash
aider

aider> "Show me how authentication is currently implemented"

# Aider searches for auth-related files
# Reads authentication modules
# Summarizes the current approach
# Ready to discuss improvements
```

#### Editing Files - Example

```bash
aider

aider> "Update all docstrings to follow Google style guide"

# Aider:
# 1. Finds all Python files with docstrings
# 2. Reads docstring formatting in each
# 3. Converts to Google style
# 4. Validates syntax
# 5. Runs tests to ensure no logic changed
```

### Speaker Notes

The power of these operations in sequence is significant. A student might ask an agent to "add authentication to all API endpoints." The agent would need to: search for endpoint files, read them, understand the current structure, edit each one consistently, write them back, then validate the changes work. This multi-step orchestration is where agentic tools shine.

---

## Slide 16: Creating Files & Project Structure

### Main Content

Agentic tools can create entire project structures, not just individual files.

#### Creating Single File

```bash
claude code /workspace

"Create a .env.example file with all required environment
variables for the application, with helpful comments explaining
each variable"
```

Result:
```
# .env.example
# Database Configuration
DATABASE_URL=postgresql://localhost/myapp_dev
DATABASE_POOL_SIZE=10

# Authentication
JWT_SECRET=your-secret-key-here
JWT_EXPIRATION_HOURS=24

# API Configuration
API_PORT=8000
API_WORKERS=4

# Email Service
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USERNAME=your-email@example.com
SMTP_PASSWORD=your-app-password

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
```

#### Creating Project Structure

```bash
claude code /workspace

"Create a complete project structure for a FastAPI
microservice with:
- Source code organized by feature
- Tests directory with fixtures
- Configuration management
- Logging setup
- Docker configuration
- Requirements files
- Documentation"
```

Result:
```
my_service/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── logging_config.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   ├── services.py
│   │   └── schemas.py
│   ├── posts/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── routes.py
│   │   └── services.py
│   └── database/
│       ├── __init__.py
│       ├── connection.py
│       └── migrations/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   ├── test_posts.py
│   └── fixtures/
│       ├── __init__.py
│       └── users.json
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   ├── README.md
│   ├── API.md
│   └── SETUP.md
├── .env.example
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
└── .dockerignore
```

All with appropriate boilerplate code in each file.

### Speaker Notes

This capability is particularly valuable for rapid project setup. Instead of manually creating directories and files, students can describe their project architecture and have the agent create it. This is especially useful for learning—students can focus on writing business logic rather than project scaffolding.

---

## Slide 17: Reading & Understanding Files

### Main Content

Agentic tools can read files to understand context and make informed decisions.

#### Reading for Context

```bash
claude code /workspace/project

"I want to add caching to the user lookup function.
First, show me:
1. The current user lookup implementation
2. How users are currently fetched from the database
3. Any existing caching patterns in the codebase
4. The database schema for users"
```

Agent will:
- Read user service files
- Read database query files
- Search for existing cache implementations
- Read database schema files
- Summarize current architecture
- Propose caching solution based on existing patterns

#### Reading for Modification Planning

```bash
aider> "I need to change the logging format across the entire app.
>      Show me all logging calls and the current format."

# Aider reads and analyzes:
# - main.py logging setup
# - All files with logging calls
# - Current format string
# - Any logging configuration files

# Then presents findings:
# "Found 47 logging calls across 12 files using format:
#  [%(levelname)s] %(asctime)s - %(name)s - %(message)s
#  Ready to update to new format?"
```

### Speaker Notes

Reading files is foundational to all agentic operations. The agent must understand the existing code before making changes. This is why giving agents clear context produces better results—agents can read files to understand your project conventions and match them.

---

## Slide 18: Editing & Modifying Files

### Main Content

Precise file editing while maintaining formatting and structure.

#### String Replacement Pattern

```python
# Terminal agent knows:
# Find exact string location
# Replace with new content
# Preserve indentation
# Keep formatting consistent

# Example:
old_code = '''def login(email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if user.password == password:
        return user
    return None'''

new_code = '''def login(email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise ValueError("Invalid credentials")
    if not verify_password(password, user.password_hash):
        raise ValueError("Invalid credentials")
    return user'''
```

#### Multi-Edit in Single File

```bash
aider> "Update the User model to:
>      1. Add password_hash field instead of plain password
>      2. Add created_at timestamp
>      3. Add is_active boolean flag
>      4. Update all field validation rules
>      5. Add __repr__ method"
```

Aider handles all edits in one operation, maintaining file integrity.

#### Partial File Modification

```bash
claude code /workspace

"In the utils.py file, find the calculate_discount function.
Add input validation for negative amounts and minimum purchase
requirements. Keep the existing logic but add these checks
at the beginning."

# Claude Code:
# 1. Finds utils.py
# 2. Locates calculate_discount function
# 3. Adds validation logic
# 4. Preserves existing logic
# 5. Maintains code style
```

### Speaker Notes

The precision here matters. Unlike simple find-and-replace, agentic tools understand context. They know about indentation, line length, code style. They won't break a file by misaligned edits. This allows for surgical modifications even in complex files.

---

## Slide 19: Directory Operations & Project-Wide Changes

### Main Content

Managing entire directories and performing project-wide operations.

#### Directory Creation

```bash
claude code /workspace/project

"Create a comprehensive logging module under src/logging/
with:
- A Logger wrapper class around Python's logging
- Configuration for file and console handlers
- Different log levels for dev/prod
- Formatters with timestamps and colors
- Usage examples"
```

Agent creates entire directory structure with appropriate files.

#### Project-Wide Search & Replace

```bash
aider

aider> "Find all references to the old 'database_connection'
>       function throughout the project and replace with
>       'get_db_connection' with appropriate context managers.
>       Update all imports and fix any broken references."

# Aider:
# 1. Searches all files (respects .gitignore)
# 2. Finds 34 references across 8 files
# 3. Updates each with proper context
# 4. Verifies all imports resolve correctly
# 5. Runs tests
```

#### Organize Imports Project-Wide

```bash
claude code /workspace

"Run isort on all Python files to organize imports consistently.
Then run black to format code. Fix any linting errors afterward."

# Claude Code:
# 1. Finds all .py files
# 2. Runs isort
# 3. Runs black
# 4. Identifies linting errors
# 5. Fixes issues (removes unused imports, etc.)
# 6. Commits with appropriate message
```

#### Delete/Archive Operations

```bash
aider

aider> "Remove all the old migration files in
>       database/migrations/old/ and update any
>       references to them in the migration runner."

# Aider safely:
# 1. Identifies which migrations are old
# 2. Checks for any references
# 3. Updates migration runner if needed
# 4. Archives old files (doesn't permanently delete)
# 5. Runs tests to verify no breakage
```

### Speaker Notes

Project-wide operations are where students often waste time. Doing these manually—searching through files, updating each reference, verifying consistency—takes hours. Agentic tools automate this. A student might ask to "reorganize the project to separate API from business logic" and the agent can systematically move files, update imports, and verify everything still works.

---

## Slide 20: Git Integration with File Operations

### Main Content

Agentic tools understand Git and integrate file changes with version control.

#### Automatic Staging for Related Changes

```bash
aider

aider> "Add a new database field 'email_verified' to the User
>       model. Update the migration, model, tests, and API
>       response schema. Then show me what will be committed."

# Aider outputs:
Modified files:
  - models/user.py
  - database/migrations/20240115_add_email_verified.py
  - schemas/user_schema.py
  - tests/test_user_model.py

Ready to commit? (y/n)
```

#### Atomic Commits for Multi-File Changes

```bash
claude code /workspace

"Update all API endpoints to return consistent error responses.
Commit the changes with a detailed message explaining the new
error format and linking to the API documentation."

# Claude Code:
# 1. Updates all endpoint files
# 2. Updates error handling module
# 3. Creates/updates tests
# 4. Stages all related changes
# 5. Commits with message:

# "feat: standardize error response format across API
#
# - All endpoints now return errors in {error, code, details} format
# - Added validation for error codes
# - Updated tests to verify error format
# - See docs/ERROR_RESPONSES.md for details"
```

#### Branch Management for Experiments

```bash
aider

aider> "Create a branch called 'optimize-db-queries' and
>       implement query optimization in the user service.
>       Profile before and after, then commit with results."

# Aider:
# 1. Creates new branch
# 2. Implements optimizations
# 3. Profiles performance
# 4. Commits with performance metrics
# 5. Stays on branch for review
```

### Speaker Notes

Git integration is crucial for professional workflows. Agentic tools that understand version control can create logical commits that group related changes together. This makes code review easier and project history clearer than if a developer manually staged random combinations of files.

---

# SECTION 4: WRITING & DOCUMENTATION

---

## Slide 21: Documentation Generation from Code

### Main Content

Agentic tools can analyze code and automatically generate comprehensive documentation.

#### Module Documentation

```bash
claude code /workspace/project

"Generate comprehensive documentation for the entire
auth module in docs/AUTH.md. Include:
- Overview of authentication system
- Flow diagrams (in ASCII art)
- How to use each public function
- Security considerations
- Examples of common use cases"
```

Generated output might look like:

```markdown
# Authentication Module

## Overview
The authentication module handles user login, token generation,
and access control for the API.

## Architecture

┌─────────────┐
│ User Login  │
└──────┬──────┘
       │
       v
┌──────────────────┐
│ Verify Password  │
└──────┬───────────┘
       │
       v
┌──────────────────┐
│ Generate JWT     │
└──────┬───────────┘
       │
       v
┌──────────────────┐
│ Return Token     │
└──────────────────┘

## Usage Examples

### Basic Login
```python
from auth import authenticate_user

user = authenticate_user("user@example.com", "password")
if user:
    print(f"Logged in as {user.name}")
```

### Token Verification
```python
from auth import verify_token

token = request.headers.get("Authorization")
user = verify_token(token)
```

## Security Considerations
- Passwords are hashed using bcrypt with salt
- Tokens expire after 24 hours
- All authentication endpoints are rate-limited
```

#### API Documentation

```bash
aider

aider> "Generate complete API documentation in docs/API.md
>       for all endpoints in the routes/ directory. Include
>       request/response examples, authentication requirements,
>       error codes, and rate limiting info."
```

Result includes:
- Endpoint definitions with HTTP methods
- Required parameters and headers
- Request/response JSON examples
- Error responses with status codes
- Rate limiting information
- Authentication requirements

### Speaker Notes

Documentation is often the last thing developers do (or don't do at all). Agentic tools flip this—they can generate documentation first, which encourages writing self-documenting code. It also ensures documentation stays in sync with code changes.

---

## Slide 22: README & Getting Started Guides

### Main Content

Generate comprehensive README files that help new developers get started quickly.

#### Smart README Generation

```bash
claude code /workspace/project

"Create a comprehensive README.md that includes:
- Brief project description
- Feature list
- Prerequisites and installation instructions
- Quick start guide with example usage
- Project structure explanation
- Development setup (virtual env, dependencies, etc)
- How to run tests
- Troubleshooting common issues
- Contributing guidelines
- License info"
```

The agent will:
1. Read project structure
2. Examine main files to understand features
3. Check for requirements.txt/package.json
4. Find test directory and understand test setup
5. Look for CONTRIBUTING.md guidelines
6. Generate comprehensive README matching project

#### Setup Guide

```bash
claude code /workspace

"Create SETUP.md with step-by-step instructions for:
1. Setting up development environment
2. Configuring database
3. Setting environment variables
4. Running the application
5. Accessing the admin panel
6. Common setup errors and fixes"
```

Example output:

```markdown
# Development Setup Guide

## Prerequisites
- Python 3.10+
- PostgreSQL 12+
- Redis 6+

## Step 1: Clone and Create Virtual Environment
bash
git clone https://github.com/yourorg/yourproject
cd yourproject
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


## Step 2: Install Dependencies
bash
pip install -r requirements-dev.txt


## Step 3: Configure Environment
bash
cp .env.example .env
# Edit .env with your local settings


## Step 4: Initialize Database
bash
alembic upgrade head
python scripts/seed_db.py


## Step 5: Start Services
bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start application
python -m uvicorn src.main:app --reload


## Step 6: Verify Setup
bash
# Run tests
pytest

# Check API is running
curl http://localhost:8000/health
```

### Speaker Notes

Good README files are invaluable for onboarding. They're especially important in academic settings where students are learning new codebases constantly. An agent-generated README, customized to your specific project, can save hours of frustration during setup.

---

## Slide 23: API Documentation

### Main Content

Automatically generate API documentation from code.

#### OpenAPI/Swagger Generation

```bash
claude code /workspace

"Generate OpenAPI 3.0 specification for all API endpoints
in the routes/ directory. Include request/response schemas,
authentication requirements, error responses, and examples.
Output as openapi.yaml."
```

Result:
```yaml
openapi: 3.0.0
info:
  title: My API
  version: 1.0.0
paths:
  /api/users:
    get:
      summary: List all users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 10
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
      security:
        - bearerAuth: []
    post:
      summary: Create new user
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: User created
        '400':
          description: Invalid input
        '409':
          description: User already exists
```

#### Interactive Documentation

```bash
aider

aider> "Generate interactive API documentation using Swagger UI.
>       Include live examples for each endpoint that developers
>       can test directly in the browser."
```

The agent:
1. Analyzes all endpoints
2. Generates OpenAPI spec
3. Creates HTML Swagger UI interface
4. Makes it accessible at /docs

Students can then visit http://localhost:8000/docs and test all endpoints interactively.

### Speaker Notes

OpenAPI documentation is increasingly expected in professional development. It's the lingua franca for API communication across teams. Having an agent generate this automatically ensures it stays in sync with code changes and saves developers from maintaining documentation manually.

---

## Slide 24: Inline Code Comments & Docstrings

### Main Content

Agentic tools can add or improve code comments automatically.

#### Add Docstrings to Functions

```bash
claude code /workspace

"Add Google-style docstrings to all functions in models/user.py
that don't have them. Keep existing docstrings unchanged but
ensure consistency of style."
```

Before:
```python
def authenticate_user(email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if verify_password(password, user.password_hash):
        return user
    return None
```

After:
```python
def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate a user with email and password.

    Queries the database for a user with the given email and
    verifies the provided password against the stored hash.

    Args:
        email: User's email address.
        password: User's plaintext password.

    Returns:
        User object if authentication successful, None otherwise.

    Raises:
        DatabaseError: If database query fails.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if verify_password(password, user.password_hash):
        return user
    return None
```

#### Add Comments Explaining Complex Logic

```bash
aider

aider> "Add clear comments to the calculate_optimal_route function
>       explaining the algorithm, especially the heuristic used
>       for pruning. Assume reader has basic CS knowledge but
>       may not know this specific algorithm."
```

Before:
```python
def calculate_optimal_route(nodes, edges):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    cost = {start: 0}

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for next_node in neighbors(current):
            new_cost = cost[current] + edge_weight(current, next_node)
            if next_node not in cost or new_cost < cost[next_node]:
                cost[next_node] = new_cost
                frontier.put(next_node, new_cost + heuristic(next_node))

    return reconstruct_path(goal, cost)
```

After:
```python
def calculate_optimal_route(nodes, edges):
    # Use A* search algorithm: combines actual cost from start
    # with heuristic estimate to goal for efficient pathfinding
    frontier = PriorityQueue()  # Nodes to explore, prioritized by f-cost
    frontier.put(start, 0)
    cost = {start: 0}  # Track lowest cost to reach each node

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break

        # Check all neighbors of current node
        for next_node in neighbors(current):
            # Calculate cost through current node
            new_cost = cost[current] + edge_weight(current, next_node)

            # If this is a better path to next_node, update it
            if next_node not in cost or new_cost < cost[next_node]:
                cost[next_node] = new_cost
                # f-cost = actual cost + heuristic estimate
                # Heuristic is Euclidean distance (admissible)
                frontier.put(next_node, new_cost + heuristic(next_node))

    return reconstruct_path(goal, cost)
```

### Speaker Notes

Good comments are invaluable for learning and maintenance. Rather than asking students to write comments themselves (which they often skip), having an agent generate them ensures all code is documented. This also teaches students what good documentation looks like.

---

## Slide 25: Type Hints & Code Annotations

### Main Content

Agentic tools can add comprehensive type hints to improve code quality.

#### Add Type Hints to Untyped Code

```bash
claude code /workspace

"Add complete Python type hints to all functions in
services/user_service.py. Use Optional for nullable types,
List/Dict from typing, and create type aliases for complex
types. Update function signatures and add return type
annotations."
```

Before:
```python
def get_user_by_email(email):
    return db.query(User).filter(User.email == email).first()

def get_users_batch(user_ids):
    return db.query(User).filter(User.id.in_(user_ids)).all()

def create_user(name, email, password):
    user = User(name=name, email=email)
    user.password_hash = hash_password(password)
    db.add(user)
    db.commit()
    return user
```

After:
```python
from typing import Optional, List
from models import User

def get_user_by_email(email: str) -> Optional[User]:
    """Fetch user by email address."""
    return db.query(User).filter(User.email == email).first()

def get_users_batch(user_ids: List[int]) -> List[User]:
    """Fetch multiple users by IDs."""
    return db.query(User).filter(User.id.in_(user_ids)).all()

def create_user(name: str, email: str, password: str) -> User:
    """Create new user with hashed password."""
    user = User(name=name, email=email)
    user.password_hash = hash_password(password)
    db.add(user)
    db.commit()
    return user
```

#### Add Type Hints to Classes

```bash
aider

aider> "Add type hints to the UserService class. Include
>       instance variable type annotations in __init__,
>       method parameters and return types, and use
>       Protocol or Abstract Base Classes where appropriate."
```

### Speaker Notes

Type hints improve code quality and catch errors early. In Python, they're optional but increasingly expected in professional code. Having an agent add them automatically reduces friction—students get typed code without having to learn all the typing module intricacies.

---

## Slide 26: Changelog & Release Notes

### Main Content

Generate documentation of changes for releases.

#### Generate Changelog

```bash
claude code /workspace

"Analyze git history since the last release tag.
Generate a CHANGELOG.md entry following Keep A Changelog
format, categorizing changes as:
- Features (new functionality)
- Bugfixes (bug fixes)
- Breaking Changes (backward incompatible)
- Deprecated (marked for removal)
- Internal (refactoring, perf improvements)"
```

Result:
```markdown
# Changelog

## [2.1.0] - 2024-01-15

### Added
- New filtering API endpoint for advanced search (Issue #234)
- Caching layer for frequently accessed data
- Email notification system for user events
- Database connection pooling for improved performance

### Changed
- Updated authentication to use JWT tokens (Breaking Change)
- Improved error messages with more helpful suggestions
- Reorganized internal module structure for better maintainability

### Fixed
- Fixed race condition in concurrent user updates
- Corrected timezone handling in timestamp comparisons
- Resolved memory leak in websocket connections

### Deprecated
- Old token-based authentication (remove in v3.0.0)
- Legacy API endpoints /v1/users/* (use /v2/users instead)

### Performance
- Database queries optimized, 40% faster on average
- Reduced memory footprint by 25%
```

#### Generate Release Notes

```bash
aider

aider> "Create RELEASE_NOTES_v2.1.0.md with:
>       - Summary of major changes
>       - Upgrade instructions
>       - New features explained with examples
>       - Known limitations or bugs
>       - Thank you section for contributors"
```

### Speaker Notes

Release documentation is often forgotten but crucial. Users need to know what changed and how it affects them. An agent that tracks changes and generates organized release notes ensures this important communication happens automatically.

---

# SECTION 5: CODEBASE RESEARCH & SEARCH

---

## Slide 27: Semantic Code Search

### Main Content

Agentic tools can search code semantically, not just by text patterns.

#### Understanding Search vs. Find

```
TEXT SEARCH (Traditional):
grep "user_id" *.py
→ Finds all lines containing "user_id"
→ Lots of noise, requires manual filtering

SEMANTIC SEARCH (Agentic):
"Find where user IDs are validated"
→ Agent understands validation concept
→ Returns validation functions and calls
→ Contextual results
```

#### Real Example: Find All Queries

```bash
claude code /workspace

"Search the codebase for all database queries that touch
the User table. Show me:
1. Direct queries (SELECT, INSERT, UPDATE, DELETE)
2. ORM queries using the User model
3. Bulk operations
4. Any N+1 query problems

Organize by type and show the query pattern."
```

Agent will:
1. Search database directory
2. Read ORM definitions
3. Find User model queries throughout codebase
4. Analyze query patterns
5. Identify performance issues
6. Provide organized report:

```
Direct SQL Queries:
- src/database/users.py:45 - SELECT user WHERE id = ?
- src/database/users.py:78 - UPDATE user SET email = ?

ORM Queries:
- src/models/user.py:12 - User.query.filter(User.email == email)
- src/services/user_service.py:34 - db.query(User).all()

N+1 Issues Found:
- src/routes/posts.py:112 - Gets posts then loops loading user
  (Should use eager loading: User.query.options(joinedload))
```

#### Find Implementation Patterns

```bash
aider

aider> "Find all error handling patterns in the codebase.
>       Show me the different approaches used, which is most
>       common, and identify any inconsistencies."

# Aider analyzes:
# try/except blocks
# Error classes defined
# Error handling middleware
# Error response formats

# Returns:
# Pattern 1: Direct try/except blocks (23 occurrences)
#   Example: src/routes/users.py:45
#
# Pattern 2: Context managers for cleanup (8 occurrences)
#   Example: src/database/connection.py:12
#
# Pattern 3: Decorator-based error handling (5 occurrences)
#   Example: src/middleware/error_handler.py:3
#
# Inconsistencies found: 3
#   - Some endpoints return {error: ...}, others return {errors: [...]}
```

### Speaker Notes

Semantic search is what separates agentic tools from grep. When you're trying to understand a codebase, you don't want "find all occurrences of 'user'", you want "find where users are authenticated." Semantic search gives you meaningful results.

---

## Slide 28: Architecture Understanding

### Main Content

Agentic tools can analyze and explain your project's architecture.

#### Understanding Project Structure

```bash
claude code /workspace

"Analyze this project's architecture. Explain:
1. Main components and how they interact
2. Data flow (how data moves through the system)
3. Key design patterns used
4. External dependencies and integrations
5. Directory structure and module organization
6. Potential architectural issues or improvements"
```

Agent will:
1. Map project structure
2. Read key files
3. Identify components
4. Trace data flow
5. Recognize patterns
6. Generate architecture document

Example output:
```markdown
# Project Architecture

## Components

┌─────────────────────────────────────────────────┐
│ Client (React Web App)                          │
└────────────────┬────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────┐
│ API Gateway (FastAPI)                           │
│ - Authentication middleware                     │
│ - Request logging                               │
│ - Error handling                                │
└────┬────────────────────────────────┬───────────┘
     │                                │
     v                                v
┌──────────────────┐        ┌──────────────────┐
│ Business Logic   │        │ External APIs    │
│ - User Service   │        │ - Stripe API     │
│ - Post Service   │        │ - AWS S3         │
│ - Auth Service   │        │ - Email Service  │
└────┬─────────────┘        └──────────────────┘
     │
     v
┌─────────────────────────────────────────────────┐
│ Data Layer (SQLAlchemy ORM)                     │
│ - Database models                               │
│ - Query builders                                │
│ - Migrations                                    │
└────┬────────────────────────────────────────────┘
     │
     v
┌─────────────────────────────────────────────────┐
│ Database (PostgreSQL) + Cache (Redis)           │
└─────────────────────────────────────────────────┘

## Data Flow Example: Create Post

User (Frontend)
  → POST /api/posts (React)
    → API validation (Pydantic)
      → Authentication check (JWT)
        → Business logic (PostService)
          → Database query (SQLAlchemy)
            → PostgreSQL (Store)
          → Cache update (Redis)
        → Return response
      → Response middleware
    → JSON to client

## Key Patterns Used
1. Layered Architecture (Presentation, Business, Data)
2. Service Layer Pattern (PostService, UserService, etc.)
3. Dependency Injection (FastAPI dependencies)
4. Repository Pattern (Database access abstraction)
5. Middleware Pattern (Error handling, logging, auth)

## Architectural Improvements
1. Add event queue (RabbitMQ) for async operations
2. Implement CQRS for read-heavy queries
3. Add API versioning for backward compatibility
4. Consider microservices split if growth continues
```

### Speaker Notes

When students start on a new project, understanding the architecture is crucial but time-consuming. Having an agent generate an architecture diagram and explanation accelerates this understanding significantly. It also provides a baseline for discussions about design decisions.

---

## Slide 29: Dependency Mapping

### Main Content

Understand what code depends on what, and trace impact of changes.

#### Create Dependency Graph

```bash
claude code /workspace

"Create a dependency graph for this Python project showing:
1. Module dependencies
2. Which modules import which
3. Circular dependencies (if any)
4. External package dependencies
5. A visual representation (ASCII or description)"
```

Output example:
```
Dependency Graph:

main.py
  ├─ models/
  │  ├─ user.py
  │  │  └─ database/connection.py
  │  └─ post.py
  │     ├─ database/connection.py
  │     └─ models/user.py (CIRCULAR REFERENCE)
  │
  ├─ routes/
  │  ├─ user_routes.py
  │  │  ├─ services/user_service.py
  │  │  └─ models/user.py
  │  └─ post_routes.py
  │     ├─ services/post_service.py
  │     └─ models/post.py
  │
  └─ middleware/
     ├─ auth_middleware.py
     │  ├─ services/auth_service.py
     │  └─ models/user.py
     └─ error_handler.py

Circular Dependencies Found:
⚠️  models/user.py ↔ models/post.py
   (Suggestion: Create models/base.py for shared structures)

Import Statistics:
- Total modules: 24
- Total imports: 87
- Average imports per module: 3.6
- Most imported module: database/connection.py (imported 12 times)
- Most importing module: routes/ (imports from 8+ modules)
```

#### Impact Analysis

```bash
aider

aider> "I want to change the User model to add an 'avatar_url'
>       field. Show me everywhere this will impact."

# Aider traces dependencies:
# Direct imports of User model (will need updates):
#   - services/user_service.py
#   - routes/user_routes.py
#   - tests/test_user.py
#   - models/post.py (via relationship)
#
# Database impacts:
#   - Need migration for new field
#   - Update fixtures in tests
#
# API impacts:
#   - User response schema in schemas/user.py
#   - Documentation in docs/API.md
#
# Test impacts:
#   - Factory definitions for User objects
#   - Expected response fixtures
#
# Suggested order of changes:
# 1. Create migration
# 2. Update model
# 3. Update schema
# 4. Update factory
# 5. Update tests
# 6. Update API docs
```

### Speaker Notes

Dependency mapping is crucial for understanding refactoring impact. Students often don't realize that changing one file affects multiple others. An agent that traces these dependencies helps them think systematically about change management.

---

## Slide 30: Aider's Repository Map Concept

### Main Content

Aider has a unique feature called "repository map" that helps it understand codebases quickly.

#### How Repository Map Works

```bash
# Start Aider with auto repository mapping
aider --repo-map

# Aider automatically creates a summary of:
# 1. Project structure (directory tree)
# 2. File purposes (what each file does)
# 3. Key classes and functions
# 4. Import relationships
# 5. Most important files

# This map is shown to the AI before each operation
```

#### Repository Map Example

```
Repository Map Summary:

models/
  user.py (180 lines)
    - class User: Main user model with auth
    - class UserSchema: Pydantic validation

  post.py (95 lines)
    - class Post: Blog post model
    - relationships to User via foreign key

services/
  user_service.py (250 lines)
    - UserService: Main business logic for users
    - Methods: create, update, delete, find_by_email
    - Uses database session injected via dependency

  post_service.py (180 lines)
    - PostService: Blog post business logic
    - Depends on UserService for validation

routes/
  user_routes.py (120 lines)
    - /api/users GET: List users (paginated)
    - /api/users POST: Create user
    - /api/users/{id} GET/PUT/DELETE: User CRUD
    - Uses UserService

database/
  connection.py (45 lines)
    - Database connection setup
    - Session factory
    - Used throughout app

Key entry points:
  - main.py: FastAPI app creation
  - models/__init__.py: Model exports
  - services/__init__.py: Service exports

External dependencies:
  - sqlalchemy, pydantic, fastapi, pytest
```

#### Using Repository Map for Requests

```bash
aider

# Aider automatically knows:
# - What files to look at
# - How they're related
# - Project conventions

aider> "Add pagination to the list posts endpoint"

# Without repo map, Aider might miss:
# - Where pagination is already implemented (user route)
# - How it's done in this project
# - Where to add parameters

# With repo map, Aider:
# 1. Sees pagination in user_routes.py
# 2. Applies same pattern to post_routes.py
# 3. Updates schema if needed
# 4. Maintains consistency
```

### Speaker Notes

Repository map is a great feature for large codebases. Instead of Aider spending time exploring the structure, it gets a summary upfront. This makes Aider's responses faster and more contextual. For students learning a new codebase, understanding the repository map helps them organize their own understanding.

---

## Slide 31: Claude Code's Explore Agent

### Main Content

Claude Code has an "explore" agent capability for codebase analysis.

#### Using the Explore Agent

```bash
claude code /workspace

# Ask Claude Code to explore the codebase
"Explore the authentication system in this codebase.
Show me:
1. How users are authenticated
2. Where authentication happens (middleware, decorators, etc.)
3. Token/session management approach
4. Security measures in place
5. Potential vulnerabilities or improvements"

# Claude Code's explore agent will:
# 1. Search for auth-related files
# 2. Read authentication implementations
# 3. Track auth flow through the system
# 4. Analyze security practices
# 5. Report findings

# Output:
---
Authentication System Analysis

Location: src/auth/ and src/middleware/

Implementation:
- Uses JWT tokens (Bearer token scheme)
- Token generation in auth/token.py
- Validation via auth_middleware.py

Flow:
1. User logs in → POST /api/auth/login
2. Verify email/password → auth_service.py
3. Generate JWT with claims → Token valid for 24h
4. Return token to client
5. Client includes in Authorization header
6. Middleware verifies token on each request

Token Structure:
{
  "sub": user_id,
  "email": user.email,
  "iat": issued_at,
  "exp": expires_at
}

Security Measures:
✓ Passwords hashed with bcrypt
✓ Token expiration implemented
✓ Token signature verification
✗ No refresh token rotation
✗ No token revocation list

Recommendations:
1. Implement refresh tokens
2. Add token blacklist for logout
3. Rate limit login attempts
4. Consider multi-factor authentication
```

#### Exploring Specific Features

```bash
"Explore the payment processing system. Map out:
- Where payments are initiated
- Third-party service integration (Stripe/PayPal)
- Error handling for failed payments
- Webhook handling
- Database tracking of transactions"
```

The explore agent handles the detective work, freeing you to focus on understanding results.

### Speaker Notes

For large, unfamiliar codebases, the explore agent is invaluable. Rather than students manually searching through files, the agent does the investigation and presents organized findings. This is like having a tour guide through the codebase.

---

## Slide 32: Finding Code Patterns & Antipatterns

### Main Content

Agentic tools can identify common patterns and antipatterns in code.

#### Finding Duplicated Code

```bash
claude code /workspace

"Find duplicated code patterns across the codebase.
Show me:
1. Code that appears multiple times (copy-paste)
2. Functions with very similar logic
3. Validation code repeated in different places
4. Error handling patterns that should be unified
5. Candidates for extraction into reusable functions"
```

Result:
```
Code Duplication Analysis

Type 1: Exact Duplication (Copy-Paste)
- Email validation in routes/user.py:45 and routes/admin.py:78
- Both: re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)
- Status: Can extract to validators.py

- Database connection setup appears in:
  - database/connection.py (main)
  - tests/conftest.py (fixtures)
  - scripts/seed_db.py
- Status: Already in connection.py, imports elsewhere

Type 2: Similar Logic Patterns
- Error response formatting in 3 different middleware files
  {code: X, message: Y, details: Z}
- Status: Should centralize in error_handler.py

Type 3: Validation Code
- Password validation (8+ chars, 1 number, 1 symbol)
  - In auth_service.py:56
  - In routes/auth.py:34
  - In tests/test_auth.py:200
- Status: Extract to validators.py:password_validator()

Recommendations:
1. Create validators.py with extracted validation functions
2. Create error_formatter.py for consistent error responses
3. Use existing database/connection.py everywhere
4. Extract common API response patterns
```

#### Finding Antipatterns

```bash
aider

aider> "Find antipatterns in the codebase. Look for:
>      - N+1 database query problems
>      - Overly broad exception handlers
>      - Global state being modified
>      - Missing error handling
>      - Hardcoded values that should be config"

# Output:
Antipatterns Found:

1. N+1 Query Problem (Performance Issue)
   Location: routes/posts.py:112
   Problem:
     posts = db.query(Post).all()
     for post in posts:
         author = db.query(User).filter(User.id == post.user_id).first()
   Solution: Use eager loading
     posts = db.query(Post).options(joinedload(Post.user)).all()

2. Bare Except (Error Handling Issue)
   Location: services/cache.py:45
   Problem:
     try:
         value = redis.get(key)
     except:  # Catches everything, including KeyboardInterrupt!
         return None
   Solution:
     except RedisError:  # Specific exceptions only
         return None

3. Hardcoded Value (Config Issue)
   Location: config.py (3 occurrences)
   - DATABASE_POOL_SIZE = 10
   - CACHE_TTL = 3600
   - MAX_RETRIES = 3
   Solution: Move to environment variables
     DATABASE_POOL_SIZE = int(os.getenv('DATABASE_POOL_SIZE', '10'))
```

### Speaker Notes

Identifying patterns and antipatterns is crucial for code quality. Students often don't know what to look for. Having an agent automatically flag these helps them learn best practices. This is educational—students see examples of good and bad patterns in their own code.

---

## Slide 33: Testing Coverage Analysis

### Main Content

Agentic tools can analyze test coverage and identify gaps.

#### Coverage Analysis

```bash
claude code /workspace

"Analyze test coverage for the User module.
1. Run coverage analysis on models/user.py and services/user_service.py
2. Show which lines are uncovered
3. Identify which test cases are missing
4. Generate those missing test cases"
```

Result:
```
Test Coverage Report

models/user.py
  Line 15-20: validate_email()        [COVERED]    100%
  Line 22-30: hash_password()         [COVERED]    100%
  Line 32-40: User.__init__()         [COVERED]    95%
    ✗ Line 37: Exception case for invalid email
  Line 42-50: User.is_active check    [UNCOVERED]  0%

services/user_service.py
  Line 10-25: create_user()           [COVERED]    80%
    ✗ Line 18: Database constraint error
    ✗ Line 20: Email already exists case
  Line 27-45: get_user()              [COVERED]    100%
  Line 47-60: update_user()           [COVERED]    70%
    ✗ Line 55: Concurrent update race condition
  Line 62-75: delete_user()           [COVERED]    100%

Overall Coverage: 84% (need 90% for merge)

Missing Test Cases:
1. test_create_user_with_invalid_email()
2. test_create_user_with_duplicate_email()
3. test_create_user_database_error()
4. test_update_user_concurrent_modification()
5. test_user_is_active_property()

Generated test code:
---
def test_create_user_with_duplicate_email():
    existing_user = UserFactory(email='test@example.com')

    with pytest.raises(IntegrityError):
        user_service.create_user(
            email='test@example.com',
            name='Another User'
        )

def test_update_user_concurrent_modification():
    user = UserFactory()

    # Simulate concurrent modification
    with patch.object(User, 'save') as mock_save:
        mock_save.side_effect = StaleObjectError()

        with pytest.raises(StaleObjectError):
            user_service.update_user(user.id, {'name': 'Updated'})
```

### Speaker Notes

Test coverage is often neglected by students who don't see its value. Having an agent identify gaps and generate tests teaches both the importance of coverage and what good tests look like. It also ensures students hit coverage requirements for assignments.

---

## Slide 34: Finding Unused Code

### Main Content

Identify and remove dead code to keep codebase clean.

#### Dead Code Analysis

```bash
claude code /workspace

"Analyze the codebase for unused code. Find:
1. Functions that are never called
2. Imports that aren't used
3. Variables that are assigned but never used
4. Classes that have no subclasses or instantiations
5. Module-level code that's never executed

List them by file and recommend removals."
```

Result:
```
Unused Code Report

Unused Functions:
- src/utils.py:45 - format_timestamp() (imported by 0 modules)
- src/services/user_service.py:120 - deprecated_get_user() (marked deprecated, not called)
- src/routes/admin.py:200 - old_user_list_handler() (replaced by new endpoint)

Unused Imports:
- src/database/connection.py:1 - import threading (not used)
- src/models/user.py:5 - from datetime import timedelta (not used)
- src/services/post_service.py:12 - import json (not used)

Unused Variables:
- src/routes/posts.py:45 - page = request.args.get('page')  (unused)
- src/middleware/auth.py:32 - request_id = uuid.uuid4()  (unused)

Unused Classes:
- src/models/legacy.py:1 - LegacyUser (no instantiations, no subclasses)

Dead Code in Main Flow:
- src/main.py:89-95 - Conditional import that's never true

Removal Recommendations:
Priority 1 (Safe to remove):
  ✓ format_timestamp()
  ✓ unused imports

Priority 2 (Verify usage first):
  ✓ old_user_list_handler() - check API clients
  ✓ LegacyUser - check if used in migrations

Files to clean:
- src/utils.py (remove 1 function, 0 imports needed)
- src/database/connection.py (remove 1 import)
- src/models/legacy.py (remove entire file if safe)
```

#### Automatic Cleanup

```bash
aider

aider> "Remove all unused imports and dead code. Skip any
>       functions marked @deprecated or with # pragma: no cover.
>       Update tests if needed."

# Aider:
# 1. Removes unused imports
# 2. Deletes unused functions
# 3. Updates any dependent tests
# 4. Verifies all tests still pass
```

### Speaker Notes

Clean code is important for maintainability. Dead code accumulates over time and confuses new developers. Having an agent automatically identify and remove it teaches good practices and keeps codebases clean. This is also good for reducing bundle size in production.

---

## Slide 35: Architecture Review & Suggestions

### Main Content

Agentic tools can review your architecture and suggest improvements.

#### Architecture Review Request

```bash
claude code /workspace

"Review the overall architecture of this application.
Provide:
1. Strengths of the current design
2. Potential bottlenecks or scalability issues
3. Security considerations and gaps
4. Performance optimization opportunities
5. Refactoring suggestions with priority
6. Comparison with industry best practices"
```

Result:
```
Architecture Review Report

Strengths:
✓ Clear separation of concerns (routes, services, models)
✓ Dependency injection pattern reduces coupling
✓ Good use of ORM for database abstraction
✓ Comprehensive error handling middleware

Areas for Improvement:

1. CRITICAL: Database Query Performance
   Issue: Several N+1 query problems identified
   Impact: Query time grows with data size
   Fix: Implement eager loading and query optimization
   Effort: Medium (2-3 days)
   ROI: High (could 10x query performance)

2. HIGH: Missing Caching Layer
   Issue: Same queries executed repeatedly
   Impact: High database load, slow response times
   Fix: Add Redis caching for frequently accessed data
   Effort: Medium
   ROI: High

3. HIGH: Async Support
   Issue: Blocking operations in routes
   Impact: Single slow request blocks entire server
   Fix: Migrate to async/await with asyncio
   Effort: High (5-7 days)
   ROI: High (handle more concurrent users)

4. MEDIUM: API Versioning
   Issue: No version strategy
   Impact: Breaking changes affect all clients
   Fix: Implement /v1/, /v2/ versioning scheme
   Effort: Low
   ROI: Medium

5. MEDIUM: Logging
   Issue: Insufficient logging for debugging production issues
   Impact: Hard to diagnose problems
   Fix: Add structured logging, correlation IDs
   Effort: Low
   ROI: Medium

Security Review:

✓ Passwords properly hashed
✓ Authentication via JWT
✓ SQL injection protection (ORM)
✓ CORS configured

✗ No rate limiting (DOS vulnerability)
✗ No input validation on some endpoints
✗ Sensitive data logged to console
✗ No HTTPS enforcement

Recommendations Priority:
1. Add rate limiting (1 day, prevents DOS)
2. Add input validation to all endpoints (2 days, prevents injection)
3. Move secrets to environment variables (1 day, basic security)
4. Add query performance optimization (3 days, improves UX)
5. Implement caching (2 days, improves scalability)
```

### Speaker Notes

Architecture reviews are valuable but often done by senior developers. Having an agent provide this analysis teaches students what to look for and how to think about system design. Over time, as they see these reviews, they internalize these evaluation criteria.

---

## Slide 36: Codebase Metrics & Analytics

### Main Content

Analyze the codebase from a metrics perspective.

#### Generate Code Metrics

```bash
claude code /workspace

"Analyze the codebase and generate metrics. Report:
1. Lines of code (total, by module, by language)
2. Complexity metrics (cyclomatic complexity per function)
3. Test coverage percentage
4. Number of files and modules
5. Average file size
6. Most complex modules
7. Technical debt assessment"
```

Result:
```
Codebase Metrics Report

Size Metrics:
- Total Lines of Code: 12,450
- Total Files: 87
- Average File Size: 143 lines
- Languages: Python (11,200), SQL (800), YAML (450)

Breakdown by Module:
- models/: 1,200 lines (9.6%)
- services/: 2,100 lines (16.9%)
- routes/: 1,800 lines (14.5%)
- database/: 900 lines (7.2%)
- middleware/: 450 lines (3.6%)
- tests/: 4,000 lines (32.2%)

Complexity Analysis:
- Average cyclomatic complexity: 4.2
- Functions with high complexity (>10): 8
  - services/user_service.py:calculate_recommendations() - 15
  - services/post_service.py:search_posts() - 12
  - routes/admin.py:bulk_import() - 11

Test Metrics:
- Total test cases: 124
- Test coverage: 84%
- Passing tests: 122 (98.4%)
- Tests execution time: 2.3 seconds

File Statistics:
- Largest file: routes/admin.py (450 lines) - Complex
- Smallest file: models/base.py (12 lines) - Simple
- Most edited file: services/user_service.py (29 commits)
- Least edited file: middleware/cors.py (1 commit)

Technical Debt:
- High complexity functions: 8
- Functions with low test coverage: 12
- Deprecated code still in use: 3
- TODO comments: 7 (index: database caching)
- FIXME comments: 2 (index: edge case handling)

Estimated Debt: 15 dev-days to address

Trends:
- Code growing at 150 lines/week
- Test coverage stable at 84%
- Complexity increasing slightly (average 3.8 → 4.2)
```

### Speaker Notes

Metrics help teams understand code quality objectively. Rather than subjective "this code is messy," metrics provide concrete data. This is valuable for prioritization—focus on high-complexity functions and low-coverage areas. For students, these metrics teach what "good code metrics" look like.

---

# SECTION 6: ONLINE RESEARCH

---

## Slide 37: Web Search Capabilities

### Main Content

Agentic tools can search the internet to find information, solutions, and current best practices.

#### Direct Web Search

```bash
claude code /workspace

"Search the web for:
1. Current best practices for JWT token handling in 2024
2. Common security vulnerabilities in FastAPI applications
3. Performance benchmarks for PostgreSQL vs MongoDB
4. Recent articles on Python async/await optimization"
```

Result includes:
- Current articles and documentation
- Stack Overflow solutions
- GitHub implementations
- Performance benchmarks
- Organized by relevance

#### Research-Driven Development

```bash
claude code /workspace

"We're considering switching from SQLAlchemy to SQLModel.
Search for:
1. Comparison with SQLAlchemy
2. Current adoption rates
3. Known issues or limitations
4. Performance characteristics
5. Community size and support
Then give me a recommendation."
```

Agent will:
- Search latest benchmarks
- Find real-world usage examples
- Identify known issues
- Review community activity
- Provide informed recommendation

### Speaker Notes

Web search integration is powerful for staying current. Technologies change rapidly, and documentation becomes outdated. An agent that can search for current best practices ensures students are learning modern approaches, not decade-old patterns.

---

## Slide 38: URL Fetching & Content Analysis

### Main Content

Agentic tools can fetch and analyze content from URLs.

#### Fetch and Understand Documentation

```bash
claude code /workspace

"Visit https://fastapi.tiangolo.com/advanced/middleware/
and tell me:
1. How middleware works in FastAPI
2. Key concepts explained
3. Code examples provided
4. How it differs from other frameworks"
```

Agent will:
- Fetch the page
- Extract relevant content
- Analyze code examples
- Summarize key concepts
- Compare with other approaches

#### Analyze GitHub Repositories

```bash
claude code /workspace

"Go to https://github.com/tiangolo/fastapi-realworld-example-app
and analyze:
1. Project structure
2. How they organize code
3. Key technologies used
4. Testing patterns
5. Deployment approach"
```

Agent can:
- Clone or analyze repository
- Understand project organization
- Extract best practices
- Compare with your project
- Suggest improvements based on real-world example

#### Fetch and Integrate API Documentation

```bash
aider

aider> "Fetch https://api.example.com/docs and help me
>      integrate their API into our application by:
>      1. Understanding their API structure
>      2. Creating client code
>      3. Adding error handling
>      4. Writing tests"
```

### Speaker Notes

The ability to fetch and analyze remote content makes agentic tools like a research assistant. Instead of students manually visiting websites and reading documentation, the agent does the heavy lifting and presents organized findings.

---

## Slide 39: MCP Integration for External Data

### Main Content

MCP (Model Context Protocol) allows agentic tools to integrate with external services and data sources.

#### What is MCP?

```
MCP (Model Context Protocol) is a standard for connecting
AI tools to external data sources and services.

Tools can access:
├─ File systems (already covered)
├─ Git repositories
├─ Web APIs
├─ Databases
├─ Documentation systems
├─ Package repositories
└─ Custom data sources
```

#### MCP Examples

```bash
# Example: Search documentation
claude code /workspace

"Using MCP to search our internal documentation repository,
find articles about database optimization and summarize them.
Then recommend which optimizations apply to our codebase."
```

```bash
# Example: Query package repository
aider

aider> "Check npm registry via MCP to find the latest
>       version and recommendations for React, Redux, and
>       other packages we use. Update package.json with
>       latest stable versions."
```

```bash
# Example: Access database directly for analysis
claude code /workspace

"Connect via MCP to our production database (read-only)
and analyze:
1. Slow queries that should be optimized
2. Tables with missing indexes
3. Data distribution to identify bottlenecks"
```

#### Custom MCP for Your Team

Teams can create custom MCP connections to:
- Internal knowledge bases
- Company documentation
- Internal APIs
- Custom databases
- Project management tools

This allows agentic tools to understand company-specific context and conventions.

### Speaker Notes

MCP is an emerging standard that will become increasingly important. It essentially allows agentic tools to have access to anything a human developer has access to. This dramatically increases their capabilities while maintaining security through the standard protocol.

---

## Slide 40: Chaining Research Tasks

### Main Content

Agentic tools excel at chaining multiple research tasks together.

#### Multi-Step Research Example

```bash
claude code /workspace

"I need to evaluate whether to migrate from JWT to OAuth2.
Please:

1. Search for current security best practices comparing JWT vs OAuth2
2. Fetch the OAuth2 RFC and RFC 6750 to understand standards
3. Analyze our current authentication code (JWT implementation)
4. Find 3 well-regarded open-source projects using OAuth2
5. Compare implementation complexity vs security benefits
6. Estimate effort to migrate our 50+ endpoints
7. Make a recommendation with justification"
```

Agent will automatically:
1. Search web for comparisons
2. Fetch official standards
3. Read your current code
4. Analyze example projects
5. Reason about tradeoffs
6. Provide detailed recommendation

Result: Comprehensive analysis that would take a human days to compile.

#### Integrated Research & Implementation

```bash
aider

aider> "Research the current best practices for API rate limiting.
>       Then implement rate limiting in our FastAPI app following
>       the best practices you find. Include:
>       1. Search for current approaches (token bucket, sliding window)
>       2. Find recommended libraries
>       3. Implement in our app
>       4. Add tests
>       5. Document in README"

# Aider will:
# - Search for best practices
# - Find recommendation libraries
# - Implement using best practices
# - Add comprehensive tests
# - Document setup and usage
```

### Speaker Notes

The power of chaining research is that the agent handles the investigation upfront, then applies findings directly to your code. This bridges the gap between learning and implementation. Students don't just learn about best practices—they see them applied to their codebase.

---

# SECTION 7: GIT WORKFLOWS

---

## Slide 41: Commit Management

### Main Content

Agentic tools can create meaningful commits and organize code changes logically.

#### Atomic Commits

```bash
aider

aider> "I've made several changes to the user authentication system:
>      1. Updated password hashing to use Argon2
>      2. Added email verification
>      3. Refactored token generation
>      4. Updated tests
>      5. Added documentation
>
>      Create 4 separate atomic commits, each focused on one aspect.
>      Use conventional commit format."

# Aider will:
# 1. Stage password hashing changes → Commit
# 2. Stage email verification changes → Commit
# 3. Stage token generation refactor → Commit
# 4. Stage test and doc updates → Commit

# Results:
# commit 1abc2def
# Author: Student <student@example.com>
#
# feat(auth): migrate password hashing to Argon2
#
# - Replace bcrypt with Argon2 for better security
# - Update password validation logic
# - Maintain backward compatibility for existing hashes
#
# commit 2ghi3jkl
# feat(auth): add email verification workflow
#
# - Require email verification after signup
# - Send verification emails via SMTP
# - Add verified_at timestamp to User model
#
# commit 3mno4pqr
# refactor(auth): simplify token generation
#
# - Extract token generation logic
# - Add comprehensive docstrings
# - Improve error messages
#
# commit 4stu5vwx
# test(auth): add tests and update docs
#
# - 12 new test cases for auth flow
# - Update API documentation
# - Add migration guide in CHANGELOG
```

#### Conventional Commits

```bash
claude code /workspace

"Review all my recent changes and create a commit message
following the Conventional Commits standard. Format:

type(scope): subject

body (explaining why, not what)

Example:
feat(users): add email verification workflow

- Require email verification after signup
- Add verified_at field to User model
- Send verification tokens via email
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `test`: Adding tests
- `docs`: Documentation
- `chore`: Build, dependencies, etc.

### Speaker Notes

Good commit messages are crucial for project history. Students often write meaningless messages like "fixed stuff" or "update file". Having an agent create meaningful, conventional commit messages teaches good practices and makes project history readable.

---

## Slide 42: Branch Management & Feature Isolation

### Main Content

Agentic tools can manage branches and isolate features effectively.

#### Create and Manage Feature Branches

```bash
claude code /workspace

"Create a feature branch for 'add-two-factor-auth'.
Build the complete feature including:
1. Database schema changes (migration)
2. Backend implementation
3. API endpoints
4. Tests
5. Documentation

Then stay on this branch for review before merging."
```

Agent will:
1. Create branch `feature/add-two-factor-auth`
2. Implement all components
3. Test thoroughly
4. Keep branch clean and ready for PR

#### Branch from Issue

```bash
aider

aider> "Create a branch for GitHub issue #234 which requests
>       'improve error messages'. Fix the issue and keep branch
>       for PR creation. Branch name: issue-234-error-messages"
```

#### Compare Branches

```bash
claude code /workspace

"Show me the differences between main and my feature branch.
List:
1. Files changed
2. Lines added/removed
3. Summary of changes
4. Potential conflicts if merging now"
```

Result:
```
Branch Comparison: main → feature/caching

Files changed: 7
- src/services/cache.py (NEW)
- src/config.py (MODIFIED)
- src/models/user.py (MODIFIED)
- src/routes/users.py (MODIFIED)
- tests/test_cache.py (NEW)
- docs/CACHING.md (NEW)
- requirements.txt (MODIFIED)

Stats:
- Lines added: 342
- Lines removed: 18
- Net change: +324 lines

Potential conflicts:
- requirements.txt has 2 new dependencies
  (check with poetry.lock if using Poetry)
- models/user.py has cache_invalidation field
  (verify with main branch changes)
```

### Speaker Notes

Effective branch management is important for collaborative development. Students often work on main or create branches without clear purpose. Teaching them to create focused feature branches with clear naming conventions improves their development practices.

---

## Slide 43: Pull Request Creation & Management

### Main Content

Agentic tools can help create well-structured pull requests.

#### Generate PR Description

```bash
claude code /workspace

"Create a pull request from feature/auth-refactor to main.
Generate a comprehensive PR description including:
1. What changed and why
2. Testing performed
3. Related issues
4. Screenshots if applicable
5. Deployment notes
6. Review checklist"
```

Generated PR:

```markdown
# Pull Request: Refactor Authentication System

## Description
This PR refactors the authentication system to improve security,
maintainability, and testability. All authentication logic has been
moved to a dedicated auth service, reducing coupling between routes
and business logic.

## Changes Made
- Created new `services/auth_service.py` with centralized auth logic
- Updated all auth-related routes to use new service
- Migrated from bcrypt to Argon2 for password hashing
- Added email verification workflow
- Removed duplicate code in 3 route handlers

## Testing
- Added 15 new unit tests for auth service
- All existing tests still pass (127/127)
- Tested locally with both email and OAuth providers
- Verified password migration works correctly

## Related Issues
Closes #234 - Improve authentication architecture
Closes #245 - Add email verification

## Deployment Notes
- Requires new environment variables: ARGON2_MEMORY, ARGON2_TIME
- Database migration required (run `alembic upgrade head`)
- Existing user passwords will be rehashed on next login

## Checklist
- [x] Tests pass locally
- [x] Code follows project style guide
- [x] Documentation updated
- [x] No new warnings from linter
- [x] Database migration created
- [x] Backward compatibility maintained

## Screenshots / Demo
[N/A - backend changes only]
```

#### Review PR Automatically

```bash
aider

aider> "Review this pull request for:
>      1. Code quality issues
>      2. Test coverage gaps
>      3. Performance concerns
>      4. Security vulnerabilities
>      5. Documentation completeness"

# Aider provides detailed review with specific file/line comments
```

### Speaker Notes

PRs are how code gets reviewed and merged in professional environments. Having agents help create comprehensive PR descriptions and even provide reviews (though human review is always needed) teaches best practices and improves code quality.

---

## Slide 44: Merge Conflict Resolution

### Main Content

Agentic tools can help resolve merge conflicts intelligently.

#### Identify and Resolve Conflicts

```bash
claude code /workspace

"Our feature branch has conflicts with main. Please:
1. Identify which files have conflicts
2. Analyze the conflicts to understand root cause
3. Propose resolution for each conflict
4. Implement resolution
5. Test to ensure nothing broke"
```

Agent will:
1. Show conflicting sections
2. Explain what each branch changed
3. Propose intelligent merging
4. Run tests to verify
5. Resolve conflicts automatically if safe

Example:

```
Conflict Analysis

File: src/services/user_service.py

Conflict 1 (Line 45):
Main branch:
    def get_user(user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        return user

Feature branch:
    def get_user(user_id: int) -> Optional[User]:
        user = db.query(User).filter(User.id == user_id).first()
        return user

Resolution: Use feature branch (adds Optional type hint - improvement)

Conflict 2 (Line 67):
Main branch: Added caching decorator
Feature branch: Added logging decorator

Resolution: Keep both - can be combined
    @cache_result
    @log_execution
    def search_users(query: str):
        ...

After resolution:
- 2 conflicts resolved
- Tests run: PASS
- Ready to merge
```

#### Abort and Rebase

```bash
aider

aider> "The conflicts are too complex. Rebase our branch
>       on top of latest main and resolve conflicts interactively."

# This brings in latest main changes first, then replays
# your branch changes, making conflicts clearer
```

### Speaker Notes

Merge conflicts intimidate many students. Having an agent analyze and resolve them teaches what's actually happening (not just "press resolve button"). Over time, students understand conflict resolution better and can handle it themselves.

---

## Slide 45: Automatic Commit Messages from Code Changes

### Main Content

Agentic tools can analyze code changes and generate meaningful commit messages automatically.

#### Smart Commit Message Generation

```bash
claude code /workspace

# You've modified multiple files, now ask agent to generate commit message

"Analyze my staged changes and generate an appropriate
conventional commit message. Consider:
1. What functionality is being added/changed
2. Why it was needed
3. Any breaking changes
4. References to issues if fixed"
```

Agent analyzes:
```
Staged changes:
  - models/post.py: Added is_pinned field and setter
  - routes/posts.py: Added /pin endpoint
  - tests/test_posts.py: Added tests for pinning
  - docs/API.md: Added documentation for new endpoint

Generated commit message:

feat(posts): add ability to pin posts

Allow users to pin important posts to the top of their profile.
- Add is_pinned boolean field to Post model
- Create /api/posts/{id}/pin endpoint for toggling pin status
- Add proper permission checks (user can only pin own posts)
- Include comprehensive tests
- Update API documentation

Closes #189
```

#### Learn from Existing Commits

```bash
aider

aider> "Generate commit messages that match the style and
>      format of our 10 most recent commits.
>      Analyze our commit history to understand our conventions."

# Aider reads recent commits:
# - Format preferences (subject line length, body style)
# - Emoji usage (if any)
# - Issue reference format
# - Scope conventions

# Then generates messages matching these patterns
```

### Speaker Notes

Consistent commit messages are hard for students. Having an agent generate them teaches message structure and makes project history clean. Over time, students internalize these patterns and can write good messages themselves.

---

## Slide 46: Git Workflow Best Practices

### Main Content

Summary of effective Git workflows with agentic tools.

#### Recommended Workflow for Students

```
┌────────────────────────────────────────────────────┐
│ 1. START FEATURE                                   │
│    $ aider                                         │
│    aider> "/create-branch feature/add-auth"       │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────v─────────────────────────────────┐
│ 2. IMPLEMENT FEATURE                              │
│    aider> "Add JWT authentication to app"         │
│    (Aider implements, commits regularly)          │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────v─────────────────────────────────┐
│ 3. TEST LOCALLY                                   │
│    aider> "Run all tests and verify nothing broke"│
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────v─────────────────────────────────┐
│ 4. CREATE PR                                      │
│    $ gh pr create                                 │
│    (Aider generates comprehensive description)   │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────v─────────────────────────────────┐
│ 5. REQUEST REVIEW                                 │
│    (Team reviews code and provides feedback)      │
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────v─────────────────────────────────┐
│ 6. ADDRESS FEEDBACK                               │
│    aider> "Address review feedback"              │
│    (Implement suggestions, new commit with history)
└────────────────┬─────────────────────────────────┘
                 │
┌────────────────v─────────────────────────────────┐
│ 7. MERGE                                          │
│    $ gh pr merge                                  │
│    (Code merged to main)                         │
└────────────────────────────────────────────────────┘
```

#### Key Principles

1. **One Feature Per Branch**
   - Keep branches focused
   - Easier to review
   - Simpler to merge

2. **Atomic Commits**
   - Each commit should be logically complete
   - Agentic tools help organize this
   - Makes history readable

3. **Meaningful Messages**
   - Use conventional commits
   - Explain why, not just what
   - Agentic tools help generate these

4. **Regular Testing**
   - Test after each change
   - Catch issues early
   - Agentic tools can run tests automatically

5. **Code Review Before Merge**
   - Never merge unreviewed code
   - PRs facilitate this
   - Agentic tools help create good PRs

#### Real Terminal Agent Workflow Example

```bash
# Day 1: Create feature branch and start implementation
$ cd /workspace/project
$ aider

aider> "/create-branch feature/caching-layer"

aider> "Implement Redis caching for user lookups:
>       1. Create cache service wrapper
>       2. Add cache invalidation on user updates
>       3. Implement TTL configuration
>       4. Add comprehensive tests
>       5. Document caching strategy"

# (Aider implements everything, creates multiple commits)

# Day 2: Verify and create PR
aider> "Run all tests and ensure everything passes"

aider> "Create a pull request with comprehensive description
>       explaining the caching implementation"

# (Aider generates PR with good description)

# Day 3: Address code review feedback
# (Team provides feedback via PR comments)

aider> "Address the code review feedback from the team:
>       - Add cache warming on startup
>       - Add metrics for cache hit rate
>       - Add documentation for cache configuration"

# (Aider implements feedback)

# Day 4: Merge
$ gh pr merge

# (Feature merged to main, history is clean and understandable)
```

### Speaker Notes

This workflow combines all the Git concepts students have learned. Emphasize that agentic tools don't replace human code review—they enhance the process by automating mechanical work (commits, branch creation, PR generation) so humans can focus on meaningful review.

---

## CONCLUSION

---

## Final Thoughts: Integrating These Tools Into Your Workflow

### Key Takeaways

1. **Terminal Agents** (Claude Code, Aider, GitHub Copilot CLI) are most powerful
   - Can chain operations automatically
   - Best for multi-file refactoring
   - Scriptable and repeatable
   - Integrate with CI/CD

2. **IDE Plugins** (Cursor, Windsurf, VS Code Copilot) excel at real-time feedback
   - Immediate suggestions
   - Less context-switching
   - Great for learning
   - Good for rapid prototyping

3. **Web Integration** allows research-driven development
   - Search for solutions
   - Fetch documentation
   - Stay current with best practices
   - Integrate external APIs

4. **Git Integration** enables professional workflows
   - Atomic commits
   - Meaningful messages
   - Branch management
   - PR automation

### Next Steps

1. Choose your primary tool (Recommend: Start with Cursor or Claude Code)
2. Practice simple tasks first (file creation, reading, editing)
3. Graduate to multi-file operations (refactoring, testing)
4. Integrate into your workflow gradually
5. Build custom workflows and automation

### Resources for Deeper Learning

- Official documentation for your chosen tool
- YouTube tutorials and demonstrations
- GitHub repositories using agentic tools effectively
- Community forums and discussions
- This slideshow - review sections relevant to your work

---

## End of Part 2: Basic Usage

### What You've Learned

You now understand:
- How agentic tools reason and operate
- Code generation and editing capabilities
- File management and project operations
- Documentation generation
- Codebase research and analysis
- Online research integration
- Git workflows and best practices

### What's Next

Part 3 will cover:
- Advanced techniques and automation
- Custom workflows for specific domains
- Performance optimization strategies
- Debugging with agentic tools
- Building your own agentic workflows

---

## Appendix: Quick Reference Guide

### Terminal Agent Commands

**Claude Code**
```bash
claude code /path/to/project
# Interactive terminal-based agent
```

**Aider**
```bash
aider src/file1.py src/file2.py
# Conversational code editing
```

**GitHub Copilot CLI**
```bash
gh copilot suggest "what you want to do"
gh copilot explain "command to understand"
```

### Common Tasks Quick Reference

**Generate Function**: "Create a function that [description]"
**Refactor Code**: "Refactor [file/section] to [improvement]"
**Add Tests**: "Write tests for [function/module]"
**Debug Issue**: "Help me debug [error/behavior]"
**Understand Code**: "Explain what this code does: [code]"
**Search Pattern**: "Find all [pattern] in the codebase"
**Create Docs**: "Generate documentation for [module]"
**Fix Error**: "Fix this error: [error message]"

---

End of Slideshow Part 2: Basic Usage

Total Slides: 46
Total Sections: 7
Focus: Terminal-based agents with comprehensive examples and real commands
