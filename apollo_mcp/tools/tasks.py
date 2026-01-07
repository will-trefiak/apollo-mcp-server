"""
Task Management Tools

Tools for managing tasks and activities in Apollo.
"""

from typing import Optional

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT


def register_task_tools(mcp):
    """Register task-related tools with the MCP server."""

    @mcp.tool()
    async def tasks_list(
        page: int = 1,
        per_page: int = 25,
        status: Optional[str] = None,
    ) -> str:
        """
        List tasks in your Apollo account.

        Args:
            page: Page number
            per_page: Results per page
            status: Filter by status (pending, completed)

        Returns:
            List of tasks
        """
        data = {
            "page": page,
            "per_page": per_page,
            "display_mode": "explorer_mode",
        }

        if status:
            data["status"] = status

        result = await make_request("POST", "/api/v1/tasks/search", data, use_app_url=True)

        tasks = result.get("tasks", [])
        total = result.get("pagination", {}).get("total_entries", 0)

        output = f"## Tasks\n\nFound {total} tasks:\n\n"

        for task in tasks:
            task_type = task.get("type", "unknown")
            priority = task.get("priority", "medium")
            due = task.get("due_at", "N/A")
            contact = task.get("contact", {}).get("name", "N/A")

            output += f"- **{task_type}** (Priority: {priority})\n"
            output += f"  Contact: {contact}, Due: {due}\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def task_create(
        contact_id: str,
        task_type: str = "action_item",
        note: Optional[str] = None,
        due_at: Optional[str] = None,
        priority: str = "medium",
    ) -> str:
        """
        Create a new task.

        Args:
            contact_id: Contact ID to associate task with
            task_type: Type of task (action_item, call, email, linkedin)
            note: Task notes/description
            due_at: Due date (ISO format)
            priority: Priority level (low, medium, high)

        Returns:
            Created task details
        """
        data = {
            "contact_id": contact_id,
            "type": task_type,
            "priority": priority,
        }

        if note:
            data["note"] = note
        if due_at:
            data["due_at"] = due_at

        result = await make_request("POST", "/api/v1/tasks", data, use_app_url=True)

        task = result.get("task", {})
        return f"## Task Created\n\n- ID: `{task.get('id')}`\n- Type: {task_type}\n- Priority: {priority}"
