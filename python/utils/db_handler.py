import sqlite3
import pathlib
import os
from typing import Optional, Dict, Any

class DBHandler:
    """
    Manages low-level SQLite transactional querying and schema state tracking.
    Uses contextual relative path resolution to query the application storage 
    layer across varying local and container execution environments.
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Resolves the target database file path location. Implements a fallback path traversal 
        sequence to bridge the boundary between the test runner and the application folder trees.
        """
        if db_path:
            self.db_path = pathlib.Path(db_path)
        else:
            # Traverses up from this utility file location to establish the repository base boundary
            workspace_root = pathlib.Path(__file__).resolve().parent.parent.parent.parent

            # Maps the workspace base path downward into the functional runtime database artifact
            self.db_path = workspace_root / "juice-shop" / "data" / "juiceshop.sqlite"

        # Defensive infrastructure check: Aborts execution immediately if the persistent store is unreachable
        if not self.db_path.exists():
            raise FileNotFoundError(
                f"SQLite database NOT found at: {self.db_path}\n"
                "Verify that the 'juice-shop' sibling directory is present and initialized."
            )

    def _execute_query(self, query: str, params: tuple = ()) -> list:
        """
        An internal data gateway that manages connections, handles statement execution, 
        and maps engine row dictionaries. Employs read-only connection parameters 
        to maximize data safety during parallel worker execution.
        """
        try:
            # Employs specific mode flags within the connection string to minimize process locks during parallel test execution
            db_uri = f"file:{self.db_path}?mode=ro"
            with sqlite3.connect(db_uri, uri=True) as conn:
                conn.row_factory = sqlite3.Row 
                cursor = conn.execute(query, params)
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            # Captures exact engine telemetry along with path targets to accelerate debugging pipelines
            print(f"Database Error: {e} | Path: {self.db_path}")
            raise e

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Queries identity tables for a matching user record string. Used primarily 
        to validate backend persistence states after frontend registration submissions.
        """
        query = "SELECT * FROM Users WHERE email = ?"
        results = self._execute_query(query, (email,))
        return results[0] if results else None

    def get_all_users(self) -> list[Dict[str, Any]]:
        """
        Exposes bulk profile record sets to support structural validation checks or systemic system state logging.
        """
        query = "SELECT * FROM Users"
        return self._execute_query(query)

    def get_basket_contents(self, user_email: str) -> list[Dict[str, Any]]:
        """
        Executes a multi-table join operation across identity, session basket, and product matrices.
        Acts as the backend verification layer to confirm database state integrity matches active UI/API basket mutations.
        """
        query = """
            SELECT 
                bi.basketId, 
                bi.productId, 
                bi.quantity, 
                p.name as product_name, 
                p.description as product_description
            FROM BasketItems bi
            JOIN Baskets b ON bi.basketId = b.id
            JOIN Users u ON b.userId = u.id
            JOIN Products p ON bi.productId = p.id
            WHERE u.email = ?
        """
        return self._execute_query(query, (user_email,))