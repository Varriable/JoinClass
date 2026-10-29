# Teams Class Joiner

Checks your timetable and, if a class is on right now, opens Chrome and joins its Microsoft Teams meeting using the meeting ID and passcode. Works on Linux and Windows.

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then from the project folder:

```bash
uv sync
uv run playwright install chromium
cp classes.example.json classes.json
```

On Windows, use `copy classes.example.json classes.json` for the last step.

If Google Chrome is installed it is used; otherwise it falls back to Playwright's own Chromium, which the `install chromium` step downloads (no admin rights needed).

Edit `classes.json` with your classes: day, start and end time (24-hour), meeting ID and passcode for each session.

## Usage

Linux:

```bash
./join-class.sh
```

Windows:

```bat
join-class.bat
```

Both run `main.py` through uv, so they work from any directory.

If a class is in progress, Chrome opens and joins the meeting in the background, so the terminal is free straight away (any errors go to `join.log`). Otherwise it prints the next class and exits.

The first run opens a fresh Chrome profile (stored in `~/.config/teams-joiner-chrome`, or `C:\Users\<you>\.config\teams-joiner-chrome` on Windows). Sign in to Teams there once and it stays signed in.

### Shortcut command

Linux (bash) - change the path to where you cloned the repo:

```bash
echo "alias joinclass='$HOME/teams-class-joiner/join-class.sh'" >> ~/.bashrc
source ~/.bashrc
```

Windows (PowerShell):

```powershell
New-Item -Force -ItemType File $PROFILE | Out-Null
Add-Content $PROFILE "function joinclass { & `"$HOME\teams-class-joiner\join-class.bat`" }"
. $PROFILE
```

Then just run `joinclass`.

### Running it automatically

Schedule the launcher at your class start times:

- **Linux:** cron, e.g. `15 8 * * 1-5 DISPLAY=:0 $HOME/teams-class-joiner/join-class.sh`
- **Windows:** Task Scheduler, e.g. `schtasks /create /tn "Join class" /sc weekly /d MON,TUE,WED,FRI /st 08:15 /tr "%USERPROFILE%\teams-class-joiner\join-class.bat"`

## Files

- `join-class.sh` / `join-class.bat` - launcher scripts
- `main.py` - entry point
- `scheduler.py` - reads `classes.json` and finds the current/next class
- `teams.py` - opens the browser and fills in the Teams join form
- `classes.example.json` - template for `classes.json`
- `pyproject.toml` / `uv.lock` - dependencies, managed by uv
