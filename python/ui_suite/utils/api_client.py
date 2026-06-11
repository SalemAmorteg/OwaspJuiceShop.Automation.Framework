import requests

from typing import Any, Dict, Optional

from shared_utils.settings import (
    JUICE_SHOP_URL,
    REQUEST_TIMEOUT
)


class APIClient:
    """
    Centralized API layer used for
    test data setup and backend verification.
    """

    def __init__(
        self,
        base_url: str = JUICE_SHOP_URL
    ) -> None:

        self.base_url = base_url.rstrip("/")

        self.session = requests.Session()

    def close(self) -> None:
        self.session.close()

    def register_user(
        self,
        email: str,
        password: str
    ) -> requests.Response:

        payload = {
            "email": email,
            "password": password
        }

        return self.session.post(
            f"{self.base_url}/api/Users/register",
            json=payload,
            timeout=REQUEST_TIMEOUT
        )

    def get_user(
        self,
        user_id: str
    ) -> Optional[Dict[str, Any]]:

        response = self.session.get(
            f"{self.base_url}/api/Users/{user_id}",
            timeout=REQUEST_TIMEOUT
        )

        if response.status_code != 200:
            return None

        return response.json().get("data")