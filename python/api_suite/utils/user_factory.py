import random
import string


def generate_user():

    suffix = "".join(random.choices(string.ascii_lowercase, k=6))

    return type("User", (), {
        "email": f"test_{suffix}@mail.com",
        "password": "Password123!"
    })()