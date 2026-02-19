import os
import sqlite3
from config.settings import DB_PATH


def _get_schema_path() -> str:
    return os.path.join(os.path.dirname(__file__), "schema.sql")


def init_db() -> None:
    os.makedirs(os.path.dirname(os.path.abspath(DB_PATH)), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        with open(_get_schema_path(), "r") as f:
            conn.executescript(f.read())
        conn.commit()


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def execute(query: str, params: tuple = ()) -> None:
    with get_connection() as conn:
        conn.execute(query, params)
        conn.commit()


def fetchall(query: str, params: tuple = ()) -> list:
    with get_connection() as conn:
        return conn.execute(query, params).fetchall()


def fetchone(query: str, params: tuple = ()):
    with get_connection() as conn:
        return conn.execute(query, params).fetchone()
