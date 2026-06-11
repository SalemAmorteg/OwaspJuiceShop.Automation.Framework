import pytest
from pydantic import ValidationError
from python.api_suite.models.auth_models import UserSchema, LoginResponseSchema

def test_user_registration_contract_and_validation(api_client, user_factory):
    """
    Validates that a POST request to /api/Users creates a user, maps against 
    the Pydantic UserSchema, and safely enforces boundary errors on duplicates.
    """
    # 1. Arrange: Generate unique identity payload credentials
    payload = user_factory()
    
    # 2. Act: Execute registration request sequence
    response = api_client.register_user(payload)
    
    # 3. Assert: Validate status code protocols
    assert response.status_code == 201
    
    # 4. Assert: Extract and validate data payload block against Pydantic definitions
    user_data = response.json().get("data")
    try:
        validated_user = UserSchema(**user_data)
        assert validated_user.email == payload["email"]
    except ValidationError as e:
        pytest.fail(f"User registration response failed data contract validation: {e}")

    # 5. Assert: Re-send same payload configuration to validate duplicate data restrictions (400 or 422 processing)
    duplicate_response = api_client.register_user(payload)
    assert duplicate_response.status_code in [400, 422], "Security Flaw: Database accepted duplicate email entry."


def test_user_login_contract_and_boundaries(api_client, user_factory):
    """
    Validates token payload integrity returned on POST /rest/user/login 
    and checks that unauthorized parameters are securely rejected.
    """
    # 1. Arrange: Register an active user profile
    credentials = user_factory()
    reg_response = api_client.register_user(credentials)
    assert reg_response.status_code == 201

    # 2. Act: Attempt authenticating against the workspace with valid credentials
    login_payload = {"email": credentials["email"], "password": credentials["password"]}
    response = api_client.login_user(login_payload)
    
    # 3. Assert: Verify backend acceptance status
    assert response.status_code == 200
    
    # 4. Assert: Validate data response structure using the LoginResponseSchema contract
    response_json = response.json()
    try:
        validated_login = LoginResponseSchema(**response_json)
        assert validated_login.authentication.umail == credentials["email"]
        assert len(validated_login.authentication.token) > 20, "Security Risk: Authentication token is invalid or truncated."
    except ValidationError as e:
        pytest.fail(f"Login response payload failed validation contract schemas: {e}")

    # 5. Assert: Verify security response behavior using invalid credentials
    bad_login_payload = {"email": credentials["email"], "password": "wrong_password_123"}
    failed_response = api_client.login_user(bad_login_payload)
    
    assert failed_response.status_code == 401
    assert "Exception" not in failed_response.text, "Information Leakage Flaw: System stacktrace structural print leaked out."