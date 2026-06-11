"""
Registration flow validation.

Validates successful user onboarding and confirms that newly
created credentials can authenticate immediately afterwards.
"""

import re
import pytest

from playwright.sync_api import (
    Page,
    expect
)

from ui_suite.pages.register_page import RegisterPage
from ui_suite.pages.login_page import LoginPage

from ui_suite.config.test_data import (
    UserCredentials,
    generate_unique_email
)


@pytest.fixture(scope="function")
def registration_user(
    page: Page,
    register_page_instance: RegisterPage
) -> UserCredentials:
    """
    Creates a fresh user through the UI registration flow.

    This fixture intentionally validates only the user-facing
    behavior and avoids direct database dependencies.
    """

    credentials = UserCredentials(
        email=generate_unique_email(
            prefix="reg_test"
        ),
        password="SecurePassword123!"
    )

    register_page_instance.navigate()

    register_page_instance.register_new_user(
        credentials.email,
        credentials.password,
        "12345"
    )

    expect(page).to_have_url(
        re.compile(r".*/login")
    )

    yield credentials


@pytest.mark.functional
def test_new_user_registration_lifecycle(
    registration_user: UserCredentials,
    login_page_instance: LoginPage,
    page: Page
) -> None:
    """
    Confirms that a newly registered user
    can immediately authenticate.
    """

    login_page_instance.navigate()

    login_page_instance.login(
        registration_user.email,
        registration_user.password
    )

    expect(page).to_have_url(
        re.compile(r".*/search")
    )