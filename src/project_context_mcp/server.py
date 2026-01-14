#!/usr/bin/env python3
"""
MCP server that exposes .context/ folder files as resources.
"""

import asyncio
import logging
import mimetypes
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Resource

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("project-context-mcp")

# File extensions to include
SUPPORTED_EXTENSIONS = {
    ".md", ".txt", ".yaml", ".yml", ".json", ".toml",
    ".sql", ".py", ".js", ".ts", ".jsx", ".tsx",
    ".html", ".css", ".sh", ".bash", ".zsh",
    ".xml", ".csv", ".ini", ".cfg", ".conf",
    ".rst", ".asciidoc", ".adoc"
}

# Patterns to ignore
IGNORE_PATTERNS = {
    "__pycache__", ".DS_Store", ".git", ".svn",
    "node_modules", ".pytest_cache", ".mypy_cache",
    "*.pyc", "*.pyo", "*.egg-info"
}

server = Server("project-context-mcp")


def get_context_dir() -> Path:
    """Get the .context directory in the current working directory."""
    return Path.cwd() / ".context"


def should_include_file(path: Path) -> bool:
    """Check if a file should be included as a resource."""
    # Skip hidden files
    if path.name.startswith("."):
        return False

    # Skip ignored patterns
    for pattern in IGNORE_PATTERNS:
        if pattern in str(path):
            return False

    # Check extension
    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return False

    return True


def extract_description(path: Path) -> str:
    """Extract a description from the file content."""
    try:
        content = path.read_text(encoding="utf-8")
        lines = content.strip().split("\n")

        for line in lines:
            line = line.strip()
            # Skip markdown headers for description, but use first real content
            if line and not line.startswith("#"):
                # Truncate long lines
                if len(line) > 100:
                    return line[:97] + "..."
                return line

        # If only headers, use the first header
        for line in lines:
            line = line.strip()
            if line.startswith("# "):
                return line[2:]

        return ""
    except Exception:
        return ""


def extract_name(path: Path) -> str:
    """Extract a human-readable name from the file."""
    try:
        content = path.read_text(encoding="utf-8")
        lines = content.strip().split("\n")

        # Look for first H1 in markdown
        if path.suffix.lower() == ".md":
            for line in lines:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:]

        # Fall back to filename without extension
        return path.stem.replace("-", " ").replace("_", " ").title()
    except Exception:
        return path.stem.replace("-", " ").replace("_", " ").title()


def get_mime_type(path: Path) -> str:
    """Get the MIME type for a file."""
    mime_type, _ = mimetypes.guess_type(str(path))
    return mime_type or "text/plain"


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List all files in .context/ as resources."""
    context_dir = get_context_dir()
    resources = []

    if not context_dir.exists():
        logger.info(f"No .context/ directory found in {Path.cwd()}")
        return resources

    if not context_dir.is_dir():
        logger.warning(".context exists but is not a directory")
        return resources

    for path in context_dir.rglob("*"):
        if not path.is_file():
            continue

        if not should_include_file(path):
            continue

        relative_path = path.relative_to(context_dir)
        uri = f"context://{relative_path}"

        resources.append(Resource(
            uri=uri,
            name=extract_name(path),
            description=extract_description(path),
            mimeType=get_mime_type(path)
        ))

    logger.info(f"Found {len(resources)} context resources")
    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read the content of a context resource."""
    # Parse the URI
    if not uri.startswith("context://"):
        raise ValueError(f"Invalid URI scheme: {uri}")

    relative_path = uri.replace("context://", "")
    context_dir = get_context_dir()
    file_path = context_dir / relative_path

    # Security: ensure the path is within .context/
    try:
        file_path.resolve().relative_to(context_dir.resolve())
    except ValueError:
        raise ValueError(f"Path traversal attempt detected: {uri}")

    if not file_path.exists():
        raise FileNotFoundError(f"Resource not found: {uri}")

    if not file_path.is_file():
        raise ValueError(f"Resource is not a file: {uri}")

    content = file_path.read_text(encoding="utf-8")
    return content


async def run_server():
    """Run the MCP server."""
    logger.info("Starting project-context-mcp server")
    logger.info(f"Working directory: {Path.cwd()}")
    logger.info(f"Looking for context in: {get_context_dir()}")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


def main():
    """Entry point."""
    asyncio.run(run_server())


if __name__ == "__main__":
    main()
