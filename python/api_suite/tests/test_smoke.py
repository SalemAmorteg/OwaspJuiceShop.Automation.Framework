import pytest


@pytest.mark.smoke
def test_api_login_health(api_client):

    response = api_client.post(
        "/rest/user/login",
        {"email": "test@test.com", "password": "test"}
    )

    assert response.status_code in [200, 400, 401]


@pytest.mark.smoke
def test_api_products_health(api_client):

    response = api_client.get("/api/Products")

    assert response.status_code in [200, 401]


@pytest.mark.smoke
def test_api_whoami_health(api_client):

    response = api_client.get("/rest/user/whoami")

    assert response.status_code in [401, 403]