"""Main controller function for the run-tracker application."""

import os
import subprocess
import sys
from datetime import datetime, timedelta

from coach import query_coach
from get_activities import get_running_in_period
from setup_config import dump_config

DUMMY_RESPONSE = False

def run_garmindb_cli():
    script_path = os.path.abspath("src/garmindb_cli.py")
    cmd = [
        sys.executable,
        script_path,
        "--activities",
        "--download",
        "--import",
        "--analyze",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("Output:", result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

    if result.returncode != 0:
        print(f"Script exited with errors (code {result.returncode})")
    else:
        print("Script completed successfully")

def main():
    if DUMMY_RESPONSE:
        recent_runs = [
            "2025-04-16 - 7.4 km - 0:41 - 5:14 mins per km",
            "2025-04-14 - 11.6 km - 1:16 - 5:08 mins per km",
            "2025-04-10 - 21.2 km - 1:44 - 4:48 mins per km",
        ]
        suggested_next_run = (
            "Based on your recent runs, let's focus on a tempo workout today to improve speed and endurance for the "
            "half marathon. Here's the plan stan:\n\n"
            "**Workout: Tempo Run**\n"
            "**Warm-Up:** 10-15 minutes easy jog.\n"
            "**Tempo Portion:** 3 x 2 km at your goal half marathon pace (around 5:08 mins/km), with 2-minute walking or light "
            "jogging breaks in between.\n"
            "**Cool-Down:** 10 minutes easy jog. Remember to stretch after the run and stay hydrated.")
    else:
        run_garmindb_cli()
        recent_runs = get_running_in_period(
            datetime.today() - timedelta(days=7), datetime.today()
        )
        suggested_next_run = query_coach(recent_runs)
    return recent_runs, suggested_next_run


if __name__ == "__main__":
    run_garmindb_cli()
    last_week = get_running_in_period(
        datetime.today() - timedelta(days=7), datetime.today()
    )
    print(last_week)
    print("Generating a suggested workout for today:")
    suggestion = query_coach(last_week)
    print(suggestion)
