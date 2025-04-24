"""Main controller function for the run-tracker application."""

import os
import json
from pathlib import Path

from fetch_and_suggest.coach import query_coach
from fetch_and_suggest.get_activities import (
    download_and_import_all_activity_data, load_database_and_get_activities, extract_activity_metrics)
from fetch_and_suggest.setup_config import dump_config, garmin_config

CONFIG_PATH = Path.home() / ".GarminDb" / "GarminConnectConfig.json"


#TODO: this should also run setup_config.py


def ensure_config_exists():
    if CONFIG_PATH.exists():
        return

    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)

    config = {
        "username": os.environ["GARMIN_USERNAME"],
        "password": os.environ["GARMIN_PASSWORD"]
    }

    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f)


def fetch_and_generate_suggestions():
    download_and_import_all_activity_data()
    activities = load_database_and_get_activities()
    recent_runs = extract_activity_metrics(activities)
    suggested_next_run = query_coach(recent_runs)
    return recent_runs, suggested_next_run

#TODO: this should save to S3


def lambda_handler(event, context):
    ensure_config_exists()

    # Delay this import until after config is written
    import garmindb

    # Your GarminDB logic here
    db = garmindb.GarminDB()
    activities = db.get_activities()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Fetched {len(activities)} activities"
        })
    }


if __name__ == "__main__":
    dump_config(garmin_config)
    recent_runs, suggested_next_run = fetch_and_generate_suggestions()
    print(f"Recent runs: {recent_runs}")
    print(f"Suggested run: {suggested_next_run}")
