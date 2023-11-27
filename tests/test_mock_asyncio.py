import asyncio
import re
import pytest
import aiohttp
from aioresponses import aioresponses, CallbackResult
from aioresponses.compat import URL

from pyogero.asyncio import Ogero
from pyogero.const import API_ENDPOINTS
from pyogero.types import ConfigUser
from pyogero.exceptions import AuthenticationException
from tests.const import NO_OUTSTANDING_SESSION_ID_SUFFIX

from .mock_data import (
    MOCK_SESSION_ID,
    bill_response_no_outstanding_bill,
    successful_login_response,
    failed_login_response,
    dashboard_response,
    bill_response,
    consumption_response,
    unauthorized_response,
)


def login_callback(url: URL, **kwargs):
    data_dict = kwargs['data']
    username = data_dict["Username"]
    password = data_dict["Password"]

    if username == "user" and password == "pass":
        mock_data, status_code, headers = successful_login_response()
        return CallbackResult(status=status_code, headers=headers, payload=mock_data)
    else:
        mock_data, status_code, headers = failed_login_response()
        return CallbackResult(status=status_code, headers=headers, payload=mock_data)


def dashboard_callback(url: URL, **kwargs):

    data_dict = url.query

    session_id = data_dict["SessionID"]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = dashboard_response()
        return CallbackResult(status=status_code, headers=headers, body=mock_data)
    else:
        mock_data, status_code, headers = unauthorized_response()
        return CallbackResult(status=status_code, headers=headers, body=mock_data)

def bill_callback(url: URL, **kwargs):

    data_dict = url.query

    session_id = data_dict["SessionID"]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = bill_response()
        return CallbackResult(status=status_code, headers=headers, body=mock_data)
    elif session_id == MOCK_SESSION_ID + NO_OUTSTANDING_SESSION_ID_SUFFIX:
        mock_data, status_code, headers = bill_response_no_outstanding_bill()
        return CallbackResult(status=status_code, headers=headers, body=mock_data)
    else:
        mock_data, status_code, headers = unauthorized_response()
        return CallbackResult(status=status_code, headers=headers, body=mock_data)

def consumption_callback(url: URL, **kwargs):

    data_dict = url.query

    session_id = data_dict["SessionID"]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = consumption_response()
        return CallbackResult(status=status_code, headers=headers, body=mock_data)
    else:
        mock_data, status_code, headers = unauthorized_response()
        return CallbackResult(status=status_code, headers=headers, body=mock_data)


@pytest.fixture(name="aio_mock")
def mock_aioresponse():
    with aioresponses() as mock:
        mock.post(API_ENDPOINTS["login"], callback=login_callback, repeat=True)

        dashboard_pattern = re.compile(r"^" + API_ENDPOINTS["dashboard"].split("?")[0])
        mock.get(dashboard_pattern, callback=dashboard_callback, repeat=True)

        bill_pattern = re.compile(r"^" + API_ENDPOINTS["bill"].split("?")[0])
        mock.get(bill_pattern, callback=bill_callback, repeat=True)

        consumption_pattern = re.compile(r"^" + API_ENDPOINTS["consumption"].split("?")[0])
        mock.get(consumption_pattern, callback=consumption_callback, repeat=True)

        yield mock


def test_missing_credentials():
    with pytest.raises(AuthenticationException):
        Ogero("", "")


@pytest.mark.asyncio
async def test_login(aio_mock: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)
        result = await client.login()
        assert result == True


@pytest.mark.asyncio
async def test_failed_login(aio_mock: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "wrongpass", session=session)

        with pytest.raises(AuthenticationException):
            await client.login()


@pytest.mark.asyncio
async def test_get_accounts(aio_mock: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        await client.login()
        accounts = await client.get_accounts()

        assert len(accounts) >= 1


@pytest.mark.asyncio
async def test_get_consumption_info(aio_mock: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        await client.login()
        accounts = await client.get_accounts()
        consumption_info = await client.get_consumption_info(accounts[0])

        assert consumption_info is not None


@pytest.mark.asyncio
async def test_get_bill_info(aio_mock: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        await client.login()
        accounts = await client.get_accounts()
        bill_info = await client.get_bill_info(accounts[0])
        assert bill_info is not None
        assert bill_info.total_outstanding is not None
        assert len(bill_info.bills) >= 1

@pytest.mark.asyncio
async def test_get_bill_info_no_outstanding_bill(aio_mock: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        await client.login()
        accounts = await client.get_accounts()
        client.session_id += NO_OUTSTANDING_SESSION_ID_SUFFIX
        bill_info = await client.get_bill_info(accounts[0])
        assert bill_info is not None
        assert bill_info.total_outstanding is not None
        assert len(bill_info.bills) >= 1

@pytest.mark.asyncio
async def test_relogin(aio_mock: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)
        client.session_id = "123"
        accounts = await client.get_accounts()

        assert len(accounts) >= 1


@pytest.mark.asyncio
async def test_fail_relogin(aio_mock: aioresponses):
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "wrongpass", session=session)
        client.session_id = "123"
        with pytest.raises(AuthenticationException):
            await client.get_accounts()
