"""
Organization/Account Tools

Tools for searching and enriching company/organization data in Apollo.
"""

from typing import Optional

from apollo_mcp.client import make_request
from apollo_mcp.utils.config import CHARACTER_LIMIT
from apollo_mcp.utils.formatting import format_organization, truncate_response


def register_organization_tools(mcp):
    """Register organization-related tools with the MCP server."""

    @mcp.tool()
    async def organization_search(
        q_keywords: Optional[str] = None,
        organization_domains: Optional[list[str]] = None,
        organization_locations: Optional[list[str]] = None,
        organization_num_employees_ranges: Optional[list[str]] = None,
        organization_industry_tag_ids: Optional[list[str]] = None,
        revenue_range: Optional[dict] = None,
        page: int = 1,
        per_page: int = 25,
    ) -> str:
        """
        Search for organizations/companies in Apollo's database.

        Args:
            q_keywords: Keywords to search (company name, description)
            organization_domains: Specific domains to find
            organization_locations: HQ locations (e.g., ["California, US"])
            organization_num_employees_ranges: Size ranges (e.g., ["1,10", "51,200"])
            organization_industry_tag_ids: Industry filter IDs
            revenue_range: Revenue filter (e.g., {"min": 1000000, "max": 10000000})
            page: Page number
            per_page: Results per page (max 100)

        Returns:
            List of matching organizations with company details

        Example:
            Find SaaS companies in California with 50-200 employees:
            organization_search(
                q_keywords="SaaS software",
                organization_locations=["California, US"],
                organization_num_employees_ranges=["51,200"]
            )
        """
        data = {
            "page": page,
            "per_page": min(per_page, 100),
        }

        if q_keywords:
            data["q_keywords"] = q_keywords
        if organization_domains:
            data["organization_domains"] = organization_domains
        if organization_locations:
            data["organization_locations"] = organization_locations
        if organization_num_employees_ranges:
            data["organization_num_employees_ranges"] = organization_num_employees_ranges
        if organization_industry_tag_ids:
            data["organization_industry_tag_ids"] = organization_industry_tag_ids
        if revenue_range:
            data["revenue_range"] = revenue_range

        result = await make_request("POST", "/v1/organizations/search", data)

        orgs = result.get("organizations", [])
        total = result.get("pagination", {}).get("total_entries", 0)

        output = f"## Organization Search Results\n\nFound {total} total matches:\n\n"

        for org in orgs[:per_page]:
            output += format_organization(org)
            output += "---\n"

        return output[:CHARACTER_LIMIT]

    @mcp.tool()
    async def organization_enrich(domain: str) -> str:
        """
        Enrich an organization's profile by domain.

        Get comprehensive company data including firmographics, technographics,
        funding info, and more.

        Args:
            domain: Company domain (e.g., "stripe.com")

        Returns:
            Enriched organization profile

        Example:
            organization_enrich(domain="openai.com")
        """
        result = await make_request("GET", "/v1/organizations/enrich", params={"domain": domain})

        org = result.get("organization", {})
        if not org:
            return f"No organization found for domain: {domain}"

        return f"## Organization Enrichment Results\n\n{format_organization(org)}\n\nFull Data:\n{truncate_response(org)}"

    @mcp.tool()
    async def organization_job_postings(organization_id: str) -> str:
        """
        Get current job postings for an organization.

        Useful for identifying growth signals and finding the right contacts.

        Args:
            organization_id: Apollo organization ID

        Returns:
            List of current job postings
        """
        result = await make_request("GET", f"/v1/organizations/{organization_id}/job_postings")

        postings = result.get("job_postings", [])

        output = f"## Job Postings\n\nFound {len(postings)} open positions:\n\n"

        for job in postings:
            title = job.get("title", "Unknown")
            location = job.get("location", "N/A")
            posted = job.get("posted_at", "N/A")
            url = job.get("url", "")
            output += f"- **{title}** - {location} (Posted: {posted})\n  {url}\n"

        return output[:CHARACTER_LIMIT]
