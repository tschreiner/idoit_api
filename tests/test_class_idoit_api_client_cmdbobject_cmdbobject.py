from idoit_api_client import Constants, API
from idoit_api_client.cmdbobject import CMDBObject
from idoit_api_client.cmdbobjecttypes import CMDBObjectTypes
from tests.test_idoit_api_client import BaseTest

class TestClassIdoitAPIClientCMDBObjectCMDBObject(BaseTest):
    """Test class idoit_api_client.cmdbobject.CMDBObject"""
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }


    def test_constructor(self):
        """Test constructor."""
        api = API(self.config)
        cmdb_object = CMDBObject(api)
        assert isinstance(cmdb_object, CMDBObject)

    def test_create_object_for_every_type(self):
        """Test create object for every type."""
        api = API(self.config)
        api.connect()
        api.login()

        object_types = CMDBObjectTypes(api)
        object_types_result = object_types.read()
        print("debug: object_types_result = {}".format(object_types_result))
        object_type_constants = [object_type['const'] for object_type in object_types_result]
        print("debug: object_type_constants = {}".format(object_type_constants))
        cmdb_object = CMDBObject(api)
        for object_type_constant in object_type_constants:
            print("debug: object_type_constant = {}".format(object_type_constant))
            object_id = cmdb_object.create(object_type_constant, self._generate_random_string())
            assert object_id is not None
            print("debug: object_id = {}".format(object_id))
        api.logout()
