"""Requests for API namespace 'cmdb.object_types"""

from idoit_api_client import API, Constants, Request

class CMDBObjectTypes(Request):
    """Requests for API namespace 'cmdb.object_types'"""

    def read(self):
        """Read object types.

        :return: Array of object types
        """
        return self._api.request("cmdb.object_types.read")
