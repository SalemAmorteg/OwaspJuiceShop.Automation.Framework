from playwright.sync_api import Page


class BasePage:
    """
    Base abstraction shared across all page objects.

    Provides navigation helpers and global UI stabilization
    mechanisms required by Juice Shop.
    """

    def __init__(self, page: Page):
        self.page = page

    def navigate(
        self,
        path: str = ""
    ) -> None:
        """
        Navigates to a Juice Shop route and clears
        blocking onboarding overlays when present.
        """

        clean_path = path.lstrip("/")

        self.page.goto(
            f"/#/{clean_path}"
        )

        self.dismiss_initial_overlays()

    def dismiss_initial_overlays(
        self
    ) -> None:

        welcome_banner = self.page.get_by_role(
            "button",
            name="Close Welcome Banner"
        )

        cookie_banner = self.page.get_by_label(
            "dismiss cookie message"
        )

        try:

            if welcome_banner.is_visible(timeout=2500):
                welcome_banner.click()

            if cookie_banner.is_visible(timeout=1000):
                cookie_banner.click()

        except Exception:
            pass