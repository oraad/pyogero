"""Tests for pyogero._http helpers."""

from __future__ import annotations

import json

import pytest

from pyogero._http import (
    build_request_params,
    check_response_auth_failure,
    validate_credentials,
)
from pyogero.exceptions import AuthenticationException
from pyogero.types import Account

from .mock_data import failed_login_response, unauthorized_response


def test_validate_credentials_empty() -> None:
    """Missing credentials raise AuthenticationException."""
    with pytest.raises(AuthenticationException):
        validate_credentials("", "pass")
    with pytest.raises(AuthenticationException):
        validate_credentials("user", "")


def test_build_request_params_requires_login() -> None:
    """build_request_params requires a session id."""
    with pytest.raises(AuthenticationException):
        build_request_params("", "user", None)


def test_build_request_params_account_fields() -> None:
    """Account phone and internet are mapped to URL params."""
    account = Account(phone="01234567", internet="L12345")
    params = build_request_params("sid", "user", account)
    assert params["session_id"] == "sid"
    assert params["username"] == "user"
    assert params["phone_account"] == "01234567"
    assert params["internet_account"] == "L12345"


def test_check_response_auth_failure_json() -> None:
    """JSON 400 responses raise AuthenticationException."""
    data, status, headers = failed_login_response()
    with pytest.raises(AuthenticationException):
        check_response_auth_failure(
            int(status),
            headers["content-type"],
            json_body=data,
        )


def test_check_response_auth_failure_html_login_required() -> None:
    """HTML login redirect raises AuthenticationException."""
    data, status, headers = unauthorized_response()
    with pytest.raises(AuthenticationException):
        check_response_auth_failure(
            int(status),
            headers["content-type"],
            html_content=data,
        )


def test_check_response_auth_failure_benign_html() -> None:
    """Dashboard HTML without login error does not raise."""
    html = "<html><body><select id='changnumber'></select></body></html>"
    check_response_auth_failure(
        200,
        "text/html",
        html_content=html,
    )


def test_check_response_auth_failure_json_from_bytes() -> None:
    """validate_response_body path uses JSON auth errors."""
    from pyogero._client import validate_response_body

    data, status, headers = failed_login_response()
    with pytest.raises(AuthenticationException):
        validate_response_body(
            int(status),
            headers["content-type"],
            json.dumps(data).encode(),
        )
