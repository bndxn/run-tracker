
import logging
import sys

import numpy as np

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
root_logger = logging.getLogger()

from garmindb.garmindb import Activities

from fetch_and_suggest.garmindb_cli import (ActivitiesDb, GarminConnectConfigManager,
                          download_data, gc_config, import_data)


def download_and_import_all_activity_data(debug=0, overwrite=True):
    """
    Download and import all available Garmin Connect personal and activity data. This information is stored to the
    directory HealthData in the root directory.
    """
    stats = gc_config.enabled_stats()

    logger.info("Starting full data download and import...")
    download_data(overwrite, latest=False, stats=stats, non_activity_data=False)
    import_data(debug, latest=False, stats=stats, non_activity_data=False)
    logger.info("Data download, import, and analysis complete.")


def load_database_and_get_activities(n_latest: int = 5):
    """
    Load a database instance.

    Returns:
    - Instance of GarminDb or ActivitiesDb
    """

    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    garmin_act_db = ActivitiesDb(db_params_dict)

    return Activities.get_latest(garmin_act_db, n_latest)

def convert_kph_to_mins_per_km(kph: float) -> tuple[int, int]:
    """Converts speed in kilometers per hour (kph) to pace in minutes and seconds per kilometer.

    Args:
        kph (float): Speed in kilometers per hour.

    Returns:
        tuple: A tuple (pace_minutes, pace_seconds) representing the time to complete one kilometer.
    """
    total_seconds_per_km = 3600 / kph
    pace_minutes = int(total_seconds_per_km // 60)
    pace_seconds = int(round(total_seconds_per_km % 60))
    return pace_minutes, pace_seconds


def extract_activity_metrics(activities: Activities) -> list[str]:
    """Retrieves and filters recent running activities within a given date range.

    This function queries the 100 most recent activities and returns a list of strings
    describing each run within the specified period. Each entry includes the start date,
    distance, duration, and pace in minutes per kilometer.

    Args:
        earliest_date (datetime): The start of the date range.
        latest_date (datetime): The end of the date range.

    Returns:
        list: A list of formatted strings for each run in the period, including the date,
              distance (in km), duration, and pace per kilometer.
    """
    output = []

    for activity in activities:
        if activity.sport == "running":
            pace_minutes, pace_seconds = convert_kph_to_mins_per_km(float(activity.avg_speed))
            h, m, s = map(lambda x: round(float(x)), str(activity.elapsed_time).split(":"))
            output.append(f"{activity.start_time.date()} - {np.round(activity.distance,1)} km - {h}:{m} "
                          f"- {pace_minutes}:{pace_seconds:02d} mins per km")

    return output



if __name__ == "__main__":
    download_and_import_all_activity_data(debug=1, overwrite=True)
    activities = load_database_and_get_activities(n_latest=5)
    for activity in activities:
        print(f"{activity.start_time.date()} - {np.round(activity.distance,2)}")
