from idoit_api_client import Constants, API
from idoit_api_client.cmdbobjecttypes import CMDBObjectTypes

from tests.test_idoit_api_client import BaseTest
from tests.constants import Category, ObjectType


class TestClassIdoitAPIClientCMDBObjectCMDBObjectTypes(BaseTest):
    """Test class idoit_api_client.cmdbobject.CMDBObjectTypes"""

    config = {
        Constants.URL: "https://demo.i-doit.com/src/jsonrpc.php",
        Constants.KEY: "c1ia5q",
        Constants.USERNAME: "admin",
        Constants.PASSWORD: "admin",
    }

    def _setUp(self) -> None:
        """Constructor."""
        api = API(self.config)
        self._instance = CMDBObjectTypes(api)

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

    def test_read_one(self):
        self._setUp()
        result = self._instance.read_one(ObjectType.SERVER)
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_batch_read(self):
        self._setUp()
        result = self._instance.batch_read(
            [ObjectType.SERVER, ObjectType.VIRTUAL_SERVER]
        )
        assert isinstance(result, list)
        assert len(result) > 0

    def test_read_by_title(self):
        self._setUp()
        result = self._instance.read_by_title("LC__CMDB__OBJTYPE__SERVER")

        assert isinstance(result, dict)
        assert len(result) > 0
