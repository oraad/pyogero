"""Shared utilities."""

from __future__ import annotations

import logging
from datetime import datetime

from bs4 import BeautifulSoup, Tag

from .const import (
    CONNECTION_SPEED,
    DOWNLOAD,
    EXTRA_CONSUMPTION,
    LAST_UPDATE,
    LEBANON_TIMEZONE,
    QUOTA,
    TOTAL_CONSUMPTION,
    UPLOAD,
)
from .exceptions import OgeroParseError
from .types import (
    Account,
    Bill,
    BillAmount,
    BillInfo,
    BillStatus,
    ConsumptionInfo,
    Content,
)


def __parse_status_value(str_val: str) -> float:
    val = str_val.split(maxsplit=1)[0]
    return float("inf") if val == "Unlimited" else float(val)


def __parse_bill_status(amount_tag: Tag) -> BillStatus:
    parent_tag = amount_tag.parent
    if (
        parent_tag is not None
        and (col_status := parent_tag.find_next_sibling("td")) is not None
    ):
        status = col_status.get_text(strip=True).lower()
        if status == "paid":
            return BillStatus.PAID
        if status == "not paid":
            return BillStatus.UNPAID
    return BillStatus.UNKNOWN


def __parse_bill(bill_tag: Tag) -> Bill | None:
    col_date = bill_tag.find(class_="BillDate")
    if col_date is None:
        return None

    date_text = col_date.get_text(strip=True)
    bill_date = datetime.strptime(date_text, "%b%Y")  # noqa: DTZ007

    logging.debug("date: %s", bill_date.strftime("%b %Y"))

    col_amount = bill_tag.find(class_="BillAmount")
    if col_amount is None or not isinstance(col_amount, Tag):
        return None
    amount_str = col_amount.get_text(strip=True)
    amount = BillAmount.parse(amount_str)
    logging.debug("amount: %s", amount)

    status = __parse_bill_status(col_amount)
    logging.debug("status: %s", status)

    return Bill(date=bill_date, amount=amount, status=status)


def parse_content(content: Content) -> BeautifulSoup:
    """Convert html into soup."""
    return BeautifulSoup(content, "html.parser")


def parse_consumption_info(content: Content) -> ConsumptionInfo:
    """Parse consumption info."""
    info = ConsumptionInfo()
    statuses = parse_content(content).find_all(class_="MyConsumptionGrid")

    for status_div in statuses:
        [key, value] = [span.text.strip() for span in status_div]

        if key == CONNECTION_SPEED:
            info.speed = value
        elif key == QUOTA:
            info.quota = int(__parse_status_value(value))
        elif key == UPLOAD:
            info.upload = __parse_status_value(value)
        elif key == DOWNLOAD:
            info.download = __parse_status_value(value)
        elif key == TOTAL_CONSUMPTION:
            info.total_consumption = __parse_status_value(value)
        elif key == EXTRA_CONSUMPTION:
            info.extra_consumption = __parse_status_value(value)
        elif key == LAST_UPDATE:
            info.last_update = datetime.strptime(value, "%d/%m/%Y %H:%M").replace(
                tzinfo=LEBANON_TIMEZONE
            )

    return info


def parse_accounts(content: Content) -> list[Account]:
    """Parse accounts."""
    accounts: list[Account] = []

    if (
        accounts_tag := parse_content(content).find("select", id="changnumber")
    ) is None or not isinstance(accounts_tag, Tag):
        msg = "Account selector not found in dashboard HTML"
        raise OgeroParseError(msg)

    account_options = accounts_tag.find_all("option")

    for account_option in account_options:
        accounts.append(
            Account(
                phone=account_option.attrs["value"],
                internet=account_option.attrs["value2"],
            )
        )

    return accounts


def parse_bills(content: Content) -> BillInfo:
    """Parse bills."""
    bill_info = BillInfo(total_outstanding=BillAmount())

    bill_outstanding_section = parse_content(content).find(
        class_="BillOutstandingSection1"
    )

    if (
        bill_outstanding_section is not None
        and (bill_span := bill_outstanding_section.find("span")) is not None
        and isinstance(bill_span, Tag)
    ):
        bill_outstanding_val = bill_span.get_text(strip=True)
        bill_info.total_outstanding = BillAmount.parse(bill_outstanding_val)
    else:
        bill_info.total_outstanding = BillAmount()

    logging.debug("outstanding %s", bill_info.total_outstanding)

    bill_table = parse_content(content).find("table", class_="BillTable")
    if bill_table is None or not isinstance(bill_table, Tag):
        msg = "Bill table not found in bill HTML"
        raise OgeroParseError(msg)
    bill_rows: list[Tag] = bill_table.find_all("tr")

    for row in bill_rows:
        logging.debug("################################")
        bill = __parse_bill(row)

        if bill is None:
            continue

        bill_info.bills.append(bill)

    logging.debug("################################")

    return bill_info


def parse_error_message(content: Content) -> str | None:
    """Parse error message."""
    script_tag = parse_content(content).find("script", {"language": "javascript"})

    if script_tag is None:
        return None

    msg = script_tag.get_text(strip=True)

    err_idx = msg.find("error=")
    if err_idx == -1:
        return None

    err_msg = msg[err_idx + 6 :]
    err_msg = err_msg.split("&")[0]
    err_msg = err_msg.split(";")[0]
    return err_msg.split('"')[0]
