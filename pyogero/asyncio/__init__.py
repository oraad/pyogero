"""aiohttp support for Ogero."""

from __future__ import annotations

import logging

try:
    from aiohttp import ClientSession
    from aiohttp.client_exceptions import ClientError
except ImportError as err:
    msg = (
        "aiohttp is required for pyogero.asyncio. Install it with: pip install aiohttp"
    )
    raise ImportError(msg) from err

from pyogero._client import (
    ensure_reauth_retries,
    fetch_accounts,
    fetch_bill_info,
    fetch_consumption_info,
    parse_login_response,
    validate_response_body,
)
from pyogero._http import build_request_params, validate_credentials
from pyogero.const import API_ENDPOINTS, DefaultHeaders, default_headers
from pyogero.exceptions import (
    AuthenticationException,
    OgeroCommunicationError,
    OgeroParseError,
)
from pyogero.types import (
    Account,
    Bill,
    BillAmount,
    BillInfo,
    BillStatus,
    ConsumptionInfo,
)

__all__ = [
    "Account",
    "AuthenticationException",
    "Bill",
    "BillAmount",
    "BillInfo",
    "BillStatus",
    "ConsumptionInfo",
    "Ogero",
    "OgeroCommunicationError",
    "OgeroParseError",
]


class Ogero:
    """aiohttp class for interacting with Ogero APIs."""

    def __init__(
        self,
        username: str,
        password: str,
        session: ClientSession,
        logger: logging.Logger | None = None,
        debug: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        validate_credentials(username, password)

        self.username = username
        self.password = password
        self.debug = debug
        self.logger = logger if logger is not None else logging.getLogger()
        self.session_id: str | None = None
        self.session = session

    async def login(self) -> bool:
        """Log into the account and caches the session id."""
        url = API_ENDPOINTS["login"]

        headers = default_headers()
        payload = {"Username": self.username, "Password": self.password}

        try:
            async with self.session.post(
                url, headers=headers, data=payload
            ) as response:
                self.session_id = None
                status = response.status
                body = await response.read()
                body = validate_response_body(
                    status,
                    response.content_type,
                    body,
                )
                jsondata = parse_login_response(body)
        except ClientError as ex:
            raise OgeroCommunicationError(str(ex)) from ex

        self.logger.debug("Login response status: %s", status)

        self.session_id = jsondata["SessionID"]

        return True

    async def get_accounts(self, account: Account | None = None) -> list[Account]:
        """Get user phone/internet accounts."""
        body = await self.request_get(API_ENDPOINTS["dashboard"], account)
        accounts = fetch_accounts(body)

        self.logger.debug("Dumping accounts response: %s", accounts)

        return accounts

    async def get_bill_info(self, account: Account | None = None) -> BillInfo:
        """Get bill info for phone account."""
        body = await self.request_get(API_ENDPOINTS["bill"], account)
        bill_info = fetch_bill_info(body)

        self.logger.debug(
            "Dumping bill response: %s \n%s",
            bill_info,
            bill_info.bills,
        )

        return bill_info

    async def get_consumption_info(
        self, account: Account | None = None
    ) -> ConsumptionInfo:
        """Get consumption info for internet account."""
        body = await self.request_get(API_ENDPOINTS["consumption"], account)
        consumption_info = fetch_consumption_info(body)

        self.logger.debug("Dumping consumption response: %s", consumption_info)

        return consumption_info

    async def request_get(
        self,
        url: str,
        account: Account | None = None,
        headers: DefaultHeaders | None = None,
        max_retries: int = 1,
    ) -> bytes:
        """Send get request and return the validated response body."""
        ensure_reauth_retries(max_retries)

        if self.session_id is None:
            await self.login()

        _headers: DefaultHeaders = headers if headers is not None else default_headers()

        try:
            assert self.session_id is not None
            params = build_request_params(self.session_id, self.username, account)
            formatted_url = url.format_map(params)
            async with self.session.get(formatted_url, headers=_headers) as response:
                body = await response.read()
                return validate_response_body(
                    response.status,
                    response.content_type,
                    body,
                )
        except AuthenticationException as ex:
            self.logger.debug("AuthenticationException: %s", ex)
            await self.login()
            return await self.request_get(url, account, headers, max_retries - 1)
        except ClientError as ex:
            raise OgeroCommunicationError(str(ex)) from ex
