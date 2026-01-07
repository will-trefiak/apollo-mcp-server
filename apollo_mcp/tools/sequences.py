"""
Email Sequence Tools

Tools for managing email sequences/campaigns in Apollo.
"""

from typing import Optional

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT


def register_sequence_tools(mcp):
    """Register sequence-related tools with the MCP server."""

    @mcp.tool()
    async def sequences_list(
        page: int = 1,
        per_page: int = 25,
        sort_by: str = "lastUsedAt",
    ) -> str:
        """
        List all email sequences in your Apollo account.

        Args:
            page: Page number
            per_page: Results per page
            sort_by: Sort field (lastUsedAt, name, created_at)

        Returns:
            List of sequences with stats
        """
        data = {
            "page": page,
            "per_page": per_page,
            "sort_by_field": sort_by,
            "sort_ascending": False,
            "display_mode": "explorer_mode",
        }

        result = await make_request("POST", "/api/v1/emailer_campaigns/search", data, use_app_url=True)

        sequences = result.get("emailer_campaigns", [])
        total = result.get("pagination", {}).get("total_entries", 0)

        output = f"## Email Sequences\n\nFound {total} sequences:\n\n"

        for seq in sequences:
            name = seq.get("name", "Unknown")
            active = "Active" if seq.get("active") else "Inactive"
            steps = seq.get("num_steps", 0)
            delivered = seq.get("unique_delivered", 0)
            reply_rate = seq.get("reply_rate", 0) * 100
            seq_id = seq.get("id", "")

            output += f"### {name}\n"
            output += f"- ID: `{seq_id}`\n"
            output += f"- Status: {active}\n"
            output += f"- Steps: {steps}\n"
            output += f"- Delivered: {delivered}\n"
            output += f"- Reply Rate: {reply_rate:.1f}%\n\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def sequence_get(sequence_id: str) -> str:
        """
        Get detailed information about a specific sequence.

        Args:
            sequence_id: The sequence ID

        Returns:
            Sequence details including steps and stats
        """
        result = await make_request(
            "GET",
            f"/api/v1/emailer_campaigns/{sequence_id}",
            use_app_url=True
        )

        seq = result.get("emailer_campaign", {})
        steps = result.get("emailer_steps", [])

        output = f"## Sequence: {seq.get('name', 'Unknown')}\n\n"
        output += f"- ID: `{seq.get('id')}`\n"
        output += f"- Status: {'Active' if seq.get('active') else 'Inactive'}\n"
        output += f"- Created: {seq.get('created_at')}\n"
        output += f"- Reply Rate: {seq.get('reply_rate', 0) * 100:.1f}%\n"
        output += f"- Open Rate: {seq.get('open_rate', 0) * 100:.1f}%\n\n"

        output += "### Steps:\n\n"
        for i, step in enumerate(steps, 1):
            step_type = step.get("type", "unknown")
            wait_time = step.get("wait_time", 0)
            wait_mode = step.get("wait_mode", "day")
            output += f"**Step {i}**: {step_type} (wait {wait_time} {wait_mode}s)\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def sequence_create(
        name: str,
        steps: list[dict],
        schedule_id: Optional[str] = None,
        active: bool = False,
    ) -> str:
        """
        Create a new email sequence with steps.

        This is a powerful tool for creating automated outreach campaigns.

        Args:
            name: Sequence name
            steps: List of step configurations. Each step should have:
                - type: "auto_email", "manual_email", "phone_call", "action_item",
                        "linkedin_connection", "linkedin_message", "linkedin_view", "linkedin_interact"
                - wait_time: Time to wait before this step (integer)
                - wait_mode: "minute", "hour", or "day"
                - For email steps, include emailer_touches with:
                    - type: "new_thread" or "reply"
                    - subject: Email subject (supports {{variables}})
                    - body_html: Email body HTML (supports {{variables}})
            schedule_id: Optional sending schedule ID
            active: Whether to activate immediately

        Returns:
            Created sequence details

        Example:
            sequence_create(
                name="New Outreach Campaign",
                steps=[
                    {
                        "type": "auto_email",
                        "wait_time": 0,
                        "wait_mode": "minute",
                        "emailer_touches": [{
                            "type": "new_thread",
                            "subject": "Quick question about {{company}}",
                            "body_html": "<p>Hi {{first_name}},</p><p>I noticed {{company}} is growing...</p>"
                        }]
                    },
                    {
                        "type": "auto_email",
                        "wait_time": 3,
                        "wait_mode": "day",
                        "emailer_touches": [{
                            "type": "reply",
                            "subject": "Re: Quick question about {{company}}",
                            "body_html": "<p>Following up on my last email...</p>"
                        }]
                    }
                ]
            )

        Available variables: {{first_name}}, {{last_name}}, {{company}}, {{title}},
                            {{email}}, {{phone}}, {{city}}, {{state}}, {{country}}
        """
        # First create the sequence
        create_data = {
            "name": name,
            "creation_type": "new",
        }

        result = await make_request("POST", "/api/v1/emailer_campaigns", create_data, use_app_url=True)
        sequence_id = result.get("emailer_campaign", {}).get("id")

        if not sequence_id:
            return "Error: Failed to create sequence"

        # Format steps for update
        formatted_steps = []
        for i, step in enumerate(steps, 1):
            formatted_step = {
                "type": step.get("type", "auto_email"),
                "wait_time": step.get("wait_time", 0),
                "wait_mode": step.get("wait_mode", "day"),
                "priority": step.get("priority", "medium"),
                "position": i,
                "emailer_touches": [],
            }

            # Format email touches
            for touch in step.get("emailer_touches", []):
                formatted_touch = {
                    "type": touch.get("type", "new_thread"),
                    "status": "active",
                    "include_signature": True,
                    "template_type": "emailer_template",
                    "emailer_template": {
                        "subject": touch.get("subject", ""),
                        "body_html": touch.get("body_html", ""),
                    },
                }
                formatted_step["emailer_touches"].append(formatted_touch)

            formatted_steps.append(formatted_step)

        # Update sequence with steps
        update_data = {
            "name": name,
            "active": active,
            "emailer_steps": formatted_steps,
        }

        if schedule_id:
            update_data["emailer_schedule_id"] = schedule_id

        await make_request(
            "PUT",
            f"/api/v1/sequences/{sequence_id}",
            update_data,
            use_app_url=True
        )

        return f"## Sequence Created Successfully!\n\n- Name: {name}\n- ID: `{sequence_id}`\n- Steps: {len(steps)}\n- Status: {'Active' if active else 'Inactive'}\n\nUse `sequence_add_contacts` to add contacts to this sequence."

    @mcp.tool()
    async def sequence_add_contacts(
        sequence_id: str,
        contact_ids: list[str],
        email_account_id: Optional[str] = None,
    ) -> str:
        """
        Add contacts to an email sequence.

        Args:
            sequence_id: The sequence ID to add contacts to
            contact_ids: List of contact IDs to add
            email_account_id: Optional email account to send from

        Returns:
            Confirmation of contacts added
        """
        data = {
            "contact_ids": contact_ids,
            "emailer_campaign_id": sequence_id,
        }

        if email_account_id:
            data["email_account_id"] = email_account_id

        result = await make_request(
            "POST",
            "/api/v1/emailer_campaign_contacts/bulk_create",
            data,
            use_app_url=True
        )

        added = result.get("emailer_campaign_contacts", [])
        return f"## Contacts Added to Sequence\n\nSuccessfully added {len(added)} contacts to sequence `{sequence_id}`"

    @mcp.tool()
    async def sequence_activate(
        sequence_id: str,
        active: bool = True,
    ) -> str:
        """
        Activate or deactivate a sequence.

        Args:
            sequence_id: The sequence ID
            active: True to activate, False to deactivate

        Returns:
            Updated sequence status
        """
        data = {"active": active}

        result = await make_request(
            "PUT",
            f"/api/v1/sequences/{sequence_id}",
            data,
            use_app_url=True
        )

        seq = result.get("emailer_campaign", {})
        status = "activated" if active else "deactivated"
        return f"## Sequence {status.title()}\n\nSequence `{seq.get('name')}` has been {status}."
