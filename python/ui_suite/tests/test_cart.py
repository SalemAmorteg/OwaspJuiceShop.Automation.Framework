import pytest

from playwright.sync_api import Page, expect

from ui_suite.config.test_data import (
    UserCredentials,
    generate_unique_email
)

from ui_suite.pages.register_page import RegisterPage
from ui_suite.pages.login_page import LoginPage
from ui_suite.pages.search_page import SearchPage
from ui_suite.pages.cart_page import CartPage


@pytest.fixture(scope="function")
def register_page_instance(page: Page) -> RegisterPage:
    return RegisterPage(page)


@pytest.fixture(scope="function")
def login_page_instance(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture(scope="function")
def search_page_instance(page: Page) -> SearchPage:
    return SearchPage(page)


@pytest.fixture(scope="function")
def cart_page_instance(page: Page) -> CartPage:
    return CartPage(page)


def create_and_login_user(
    register_page_instance,
    login_page_instance
):
    """
    Common macro function to build a clean state profile before executing 
    isolated transactional commerce operations.
    """

    email = generate_unique_email(
        prefix="cart_test"
    )

    password = "Password123!"

    register_page_instance.navigate()

    register_page_instance.register_new_user(
        email,
        password,
        "Answer123"
    )

    login_page_instance.navigate()

    login_page_instance.login(
        email,
        password
    )


def test_add_single_item_to_cart(
    register_page_instance,
    login_page_instance,
    search_page_instance,
    cart_page_instance
):
    """
    Validates the standard commerce path for item additions.
    Ensures addition mutations persist when pivoting focus to the cart tables.
    """

    create_and_login_user(
        register_page_instance,
        login_page_instance
    )

    search_page_instance.search_for(
        "Apple Juice"
    )

    search_page_instance.add_product_to_basket_direct(
        "Apple Juice"
    )

    cart_page_instance.open_cart()

    # Refactored: Assertion executed at the test layer via locator abstraction
    expect(cart_page_instance.get_cart_item("Apple Juice")).to_be_visible()


def test_increase_quantity(
    register_page_instance,
    login_page_instance,
    search_page_instance,
    cart_page_instance
):
    """
    Validates transactional inventory updates inside the basket layout.
    Ensures increments trigger recalculations of the item row count state.
    """

    create_and_login_user(
        register_page_instance,
        login_page_instance
    )

    search_page_instance.search_for(
        "Apple Juice"
    )

    search_page_instance.add_product_to_basket_direct(
        "Apple Juice"
    )

    cart_page_instance.open_cart()

    cart_page_instance.increase_quantity(
        "Apple Juice"
    )

    # Refactored: Assertion executed at the test layer via locator abstraction
    expect(cart_page_instance.get_quantity_cell("Apple Juice")).to_have_text(
        "2"
    )


def test_remove_product(
    register_page_instance,
    login_page_instance,
    search_page_instance,
    cart_page_instance
):
    """
    Validates complete line-item drop actions.
    Ensures row deletion transitions the component state back to empty.
    """

    create_and_login_user(
        register_page_instance,
        login_page_instance
    )

    search_page_instance.search_for(
        "Apple Juice"
    )

    search_page_instance.add_product_to_basket_direct(
        "Apple Juice"
    )

    cart_page_instance.open_cart()

    cart_page_instance.remove_product(
        "Apple Juice"
    )

    # Refactored: Assertion executed at the test layer via locator abstraction
    expect(cart_page_instance.get_cart_rows_locator()).to_have_count(0)