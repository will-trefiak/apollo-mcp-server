"""
Deal/Opportunity Tools

Tools for managing deals and opportunities in the Apollo sales pipeline.
"""

from typing import Optional

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT


def register_deal_tools(mcp):
    """Register deal-related tools with the MCP server."""

    @mcp.tool()
    async def deals_list(
        page: int = 1,
        per_page: int = 25,
        stage_id: Optional[str] = None,
    ) -> str:
        """
        List deals/opportunities in your Apollo pipeline.

        Args:
            page: Page number
            per_page: Results per page
            stage_id: Filter by pipeline stage ID

        Returns:
            List of deals
        """
        data = {
            "page": page,
            "per_page": per_page,
            "sort_by_field": "updated_at",
            "sort_ascending": False,
        }

        if stage_id:
            data["stage_id"] = stage_id

        result = await make_request("POST", "/api/v1/opportunities/search", data, use_app_url=True)

        deals = result.get("opportunities", [])
        total = result.get("pagination", {}).get("total_entries", 0)

        output = f"## Deals/Opportunities\n\nFound {total} deals:\n\n"

        for deal in deals:
            name = deal.get("name", "Unknown")
            deal_id = deal.get("id", "")
            amount = deal.get("amount", 0)
            stage = deal.get("stage_name", "N/A")
            account = deal.get("account", {}).get("name", "N/A")

            output += f"### {name}\n"
            output += f"- ID: `{deal_id}`\n"
            output += f"- Amount: ${amount:,.2f}\n"
            output += f"- Stage: {stage}\n"
            output += f"- Account: {account}\n\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def deal_create(
        name: str,
        account_id: str,
        amount: Optional[float] = None,
        stage_id: Optional[str] = None,
        owner_id: Optional[str] = None,
    ) -> str:
        """
        Create a new deal/opportunity.

        Args:
            name: Deal name
            account_id: Account/company ID
            amount: Deal value
            stage_id: Pipeline stage ID
            owner_id: Owner user ID

        Returns:
            Created deal details
        """
        data = {
            "name": name,
            "account_id": account_id,
        }

        if amount is not None:
            data["amount"] = amount
        if stage_id:
            data["stage_id"] = stage_id
        if owner_id:
            data["owner_id"] = owner_id

        result = await make_request("POST", "/api/v1/opportunities", data, use_app_url=True)

        deal = result.get("opportunity", {})
        return f"## Deal Created\n\n- Name: {name}\n- ID: `{deal.get('id')}`\n- Amount: ${amount or 0:,.2f}"
