from playwright.sync_api import Page, Locator
from .base_page import BasePage

class CartPage(BasePage):
    """
    Encapsulates interactions within the core shopping cart layout, 
    managing quantities, item line-item isolation, and checkout state verification.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_button = self.page.get_by_role(
            "button",
            name="Show the shopping cart"
        )

        self.cart_rows = self.page.locator(
            "mat-row"
        )

        self.total_price_text = self.page.get_by_text(
            "Total Price:"
        )

    def open_cart(self) -> None:
        """Navigates directly to the cart interface via the main application header."""
        self.cart_button.wait_for(
            state="visible"
        )
        self.cart_button.click()

    def get_cart_item(self, product_name: str) -> Locator:
        """Returns the locator context matching a single product row item."""
        return self.cart_rows.filter(has_text=product_name)

    def increase_quantity(self, product_name: str) -> None:
        """Locates the line item container and increments its count by one unit."""
        cart_item = self.get_cart_item(product_name)
        plus_button = cart_item.locator("button").nth(1)
        plus_button.click()

    def decrease_quantity(self, product_name: str) -> None:
        """Locates the line item container and decrements its count by one unit."""
        cart_item = self.get_cart_item(product_name)
        minus_button = cart_item.locator("button").first
        minus_button.click()

    def get_quantity_cell(self, product_name: str) -> Locator:
        """Returns the relative mat-cell locator context containing item counts."""
        cart_item = self.get_cart_item(product_name)
        return cart_item.locator("mat-cell").nth(2)

    def get_total_price_locator(self) -> Locator:
        """Exposes the summary label locator for total cost computations."""
        return self.total_price_text

    def get_cart_rows_locator(self) -> Locator:
        """Exposes the collection of row indicators inside the data matrix."""
        return self.cart_rows

    def remove_product(self, product_name: str) -> None:
        """Deletes a selected row entirely using the contextual removal option."""
        cart_item = self.get_cart_item(product_name)
        delete_button = cart_item.locator("button").nth(2)
        delete_button.click()