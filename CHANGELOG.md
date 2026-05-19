# Changelog

## Unreleased

- Development tooling switched from Pipenv to [uv](https://docs.astral.sh/uv/) (`uv.lock`, `[dependency-groups]` in `pyproject.toml`).
- CI and devcontainer use Python 3.14.
- GitHub Actions modernized: pinned action SHAs, composite `setup-uv`, unified `ci.yml` and `release.yml` (auto-tag on `main` when missing, publish on `v*` tag push).

## 0.13.0

- Add PEP 561 `py.typed` marker for type checkers.
- **Breaking:** `pyogero.asyncio.Ogero` requires an injected `aiohttp.ClientSession`; it no longer creates its own session. Pass `async with aiohttp.ClientSession() as session:` (or Home Assistant `async_get_clientsession(hass)`).

## 0.12.0

- Development tooling switched from Poetry to Pipenv (`Pipfile`, committed `Pipfile.lock`, PEP 621 `pyproject.toml`, `python -m build` for releases).
- Fix async client reading the HTTP response body twice (empty parse after auth check).
- Add shared `_client` module for sync/async orchestration.
- Raise `OgeroCommunicationError` for network and HTTP error responses.
- Raise `OgeroParseError` when dashboard or bill HTML cannot be parsed.
- Raise `AuthenticationException` when re-login retries are exhausted (instead of returning `None`).
- Expand unit tests for `_http`, parsers, communication errors, and async body-read regression.
- Export `OgeroCommunicationError`, `OgeroParseError`, and bill types from `pyogero.asyncio`.

## 0.11.0

- Shared HTTP helpers, dataclass types, and structured exceptions.
- Refactored sync and async clients.
