from idoit_api_client import API, Constants
from idoit_api_client.cmdbobjects import CMDBObjects
from tests.constants import ObjectType
from tests.test_idoit_api_client import BaseTest


class TestClassIdoitAPIClientCMDBObjectsCMDBObjects(BaseTest):
    """Test class idoit_api_client.cmdbobjects.CMDBObjects"""

    def _set_up(self):
        config = {
            Constants.URL: "https://demo.i-doit.com/src/jsonrpc.php",
            Constants.KEY: "c1ia5q",
            Constants.USERNAME: "admin",
            Constants.PASSWORD: "admin",
        }
        self.api = API(config)
        self._instance = CMDBObjects(self.api)

    def test_constructor(self):
        """Test constructor."""
        api = API(self.config)
        cmdb_object = CMDBObjects(api)
        assert isinstance(cmdb_object, CMDBObjects)

    def test_create(self):
        self._set_up()
        object_ids = self._instance.create(
            [
                {"type": ObjectType.SERVER, "title": "Server No. One"},
                {"type": ObjectType.SERVER, "title": "Server No. Two"},
                {"type": ObjectType.SERVER, "title": "Server No. Three"},
            ]
        )

        assert isinstance(object_ids, list)
        assert len(object_ids) == 3

        for object_id in object_ids:
            assert isinstance(object_id, int)
            assert self._is_id(object_id)

    def test_read(self):
        self._set_up()
        objects = self._instance.read()

        assert isinstance(objects, list)
        assert len(objects) > 0

        for object in objects:
            self._is_object(object)

    def test_read_by_type(self):
        self._set_up()
        objects = self._instance.read_by_type(ObjectType.PERSON)

        assert isinstance(objects, list)
        assert len(objects) > 0

        for object in objects:
            self._is_object(object)
