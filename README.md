# project-context-mcp

An MCP (Model Context Protocol) server that exposes files from a `.context/` directory as resources in Claude Code. This creates a convention for "always-available project context" similar to Claude Desktop's project files feature.

## Installation

Install the server globally for Claude Code (one-time setup):

```bash
claude mcp add project-context -s user -- uvx project-context-mcp
```

## Usage

### 1. Create a `.context/` folder in your project

```
my-project/
├── .context/
│   ├── architecture.md
│   ├── conventions.md
│   └── api-patterns.md
├── src/
└── ...
```

### 2. Add project documentation

Put any documentation you want readily available in the `.context/` folder. Common examples:

- `architecture.md` - System architecture overview
- `conventions.md` - Coding standards and patterns
- `api-patterns.md` - API design guidelines
- `database-schema.md` - Database structure documentation
- `deployment.md` - Deployment procedures

### 3. Use `@` mentions in Claude Code

When you type `@` in Claude Code, your context files appear as suggestions:

```
@ Suggestions:
  src/main.py
  .context/architecture.md    ← Context files appear here
  .context/conventions.md
  .context/api-patterns.md
```

Include relevant context in your prompts:

```
> Help me add a new endpoint @api-patterns.md @conventions.md
```

## Supported File Types

The server exposes files with these extensions:

- **Documentation**: `.md`, `.txt`, `.rst`, `.asciidoc`, `.adoc`
- **Data**: `.yaml`, `.yml`, `.json`, `.toml`, `.xml`, `.csv`
- **Config**: `.ini`, `.cfg`, `.conf`
- **Code**: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.html`, `.css`, `.sql`
- **Scripts**: `.sh`, `.bash`, `.zsh`

Hidden files (starting with `.`) and common ignore patterns (`__pycache__`, `node_modules`, etc.) are automatically excluded.

## Configuration

No configuration needed. The server automatically:

- Looks for `.context/` in the current working directory
- Recursively discovers all supported files
- Extracts names and descriptions from file content
- Handles missing `.context/` directories gracefully

## How It Works

1. When Claude Code starts in a directory, the MCP server checks for a `.context/` folder
2. All supported files in that folder are exposed as MCP resources
3. Resources appear in Claude Code's `@` autocomplete menu
4. When you select a resource, its content is included in your conversation

### URI Scheme

Resources use the `context://` URI scheme:

- `.context/architecture.md` → `context://architecture.md`
- `.context/api/patterns.md` → `context://api/patterns.md`

## Example

See the `examples/sample-project/` directory for a demonstration of how to structure your `.context/` folder.

## Development

### Local Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/project-context-mcp.git
cd project-context-mcp

# Install in development mode
pip install -e .

# Run the server directly
python -m project_context_mcp.server
```

### Testing with Claude Code

```bash
# Add local version to Claude Code
claude mcp add project-context -s user -- python -m project_context_mcp.server
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.
