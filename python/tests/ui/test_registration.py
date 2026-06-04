import pytest
import re
from playwright.sync_api import Page, expect
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from config.test_data import UserCredentials, generate_unique_email
from utils.db_handler import DBHandler

@pytest.fixture(scope="function")
def registration_user(
    page: Page, 
    register_page_instance: RegisterPage, 
    db_handler: DBHandler
) -> UserCredentials:
    """
    Handles user onboarding orchestrations directly via front-end flows.
    Executes core validation tasks against internal security schemas during initialization.
    """
    password = "SecurePassword123!"
    email = generate_unique_email(prefix="reg_test")
    credentials = UserCredentials(email=email, password=password)
    security_answer = "Mariana"

    # Registration sequence trigger
    register_page_instance.navigate()
    register_page_instance.register_new_user(
        credentials.email, 
        credentials.password, 
        security_answer
    )

    expect(page).to_have_url(re.compile(r".*/login"))

    # Backend Hashing & Identity Persistence Checks
    user_in_db = db_handler.get_user_by_email(credentials.email)
    assert user_in_db is not None, f"User {credentials.email} was not found in the database after registration."
    assert user_in_db['password'] != credentials.password, "SECURITY RISK: Password not hashed."
    
    yield credentials

    pass


def test_new_user_registration_lifecycle(
    registration_user: UserCredentials, 
    login_page_instance: LoginPage, 
    page: Page
) -> None:
    """
    Integration Sweep: Confirms end-to-end credential usability,
    ensuring newly established records execute authentications smoothly.
    """
    email = registration_user.email
    password = registration_user.password

    login_page_instance.navigate()
    login_page_instance.login(email, password)

    expect(page).to_have_url(re.compile(r".*/search"))