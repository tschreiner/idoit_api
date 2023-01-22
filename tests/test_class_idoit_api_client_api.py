import pytest
from click.testing import CliRunner

from idoit_api_client import Constants, API

class TestClassIdoitAPIClientAPI:
    """Test class idoit_api_client.API"""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }

    def test_constructor(self):
        """Test constructor."""
        api = API(self.config)
        assert isinstance(api, API)

    def test_destructor(self):
        """Test destructor."""
        api = API(self.config)
        del api

    def test_is_connected(self):
        """Test is_connected."""
        api = API(self.config)
        assert api.is_connected() is False
        api.connect()
        assert api.is_connected() is True
        api.disconnect()
        assert api.is_connected() is False

    def test_is_logged_in(self):
        """Test login."""
        api = API(self.config)
        api.connect()
        result = api.login()
        assert api.is_logged_in() is True

    def test_is_logged_out(self):
        """Test logout."""
        api = API(self.config)
        api.connect()
        result = api.login()
        assert api.is_logged_in() is True
        api.logout()
        assert api.is_logged_in() is False

    def test_request(self):
        """Test request."""
        api = API(self.config)
        api.connect()
        api.login()
        result = api.request('cmdb.category.read', {
            'objID': 1,
            'category': 'C__CATG__GLOBAL'
        })
        assert type(result) is list

    def test_count_requests(self):
        """Test count_requests."""
        api = API(self.config)

        api.request('idoit.version')
        count = api.count_requests()
        assert type(count) is int
        assert count == 1

        api.request('idoit.version')
        count = api.count_requests()
        assert type(count) is int
        assert count == 2

    def test_batch_request(self):
        """Test batch_request."""
        api = API(self.config)
        object_id = 1
        result = api.batch_request([
            {
                'method': 'idoit.version'
            },
            {
                'method': 'cmdb.object.read',
                'params': {
                    'id': object_id
                }
            }
        ])
        assert type(result) is list
        assert len(result) == 2
        for result in result:
            assert type(result) is dict
            assert len(result) != 0

    """TODO: Implement remaining tests from https://github.com/i-doit/api-client-php/blob/main/tests/Idoit/APIClient/APITest.php"""
