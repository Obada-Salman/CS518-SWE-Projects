import sqlite3
import threading
# from pathlib import Path #-> incomtabale with pyisntaller
from typing import Any, Optional
import resource_path


# DEFAULT_DB_PATH = Path(__file__).resolve().parent.parent / "data" / "leaderboard.db"
DEFAULT_DB_PATH = resource_path.get_leaderboard_database()


class LeaderboardRepository:
    def __init__(self, db_path: Optional[str] = None) -> None:
        self.db_path = db_path if db_path else DEFAULT_DB_PATH
        # self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS leaderboard_entries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    score INTEGER NOT NULL CHECK (score >= 0),
                    completion_time_ms INTEGER NOT NULL CHECK (completion_time_ms >= 0),
                    level_name TEXT,
                    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
                );

                CREATE INDEX IF NOT EXISTS idx_leaderboard_ranking
                ON leaderboard_entries (score DESC, completion_time_ms ASC, created_at ASC);
                """
            )

    def add_entry(
        self,
        username: str,
        score: int,
        completion_time_ms: int,
        level_name: Optional[str] = None,
    ) -> dict[str, Any]:
        username = username.strip()
        normalized_level = level_name.strip() if isinstance(level_name, str) and level_name.strip() else None

        with self._lock:
            with self._connect() as connection:
                cursor = connection.execute(
                    """
                    INSERT INTO leaderboard_entries (username, score, completion_time_ms, level_name)
                    VALUES (?, ?, ?, ?)
                    """,
                    (username, score, completion_time_ms, normalized_level),
                )
                inserted_id = cursor.lastrowid
                row = connection.execute(
                    """
                    SELECT id, username, score, completion_time_ms, level_name, created_at
                    FROM leaderboard_entries
                    WHERE id = ?
                    """,
                    (inserted_id,),
                ).fetchone()

        return self._row_to_dict(row)

    def list_entries(self, limit: int = 25, level_name: Optional[str] = None) -> list[dict[str, Any]]:
        safe_limit = min(max(limit, 1), 200)

        query = (
            """
            SELECT id, username, score, completion_time_ms, level_name, created_at
            FROM leaderboard_entries
            """
        )
        params: list[Any] = []

        if level_name and level_name.strip():
            query += "WHERE level_name = ? "
            params.append(level_name.strip())

        query += "ORDER BY score DESC, completion_time_ms ASC, created_at ASC LIMIT ?"
        params.append(safe_limit)

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()

        return [self._row_to_dict(row) for row in rows]

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": row["id"],
            "username": row["username"],
            "score": row["score"],
            "completion_time_ms": row["completion_time_ms"],
            "level_name": row["level_name"],
            "created_at": row["created_at"],
        }
