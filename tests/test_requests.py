"""
Using this
You really need a file called "ogero.json" in either the local dir or ~/.config/.
It needs at least one user in the "users" field. eg:
{
    "users" : [
        { "username" : "username", "password" : "password" }
    ]
}
"""

import pytest
import requests
from ogero import Ogero
from ogero.exceptions import AuthenticationException

from .test_utils import configloader

CONFIG = configloader()
if CONFIG is None or len(CONFIG.users) == 0:
    pytest.exit("You need some users in config.json")


@pytest.fixture(name="clients", scope="session")
def userfactory() -> list[Ogero]:
    """API factory"""
    session = requests.Session()
    return [
        Ogero(username=user.username, password=user.password, session=session)
        for user in CONFIG.users
    ]


def test_missing_credentials():
    with pytest.raises(AuthenticationException):
        Ogero("", "")


def test_login(clients: list[Ogero]):
    for client in clients:
        result = client.login()
        assert result == True


def test_failed_login():
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)

        with pytest.raises(AuthenticationException):
            client.login()


def test_get_accounts(clients: list[Ogero]):
    for client in clients:
        client.login()
        accounts = client.get_accounts()

        assert len(accounts) >= 1


def test_get_consumption_info(clients: list[Ogero]):
    for client in clients:

        client.login()
        accounts = client.get_accounts()
        consumption_info = client.get_consumption_info(accounts[0])

        assert consumption_info is not None


def test_get_bill_info(clients: list[Ogero]):
    for client in clients:
        client.login()
        accounts = client.get_accounts()
        bill_info = client.get_bill_info(accounts[0])
        assert bill_info is not None
        assert bill_info.total_outstanding is not None
        assert len(bill_info.bills) >= 1


def test_relogin(clients: list[Ogero]):
    for client in clients:
        client.session_id = "123"
        accounts = client.get_accounts()

        assert len(accounts) >= 1


def test_fail_relogin(clients: list[Ogero]):
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)
        client.session_id = "123"
        with pytest.raises(AuthenticationException):
            client.get_accounts()
