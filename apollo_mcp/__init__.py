"""
Apollo MCP Server - Model Context Protocol server for Apollo.io

A comprehensive MCP server providing 34+ tools for Apollo.io sales automation:
- People/Contact Search & Enrichment
- Organization/Account Search & Enrichment
- Email Sequences with A/B Testing
- Contact Management & Lists
- Workflow Automation
- Tasks, Deals & Analytics

For usage instructions, see: https://github.com/yourusername/apollo-mcp-server
"""

__version__ = "1.0.0"
__author__ = "Apollo MCP Contributors"

def create_server():
    """Create and configure the Apollo MCP server."""
    from apollo_mcp.server import create_server as _create_server
    return _create_server()


def run_server():
    """Run the Apollo MCP server."""
    from apollo_mcp.server import run_server as _run_server
    _run_server()


__all__ = ["create_server", "run_server", "__version__"]
