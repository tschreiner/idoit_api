from idoit_api_client import Request

"""Requests for API namespace 'cmdb.object_type_categories'"""


class CMDBObjectTypeCategories(Request):
    """Requests for API namespace 'cmdb.object_type_categories'"""

    def read_by_id(self, object_type_id):
        """Fetches assigned categories for a specific object type by its identifier.

        :param object_type_id: Object type identifier

        :return: Array"""
        return self._api.request(
            "cmdb.object_type_categories.read", {"type": object_type_id}
        )

    def read_by_const(self, object_type_constant):
        """Fetches assigned categories for a specific object type by its constant.

        :param object_type_constant: Object type constant

        :return: Array"""
        return self._api.request(
            "cmdb.object_type_categories.read", {"type": object_type_constant}
        )

    def batch_read_by_id(self, object_type_ids):
        """Fetches assigned categories for one or more objects types at once identified by their identifiers.

        :param object_type_ids: List of object types identifiers as integers

        :return: Array"""
        requests = []

        for object_type_id in object_type_ids:
            request = {
                "method": "cmdb.object_type_categories.read",
                "params": {"type": object_type_id},
            }
            requests.append(request)

        return self._api.batch_request(requests)

    def batch_read_by_const(self, object_type_consts):
        """Fetches assigned categories for one or more objects types at once identified by their constants.

        :param object_type_consts: List of object types constants as strings

        :return: Array"""
        requests = []

        for object_type_const in object_type_consts:
            request = {
                "method": "cmdb.object_type_categories.read",
                "params": {"type": object_type_const},
            }
            requests.append(request)

        return self._api.batch_request(requests)
