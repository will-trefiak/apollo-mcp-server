"""Configuration and environment settings for Apollo MCP Server."""

import os
from typing import Optional

# API Configuration
APOLLO_API_KEY: str = os.environ.get("APOLLO_API_KEY", "")
APOLLO_BASE_URL: str = "https://api.apollo.io"
APOLLO_APP_URL: str = "https://app.apollo.io"

# Response limits
CHARACTER_LIMIT: int = 25000
DEFAULT_PER_PAGE: int = 25
MAX_PER_PAGE: int = 100

# Request timeout (seconds)
REQUEST_TIMEOUT: float = 60.0


def get_api_key() -> str:
    """
    Get Apollo API key from environment.

    Returns:
        str: The Apollo API key

    Raises:
        ValueError: If APOLLO_API_KEY environment variable is not set
    """
    if not APOLLO_API_KEY:
        raise ValueError(
            "APOLLO_API_KEY environment variable is not set. "
            "Please set it to your Apollo.io API key. "
            "Get your API key from: https://app.apollo.io/settings/integrations/api"
        )
    return APOLLO_API_KEY


def get_headers(include_api_key: bool = True) -> dict:
    """
    Get HTTP headers for Apollo API requests.

    Args:
        include_api_key: Whether to include the API key header

    Returns:
        dict: Headers dictionary for HTTP requests
    """
    headers = {
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
    }
    if include_api_key:
        headers["X-Api-Key"] = get_api_key()
    return headers
