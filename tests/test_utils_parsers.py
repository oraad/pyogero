"""Unit tests for HTML/JSON parsers."""

from __future__ import annotations

from datetime import datetime

import pytest

from pyogero.const import LEBANON_TIMEZONE
from pyogero.exceptions import OgeroParseError
from pyogero.utils import (
    parse_accounts,
    parse_bills,
    parse_consumption_info,
    parse_error_message,
)

from .mock_data import (
    bill_response,
    consumption_response,
    dashboard_response,
    unauthorized_response,
)


def test_parse_accounts_success() -> None:
    """Parse accounts from dashboard HTML."""
    data, _, _ = dashboard_response()
    accounts = parse_accounts(data)
    assert len(accounts) == 1
    assert accounts[0].phone == "xxxxxxxx"
    assert accounts[0].internet == "Lxxxxxx"


def test_parse_accounts_missing_selector() -> None:
    """Missing account selector raises OgeroParseError."""
    with pytest.raises(OgeroParseError, match="Account selector"):
        parse_accounts("<html><body></body></html>")


def test_parse_bills_success() -> None:
    """Parse bills from bill HTML."""
    data, _, _ = bill_response()
    bill_info = parse_bills(data)
    assert bill_info.total_outstanding.amount > 0
    assert len(bill_info.bills) >= 1


def test_parse_bills_missing_table() -> None:
    """Missing bill table raises OgeroParseError."""
    with pytest.raises(OgeroParseError, match="Bill table"):
        parse_bills("<html><body></body></html>")


def test_parse_consumption_info_fields() -> None:
    """Parse consumption metrics and timestamp."""
    data, _, _ = consumption_response()
    info = parse_consumption_info(data)
    assert info.speed == "up to 50Mbps (FUP)"
    assert info.quota == 800
    assert info.total_consumption == 499.0
    assert info.extra_consumption == 0.0
    assert info.last_update == datetime(2024, 6, 25, 21, 17, tzinfo=LEBANON_TIMEZONE)


def test_parse_error_message_login_required() -> None:
    """Extract login error from script tag."""
    data, _, _ = unauthorized_response()
    msg = parse_error_message(data)
    assert msg is not None
    assert msg.startswith("You are required to login")
