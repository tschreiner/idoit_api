from random import random

from attr import attr
from idoit_api_client import Constants, API
from idoit_api_client.cmdbcategoryinfo import CMDBCategoryInfo
from idoit_api_client.cmdbobject import CMDBObject
from idoit_api_client.cmdbobjecttypes import CMDBObjectTypes
from tests.test_idoit_api_client import BaseTest
from tests.constants import Category, ObjectType

import random

class TestClassIdoitAPIClientCMDBCategoryInfoCMDBCategoryInfo(BaseTest):
    """Test class idoit_api_client.cmdbcategoryinfo.CMDBCategoryInfo"""

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
    _instance = None
    _categories = []

    def _set_up(self) -> None:
        """Constructor."""
        api = API(self.config)
        self._instance = CMDBCategoryInfo(api)
        config = {
            Constants.URL: "https://demo.i-doit.com/src/jsonrpc.php",
            Constants.KEY: "c1ia5q",
            Constants.USERNAME: "admin",
            Constants.PASSWORD: "admin",
        }
        self._config = config
        self._api = API(config)

        self._categories = [
            Category.CATG__GLOBAL,
            Category.CATG__IP,
            Category.CATS__PERSON_MASTER
        ]

    def test_read(self):
        """Test read."""
        self._set_up()
        for category_const in self._categories:
            result = self._instance.read(category_const)
            
            assert isinstance(result, dict)
            assert len(result) > 0

            self._is_category_info(result)

    def _is_attribute_info(self, attribute):
        # "title": 
        assert "title" in attribute
        assert isinstance(attribute["title"], str)
        assert len(attribute["title"]) > 0

        # "info":
        assert "info" in attribute
        assert isinstance(attribute["info"], dict)
        # info.primary_field is optional
        if "primary_field" in attribute["info"]:
            assert isinstance(attribute["info"]["primary_field"], bool)

        assert "type" in attribute["info"]
        assert isinstance(attribute["info"]["type"], str)
        assert len(attribute["info"]["type"]) > 0

        # "info.backward" is optional:
        if "backward" in attribute["info"]:
            assert isinstance(attribute["info"]["backward"], bool)

        assert "title" in attribute["info"]
        assert isinstance(attribute["info"]["title"], str)
        assert len(attribute["info"]["title"]) > 0

        if "description" in attribute["info"]:
            assert isinstance(attribute["info"]["description"], str)
            assert len(attribute["info"]["description"]) > 0

        # data

        assert "data" in attribute
        assert isinstance(attribute["data"], dict)

        assert "type" in attribute["data"]
        assert isinstance(attribute["data"]["type"], str)
        assert len(attribute["data"]["type"]) > 0

        # "data.readonly" is optional
        if "readonly" in attribute["data"]:
            assert isinstance(attribute["data"]["readonly"], bool)

        assert "index" in attribute["data"]
        assert isinstance(attribute["data"]["index"], bool)

        if "field" in attribute["data"]:
            assert isinstance(attribute["data"]["field"], str)
            assert len(attribute["data"]["field"]) > 0

        if "table_alias" in attribute["data"]:
            assert isinstance(attribute["data"]["table_alias"], str)
            assert len(attribute["data"]["table_alias"]) > 0

        assert "ui" in attribute
        assert isinstance(attribute["ui"], dict)

        assert "type" in attribute["ui"]
        assert isinstance(attribute["ui"]["type"], str)
        assert len(attribute["ui"]["type"]) > 0

        if "params" in attribute["ui"]:
            assert isinstance(attribute["ui"]["params"], dict)

        if "id" in attribute["ui"]:
            assert isinstance(attribute["ui"]["id"], str)

        assert "check" in attribute
        assert isinstance(attribute["check"], dict)

        assert "mandatory" in attribute["check"]

        if attribute["check"]["mandatory"] is not None:
            assert isinstance(attribute["check"]["mandatory"], bool)

        # continue from https://github.com/i-doit/api-client-php/blob/8c1fe9222b1cff67c7501dbe60bcf44bead3044a/tests/Idoit/APIClient/CMDBCategoryInfoTest.php#L237

    def test_batch_read(self):
        self._set_up()
        result = self._instance.batch_read(self._categories)
        assert isinstance(result, list)
        assert len(result) == len(self._categories)

        for category_info in result:
            assert isinstance(category_info, dict)
            assert len(category_info) > 0
            self._is_category_info(category_info)

    def test_read_all(self):
        self._set_up()
        result = self._instance.read_all()

        assert isinstance(result, dict)
        assert len(result) != 0

        for category_const, category_info in result.items():
            if isinstance(category_const, str) and isinstance(category_info, dict):
                self._is_category_info(category_info)

    def _is_category_info(self, category):
        for attribute_title, attribute in category.items():
            assert isinstance(attribute_title, str)
            assert len(attribute) > 0

            assert isinstance(attribute, dict)
            self._is_attribute_info(attribute)