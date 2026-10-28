
import json
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
from pathlib import Path


CONFIG_FILE = Path(__file__).with_name("classes.json")


def load_config():
    """Read the timetable from the JSON file."""
    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def parse_time(value):
    """Convert a string such as '09:30' into a time object."""
    return time.fromisoformat(value)


def get_sessions(config, today, now):
    """Return today's scheduled sessions."""
    sessions = []

    for course in config["classes"]:
        for session in course["sessions"]:
            if session["day"].lower() != today.strftime("%A").lower():
                continue

            start_time = parse_time(session["start"])
            end_time = parse_time(session["end"])

            if end_time <= start_time:
                raise ValueError(
                    f"Invalid time range for {course['name']}"
                )

            start = datetime.combine(today, start_time, tzinfo=now.tzinfo)
            end = datetime.combine(today, end_time, tzinfo=now.tzinfo)

            sessions.append({
                **session,
                "name": course["name"],
                "start_datetime": start,
                "end_datetime": end,
            })

    return sorted(sessions, key=lambda item: item["start_datetime"])


def find_current_class(config, now=None):
    """Find the class whose scheduled time includes now."""
    timezone = ZoneInfo(config["timezone"])

    if now is None:
        now = datetime.now(timezone)
    else:
        now = now.astimezone(timezone)

    sessions = get_sessions(config, now.date(), now)

    for session in sessions:
        if session["start_datetime"] <= now < session["end_datetime"]:
            return session

    return None


def find_next_class(config, now=None):
    """Find the next session starting after the current time."""
    timezone = ZoneInfo(config["timezone"])

    if now is None:
        now = datetime.now(timezone)
    else:
        now = now.astimezone(timezone)

    upcoming = []

    # Search the next eight calendar days, including today.
    for offset in range(8):
        target_date = now.date() + timedelta(days=offset)

        for course in config["classes"]:
            for session in course["sessions"]:
                if session["day"].lower() != target_date.strftime("%A").lower():
                    continue

                start = datetime.combine(
                    target_date,
                    parse_time(session["start"]),
                    tzinfo=timezone,
                )

                if start > now:
                    upcoming.append({
                        **session,
                        "name": course["name"],
                        "start_datetime": start,
                    })

    return min(
        upcoming,
        key=lambda item: item["start_datetime"],
        default=None,
    )

