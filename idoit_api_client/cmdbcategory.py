"""Requests for API namespace 'cmdb.category'"""

from idoit_api_client import Request

class CMDBCategory(Request):
    """CMDBCategories class for i-doit API client."""

    def save(self, object_id, category_constant, attributes, entry_id=None):
        """Create new or update existing category entry for a specific object.

        Suitable for single- and multi-value categories.

        :param object_id: Object identifier
        :param category_constant: Category constant
        :param attributes: Attributes as key-value pairs
        :param entry_id: Entry identifier (only needed for multi-valued categories)"""
        params = {
            "object": object_id,
            "data": attributes,
            "category": category_constant
        }

        if entry_id is not None:
            params["entry"] = entry_id

        result = self._api.request("cmdb.category.save", params)

        if "entry" not in result or not isinstance(result["entry"], int) or "success" not in result or not result["success"]:
            if "message" in result:
                raise Exception(f'Bad result: {result["message"]}')
            else:
                raise Exception("Bad result")

        return result["entry"]

    def create(self, object_id, category_const, attributes):
        """Create new category entry for a specific object.

        Suitable for multi-value categories only.

        :param object_id: Object identifier
        :param category_const: Category constant
        :param attributes: Attributes as key-value pairs

        :return: Entry identifier"""
        params = {
            "objID": object_id,
            "data": attributes,
            "category": category_const
        }

        result = self._api.request("cmdb.category.create", params)

        return self.require_success_for(result)

    def read(self, object_id, category_const, status=2):
        """Read one or more category entries for a specific object (works with both single- and multi-valued categories).

        :param object_id: Object identifier
        :param category_const: Category constant
        :param status: (Optional) Filter entries by status:
            2 = normal;
            3 = archived;
            4 = deleted;
            -1 = combination of all;
            defaults to: 2 = normal;
            note: a status != 2 is only suitable for multi-value categoriesd

        :return: Indexed array of result sets (for both single- and multi-valued categories)"""
        result = self._api.request("cmdb.category.read", {
            "objID": object_id,
            "category": category_const,
            "status": status
        })
        return result
