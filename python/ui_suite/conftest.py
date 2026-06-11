import re

from pathlib import Path

import pytest
import requests

from playwright.sync_api import (
    Page,
    expect
)

from ui_suite.config.test_data import (
    UserCredentials,
    generate_unique_email
)

from ui_suite.pages.login_page import LoginPage
from ui_suite.pages.register_page import RegisterPage
from ui_suite.pages.search_page import SearchPage
from ui_suite.pages.cart_page import CartPage
from ui_suite.pages.product_details_page import ProductDetailsPage

from shared_utils.settings import JUICE_SHOP_URL


# -----------------------------------------------------------------------------
# Environment Validation
# -----------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def verify_environment() -> None:
    """
    Validates Juice Shop availability before test execution begins.

    Prevents false negatives caused by infrastructure or
    application startup failures.
    """

    try:

        response = requests.get(
            JUICE_SHOP_URL,
            timeout=5
        )

        if response.status_code != 200:

            pytest.exit(
                f"Juice Shop returned unexpected status code: "
                f"{response.status_code}"
            )

    except requests.exceptions.RequestException as exc:

        pytest.exit(
            f"Unable to reach Juice Shop environment: {exc}"
        )


# -----------------------------------------------------------------------------
# Test User Provisioning
# -----------------------------------------------------------------------------

@pytest.fixture(scope="function")
def ui_seeded_user(
    page: Page,
    register_page_instance: RegisterPage
) -> UserCredentials:
    """
    Creates a fresh user through the UI registration flow.

    This fixture intentionally avoids API-based user creation
    to keep Sprint 1 focused on validating the actual
    business workflow exposed to end users.

    Returns:
        UserCredentials: Newly registered user credentials.
    """

    credentials = UserCredentials(
        email=generate_unique_email(
            prefix="ui_test"
        ),
        password="Password123!"
    )

    register_page_instance.navigate()

    register_page_instance.register_new_user(
        credentials.email,
        credentials.password,
        "Answer123"
    )

    expect(page).to_have_url(
        re.compile(r".*/login")
    )

    return credentials


# -----------------------------------------------------------------------------
# Standard Page Object Fixtures
# -----------------------------------------------------------------------------

@pytest.fixture(scope="function")
def register_page_instance(
    page: Page
) -> RegisterPage:
    """
    Provides a fresh RegisterPage instance.
    """

    return RegisterPage(page)


@pytest.fixture(scope="function")
def login_page_instance(
    page: Page
) -> LoginPage:
    """
    Provides a fresh LoginPage instance.
    """

    return LoginPage(page)


@pytest.fixture(scope="function")
def search_page_instance(
    page: Page
) -> SearchPage:
    """
    Provides a fresh SearchPage instance.
    """

    return SearchPage(page)


@pytest.fixture(scope="function")
def cart_page_instance(
    page: Page
) -> CartPage:
    """
    Provides a fresh CartPage instance.
    """

    return CartPage(page)


@pytest.fixture(scope="function")
def product_details_page_instance(
    page: Page
) -> ProductDetailsPage:
    """
    Provides a fresh ProductDetailsPage instance.
    """

    return ProductDetailsPage(page)


# -----------------------------------------------------------------------------
# Screenshot on Failure
# -----------------------------------------------------------------------------

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Captures a screenshot whenever a test fails.

    Screenshots are stored under:

        artifacts/screenshots/

    This provides visual evidence for debugging
    and simplifies failure investigation.
    """

    outcome = yield

    report = outcome.get_result()

    if report.when != "call":
        return

    if report.passed:
        return

    page = item.funcargs.get("page")

    if page is None:
        return

    screenshots_dir = Path(
        "artifacts/screenshots"
    )

    screenshots_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    screenshot_name = (
        f"{item.name}.png"
    )

    screenshot_path = (
        screenshots_dir / screenshot_name
    )

    page.screenshot(
        path=str(screenshot_path),
        full_page=True
    )

    print(
        f"\nScreenshot saved: "
        f"{screenshot_path}"
    )