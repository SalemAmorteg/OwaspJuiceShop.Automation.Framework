from dataclasses import dataclass


@dataclass
class User:
    email: str
    password: str


VALID_USER = User(
    email="admin@juice-sh.op",
    password="admin123"
)