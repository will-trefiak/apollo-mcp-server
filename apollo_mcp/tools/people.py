"""
People/Contact Tools

Tools for searching and enriching people/contact data in Apollo.
"""

from typing import Optional

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT
from apollo_mcp.utils.formatting import format_person, truncate_response


def register_people_tools(mcp):
    """Register people-related tools with the MCP server."""

    @mcp.tool()
    async def people_search(
        q_keywords: Optional[str] = None,
        person_titles: Optional[list[str]] = None,
        person_seniorities: Optional[list[str]] = None,
        organization_domains: Optional[list[str]] = None,
        organization_locations: Optional[list[str]] = None,
        organization_num_employees_ranges: Optional[list[str]] = None,
        person_locations: Optional[list[str]] = None,
        contact_email_status: Optional[list[str]] = None,
        page: int = 1,
        per_page: int = 25,
    ) -> str:
        """
        Search for people/contacts in Apollo's database.

        This is Apollo's core prospecting tool - use it to find leads matching specific criteria.

        Args:
            q_keywords: Keywords to search for (e.g., "sales director")
            person_titles: Job titles to filter by (e.g., ["CEO", "CTO", "VP Sales"])
            person_seniorities: Seniority levels (e.g., ["c_suite", "vp", "director", "manager"])
            organization_domains: Company domains to search (e.g., ["google.com", "meta.com"])
            organization_locations: Company HQ locations (e.g., ["California, US", "New York, US"])
            organization_num_employees_ranges: Employee count ranges (e.g., ["1,10", "11,50", "51,200"])
            person_locations: Where person is located (e.g., ["San Francisco, CA"])
            contact_email_status: Email verification status (e.g., ["verified", "likely_to_engage"])
            page: Page number (default 1)
            per_page: Results per page (default 25, max 100)

        Returns:
            List of matching people with contact information

        Example:
            Search for VPs of Sales at tech companies in California:
            people_search(
                person_titles=["VP Sales", "Vice President of Sales"],
                organization_locations=["California, US"],
                organization_num_employees_ranges=["51,200", "201,500"]
            )
        """
        data = {
            "page": page,
            "per_page": min(per_page, 100),
        }

        if q_keywords:
            data["q_keywords"] = q_keywords
        if person_titles:
            data["person_titles"] = person_titles
        if person_seniorities:
            data["person_seniorities"] = person_seniorities
        if organization_domains:
            data["organization_domains"] = organization_domains
        if organization_locations:
            data["organization_locations"] = organization_locations
        if organization_num_employees_ranges:
            data["organization_num_employees_ranges"] = organization_num_employees_ranges
        if person_locations:
            data["person_locations"] = person_locations
        if contact_email_status:
            data["contact_email_status"] = contact_email_status

        result = await make_request("POST", "/v1/mixed_people/api_search", data)

        people = result.get("people", [])
        total = result.get("pagination", {}).get("total_entries", 0)

        output = f"## People Search Results\n\nFound {total} total matches (showing page {page}):\n\n"

        for person in people[:per_page]:
            output += format_person(person)
            output += "---\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def people_enrich(
        email: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        organization_name: Optional[str] = None,
        domain: Optional[str] = None,
        linkedin_url: Optional[str] = None,
    ) -> str:
        """
        Enrich a person's profile with additional data from Apollo.

        Provide at least one identifier (email, LinkedIn URL, or name + company).
        Apollo will return comprehensive profile data including contact info,
        work history, and social profiles.

        Args:
            email: Person's email address (best identifier)
            first_name: Person's first name
            last_name: Person's last name
            organization_name: Current company name
            domain: Company domain (e.g., "google.com")
            linkedin_url: LinkedIn profile URL

        Returns:
            Enriched person profile with all available data

        Example:
            Enrich by email:
            people_enrich(email="john.smith@company.com")

            Enrich by name + company:
            people_enrich(first_name="John", last_name="Smith", organization_name="Acme Corp")
        """
        data = {}

        if email:
            data["email"] = email
        if first_name:
            data["first_name"] = first_name
        if last_name:
            data["last_name"] = last_name
        if organization_name:
            data["organization_name"] = organization_name
        if domain:
            data["domain"] = domain
        if linkedin_url:
            data["linkedin_url"] = linkedin_url

        if not data:
            return "Error: Please provide at least one identifier (email, LinkedIn URL, or name + company)"

        result = await make_request("POST", "/v1/people/match", data)

        person = result.get("person", {})
        if not person:
            return "No matching person found. Try with different identifiers."

        return f"## Person Enrichment Results\n\n{format_person(person)}\n\nFull Data:\n{truncate_response(person)}"

    @mcp.tool()
    async def contacts_search(
        q_keywords: Optional[str] = None,
        contact_stage_ids: Optional[list[str]] = None,
        owner_id: Optional[str] = None,
        emailer_campaign_ids: Optional[list[str]] = None,
        page: int = 1,
        per_page: int = 25,
    ) -> str:
        """
        Search contacts in your Apollo CRM/database.

        Unlike people_search which searches Apollo's global database, this searches
        contacts you've already added to your Apollo account.

        Args:
            q_keywords: Search keywords
            contact_stage_ids: Filter by contact stage IDs
            owner_id: Filter by owner user ID
            emailer_campaign_ids: Filter by sequence IDs
            page: Page number
            per_page: Results per page

        Returns:
            List of contacts from your Apollo database
        """
        data = {
            "page": page,
            "per_page": per_page,
            "display_mode": "explorer_mode",
        }

        if q_keywords:
            data["q_keywords"] = q_keywords
        if contact_stage_ids:
            data["contact_stage_ids"] = contact_stage_ids
        if owner_id:
            data["owner_id"] = owner_id
        if emailer_campaign_ids:
            data["emailer_campaign_ids"] = emailer_campaign_ids

        result = await make_request("POST", "/api/v1/contacts/search", data, use_app_url=True)

        contacts = result.get("contacts", [])
        total = result.get("pagination", {}).get("total_entries", 0)

        output = f"## Contacts Search Results\n\nFound {total} contacts:\n\n"

        for contact in contacts:
            name = contact.get("name", "Unknown")
            email = contact.get("email", "N/A")
            title = contact.get("title", "N/A")
            company = contact.get("organization_name", "N/A")
            output += f"- **{name}** ({email}) - {title} at {company}\n"

        return output[:CHARACTER_LIMIT]
