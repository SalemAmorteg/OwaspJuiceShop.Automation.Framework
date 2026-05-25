import pytest
import re
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from config.test_data import UserCredentials, generate_unique_email
from utils.db_handler import DBHandler

@pytest.fixture(scope="function")
def login_page(page):
    return LoginPage(page)

def test_successful_login_with_ui_seeded_user(ui_seeded_user: UserCredentials, login_page: LoginPage, page: Page, db_handler: DBHandler):
    """
    Validates successful authentication using a dynamically seeded UI user.
    Ensures the user is correctly persisted in the database.
    """
    # 1. Arrange: User is already seeded by the 'ui_seeded_user' fixture
    email = ui_seeded_user.email
    password = ui_seeded_user.password

    # 2. Act
    login_page.navigate()
    login_page.login(email, password)

    # 3. Assert: Web-First Assertions
    # Verify URL transition
    expect(page).to_have_url(re.compile(r".*/search"))

    # Verify Session Hydration (The Shopping Cart)
    expect(page.get_by_role("button", name="Show the shopping cart")).to_be_visible(timeout=10000)

    # 4. Backend Assertion: Verify user exists in DB
    user_in_db = db_handler.get_user_by_email(email)
    assert user_in_db is not None, f"User {email} was not found in the database after successful login."
    assert user_in_db['email'] == email

def test_unsuccessful_login_with_invalid_credentials(login_page: LoginPage):
    """
    Negative path: Validates system resilience against incorrect credentials.
    Uses a known non-existent email pattern.
    """
    # 1. Arrange: Use a known non-existent email pattern
    invalid_email = "nonexistent_user_999@juice-sh.op"
    invalid_pass = "wrong_pass"

    # 2. Act
    login_page.navigate()
    login_page.login(invalid_email, invalid_pass)
    
    # 3. Assert
    expect(login_page.error_message).to_be_visible()
