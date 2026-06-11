import pytest
from shared_utils.db_handler import DBHandler

@pytest.fixture(scope="module")
def db_handler():
    """Provides module-scoped access to backend storage layers for data tracking."""
    return DBHandler()

def test_get_all_users(db_handler):
    """
    Verifies the operational status of the low-level database handler queries.
    Validates that record extraction yields active entries and captures system state logs.
    """
    users = db_handler.get_all_users()
    assert users is not None, "Expected users to be retrieved, but got None"
    assert len(users) > 0, "Expected at least one user in the database"
    print(f"""
Retrieved {len(users)} users:""")
    for user in users:
        print(user)