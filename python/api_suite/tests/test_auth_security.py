import pytest

from core.config.test_data import VALID_USER


@pytest.mark.security
def test_login_sql_injection_attempt(api_client):

    payload = {
        "email": "' OR 1=1--",
        "password": "' OR 1=1--"
    }

    response = api_client.post(
        "/rest/user/login",
        payload
    )

    assert response.status_code in [400, 401]


@pytest.mark.security
def test_user_enumeration_protection(api_client):

    fake_user_response = api_client.post(
        "/rest/user/login",
        {
            "email": "fake@test.com",
            "password": "Password123!"
        }
    )

    wrong_password_response = api_client.post(
        "/rest/user/login",
        {
            "email": VALID_USER.email,
            "password": "wrong_password"
        }
    )

    assert (
        fake_user_response.status_code
        ==
        wrong_password_response.status_code
    )