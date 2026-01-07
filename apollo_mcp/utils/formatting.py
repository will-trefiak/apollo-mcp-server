"""Formatting utilities for Apollo API responses."""

import json
from typing import Any

from apollo_mcp.utils.config import CHARACTER_LIMIT


def truncate_response(data: Any, max_chars: int = CHARACTER_LIMIT) -> str:
    """
    Truncate response data to fit within character limit.

    Args:
        data: Data to serialize and truncate
        max_chars: Maximum characters allowed

    Returns:
        str: JSON string, truncated if necessary
    """
    text = json.dumps(data, indent=2)
    if len(text) > max_chars:
        return text[:max_chars] + "\n... [truncated]"
    return text


def format_person(person: dict) -> str:
    """
    Format a person/contact record for display.

    Args:
        person: Person data dictionary from Apollo API

    Returns:
        str: Formatted markdown string
    """
    name = person.get("name", "Unknown")
    title = person.get("title", "N/A")
    company = person.get("organization", {}).get("name", "N/A")
    email = person.get("email", "N/A")
    linkedin = person.get("linkedin_url", "N/A")

    return f"""
**{name}**
- Title: {title}
- Company: {company}
- Email: {email}
- LinkedIn: {linkedin}
"""


def format_organization(org: dict) -> str:
    """
    Format an organization/company record for display.

    Args:
        org: Organization data dictionary from Apollo API

    Returns:
        str: Formatted markdown string
    """
    name = org.get("name", "Unknown")
    domain = org.get("primary_domain", "N/A")
    industry = org.get("industry", "N/A")
    employees = org.get("estimated_num_employees", "N/A")

    return f"""
**{name}**
- Domain: {domain}
- Industry: {industry}
- Employees: {employees}
"""


def format_sequence(seq: dict) -> str:
    """
    Format an email sequence for display.

    Args:
        seq: Sequence data dictionary from Apollo API

    Returns:
        str: Formatted markdown string
    """
    name = seq.get("name", "Unknown")
    active = "Active" if seq.get("active") else "Inactive"
    steps = seq.get("num_steps", 0)
    delivered = seq.get("unique_delivered", 0)
    reply_rate = seq.get("reply_rate", 0) * 100
    seq_id = seq.get("id", "")

    return f"""### {name}
- ID: `{seq_id}`
- Status: {active}
- Steps: {steps}
- Delivered: {delivered}
- Reply Rate: {reply_rate:.1f}%
"""


def format_workflow(wf: dict) -> str:
    """
    Format a workflow for display.

    Args:
        wf: Workflow data dictionary from Apollo API

    Returns:
        str: Formatted markdown string
    """
    name = wf.get("name", "Unknown")
    wf_id = wf.get("id", "")
    active = "Active" if wf.get("active") else "Inactive"
    trigger_type = wf.get("trigger_type", "N/A")

    return f"""### {name}
- ID: `{wf_id}`
- Status: {active}
- Trigger: {trigger_type}
"""
