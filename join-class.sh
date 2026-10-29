#!/usr/bin/env bash
# Run the class joiner from anywhere, using the project's uv environment.
set -euo pipefail

# uv's default install location, which cron and desktop launchers don't have on PATH.
export PATH="$HOME/.local/bin:$PATH"

cd "$(dirname "$(readlink -f "$0")")"
exec uv run main.py "$@"
