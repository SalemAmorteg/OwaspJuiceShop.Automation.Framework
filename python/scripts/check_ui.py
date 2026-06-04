import sys
import os
from playwright.sync_api import sync_playwright

def check_login_page():
    """
    Performs an immediate, lightweight sanity check on critical login views 
    to troubleshoot localized container availability or rendering anomalies.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:3000/#/login")
        
        # Enforces a brief state settle to let heavy SPA asynchronous assets load completely
        page.wait_for_timeout(2000)
        
        email = page.get_by_role("textbox", name="Text field for the login email")
        print(f"Email visible: {email.is_visible()}")
        
        password = page.get_by_role("textbox", name="Text field for the login password")
        print(f"Password visible: {password.is_visible()}")
        
        login_btn = page.get_by_role("button", name="Login", exact=True)
        print(f"Login button visible: {login_btn.is_visible()}")
        
        # Dumps DOM context snapshot on failure to accelerate selector debugging
        if not email.is_visible():
            print("Page Content Snippet:")
            print(page.content()[:2000])
            
        browser.close()

if __name__ == "__main__":
    check_login_page()