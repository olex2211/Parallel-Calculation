from fastapi import Request
import httpx


def get_http_client(request: Request) -> httpx.AsyncClient:
    """Dependency to get the app-level httpx.AsyncClient."""
    return request.app.state.http_client
