API Reference
=============

.. contents::
   :local:
   :backlinks: none

Client
------

.. autoclass:: usda.client.UsdaClient
   :members:

Domain
------

Base classes
^^^^^^^^^^^^

.. automodule:: usda.domain
   :members: UsdaObject, ListItem

Items
^^^^^

.. automodule:: usda.domain
   :members: Food, Nutrient, Measure 

Food Reports
^^^^^^^^^^^^

.. automodule:: usda.domain
   :members: FoodReport, FoodReportV2, Source

Nutrient Reports
^^^^^^^^^^^^^^^^

.. automodule:: usda.domain
   :members: NutrientReportFood

Enums
-----

.. automodule:: usda.enums
   :members: UsdaUriActions, UsdaNdbListType, UsdaNdbReportType

Low level classes
-----------------

Base client
^^^^^^^^^^^

.. automodule:: usda.base
   :members: BASE_URI, DataGovClientBase, api_request

Exceptions
^^^^^^^^^^

.. automodule:: usda.base
   :members: DataGovApiError, DataGovApiRateExceededError,
      DataGovInvalidApiKeyError

Pagination
^^^^^^^^^^

All USDA NDB list API responses are paginated ; to help users not deal with
pagination, some specific generators ("paginators") have been created.
They are designed to be lazy and will only make requests when necessary.

.. automodule:: usda.pagination
   :members: RawPaginator, ModelPaginator, RawNutrientReportPaginator
