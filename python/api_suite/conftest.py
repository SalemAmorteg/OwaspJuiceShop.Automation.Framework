import pytest
import random
from typing import Dict, Any, Callable
from python.api_suite.clients.api_client import APIClient

@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """
    Initializes and provides a session-scoped API client instance 
    bound to the target container endpoint.
    """
    return APIClient("http://localhost:3000")

@pytest.fixture(scope="function")
def user_factory() -> Callable[..., Dict[str, Any]]:
    """
    A factory utility generating unique user registration payloads dynamically
    to prevent test data collision between concurrent executions.
    """
    def _create_payload(email: str = None, password: str = "Pass123!") -> Dict[str, Any]:
        if email is None:
            unique_id = random.randint(10000, 99999)
            email = f"natalia_sdet_{unique_id}@test.com"
        return {
            "email": email,
            "password": password
        }
    return _create_payload