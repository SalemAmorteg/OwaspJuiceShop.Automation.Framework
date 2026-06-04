import pytest
import re
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from config.test_data import UserCredentials, generate_unique_email
from utils.db_handler import DBHandler

@pytest.fixture(scope="function")
def login_page_instance(page):
    return LoginPage(page)

def test_successful_login_with_ui_seeded_user(ui_seeded_user: UserCredentials, login_page_instance: LoginPage, page: Page, db_handler: DBHandler):
    """
    Validates happy-path authentication states via dynamic fixture injection.
    Performs cross-layer validations between UI session states and persistent storage values.
    """
    email = ui_seeded_user.email
    password = ui_seeded_user.password

    login_page_instance.navigate()
    login_page_instance.login(email, password)

    # Confirms routing transition was processed correctly
    expect(page).to_have_url(re.compile(r".*/search"))

    # Confirms state hydration completed cleanly before ending the check
    expect(page.get_by_role("button", name="Show the shopping cart")).to_be_visible(timeout=10000)

    # Verifies that persistence tracking aligns with active interface layers
    user_in_db = db_handler.get_user_by_email(email)
    assert user_in_db is not None, f"User {email} was not found in the database after successful login."
    assert user_in_db['email'] == email

def test_unsuccessful_login_with_invalid_credentials(login_page_instance: LoginPage):
    """
    Negative Path: Asserts system resilience and rejection handling 
    when provided with untrusted or non-matching auth criteria.
    """
    invalid_email = "nonexistent_user_999@juice-sh.op"
    invalid_pass = "wrong_pass"

    login_page_instance.navigate()
    login_page_instance.login(invalid_email, invalid_pass)
    
    # Refactored: Assertion executed via locator getter exposure
    expect(login_page_instance.get_error_message_locator()).to_be_visible()