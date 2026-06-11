"""
User Authentication Boundary and UI Validation Suite.

Validates authentication behavior through the UI layer,
including successful login workflows and rejection paths
for invalid credentials.
"""

import re

from playwright.sync_api import (
    Page,
    expect
)

from ui_suite.config.test_data import (
    UserCredentials
)

from ui_suite.pages.login_page import LoginPage


def test_successful_login_with_ui_seeded_user(
    ui_seeded_user: UserCredentials,
    login_page_instance: LoginPage,
    page: Page
) -> None:
    """
    Happy Path Authentication Validation.

    Creates a fresh user through the registration workflow
    and validates that the account can successfully
    authenticate immediately afterward.

    Verification Points:
    - Login request succeeds
    - User is redirected to the search page
    - Authenticated UI elements become visible
    """

    email = ui_seeded_user.email
    password = ui_seeded_user.password

    login_page_instance.navigate()

    login_page_instance.login(
        email,
        password
    )

    # Verify successful route transition
    expect(page).to_have_url(
        re.compile(r".*/search")
    )

    # Verify authenticated application state
    expect(
        page.get_by_role(
            "button",
            name="Show the shopping cart"
        )
    ).to_be_visible()


def test_unsuccessful_login_with_invalid_credentials(
    login_page_instance: LoginPage
) -> None:
    """
    Negative Path Authentication Validation.

    Confirms that invalid credentials are rejected and
    appropriate error feedback is displayed to the user.

    Verification Points:
    - Authentication fails
    - Error message becomes visible
    """

    invalid_email = (
        "nonexistent_user_999@juice-sh.op"
    )

    invalid_password = (
        "wrong_password"
    )

    login_page_instance.navigate()

    login_page_instance.login(
        invalid_email,
        invalid_password
    )

    expect(
        login_page_instance.get_error_message_locator()
    ).to_be_visible()