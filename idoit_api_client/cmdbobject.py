"""CMDBObject class for i-doit API client."""
from idoit_api_client import Request


class CMDBObject(Request):
    """CMDBObject class for i-doit API client."""

    def create(self, type, title, attributes={}):
        """Create a new object.

        :param type: Object type identifier or its constant
        :param title: Object title
        :param attributes: (Optional) additional common attributes:
            - category
            - cmdb_status
            - defaultTemplate
            - description
            - purpose
            - status
            - sysid

        :return: Object identifier
        """
        attributes["type"] = type
        attributes["title"] = title

        result = self._api.request("cmdb.object.create", attributes)

        if "id" in result:
            return result["id"]

        raise Exception("Unable to create object")

    def create_with_categories(self, type, title, categories={}, attributes={}):
        """Create new object with category entries.

        :param type: Object type identifier or its constant
        :param title: Object title
        :param categories: Also create category entries
            Set category constant (string) as key and
            one (array of attributes) entry or even several entries (array of arrays) as value
        :param attributes: (Optional) additional common attributes:
            - category
            - cmdb_status
            - defaultTemplate
            - description
            - purpose
            - status
            - sysid

        :return: Result with object identifier('id') and key-value pairs of category constants and array of category entry identifiers as integers
        """
        attributes["type"] = type
        attributes["title"] = title

        if len(categories) > 0:
            attributes["categories"] = categories

        return self._api.request("cmdb.object.create", attributes)

    def read(self, id):
        """Read common information about object

        :param id: Object identifier

        :return: Object information
        """
        return self._api.request("cmdb.object.read", {"id": id})

    def update(self, object_id, attributes):
        """Update common information about object

        :param id: Object identifier
        :param attributes: (Optional) common attributes (only 'title' is supported at the moment)
        """
        params = {"id": object_id}

        supported_attributes = ["title"]

        for supported_attribute in supported_attributes:
            if supported_attribute in attributes:
                params[supported_attribute] = attributes[supported_attribute]

        result = self._api.request("cmdb.object.update", params)

        if "success" not in result or result["success"] == False:
            raise Exception(f"Unable to update object {object_id}")

    def archive(self, object_id):
        """Archive object

        :param object_id: Object identifier
        """
        result = self._api.request("cmdb.object.archive", {"object": object_id})

        if "success" not in result or result["success"] == False:
            raise Exception(f"Unable to archive object {id}")

    def delete(self, object_id):
        """Mark object as deleted (it's still available)

        :param object_id: Object identifier
        """
        result = self._api.request("cmdb.object.delete", {"object": object_id})

    def purge(self, object_id):
        """Purge object (delete it irrevocable)

        :param object_id: Object identifier
        """
        result = self._api.request("cmdb.object.purge", {"object": object_id})

    def mark_as_template(self, object_id):
        """Convert object to template

        Works only for "normal objects" and "mass change templates"

        :param object_id: Object identifier
        """
        result = self._api.request("cmdb.object.markAsTemplate", {"object": object_id})

    def mark_as_mass_change_template(self, object_id):
        """Convert object to mass change template

        Works only for "normal objects" and "templates"

        :param object_id: Object identifier
        """
        result = self._api.request("cmdb.object.markAsMassChangeTemplate", {"object": object_id})

    def recycle(self, object_id):
        """Restore object to "normal" status

        Works with archived and deleted objects, templates and mass change templates

        :param object_id: Object identifier
        """
        result = self._api.request("cmdb.object.recycle", {"object": object_id})

    def load(self, object_id):
        """Load all data about object

        :param object_id: Object identifier

        :return: Multi-dimensional array
        """
        object = self.read(object_id)

        if len(object) == 0:
            raise Exception(f"Object {object_id} not found")

        if "objecttype" not in object:
            raise Exception(f"Object {object_id} has no type")

        cmdb_object_type_categories = CMDBObjectTypeCategories(self._api) # TODO: Port CMDBObjectTypeCategories

        object += cmdb_object_type_categories.read(object["objecttype"])

        cmdb_category = CMDBCategory(self._api) # TODO: Port CMDBCategory

        category_types = ["catg", "cats", "custom"]

        cmdb_category_info = CMDBCategoryInfo(self._api) # TODO: Port CMDBCategoryInfo
        blacklisted_category_constants = cmdb_category_info.get_virtual_category_constants()

        for category_type in category_types:
            if category_type not in object:
                continue

            category_constants = []

            # TODO: Continue porting from https://github.com/i-doit/api-client-php/blob/main/src/CMDBObject.php#L335
