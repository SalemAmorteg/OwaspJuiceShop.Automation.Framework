import requests
from typing import Dict, Any, Optional

class APIClient:
    """
    Core HTTP engine handling communication tracks with the Juice Shop API surface.
    Designed to expose raw response structures for granular validation within assertions.
    """
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        # Initialize standard content transmission headers for API tracks
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def register_user(self, payload: Dict[str, Any]) -> requests.Response:
        """
        Transmits a request payload to create a new user record via POST /api/Users.
        """
        url = f"{self.base_url}/api/Users"
        return self.session.post(url, json=payload)

    def login_user(self, payload: Dict[str, Any]) -> requests.Response:
        """
        Transmits user login parameters to request validation via POST /rest/user/login.
        """
        url = f"{self.base_url}/rest/user/login"
        return self.session.post(url, json=payload)

    def set_auth_token(self, token: str) -> None:
        """
        Appends the Bearer token to session headers for authenticated tracks.
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})