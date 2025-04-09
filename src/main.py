import os
import subprocess
import sys
from datetime import datetime, timedelta

from coach import query_coach
from get_activities import get_running_in_period
from setup_config import dump_config

# DUMMY_RESPONSE = True if os.getenv("DUMMY_RESPONSE") == "" else False
DUMMY_RESPONSE = True

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
            "2025-03-26 - 5.76 km - 0:40:31 - 5:27 mins per km",
            "2025-03-25 - 8.59 km - 0:46:04 - 4:33 mins per km",
            "2025-03-23 - 21.26 km - 1:59:18 - 5:08 mins per km",
            "2025-03-22 - 5.59 km - 0:33:22 - 5:52 mins per km",
            "2025-03-22 - 3.61 km - 0:30:21 - 6:13 mins per km"
        ]
        suggested_next_run = (
            "Based on your recent runs, let's focus on a tempo workout today to improve speed and endurance for the "
            "half marathon. Here's the plan:\n\n"
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
