"""Domain models for the tour agency application."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class Tourist:
    id: Optional[int]
    first_name: str
    last_name: str
    passport_number: str
    phone: Optional[str] = None
    email: Optional[str] = None
    date_of_birth: Optional[date] = None
    notes: Optional[str] = None


@dataclass
class Booking:
    id: Optional[int]
    tourist_id: int
    destination: str
    start_date: date
    end_date: date
    price: float
    description: Optional[str] = None
