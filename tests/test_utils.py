"""test utils."""

import json
from pathlib import Path

import pytest

from pyogero.types import OgeroConfigFile


def configloader() -> OgeroConfigFile:
    """Load config."""
    user_path = Path("~/.config/ogero.json")
    for filename in [Path.expanduser(user_path), "ogero.json"]:
        filepath = Path(filename).resolve()
        if filepath.exists():
            try:
                with Path.open(filepath) as f:
                    return OgeroConfigFile.model_validate_json(f.read())
            except json.JSONDecodeError as json_error:
                pytest.exit(f"Failed to parse config file: {json_error}")
    return OgeroConfigFile()
