"""SQLite database utilities for the tour agency application."""
from __future__ import annotations

import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

DEFAULT_DB_PATH = Path("tour_agency.db")


def initialise_database(db_path: Path = DEFAULT_DB_PATH) -> None:
    """Create required tables if they do not exist.

    Parameters
    ----------
    db_path:
        Path to the SQLite database file.
    """
    with sqlite3.connect(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tourist (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                passport_number TEXT UNIQUE NOT NULL,
                phone TEXT,
                email TEXT,
                date_of_birth TEXT,
                notes TEXT
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tourist_id INTEGER NOT NULL,
                destination TEXT NOT NULL,
                start_date TEXT NOT NULL,
                end_date TEXT NOT NULL,
                price REAL NOT NULL,
                description TEXT,
                FOREIGN KEY (tourist_id) REFERENCES tourist(id) ON DELETE CASCADE
            )
            """
        )
        connection.commit()


@contextmanager
def get_connection(db_path: Path = DEFAULT_DB_PATH) -> Iterator[sqlite3.Connection]:
    """Context manager yielding a SQLite connection."""
    connection = sqlite3.connect(db_path)
    try:
        yield connection
    finally:
        connection.close()
