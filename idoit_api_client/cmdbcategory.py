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
            "category": category_constant,
        }

        if entry_id is not None:
            params["entry"] = entry_id

        result = self._api.request("cmdb.category.save", params)

        if (
            "entry" not in result
            or not isinstance(result["entry"], int)
            or "success" not in result
            or not result["success"]
        ):
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
        params = {"objID": object_id, "data": attributes, "category": category_const}

        result = self._api.request("cmdb.category.create", params)

        return result["id"]

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
        result = self._api.request(
            "cmdb.category.read",
            {"objID": object_id, "category": category_const, "status": status},
        )
        return result

    def read_one_by_id(self, object_id, category_const, entry_id, status=2):
        """Read one category entry for a specific object (works with both single- and multi-valued categories).

        :param object_id: Object identifier
        :param category_const: Category constant
        :param entry_id: Entry identifier
        :param status: (Optional) Filter entries by status:
            2 = normal;
            3 = archived;
            4 = deleted;
            -1 = combination of all;
            defaults to: 2 = normal;
            note: a status != 2 is only suitable for multi-value categories

        :return: Associative array"""
        entries = self.read(object_id, category_const, status)

        for entry in entries:
            if "id" not in entry:
                raise Exception(
                    f'Entries for category "{category_const}" contain no identifier'
                )

            current_id = int(entry["id"])

            if current_id == entry_id:
                return entry

        raise Exception(
            f'No entry with identifier "{entry_id}" found in category "{category_const}" for object "{object_id}"'
        )

    def read_first(self, object_id, category_const):
        """Read first category entry for a specific object (works with both single- and multi-valued categories).

        :param object_id: Object identifier
        :param category_const: Category constant

        :return: Associative array, otherwise empty array when there is no entry"""
        entries = self.read(object_id, category_const)

        if len(entries) == 0:
            return []

        return entries[0]

    def update(self, object_id, category_const, attributes, entry_id=None):
        """Update category entry for a specific object.

        :param object_id: Object identifier
        :param category_const: Category constant
        :param attributes: Attributes as key-value pairs
        :param entry_id: Entry identifier (only needed for multi-valued categories)

        :return returns itself"""
        if entry_id is not None:
            attributes["category_id"] = entry_id

        result = self._api.request(
            "cmdb.category.update",
            {"objID": object_id, "category": category_const, "data": attributes},
        )

        self._require_success_without_identifier(result, True)

        return self

    def archive(self, object_id, category_const, entry_id):
        """Archive entry in a multi-value category for a specific object.

        :param object_id: Object identifier
        :param category_const: Category constant
        :param entry_id: Entry identifier"""

        self._api.request(
            "cmdb.category.archive",
            {"object": object_id, "category": category_const, "entry": entry_id},
        )

    def delete(self, object_id, category_const, entry_id):
        """Mark entry in a multi-value category for a specific object as deleted.

        :param object_id: Object identifier
        :param category_const: Category constant
        :param entry_id: Entry identifier

        :return returns itself"""
        self._api.request(
            "cmdb.category.delete",
            {"object": object_id, "category": category_const, "entry": entry_id},
        )

        return self

    def purge(self, object_id, category_const, entry_id):
        """Purge entry in a single- or multi-value category for a specific object.

        :param object_id: Object identifier
        :param category_const: Category constant
        :param entry_id: Entry identifier (only needed for multi-valued categories)

        :return returns itself"""
        params = {"object": object_id, "category": category_const}

        if entry_id is not None:
            params["entry"] = entry_id

        self._api.request("cmdb.category.purge", params)

        return self

    def recycle(self, object_id, category_const, entry_id):
        """Restore entry in a multi-value category for a specific object to "normal" state

        :param object_id: Object identifier
        :param category_const: Category constant
        :param entry_id: Entry identifier

        :return returns itself"""
        self._api.request(
            "cmdb.category.recycle",
            {"object": object_id, "category": category_const, "entry": entry_id},
        )

        return self

    def quick_purge(self, object_id, category_const, entry_id):
        """Purge entry in a multi-value category for a specific object.

        :param object_id: Object identifier
        :param category_const: Category constant
        :param entry_id: Entry identifier

        :return returns itself"""
        result = self._api.request(
            "cmdb.category.quickpurge",
            {"object": object_id, "category": category_const, "entry": entry_id},
        )

        self.require_success_without_identifier(result)

        return self

    def batch_create(self, object_ids, category_const, attributes):
        """Create multiple entries for a specific category and one or more objects.

        :param object_ids List of object identifiers as integers
        :param category_const Category constant
        :param attributes Indexed array of attributes as key-value pairs

        :return List of entry identifiers as integers"""
        entry_ids = []

        requests = []

        for object_id in object_ids:
            for data in attributes:
                params = {"objID": object_id, "data": data, "category": category_const}

                requests.append({"method": "cmdb.category.create", "params": params})

        result = self._api.batch_request(requests)
        #  Do not check 'id' because in a batch request it is always NULL:
        for entry in result:
            if "success" not in entry or entry["success"] is not True:
                if "message" in entry:
                    raise Exception(f"Bad result: {entry['message']}")
                raise Exception("Bad result")

            entry_ids.append(int(entry["id"]))

        return entry_ids

    def batch_read(self, object_ids, category_constants, status=2):
        if not isinstance(object_ids, list):
            raise Exception("Object IDs must be an array")
        if len(object_ids) == 0:
            raise Exception("Needed at least one object identifier")

        if not isinstance(category_constants, list):
            raise Exception("Category constants must be a list")
        if len(category_constants) == 0:
            raise Exception("Needed at least one category constant")

        requests = []

        for object_id in object_ids:
            if not isinstance(object_id, int) or object_id < 0:
                raise Exception("Each object identifier must be a positive integer")

            for category_constant in category_constants:
                if (
                    not isinstance(category_constant, str)
                    or len(category_constant) == 0
                ):
                    raise Exception("Each category constant must be a non-empty string")

                requests.append(
                    {
                        "method": "cmdb.category.read",
                        "params": {
                            "objID": object_id,
                            "category": category_constant,
                            "status": status,
                        },
                    }
                )

        results = self._api.batch_request(requests)

        expected_amount_of_results = len(object_ids) * len(category_constants)
        actual_amount_of_results = len(results)
        count_objects = len(object_ids)
        count_category_constants = len(category_constants)

        if actual_amount_of_results != expected_amount_of_results:
            raise Exception(
                f"Requested entries for {count_objects} object(s), and {count_category_constants} category constant(s), but got {actual_amount_of_results} result(s)"
            )

        return results

    def batch_update(self, object_ids, category_const, attributes):
        """Update single-value category for one or more objects.

        :param object_ids List of object identifiers as integers
        :param category_const Category constant
        :param attributes Attributes as key-value pairs

        :return returns itself"""
        requests = []

        for object_id in object_ids:
            requests.append(
                {
                    "method": "cmdb.category.update",
                    "params": {
                        "objID": object_id,
                        "category": category_const,
                        "data": attributes,
                    },
                }
            )

        results = self._api.batch_request(requests)

        self._require_success_for_all(results, ignore_deprecated=True)

        return self

    def clear(self):
        raise ("Not implemented")
