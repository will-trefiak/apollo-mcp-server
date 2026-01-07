# Apollo MCP Server

A Model Context Protocol (MCP) server for [Apollo.io](https://apollo.io) - the leading sales intelligence and engagement platform. This server provides 34+ tools for automating sales outreach, prospecting, and pipeline management.

## Features

- **People Search & Enrichment** - Find and enrich contact data from Apollo's 275M+ contact database
- **Organization Search & Enrichment** - Search companies by industry, size, location, and more
- **Email Sequences** - Create and manage automated outreach campaigns with A/B testing
- **Contact Management** - Organize contacts into lists and manage pipeline stages
- **Workflow Automation** - Build event-driven automations for your sales process
- **Tasks & Activities** - Create and track sales activities
- **Deals Pipeline** - Manage opportunities through your sales pipeline
- **Analytics** - Track sequence performance and email deliverability

## Installation

### Prerequisites

- Python 3.10+
- An [Apollo.io](https://apollo.io) account with API access
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Install with uv

```bash
# Clone the repository
git clone https://github.com/yourusername/apollo-mcp-server.git
cd apollo-mcp-server

# Install dependencies
uv pip install -e .
```

### Install with pip

```bash
pip install -e .
```

## Configuration

### Get Your Apollo API Key

1. Log in to [Apollo.io](https://app.apollo.io)
2. Go to **Settings** > **Integrations** > **API**
3. Generate or copy your API key

### Set Environment Variable

```bash
export APOLLO_API_KEY="your-api-key-here"
```

Or add to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
echo 'export APOLLO_API_KEY="your-api-key-here"' >> ~/.zshrc
```

## Usage

### With Claude Code

Add to your Claude Code MCP configuration (`~/.claude.json`):

```json
{
  "mcpServers": {
    "apollo": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/apollo-mcp-server", "python", "-m", "apollo_mcp.server"],
      "env": {
        "APOLLO_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

### Standalone

```bash
# Run the server
python -m apollo_mcp.server
```

## Available Tools

### People & Contacts (6 tools)

| Tool | Description |
|------|-------------|
| `people_search` | Search Apollo's 275M+ contact database with filters |
| `people_enrich` | Enrich a person's profile by email, name, or LinkedIn |
| `contacts_search` | Search contacts in your Apollo CRM |

### Organizations (3 tools)

| Tool | Description |
|------|-------------|
| `organization_search` | Search companies by industry, size, location |
| `organization_enrich` | Get comprehensive company data by domain |
| `organization_job_postings` | Get current job postings for a company |

### Email Sequences (5 tools)

| Tool | Description |
|------|-------------|
| `sequences_list` | List all email sequences |
| `sequence_get` | Get sequence details and stats |
| `sequence_create` | Create multi-step outreach sequences |
| `sequence_add_contacts` | Add contacts to a sequence |
| `sequence_activate` | Activate or pause a sequence |

### Contact Lists (3 tools)

| Tool | Description |
|------|-------------|
| `lists_get` | Get all saved lists |
| `list_create` | Create a new contact list |
| `list_add_contacts` | Add contacts to a list |

### Workflows (7 tools)

| Tool | Description |
|------|-------------|
| `workflows_list` | List all workflow automations |
| `workflow_get` | Get workflow details |
| `workflow_create` | Create event-driven automations |
| `workflow_update` | Update workflow configuration |
| `workflow_activate` | Activate or deactivate workflows |
| `workflow_delete` | Delete a workflow |
| `workflow_templates_list` | Browse workflow templates |
| `workflow_create_from_template` | Create from a template |

### Email (2 tools)

| Tool | Description |
|------|-------------|
| `email_preview` | Preview emails with variable substitution |
| `email_send` | Send one-off emails |

### Tasks (2 tools)

| Tool | Description |
|------|-------------|
| `tasks_list` | List all tasks |
| `task_create` | Create tasks for contacts |

### Deals (2 tools)

| Tool | Description |
|------|-------------|
| `deals_list` | List pipeline opportunities |
| `deal_create` | Create new deals |

### Analytics (2 tools)

| Tool | Description |
|------|-------------|
| `analytics_sequences` | Get sequence performance metrics |
| `analytics_email_accounts` | Get email deliverability stats |

### Utility (4 tools)

| Tool | Description |
|------|-------------|
| `get_available_fields` | List email personalization variables |
| `get_email_schedules` | Get sending schedule options |
| `get_contact_stages` | Get contact pipeline stages |
| `get_account_stages` | Get account pipeline stages |

## Examples

### Search for Decision Makers

```python
# Find VPs of Sales at tech companies in California
people_search(
    person_titles=["VP Sales", "Vice President of Sales"],
    organization_locations=["California, US"],
    organization_num_employees_ranges=["51,200", "201,500"]
)
```

### Create an Outreach Sequence

```python
sequence_create(
    name="New Lead Outreach",
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
```

### Create a Workflow Automation

```python
workflow_create(
    name="New Contact Nurture",
    trigger_type="event",
    trigger_events=["contact_saved_or_created"],
    actions=[
        {"type": "add_to_sequence", "config": {"sequence_id": "abc123"}}
    ]
)
```

## Email Personalization Variables

Use these variables in email templates:

| Variable | Description |
|----------|-------------|
| `{{first_name}}` | Contact's first name |
| `{{last_name}}` | Contact's last name |
| `{{company}}` | Company name |
| `{{title}}` | Job title |
| `{{email}}` | Email address |
| `{{city}}` | City |
| `{{state}}` | State/region |
| `{{country}}` | Country |

## API Endpoints

The server uses two Apollo API endpoints:

- **Public API** (`api.apollo.io/v1/`): People search, enrichment
- **App API** (`app.apollo.io/api/v1/`): Sequences, workflows, lists, etc.

All requests use the `X-Api-Key` header for authentication.

## Development

### Project Structure

```
apollo-mcp-server/
├── apollo_mcp/
│   ├── __init__.py          # Package initialization
│   ├── server.py             # Main MCP server
│   ├── client.py             # HTTP client for Apollo API
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration and settings
│   │   └── formatting.py     # Output formatting utilities
│   └── tools/
│       ├── __init__.py       # Tool registration
│       ├── people.py         # People/contact tools
│       ├── organizations.py  # Organization tools
│       ├── sequences.py      # Email sequence tools
│       ├── lists.py          # List management tools
│       ├── workflows.py      # Workflow automation tools
│       ├── email.py          # Email tools
│       ├── tasks.py          # Task management tools
│       ├── deals.py          # Deal/opportunity tools
│       ├── analytics.py      # Analytics tools
│       └── utility.py        # Helper tools
├── examples/
│   └── basic_usage.py        # Usage examples
├── pyproject.toml            # Project configuration
├── requirements.txt          # Dependencies
└── README.md
```

### Running Tests

```bash
# Install dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- [Apollo.io](https://apollo.io) for the sales intelligence platform
- [Anthropic](https://anthropic.com) for the Model Context Protocol
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP Python framework
