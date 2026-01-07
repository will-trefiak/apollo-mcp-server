"""
Workflow Automation Tools

Tools for managing workflow automations in Apollo.
"""

from typing import Optional
from datetime import datetime, timedelta

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT


def register_workflow_tools(mcp):
    """Register workflow-related tools with the MCP server."""

    @mcp.tool()
    async def workflows_list(
        page: int = 1,
        per_page: int = 25,
        active_only: bool = False,
    ) -> str:
        """
        List all workflows in your Apollo account.

        Workflows automate actions based on triggers (events or schedules).

        Args:
            page: Page number
            per_page: Results per page
            active_only: Only show active workflows

        Returns:
            List of workflows with their status and configuration
        """
        data = {
            "page": page,
            "per_page": per_page,
            "sort_by_field": "updated_at",
            "sort_ascending": False,
        }

        if active_only:
            data["active"] = True

        result = await make_request("POST", "/api/v1/rule_configs/search", data, use_app_url=True)

        workflows = result.get("rule_configs", [])
        total = result.get("pagination", {}).get("total_entries", 0)

        output = f"## Workflows\n\nFound {total} workflows:\n\n"

        for wf in workflows:
            name = wf.get("name", "Unknown")
            wf_id = wf.get("id", "")
            active = "Active" if wf.get("active") else "Inactive"
            trigger_type = wf.get("trigger_type", "N/A")

            output += f"### {name}\n"
            output += f"- ID: `{wf_id}`\n"
            output += f"- Status: {active}\n"
            output += f"- Trigger: {trigger_type}\n\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def workflow_get(workflow_id: str) -> str:
        """
        Get detailed information about a specific workflow.

        Args:
            workflow_id: The workflow ID

        Returns:
            Workflow details including triggers, actions, and enrollment criteria
        """
        result = await make_request(
            "GET",
            f"/api/v1/rule_configs/{workflow_id}",
            use_app_url=True
        )

        wf = result.get("rule_config", {})

        output = f"## Workflow: {wf.get('name', 'Unknown')}\n\n"
        output += f"- ID: `{wf.get('id')}`\n"
        output += f"- Status: {'Active' if wf.get('active') else 'Inactive'}\n"
        output += f"- Trigger Type: {wf.get('trigger_type', 'N/A')}\n"
        output += f"- Target Type: {wf.get('target_type', 'N/A')}\n"
        output += f"- Created: {wf.get('created_at')}\n"
        output += f"- Updated: {wf.get('updated_at')}\n\n"

        # Show trigger events
        workflow_triggers = wf.get("workflow_triggers", [])
        if workflow_triggers:
            output += "### Trigger Events:\n"
            for trigger in workflow_triggers:
                trigger_type = trigger.get("trigger_type", "unknown")
                output += f"- {trigger_type}\n"
            output += "\n"

        # Show actions
        actions = wf.get("actions", [])
        if actions:
            output += "### Actions:\n"
            for action in actions:
                action_type = action.get("type", "unknown")
                output += f"- {action_type}\n"
            output += "\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def workflow_create(
        name: str,
        trigger_type: str = "event",
        model_type: str = "Contact",
        trigger_events: Optional[list[str]] = None,
        actions: Optional[list[dict]] = None,
        enrollment_filters: Optional[dict] = None,
        active: bool = False,
        first_run_on: Optional[str] = None,
    ) -> str:
        """
        Create a new workflow automation.

        Workflows trigger actions based on events or schedules.

        Args:
            name: Workflow name
            trigger_type: "event" or "schedule" (default: "event")
            model_type: "Contact", "Account", or "Opportunity" (default: "Contact")
            trigger_events: List of trigger events (for event-based workflows):
                - "contact_saved_or_created" - When a contact is saved/created
                - "contact_updated" - When contact fields change
                - "contact_added_to_list" - When added to a list
                - "contact_added_to_sequence" - When added to a sequence
                - "contact_finished_sequence" - When sequence completes
                - "contact_changed_jobs" - When job change detected
                - "call_logged" - When a call is logged
            actions: List of actions to perform. Each action has:
                - type: "add_to_sequence", "add_to_list", "update_field",
                       "create_task", "send_webhook", "remove_from_sequence"
                - config: Action-specific configuration
            enrollment_filters: Filters to determine which contacts qualify
            active: Whether to activate immediately
            first_run_on: Date for first run (ISO format, e.g., "2026-01-08").
                         Required for schedule-based workflows.

        Returns:
            Created workflow details

        Example:
            workflow_create(
                name="New Lead Nurture",
                trigger_type="event",
                trigger_events=["contact_saved_or_created"],
                actions=[
                    {"type": "add_to_sequence", "config": {"sequence_id": "abc123"}}
                ]
            )
        """
        data = {
            "name": name,
            "trigger_type": trigger_type,
            "model_type": model_type,
            "active": active,
        }

        # Set first_run_on (required by API)
        if first_run_on:
            data["first_run_on"] = first_run_on
        else:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            data["first_run_on"] = tomorrow

        if trigger_events:
            data["workflow_triggers"] = [
                {"trigger_type": event} for event in trigger_events
            ]
        if actions:
            data["actions"] = actions
        if enrollment_filters:
            data["filters"] = enrollment_filters

        result = await make_request("POST", "/api/v1/rule_configs", data, use_app_url=True)

        wf = result.get("rule_config", {})
        return f"## Workflow Created\n\n- Name: {name}\n- ID: `{wf.get('id')}`\n- Status: {'Active' if active else 'Inactive (use workflow_activate to enable)'}"

    @mcp.tool()
    async def workflow_update(
        workflow_id: str,
        name: Optional[str] = None,
        trigger_events: Optional[list[str]] = None,
        actions: Optional[list[dict]] = None,
        enrollment_filters: Optional[dict] = None,
        active: Optional[bool] = None,
    ) -> str:
        """
        Update an existing workflow.

        Args:
            workflow_id: The workflow ID to update
            name: New workflow name
            trigger_events: Updated trigger events
            actions: Updated actions
            enrollment_filters: Updated enrollment filters
            active: Set active/inactive status

        Returns:
            Updated workflow details
        """
        data = {}

        if name:
            data["name"] = name
        if trigger_events:
            data["workflow_triggers"] = [
                {"trigger_type": event} for event in trigger_events
            ]
        if actions:
            data["actions"] = actions
        if enrollment_filters:
            data["enrollment_filters"] = enrollment_filters
        if active is not None:
            data["active"] = active

        result = await make_request(
            "PUT",
            f"/api/v1/rule_configs/{workflow_id}",
            data,
            use_app_url=True
        )

        wf = result.get("rule_config", {})
        return f"## Workflow Updated\n\n- Name: {wf.get('name')}\n- ID: `{workflow_id}`\n- Status: {'Active' if wf.get('active') else 'Inactive'}"

    @mcp.tool()
    async def workflow_activate(workflow_id: str, active: bool = True) -> str:
        """
        Activate or deactivate a workflow.

        Note: Activation may require the workflow to have actions configured.
        If activation fails, configure actions via Apollo UI first.

        Args:
            workflow_id: The workflow ID
            active: True to activate, False to deactivate

        Returns:
            Updated workflow status
        """
        data = {"active": active}

        if active:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            data["first_run_on"] = tomorrow

        result = await make_request(
            "PUT",
            f"/api/v1/rule_configs/{workflow_id}",
            data,
            use_app_url=True
        )

        wf = result.get("rule_config", {})
        status = "activated" if active else "deactivated"
        return f"## Workflow {status.title()}\n\nWorkflow `{wf.get('name')}` has been {status}."

    @mcp.tool()
    async def workflow_delete(workflow_id: str) -> str:
        """
        Delete a workflow.

        Args:
            workflow_id: The workflow ID to delete

        Returns:
            Confirmation of deletion
        """
        await make_request(
            "DELETE",
            f"/api/v1/rule_configs/{workflow_id}",
            use_app_url=True
        )

        return f"## Workflow Deleted\n\nWorkflow `{workflow_id}` has been deleted."

    @mcp.tool()
    async def workflow_templates_list(page: int = 1, per_page: int = 25) -> str:
        """
        List available workflow templates.

        Templates provide pre-built workflows for common automation scenarios.

        Args:
            page: Page number
            per_page: Results per page

        Returns:
            List of workflow templates
        """
        data = {"page": page, "per_page": per_page}

        result = await make_request("POST", "/api/v1/unified_templates/search", data, use_app_url=True)

        templates = result.get("unified_templates", [])

        output = "## Workflow Templates\n\n"

        for tpl in templates:
            name = tpl.get("name", "Unknown")
            tpl_id = tpl.get("id", "")
            description = tpl.get("description", "N/A")

            output += f"### {name}\n"
            output += f"- ID: `{tpl_id}`\n"
            output += f"- Description: {description}\n\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def workflow_create_from_template(
        template_id: str,
        name: Optional[str] = None,
    ) -> str:
        """
        Create a new workflow from a template.

        Args:
            template_id: The template ID to use
            name: Optional custom name for the workflow

        Returns:
            Created workflow details
        """
        data = {"template_id": template_id}

        if name:
            data["name"] = name

        result = await make_request("POST", "/api/v1/rule_configs/create_from_template", data, use_app_url=True)

        wf = result.get("rule_config", {})
        return f"## Workflow Created from Template\n\n- Name: {wf.get('name')}\n- ID: `{wf.get('id')}`\n- Status: Inactive (use workflow_activate to enable)"
