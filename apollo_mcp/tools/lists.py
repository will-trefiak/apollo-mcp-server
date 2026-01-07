"""
List Management Tools

Tools for managing contact lists in Apollo.
"""

from apollo_mcp.client import make_request


def register_list_tools(mcp):
    """Register list-related tools with the MCP server."""

    @mcp.tool()
    async def lists_get(page: int = 1, per_page: int = 25) -> str:
        """
        Get all saved lists in Apollo.

        Args:
            page: Page number
            per_page: Results per page

        Returns:
            List of saved lists
        """
        data = {"page": page, "per_page": per_page}

        result = await make_request("POST", "/api/v1/labels/search", data, use_app_url=True)

        lists = result.get("labels", [])

        output = "## Saved Lists\n\n"

        for lst in lists:
            name = lst.get("name", "Unknown")
            list_id = lst.get("id", "")
            count = lst.get("cached_count", 0)
            output += f"- **{name}** (ID: `{list_id}`) - {count} contacts\n"

        return output

    @mcp.tool()
    async def list_create(name: str, modality: str = "contacts") -> str:
        """
        Create a new list.

        Args:
            name: List name
            modality: List type - "contacts" (default), "people", or "static"

        Returns:
            Created list details
        """
        data = {"name": name, "modality": modality}

        result = await make_request("POST", "/api/v1/labels", data, use_app_url=True)

        lst = result.get("label", {})
        return f"## List Created\n\n- Name: {name}\n- ID: `{lst.get('id')}`\n- Type: {modality}"

    @mcp.tool()
    async def list_add_contacts(list_id: str, contact_ids: list[str]) -> str:
        """
        Add contacts to a list.

        Args:
            list_id: List ID
            contact_ids: Contact IDs to add

        Returns:
            Confirmation
        """
        data = {"label_id": list_id, "contact_ids": contact_ids}

        await make_request("POST", "/api/v1/labels/add_contacts", data, use_app_url=True)

        return f"## Contacts Added\n\nAdded {len(contact_ids)} contacts to list `{list_id}`"
