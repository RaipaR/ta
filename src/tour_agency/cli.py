"""Command line interface for the tour agency application."""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from typing import Optional

from . import database, repository
from .document_service import render_booking_contract
from .models import Booking, Tourist


def _parse_date(value: str) -> date:
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "Date must be in ISO format (YYYY-MM-DD)"
        ) from exc


def init_database(args: argparse.Namespace) -> None:
    database.initialise_database(Path(args.database))
    print(f"Database initialised at {Path(args.database).resolve()}")


def add_tourist(args: argparse.Namespace) -> None:
    tourist = Tourist(
        id=None,
        first_name=args.first_name,
        last_name=args.last_name,
        passport_number=args.passport,
        phone=args.phone,
        email=args.email,
        date_of_birth=_parse_date(args.date_of_birth) if args.date_of_birth else None,
        notes=args.notes,
    )
    tourist_id = repository.add_tourist(tourist, db_path=Path(args.database))
    print(f"Tourist created with id {tourist_id}")


def list_tourists(args: argparse.Namespace) -> None:
    tourists = repository.list_tourists(db_path=Path(args.database))
    if not tourists:
        print("No tourists found.")
        return

    for tourist in tourists:
        dob = tourist.date_of_birth.isoformat() if tourist.date_of_birth else "-"
        print(
            f"[{tourist.id}] {tourist.last_name} {tourist.first_name} | "
            f"Passport: {tourist.passport_number} | Phone: {tourist.phone or '-'} | DOB: {dob}"
        )


def add_booking(args: argparse.Namespace) -> None:
    tourist = repository.get_tourist_by_passport(args.passport, db_path=Path(args.database))
    if tourist is None:
        raise SystemExit("Tourist with provided passport not found.")

    booking = Booking(
        id=None,
        tourist_id=tourist.id,
        destination=args.destination,
        start_date=args.start_date,
        end_date=args.end_date,
        price=args.price,
        description=args.description,
    )
    booking_id = repository.add_booking(booking, db_path=Path(args.database))
    print(f"Booking created with id {booking_id} for tourist {tourist.last_name} {tourist.first_name}")


def list_bookings(args: argparse.Namespace) -> None:
    tourist = repository.get_tourist_by_passport(args.passport, db_path=Path(args.database))
    if tourist is None:
        raise SystemExit("Tourist with provided passport not found.")

    bookings = list(repository.get_bookings_for_tourist(tourist.id, db_path=Path(args.database)))
    if not bookings:
        print("No bookings found for tourist.")
        return

    for booking in bookings:
        print(
            f"[{booking.id}] {booking.destination} | {booking.start_date.isoformat()} - {booking.end_date.isoformat()} | "
            f"Price: {booking.price:.2f}"
        )


def generate_contract(args: argparse.Namespace) -> None:
    booking = repository.get_booking_by_id(args.booking_id, db_path=Path(args.database))
    if booking is None:
        raise SystemExit("Booking not found.")

    tourist = repository.get_tourist_by_id(booking.tourist_id, db_path=Path(args.database))
    if tourist is None:
        raise SystemExit("Tourist associated with booking not found.")

    output_path = render_booking_contract(
        tourist,
        booking,
        template_path=Path(args.template),
        output_path=Path(args.output),
    )
    print(f"Document generated at {output_path.resolve()}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tour agency management tool")
    parser.add_argument(
        "--database",
        default=str(database.DEFAULT_DB_PATH),
        help="Path to the SQLite database file",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init-db", help="Initialise the database schema")
    init_parser.set_defaults(func=init_database)

    tourist_parser = subparsers.add_parser("add-tourist", help="Create a new tourist")
    tourist_parser.add_argument("first_name")
    tourist_parser.add_argument("last_name")
    tourist_parser.add_argument("passport", help="Passport number")
    tourist_parser.add_argument("--phone")
    tourist_parser.add_argument("--email")
    tourist_parser.add_argument("--date-of-birth")
    tourist_parser.add_argument("--notes")
    tourist_parser.set_defaults(func=add_tourist)

    list_tourists_parser = subparsers.add_parser("list-tourists", help="List all tourists")
    list_tourists_parser.set_defaults(func=list_tourists)

    booking_parser = subparsers.add_parser("add-booking", help="Create a new booking for a tourist")
    booking_parser.add_argument("passport", help="Passport number of the tourist")
    booking_parser.add_argument("destination")
    booking_parser.add_argument("start_date", type=_parse_date)
    booking_parser.add_argument("end_date", type=_parse_date)
    booking_parser.add_argument("price", type=float)
    booking_parser.add_argument("--description")
    booking_parser.set_defaults(func=add_booking)

    list_bookings_parser = subparsers.add_parser("list-bookings", help="List bookings for a tourist")
    list_bookings_parser.add_argument("passport", help="Passport number of the tourist")
    list_bookings_parser.set_defaults(func=list_bookings)

    contract_parser = subparsers.add_parser("generate-contract", help="Generate a Word contract from a template")
    contract_parser.add_argument("booking_id", type=int)
    contract_parser.add_argument("template", help="Path to the .docx template")
    contract_parser.add_argument("output", help="Where to save the generated document")
    contract_parser.set_defaults(func=generate_contract)

    return parser


def main(argv: Optional[list[str]] = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
