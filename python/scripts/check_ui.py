import sys
import os
from playwright.sync_api import sync_playwright

def check_login_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:3000/#/login")
        
        # Give it a second to load
        page.wait_for_timeout(2000)
        
        # Check for email field
        email = page.get_by_role("textbox", name="Text field for the login email")
        print(f"Email visible: {email.is_visible()}")
        
        # Check for password field
        password = page.get_by_role("textbox", name="Text field for the login password")
        print(f"Password visible: {password.is_visible()}")
        
        # Check for login button
        login_btn = page.get_by_role("button", name="Login", exact=True)
        print(f"Login button visible: {login_btn.is_visible()}")
        
        if not email.is_visible():
            print("Page Content Snippet:")
            print(page.content()[:2000])
            
        browser.close()

if __name__ == "__main__":
    check_login_page()
