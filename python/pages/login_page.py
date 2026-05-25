from playwright.sync_api import Page
from pages.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        # Locator priority: Role -> Label -> Text[cite: 2]
        self.email_input = page.get_by_role("textbox", name="Text field for the login email")
        self.password_input = page.get_by_role("textbox", name="Text field for the login password")
        self.login_button = page.get_by_role("button", name="Login", exact=True) 
        self.error_message = page.get_by_text("Invalid email or password.")

    def navigate(self) -> None:
        """Standardized override for the Login route[cite: 1]."""
        super().navigate("login")

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.login_button.click()