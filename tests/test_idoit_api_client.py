#!/usr/bin/env python
"""Tests for `idoit_api_client` package."""

import pytest
from click.testing import CliRunner

import random
import string

from idoit_api_client import Constants, API
from idoit_api_client import cli

class BaseTest:
    """Base test class."""
    def _generate_random_string(self):
        """Generate random string."""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

class APITest(BaseTest):
    """Test API."""
    def test_constructor(self):
        """Test constructor."""
        config = {
            Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
            Constants.KEY: 'c1ia5q'
        }
        api = API(config)
        assert api is instanceof(API)

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

#def test_connect_no_url():
#def test_connect_no_key():
#def test_connect_no_username():
#def test_connect_no_password():

#def test_login_no_url():
#def test_login_no_key():
#def test_login_no_username():
#def test_login_no_password():

#def test_request_no_url():
#def test_request_no_key():
#def test_request_no_username():
#def test_request_no_password():

#def test_request_no_method():
#def test_request_no_params():

#def test_request_invalid_method():
#def test_request_invalid_params():

#def test_is_connected():
#def test_is_logged_in():

#def test_request_content():
#def test_request_invalid_content():



#def test _request():
#def test_raw_request():
#def test_batch_request():

def test_scenario():
    """Test a complete scenario."""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }
    api = API(config)
    api.connect()
    api.login()
    result = api.request('cmdb.category.read', {
        'objID': 1,
        'category': 'C__CATG__GLOBAL'
    })
    api.logout()
    assert result is not None

def test_batch_scenario():
    """Test a complete batch scenario."""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }
    api = API(config)
    api.connect()
    api.login()
    result = api.batch_request([
        {
            'method': 'cmdb.category.read',
            'params': {
                'objID': 1,
                'category': 'C__CATG__GLOBAL'
            }
        },
        {
            'method': 'cmdb.category.read',
            'params': {
                'objID': 1,
                'category': 'C__CATG__GLOBAL'
            }
        }
    ])
    api.logout()
    assert result is not None

def test_connect():
    """Test connect."""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q'
    }
    api = API(config)
    api.connect()
    assert api._resource is not None

def test_login():
    """Test login."""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }
    api = API(config)
    api.login()
    assert api.is_logged_in() is True

def test_request():
    """Test request."""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }
    api = API(config)
    api.login()
    result = api.request('cmdb.category.read', {
        'objID': 1,
        'category': 'C__CATG__GLOBAL'
    })
    assert result is not None

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
