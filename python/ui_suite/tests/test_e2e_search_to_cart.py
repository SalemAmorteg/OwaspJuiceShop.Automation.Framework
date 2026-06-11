import pytest
import re
from playwright.sync_api import Page, expect

from ui_suite.config.test_data import UserCredentials
from ui_suite.pages.login_page import LoginPage
from ui_suite.pages.register_page import RegisterPage
from ui_suite.pages.search_page import SearchPage
from ui_suite.pages.cart_page import CartPage

@pytest.fixture(scope="function")
def login_page_instance(page: Page) -> LoginPage: return LoginPage(page)
@pytest.fixture(scope="function")
def register_page_instance(page: Page) -> RegisterPage: return RegisterPage(page)
@pytest.fixture(scope="function")
def search_page_instance(page: Page) -> SearchPage: return SearchPage(page)
@pytest.fixture(scope="function")
def cart_page_instance(page: Page) -> CartPage: return CartPage(page)

def test_search_and_product_interaction_flow(
    authenticated_page: Page,
    login_page_instance: LoginPage,
    search_page_instance: SearchPage,
    cart_page_instance: CartPage,
    session_ui_seeded_user: UserCredentials
) -> None:
    """
    Sprint 2 Core E2E Regression:
    Traces user onboarding, catalog navigation, collection mutations, 
    and UI feedback confirmation states within a unified session lifecycle.
    """

    # Data Initialization (Using session-scoped credentials)
    target_product = "Apple Juice"

    # Authentication Session Hook (REMOVED - Now handled by authenticated_page fixture)

    # Ensure UI hydration before searching
    expect(search_page_instance.search_trigger).to_be_visible()

    # Marketplace Query Execution
    search_page_instance.search_for(target_product)
    expect(search_page_instance.get_product_card(target_product)).to_be_visible()

    # Cart State Manipulation
    search_page_instance.add_product_to_basket_direct(target_product)

    # Asynchronous Toast Alert Interception
    expect(search_page_instance.get_success_snackbar_locator()).to_contain_text(f"Placed {target_product}")

    # Navigation Context Pivot
    cart_page_instance.open_cart()

    # Final Inventory Summary Assertion
    expect(cart_page_instance.get_cart_item(target_product)).to_be_visible()