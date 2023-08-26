""" shared utilities """
from datetime import datetime
import logging
from typing import Optional
from bs4 import BeautifulSoup, ResultSet, Tag, NavigableString
from .const import (
    CONNECTION_SPEED,
    DOWNLOAD,
    EXTRA_CONSUMPTION,
    LAST_UPDATE,
    QUOTA,
    TOTAL_CONSUMPTION,
    UPLOAD,
)
from .types import (
    Account,
    Bill,
    BillAmount,
    BillInfo,
    BillStatus,
    Content,
    ConsumptionInfo,
)


def __parse_status_value(str_val: str):
    val = str_val.split()[0]

    if val == "Unlimited":
        return float("inf")
    else:
        return float(val)


def __parse_bill_status(amount_tag: Tag | NavigableString, bill: Bill) -> None:
    if amount_tag.parent is None:
        return

    col_status = amount_tag.parent.findNextSibling("td")
    if col_status is None:
        return

    status = col_status.get_text(strip=True).lower()
    if status == "paid":
        bill.status = BillStatus.PAID
    elif status == "not paid":
        bill.status = BillStatus.UNPAID
    else:
        bill.status = BillStatus.UNKNOWN
    logging.debug(f"status: {bill.status}")


def __parse_bill(bill_tag: Tag):
    bill = Bill()
    col_date = bill_tag.find(class_="BillDate")
    if col_date is None:
        return None

    date_text = col_date.get_text(strip=True)
    bill.date = datetime.strptime(date_text, "%b%Y")

    logging.debug(f"date: {bill.date.strftime('%b %Y')}")

    col_amount = bill_tag.find(class_="BillAmount")
    if col_amount is None:
        return

    amount_str = col_amount.get_text(strip=True)
    bill.amount = BillAmount.parse(amount_str)
    logging.debug(f"amount: {bill.amount}")

    __parse_bill_status(col_amount, bill)

    return bill


def parse_content(content: Content):
    """
    convert html into soup
    """
    return BeautifulSoup(content, "html.parser")


def parse_consumption_info(content: Content) -> ConsumptionInfo:

    info = ConsumptionInfo()
    statuses = parse_content(content).find_all(class_="MyConsumptionGrid")

    for status_div in statuses:
        [key, value] = [span.text.strip() for span in status_div]

        if key == CONNECTION_SPEED:
            info.speed = value
        elif key == QUOTA:
            info.quota = __parse_status_value(value)
        elif key == UPLOAD:
            info.upload = __parse_status_value(value)
        elif key == DOWNLOAD:
            info.download = __parse_status_value(value)
        elif key == TOTAL_CONSUMPTION:
            info.total_consumption = __parse_status_value(value)
        elif key == EXTRA_CONSUMPTION:
            info.extra_consumption = __parse_status_value(value)
        elif key == LAST_UPDATE:
            info.last_update = datetime.strptime(value, "%B %d,%Y  %H:%M")

    return info


def parse_accounts(content: Content) -> list[Account]:

    accounts: list[Account] = []

    account_options_node = parse_content(content).find("select", id="changnumber")
    if account_options_node is None or isinstance(
        account_options_node, NavigableString
    ):
        return []

    account_options = account_options_node.find_all("option")

    for account_option in account_options:
        account = Account()
        account.phone = account_option.attrs["value"]
        account.internet = account_option.attrs["value2"]

        accounts.append(account)

    return accounts


def parse_bills(content: Content) -> BillInfo:
    
    bill_info = BillInfo()

    bill_outstanding_section: Optional[Tag | NavigableString] = parse_content(
        content
    ).find(class_="BillOutstandingSection1")

    if bill_outstanding_section is not None:
        tag:Tag = bill_outstanding_section.find("span") # type: ignore
        bill_outstanding_val = tag.get_text(strip=True)

        bill_info.total_outstanding = BillAmount.parse(bill_outstanding_val)
    else:
        bill_info.total_outstanding = BillAmount()

    logging.debug(f"outstanding {bill_info.total_outstanding}")

    bill_table: Tag = parse_content(content).find("table", class_="BillTable") # type: ignore
    bill_rows: list[Tag] = bill_table.find_all("tr")

    for row in bill_rows:
        logging.debug(f"################################")
        bill = __parse_bill(row)

        if bill is None:
            continue

        bill_info.bills.append(bill)

    logging.debug(f"################################")

    return bill_info


def parse_error_message(content: Content):

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
    err_msg = err_msg.split('"')[0]

    return err_msg
