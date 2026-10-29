@echo off
rem Run the class joiner from anywhere, using the project's uv environment.
cd /d "%~dp0"
uv run main.py %*
