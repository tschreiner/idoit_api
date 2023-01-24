from random import random
from idoit_api_client import Constants, API
from idoit_api_client.cmdbobject import CMDBObject
from idoit_api_client.cmdbobjecttypes import CMDBObjectTypes
from tests.test_idoit_api_client import BaseTest
from tests.constants import Category, ObjectType

import random

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

    def test_create(self):
        """Test create."""
        cmdb_object = self._use_cmdb_object()
        object_id = cmdb_object.create('C__OBJTYPE__SERVER', self._generate_random_string())
        assert isinstance(object_id, int)
        assert self._is_id(object_id)

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

    def test_create_with_more_attributes(self):
        """Test create with more attributes."""
        cmdb_object = self._use_cmdb_object()
        object_id = cmdb_object.create(
            ObjectType.SERVER,
            self._generate_random_string(),
            {
                'category': 'Test',
                'cmdb_status': 0,
                'description': self._generate_description(),
                'purporse': 'for reasons',
                'sysid': self._generate_random_string(),
            }
        )
        assert isinstance(object_id, int)
        assert self._is_id(object_id)

    def test_create_normal_object(self):
        cmdb_object = self._use_cmdb_object()
        object_id = cmdb_object.create(ObjectType.SERVER, self._generate_random_string(), {
            "status": 2
        })
        self._is_id(object_id)
        self._is_normal(object_id)

    def test_create_archived_object(self):
        cmdb_object = self._use_cmdb_object()
        object_id = cmdb_object.create(ObjectType.SERVER, self._generate_random_string(), {
            "status": 3
        })
        self._is_id(object_id)
        self._is_archived(object_id)

    def test_create_deleted_object(self):
        cmdb_object = self._use_cmdb_object()
        object_id = cmdb_object.create(ObjectType.SERVER, self._generate_random_string(), {
            "status": 4
        })
        self._is_id(object_id)
        self._is_deleted(object_id)

    def test_create_template(self):
        cmdb_object = self._use_cmdb_object()
        object_id = cmdb_object.create(ObjectType.SERVER, self._generate_random_string(), {
            "status": 6
        })
        self._is_id(object_id)
        self._is_template(object_id)

    def test_create_mass_change_template(self):
        cmdb_object = self._use_cmdb_object()
        object_id = cmdb_object.create(ObjectType.SERVER, self._generate_random_string(), {
            "status": 7
        })
        self._is_id(object_id)
        self._is_mass_change_template(object_id)

    def test_create_with_categories(self):
        cmdb_object = self._use_cmdb_object()

        categories = {
            Category.CATG__MODEL: [{
                "manufacturer": self._generate_random_string(),
                "title": self._generate_random_string()
            }],
            Category.CATG__IP: [
                {
                    "net": self._get_ipv4_net(),
                    "active": random.randint(0, 1),
                    "primary": 1,
                    "net_type": 1,
                    "ipv4_assignment": 2,
                    "ipv4_address": self._generate_ipv4_address(),
                    "description": self._generate_description()
                },
                {
                    "net": self._get_ipv4_net(),
                    "active": random.randint(0, 1),
                    "primary": 1,
                    "net_type": 1,
                    "ipv4_assignment": 2,
                    "ipv4_address": self._generate_ipv4_address(),
                    "description": self._generate_description()
                }
            ]
        }

        result = cmdb_object.create_with_categories(
            ObjectType.SERVER,
            self._generate_random_string(),
            categories
        )

        assert isinstance(result, dict)
        assert "id" in result
        assert self._is_id(result["id"])

        assert "categories" in result
        assert isinstance(result["categories"], dict)
        assert len(result["categories"]) == 2

        assert Category.CATG__MODEL in result["categories"]
        assert isinstance(result["categories"][Category.CATG__MODEL], list)
        assert len(result["categories"][Category.CATG__MODEL]) == 1
        assert result["categories"][Category.CATG__MODEL][0] is not None
        assert self._is_id(result["categories"][Category.CATG__MODEL][0])

        assert Category.CATG__IP in result["categories"]
        assert isinstance(result["categories"][Category.CATG__IP], list)
        assert len(result["categories"][Category.CATG__IP]) == 2
        assert result["categories"][Category.CATG__IP][0] is not None
        assert self._is_id(result["categories"][Category.CATG__IP][0])
        assert result["categories"][Category.CATG__IP][1] is not None
        assert self._is_id(result["categories"][Category.CATG__IP][1])

        """Verify entries"""

        object_id = result["id"]
        model_entry_id = result["categories"][Category.CATG__MODEL][0]
        first_ip_entry_id = result["categories"][Category.CATG__IP][0]
        second_ip_entry_id = result["categories"][Category.CATG__IP][1] # bug in original code: https://github.com/i-doit/api-client-php/blob/main/tests/Idoit/APIClient/CMDBObjectTest.php

        cmdb_category = self._use_cmdb_category()
        model = cmdb_category.read_one_by_id(object_id, Category.CATG__MODEL, model_entry_id)
        assert "id" in model.keys()
        self._is_id_as_string(model["id"])
        id = int(model["id"])
        assert id == model_entry_id

        cmdb_category = self._use_cmdb_category()
        first_ip_entry = cmdb_category.read_one_by_id(object_id, Category.CATG__IP, first_ip_entry_id)
        assert "id" in first_ip_entry.keys()
        self._is_id_as_string(first_ip_entry["id"])
        id = int(first_ip_entry["id"])
        assert id == first_ip_entry_id

        cmdb_category = self._use_cmdb_category()
        second_ip_entry = cmdb_category.read_one_by_id(object_id, Category.CATG__IP, second_ip_entry_id)
        assert "id" in second_ip_entry.keys()
        self._is_id_as_string(second_ip_entry["id"])
        id = int(second_ip_entry["id"])
        assert id == second_ip_entry_id

    def test_read(self):
        object_id = self._create_server()
        result = self._use_cmdb_object().read(object_id)
        assert isinstance(result, dict)
        self._is_one_object(result)

    def test_update(self):
        object_id = self._create_server()
        cmdb_object = self._use_cmdb_object()
        result = cmdb_object.update(object_id, {
            "title": "Anne Admin"
        })
        assert isinstance(result, CMDBObject)

    def test_load(self):
        object_id = self._create_server()
        cmdb_object = self._use_cmdb_object()
        result = cmdb_object.load(object_id)
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_read_all(self):
        # https://github.com/i-doit/api-client-php/blob/f3ec2be54943eb15e63cd1713a618c279253683a/tests/Idoit/APIClient/CMDBObjectTest.php#L370
        cmdb_objects = self._use_cmdb_objects()
        cmdb_objects.read([], 10, 0, 'id', CMDBObjects.SORT_DESCENDING)
        raise Exception("Not implemented")

    def test_read_all_from_non_existing_object():
        # https://github.com/i-doit/api-client-php/blob/f3ec2be54943eb15e63cd1713a618c279253683a/tests/Idoit/APIClient/CMDBObjectTest.php#L423
        raise Exception("Not Implemented")

    def test_upsert(self):
        # https://github.com/i-doit/api-client-php/blob/f3ec2be54943eb15e63cd1713a618c279253683a/tests/Idoit/APIClient/CMDBObjectTest.php#L432
        raise Exception("not implemented")
