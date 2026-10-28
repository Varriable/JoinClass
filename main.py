from datetime import datetime
from zoneinfo import ZoneInfo

from scheduler import load_config, find_current_class, find_next_class
from teams import join_meeting


def main():
    """Join the class that is on now, or report the next one."""
    config = load_config()
    timezone = ZoneInfo(config["timezone"])
    now = datetime.now(timezone)

    print(f"Current time: {now:%A %d %B %Y, %H:%M:%S}")

    current = find_current_class(config, now)

    if current:
        print(f"Class in progress: {current['name']}")
        print(f"Scheduled time: {current['start']} - {current['end']}")
        join_meeting(current)
        return

    print("No class is currently scheduled.")

    upcoming = find_next_class(config, now)

    if upcoming:
        print(f"Next class: {upcoming['name']}")
        print("Starts:", upcoming["start_datetime"].strftime("%A %d %B at %H:%M"))
    else:
        print("No upcoming classes were found.")


if __name__ == "__main__":
    main()
