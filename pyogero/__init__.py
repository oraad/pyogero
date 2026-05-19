"""A class for interacting with Ogero APIs."""

from __future__ import annotations

import logging
from typing import Any

from requests import Session
from requests.exceptions import RequestException

from ._client import (
    ensure_reauth_retries,
    fetch_accounts,
    fetch_bill_info,
    fetch_consumption_info,
    parse_login_response,
    validate_response_body,
)
from ._http import build_request_params, validate_credentials
from .const import API_ENDPOINTS, DefaultHeaders, default_headers
from .exceptions import (
    AuthenticationException,
    OgeroCommunicationError,
    OgeroError,
    OgeroParseError,
)
from .types import (
    Account,
    Bill,
    BillAmount,
    BillInfo,
    BillStatus,
    ConsumptionInfo,
    LoginResponse,
)

__all__ = [
    "Account",
    "AuthenticationException",
    "Bill",
    "BillAmount",
    "BillInfo",
    "BillStatus",
    "ConsumptionInfo",
    "LoginResponse",
    "Ogero",
    "OgeroCommunicationError",
    "OgeroError",
    "OgeroParseError",
]


class Ogero:
    """A class for interacting with Ogero APIs."""

    def __init__(
        self,
        username: str,
        password: str,
        session: Session | None = None,
        logger: logging.Logger | None = None,
        debug: bool = False,  # noqa: FBT001, FBT002
    ) -> None:
        validate_credentials(username, password)

        self.username = username
        self.password = password
        self.debug = debug
        self.logger = logger if logger is not None else logging.getLogger()
        self.session_id: str | None = None

        self.session = session or Session()
        self.session.verify = True

    def login(self) -> bool:
        """Log into the account and caches the session id."""
        url = API_ENDPOINTS["login"]

        headers: Any = default_headers()
        payload = {"Username": self.username, "Password": self.password}

        try:
            with self.session.post(url, headers=headers, data=payload) as response:
                self.session_id = None
                status_code = response.status_code
                body = validate_response_body(
                    status_code,
                    response.headers.get("content-type"),
                    response.content,
                )
                jsondata = parse_login_response(body)
        except RequestException as ex:
            raise OgeroCommunicationError(str(ex)) from ex

        self.logger.debug("Login response status: %s", status_code)

        self.session_id = jsondata["SessionID"]

        return True

    def get_accounts(self) -> list[Account]:
        """Get user phone/internet accounts."""
        body = self.request_get(API_ENDPOINTS["dashboard"])
        accounts = fetch_accounts(body)

        self.logger.debug("Dumping accounts response: %s", accounts)

        return accounts

    def get_bill_info(self, account: Account | None = None) -> BillInfo:
        """Get bill info for phone account."""
        body = self.request_get(API_ENDPOINTS["bill"], account)
        bill_info = fetch_bill_info(body)

        self.logger.debug(
            "Dumping bill response: %s \n%s",
            bill_info,
            bill_info.bills,
        )

        return bill_info

    def get_consumption_info(self, account: Account | None = None) -> ConsumptionInfo:
        """Get consumption info for internet account."""
        body = self.request_get(API_ENDPOINTS["consumption"], account)
        consumption_info = fetch_consumption_info(body)

        self.logger.debug("Dumping consumption response: %s", consumption_info)

        return consumption_info

    def request_get(
        self,
        url: str,
        account: Account | None = None,
        headers: DefaultHeaders | None = None,
        max_retries: int = 1,
    ) -> bytes:
        """Send get request and return the validated response body."""
        ensure_reauth_retries(max_retries)

        if self.session_id is None:
            self.login()

        _headers: Any = headers if headers is not None else default_headers()

        try:
            assert self.session_id is not None
            params = build_request_params(self.session_id, self.username, account)
            formatted_url = url.format_map(params)
            response = self.session.get(formatted_url, headers=_headers)
            return validate_response_body(
                response.status_code,
                response.headers.get("content-type"),
                response.content,
            )
        except AuthenticationException as ex:
            self.logger.debug("AuthenticationException: %s", ex)
            self.login()
            return self.request_get(url, account, headers, max_retries - 1)
        except RequestException as ex:
            raise OgeroCommunicationError(str(ex)) from ex
