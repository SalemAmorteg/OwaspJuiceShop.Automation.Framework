import sys
import os
# Add the parent directory (python/) to sys.path so we can import from utils, pages, etc.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_handler import DBHandler

try:
    db = DBHandler()
    users = db._execute_query("SELECT email FROM Users LIMIT 5")
    print(f"Users in DB: {[u['email'] for u in users]}")
except Exception as e:
    print(f"Error: {e}")
