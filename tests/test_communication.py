"""Communication and regression tests for sync/async clients."""

from __future__ import annotations

import re
from http import HTTPStatus
from typing import TYPE_CHECKING, Any

import aiohttp
import pytest
import requests
from aioresponses import CallbackResult, aioresponses

from pyogero import Ogero as SyncOgero
from pyogero.asyncio import Ogero as AsyncOgero
from pyogero.const import API_ENDPOINTS
from pyogero.exceptions import AuthenticationException, OgeroCommunicationError
from tests.const import NO_OUTSTANDING_SESSION_ID_SUFFIX

from .mock_data import (
    MOCK_SESSION_ID,
    bill_response,
    bill_response_no_outstanding_bill,
    consumption_response,
    dashboard_response,
    unauthorized_response,
)
from .test_mock_asyncio import login_callback
from .test_mock_requests import login_callback as sync_login_callback

if TYPE_CHECKING:
    import requests_mock
    from aioresponses.compat import URL


def test_sync_communication_error(requests_mock: requests_mock.Mocker) -> None:
    """HTTP 503 is raised as OgeroCommunicationError."""
    requests_mock.post(API_ENDPOINTS["login"], json=sync_login_callback)
    requests_mock.get(
        API_ENDPOINTS["dashboard"].split("?")[0],
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
    )
    with requests.Session() as session:
        client = SyncOgero("user", "pass", session=session)
        client.login()
        with pytest.raises(OgeroCommunicationError):
            client.get_accounts()


@pytest.fixture(name="aio_mock")
def mock_aioresponse() -> Any:
    """Mock aio responses for async client tests."""
    with aioresponses() as mock:
        mock.post(API_ENDPOINTS["login"], callback=login_callback, repeat=True)
        dashboard_pattern = re.compile(r"^" + API_ENDPOINTS["dashboard"].split("?")[0])
        mock.get(dashboard_pattern, callback=dashboard_callback, repeat=True)
        bill_pattern = re.compile(r"^" + API_ENDPOINTS["bill"].split("?")[0])
        mock.get(bill_pattern, callback=bill_callback, repeat=True)
        consumption_pattern = re.compile(
            r"^" + API_ENDPOINTS["consumption"].split("?")[0]
        )
        mock.get(consumption_pattern, callback=consumption_callback, repeat=True)
        yield mock


def dashboard_callback(url: URL, **kwargs: dict[str, Any]) -> CallbackResult:
    """Dashboard callback for async tests."""
    session_id = url.query["SessionID"]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = dashboard_response()
    else:
        mock_data, status_code, headers = unauthorized_response()
    return CallbackResult(status=status_code, headers=headers, body=mock_data)


def bill_callback(url: URL, **kwargs: dict[str, Any]) -> CallbackResult:
    """Bill callback for async tests."""
    session_id = url.query["SessionID"]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = bill_response()
    elif session_id == MOCK_SESSION_ID + NO_OUTSTANDING_SESSION_ID_SUFFIX:
        mock_data, status_code, headers = bill_response_no_outstanding_bill()
    else:
        mock_data, status_code, headers = unauthorized_response()
    return CallbackResult(status=status_code, headers=headers, body=mock_data)


def consumption_callback(url: URL, **kwargs: dict[str, Any]) -> CallbackResult:
    """Consumption callback for async tests."""
    session_id = url.query["SessionID"]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = consumption_response()
    else:
        mock_data, status_code, headers = unauthorized_response()
    return CallbackResult(status=status_code, headers=headers, body=mock_data)


@pytest.mark.asyncio
async def test_async_communication_error() -> None:
    """HTTP 503 is raised as OgeroCommunicationError."""
    pattern = re.compile(r"^" + API_ENDPOINTS["dashboard"].split("?")[0])
    with aioresponses() as aio_mock:
        aio_mock.post(API_ENDPOINTS["login"], callback=login_callback, repeat=True)
        aio_mock.get(
            pattern,
            status=HTTPStatus.SERVICE_UNAVAILABLE,
            repeat=True,
        )
        async with aiohttp.ClientSession() as session:
            client = AsyncOgero("user", "pass", session=session)
            await client.login()
            with pytest.raises(OgeroCommunicationError):
                await client.get_accounts()


@pytest.mark.asyncio
async def test_async_body_read_once_regression(aio_mock: aioresponses) -> None:
    """Dashboard HTML is fully parsed after auth validation (single body read)."""
    async with aiohttp.ClientSession() as session:
        client = AsyncOgero("user", "pass", session=session)
        await client.login()
        accounts = await client.get_accounts()
        assert len(accounts) >= 1
        assert accounts[0].phone == "xxxxxxxx"


@pytest.mark.asyncio
async def test_async_fail_relogin_raises(aio_mock: aioresponses) -> None:
    """Exhausted re-login retries raise AuthenticationException."""
    async with aiohttp.ClientSession() as session:
        client = AsyncOgero("user", "wrongpass", session=session)
        client.session_id = "invalid"
        with pytest.raises(AuthenticationException):
            await client.get_accounts()
