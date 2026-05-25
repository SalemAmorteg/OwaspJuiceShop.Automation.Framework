import requests
from typing import Dict, Any, Optional
from config.test_data import UserCredentials

class APIClient:
    """
    Handles API interactions for Juice Shop to facilitate rapid state seeding.
    Designed for high-velocity automation.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def register_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Registers a new user via the API.
        """
        url = f"{self.base_url}/api/Users/register"
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()

    def delete_user(self, email: str) -> None:
        """
        Deletes a user via the API.
        """
        url = f"{self.base_url}/api/Users/{email}"
        response = requests.delete(url)
        if response.status_code not in [200, 204, 404]:
            print(f"Warning: Failed to delete user {email}: {response.status_code}")

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a user by email via API.
        """
        url = f"{self.base_url}/api/Users/{email}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return None
