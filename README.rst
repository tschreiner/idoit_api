============================
i-doit API Client for Python
============================

.. image:: https://github.com/tschreiner/idoit_api/actions/workflows/build.yml/badge.svg
        :target: https://github.com/tschreiner/idoit_api/actions/workflows/build.yml

.. image:: https://img.shields.io/pypi/v/idoit_api_client.svg
        :target: https://pypi.python.org/pypi/idoit_api_client

.. image:: https://readthedocs.org/projects/idoit-api/badge/?version=latest
        :target: https://idoit-api.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

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

Installation
------------

Option 1: pip install from PyPI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install ``idoit_api_client`` using ``pip`` from PyPI (recommended for most users)::

    $ pip install idoit_api_client

Option 2: pip install from GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install ``idoit_api_client`` using ``pip`` from GitHub::

    $ pip install git+https://github.com/tschreiner/idoit_api.git@main

Option 3: Install ``idoit_api_client`` from source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install ``idoit_api_client`` from source::

    $ git clone
    $ cd idoit_api_client
    $ python setup.py install

Option 4: Install ``idoit_api_client`` from source (in development mode)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install ``idoit_api_client`` from source (in development mode)::

    $ git clone https://github.com/tschreiner/idoit_api.git
    $ cd idoit_api_client
    $ python setup.py develop

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
