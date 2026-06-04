from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class RegisterPage(BasePage):
    """
    Encapsulates user account signup form registration flows, managing input focus validation, 
    and Angular select list picker mechanics.
    """
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input = page.get_by_role("textbox", name="Email address field")
        self.password_input = page.get_by_role("textbox", name="Field for the password")
        self.repeat_password_input = page.get_by_role("textbox", name="Field to confirm the password")
        self.security_question_dropdown = page.get_by_role("combobox", name="Selection list for the")
        self.security_answer_input = page.get_by_role("textbox", name="Field for the answer to the")
        self.register_button = page.get_by_role("button", name="Button to complete the")

    def navigate(self) -> None:
        """Directly updates routing history context to point to the registration page path."""
        super().navigate("register")

    def register_new_user(self, email: str, password: str, security_answer: str) -> None:
        """Completes account creation profiles by filling fields and selecting a security recovery fallback."""
        # Concurrency Protection: Sweep and clear any delayed welcome banners 
        # before interacting with the initial form element.
        self.dismiss_initial_overlays()
        
        # Enforce defensive verification gates before interactions
        self.email_input.wait_for(state="visible")
        self.email_input.fill(email)
        
        self.password_input.fill(password)
        
        # Secondary sweep check before filling password confirmations
        self.dismiss_initial_overlays()
        self.repeat_password_input.fill(password)
        
        # Final sweep check right before interacting with the dropdown field
        self.dismiss_initial_overlays()
        self.security_question_dropdown.wait_for(state="visible")
        self.security_question_dropdown.click()
        
        self.page.locator("mat-option").first.wait_for(state="visible")
        self.page.locator("mat-option").first.click()
        
        self.security_answer_input.fill(security_answer)
        
        self.register_button.wait_for(state="visible")
        self.register_button.click()