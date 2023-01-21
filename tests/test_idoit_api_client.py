#!/usr/bin/env python
"""Tests for `idoit_api_client` package."""

import pytest
from click.testing import CliRunner

from idoit_api_client import Constants, API
from idoit_api_client import cli


@pytest.fixture
def response():
    """Sample pytest fixture.    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string

def test_api():
    """Test API."""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'ABC'
    }
    api = API(config)
    assert api is not None

def test_constants():
    """Test constants."""
    constants =  Constants
    assert constants.URL == 'url'
    assert constants.PORT == 'port'
    assert constants.PORT_MIN == 1
    assert constants.PORT_MAX == 65535
    assert constants.KEY == 'key'
    assert constants.USERNAME == 'username'
    assert constants.PASSWORD == 'password'
    assert constants.LANGUAGE == 'language'
    assert constants.PROXY == 'proxy'
    assert constants.PROXY_ACTIVE == 'active'
    assert constants.PROXY_TYPE == 'type'
    assert constants.PROXY_TYPE_HTTP == 'HTTP'
    assert constants.PROXY_TYPE_SOCKS5 == 'SOCKS5'
    assert constants.PROXY_HOST == 'host'
    assert constants.PROXY_PORT == 'port'
    assert constants.PROXY_USERNAME == 'username'
    assert constants.PROXY_PASSWORD == 'password'
    assert constants.BYPASS_SECURE_CONNECTION == 'bypassSecureConnection'
    assert constants.CURLPROTO_HTTP == 1
    assert constants.CURLPROTO_HTTPS == 2

def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'idoit_api_client.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output
