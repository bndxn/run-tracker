from datetime import datetime

import numpy as np
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import Activities, ActivitiesDb, ActivityLaps, GarminDb

gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()

garmin_db = GarminDb(db_params_dict)
garmin_act_db = ActivitiesDb(db_params_dict)


def convert_kph_to_mins_per_km(kph: float):

    total_seconds_per_km = 3600 / kph
    pace_minutes = int(total_seconds_per_km // 60)
    pace_seconds = int(round(total_seconds_per_km % 60))
    return pace_minutes, pace_seconds


def get_running_in_period(earliest_date: datetime, latest_date: datetime):

    """Queries the 100 most recent activities, then returns the date, distance, and duration for those in a period.

    Returns:
        list: a list containing dictionaries of the starting date, distance, and duration, for each run in the period.
    """

    output = []

    activities = Activities.get_latest(garmin_act_db, 10)
    for activity in activities:
        if (activity.sport == "running" and earliest_date < activity.stop_time < latest_date):
            pace_minutes, pace_seconds = convert_kph_to_mins_per_km(float(activity.avg_speed))
            h, m, s = map(lambda x: round(float(x)), str(activity.elapsed_time).split(":"))
            output.append(f"{activity.start_time.date()} - {np.round(activity.distance,1)} km - {h}:{m} "
                          f"- {pace_minutes}:{pace_seconds:02d} mins per km")

    return output
