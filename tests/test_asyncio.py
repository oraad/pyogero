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
import aiohttp
from ogero.asyncio import Ogero
from ogero.types import ConfigUser
from ogero.exceptions import AuthenticationException

from .test_utils import configloader

CONFIG = configloader()
if CONFIG is None or len(CONFIG.users) == 0:
    pytest.exit("You need some users in config.json")


@pytest.fixture(name="users")
def userfactory() -> list[ConfigUser]:
    """API factory"""

    return CONFIG.users


def test_missing_credentials():
    with pytest.raises(AuthenticationException):
        Ogero("", "")


@pytest.mark.asyncio
async def test_login(users: list[ConfigUser]):
    for user in users:
        async with aiohttp.ClientSession() as session:
            client = Ogero(user.username, user.password, session=session)
            result = await client.login()
            assert result == True


@pytest.mark.asyncio
async def test_failed_login():
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)

        with pytest.raises(AuthenticationException):
            await client.login()


@pytest.mark.asyncio
async def test_get_accounts(users: list[ConfigUser]):
    for user in users:
        async with aiohttp.ClientSession() as session:
            client = Ogero(user.username, user.password, session=session)

            await client.login()
            accounts = await client.get_accounts()

            assert len(accounts) >= 1


@pytest.mark.asyncio
async def test_get_consumption_info(users: list[ConfigUser]):
    for user in users:
        async with aiohttp.ClientSession() as session:
            client = Ogero(user.username, user.password, session=session)

            await client.login()
            accounts = await client.get_accounts()
            consumption_info = await client.get_consumption_info(accounts[0])

            assert consumption_info is not None


@pytest.mark.asyncio
async def test_get_bill_info(users: list[ConfigUser]):
    for user in users:
        async with aiohttp.ClientSession() as session:
            client = Ogero(user.username, user.password, session=session)

            await client.login()
            accounts = await client.get_accounts()
            bill_info = await client.get_bill_info(accounts[0])
            assert bill_info is not None
            assert bill_info.total_outstanding is not None
            assert len(bill_info.bills) >= 1


@pytest.mark.asyncio
async def test_relogin(users: list[ConfigUser]):
    for user in users:
        async with aiohttp.ClientSession() as session:
            client = Ogero(user.username, user.password, session=session)
            client.session_id = "123"
            accounts = await client.get_accounts()

            assert len(accounts) >= 1


@pytest.mark.asyncio
async def test_fail_relogin():
    async with aiohttp.ClientSession() as session:
        client = Ogero("user", "pass", session=session)
        client.session_id = "123"
        with pytest.raises(AuthenticationException):
            await client.get_accounts()
