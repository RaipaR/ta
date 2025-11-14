"""Data access layer for the tour agency application."""
from __future__ import annotations

from datetime import date
from typing import Iterable, List, Optional

from .database import DEFAULT_DB_PATH, get_connection
from .models import Booking, Tourist


def _parse_date(value: Optional[str]) -> Optional[date]:
    if value is None:
        return None
    return date.fromisoformat(value)


def _row_to_tourist(row) -> Tourist:
    return Tourist(
        id=row[0],
        first_name=row[1],
        last_name=row[2],
        passport_number=row[3],
        phone=row[4],
        email=row[5],
        date_of_birth=_parse_date(row[6]),
        notes=row[7],
    )


def add_tourist(tourist: Tourist, db_path=DEFAULT_DB_PATH) -> int:
    """Insert a tourist into the database and return the new row id."""
    with get_connection(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO tourist (
                first_name, last_name, passport_number, phone, email, date_of_birth, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tourist.first_name,
                tourist.last_name,
                tourist.passport_number,
                tourist.phone,
                tourist.email,
                tourist.date_of_birth.isoformat() if tourist.date_of_birth else None,
                tourist.notes,
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


def get_tourist_by_passport(passport_number: str, db_path=DEFAULT_DB_PATH) -> Optional[Tourist]:
    with get_connection(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, first_name, last_name, passport_number, phone, email, date_of_birth, notes FROM tourist WHERE passport_number = ?",
            (passport_number,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_tourist(row)


def get_tourist_by_id(tourist_id: int, db_path=DEFAULT_DB_PATH) -> Optional[Tourist]:
    with get_connection(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, first_name, last_name, passport_number, phone, email, date_of_birth, notes FROM tourist WHERE id = ?",
            (tourist_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return _row_to_tourist(row)


def list_tourists(db_path=DEFAULT_DB_PATH) -> List[Tourist]:
    with get_connection(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, first_name, last_name, passport_number, phone, email, date_of_birth, notes FROM tourist ORDER BY last_name"
        )
        rows = cursor.fetchall()
        return [_row_to_tourist(row) for row in rows]


def add_booking(booking: Booking, db_path=DEFAULT_DB_PATH) -> int:
    with get_connection(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO booking (
                tourist_id, destination, start_date, end_date, price, description
            ) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                booking.tourist_id,
                booking.destination,
                booking.start_date.isoformat(),
                booking.end_date.isoformat(),
                booking.price,
                booking.description,
            ),
        )
        connection.commit()
        return int(cursor.lastrowid)


def get_booking_by_id(booking_id: int, db_path=DEFAULT_DB_PATH) -> Optional[Booking]:
    with get_connection(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, tourist_id, destination, start_date, end_date, price, description FROM booking WHERE id = ?",
            (booking_id,),
        )
        row = cursor.fetchone()
        if row is None:
            return None
        return Booking(
            id=row[0],
            tourist_id=row[1],
            destination=row[2],
            start_date=date.fromisoformat(row[3]),
            end_date=date.fromisoformat(row[4]),
            price=float(row[5]),
            description=row[6],
        )


def get_bookings_for_tourist(tourist_id: int, db_path=DEFAULT_DB_PATH) -> Iterable[Booking]:
    with get_connection(db_path) as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, tourist_id, destination, start_date, end_date, price, description FROM booking WHERE tourist_id = ? ORDER BY start_date",
            (tourist_id,),
        )
        rows = cursor.fetchall()
        for row in rows:
            yield Booking(
                id=row[0],
                tourist_id=row[1],
                destination=row[2],
                start_date=date.fromisoformat(row[3]),
                end_date=date.fromisoformat(row[4]),
                price=float(row[5]),
                description=row[6],
            )
