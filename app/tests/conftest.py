import pytest

from app.tests.response_tester import APIResponseTester

API_URL = "http://localhost:8000/"


@pytest.fixture
def api_response_tester():
    return APIResponseTester(API_URL)
