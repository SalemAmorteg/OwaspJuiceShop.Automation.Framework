import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'python'))
from utils.db_handler import DBHandler

try:
    db = DBHandler()
    users = db._execute_query("SELECT email FROM Users LIMIT 5")
    print(f"Users in DB: {[u['email'] for u in users]}")
except Exception as e:
    print(f"Error: {e}")
