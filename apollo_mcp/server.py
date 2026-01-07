"""
Apollo MCP Server

Main entry point for the Apollo.io MCP server.
Provides 34 tools for sales outreach automation including:
- People/contact search and enrichment
- Organization/company search and enrichment
- Email sequences and campaigns
- Contact list management
- Workflow automation
- Email preview and sending
- Task management
- Deal/opportunity pipeline
- Analytics and reporting
"""

from mcp.server.fastmcp import FastMCP

from apollo_mcp.tools import register_all_tools


def create_server() -> FastMCP:
    """
    Create and configure the Apollo MCP server.

    Returns:
        Configured FastMCP server instance with all Apollo tools registered.
    """
    mcp = FastMCP("Apollo MCP Server")

    # Register all Apollo tools
    register_all_tools(mcp)

    return mcp


def run_server():
    """Run the Apollo MCP server."""
    mcp = create_server()
    mcp.run()


# Lazy-loaded server instance
_mcp = None


def get_server() -> FastMCP:
    """Get or create the Apollo MCP server instance."""
    global _mcp
    if _mcp is None:
        _mcp = create_server()
    return _mcp


# For direct module execution
if __name__ == "__main__":
    run_server()
