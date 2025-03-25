import subprocess
import sys
import os
from datetime import datetime, timedelta

from get_activities import get_running_in_period
from coach import query_coach
from setup_config import dump_config


def run_garmindb_cli():
    script_path = os.path.abspath("src/garmindb_cli.py")
    cmd = [
        sys.executable,
        script_path,
        "--activities",
        "--download",
        # "--import",
        ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("Output:", result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

    if result.returncode != 0:
        print(f"Script exited with errors (code {result.returncode})")
    else:
        print("Script completed successfully")


if __name__ == "__main__":
    run_garmindb_cli()
    print("Downloading recent runs:")
    recent_runs = get_running_in_period(
        datetime.today() - timedelta(days=7), datetime.today()
    )
    for run in recent_runs:
        print(f"* {run["date"]} - {run["distance"]} - {run["duration"]}")
    print("Generating a suggested workout for today:")
    suggestion = query_coach(recent_runs)
    print(suggestion)
