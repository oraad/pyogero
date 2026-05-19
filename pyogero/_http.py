"""Shared HTTP helpers for sync and async Ogero clients."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .const import HTTP_STATUS_BAD_REQUEST, HTTP_STATUS_OK
from .exceptions import AuthenticationException
from .utils import parse_error_message

if TYPE_CHECKING:
    from .types import Account, ErrorResponse

LOGIN_REQUIRED_PREFIX = "You are required to login"


def validate_credentials(username: str, password: str) -> None:
    """Raise if username or password is missing."""
    if not (username and password):
        msg = "You need to supply both username and password"
        raise AuthenticationException(msg)


def build_request_params(
    session_id: str,
    username: str,
    account: Account | None = None,
) -> dict[str, str]:
    """Build URL format_map params for authenticated requests."""
    if not session_id:
        msg = "Login first"
        raise AuthenticationException(msg)

    return {
        "session_id": session_id,
        "username": username,
        "phone_account": account.phone if account else "",
        "internet_account": account.internet if account else "",
    }


def check_response_auth_failure(
    status: int,
    content_type: str | None,
    *,
    json_body: ErrorResponse | None = None,
    html_content: str | bytes | None = None,
) -> None:
    """Raise AuthenticationException when the response indicates auth failure."""
    if (
        status == HTTP_STATUS_BAD_REQUEST
        and content_type is not None
        and "application/json" in content_type
        and json_body is not None
    ):
        msg = json_body["error"]["message"]
        raise AuthenticationException(msg)

    if (
        status == HTTP_STATUS_OK
        and content_type is not None
        and "text/html" in content_type
        and html_content is not None
    ):
        msg = parse_error_message(html_content)
        if msg is not None and msg.startswith(LOGIN_REQUIRED_PREFIX):
            raise AuthenticationException(msg)
