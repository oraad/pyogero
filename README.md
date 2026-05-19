# pyOgero: Ogero API Python module

[![PyPI Latest Release](https://img.shields.io/pypi/v/pyogero)](https://pypi.org/project/pyogero/)
[![Package Status](https://img.shields.io/pypi/status/pyogero)](https://pypi.org/project/pyogero/)
[![GitHub branch checks state](https://img.shields.io/github/checks-status/oraad/pyogero/main)](https://github.com/oraad/pyogero/)
[![License](https://img.shields.io/pypi/l/pyogero)](https://github.com/oraad/pyogero/blob/main/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)

Ogero does not currently provide a rest api to access it services,
therefore this module web scrap the mobile version of the pages to collect data.

## Async client

The async client (`pyogero.asyncio.Ogero`) requires an injected `aiohttp.ClientSession` (for example from Home Assistant `async_get_clientsession(hass)`):

```python
import aiohttp
from pyogero.asyncio import Ogero

async with aiohttp.ClientSession() as session:
    client = Ogero("user", "pass", session=session)
    await client.login()
```

## Home Assistant compatibility

Runtime dependency versions are capped at the versions used by [Home Assistant 2026.3.2](https://github.com/home-assistant/core/blob/2026.3.2/homeassistant/package_constraints.txt) (`requests`, `aiohttp`, `beautifulsoup4`, `pydantic`). To install exact pins in a virtual environment:

```bash
pip install -e . -c constraints-home-assistant-2026.3.2.txt
```

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependencies and a PEP 621 `pyproject.toml` for package metadata. Python **3.14** is used for CI and local development (see `.python-version`).

```bash
uv sync --group dev
uv run pytest tests/ -m "not integration"
uv run ruff check .
uv run ruff format .
```

To match Home Assistant pins after syncing dev dependencies:

```bash
uv sync --group dev
uv pip install -c constraints-home-assistant-2026.3.2.txt -e .
```

Build release artifacts with `uv run python -m build` (requires dev dependencies).

## Releasing

1. Bump `version` in `pyproject.toml` and document changes in `CHANGELOG.md`.
2. Merge to `main`. CI runs on push; the Release workflow then runs tests and creates tag `vX.Y.Z` if that tag does not exist yet.
3. Pushing the new tag triggers the publish job (GitHub release + PyPI). Re-pushing `main` without a version bump does not re-release because the tag already exists.
4. You can also run the **Release** workflow manually via `workflow_dispatch` to re-run pre-release checks.

### PyPI publishing

CI publishes with [trusted publishing](https://docs.pypi.org/trusted-publishers/) (OIDC) when the PyPI project is linked to this GitHub repository. The workflow also supports `PYPI_TOKEN` in repository secrets as a fallback if trusted publishing is not configured yet.
