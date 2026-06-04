from playwright.sync_api import Page, Locator
from .base_page import BasePage

class SearchPage(BasePage):
    """
    Manages catalog filtering queries, handling visibility shifts on expansion toggles, 
    and bulk list verification layers across the marketplace results view.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.search_trigger = self.page.get_by_label(
            "Click to search"
        )

        self.search_input = (
            self.search_trigger.locator("input")
        )

        self.product_cards = self.page.locator(
            "mat-card"
        )

        self.success_snackbar = (
            self.page.locator(
                "simple-snack-bar"
            ).last
        )

    def search_for(
        self,
        term: str
    ) -> None:
        """
        Submits product criteria lookups. Uses defensive wait assertions to safely interact 
        with the layout whether the search box is currently closed or already open.
        """
        # Concurrency Protection: Sweep and clear any delayed welcome banners
        # that might have lagged during the initial page navigation load.
        self.dismiss_initial_overlays()

        # Enforce actionability on the search icon button container
        self.search_trigger.wait_for(state="visible")

        # Expands search input if it is hidden from view behind the navigation header icon
        if not self.search_input.is_visible():
            self.search_trigger.click()

        self.search_input.wait_for(state="visible")
        
        self.search_input.fill(term)
        self.search_input.press("Enter")

    def get_product_card(self, product_name: str) -> Locator:
        """Returns the container locator target representing a specific catalog card item."""
        return self.product_cards.filter(has_text=product_name).first

    def get_all_product_cards_locator(self) -> Locator:
        """Exposes the comprehensive item grid locator reference."""
        return self.product_cards

    def get_success_snackbar_locator(self) -> Locator:
        """Exposes the contextual feedback alert banner locator."""
        return self.success_snackbar

    def add_product_to_basket_direct(
        self,
        product_name: str
    ) -> None:
        """Triggers quick cart addition options directly from the primary product listing grid card."""
        target_card = self.get_product_card(product_name)
        basket_button = target_card.get_by_label("Add to Basket")
        basket_button.click()

    def open_product(
        self,
        product_name: str
    ) -> None:
        """Opens information card summaries from target item grids to show deep product options."""
        target_card = self.get_product_card(product_name)
        details_button = target_card.get_by_label("Click for more information")
        details_button.click()