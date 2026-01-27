#!/bin/bash
# Activate the MCP server virtual environment

source /Users/wergilius/Documents/My_MCPs/.venv/bin/activate

echo "✓ Virtual environment activated"
echo "✓ Python version: $(python --version)"
echo ""
echo "You can now run the MCP server with:"
echo "  python paper_search/mcp_server.py"
