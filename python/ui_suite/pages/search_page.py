from playwright.sync_api import (
    Page,
    Locator
)

from .base_page import BasePage


class SearchPage(BasePage):
    """
    Encapsulates catalog search interactions,
    product discovery,
    and cart actions.
    """

    def __init__(
        self,
        page: Page
    ):
        super().__init__(page)

        self.search_trigger = page.get_by_label(
            "Click to search"
        )

        self.search_input = page.get_by_role(
            "textbox"
        )

        self.product_cards = page.locator(
            "mat-card"
        )

        self.success_snackbar = page.locator(
            "simple-snack-bar"
        ).last

    # ---------------------------------------------------------------------
    # Search
    # ---------------------------------------------------------------------

    def search_for(
        self,
        term: str
    ) -> None:

        if not self.search_input.is_visible():

            self.search_trigger.click()

        self.search_input.fill(term)

    # ---------------------------------------------------------------------
    # Locators
    # ---------------------------------------------------------------------

    def get_product_card(
        self,
        product_name: str
    ) -> Locator:

        return self.product_cards.filter(
            has_text=product_name
        ).first

    def get_all_product_cards_locator(
        self
    ) -> Locator:

        return self.product_cards

    def get_success_snackbar_locator(
        self
    ) -> Locator:

        return self.success_snackbar

    # ---------------------------------------------------------------------
    # Actions
    # ---------------------------------------------------------------------

    def add_product_to_basket_direct(
        self,
        product_name: str
    ) -> None:

        product_card = self.get_product_card(
            product_name
        )

        product_card.get_by_role(
            "button",
            name="Add to Basket"
        ).click()

    def open_product(
        self,
        product_name: str
    ) -> None:

        product_card = self.get_product_card(
            product_name
        )

        product_card.locator(
            ".product"
        ).click()