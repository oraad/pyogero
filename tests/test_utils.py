""" test utils """

import json
import os
from pathlib import Path

import pytest

from pyogero.types import OgeroConfigFile

def configloader() -> OgeroConfigFile:
    """ loads config """
    for filename in [ os.path.expanduser("~/.config/ogero.json"), "ogero.json" ]:
        filepath = Path(filename).resolve()
        print("filename", filepath)
        if filepath.exists():
            try:
                with open(filepath, 'r') as f:
                    return OgeroConfigFile.model_validate_json(f.read())
            except json.JSONDecodeError as json_error:
                pytest.exit(f"Failed to parse config file: {json_error}")
    return OgeroConfigFile()
