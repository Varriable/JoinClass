from pathlib import Path

from playwright.sync_api import Playwright, sync_playwright


MEETING_URL = "https://www.microsoft.com/en-us/microsoft-teams/join-a-meeting"

# A dedicated Chrome profile that keeps its cookies and logins between runs.
# Sign in to Teams once in the window this opens and it stays signed in.
PROFILE_DIR = Path.home() / ".config" / "teams-joiner-chrome"


def join(playwright: Playwright, meeting) -> None:
    context = playwright.chromium.launch_persistent_context(
        PROFILE_DIR,
        channel="chrome",  # use the installed Google Chrome, not Playwright's Chromium
        headless=False,
        no_viewport=True,
        chromium_sandbox=True,  # Playwright passes --no-sandbox unless told otherwise
        ignore_default_args=["--enable-automation"],  # hides the "controlled by automated software" bar
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto(MEETING_URL)

    page.get_by_role("textbox", name="Enter meeting ID").fill(meeting["meeting_id"])
    page.get_by_role("textbox", name="Enter meeting Passcode").fill(meeting["passcode"])
    page.get_by_role("button", name="Join a Teams meeting now.").click()

    # Keep the browser open for the class; it closes when you close the window.
    context.wait_for_event("close", timeout=0)


def join_meeting(meeting):
    """Open Chrome and join the given class's meeting."""
    with sync_playwright() as playwright:
        join(playwright, meeting)
