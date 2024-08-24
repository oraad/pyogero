"""
Using this.

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

from pyogero import Ogero
from pyogero.exceptions import AuthenticationException

from .test_utils import configloader

CONFIG = configloader()
if CONFIG is None or CONFIG.users is None or len(CONFIG.users) == 0:
    pytest.exit("You need some users in config.json")


@pytest.fixture(name="clients", scope="session")
def userfactory() -> list[Ogero] | None:
    """Get API factory."""
    session = requests.Session()
    if CONFIG.users is None:
        return None
    return [
        Ogero(username=user.username, password=user.password, session=session)
        for user in CONFIG.users
    ]


def test_missing_credentials() -> None:
    """Test missing creadentials."""
    with pytest.raises(AuthenticationException):
        Ogero("", "")


def test_login(clients: list[Ogero]) -> None:
    """Test login."""
    for client in clients:
        result = client.login()
        assert result is True


def test_failed_login() -> None:
    """Test failed login."""
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)

        with pytest.raises(AuthenticationException):
            client.login()


def test_get_accounts(clients: list[Ogero]) -> None:
    """Test get accounts."""
    for client in clients:
        client.login()
        accounts = client.get_accounts()

        assert accounts is not None
        assert len(accounts) >= 1


def test_get_consumption_info(clients: list[Ogero]) -> None:
    """Test get consumption info."""
    for client in clients:
        client.login()
        accounts = client.get_accounts()
        assert accounts is not None

        consumption_info = client.get_consumption_info(accounts[0])

        assert consumption_info is not None


def test_get_bill_info(clients: list[Ogero]) -> None:
    """Test get bill info."""
    for client in clients:
        client.login()
        accounts = client.get_accounts()
        assert accounts is not None
        bill_info = client.get_bill_info(accounts[0])
        assert bill_info is not None
        assert bill_info.total_outstanding is not None
        assert len(bill_info.bills) >= 1


def test_relogin(clients: list[Ogero]) -> None:
    """Test re-login."""
    for client in clients:
        client.session_id = "123"
        accounts = client.get_accounts()
        assert accounts is not None
        assert len(accounts) >= 1


def test_fail_relogin() -> None:
    """Test fail login."""
    with requests.Session() as session:
        client = Ogero("user", "pass", session=session)
        client.session_id = "123"
        with pytest.raises(AuthenticationException):
            client.get_accounts()
