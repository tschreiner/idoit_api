"""Requests for API namespace 'cmdb.object_types"""

from idoit_api_client import API, Constants, Request

class CMDBObjectTypes(Request):
    """Requests for API namespace 'cmdb.object_types'"""

    def read(self):
        """Read object types.

        :return: Array of object types
        """
        return self._api.request("cmdb.object_types.read")

    def read_one(self, object_type):
        """Fetches information about an object type by its constant.

        :param object_type: Object type constant

        :return: Object type information
        """
        params = {
            "filter": {
                "id": object_type,
            },
            "countobjects": True
        }
        
        return self._api.request("cmdb.object_types.read", params)[-1]

    def batch_read(self, object_types):
        """Fetches information about multiple object types by their constants.

        :param object_types: Array of object type constants

        :return: Array of object type information
        """
        params = {
            "filter": {
                "ids": object_types,
            },
            "countobjects": True
        }
        
        return self._api.request("cmdb.object_types", params)

    def read_by_title(self, title):
        """Fetches information about an object type by its title (which could be a "language constant")

        :param title: Object title

        :return: Object type information
        """
        params = {
            "filter": {
                "title": title,
            },
            "countobjects": True
        }
        return self._api.request("cmdb.object_types", params)[-1]
    