import pytest
import re
from playwright.sync_api import Page, expect, sync_playwright
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from config.test_data import UserCredentials, generate_unique_email
from utils.db_handler import DBHandler

@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as p:
        # Standardized on chromium per Engineering Strategy[cite: 4]
        browser = p.chromium.launch(headless=False) 
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def db_handler():
    return DBHandler()

@pytest.fixture(scope="function")
def page(browser, base_url):
    """
    Zero-State Leakage strategy: Injects base_url into context[cite: 2].
    """
    context = browser.new_context(base_url=base_url)
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def login_page(page):
    return LoginPage(page)

@pytest.fixture(scope="function")
def register_page(page):
    return RegisterPage(page)

@pytest.fixture(scope="function")
def ui_seeded_user(page: Page, register_page: RegisterPage, db_handler: DBHandler) -> UserCredentials:
    """
    UI-driven user seeding fixture.
    Creates a unique user via the Registration UI before the test.
    This ensures the user is fully 'real' in the system context.
    """
    password = "Password123!"
    email = generate_unique_email(prefix="ui_test")
    credentials = UserCredentials(email=email, password=password)
    security_answer = "Answer123"

    # 1. Setup: Register via UI
    register_page.navigate()
    register_page.register_new_user(credentials.email, credentials.password, security_answer)
    
    # Verification that registration succeeded via UI (e.g., redirect or success message)
    # In Juice Shop, registration usually redirects to the home/login page.
    expect(page).to_have_url(re.compile(r".*/login"))

    yield credentials

    # 2. Teardown: (Best effort) Cleanup is harder via UI without an admin account.
    # For this prototype, we rely on the unique email to avoid collisions.
    # In a production-grade setup, we would use an API call here.
    pass
