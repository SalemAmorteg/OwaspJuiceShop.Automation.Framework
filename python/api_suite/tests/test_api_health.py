import pytest


@pytest.mark.smoke
def test_api_is_alive(api_client):
    """
    Basic health check for the API.
    We only verify that the server responds.
    """

    response = api_client.get("/rest/user/login")

    assert response.status_code in [200, 400, 401, 405]


@pytest.mark.smoke
def test_products_endpoint_is_reachable(api_client):
    """
    Checks that products endpoint is accessible.
    """

    response = api_client.get("/api/Products")

    assert response.status_code in [200, 401]


@pytest.mark.smoke
def test_user_session_endpoint_is_alive(api_client):
    """
    Checks that whoami endpoint responds (auth required).
    """

    response = api_client.get("/rest/user/whoami")

    assert response.status_code in [401, 403]