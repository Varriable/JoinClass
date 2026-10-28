import os
import sys
import traceback
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from scheduler import load_config, find_current_class, find_next_class
from teams import join_meeting


LOG_FILE = Path(__file__).with_name("join.log")


def join_in_background(meeting):
    """Join the meeting in a detached process so the terminal is freed."""
    if os.fork() > 0:
        print(f"Joining in the background. Output goes to {LOG_FILE.name}.")
        return

    # Child: leave the terminal's session and send output to the log file.
    os.setsid()
    with open(os.devnull) as devnull, LOG_FILE.open("a") as log:
        os.dup2(devnull.fileno(), 0)
        os.dup2(log.fileno(), 1)
        os.dup2(log.fileno(), 2)

    try:
        join_meeting(meeting)
    except BaseException:
        sys.stdout.flush()
        traceback.print_exc()
    finally:
        os._exit(0)


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
        join_in_background(current)
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
