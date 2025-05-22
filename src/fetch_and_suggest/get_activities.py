"""Contains helpers to get activities from GarminDB and return them in an easily-readable format."""

import numpy as np
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import Activities, ActivitiesDb


def convert_kph_to_mins_per_km(kph: float) -> tuple[int, int]:
    """Convert speed in kilometers per hour (kph) to pace in minutes and seconds per kilometer.

    Args:
    ----
        kph (float): Speed in kilometers per hour.

    Returns:
    -------
        tuple: A tuple (pace_minutes, pace_seconds) representing the time to complete one kilometer.

    """
    total_seconds_per_km = 3600 / kph
    pace_minutes = int(total_seconds_per_km // 60)
    pace_seconds = int(round(total_seconds_per_km % 60))
    return pace_minutes, pace_seconds


def get_running_in_period() -> list[str]:
    """Retrieve and filter recent running activities within a given date range.

    This function queries the 100 most recent activities and returns a list of strings
    describing each run within the specified period. Each entry includes the start date,
    distance, duration, and pace in minutes per kilometer.

    Args:
    ----
        earliest_date (datetime): The start of the date range.
        latest_date (datetime): The end of the date range.

    Returns:
    -------
        list: A list of formatted strings for each run in the period, including the date,
              distance (in km), duration, and pace per kilometer.

    """
    output = []

    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()

    garmin_act_db = ActivitiesDb(db_params_dict)

    activities = Activities.get_latest(garmin_act_db, 5)
    for activity in activities:
        if activity.sport == "running":
            pace_minutes, pace_seconds = convert_kph_to_mins_per_km(
                float(activity.avg_speed)
            )
            h, m = map(lambda x: round(float(x)), str(activity.elapsed_time).split(":"))
            output.append(
                f"{activity.start_time.date()} - {np.round(activity.distance,1)} km - {h}:{m} "
                f"- {pace_minutes}:{pace_seconds:02d} mins per km"
            )

    return output
