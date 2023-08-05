=============================
API clients permission.
=============================

.. image:: https://badge.fury.io/py/api_clients.svg
    :target: https://badge.fury.io/py/api_clients

.. image:: https://travis-ci.org/jeromecaisip/api_clients.svg?branch=master
    :target: https://travis-ci.org/jeromecaisip/api_clients

.. image:: https://codecov.io/gh/jeromecaisip/api_clients/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/jeromecaisip/api_clients

Permission handler for drf API's.

Documentation
-------------

The full documentation is at https://api_clients.readthedocs.io.

Quickstart
----------

Install API clients permission.::

    pip install api_clients

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'api_clients.apps.ApiClientsConfig',
        ...
    )

Add API clients permission.'s URL patterns:

.. code-block:: python

    from api_clients import urls as api_clients_urls


    urlpatterns = [
        ...
        url(r'^', include(api_clients_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
