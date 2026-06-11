import pytest

from api_suite.utils.user_factory import generate_user


REGISTER_ENDPOINT = "/api/Users/"


@pytest.mark.functional
def test_register_user_success(api_client):

    user = generate_user()

    response = api_client.post(
        REGISTER_ENDPOINT,
        {
            "email": user.email,
            "password": user.password
        }
    )

    assert response.status_code in [200, 201, 409]


@pytest.mark.functional
def test_registration_response_discovery(api_client):

    user = generate_user()

    response = api_client.post(
        REGISTER_ENDPOINT,
        {
            "email": user.email,
            "password": user.password
        }
    )

    print("\nREG RESPONSE:", response.text)

    assert response.status_code in [200, 201, 409]