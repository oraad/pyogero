"""Shared client orchestration for sync and async Ogero transports."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from ._http import check_response_auth_failure
from .const import HTTP_STATUS_BAD_REQUEST
from .exceptions import AuthenticationException, OgeroCommunicationError
from .utils import parse_accounts, parse_bills, parse_consumption_info

if TYPE_CHECKING:
    from .types import Account, BillInfo, ConsumptionInfo, ErrorResponse, LoginResponse

REAUTH_FAILED_MSG = "Re-authentication failed"


def ensure_reauth_retries(max_retries: int) -> None:
    """Raise when the re-login retry budget is exhausted."""
    if max_retries < 0:
        raise AuthenticationException(REAUTH_FAILED_MSG)


def validate_response_body(
    status: int,
    content_type: str | None,
    body: bytes,
) -> bytes:
    """Validate auth/HTTP status and return the response body for parsing."""
    json_body: ErrorResponse | None = None
    if (
        status == HTTP_STATUS_BAD_REQUEST
        and content_type is not None
        and "application/json" in content_type
    ):
        json_body = json.loads(body.decode())

    check_response_auth_failure(
        status,
        content_type,
        json_body=json_body,
        html_content=body,
    )

    if status >= 400:
        msg = f"HTTP {status}"
        if json_body is not None:
            msg = json_body["error"]["message"]
        raise OgeroCommunicationError(msg)

    return body


def parse_login_response(body: bytes) -> LoginResponse:
    """Parse a successful login JSON body."""
    return json.loads(body.decode())


def fetch_accounts(body: bytes) -> list[Account]:
    """Parse dashboard HTML into accounts."""
    return parse_accounts(body)


def fetch_bill_info(body: bytes) -> BillInfo:
    """Parse bill HTML into bill info."""
    return parse_bills(body)


def fetch_consumption_info(body: bytes) -> ConsumptionInfo:
    """Parse consumption HTML."""
    return parse_consumption_info(body)
