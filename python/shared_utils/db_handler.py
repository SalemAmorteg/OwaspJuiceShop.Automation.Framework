import sqlite3

from typing import Any, Dict, List, Optional

from shared_utils.settings import (
    DATABASE_PATH,
    DATABASE_TIMEOUT
)


class DBHandler:
    """
    Lightweight SQLite access layer used exclusively for
    persistence validation within automated tests.

    Database interactions should verify application state,
    not create or manipulate test data.
    """

    def fetch_all(
        self,
        query: str,
        params: tuple = ()
    ) -> List[Dict[str, Any]]:

        db_uri = f"file:{DATABASE_PATH}?mode=ro"

        with sqlite3.connect(
            db_uri,
            uri=True
        ) as connection:

            connection.row_factory = sqlite3.Row

            return [
                dict(row)
                for row in connection.execute(
                    query,
                    params
                ).fetchall()
            ]

    def fetch_one(
        self,
        query: str,
        params: tuple = ()
    ) -> Optional[Dict[str, Any]]:

        results = self.fetch_all(
            query,
            params
        )

        return results[0] if results else None

    def execute_write(
        self,
        query: str,
        params: tuple = ()
    ) -> None:

        with sqlite3.connect(
            DATABASE_PATH,
            timeout=DATABASE_TIMEOUT
        ) as connection:

            connection.execute(
                query,
                params
            )

            connection.commit()

    def get_user_by_email(
        self,
        email: str
    ) -> Optional[Dict[str, Any]]:

        return self.fetch_one(
            "SELECT * FROM Users WHERE email = ?",
            (email,)
        )