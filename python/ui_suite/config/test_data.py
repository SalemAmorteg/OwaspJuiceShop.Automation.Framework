import time
from dataclasses import dataclass

@dataclass(frozen=True)
class UserCredentials:
    email: str
    password: str

def generate_unique_email(prefix: str = "test_user") -> str:
    """
    Generates a unique email address using a timestamp to ensure idempotency.
    Example: test_user_1723456789@juice-sh.op
    """
    timestamp = int(time.time())
    return f"{prefix}_{timestamp}@juice-sh.op"
