#!/bin/bash
# Usage: ./scripts/bump-version.sh 0.2.0

set -e

if [ -z "$1" ]; then
    echo "Usage: $0 <new-version>"
    echo "Example: $0 0.2.0"
    exit 1
fi

NEW_VERSION=$1

# Update pyproject.toml
sed -i.bak "s/^version = \".*\"/version = \"$NEW_VERSION\"/" pyproject.toml && rm pyproject.toml.bak

# Update __init__.py
sed -i.bak "s/__version__ = \".*\"/__version__ = \"$NEW_VERSION\"/" src/project_context_mcp/__init__.py && rm src/project_context_mcp/__init__.py.bak

echo "Version bumped to $NEW_VERSION"
echo ""
echo "Files updated:"
echo "  - pyproject.toml"
echo "  - src/project_context_mcp/__init__.py"
echo ""
echo "Next steps:"
echo "  1. git add -A && git commit -m 'Bump version to $NEW_VERSION'"
echo "  2. Merge to main (GitHub Action will publish to PyPI)"
