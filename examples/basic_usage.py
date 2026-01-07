"""
Apollo MCP Server - Basic Usage Examples

These examples show how to use the Apollo MCP tools programmatically.
In practice, you'll use these through Claude or another MCP client.
"""

# Example 1: Search for Decision Makers
# =====================================
# Find VPs of Sales at tech companies in California

PEOPLE_SEARCH_EXAMPLE = {
    "person_titles": ["VP Sales", "Vice President of Sales", "Head of Sales"],
    "organization_locations": ["California, US"],
    "organization_num_employees_ranges": ["51,200", "201,500"],
    "contact_email_status": ["verified"],
    "per_page": 25,
}


# Example 2: Enrich a Contact
# ===========================
# Get full profile data for a person

PEOPLE_ENRICH_EXAMPLE = {
    "email": "john.smith@company.com"
}

# Or by name + company:
PEOPLE_ENRICH_BY_NAME = {
    "first_name": "John",
    "last_name": "Smith",
    "organization_name": "Acme Corp"
}


# Example 3: Search for Companies
# ===============================
# Find SaaS companies in specific locations

ORGANIZATION_SEARCH_EXAMPLE = {
    "q_keywords": "SaaS software",
    "organization_locations": ["California, US", "New York, US"],
    "organization_num_employees_ranges": ["51,200", "201,500"],
    "per_page": 25,
}


# Example 4: Create an Email Sequence
# ===================================
# Multi-step outreach campaign with follow-ups

SEQUENCE_CREATE_EXAMPLE = {
    "name": "New Lead Outreach - Q1 2024",
    "steps": [
        {
            "type": "auto_email",
            "wait_time": 0,
            "wait_mode": "minute",
            "emailer_touches": [{
                "type": "new_thread",
                "subject": "Quick question about {{company}}",
                "body_html": """
                    <p>Hi {{first_name}},</p>
                    <p>I noticed {{company}} is growing rapidly in the {{industry}} space.
                    Congratulations on the momentum!</p>
                    <p>I'm reaching out because we help companies like yours
                    [specific value proposition].</p>
                    <p>Would you be open to a quick 15-minute call this week?</p>
                    <p>Best,<br>{{sender_first_name}}</p>
                """
            }]
        },
        {
            "type": "auto_email",
            "wait_time": 3,
            "wait_mode": "day",
            "emailer_touches": [{
                "type": "reply",
                "subject": "Re: Quick question about {{company}}",
                "body_html": """
                    <p>Hi {{first_name}},</p>
                    <p>Just wanted to follow up on my previous email.
                    I understand you're busy, so I'll keep this brief.</p>
                    <p>[Share a relevant insight or case study]</p>
                    <p>Would a short call make sense?</p>
                    <p>Best,<br>{{sender_first_name}}</p>
                """
            }]
        },
        {
            "type": "auto_email",
            "wait_time": 5,
            "wait_mode": "day",
            "emailer_touches": [{
                "type": "reply",
                "subject": "Re: Quick question about {{company}}",
                "body_html": """
                    <p>Hi {{first_name}},</p>
                    <p>I'll keep this final follow-up short.
                    If now isn't the right time, no worries at all.</p>
                    <p>But if [specific problem you solve] is on your radar,
                    I'd love to share how we've helped similar companies.</p>
                    <p>Either way, wishing you and the {{company}} team continued success!</p>
                    <p>Best,<br>{{sender_first_name}}</p>
                """
            }]
        }
    ],
    "active": False  # Set to True to activate immediately
}


# Example 5: Create a Workflow Automation
# ======================================
# Automatically add new contacts to a sequence

WORKFLOW_CREATE_EXAMPLE = {
    "name": "New Lead Auto-Nurture",
    "trigger_type": "event",
    "model_type": "Contact",
    "trigger_events": ["contact_saved_or_created"],
    "actions": [
        {
            "type": "add_to_sequence",
            "config": {
                "sequence_id": "your-sequence-id-here"
            }
        }
    ],
    "active": False
}


# Example 6: Create a Contact List
# ================================

LIST_CREATE_EXAMPLE = {
    "name": "Q1 2024 Target Accounts",
    "modality": "contacts"  # Options: "contacts", "people", "static"
}


# Example 7: Email Preview with Variables
# =======================================

EMAIL_PREVIEW_EXAMPLE = {
    "subject": "Quick question about {{company}}",
    "body_html": "<p>Hi {{first_name}},</p><p>I noticed {{company}} is growing...</p>",
    "contact_id": "optional-contact-id-for-real-data-preview"
}


# Available Email Personalization Variables
# =========================================
EMAIL_VARIABLES = """
Contact Fields:
- {{first_name}}
- {{last_name}}
- {{name}}
- {{email}}
- {{phone}}
- {{title}}
- {{city}}
- {{state}}
- {{country}}

Company Fields:
- {{company}}
- {{company_domain}}
- {{company_phone}}
- {{industry}}
- {{company_city}}
- {{company_state}}
- {{company_country}}

Sender Fields:
- {{sender_first_name}}
- {{sender_last_name}}
- {{sender_email}}
- {{sender_phone}}
- {{sender_title}}
- {{sender_company}}
"""


if __name__ == "__main__":
    print("Apollo MCP Server - Example Configurations")
    print("=" * 50)
    print("\nThese examples show the data structures used with Apollo MCP tools.")
    print("In practice, you'll use these through Claude or another MCP client.")
    print("\nAvailable examples:")
    print("- PEOPLE_SEARCH_EXAMPLE")
    print("- PEOPLE_ENRICH_EXAMPLE")
    print("- ORGANIZATION_SEARCH_EXAMPLE")
    print("- SEQUENCE_CREATE_EXAMPLE")
    print("- WORKFLOW_CREATE_EXAMPLE")
    print("- LIST_CREATE_EXAMPLE")
    print("- EMAIL_PREVIEW_EXAMPLE")
