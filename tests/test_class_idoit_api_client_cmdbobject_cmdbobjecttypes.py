from idoit_api_client import Constants, API
from idoit_api_client.cmdbobjecttypes import CMDBObjectTypes

class TestClassIdoitAPIClientCMDBObjectCMDBObjectTypes:
    """Test class idoit_api_client.cmdbobject.CMDBObjectTypes"""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }

    _instance = None

    def test_constructor(self):
        """Test constructor."""
        api = API(self.config)
        cmdb_object_types = CMDBObjectTypes(api)
        assert isinstance(cmdb_object_types, CMDBObjectTypes)

    def test_read(self):
        """Test read."""
        api = API(self.config)
        api.connect()
        api.login()
        cmdb_object_types = CMDBObjectTypes(api)
        result = cmdb_object_types.read()

        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0
