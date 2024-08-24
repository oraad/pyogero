"""A class for interacting with Ogero APIs."""

import logging
from typing import Any

from requests import Response, Session

from .const import (
    API_ENDPOINTS,
    # CERT_PATH,
    HTTP_STATUS_BAD_REQUEST,
    HTTP_STATUS_OK,
    DefaultHeaders,
    default_headers,
)
from .exceptions import AuthenticationException
from .types import Account, BillInfo, ConsumptionInfo, ErrorResponse, LoginResponse
from .utils import (
    parse_accounts,
    parse_bills,
    parse_consumption_info,
    parse_error_message,
)


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
        """
        Init class.

        ```
        @param username: str - username for Ogero account
        @param password: str - password for Ogero account
        @param debug: bool - debug mode
        @param logger: Logger
        ```
        """
        if not (username and password):
            msg = "You need to supply both username and password"
            raise AuthenticationException(msg)

        self.username = username
        self.password = password
        self.debug = debug
        self.logger = logger if logger is not None else logging.getLogger()
        self.session_id = None

        if not session:
            self.session = Session()
        else:
            self.session = session

        self.session.verify = True

    def login(self) -> bool:
        """Log into the account and caches the session id."""
        url = API_ENDPOINTS["login"]

        headers: Any = default_headers()
        payload = {"Username": self.username, "Password": self.password}

        with self.session.post(url, headers=headers, data=payload) as response:
            self.session_id = None
            self.handle_response_fail(response)
            jsondata: LoginResponse = response.json()

        self.logger.debug("Login response status: %s", response.status_code)

        self.session_id = jsondata["SessionID"]

        return True

    def get_accounts(self) -> list[Account] | None:
        """Get user phone/internet accounts."""
        url = API_ENDPOINTS["dashboard"]

        response = self.request_get(url)
        if response is None:
            return None
        content = response.content
        accounts = parse_accounts(content)

        self.logger.debug("Dashboard response status: %s", response.status_code)
        self.logger.debug("Dumping accounts response: %s", accounts)

        return accounts

    def get_bill_info(self, account: Account | None = None) -> BillInfo | None:
        """
        Get bill info for phone account.

        ```
        @param account: Account - Phone/Internet account
        ```
        """
        url = API_ENDPOINTS["bill"]

        response = self.request_get(url, account)
        if response is None:
            return None
        content = response.content
        bill_info = parse_bills(content)

        self.logger.debug("Bill response status: %s", response.status_code)
        self.logger.debug(
            "Dumping bill response: %s \n%s",
            bill_info,
            bill_info.bills if bill_info is not None else None,
        )

        return bill_info

    def get_consumption_info(
        self, account: Account | None = None
    ) -> ConsumptionInfo | None:
        """
        Get consumption info for internet account.

        ```
        @param account: Account - Phone/Internet account
        ```
        """
        url = API_ENDPOINTS["consumption"]

        response = self.request_get(url, account)

        if response is None:
            return None

        content = response.content
        consumption_info = parse_consumption_info(content)

        self.logger.debug("Consumption response status: %s", response.status_code)
        self.logger.debug("Dumping consumption response: %s", consumption_info)

        return consumption_info

    def request_get(
        self,
        url: str,
        account: Account | None = None,
        headers: DefaultHeaders | None = None,
        max_retries: int = 1,
    ) -> Response | None:
        """
        Send get request and check if session is active.

        ```
        @param url: str - Endpoint url
        @param account: Account - Phone/Internet account
        @param headers: DefaultHeaders
        @param max_retries: int - Maximum retries
        ```
        """
        if max_retries < 0:
            return None

        if self.session_id is None:
            self.login()

        _headers: Any = headers if headers is not None else default_headers()

        try:
            params = self._get_params(account)
            formatted_url = url.format_map(params)
            response = self.session.get(formatted_url, headers=_headers)
            self.handle_response_fail(response)
        except AuthenticationException as ex:
            self.logger.debug("AuthenticationException: %s", ex)
            self.login()
            response = self.request_get(url, account, headers, max_retries - 1)

        return response

    def _get_params(self, account: Account | None = None) -> dict[str, str]:
        """
        Generate URL required params.

        ```
        @param account: Account - Phone/Internet account
        ```
        """
        if self.session_id is None:
            msg = "Login first"
            raise AuthenticationException(msg)

        return {
            "session_id": self.session_id,
            "username": self.username,
            "phone_account": account.phone if account else "",
            "internet_account": account.internet if account else "",
        }

    def handle_response_fail(
        self,
        response: Response,
    ) -> None:
        """
        Handle response status codes.

        ```
        @param response - requests.Response - the full response object
        ```
        """
        self.logger.debug(
            "status: %s, type: %s",
            {response.status_code},
            {response.headers.get("content-type")},
        )
        if (
            response.status_code == HTTP_STATUS_BAD_REQUEST
            and (content_type := response.headers.get("content-type")) is not None
            and "application/json" in content_type
        ):
            resp: ErrorResponse = response.json()
            msg = resp["error"]["message"]
            self.logger.debug("AuthenticationException: %s", msg)
            raise AuthenticationException(msg)

        if (
            response.status_code == HTTP_STATUS_OK
            and (content_type := response.headers.get("content-type")) is not None
            and "text/html" in content_type
        ):
            content = response.content
            msg = parse_error_message(content)
            if msg is not None and msg.startswith("You are required to login"):
                raise AuthenticationException(msg)

        response.raise_for_status()
