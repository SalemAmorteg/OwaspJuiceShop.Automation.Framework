import sys
import os

# Resolves workspace environment paths to enable local cross-module diagnostic execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_handler import DBHandler

try:
    db = DBHandler()
    print(f"DB Path: {db.db_path}")
    print(f"DB Exists: {db.db_path.exists()}")
    
    # Smoke check: Verify basic query capability against the user schema
    user = db.get_user_by_email("miguel1234@gmail.com")
    print(f"User Miguel: {user}")
except Exception as e:
    print(f"Error: {e}")