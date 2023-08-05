import pytest

from ._mock_app import test_app
from meos_sdk.testing.client import MeosAppTestClient


@pytest.fixture
def test_app_client():
    return MeosAppTestClient(app=test_app)
