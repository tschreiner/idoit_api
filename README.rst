============================
i-doit API Client for Python
============================


.. image:: https://img.shields.io/pypi/v/idoit_api_client.svg
        :target: https://pypi.python.org/pypi/idoit_api_client

.. image:: https://img.shields.io/travis/tschreiner/idoit_api.svg
        :target: https://travis-ci.com/tschreiner/idoit_api

.. image:: https://readthedocs.org/projects/idoit-api/badge/?version=latest
        :target: https://idoit-api.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/tschreiner/idoit_api/shield.svg
     :target: https://pyup.io/repos/github/tschreiner/idoit_api/
     :alt: Updates



i-doit API Client for Python. Port of the original PHP i-doit API Client.


* Free software: GNU General Public License v3
* Documentation: https://idoit-api.readthedocs.io.


Features
--------

* Make requests to the i-doit API with a method name and parameters
* Requests are parsed, checked and returned as a dictionary
* Make raw requests to the i-doit API
* TODO: Read/create/upsert i-doit Objects, Object Types, Object Categories and Object Category Attributes

Implemented Objects and Methods
-------------------------------

| Object | Method | Implemented | Tests implemented |
|--------|--------|-------------|-------------------|
| CMDBObjectType | read | Yes | Yes |

Usage
-----

Simple usage example::

    from idoit_api_client import Constants, API
    config = {
        Constants.URL: 'https://demo.i-doit.com/src/jsonrpc.php',
        Constants.KEY: 'c1ia5q',
        Constants.USERNAME: 'admin',
        Constants.PASSWORD: 'admin'
    }
    api = API(config)
    api.login()
    result = api.request('cmdb.category.read', {
        'objID': 1,
        'category': 'C__CATG__GLOBAL'
    })
    print(result)

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
