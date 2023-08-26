# Changelog

## 0.3.0

- Update minimum python to 3.10
- Upgrade `requests` to 2.31.0
- Upgrade `beautifulsoup4` to 4.12.2
- Upgrade `aiohttp` to 3.8.5
- Upgrade `pydantic` to 1.10.12
- Fix typing issues

## 0.2.0

- Upgrade `aiohttp` to 3.8.3
- Fix `get_bill_info` method to support cases with no outstanding bill
- Added `BillAmount` class to parse bill amount

## 0.1.0

- Added `login` method
- Added `get_accounts` method
- Added `get_bill_info` method
- Added `get_consumption_info` method
- Added `asyncio` submodule
