import sys
import os

# Resolves workspace environment paths to enable local cross-module diagnostic execution
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.db_handler import DBHandler

try:
    db = DBHandler()
    users = db.get_all_users()
    
    # Truncates execution logging output to prevent console flooding during heavy volume runs
    print("User Credentials (Email: Password):")
    for i, user in enumerate(users):
        if i >= 5:  
            break
        print(f"{user['email']}: {user['password']}")

except Exception as e:
    print(f"Error: {e}")