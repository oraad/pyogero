# Changelog

## 0.8.1

- Revert conflicting dependencies

## 0.8.0

- Update dependecies
- Add Ogero and RapidSSL intermediate certificate for verification

## 0.7.0

- Fix dependency version to support home-assistant

## 0.6.0

- Add timezone info to last_update

## 0.5.1

- Fix tests pyogero import

## 0.5.0

- Refactor `ogero` module into `pyogero`

## 0.4.0

- Downgrade `aiohttp` to >=3.8.5
- Remove support for Python 3.8 and 3.9

## 0.3.0

- Update `requests` to 2.31.0
- Update `beautifulsoup4` to 4.12.2
- Update `aiohttp` to 3.9.1
- Update `pydantic` to 1.10.13
- Update dev-dependency `pytest` to 7.4.3
- Update dev-dependency `black` to 22.12.0
- Update dev-dependency `requests-mock` to 1.11.0
- Add support for Python 3.11

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
