
import pytest
import json
from httmock import HTTMock, urlmatch
from usda.client import UsdaClient
from usda.pagination import RawPaginator, ModelPaginator
from usda.tests.sample_data import FOOD_LIST_DATA


class TestPagination(object):
    """Unit tests for pagination helpers"""

    @urlmatch(path=r'/ndb/list')
    def api_list(self, uri, request):
        assert 'offset=42' in uri.query
        return json.dumps(FOOD_LIST_DATA)

    @pytest.fixture
    def apimock(self):
        return HTTMock(self.api_list)

    def test_offset(self, apimock):
        """
        Test the paginator handles setting the offset correctly
        """
        client = UsdaClient('SOME_KEY')
        result = client.list_foods_raw(max=10, offset=42)
        assert isinstance(result, RawPaginator)
        assert result.current_offset == 42
        with apimock:
            data = list(result)
        assert data == FOOD_LIST_DATA['list']['item']

    def test_model_offset(self, apimock):
        """
        Test the ModelPaginator handles offsets correctly
        """
        client = UsdaClient('SOME_KEY')
        result = client.list_foods(max=10, offset=42)
        assert isinstance(result, ModelPaginator)
        assert result.raw.current_offset == 42
        with apimock:
            foods = list(result)
        assert foods[0].name == 'Pizza'
        assert foods[1].name == 'Pizza with pineapple'
