import pytest
from utils.db_handler import DBHandler

@pytest.fixture(scope="module")
def db_handler():
    """Provides a DBHandler instance for tests."""
    return DBHandler()

def test_get_all_users(db_handler):
    """
    Tests that get_all_users retrieves a list of users from the database.
    """
    users = db_handler.get_all_users()
    assert users is not None, "Expected users to be retrieved, but got None"
    assert len(users) > 0, "Expected at least one user in the database"
    print(f"""
Retrieved {len(users)} users:""")
    for user in users:
        print(user)