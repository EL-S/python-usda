#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for Data.gov API features"""

import pytest
import json
from httmock import urlmatch, HTTMock
from usda.client import UsdaClient
from usda.base import DataGovApiError
from usda.tests.sample_data import \
    FOOD_LIST_DATA, NUTRIENT_LIST_DATA, \
    FOOD_GROUP_LIST_DATA, DERIVATION_CODES_LIST_DATA, \
    FOOD_REPORT_DATA, FOOD_REPORT_V2_DATA, NUTRIENT_REPORT_DATA, \
    FOOD_SEARCH_DATA


class TestClient(object):
    """Tests for UsdaClient"""

    @urlmatch(path=r'/ndb/list')
    def api_list(self, uri, request):
        if "lt=f" in uri.query:
            return json.dumps(FOOD_LIST_DATA)
        elif "lt=n" in uri.query:
            return json.dumps(NUTRIENT_LIST_DATA)
        elif "lt=g" in uri.query:
            return json.dumps(FOOD_GROUP_LIST_DATA)
        elif "lt=d" in uri.query:
            return json.dumps(DERIVATION_CODES_LIST_DATA)

    @urlmatch(path=r'/ndb/reports')
    def api_report(self, uri, request):
        return json.dumps(FOOD_REPORT_DATA)

    @urlmatch(path=r'/ndb/V2/reports')
    def api_report_v2(self, uri, request):
        if "ndbno=666" in uri.query:
            return json.dumps({
                "foods": [{"error": "Not found"}],
                "count": "1",
                "notfound": "1"
            })
        return json.dumps(FOOD_REPORT_V2_DATA)

    @urlmatch(path=r'/ndb/nutrients')
    def api_nutrients(self, uri, request):
        return json.dumps(NUTRIENT_REPORT_DATA)

    @urlmatch(path=r'/ndb/search')
    def api_search(self, uri, request):
        return json.dumps(FOOD_SEARCH_DATA)

    @pytest.fixture
    def apimock(self):
        return HTTMock(self.api_list, self.api_report, self.api_report_v2,
                       self.api_nutrients, self.api_search)

    def test_client_init(self):
        cli = UsdaClient("API_KAY")
        assert cli.uri_part == "ndb/"
        assert cli.key == "API_KAY"
        assert cli.use_format

    def test_client_list_foods_raw(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            data = list(cli.list_foods_raw(max=5))
        assert data == FOOD_LIST_DATA['list']['item']

    def test_client_list_foods(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            foods = list(cli.list_foods(5))
        assert foods[0].name == "Pizza"
        assert foods[1].name == "Pizza with pineapple"

    def test_client_list_nutrients_raw(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            data = list(cli.list_nutrients_raw(max=5))
        assert data == NUTRIENT_LIST_DATA['list']['item']

    def test_client_list_nutrients(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            nutrients = list(cli.list_nutrients(5))
        assert nutrients[0].name == "Calcium"
        assert nutrients[1].name == "Lactose"

    def test_client_list_food_groups_raw(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            groups = list(cli.list_food_groups_raw(max=5))
        assert groups == FOOD_GROUP_LIST_DATA['list']['item']

    def test_client_list_food_groups(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            groups = list(cli.list_food_groups(5))
        assert groups[0].name == "Dairy and Eggs Products"
        assert groups[1].name == "Baby Foods"

    def test_client_list_derivation_codes_raw(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            codes = list(cli.list_derivation_codes_raw(max=5))
        assert codes == DERIVATION_CODES_LIST_DATA['list']['item']

    def test_client_list_derivation_codes(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            codes = list(cli.list_derivation_codes(5))
        assert codes[0].name == "Analytical data"
        assert codes[1].name == "Analytical data; derived by linear regression"

    def test_client_food_report_raw(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            data = cli.get_food_report_raw(ndbno=123456)
        assert data == FOOD_REPORT_DATA

    def test_client_food_report(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            fr = cli.get_food_report(123456)
        assert fr.food.name == "Pizza"

    def test_client_food_report_v2_raw(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            data = cli.get_food_report_v2_raw(ndbno=123456)
        assert data == FOOD_REPORT_V2_DATA

    def test_client_food_report_v2(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            fr = cli.get_food_report_v2(123456)
        assert fr[0].food.name == "Pizza"

    def test_client_food_report_v2_error(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            with pytest.raises(DataGovApiError):
                cli.get_food_report_v2(666)

    def test_client_nutrient_report_raw(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            data = list(cli.get_nutrient_report_raw(nutrients=[42, 1337]))
        assert data == NUTRIENT_REPORT_DATA['report']['foods']

    def test_client_nutrient_report(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            with pytest.raises(ValueError):
                # Go over 20 nutrients
                cli.get_nutrient_report(*range(21))
            nr = list(cli.get_nutrient_report(42, 1337))
        assert nr[0].name == "Pizza with pineapple"

    def test_client_search_foods_raw(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            data = list(cli.search_foods_raw(q='pizza', max=5))
        assert data == FOOD_SEARCH_DATA['list']['item']

    def test_client_search_foods(self, apimock):
        cli = UsdaClient("API_KAY")
        with apimock:
            foods = list(cli.search_foods('pizza', 5))
        assert foods[0].name == "Pizza"
        assert foods[1].name == "Pizza with pineapple"
