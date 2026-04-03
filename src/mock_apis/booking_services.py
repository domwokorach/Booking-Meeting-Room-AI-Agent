# src/mock_apis/booking_services.py
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Union, Dict

from langchain_core.tools import tool

from config import BOOKINGS_FILE, DELAY


# @tool("load_bookings", description="Load existing bookings from external file.")
def load_bookings(
        filepath: Path = BOOKINGS_FILE
    ) -> Dict[str, List[Dict[str, Union[str, datetime]]]]:
    """Load existing bookings from external file."""
    existing_data: Dict[str, List[Dict[str, Union[str, datetime]]]] = {}
    try:
        with open(filepath, "r") as f:
            existing_data = json.load(f)
    except json.JSONDecodeError:
        print(f"Warning: Could not decode existing JSON in {filepath}. Starting fresh.")
        existing_data = {}
    return existing_data


# @tool("save_bookings", description="Save bookings to the database.")
def save_bookings_tool(
        room_id: Union[int, str],
        booking: Dict, filepath: Path = BOOKINGS_FILE
    ):
    """Save bookings to the database."""
    bookings = load_bookings(filepath=filepath)
    room_id = str(room_id)
    room_bookings = bookings.get(room_id, [])
    print(f"Current bookings for room {room_id}: {room_bookings}")
    room_bookings.append(booking)
    bookings[room_id] = room_bookings

    with open(filepath, "w") as f:
        json.dump(bookings, f, indent=4)

# @tool("check_time_conflict", description="Check if a room has a time conflict for the requested time.")
def check_time_conflict_tool(
        existing_bookings: Dict[str, List[Dict[str, Union[str, datetime]]]],
        room_id: Union[int, str], start_time: Union[str, datetime],
        end_time: Optional[Union[str, datetime]] = None, duration_hours: Optional[float] = None,
    ) -> bool:
    """
    Check if a room has a time conflict for the requested time.
    """
    if isinstance(start_time, str):
        start_time = datetime.fromisoformat(start_time)
    if end_time is not None:
        if isinstance(end_time, str):
            end_time = datetime.fromisoformat(end_time)
    else:
        end_time = start_time + timedelta(hours=duration_hours or 1.0)

    room_bookings = existing_bookings.get(str(room_id), [])
    if not room_bookings:
        return False
    for booking in room_bookings:
        booking_start = datetime.fromisoformat(str(booking['start_time']))
        booking_end = datetime.fromisoformat(str(booking['end_time'])) + DELAY
        if start_time < booking_end and end_time > booking_start:
            return True
    return False

def get_room_reserved_time_slots(
        room_id: Union[int, str],
        existing_bookings: Dict[str, List[Dict[str, Union[str, datetime]]]]) -> List[Dict]:

    free_time_slots = []
    room_id = str(room_id)

    return free_time_slots


@tool("book_room", description="Book a room for the specified time and user.")
def book_room_tool(
        room_id: int, start_time: str,
        end_time: str, user_name: str
    ) -> Optional[Dict]:
    """Book a room for the specified time and user."""
    existing_bookings = load_bookings()
    duration = (datetime.fromisoformat(end_time) - datetime.fromisoformat(start_time)).total_seconds() / 3600
    if check_time_conflict_tool(
        existing_bookings,
        room_id, start_time,
        duration_hours=duration
    ):
        return None
    booking = {
        "room_id": room_id,
        "start_time": start_time,
        "end_time": end_time,
        "booked_by": user_name,
    }
    save_bookings_tool(room_id, booking)
    return booking
