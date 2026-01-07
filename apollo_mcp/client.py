"""
Apollo API Client

HTTP client for making requests to Apollo.io API endpoints.
"""

from typing import Optional
import httpx

from apollo_mcp.utils.config import (
    APOLLO_BASE_URL,
    APOLLO_APP_URL,
    REQUEST_TIMEOUT,
    get_headers,
)


class ApolloAPIError(Exception):
    """Exception raised for Apollo API errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


async def make_request(
    method: str,
    endpoint: str,
    data: Optional[dict] = None,
    params: Optional[dict] = None,
    use_app_url: bool = False,
) -> dict:
    """
    Make an async HTTP request to Apollo API.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path (e.g., "/v1/people/search")
        data: Request body data (for POST/PUT)
        params: Query parameters (for GET)
        use_app_url: Use app.apollo.io instead of api.apollo.io

    Returns:
        dict: JSON response from the API

    Raises:
        ApolloAPIError: If the request fails
        ValueError: If an unsupported HTTP method is provided

    Example:
        >>> result = await make_request(
        ...     "POST",
        ...     "/v1/mixed_people/api_search",
        ...     data={"person_titles": ["CEO"]}
        ... )
    """
    base_url = APOLLO_APP_URL if use_app_url else APOLLO_BASE_URL
    url = f"{base_url}{endpoint}"

    # Initialize data and params if None
    if data is None:
        data = {}
    if params is None:
        params = {}

    # Get headers with API key
    headers = get_headers(include_api_key=True)

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            if method.upper() == "GET":
                response = await client.get(url, params=params, headers=headers)
            elif method.upper() == "POST":
                response = await client.post(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = await client.put(url, json=data, params=params, headers=headers)
            elif method.upper() == "DELETE":
                response = await client.delete(url, params=params, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

    except httpx.HTTPStatusError as e:
        raise ApolloAPIError(
            f"API request failed: {e.response.text}",
            status_code=e.response.status_code
        )
    except httpx.RequestError as e:
        raise ApolloAPIError(f"Request failed: {str(e)}")
