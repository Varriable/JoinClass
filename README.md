# Teams Class Joiner

Checks your timetable and, if a class is on right now, opens Chrome and joins its Microsoft Teams meeting using the meeting ID and passcode.

## Setup

```bash
python3 -m venv .venv
.venv/bin/pip install playwright
.venv/bin/playwright install chrome
cp classes.example.json classes.json
```

Edit `classes.json` with your classes: day, start and end time (24-hour), meeting ID and passcode for each session.

## Usage

```bash
./join-class.sh
```

`join-class.sh` runs `main.py` with the project's virtualenv, so it works from any directory.

To run it with a single word, add an alias to `~/.bashrc` (change the path to where you cloned the repo):

```bash
echo "alias joinclass='$HOME/teams-class-joiner/join-class.sh'" >> ~/.bashrc
source ~/.bashrc
```

Then just run `joinclass`.

If a class is in progress, Chrome opens and joins the meeting. Otherwise it prints the next class and exits.

The first run opens a fresh Chrome profile (stored in `~/.config/teams-joiner-chrome`). Sign in to Teams there once and it stays signed in.

To run it automatically, schedule `join-class.sh` (e.g. with cron) at your class start times.

## Files

- `join-class.sh` - launcher script
- `main.py` - entry point
- `scheduler.py` - reads `classes.json` and finds the current/next class
- `teams.py` - opens Chrome and fills in the Teams join form
- `classes.example.json` - template for `classes.json`
