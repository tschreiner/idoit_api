from idoit_api_client import Constants, API
from idoit_api_client.cmdbcategory import CMDBCategory
from idoit_api_client.cmdbobject import CMDBObject

from tests.constants import Category, ObjectType

import string
import random


class TestClassIdoitAPIClientCMDBCategory:
    """Test class idoit_api_client.cmdbcategory.CMDBCategory"""

    config = {
        Constants.URL: "https://demo.i-doit.com/src/jsonrpc.php",
        Constants.KEY: "c1ia5q",
        Constants.USERNAME: "admin",
        Constants.PASSWORD: "admin",
    }

    """Base test class."""
    _config = None
    _api = None
    cmdb_object = None
    cmdb_category = None

    def use_cmdb_object(self):
        if self.cmdb_object is None:
            self.cmdb_object = CMDBObject(self._api)

        return self.cmdb_object

    def _set_up(self) -> None:
        """Constructor."""
        api = API(self.config)
        self._instance = CMDBCategory(api)
        config = {
            Constants.URL: "https://demo.i-doit.com/src/jsonrpc.php",
            Constants.KEY: "c1ia5q",
            Constants.USERNAME: "admin",
            Constants.PASSWORD: "admin",
        }
        self._config = config
        self._api = API(config)

    def _generate_random_string(self):
        """Generate random string."""
        return "".join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(10)
        )

    def _use_cmdb_object(self):
        if self._api is None:
            self._set_up()

        if self.cmdb_object is None:
            self.cmdb_object = CMDBObject(self._api)

        return self.cmdb_object

    def _use_cmdb_category(self):
        if self._api is None:
            self._set_up()

        if self.cmdb_category is None:
            self.cmdb_category = CMDBCategory(self._api)

        return self.cmdb_category

    def _create_server(self):
        cmdb_object = self._use_cmdb_object()
        result = cmdb_object.create(ObjectType.SERVER, self._generate_random_string())

        return result

    def _is_id(self, value):
        assert isinstance(value, int)
        assert value > 0

    def test_constructor(self):
        """Test constructor."""
        api = API(self.config)
        cmdb_object_types = CMDBCategory(api)
        assert isinstance(cmdb_object_types, CMDBCategory)

    def test_save_new_entry_in_single_value_category(self):
        """Test save new entry in single value category."""
        object_id = self._create_server()

        attributes = {
            "manufacturer": self._generate_random_string(),
            "title": self._generate_random_string(),
        }

        cmdb_category = self._use_cmdb_category()
        entry_id = cmdb_category.save(object_id, Category.CATG__MODEL, attributes)

        assert isinstance(entry_id, int)
        self._is_id(entry_id)

        entries = cmdb_category.read(object_id, Category.CATG__MODEL)

        assert isinstance(entries, list)
        assert len(entries) == 1
        assert entries[0] is not None

        entry = entries[0]

        # Check both dialog+ attributes
        for attribute, value in attributes.items():
            # assert entry in attribute
            assert isinstance(entry[attribute], dict)
            assert "title" in entry[attribute]
            assert value == entry[attribute]["title"]

    def test_update(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.update()

    def test_archive(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.archive()

    def test_delete(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.delete()

    def test_purge(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.purge()

    def test_recycle(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.recycle()

    def test_quick_purge(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.quick_purge()

    def test_batch_create(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.batch_create()

    def test_batch_read(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.batch_read()

    def test_batch_update(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.batch_update()

    def test_clear(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.clear()