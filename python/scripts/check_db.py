import sys
import os
# Add the parent directory (python/) to sys.path so we can import from utils, pages, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_handler import DBHandler

try:
    db = DBHandler()
    print(f"DB Path: {db.db_path}")
    print(f"DB Exists: {db.db_path.exists()}")
    user = db.get_user_by_email("miguel1234@gmail.com")
    print(f"User Miguel: {user}")
except Exception as e:
    print(f"Error: {e}")
