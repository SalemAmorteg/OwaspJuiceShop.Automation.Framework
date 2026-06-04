import pytest
from playwright.sync_api import Page, expect
from pages.search_page import SearchPage


@pytest.fixture(scope="function")
def search_page_instance(page: Page) -> SearchPage:
    """Provides a fresh, isolated SearchPage instance per test execution."""
    return SearchPage(page)


def test_search_existing_product(
    search_page_instance: SearchPage
) -> None:
    """
    Positive Path Validation:
    Verifies catalog filtering mechanism accurately isolates and returns 
    matching product records when provided with valid standard alphanumeric queries.
    """

    search_page_instance.navigate()

    search_page_instance.search_for(
        "Apple Juice"
    )

    # Refactored: Assertion elevated to the test file
    expect(search_page_instance.get_product_card("Apple Juice")).to_be_visible()


def test_search_nonexistent_product(
    search_page_instance: SearchPage
) -> None:
    """
    Negative Path Validation:
    Asserts application boundary behavior when a search query yields zero matches, 
    ensuring the interface handles empty results states cleanly without DOM exceptions.
    """

    search_page_instance.navigate()

    search_page_instance.search_for(
        "product_that_does_not_exist_12345"
    )

    # Refactored: Assertion elevated to the test file
    expect(search_page_instance.get_all_product_cards_locator()).to_have_count(0)


def test_search_special_characters(
    search_page_instance: SearchPage
) -> None:
    """
    Edge Case Input Validation:
    Evaluates system resilience against special symbol string streams, 
    ensuring character sanitization or exact-match query filters execute safely 
    without disrupting the presentation layer structure.
    """

    search_page_instance.navigate()

    search_page_instance.search_for(
        "@#$%^&*"
    )

    # Refactored: Assertion elevated to the test file
    expect(search_page_instance.get_all_product_cards_locator()).to_have_count(0)