import pytest
import re
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from config.test_data import UserCredentials, generate_unique_email
from utils.db_handler import DBHandler

# -----------------------------------------------------------------------------
# Configuration Hooks 
# -----------------------------------------------------------------------------

def pytest_configure(config):
    """
    Hooks into global pytest initialization properties.
    Manages runtime profile changes or cross-process variables for worker pools.
    """
    pass

# -----------------------------------------------------------------------------
# Core Infrastructure & Database Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture(scope="function")
def db_handler() -> DBHandler:
    """Exposes low-level transaction handlers to manage assertions or clean up state records."""
    return DBHandler()

# -----------------------------------------------------------------------------
# Page Object Injection Layer (Strict POM Separation)
# -----------------------------------------------------------------------------

@pytest.fixture(scope="function")
def login_page_instance(page: Page) -> LoginPage:
    """Instantiates a distinct login interface layer within the current session context."""
    return LoginPage(page)


@pytest.fixture(scope="function")
def register_page_instance(page: Page) -> RegisterPage:
    """Instantiates a distinct sign-up interface layer within the current session context."""
    return RegisterPage(page)


@pytest.fixture(scope="function")
def search_page_instance(page: Page) -> SearchPage:
    """Instantiates a distinct marketplace filter layer within the current session context."""
    return SearchPage(page)


@pytest.fixture(scope="function")
def cart_page_instance(page: Page) -> CartPage:
    """Instantiates a distinct checkout collection layer within the current session context."""
    return CartPage(page)

# -----------------------------------------------------------------------------
# Data Seeding & Setup Orchestration
# -----------------------------------------------------------------------------

@pytest.fixture(scope="function")
def ui_seeded_user(
    page: Page, 
    register_page_instance: RegisterPage, 
    db_handler: DBHandler
) -> UserCredentials:
    """
    Seeding Hook: Directs an interactive workflow to create an active user identity.
    Enforces automated targeted removals post-execution to avoid local state pollution.
    """
    password = "Password123!"
    email = generate_unique_email(prefix="ui_test")
    credentials = UserCredentials(email=email, password=password)
    security_answer = "Answer123"

    # Orchestrates the front-end profile creation process
    register_page_instance.navigate()
    register_page_instance.register_new_user(
        credentials.email, 
        credentials.password, 
        security_answer
    )
    
    expect(page).to_have_url(re.compile(r".*/login"))

    yield credentials

    # Teardown Sequence: Sweeps data remnants to maintain consistent parallel worker runs
    try:
        db_handler.delete_user_by_email(credentials.email)
    except Exception as e:
        print(f"\n[WARNING] Background cleanup failed for user {credentials.email}: {str(e)}")