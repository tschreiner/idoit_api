from idoit_api_client import API, Constants
from idoit_api_client.cmdbobjecttypecategories import CMDBObjectTypeCategories
from idoit_api_client.cmdbobjecttypes import CMDBObjectTypes
from tests.test_idoit_api_client import BaseTest

class TestClassIdoitAPIClientCMDBObjectTypeCategoriesCMDBObjectTypeCategories(BaseTest):
    _instance = None
    _object_type_ids = []
    _object_type_consts = []

    def _set_up(self) -> None:
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

        self._instance = CMDBObjectTypeCategories(self._api)

        cmdb_object_types = CMDBObjectTypes(self._api)
        object_types = cmdb_object_types.read()

        for object_type in object_types:
            self._object_type_ids.append(int(object_type["id"]))
            self._object_type_consts.append(object_type["const"])

    def test_constructor(self):
        """Test constructor."""
        self._set_up()
        assert isinstance(self._instance, CMDBObjectTypeCategories)

    def test_read_by_identifier(self):
        """Test read by identifier."""
        self._set_up()

        categories = []
        
        for object_type_id in self._object_type_ids:
            categories.append(self._instance.read_by_id(object_type_id))

        self._check_assigned_categories(categories)

    def test_read_by_constant(self):
        """Test read by constant."""
        self._set_up()

        categories = []
        
        for object_type_const in self._object_type_consts:
            categories.append(self._instance.read_by_const(object_type_const))

        self._check_assigned_categories(categories)        

    def test_batch_read_by_identifier(self):
        """Test batch read by identifier."""
        self._set_up()
        
        batch_result = self._instance.batch_read_by_id(self._object_type_ids)

        assert isinstance(batch_result, list)
        assert len(batch_result) > 0

        for categories in batch_result:
            self._check_assigned_categories(categories)

    def test_batch_read_by_constant(self):
        """Test batch read by constant."""
        self._set_up()
        
        batch_result = self._instance.batch_read_by_const(self._object_type_consts)

        assert isinstance(batch_result, list)
        assert len(batch_result) > 0

        for categories in batch_result:
            self._check_assigned_categories(categories)

    def _check_assigned_categories(self, categories):
        """Validate assigned categories.

        :param categories: List of categories."""
        assert isinstance(categories, dict)

        for key, category in categories.items():
            assert isinstance(category, list)
            assert len(category) > 0