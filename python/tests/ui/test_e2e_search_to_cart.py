import pytest
from playwright.sync_api import Page, expect

from config.test_data import (
    UserCredentials,
    generate_unique_email
)

from pages.login_page import LoginPage
from pages.register_page import RegisterPage
from pages.search_page import SearchPage
from pages.cart_page import CartPage


@pytest.fixture(scope="function")
def login_page_instance(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def register_page_instance(page: Page) -> RegisterPage:
    return RegisterPage(page)


@pytest.fixture(scope="function")
def search_page_instance(page: Page) -> SearchPage:
    return SearchPage(page)


@pytest.fixture(scope="function")
def cart_page_instance(page: Page) -> CartPage:
    return CartPage(page)


def test_search_and_product_interaction_flow(
    page: Page,
    register_page_instance: RegisterPage,
    login_page_instance: LoginPage,
    search_page_instance: SearchPage,
    cart_page_instance: CartPage
) -> None:
    """
    Sprint 2 Core E2E Regression:
    Traces user onboarding, catalog navigation, collection mutations, 
    and UI feedback confirmation states within a unified session lifecycle.
    """

    # Data Initialization
    password = "Password123!"
    email = generate_unique_email(prefix="miguel_flow")
    credentials = UserCredentials(email=email, password=password)
    security_answer = "Answer123"
    target_product = "Apple Juice"

    # Profile Setup Phase
    register_page_instance.navigate()
    register_page_instance.register_new_user(
        credentials.email,
        credentials.password,
        security_answer
    )

    # Authentication Session Hook
    login_page_instance.navigate()
    login_page_instance.login(
        credentials.email,
        credentials.password
    )

    # Marketplace Query Execution
    search_page_instance.search_for(target_product)
    # Refactored: Assertion executed at the test layer
    expect(search_page_instance.get_product_card(target_product)).to_be_visible()

    # Cart State Manipulation
    search_page_instance.add_product_to_basket_direct(target_product)

    # Asynchronous Toast Alert Interception
    # Refactored: Assertion executed at the test layer
    expect(search_page_instance.get_success_snackbar_locator()).to_contain_text(f"Placed {target_product}")

    # Navigation Context Pivot
    cart_page_instance.open_cart()

    # Final Inventory Summary Assertion
    # Refactored: Assertion executed at the test layer
    expect(cart_page_instance.get_cart_item(target_product)).to_be_visible()