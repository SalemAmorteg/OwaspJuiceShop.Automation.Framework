from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class RegisterPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input = page.get_by_role("textbox", name="Email address field")
        self.password_input = page.get_by_role("textbox", name="Field for the password")
        self.repeat_password_input = page.get_by_role("textbox", name="Field to confirm the password")
        self.security_question_dropdown = page.get_by_role("combobox", name="Selection list for the")
        self.security_answer_input = page.get_by_role("textbox", name="Field for the answer to the")
        self.register_button = page.get_by_role("button", name="Button to complete the")

    def navigate(self) -> None:
        """Standardized override for the Register route[cite: 1]."""
        super().navigate("register")

    def register_new_user(self, email: str, password: str, security_answer: str) -> None:
        self.email_input.fill(email)
        self.email_input.press("Tab") 
        self.password_input.fill(password)
        self.repeat_password_input.fill(password)
        
        self.security_question_dropdown.click()
        self.page.get_by_role("option").first.click()
        self.security_answer_input.fill(security_answer)
        
        expect(self.register_button).to_be_enabled(timeout=7000)
        self.register_button.click()