import pytest

from api_suite.config.test_data import VALID_USER
from models.auth_models import LoginResponseSchema


LOGIN_ENDPOINT = "/rest/user/login"


@pytest.mark.smoke
@pytest.mark.functional
def test_login_success(api_client):
    """
    Valid login returns JWT token.
    """

    response = api_client.post(
        LOGIN_ENDPOINT,
        {
            "email": VALID_USER.email,
            "password": VALID_USER.password
        }
    )

    assert response.status_code == 200

    schema = LoginResponseSchema.model_validate(response.json())

    assert schema.authentication.token
    assert schema.is_jwt


@pytest.mark.functional
@pytest.mark.parametrize(
    "payload,expected_status",
    [
        (
            {"email": "unknown@test.com", "password": "Password123!"},
            401
        ),
        (
            {"email": VALID_USER.email, "password": "wrong_password"},
            401
        ),
        (
            {"email": "", "password": ""},
            400
        ),
        (
            {"email": "not_an_email", "password": "Password123!"},
            400
        ),
    ]
)
def test_login_negative_matrix(api_client, payload, expected_status):
    """
    Negative login scenarios.
    """

    response = api_client.post(LOGIN_ENDPOINT, payload)

    assert response.status_code == expected_status


@pytest.mark.functional
def test_login_error_response_discovery(api_client):
    """
    Contract discovery test (safe JSON handling).
    """

    response = api_client.post(
        LOGIN_ENDPOINT,
        {"email": "fake@test.com", "password": "wrong_password"}
    )

    print("\nSTATUS:", response.status_code)
    print("BODY:", response.text)

    assert response.status_code in [400, 401]


@pytest.mark.security
def test_login_does_not_expose_internal_errors(api_client):

    response = api_client.post(
        LOGIN_ENDPOINT,
        {"email": "", "password": ""}
    )

    body = response.text.lower()

    forbidden = [
        "sequelize",
        "exception",
        "stack",
        "trace",
        "syntaxerror",
        "referenceerror"
    ]

    for item in forbidden:
        assert item not in body