"""
Pytest configuration ensuring required Ape plugins are installed before tests run.
"""

import importlib.util

import pytest


REQUIRED_PLUGINS = ("ape_solidity",)


for plugin in REQUIRED_PLUGINS:
    if importlib.util.find_spec(plugin) is None:
        pytest.fail(
            f"Missing required Ape plugin '{plugin}'. "
            "Install dependencies via `pip install -r requirements.txt` "
            "or `ape plugins install solidity`."
        )
