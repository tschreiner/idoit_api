#!/usr/bin/env python
"""Tests for `idoit_api_client` package."""

import pytest
from click.testing import CliRunner

import random
import string
#import datetime
#from dateutil.parser import parse as timeparse


from idoit_api_client import Constants, API
from idoit_api_client import cli
from idoit_api_client.cmdbobject import CMDBObject
from idoit_api_client.cmdbobjects import CMDBObjects
from idoit_api_client.cmdbcategory import CMDBCategory


from tests.constants import Category, ObjectType


class BaseTest:
    """Base test class."""
    _cmdb_object = None
    _cmdb_category = None
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q'
    }
    _api = None
    _conditions = [
        1,  # Unfinished
        2,  # Normal
        3,  # Archived
        4,  # Deleted
        6,  # Template
        7  # Mass change template
    ]

    def _set_up(self) -> None:
        """Constructor."""
        api = API(self.config)
        #self._instance = CMDBCategory(api)
        config = {
            Constants.URL: "https://demo.i-doit.com/src/jsonrpc.php",
            Constants.KEY: "c1ia5q",
            Constants.USERNAME: "admin",
            Constants.PASSWORD: "admin",
        }
        self._config = config
        self._api = API(config)

    def _is_id(self, id):
        """Check if id is a valid id."""
        return isinstance(id, int) and id > 0

    def _is_id_as_string(self, value):
        """Check if id is a valid id."""
        assert isinstance(value, str)
        id = int(value)
        assert id > 0
    
    def _generate_random_string(self):
        """Generate random string."""
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

    def _create_server(self):
        cmdb_object = self._use_cmdb_object()
        result = cmdb_object.create(ObjectType.SERVER, self._generate_random_string())

        return result

    def _generate_description(self):
        """Generate longer description text."""
        description_text = f"This is a test object created by the idoit_api_client test suite. "
        return description_text

    def _use_cmdb_category(self):
        if self._api is None:
            self._set_up()

        if self._cmdb_category is None:
            self._cmdb_category = CMDBCategory(self._api)

        return self._cmdb_category

    def _use_cmdb_object(self):
        """Use CMDBObject."""
        api = API(self.config)
        api.connect()
        api.login()
        cmdb_object = CMDBObject(api)
        return cmdb_object

    def _use_cmdb_objects(self):
        """Use CMDBObjects."""
        api = API(self.config)
        api.connect()
        api.login()
        cmdb_objects = CMDBObjects(api)
        return cmdb_objects

    def _is_id(self, id):
        """Check if id is a valid id."""
        return isinstance(id, int) and id > 0

    def _is_normal(self, object_id):
        """Check if object is normal."""
        cmdb_object = self._use_cmdb_object()
        object_data = cmdb_object.read(object_id)
        assert isinstance(object_data, dict)
        assert "status" in object_data
        assert 2 == int(object_data["status"])

    def _is_archived(self, object_id):
        """Check if object is archived."""
        cmdb_object = self._use_cmdb_object()
        object_data = cmdb_object.read(object_id)
        assert isinstance(object_data, dict)
        assert "status" in object_data
        assert 3 == int(object_data["status"])

    def _is_deleted(self, object_id):
        """Check if object is archived."""
        cmdb_object = self._use_cmdb_object()
        object_data = cmdb_object.read(object_id)
        assert isinstance(object_data, dict)
        assert "status" in object_data
        assert 4 == int(object_data["status"])

    def _is_purged(self, object_id):
        """Check if object is purged."""
        cmdb_object = self._use_cmdb_object()
        object_data = cmdb_object.read(object_id)
        assert len(object_data) == 0

    def _is_template(self, object_id):
        """Check if object is template."""
        cmdb_object = self._use_cmdb_object()
        object_data = cmdb_object.read(object_id)
        assert isinstance(object_data, dict)
        assert "status" in object_data
        assert 6 == int(object_data["status"])

    def _is_mass_change_template(self, object_id):
        """Check if object is mass change template."""
        cmdb_object = self._use_cmdb_object()
        object_data = cmdb_object.read(object_id)
        assert isinstance(object_data, dict)
        assert "status" in object_data
        assert 7 == int(object_data["status"])

    def _generate_ipv4_address(self):
        """Generate random IPv4 address."""
        return ".".join(map(str, (random.randint(0, 255) for _ in range(4))))

    def _get_ipv4_net(self):
        """Find object "Global v4"""
        cmdb_objects = self._use_cmdb_objects()
        global_v4_net = cmdb_objects.get_id("Global v4", ObjectType.LAYER3_NET)
        return global_v4_net

    def _is_time(self, time):
        timestamp = timeparse.strftime('%s')

    def _is_one_object(self, object):
        required_keys = [
            'id',
            'title',
            'sysid',
            'objecttype',
            'created',
            'type_title',
            'type_icon',
            'status',
            'cmdb_status',
            'cmdb_status_title',
            'image'
        ]

        optional_keys = [
            'updated'
        ]

        keys = required_keys + optional_keys

        for key in object.keys():
            assert key in keys

        for key in required_keys:
            assert key in object.keys()

        assert isinstance(object['id'], int)
        self._is_id(object['id'])

        assert isinstance(object['title'], str)

        assert isinstance(object['sysid'], str)

        assert isinstance(object['objecttype'], int)
        assert self._is_id(object['objecttype'])

        assert isinstance(object['type_title'], str)

        assert isinstance(object['type_icon'], str)

        assert isinstance(object['status'], int)
        self._is_id(object['status'])
        assert object['status'] in self._conditions

        assert isinstance(object['created'], str)
        #self._is_time(object['created'])

        if "updated" in object.keys():
            assert isinstance(object['updated'], str)
            #self._is_time(object['updated'])

        assert isinstance(object['cmdb_status'], int)
        self._is_id(object['cmdb_status'])

        assert isinstance(object['cmdb_status_title'], str)

        assert isinstance(object['image'], str)

class APITest(BaseTest):
    """Test API."""
    def test_constructor(self):
        """Test constructor."""
        config = {
            Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
            Constants.KEY: 'c1ia5q'
        }
        api = API(config)
        assert isinstance(api, API)

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
