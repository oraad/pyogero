"""Test mock asyncio."""

import re
from collections.abc import Generator
from typing import Any

import aiohttp
import pytest
from aioresponses import CallbackResult, aioresponses
from aioresponses.compat import URL

from pyogero.asyncio import Ogero
from pyogero.const import API_ENDPOINTS
from pyogero.exceptions import AuthenticationException
from tests.const import NO_OUTSTANDING_SESSION_ID_SUFFIX

from .mock_data import (
    MOCK_SESSION_ID,
    bill_response,
    bill_response_no_outstanding_bill,
    consumption_response,
    dashboard_response,
    failed_login_response,
    successful_login_response,
    unauthorized_response,
)


def login_callback(url: URL, **kwargs: dict[str, Any]) -> CallbackResult:
    """Login callback."""
    data_dict = kwargs["data"]
    username = data_dict["Username"]
    password = data_dict["Password"]

    if username == "user" and password == "pass":  # noqa: S105
        mock_data, status_code, headers = successful_login_response()
        callback_result = CallbackResult(
            status=status_code, headers=headers, payload=mock_data
        )
    else:
        mock_data, status_code, headers = failed_login_response()
        callback_result = CallbackResult(
            status=status_code, headers=headers, payload=mock_data
        )
    return callback_result


def dashboard_callback(url: URL, **kwargs: dict[str, Any]) -> CallbackResult:
    """Dashboard callback."""
    data_dict = url.query

    session_id = data_dict["SessionID"]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = dashboard_response()
        callback_result = CallbackResult(
            status=status_code, headers=headers, body=mock_data
        )
    else:
        mock_data, status_code, headers = unauthorized_response()
        callback_result = CallbackResult(
            status=status_code, headers=headers, body=mock_data
        )
    return callback_result


def bill_callback(url: URL, **kwargs: dict[str, Any]) -> CallbackResult:
    """Bill callback."""
    data_dict = url.query

    session_id = data_dict["SessionID"]

    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = bill_response()
        callback_result = CallbackResult(
            status=status_code, headers=headers, body=mock_data
        )
    elif session_id == MOCK_SESSION_ID + NO_OUTSTANDING_SESSION_ID_SUFFIX:
        mock_data, status_code, headers = bill_response_no_outstanding_bill()
        callback_result = CallbackResult(
            status=status_code, headers=headers, body=mock_data
        )
    else:
        mock_data, status_code, headers = unauthorized_response()
        callback_result = CallbackResult(
            status=status_code, headers=headers, body=mock_data
        )
    return callback_result


def consumption_callback(url: URL, **kwargs: dict[str, Any]) -> CallbackResult:
    """Consumption callback."""
    data_dict = url.query

    session_id = data_dict["SessionID"]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = consumption_response()
        callback_result = CallbackResult(
            status=status_code, headers=headers, body=mock_data
        )
    else:
        mock_data, status_code, headers = unauthorized_response()
        callback_result = CallbackResult(
            status=status_code, headers=headers, body=mock_data
        )
    return callback_result


@pytest.fixture(name="aio_mock")
def mock_aioresponse() -> Generator[aioresponses, Any, None]:
    """Mock aio response."""
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


@pytest.mark.asyncio()
def test_missing_credentials(aio_mock: aioresponses) -> None:
    """Test missing credentials."""
    with pytest.raises(AuthenticationException):
        Ogero("", "")


@pytest.mark.asyncio()
async def test_login(aio_mock: aioresponses) -> None:
    """Test login."""
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)
        result = await client.login()
        assert result is True


@pytest.mark.asyncio()
async def test_failed_login() -> None:
    """Test failed login."""
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "wrongpass", session=session)

        with pytest.raises(AuthenticationException):
            await client.login()


@pytest.mark.asyncio()
async def test_get_accounts(aio_mock: aioresponses) -> None:
    """Test get accounts."""
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        await client.login()
        accounts = await client.get_accounts()

        assert accounts is not None
        assert len(accounts) >= 1


@pytest.mark.asyncio()
async def test_get_consumption_info(aio_mock: aioresponses) -> None:
    """Test get consumption info."""
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        await client.login()
        accounts = await client.get_accounts()
        assert accounts is not None
        consumption_info = await client.get_consumption_info(accounts[0])

        assert consumption_info is not None


@pytest.mark.asyncio()
async def test_get_bill_info(aio_mock: aioresponses) -> None:
    """Test get bill info."""
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        await client.login()
        accounts = await client.get_accounts()

        assert accounts is not None
        bill_info = await client.get_bill_info(accounts[0])
        assert bill_info is not None
        assert bill_info.total_outstanding is not None
        assert len(bill_info.bills) >= 1


@pytest.mark.asyncio()
async def test_get_bill_info_no_outstanding_bill(aio_mock: aioresponses) -> None:
    """Test get bill info no outstanding bill."""
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        await client.login()
        accounts = await client.get_accounts()
        assert client.session_id is not None
        client.session_id += NO_OUTSTANDING_SESSION_ID_SUFFIX
        assert accounts is not None
        bill_info = await client.get_bill_info(accounts[0])
        assert bill_info is not None
        assert bill_info.total_outstanding is not None
        assert len(bill_info.bills) >= 1


@pytest.mark.asyncio()
async def test_relogin(aio_mock: aioresponses) -> None:
    """Test re-login."""
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)
        client.session_id = "123"
        accounts = await client.get_accounts()

        assert accounts is not None
        assert len(accounts) >= 1


@pytest.mark.asyncio()
async def test_fail_relogin(aio_mock: aioresponses) -> None:
    """Test fail re-login."""
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "wrongpass", session=session)
        client.session_id = "123"
        with pytest.raises(AuthenticationException):
            await client.get_accounts()
