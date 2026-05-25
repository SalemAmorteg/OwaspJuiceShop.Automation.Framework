import sqlite3
import pathlib
import os
from typing import Optional, Dict, Any

class DBHandler:
    """
    Handles all SQLite database interactions for the Juice Shop.
    Designed with sibling-directory resolution to support realistic workspace layouts[cite: 2, 3].
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Refined path resolution to handle multi-environment execution.
        Standardizes on the sibling directory structure found in the workspace[cite: 3, 4].
        """
        if db_path:
            self.db_path = pathlib.Path(db_path)
        else:
            # 1. Resolve absolute path of THIS file: root/python/utils/db_handler.py
            # 2. Move up 4 levels to reach the workspace root (qa-workspace/)
            workspace_root = pathlib.Path(__file__).resolve().parent.parent.parent.parent
            
            # 3. Target the sibling directory where the application and DB actually live[cite: 3]
            self.db_path = workspace_root / "juice-shop" / "data" / "juiceshop.sqlite"

        # Staff Practice: Fail-fast if the infrastructure is missing
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"SQLite database NOT found at: {self.db_path}\n"
                "Verify that the 'juice-shop' sibling directory is present and initialized[cite: 3]."
            )

    def _execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Private helper to manage the connection lifecycle.
        Uses URI mode for read-only access to prevent database locking in parallel runs[cite: 2].
        """
        try:
            # URI mode with mode=ro ensures we don't accidentally corrupt app data[cite: 2, 3]
            db_uri = f"file:{self.db_path}?mode=ro"
            with sqlite3.connect(db_uri, uri=True) as conn:
                conn.row_factory = sqlite3.Row 
                cursor = conn.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            # Senior logging includes the path and error context for faster debugging[cite: 2]
            print(f"Database Error: {e} | Path: {self.db_path}")
            raise e

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a user record to verify successful registration in integration tests[cite: 1, 2].
        """
        query = "SELECT * FROM Users WHERE email = ?"
        results = self._execute_query(query, (email,))
        return results[0] if results else None

    def get_all_users(self) -> list[Dict[str, Any]]:
        """
        Retrieves all user records from the database.
        """
        query = "SELECT * FROM Users"
        return self._execute_query(query)