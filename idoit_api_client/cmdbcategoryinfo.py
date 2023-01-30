from idoit_api_client import Request
from idoit_api_client.cmdbobjecttypecategories import CMDBObjectTypeCategories
from idoit_api_client.cmdbobjecttypes import CMDBObjectTypes


class CMDBCategoryInfo(Request):
    """Requests for API namespace 'cmdb.category_info'."""

    def read(self, category_const):
        """Fetches information about a category.

        :param category_const: Category constant

        :return: Result set
        """
        return self._api.request("cmdb.category_info", {"category": category_const})

    def batch_read(self, categories):
        """Fetches information about one or more categories.

        :param categories: List of category constants as strings

        :return: Indexed array of associative arrays
        """
        requests = []

        for category in categories:
            requests.append(
                {"method": "cmdb.category_info", "params": {"category": category}}
            )

        return self._api.batch_request(requests)

    def read_all(self):
        """Try to fetch information about all available categories.

        Ignored:
            * custom categories
            * Categories which are not assigned to any object types

        Notice: This method causes 3 api calls.

        :return: Indexed array of associative arrays
        """
        cmdb_object_types = CMDBObjectTypes(self._api)
        cmdb_object_type_categories = CMDBObjectTypeCategories(self._api)
        category_consts = []
        object_types = cmdb_object_types.read()
        object_type_ids = [object_type["id"] for object_type in object_types]
        object_type_categories_batch = cmdb_object_type_categories.batch_read_by_id(
            object_type_ids
        )
        cat_types = ["catg", "cats"]

        for object_type_categories in object_type_categories_batch:
            for cat_type in cat_types:
                if cat_type not in object_type_categories:
                    continue
                more = [
                    category["const"] for category in object_type_categories[cat_type]
                ]
                category_consts += more

        category_consts = list(set(category_consts))

        blacklisted_category_consts = self.get_virtual_category_constants()
        clean_category_constants = []

        skipped_categories = []

        for category_constant in category_consts:
            if category_constant not in blacklisted_category_consts:
                clean_category_constants.append(category_constant)
            else:
                skipped_categories.append(category_constant)

        clean_category_constants.sort()
        skipped_categories.sort()

        # for clean_category_constant in clean_category_constants:
        #    category_clean = self.batch_read([clean_category_constant])
        #    print("hi")

        categories = self.batch_read(clean_category_constants)

        combined_array = dict(zip(clean_category_constants, categories))

        if not isinstance(combined_array, dict):
            raise Exception("Unable to restructure result")

        return combined_array

    def get_virtual_category_constants(self):
        """Get list of constants for virtual categories

        "Virtual" means these categories have no attributes to call.

        :return array Array of strings"""
        return [
            "C__CATG__CABLING",
            "C__CATG__CABLE_CONNECTION",
            "C__CATG__CLUSTER_SHARED_STORAGE",
            "C__CATG__CLUSTER_VITALITY",
            "C__CATG__CLUSTER_SHARED_VIRTUAL_SWITCH",
            "C__CATG__DATABASE_FOLDER",
            "C__CATG__FLOORPLAN",
            "C__CATG__JDISC_DISCOVERY",
            "C__CATG__LIVESTATUS",
            "C__CATG__MULTIEDIT",
            "C__CATG__NDO",
            "C__CATG__NET_ZONE",
            "C__CATG__NET_ZONE_SCOPES",
            "C__CATG__OBJECT_VITALITY",
            "C__CATG__RACK_VIEW",
            "C__CATG__SANPOOL",
            "C__CATG__STACK_MEMBERSHIP",
            "C__CATG__STACK_PORT_OVERVIEW",
            "C__CATG__STORAGE",
            "C__CATG__VIRTUAL_AUTH",
            "C__CATG__VIRTUAL_RELOCATE_CI",
            "C__CATG__VIRTUAL_SUPERNET",
            "C__CATG__VIRTUAL_TICKETS",
            "C__CATG__VRRP_VIEW",
            "C__CATS__BASIC_AUTH",
            "C__CATS__CHASSIS_CABLING",
            "C__CATS__PDU_OVERVIEW",
            "C__CMDB__OBJTYPE__CONDUIT",
            "C__CATS__PERSON_GROUP_NAGIOS",
            "C__CATS__PERSON_NAGIOS",
        ]
