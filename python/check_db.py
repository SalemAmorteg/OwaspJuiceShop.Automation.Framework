import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'python'))
from utils.db_handler import DBHandler

try:
    db = DBHandler()
    print(f"DB Path: {db.db_path}")
    print(f"DB Exists: {db.db_path.exists()}")
    user = db.get_user_by_email("miguel1234@gmail.com")
    print(f"User Miguel: {user}")
except Exception as e:
    print(f"Error: {e}")
