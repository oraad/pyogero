"""Domain types for Ogero API responses."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import TYPE_CHECKING, TypedDict

from pydantic import BaseModel

if TYPE_CHECKING:
    from datetime import datetime

Content = bytes | str


@dataclass
class Account:
    """Phone and internet account identifiers."""

    phone: str = ""
    internet: str = ""

    def __str__(self) -> str:
        return f"DSL# {self.internet} | Phone# {self.phone}"

    def __repr__(self) -> str:
        return self.__str__()


class BillStatus(Enum):
    """Bill payment status."""

    UNKNOWN = 0
    PAID = 1
    UNPAID = 2


@dataclass
class BillAmount:
    """Monetary amount with currency."""

    amount: float = 0
    currency: str = "LBP"

    def __post_init__(self) -> None:
        if self.currency in ("L.L.", "LL", "L.L"):
            self.currency = "LBP"

    @staticmethod
    def parse(str_val: str) -> BillAmount:
        """Parse a string like ``1,234 L.L.`` into a BillAmount."""
        amount_str, currency = str_val.split(" ", 1)
        amount = float(amount_str.replace(",", ""))
        return BillAmount(amount=amount, currency=currency)

    def __str__(self) -> str:
        return f"{self.amount!s} {self.currency}"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class Bill:
    """A single bill row."""

    date: datetime
    amount: BillAmount
    status: BillStatus = BillStatus.UNKNOWN

    def __str__(self) -> str:
        if self.status == BillStatus.PAID:
            status = "paid"
        elif self.status == BillStatus.UNPAID:
            status = "not paid"
        else:
            status = "unknown"

        return f"Bill [{self.date.strftime('%b %Y')}], {self.amount}: {status}"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class BillInfo:
    """Outstanding balance and bill history."""

    total_outstanding: BillAmount
    bills: list[Bill] = field(default_factory=list)

    def __str__(self) -> str:
        return f"Total outstanding: {self.total_outstanding}"

    def __repr__(self) -> str:
        return self.__str__()


@dataclass
class ConsumptionInfo:
    """Internet consumption snapshot."""

    speed: str = ""
    quota: int = 0
    total_consumption: float = 0
    extra_consumption: float = 0
    last_update: datetime | None = None

    def __str__(self) -> str:
        return (
            f"Total Consumption: {self.total_consumption} GB; "
            f"Last update: {self.last_update}"
        )

    def __repr__(self) -> str:
        return self.__str__()


class ErrorResponseContent(TypedDict):
    code: int | str
    message: str


class ErrorResponse(TypedDict):
    error: ErrorResponseContent


class LoginResponse(TypedDict):
    SessionID: str


class ConfigUser(BaseModel):
    username: str
    password: str


class OgeroConfigFile(BaseModel):
    """Config file definition for integration tests."""

    users: list[ConfigUser] | None = None
