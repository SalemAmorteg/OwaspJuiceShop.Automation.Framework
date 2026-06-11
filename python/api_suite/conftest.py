import pytest

from api_suite.clients.api_client import APIClient
from api_suite.config.test_data import VALID_USER


BASE_URL = "http://localhost:3000"


@pytest.fixture(scope="session")
def api_client():
    """
    Shared API client for all API tests.
    """
    return APIClient(BASE_URL)


@pytest.fixture
def authenticated_api_client(api_client):
    """
    Returns API client already authenticated.
    """

    response = api_client.login(
        VALID_USER.email,
        VALID_USER.password
    )

    assert response.status_code == 200

    token = response.json()["authentication"]

    api_client.set_auth_token(token)

    return api_client