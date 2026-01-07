"""
Apollo MCP Tools

This module contains all the MCP tools organized by category:
- people: People/contact search and enrichment
- organizations: Company search and enrichment
- sequences: Email sequence management
- lists: Contact list management
- workflows: Workflow automation
- email: Email preview and sending
- tasks: Task management
- deals: Deal/opportunity management
- analytics: Reporting and analytics
"""

from apollo_mcp.tools.people import register_people_tools
from apollo_mcp.tools.organizations import register_organization_tools
from apollo_mcp.tools.sequences import register_sequence_tools
from apollo_mcp.tools.lists import register_list_tools
from apollo_mcp.tools.workflows import register_workflow_tools
from apollo_mcp.tools.email import register_email_tools
from apollo_mcp.tools.tasks import register_task_tools
from apollo_mcp.tools.deals import register_deal_tools
from apollo_mcp.tools.analytics import register_analytics_tools
from apollo_mcp.tools.utility import register_utility_tools


def register_all_tools(mcp):
    """
    Register all Apollo tools with the MCP server.

    Args:
        mcp: FastMCP server instance
    """
    register_people_tools(mcp)
    register_organization_tools(mcp)
    register_sequence_tools(mcp)
    register_list_tools(mcp)
    register_workflow_tools(mcp)
    register_email_tools(mcp)
    register_task_tools(mcp)
    register_deal_tools(mcp)
    register_analytics_tools(mcp)
    register_utility_tools(mcp)


__all__ = ["register_all_tools"]
