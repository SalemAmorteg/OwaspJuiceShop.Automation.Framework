import sys
import os
import re
from playwright.sync_api import sync_playwright, expect
# Add the parent directory (python/) to sys.path so we can import from utils, pages, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.login_page import LoginPage
from pages.register_page import RegisterPage

def test_flow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(base_url="http://localhost:3000")
        
        reg_page = RegisterPage(page)
        reg_page.navigate()
        print("Registering user...")
        reg_page.register_new_user("miguel1234@gmail.com", "12345", "Mariana")
        
        login_page = LoginPage(page)
        login_page.navigate()
        print("Logging in...")
        login_page.login("miguel1234@gmail.com", "12345")
        
        try:
            # Use Playwright's built-in expect for URL verification
            expect(page).to_have_url(re.compile(r".*/search"))
            print("Login Successful!")
        except Exception as e:
            print(f"Login Failed: {e}")
            print(f"URL: {page.url}")
            
        browser.close()

if __name__ == "__main__":
    test_flow()
