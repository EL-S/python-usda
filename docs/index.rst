python-usda documentation
=========================

:ref:`genindex` - :ref:`modindex` - :ref:`search`

.. image:: https://img.shields.io/pypi/l/python-usda.svg
   :target: https://pypi.org/project/python-usda/
   :alt: Package license badge

.. image:: https://img.shields.io/pypi/format/python-usda.svg
   :target: https://pypi.org/project/python-usda/
   :alt: Python package format badge

.. image:: https://img.shields.io/pypi/pyversions/python-usda.svg
   :target: https://pypi.org/project/python-usda/
   :alt: Compatible Python versions badge

.. image:: https://img.shields.io/pypi/status/python-usda.svg
   :target: https://pypi.org/project/python-usda/
   :alt: Python package status badge

.. image:: https://requires.io/github/Lucidiot/python-usda/requirements.svg?branch=master
   :target: https://requires.io/github/Lucidiot/python-usda/requirements/?branch=master
   :alt: Requires.io requirements badge

.. image:: https://api.codeclimate.com/v1/badges/9a969172a5d47456376e/maintainability
   :target: https://codeclimate.com/github/Lucidiot/python-usda/maintainability
   :alt: CodeClimate maintanability badge

.. image:: https://landscape.io/github/Lucidiot/python-usda/master/landscape.svg?style=flat
   :target: https://landscape.io/github/Lucidiot/python-usda/master
   :alt: Landscape.io health badge

.. image:: https://codecov.io/gl/Lucidiot/python-usda/branch/master/graph/badge.svg
   :target: https://codecov.io/gl/Lucidiot/python-usda
   :alt: Codecov coverage badge

.. image:: https://img.shields.io/github/last-commit/Lucidiot/python-usda.svg
   :target: https://gitlab.com/Lucidiot/python-usda/commits/master
   :alt: Last commit badge

.. image:: https://img.shields.io/gitter/room/BrainshitPseudoScience/Lobby.svg?logo=gitter-white
   :target: https://gitter.im/BrainshitPseudoScience/Lobby
   :alt: Chat on Gitter

.. image:: https://img.shields.io/badge/badge%20count-14-brightgreen.svg
   :target: https://gitlab.com/Lucidiot/python-usda
   :alt: Badge count badge

.. image:: https://gitlab.com/Lucidiot/python-usda/badges/master/pipeline.svg
   :target: https://gitlab.com/Lucidiot/python-usda/pipelines
   :alt: GitLab pipeline status badge

.. image:: https://gitlab.com/Lucidiot/python-usda/badges/master/coverage.svg
   :target: https://gitlab.com/Lucidiot/python-usda/pipelines
   :alt: GitLab coverage badge

.. image:: https://readthedocs.org/projects/python-usda/badge/?version=latest
   :target: https://python-usda.readthedocs.io/en/latest
   :alt: Read The Docs build status badge

Introduction
------------

python-usda is a fork of `pygov <https://pypi.org/project/pygov/>`_
focused on `USDA's Food Composition Database
API <http://ndb.nal.usda.gov/ndb/doc/>`_.

It was initially created to make it easier to fetch up-to-date
nutritional data for some pseudo-scientific calculations in the
`PseudoScience <https://gitlab.com/Lucidiot/PseudoScience>`_ project
but has been extended to provide a better coverage of the API.

Setup
-----

::

   pip install python-usda

Usage
-----

python-usda provides an API client called ``UsdaClient`` that is the
base to all API requests:

.. code:: python

   from usda import UsdaClient
   client = UsdaClient('API_KEY')

The USDA API requires a Data.gov API key that you can get for free
`here <https://api.data.gov/signup/>`_.

Using the client, you can list food items:

.. code:: python

   foods_list = client.list_foods(5)
   for _ in range(5):
       food_item = next(foods_list)
       print(food_item.name)

Be careful; the ``5`` argument in the ``list_foods`` method only sets the
amount of items that are returned at once; requesting one more will perform
a request for another page of 5 results.

Instead of just listing food items, it is possible to perform a text search:

.. code:: python

   foods_search = client.search_foods(
        'coffee, instant, regular, prepared with water', 1)

   coffee = next(foods_search)
   print(coffee)

The above code will output::

   Food ID 14215 'Beverages, coffee, instant, regular, prepared with water'

We can then use this food item's ID to request a Food Report:

.. code:: python

   report = client.get_food_report(coffee.id)
   for nutrient in report.nutrients:
        print(nutrient.name, nutrient.value, nutrient.unit)

The above code will output::

   Water 99.09 g
   Energy 2.0 kcal
   Protein 0.1 g
   [...]
   Cholesterol 0.0 mg
   Caffeine 26.0 mg

And there it is, your first nutritional information report.

There is more available than mere food items and nutritional facts;
head over to the `API Guide <guide>`_ to learn more.

Error handling
--------------

The API client uses `requests <https://python-requests.org>`_ to perform
requests to USDA's API and does not explicitly handle its errors to let
this library's users deal with network-related errors.

As the API has a very inconsistent way of returning errors, it cannot be
fully guaranteed that all API errors are properly handled. If you
encounter a case of an unhandled error response from the API, please
file an issue.

All API errors are subclasses of :class:`usda.base.DataGovApiError`.

When an invalid API key is supplied, any API requests may raise a
:class:`usda.base.DataGovInvalidApiKeyError`.

When the allowed requests limit has been reached, a
:class:`usda.base.DataGovApiRateExceededError` is raised.

Raw results
-----------

If you prefer to receive the raw JSON data instead of classes, append
``_raw`` to any client request method. For example, to retrieve the raw
JSON data for a foods list requests, use ``client.list_foods_raw``.
Those raw methods will pass all keyword arguments as parameters in the
request URL.

Other topics
------------

.. toctree::
   :maxdepth: 2
   
   guide
   contributing
   api
