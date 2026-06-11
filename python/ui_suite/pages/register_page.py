from playwright.sync_api import Page

from ui_suite.pages.base_page import BasePage


class RegisterPage(BasePage):
    """
    Encapsulates user registration workflows and
    account creation interactions.
    """

    def __init__(
        self,
        page: Page
    ) -> None:

        super().__init__(page)

        self.email_input = page.get_by_role(
            "textbox",
            name="Email address field"
        )

        self.password_input = page.get_by_role(
            "textbox",
            name="Field for the password"
        )

        self.repeat_password_input = page.get_by_role(
            "textbox",
            name="Field to confirm the password"
        )

        self.security_question_dropdown = page.get_by_role(
            "combobox",
            name="Selection list for the"
        )

        self.security_answer_input = page.get_by_role(
            "textbox",
            name="Field for the answer to the"
        )

        self.register_button = page.get_by_role(
            "button",
            name="Button to complete the"
        )

    def navigate(
        self
    ) -> None:
        """
        Navigates directly to the registration page.
        """

        super().navigate("register")

    def register_new_user(
        self,
        email: str,
        password: str,
        security_answer: str
    ) -> None:
        """
        Completes the registration workflow.

        The Tab action is intentionally preserved because
        Angular validation occasionally requires focus loss
        before enabling dependent form controls.
        """

        self.email_input.fill(email)

        self.email_input.press("Tab")

        self.password_input.fill(password)

        self.repeat_password_input.fill(password)

        self.security_question_dropdown.click()

        self.page.get_by_role(
            "option"
        ).first.click()

        self.security_answer_input.fill(
            security_answer
        )

        self.register_button.click()