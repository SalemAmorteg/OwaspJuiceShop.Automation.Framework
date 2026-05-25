import pytest
import re
from playwright.sync_api import Page, expect
from pages.register_page import RegisterPage
from pages.login_page import LoginPage
from config.test_data import UserCredentials, generate_unique_email
from utils.db_handler import DBHandler

@pytest.fixture(scope="function")
def registration_user(page: Page, register_page: RegisterPage, db_handler: DBHandler) -> UserCredentials:
    """
    Custom fixture for registration-specific seeding.
    Uses the UI to register a user and verifies DB persistence.
    """
    password = "SecurePassword123!"
    email = generate_unique_email(prefix="reg_test")
    credentials = UserCredentials(email=email, password=password)
    security_answer = "Mariana"

    # 1. Setup: Register via UI
    register_page.navigate()
    register_page.register_new_user(credentials.email, credentials.password, security_answer)

    # Verify successful redirect
    expect(page).to_have_url(re.compile(r".*/login"))

    # 2. Validate Persistence (The Backend Assertion)
    user_in_db = db_handler.get_user_by_email(credentials.email)
    assert user_in_db is not None, f"User {credentials.email} was not found in the database after registration."
    assert user_in_db['password'] != credentials.password, "SECURITY RISK: Password not hashed."
    
    yield credentials

    # 3. Teardown: (Best effort)
    pass

def test_new_user_registration_lifecycle(registration_user: UserCredentials, login_page: LoginPage, page: Page):
    """
    Integration Test: Verifies the full lifecycle of a new user from registration to login.
    """
    # 1. Arrange: User is already registered via the fixture
    email = registration_user.email
    password = registration_user.password

    # 2. Act: Perform a login with the newly registered user
    login_page.navigate()
    login_page.login(email, password)

    # 3. Assert: Verify successful login
    expect(page).to_have_url(re.compile(r".*/search"))