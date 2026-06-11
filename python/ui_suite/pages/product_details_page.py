from playwright.sync_api import Page, Locator
from .base_page import BasePage

class ProductDetailsPage(BasePage):
    """
    Models the modal container that displays individual item information 
    and handles nested verification layers like review lists and picture rendering.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.product_dialog = self.page.locator(
            "mat-dialog-container"
        )

        self.product_title = self.product_dialog.get_by_role(
            "heading"
        )

        self.product_image = self.product_dialog.get_by_role(
            "img"
        )

        self.product_price = self.product_dialog.locator(
            "p"
        )

        self.reviews_button = self.product_dialog.get_by_role(
            "button",
            name="Reviews"
        )

        self.close_dialog_button = self.product_dialog.get_by_role(
            "button",
            name="Close Dialog"
        )

    def get_dialog_locator(self) -> Locator:
        """Exposes the primary dynamic container overlay context."""
        return self.product_dialog

    def get_product_title_locator(self) -> Locator:
        """Exposes the main layout description card item title component."""
        return self.product_title

    def get_product_image_locator(self) -> Locator:
        """Exposes asset graphic target regions inside information grids."""
        return self.product_image

    def get_product_price_locator(self) -> Locator:
        """Exposes pricing cluster text indicators."""
        return self.product_price.first

    def get_reviews_button_locator(self) -> Locator:
        """Exposes interactive feedback link components."""
        return self.reviews_button

    def close_dialog(self) -> None:
        """Closes the active product overview modal to return back to catalog grid exploration."""
        self.close_dialog_button.click()