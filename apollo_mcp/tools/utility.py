"""
Utility Tools

Helper tools for getting configuration data from Apollo.
"""

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT


def register_utility_tools(mcp):
    """Register utility tools with the MCP server."""

    @mcp.tool()
    async def get_available_fields() -> str:
        """
        Get all available fields/variables for email personalization.

        Returns:
            List of available variables that can be used in emails
        """
        # Return static list of known Apollo personalization variables
        output = """## Available Email Personalization Fields

### Contact Fields
- `{{first_name}}` - Contact's first name
- `{{last_name}}` - Contact's last name
- `{{name}}` - Contact's full name
- `{{email}}` - Contact's email address
- `{{phone}}` - Contact's phone number
- `{{title}}` - Contact's job title
- `{{city}}` - Contact's city
- `{{state}}` - Contact's state/region
- `{{country}}` - Contact's country

### Company Fields
- `{{company}}` - Company name
- `{{company_domain}}` - Company website domain
- `{{company_phone}}` - Company phone number
- `{{industry}}` - Company industry
- `{{company_city}}` - Company headquarters city
- `{{company_state}}` - Company headquarters state
- `{{company_country}}` - Company headquarters country

### Sender Fields
- `{{sender_first_name}}` - Your first name
- `{{sender_last_name}}` - Your last name
- `{{sender_email}}` - Your email address
- `{{sender_phone}}` - Your phone number
- `{{sender_title}}` - Your job title
- `{{sender_company}}` - Your company name

### Custom Fields
Custom fields can be referenced using: `{{custom_field_name}}`
"""
        return output

    @mcp.tool()
    async def get_email_schedules() -> str:
        """
        Get available email sending schedules.

        Returns:
            List of sending schedules with their configurations
        """
        result = await make_request("GET", "/api/v1/emailer_schedules", use_app_url=True)

        schedules = result.get("emailer_schedules", [])

        output = "## Email Sending Schedules\n\n"

        for schedule in schedules:
            name = schedule.get("name", "Unknown")
            schedule_id = schedule.get("id", "")
            timezone = schedule.get("timezone", "N/A")

            output += f"### {name}\n"
            output += f"- ID: `{schedule_id}`\n"
            output += f"- Timezone: {timezone}\n\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def get_contact_stages() -> str:
        """
        Get available contact stages for pipeline management.

        Returns:
            List of contact stages
        """
        result = await make_request("GET", "/api/v1/contact_stages", use_app_url=True)

        stages = result.get("contact_stages", [])

        output = "## Contact Stages\n\n"

        for stage in stages:
            name = stage.get("name", "Unknown")
            stage_id = stage.get("id", "")
            order = stage.get("order", 0)

            output += f"- **{name}** (ID: `{stage_id}`, Order: {order})\n"

        return output

    @mcp.tool()
    async def get_account_stages() -> str:
        """
        Get available account/company stages.

        Returns:
            List of account stages
        """
        result = await make_request("GET", "/api/v1/account_stages", use_app_url=True)

        stages = result.get("account_stages", [])

        output = "## Account Stages\n\n"

        for stage in stages:
            name = stage.get("name", "Unknown")
            stage_id = stage.get("id", "")
            order = stage.get("order", 0)

            output += f"- **{name}** (ID: `{stage_id}`, Order: {order})\n"

        return output
