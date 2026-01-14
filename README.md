# project-context-mcp

[![PyPI version](https://badge.fury.io/py/project-context-mcp.svg)](https://badge.fury.io/py/project-context-mcp)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

**Give Claude Code instant access to your project's institutional knowledge.**

An MCP server that makes your project documentation instantly accessible in Claude Code through `@` mentions. Create a `.context/` folder, add your docs, and watch Claude become an expert on *your* codebase.

---

## The Problem

You're working with Claude Code on a complex project. Claude is smart, but it doesn't know:

- Your team's coding conventions
- Why you chose that weird architecture
- The gotchas in your database schema
- Your API design patterns
- That one thing that breaks if you don't do it *just right*

You end up copy-pasting the same context into every conversation. Or worse, Claude makes suggestions that violate your project's conventions.

## The Solution

Create a `.context/` folder in your project. Drop in your documentation. Now when you type `@` in Claude Code, your context files appear right alongside your source files:

```
┌─────────────────────────────────────────────────────────────┐
│  > Help me add a new API endpoint @                         │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Suggestions:                                         │   │
│  │   📄 src/api/routes.py                              │   │
│  │   📄 src/models/user.py                             │   │
│  │   📘 architecture.md          <- Your context!      │   │
│  │   📘 api-patterns.md          <- Your context!      │   │
│  │   📘 conventions.md           <- Your context!      │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

One `@api-patterns.md` mention and Claude knows exactly how you structure endpoints.

---

## Quick Start

### 1. Install the MCP server (one time)

```bash
claude mcp add project-context -s user -- uvx project-context-mcp
```

That's it. The server is now available in all your Claude Code sessions.

### 2. Create a `.context/` folder in your project

```
my-project/
├── .context/               <- Create this folder
│   ├── architecture.md
│   ├── conventions.md
│   └── api-patterns.md
├── src/
├── tests/
└── ...
```

### 3. Use `@` to include context

```
> Help me refactor this function @conventions.md
> Add a new database table @database-schema.md @naming-conventions.md
> Why is this test failing? @architecture.md @testing-patterns.md
```

---

## What to Put in `.context/`

Your `.context/` folder is for **institutional knowledge** — the stuff that isn't obvious from reading the code.

### Recommended Files

| File | What to Include |
|------|-----------------|
| `architecture.md` | System overview, component relationships, data flow diagrams |
| `conventions.md` | Coding standards, naming conventions, file organization |
| `api-patterns.md` | Endpoint structure, authentication, error handling patterns |
| `database-schema.md` | Table relationships, naming conventions, migration patterns |
| `testing-patterns.md` | Test organization, mocking strategies, fixture patterns |
| `deployment.md` | Environment setup, deployment procedures, rollback steps |
| `gotchas.md` | Known issues, workarounds, "don't do this" warnings |
| `glossary.md` | Domain-specific terms, abbreviations, business logic |

### Example: `conventions.md`

```markdown
# Coding Conventions

## Naming
- Files: `snake_case.py`
- Classes: `PascalCase`
- Functions: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

## Error Handling
- Use custom exceptions from `src/exceptions.py`
- Always log with context: `logger.error("Failed to process", extra={"user_id": id})`
- API endpoints return `{"error": {"code": "...", "message": "..."}}`

## Testing
- One test file per module: `test_<module_name>.py`
- Use fixtures from `conftest.py`, don't create new ones without discussion
- Mock external services, never hit real APIs in tests
```

### Example: `architecture.md`

```markdown
# Architecture Overview

## System Components

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Next.js   │────▶│   FastAPI   │────▶│  PostgreSQL │
│  Frontend   │     │   Backend   │     │   Database  │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                           ▼
                    ┌─────────────┐
                    │    Redis    │
                    │    Cache    │
                    └─────────────┘

## Key Design Decisions

1. **Why FastAPI over Flask?**
   - Native async support for high-concurrency endpoints
   - Automatic OpenAPI documentation
   - Pydantic validation built-in

2. **Why Redis for caching?**
   - Session storage for horizontal scaling
   - Rate limiting with sliding windows
   - Pub/sub for real-time features
```

---

## Supported File Types

The server exposes files with these extensions:

| Category | Extensions |
|----------|------------|
| **Documentation** | `.md`, `.txt`, `.rst`, `.asciidoc`, `.adoc` |
| **Data/Config** | `.yaml`, `.yml`, `.json`, `.toml`, `.xml`, `.csv`, `.ini`, `.cfg`, `.conf` |
| **Code Examples** | `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.html`, `.css`, `.sql`, `.sh` |

**Automatically excluded:** Hidden files (`.foo`), `__pycache__`, `node_modules`, `.git`, `.DS_Store`

---

## Features

### Smart Resource Names

The server extracts human-readable names from your files:

- Markdown files: Uses the first `# Heading` as the name
- Other files: Converts filename to title case (`api-patterns.md` → "Api Patterns")

### Automatic Descriptions

First paragraph of each file becomes the description shown in autocomplete, helping you pick the right context quickly.

### Nested Folders

Organize complex documentation with subfolders:

```
.context/
├── architecture.md
├── api/
│   ├── authentication.md
│   ├── pagination.md
│   └── error-codes.md
├── database/
│   ├── schema.md
│   └── migrations.md
└── frontend/
    ├── components.md
    └── state-management.md
```

All files are discovered recursively and accessible via `@`.

### Zero Configuration

No config files. No setup. No environment variables. Just create `.context/` and go.

---

## How It Works

```
┌──────────────────┐         ┌─────────────────────┐
│   Claude Code    │◀───────▶│  project-context-mcp │
│                  │   MCP   │                     │
│  You type: @     │ Protocol│  1. Finds .context/ │
│                  │         │  2. Lists all files │
│  Server returns  │◀────────│  3. Returns as      │
│  your docs as    │         │     MCP resources   │
│  suggestions     │         │                     │
└──────────────────┘         └─────────────────────┘
```

1. **On startup**: MCP server checks current directory for `.context/`
2. **On `@` keystroke**: Claude Code requests available resources
3. **Server responds**: List of files with names, descriptions, and URIs
4. **On selection**: File content is fetched and included in your prompt

### URI Scheme

Resources use the `context://` scheme:
- `.context/architecture.md` → `context://architecture.md`
- `.context/api/patterns.md` → `context://api/patterns.md`

---

## Use Cases

### Onboarding New Team Members

Share your `.context/` folder in your repo. New developers get the same Claude experience as veterans — Claude knows the conventions from day one.

### Enforcing Consistency

Instead of hoping everyone remembers the coding standards, put them in `.context/conventions.md`. Claude will suggest code that matches your patterns.

### Complex Domains

Working in healthcare? Finance? Legal tech? Put your domain glossary and business rules in `.context/`. Claude won't confuse your specific terminology.

### Legacy Codebases

Document the "why" behind legacy decisions. When Claude suggests a refactor, you can include `@legacy-decisions.md` to explain constraints.

### Multi-Service Architecture

Keep architecture docs in context. Claude can help you make changes that respect service boundaries and communication patterns.

---

## Comparison

| Approach | Pros | Cons |
|----------|------|------|
| **Copy-paste context** | No setup | Tedious, inconsistent, clutters prompt |
| **CLAUDE.md file** | Auto-included | Single file, always included even when not relevant |
| **`.context/` folder** | Organized, selective, discoverable | Requires explicit `@` mention |

This tool is ideal when you have **multiple context documents** and want to **selectively include** the relevant ones for each task.

---

## Installation Options

### Recommended: uvx (no install needed)

```bash
claude mcp add project-context -s user -- uvx project-context-mcp
```

### Alternative: pip install

```bash
pip install project-context-mcp
claude mcp add project-context -s user -- project-context-mcp
```

### Development: from source

```bash
git clone https://github.com/ericbrown/project-context-mcp.git
cd project-context-mcp
pip install -e .
claude mcp add project-context -s user -- python -m project_context_mcp.server
```

---

## Troubleshooting

### Context files not appearing?

1. **Check the folder name**: Must be exactly `.context/` (with the dot)
2. **Check file extensions**: Only [supported types](#supported-file-types) are included
3. **Restart Claude Code**: MCP servers initialize on startup
4. **Check server is registered**: Run `claude mcp list`

### Want to see what's discovered?

Run the server directly to see logs:

```bash
cd your-project
python -m project_context_mcp.server
```

You'll see:
```
INFO:project-context-mcp:Starting project-context-mcp server
INFO:project-context-mcp:Working directory: /path/to/your-project
INFO:project-context-mcp:Looking for context in: /path/to/your-project/.context
INFO:project-context-mcp:Found 5 context resources
```

---

## Contributing

Contributions welcome! Ideas for improvements:

- [ ] File watching for hot reload
- [ ] `context.yaml` manifest for custom metadata
- [ ] Search tool to find content across context files
- [ ] Support for remote context (URLs, Notion, Confluence)
- [ ] Team sync via cloud storage

### Development Setup

```bash
git clone https://github.com/ericbrown/project-context-mcp.git
cd project-context-mcp
pip install -e .
```

### Running Tests

```bash
cd examples/sample-project
python -m project_context_mcp.server
```

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Related

- [Model Context Protocol](https://modelcontextprotocol.io/) — The protocol this server implements
- [Claude Code](https://claude.ai/code) — Anthropic's CLI for Claude
- [MCP Servers](https://github.com/modelcontextprotocol/servers) — Other MCP server implementations

---

**Built for developers who are tired of repeating themselves.**

*Star this repo if it saves you time!*
