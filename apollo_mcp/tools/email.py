"""
Email Tools

Tools for email preview and sending in Apollo.
"""

from typing import Optional

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT


def register_email_tools(mcp):
    """Register email-related tools with the MCP server."""

    @mcp.tool()
    async def email_preview(
        subject: str,
        body_html: str,
        contact_id: Optional[str] = None,
    ) -> str:
        """
        Preview an email with variable substitution.

        Test how your email will look with real contact data.

        Args:
            subject: Email subject (can include {{variables}})
            body_html: Email body HTML (can include {{variables}})
            contact_id: Optional contact ID to preview with real data

        Returns:
            Rendered email preview
        """
        data = {
            "subject": subject,
            "body_html": body_html,
            "type": "new_thread",
            "include_signature": True,
            "force_parallel_enrichment": True,
        }

        if contact_id:
            data["contact_id"] = contact_id

        result = await make_request("POST", "/api/v1/emailer_previews/preview", data, use_app_url=True)

        msg = result.get("emailer_message", {})

        output = "## Email Preview\n\n"
        output += f"**To:** {msg.get('to_name', 'N/A')} <{msg.get('to_email', 'N/A')}>\n"
        output += f"**From:** {msg.get('from_name', 'N/A')} <{msg.get('from_email', 'N/A')}>\n"
        output += f"**Subject:** {msg.get('subject', 'N/A')}\n\n"
        output += "---\n\n"
        output += msg.get("body_text", "")

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def email_send(
        to_email: str,
        subject: str,
        body_html: str,
        contact_id: Optional[str] = None,
    ) -> str:
        """
        Send a one-off email to a contact.

        Args:
            to_email: Recipient email address
            subject: Email subject
            body_html: Email body HTML
            contact_id: Optional contact ID to link email to

        Returns:
            Confirmation of email sent
        """
        data = {
            "to_email": to_email,
            "subject": subject,
            "body_html": body_html,
        }

        if contact_id:
            data["contact_id"] = contact_id

        await make_request("POST", "/api/v1/emails/send", data, use_app_url=True)

        return f"## Email Sent\n\nEmail successfully sent to {to_email}"
