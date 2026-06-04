from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class LoginPage(BasePage):
    """
    Manages authentication view inputs, form submittals, and error message tracking.
    """
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        
        self.email_input = page.get_by_role("textbox", name="Text field for the login email")
        self.password_input = page.get_by_role("textbox", name="Text field for the login password")
        self.login_button = page.get_by_role("button", name="Login", exact=True) 
        self.error_message = page.get_by_text("Invalid email or password.")

    def navigate(self) -> None:
        """Forces immediate navigation to the authentication endpoint routing path."""
        super().navigate("login")

    def login(self, email: str, password: str) -> None:
        """Populates credential input forms and executes authentication submittal."""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_message_locator(self) -> Locator:
        """Exposes the error label text field for assertion layers."""
        return self.error_message