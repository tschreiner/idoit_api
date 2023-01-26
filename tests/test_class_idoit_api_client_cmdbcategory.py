from idoit_api_client import Constants, API
from idoit_api_client.cmdbcategory import CMDBCategory
from idoit_api_client.cmdbobject import CMDBObject

from tests.constants import Category, ObjectType

import string
import random

from tests.test_idoit_api_client import BaseTest


class TestClassIdoitAPIClientCMDBCategory(BaseTest):
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

    def test_save_new_entry_in_multi_value_category(self):
        object_id = self._create_server()

        attributes = {
            'net': self._get_ipv4_net(),
            'active': 0,
            'primary': 0,
            'net_type': 1,
            'ipv4_assignment': 2,
            'ipv4_address': self._generate_ipv4_address(),
            'description': self._generate_description()
        }

        cmdb_category = self._use_cmdb_category()
        entry_id = cmdb_category.save(object_id, Category.CATG__IP, attributes)

        assert isinstance(entry_id, int)
        self._is_id(entry_id)

        entries = cmdb_category.read(object_id, Category.CATG__IP)

        assert isinstance(entries, list)
        assert len(entries) == 1
        assert entries[0] is not None

        entry = entries[0]

        for attribute in attributes:
            assert attribute in entry

    def test_save_existing_entry_in_single_value_category(self):
        object_id = self._create_server()

        # original entry:

        attributes = {
            "manufacturer": self._generate_random_string(),
            "title": self._generate_random_string()
        }

        cmdb_category = self._use_cmdb_category()
        entry_id = cmdb_category.save(object_id, Category.CATG__MODEL, attributes)

        assert isinstance(entry_id, int)
        self._is_id(entry_id)

        entries = cmdb_category.read(object_id, Category.CATG__MODEL)

        assert isinstance(entries, list)
        assert len(entries) == 1
        assert 0 < len(entries)

        entry = entries[0]

        assert "id" in entry
        id = int(entry["id"])
        assert entry_id == id

        for attribute, value in attributes.items():
            assert attribute in entry
            assert isinstance(entry[attribute], dict)
            assert "title" in entry[attribute]
            assert value == entry[attribute]["title"]


        # updated entry:

        new_attributes = {
            "manufacturer": self._generate_random_string(),
            "title": self._generate_random_string()
        }

        new_entry_id = cmdb_category.save(object_id, Category.CATG__MODEL, new_attributes)

        assert isinstance(new_entry_id, int)
        self._is_id(new_entry_id)

        entries = cmdb_category.read(object_id, Category.CATG__MODEL)

        assert isinstance(entries, list)
        assert len(entries) == 1
        assert 0 < len(entries)

        new_entry = entries[0]

        assert "id" in new_entry
        id = int(new_entry["id"])
        assert new_entry_id == id
        assert new_entry_id == entry_id

        for attribute, value in new_attributes.items():
            assert attribute in new_entry
            assert isinstance(new_entry[attribute], dict)
            assert "title" in new_entry[attribute]
            assert value == new_entry[attribute]["title"]

        # Verify that further tests really pass:
        for attribute in attributes.keys():
            assert entry[attribute] != new_entry[attribute]

    def test_update(self):
        object_id = self._create_server()

        cmdb_category = self._use_cmdb_category()
        itself = cmdb_category.update(object_id, Category.CATG__GLOBAL, { "cmdb_status": 10 })

        assert isinstance(itself, CMDBCategory)

        # Test multi-value category:
        amount = 3
        entry_ids = []

        for idx, x in enumerate(range(amount)):
            entry_ids.append(self._add_ipv4(object_id))

        for idx, x in enumerate(range(amount)):
            cmdb_category.update(object_id, Category.CATG__IP, { "ipv4_address": self._generate_ipv4_address() }, entry_ids[idx])
            assert isinstance(itself, CMDBCategory)

        cmdb_object = self._use_cmdb_object()
        result = cmdb_object.update(object_id, {"title": "Anne Admin"})
        assert isinstance(result, CMDBObject)

    def test_archive(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.archive()

    def test_delete(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.delete()

    def test_create(self):
        object_id = self._create_server()
        cmdb_category = self._use_cmdb_category()
        
        entry_id = cmdb_category.create(object_id, Category.CATG__IP, {
            "net": self._get_ipv4_net(),
            "active": 0,
            "primary": 0,
            "net_type": 1,
            "ipv4_assignment": 2,
            "ipv4_address": self._generate_ipv4_address(),
            "description": self._generate_description()
        })
        
        assert entry_id >= 1    

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
        object_id1 = self._create_server()
        object_id2 = self._create_server()

        cmdb_category = self._use_cmdb_category()

        # Single-valued category:
        result = cmdb_category.batch_create(
            [object_id1, object_id2],
            Category.CATG__MODEL,
            [
                {
                    'manufacturer': self._generate_random_string(),
                    'title': self._generate_random_string(),
                    # 'serial': self._generate_random_string(), ## TODO: Create issue for this. Cannot create multiple entries with same serial.
                    'description': self._generate_description()
                }
            ]
        )

        assert isinstance(result, list)
        assert len(result) == 2

        for entry_id in result:
            assert isinstance(entry_id, int)
            assert entry_id > 0

        # Multi-valued category:
        result = cmdb_category.batch_create(
            [object_id1, object_id2],
            Category.CATG__IP,
            [
                {
                    'net': self._get_ipv4_net(),
                    'active': 1,
                    'primary': 1,
                    'net_type': 1,
                    'ipv4_assignment': 2,
                    'ipv4_address': self._generate_ipv4_address(),
                    'description': self._generate_description()
                },
                {
                    'net': self._get_ipv4_net(),
                    'active': 1,
                    'primary': 0,
                    'net_type': 1,
                    'ipv4_assignment': 2,
                    'ipv4_address': self._generate_ipv4_address(),
                    'description': self._generate_description()
                }
            ]
        )

        assert isinstance(result, list)
        assert len(result) == 4

        for entry_id in result:
            assert isinstance(entry_id, int)
            assert entry_id > 0

    def test_batch_read(self):
        object_id1 = self._create_server()
        object_id2 = self._create_server()
        self._add_ipv4(object_id1)
        self._add_ipv4(object_id2)
        self._define_model(object_id1)
        self._define_model(object_id2)
        
        cmdb_category = self._use_cmdb_category()
        batch_result = cmdb_category.batch_read([object_id1, object_id2], [Category.CATG__IP, Category.CATG__MODEL])

        assert isinstance(batch_result, list)
        assert len(batch_result) == 4

        if isinstance(batch_result, list):
            for result in batch_result:
                assert isinstance(result, list)
                assert len(result) > 0


    def test_batch_update(self):
        object_id1 = self._create_server()
        object_id2 = self._create_server()

        cmdb_category = self._use_cmdb_category()

        entry_ids = []

        entry_ids.append(self._define_model(object_id1))
        entry_ids.append(self._define_model(object_id2))

        itself = cmdb_category.batch_update(
            [object_id1, object_id2],
            Category.CATG__MODEL,
            {
                "manufacturer": self._generate_random_string(),
                "title": self._generate_random_string(),
                # "serial": self._generate_random_string(), #  TODO: Create issue for this - You cannot update different models with the same serial number
                "description": self._generate_description()
            }
        )

        assert isinstance(itself, CMDBCategory)

    def test_clear(self):
        cmdb_category = self._use_cmdb_category()
        cmdb_category.clear()

    def test_create_archived_object(self):
        cmdb_object = self._use_cmdb_object()
        object_id = cmdb_object.create(ObjectType.SERVER, self._generate_random_string(), {"status": 3})
        self._is_id(object_id)
        self._is_archived(object_id)