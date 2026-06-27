"""Mock data."""

from __future__ import annotations

import re
from http import HTTPStatus
from pathlib import Path
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pyogero.types import ErrorResponse, LoginResponse

json_headers = {"content-type": "application/json"}
html_headers = {"content-type": "text/html"}

MOCK_SESSION_ID = "session_id1"
_FIXTURES = Path(__file__).resolve().parent / "fixtures"

type MockDataResponse = tuple[LoginResponse | ErrorResponse | str, HTTPStatus, Any]


def _load_fixture(name: str) -> str:
    return (_FIXTURES / name).read_text(encoding="utf-8")


def successful_login_response() -> MockDataResponse:
    """Successful Login Response."""
    data: LoginResponse = {"SessionID": MOCK_SESSION_ID}
    return data, HTTPStatus.OK, json_headers


def failed_login_response() -> MockDataResponse:
    """Failed login response."""
    data: ErrorResponse = {
        "error": {"code": "2002", "message": "Wrong username/password combination"}
    }
    return data, HTTPStatus.BAD_REQUEST, json_headers


def unauthorized_response() -> MockDataResponse:
    """Unauthorized response."""
    data: str = '<script language="javascript">window.location="login.logout.php?error=You are required to login to access this section";</script>'
    return data, HTTPStatus.OK, html_headers


def dashboard_response() -> MockDataResponse:
    """Dashboard response (redacted live sample)."""
    return _load_fixture("dashboard.html"), HTTPStatus.OK, html_headers


def consumption_response() -> MockDataResponse:
    """Consumption response (redacted live sample)."""
    return _load_fixture("consumption.html"), HTTPStatus.OK, html_headers


def consumption_response_split_spans() -> MockDataResponse:
    """Consumption response with split value spans and whitespace text nodes."""
    data: str = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <title>Ogero - My Consumption</title>
    </head>
    <body>
        <div class="MyConsumptionLeft">
            <div class="MyConsumptionGrid">
                <span>Current Bundle</span> <span>up to 50Mbps</span> <span>(FUP)</span>
            </div>
            <div class="MyConsumptionGrid">
                <span>Total Quota</span> <span>800</span> <span>GB FUP</span>
            </div>
            <div class="MyConsumptionGrid"><span>Upload</span><span>12.0 GB</span></div>
            <div class="MyConsumptionGrid"><span>Download</span><span>143.4 GB</span></div>
            <div class="MyConsumptionGrid">
                <span>Total Consumption</span> <span>499</span> <span>GB</span>
            </div>
            <div class="MyConsumptionGrid"><span>Extra Consumption</span><span>0 GB</span></div>
            <div class="MyConsumptionGrid"><span>Consumption Until</span><span>25/06/2024 21:17</span></div>
        </div>
    </body>
</html>
"""

    return data, HTTPStatus.OK, html_headers


def bill_response() -> MockDataResponse:
    """Bill response (redacted live sample)."""
    return _load_fixture("bill.html"), HTTPStatus.OK, html_headers


def bill_response_no_outstanding_bill() -> MockDataResponse:
    """Bill response with no outstanding bill section."""
    data = _load_fixture("bill.html")
    data = re.sub(
        r'<div class="BillOutstandingSection1"[^>]*>.*?</div>\s*'
        r'<div class="BillOutstandingSection2[^"]*"[^>]*>.*?</div>\s*'
        r'<div class="sep"></div>\s*',
        "",
        data,
        count=1,
        flags=re.DOTALL,
    )
    return data, HTTPStatus.OK, html_headers
