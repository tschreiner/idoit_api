"""CMDBObject class for i-doit API client."""
from idoit_api_client import Request
from idoit_api_client.cmdbcategory import CMDBCategory
from idoit_api_client.cmdbcategoryinfo import CMDBCategoryInfo
from idoit_api_client.cmdbobjects import CMDBObjects
from idoit_api_client.cmdbobjecttypecategories import CMDBObjectTypeCategories

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

    def read_all(self, object_id):
        """Read all information about object including category entries

        :param object_id: OObject identifier

        :return:Multi-dimensional array
        """
        cmdb_objects = CMDBObjects(self._api)
        objects = cmdb_objects.read({"ids": [object_id]}, None, None, None, None, True)

        if len(objects) == 0:
            raise Exception(f"Object not found by identifier {object_id}")
        elif len(objects) == 1:
            return objects[-1] 
        else:
            raise Exception(f"Found multiple objects by identifier {object_id}")

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

        return self

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

        cmdb_object_type_categories = CMDBObjectTypeCategories(self._api)

        object = {**object, **cmdb_object_type_categories.read_by_id(object["objecttype"])}

        cmdb_category = CMDBCategory(self._api)

        category_types = ["catg", "cats", "custom"]

        cmdb_category_info = CMDBCategoryInfo(self._api) # TODO: Port CMDBCategoryInfo
        blacklisted_category_constants = cmdb_category_info.get_virtual_category_constants()

        for category_type in category_types:
            if category_type not in object:
                continue

            category_constants = []

            i = 0
            for object_category_type in object[category_type]:
                if "const" not in object_category_type:
                    raise Exception("Information about categories is broken. Constant is missing.")
                category_constant = object[category_type][i]["const"]
                
                if category_constant in blacklisted_category_constants:
                    continue

                object[category_type][i]["entries"] = []

                category_constants.append(category_constant)
                i += 1

            category_entries = cmdb_category.batch_read([object_id], category_constants)

            i = 0
            for category_entry in category_entries:
                index = -1
                entries = []

                ii = 0
                for category in object[category_type]:
                    if category["const"] == category_constants[i]:
                        index = ii
                        entries = category_entries[i]
                        break
                    ii = ii + 1

                object[category_type][index]["entries"] = entries
                i = i + 1

        return object


    def upsert(self, type, title, attributes={}):
        """Create new object or fetch existing one based on its title and type.

        :param type: Object type identifier or its constant
        :param title: Object title
        :param attributes: (Optional) additional common attributes ('category', 'purpose', 'cmdb_status', 'description')

        :return Object identifier"""
        cmdb_objects = CMDBObjects(self._api)

        filter = {
            "title": title,
            "type": type
        }

        result = cmdb_objects.read(filter)

        if len(result) == 0:
            return self.create(type, title, attributes)
        elif len(result) == 1:
            if result[0] is None or result[0]["id"] is None:
                raise Exception("Bad result")
            return result[0]["id"]
        else:
            number_of_objects = len(result)
            raise Exception(f"Found {number_of_objects} objects")
