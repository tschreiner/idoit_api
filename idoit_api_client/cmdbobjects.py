"""Requests for API namespace 'cmdb.objects'."""

from idoit_api_client import Request

class CMDBObjects(Request):
    SORT_ASCENDING = "asc"
    SORT_DESCENDING = "desc"

    def create(self, objects):
        """Create one or more objects

        :param list objects Mandatory attributes ('type', 'title') and optional attributes
            ('category', 'purpose', 'cmdb_status', 'description')

        :return array List of object identifiers"""
        requests = []

        for object in objects:
            requests.append({
                "method": "cmdb.object.create",
                "params": object
            })

        result = self._api.batch_request(requests)

        object_ids = []

        for result in results:
            object_ids.append(result["id"])

        return object_ids

    def read(self, filter={}, limit=None, offset=None, order_by=None, sort=None, categories=None):
        """Fetch objects.

        :param dict filter (Optional) Filter; use any combination of 'ids' (array of object identifiers),
            'type' (object type identifier), 'type_group', 'status', 'title' (object title), 'type_title' (l10n object type title),
            'location', 'sysid', 'first_name', 'last_name', 'email'
        :param int limit (Optional) Limit result set
        :param int offset Offset
        :param str order_by Order result set by 'isys_obj_type__id', 'isys_obj__isys_obj_type__id', 'type',
        'isys_obj__title', 'title', 'isys_obj_type__title', 'type_title', 'isys_obj__sysid', 'sysid',
        'isys_cats_person_list__first_name', 'first_name', 'isys_cats_person_list__last_name', 'last_name',
        'isys_cats_person_list__mail_address', 'email', 'isys_obj__id', 'id'
        :param str sort Sort ascending ('ASC') or descending ('DESC')
        :param bool|array categories Also fetch category entries; add a list of category constants as array of strings
        or true for all assigned categories, otherwise false for none; defaults to false

        :return list Indexed array of associative arrays"""
        params = {}

        if len(filter) > 0:
            params["filter"] = filter

        if categories is not False:
            params["categories"] = categories

        if limit is not None:
            if offset is not None:
                params["limit"] = f"{offset},{limit}"
            else:
                params["limit"] = limit

        if order_by is not None:
            params["order_by"] = order_by

        if sort is not None:
            params["sort"] = sort

        return self._api.request("cmdb.objects.read", params)

    def read_by_ids(self, object_ids, categories=None):
        """Fetch objects by their identifiers.

        :param list object_ids List of object identifiers as integers
        :param bool|array categories Also fetch category entries; add a list of category constants as array of strings
        or true for all assigned categories, otherwise false for none; defaults to false

        :return list Indexed array of associative arrays"""
        params = {
            "filter": {
                "ids": object_ids
            }
        }

        if categories is not False:
            params["categories"] = categories

        return self._api.request("cmdb.objects.read", params)

    def get_id(self, title, type=None):
        """Fetch an object identifier by object title and (optional) type.

        :param str title Object title
        :param str type (Optional) type constant

        :return int Object identifier"""
        filter = {
            "title": title
        }

        if type is not None:
            filter["type"] = type

        result = self.read(filter)

        result_count = len(result)

        if result_count == 0:
            raise Exception("Object not found")
        elif result_count == 1:
            if not result[0] or "id" not in result[0].keys():
                raise Exception("Bad result")
            return result[0]["id"]
        raise Exception("Found {} objects".format(result_count))