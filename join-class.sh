#!/usr/bin/env bash
# Run the class joiner from anywhere, using the project's virtualenv.
set -euo pipefail

cd "$(dirname "$(readlink -f "$0")")"
exec .venv/bin/python main.py "$@"
