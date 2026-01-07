"""
Analytics and Reporting Tools

Tools for accessing analytics and reporting data in Apollo.
"""

from typing import Optional

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT


def register_analytics_tools(mcp):
    """Register analytics-related tools with the MCP server."""

    @mcp.tool()
    async def analytics_sequences(
        sequence_ids: Optional[list[str]] = None,
    ) -> str:
        """
        Get analytics for email sequences.

        Args:
            sequence_ids: Optional list of sequence IDs to get stats for

        Returns:
            Sequence performance analytics
        """
        data = {
            "page": 1,
            "per_page": 25,
            "sort_by_field": "lastUsedAt",
            "sort_ascending": False,
            "display_mode": "explorer_mode",
        }

        if sequence_ids:
            data["ids"] = sequence_ids

        result = await make_request("POST", "/api/v1/emailer_campaigns/search", data, use_app_url=True)

        sequences = result.get("emailer_campaigns", [])

        output = "## Sequence Analytics\n\n"

        for seq in sequences:
            name = seq.get("name", "Unknown")
            seq_id = seq.get("id", "")

            # Performance metrics
            delivered = seq.get("unique_delivered", 0)
            opened = seq.get("unique_opened", 0)
            replied = seq.get("unique_replied", 0)
            bounced = seq.get("unique_bounced", 0)

            open_rate = seq.get("open_rate", 0) * 100
            reply_rate = seq.get("reply_rate", 0) * 100
            bounce_rate = seq.get("bounce_rate", 0) * 100

            output += f"### {name}\n"
            output += f"- ID: `{seq_id}`\n"
            output += f"- Delivered: {delivered}\n"
            output += f"- Opened: {opened} ({open_rate:.1f}%)\n"
            output += f"- Replied: {replied} ({reply_rate:.1f}%)\n"
            output += f"- Bounced: {bounced} ({bounce_rate:.1f}%)\n\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def analytics_email_accounts() -> str:
        """
        Get email account health and deliverability stats.

        Returns:
            Email account analytics including deliverability scores
        """
        result = await make_request("GET", "/api/v1/email_accounts", use_app_url=True)

        accounts = result.get("email_accounts", [])

        output = "## Email Account Analytics\n\n"

        for account in accounts:
            email = account.get("email", "Unknown")
            account_id = account.get("id", "")
            active = "Active" if account.get("active") else "Inactive"

            # Health metrics
            reputation_score = account.get("reputation_score", "N/A")
            daily_limit = account.get("daily_email_limit", "N/A")
            emails_sent_today = account.get("emails_sent_today", 0)

            output += f"### {email}\n"
            output += f"- ID: `{account_id}`\n"
            output += f"- Status: {active}\n"
            output += f"- Reputation Score: {reputation_score}\n"
            output += f"- Daily Limit: {daily_limit}\n"
            output += f"- Sent Today: {emails_sent_today}\n\n"

        return output[:CHARACTER_LIMIT]
