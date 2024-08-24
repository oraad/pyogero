"""Test mock requests."""

from urllib.parse import parse_qs

import pytest
import requests
import requests_mock

from pyogero import Ogero
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


def login_callback(request: requests.Request, context: requests.Response):
    data_dict = parse_qs(request.text)
    username = data_dict["Username"][0]
    password = data_dict["Password"][0]

    if username == "user" and password == "pass":
        mock_data, status_code, headers = successful_login_response()
        context.headers = headers
        context.status_code = status_code

    else:
        mock_data, status_code, headers = failed_login_response()
        context.headers = headers
        context.status_code = status_code

    return mock_data


def dashboard_callback(request: requests.Request, context: requests.Response):
    data_dict = request.qs

    session_id = data_dict["sessionid"][0]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = dashboard_response()
        context.status_code = status_code
        context.headers = headers
    else:
        mock_data, status_code, headers = unauthorized_response()
        context.status_code = status_code
        context.headers = headers

    return mock_data


def bill_callback(request: requests.Request, context: requests.Response):
    data_dict = request.qs

    session_id = data_dict["sessionid"][0]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = bill_response()
        context.status_code = status_code
        context.headers = headers
    elif session_id == MOCK_SESSION_ID + NO_OUTSTANDING_SESSION_ID_SUFFIX:
        mock_data, status_code, headers = bill_response_no_outstanding_bill()
        context.status_code = status_code
        context.headers = headers
    else:
        mock_data, status_code, headers = unauthorized_response()
        context.status_code = status_code
        context.headers = headers

    return mock_data


def consumption_callback(request: requests.Request, context: requests.Response):
    data_dict = request.qs

    session_id = data_dict["sessionid"][0]
    if session_id == MOCK_SESSION_ID:
        mock_data, status_code, headers = consumption_response()
        context.status_code = status_code
        context.headers = headers
    else:
        mock_data, status_code, headers = unauthorized_response()
        context.status_code = status_code
        context.headers = headers

    return mock_data


@pytest.fixture(name="requests_mock")
def mock_response():
    with requests_mock.Mocker() as mock:
        mock.post(API_ENDPOINTS["login"], json=login_callback)
        mock.get(API_ENDPOINTS["dashboard"].split("?")[0], text=dashboard_callback)
        mock.get(API_ENDPOINTS["bill"].split("?")[0], text=bill_callback)
        mock.get(API_ENDPOINTS["consumption"].split("?")[0], text=consumption_callback)

        yield mock


def test_missing_credentials(requests_mock: requests_mock.Mocker):
    with pytest.raises(AuthenticationException):
        Ogero("", "")


def test_login(requests_mock: requests_mock.Mocker):
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)
        result = client.login()
        assert result is True


def test_failed_login(requests_mock: requests_mock.Mocker):
    with requests.Session() as session:
        client = Ogero("user", "wrongpass", session=session)

        with pytest.raises(AuthenticationException):
            client.login()


def test_get_accounts(requests_mock: requests_mock.Mocker):
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)
        client.login()
        accounts = client.get_accounts()

        assert accounts is not None
        assert len(accounts) >= 1


def test_get_consumption_info(requests_mock: requests_mock.Mocker):
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)

        client.login()
        accounts = client.get_accounts()
        assert accounts is not None
        consumption_info = client.get_consumption_info(accounts[0])

        assert consumption_info is not None


def test_get_bill_info(requests_mock: requests_mock.Mocker):
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)
        client.login()
        accounts = client.get_accounts()
        assert accounts is not None
        bill_info = client.get_bill_info(accounts[0])
        assert bill_info is not None
        assert bill_info.total_outstanding is not None
        assert len(bill_info.bills) >= 1


def test_get_bill_info_no_outstanding(requests_mock: requests_mock.Mocker):
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)
        client.login()
        accounts = client.get_accounts()
        assert client.session_id is not None
        client.session_id += NO_OUTSTANDING_SESSION_ID_SUFFIX
        assert accounts is not None
        bill_info = client.get_bill_info(accounts[0])
        assert bill_info is not None
        assert bill_info.total_outstanding is not None
        assert len(bill_info.bills) >= 1


def test_relogin(requests_mock: requests_mock.Mocker):
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)
        client.session_id = "123"
        accounts = client.get_accounts()
        assert accounts is not None
        assert len(accounts) >= 1


def test_fail_relogin(requests_mock: requests_mock.Mocker) -> None:
    with requests.Session() as session:
        client = Ogero("user", "wrongpass", session=session)
        client.session_id = "123"
        with pytest.raises(AuthenticationException):
            client.get_accounts()
