#!/usr/bin/env python
"""Tests for `idoit_api_client` package."""

import pytest
from click.testing import CliRunner

from idoit_api_client import Constants, API
from idoit_api_client import cli

def test_constructor():
    """Test constructor."""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q'
    }
    api = API(config)
    assert isinstance(api, API)
