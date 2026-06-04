import pytest

from playwright.sync_api import Page, expect

from pages.search_page import SearchPage
from pages.product_details_page import ProductDetailsPage


@pytest.fixture(scope="function")
def search_page_instance(page: Page) -> SearchPage:
    return SearchPage(page)


@pytest.fixture(scope="function")
def product_details_page_instance(
    page: Page
) -> ProductDetailsPage:
    return ProductDetailsPage(page)


def test_product_details_displayed(
    search_page_instance: SearchPage,
    product_details_page_instance: ProductDetailsPage
) -> None:
    """
    Validates dialog layout visibility boundaries.
    Ensures that dynamic info text fragments render properly under focus.
    """

    target_product = "Apple Juice"

    search_page_instance.navigate()

    search_page_instance.search_for(
        target_product
    )

    search_page_instance.open_product(
        target_product
    )

    # Refactored: Assertions elevated to the test module layout
    expect(product_details_page_instance.get_dialog_locator()).to_be_visible()

    expect(product_details_page_instance.get_product_title_locator()).to_be_visible()

    expect(product_details_page_instance.get_product_title_locator()).to_contain_text(
        target_product
    )


def test_product_image_visible(
    search_page_instance: SearchPage,
    product_details_page_instance: ProductDetailsPage
) -> None:
    """
    Validates dynamic media asset attachment properties within descriptive panels.
    """

    target_product = "Apple Juice"

    search_page_instance.navigate()

    search_page_instance.search_for(
        target_product
    )

    search_page_instance.open_product(
        target_product
    )

    # Refactored: Assertion handled at test layer
    expect(product_details_page_instance.get_product_image_locator()).to_be_visible()


def test_product_reviews_button_visible(
    search_page_instance: SearchPage,
    product_details_page_instance: ProductDetailsPage
) -> None:
    """
    Validates interaction target entrypoints for social feedback listings.
    """

    target_product = "Apple Juice"

    search_page_instance.navigate()

    search_page_instance.search_for(
        target_product
    )

    search_page_instance.open_product(
        target_product
    )

    # Refactored: Assertion handled at test layer
    expect(product_details_page_instance.get_reviews_button_locator()).to_be_visible()


def test_product_price_visible(
    search_page_instance: SearchPage,
    product_details_page_instance: ProductDetailsPage
) -> None:
    """
    Validates accuracy of currency visibility controls within descriptions.
    """

    target_product = "Apple Juice"

    search_page_instance.navigate()

    search_page_instance.search_for(
        target_product
    )

    search_page_instance.open_product(
        target_product
    )

    # Refactored: Assertion handled at test layer
    expect(product_details_page_instance.get_product_price_locator()).to_be_visible()