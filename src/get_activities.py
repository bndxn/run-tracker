import numpy as np
from datetime import datetime
from garmindb import GarminConnectConfigManager
from garmindb.garmindb import GarminDb, ActivitiesDb, Activities, ActivityLaps

gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()

garmin_db = GarminDb(db_params_dict)
garmin_act_db = ActivitiesDb(db_params_dict)


def get_running_in_period(earliest_date: datetime, latest_date: datetime):

    """Queries the 100 most recent activities, then returns the date, distance, and duration for those in a period.

    Returns:
        list: a list containing dictionaries of the starting date, distance, and duration, for each run in the period.
    """

    output = []

    activities = Activities.get_latest(garmin_act_db, 100)
    for activity in activities:
        if (
            activity.sport == "running"
            and earliest_date < activity.stop_time < latest_date
        ):
            h, m, s = map(
                lambda x: round(float(x)), str(activity.elapsed_time).split(":")
            )
            output.append(
                {
                    "date": f"{activity.start_time.date()}",
                    "distance": f"{np.round(activity.distance,2)} km",
                    "duration": f"{h} hour {m} mins {s} seconds"
                    if h > 0
                    else f"{m} mins {s} seconds",
                }
            )

    return output
