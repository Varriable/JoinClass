import subprocess
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from scheduler import load_config, find_current_class, find_next_class
from teams import check_browser, join_meeting


LOG_FILE = Path(__file__).with_name("join.log")

# Passed to the background copy of this script so it joins instead of relaunching.
FOREGROUND_FLAG = "--foreground"


def join_in_background():
    """Re-run this script detached from the terminal to do the joining."""
    options = {}

    if sys.platform == "win32":
        options["creationflags"] = (
            subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP
        )
    else:
        options["start_new_session"] = True

    with LOG_FILE.open("a") as log:
        subprocess.Popen(
            # -u keeps the log in order by not buffering output.
            [sys.executable, "-u", str(Path(__file__).resolve()), FOREGROUND_FLAG],
            stdin=subprocess.DEVNULL,
            stdout=log,
            stderr=log,
            **options,
        )

    print(f"Joining in the background. Output goes to {LOG_FILE.name}.")


def main():
    """Join the class that is on now, or report the next one."""
    foreground = FOREGROUND_FLAG in sys.argv[1:]

    config = load_config()
    timezone = ZoneInfo(config["timezone"])
    now = datetime.now(timezone)

    print(f"Current time: {now:%A %d %B %Y, %H:%M:%S}")

    current = find_current_class(config, now)

    if current:
        print(f"Class in progress: {current['name']}")
        print(f"Scheduled time: {current['start']} - {current['end']}")

        try:
            check_browser()
        except RuntimeError as error:
            print(error)
            sys.exit(1)

        if foreground:
            join_meeting(current)
        else:
            join_in_background()
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
