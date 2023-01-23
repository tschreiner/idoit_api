"""Test create object for every type."""

# Helper imports
import random
import string

# i-doit imports
from idoit_api_client import Constants, API
from idoit_api_client.cmdbobject import CMDBObject
from idoit_api_client.cmdbobjecttypes import CMDBObjectTypes
from tests.test_idoit_api_client import BaseTest

# Helper function
def _generate_random_string():
    """Generate random string."""
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

# Create config
config = {
    Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
    Constants.KEY: 'c1ia5q',
    Constants.USERNAME: 'admin',
    Constants.PASSWORD: 'admin'
}

# Create API object
api = API(config)
api.connect()
api.login()

# Read object types from i-doit
object_types = CMDBObjectTypes(api)
object_types_result = object_types.read()
# Print all object types
print("debug: object_types_result = {}".format(object_types_result))

# Create a list of object type constants
object_type_constants = [object_type['const'] for object_type in object_types_result]
print("debug: object_type_constants = {}".format(object_type_constants))

# Create a CMDBObject object which is used to persist objects to i-doit
cmdb_object = CMDBObject(api)

# Go through all object types and create an object for each type
for object_type_constant in object_type_constants:
    object_title = _generate_random_string()
    object_id = cmdb_object.create(object_type_constant, object_title)
    if object_id is None:
        print("debug: object_type_constant = {} could not be created".format(object_type_constant))
        continue
    print(f"debug: Created object with title '{object_title}' and id '{object_id}' for object type '{object_type_constant}'")

# Logout
api.logout()