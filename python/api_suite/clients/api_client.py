import requests


class APIClient:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, endpoint, headers=None):
        return requests.get(
            f"{self.base_url}{endpoint}",
            headers=headers
        )

    def post(self, endpoint, payload=None, headers=None):
        return requests.post(
            f"{self.base_url}{endpoint}",
            json=payload,
            headers=headers
        )

    def login(self, email, password):
        return self.post(
            "/rest/user/login",
            {
                "email": email,
                "password": password
            }
        )

    def register_user(self, email, password):
        return self.post(
            "/api/Users",
            {
                "email": email,
                "password": password,
                "passwordRepeat": password
            }
        )