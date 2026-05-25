import re
from playwright.sync_api import Page, expect

class BasePage:
    """
    Staff-Level BasePage: Provides a shared interface for all pages.
    Centralizes UI blocker management to prevent race conditions[cite: 2].
    """
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = ""):
        """
        Unified navigation method inherited by all Page Objects[cite: 2].
        Ensures Juice Shop hash-routing and overlay dismissal are handled.
        """
        # Ensure the path starts with /#/ for Juice Shop's SPA architecture
        clean_path = path.lstrip("/")
        target_path = f"/#/{clean_path}"
        
        # Playwright prepends the base_url from pytest.ini automatically[cite: 2]
        self.page.goto(target_path)
        self.dismiss_initial_overlays()
    
    def dismiss_initial_overlays(self):
        """
        Resiliently handles global UI blockers per Engineering Standards.
        """
        welcome_btn = self.page.get_by_role("button", name="Close Welcome Banner")
        cookie_btn = self.page.get_by_label("dismiss cookie message")
        
        # Non-blocking checks with short timeouts to maintain velocity
        try:
            if welcome_btn.is_visible(timeout=2500):
                welcome_btn.click()
                
            if cookie_btn.is_visible(timeout=1000):
                cookie_btn.click()
        except Exception:
            # Prevent fragile hangs if overlays were cleared by other means[cite: 2]
            pass