
from idoit_api_client import Request


class CMDBCategoryInfo(Request):
    """Requests for API namespace 'cmdb.category_info'."""

    def read(self, category_const):
        """Fetches information about a category.

        :param category_const: Category constant

        :return: Result set
        """
        return self._api.request("cmdb.category_info", {"category": category_const})