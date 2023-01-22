from unicodedata import category
import pytest
from click.testing import CliRunner

from idoit_api_client.constants import Category, ObjectType

class TestClassIdoitApiClientConstantsCategory:
    """Test class idoit_api_client.Constants"""
    def test_constructor(self):
        """Test constructor."""
        category = Category()
        assert isinstance(category, Category)

    def test_constant_catg_global(self):
        """Test get_constants."""
        category = Category()
        assert category.CATG__GLOBAL == 'C__CATG__GLOBAL'

class TestClassIdoitApiClientConstantsObjectType:
    """Test class idoit_api_client.ObjectType:"""
    def test_constructor(self):
        """Test constructor."""
        object_type = ObjectType()
        assert isinstance(object_type, ObjectType)

    def test_constant_server(self):
        """Test get_constants."""
        object_type = ObjectType()
        assert object_type.SERVER == 'C__OBJTYPE__SERVER'

