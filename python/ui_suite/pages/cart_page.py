from playwright.sync_api import Page, Locator, expect
from .base_page import BasePage


class CartPage(BasePage):

    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_button = page.get_by_role(
            "button",
            name="Show the shopping cart"
        )

        self.cart_rows = page.locator("mat-row")

        self.total_price = page.get_by_text(
            "Total Price:"
        )

    def open_cart(self) -> None:

        self.cart_button.click()

        expect(
            self.cart_rows.first
        ).to_be_visible(timeout=10000)

    def get_cart_item(
        self,
        product_name: str
    ) -> Locator:

        return self.cart_rows.filter(
            has=self.page.get_by_text(
                product_name,
                exact=True
            )
        )

    def increase_quantity(
        self,
        product_name: str
    ) -> None:

        row = self.get_cart_item(product_name)

        row.locator("button").nth(1).click()

    def decrease_quantity(
        self,
        product_name: str
    ) -> None:

        row = self.get_cart_item(product_name)

        row.locator("button").nth(0).click()

    def remove_product(
        self,
        product_name: str
    ) -> None:

        row = self.get_cart_item(product_name)

        row.locator("button").nth(2).click()

    def get_quantity_cell(
        self,
        product_name: str
    ) -> Locator:

        row = self.get_cart_item(product_name)

        return row.locator("mat-cell").nth(2)

    def get_total_price_locator(self) -> Locator:

        return self.total_price

    def get_cart_rows_locator(self) -> Locator:

        return self.cart_rows