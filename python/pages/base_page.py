import re
from playwright.sync_api import Page

class BasePage:
    """
    Orchestrates shared UI states and high-frequency lifecycle interactions 
    such as banner dismissal, layout overlays, and global routing hooks.
    """
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, path: str = "") -> None:
        """
        Handles SPA routing normalization by formatting paths to support 
        the application's hash-routing strategy (#/) before triggering navigation.
        """
        clean_path = path.lstrip("/")
        target_path = f"/#/{clean_path}"
        
        self.page.goto(target_path)
        self.dismiss_initial_overlays()
    
    def dismiss_initial_overlays(self) -> None:
        """
        Aggressively intercepts and dismisses persistent global welcome modals 
        and cookies overlays using short-circuit waiting gates to protect parallel runs.
        """
        welcome_dialog = self.page.locator("mat-dialog-container")
        welcome_close_btn = self.page.get_by_role("button", name="Close Welcome Banner")
        cookie_dismiss_btn = self.page.get_by_label("dismiss cookie message")
        
        try:
            # Short timeout to detect if the banner is loading or visible
            if welcome_dialog.is_visible(timeout=1500):
                welcome_close_btn.wait_for(state="visible", timeout=1500)
                welcome_close_btn.click()
                welcome_dialog.wait_for(state="hidden", timeout=2000)
                
            if cookie_dismiss_btn.is_visible(timeout=500):
                cookie_dismiss_btn.click()
                cookie_dismiss_btn.wait_for(state="hidden", timeout=1500)
        except Exception:
            pass