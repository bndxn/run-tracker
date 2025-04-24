
import logging
import sys
import numpy as np

logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
root_logger = logging.getLogger()

from garmindb_cli import gc_config, download_data, import_data, ActivitiesDb, GarminConnectConfigManager
from garmindb.garmindb import Activities

def download_and_import_all_activity_data(debug=0, overwrite=True):
    """Download and import all available Garmin Connect activity data."""
    stats = gc_config.enabled_stats()

    logger.info("Starting full data download and import...")
    download_data(overwrite, latest=False, stats=stats, non_activity_data=False)
    import_data(debug, latest=False, stats=stats, non_activity_data=False)
    logger.info("Data download, import, and analysis complete.")


def load_database(db_type="garmin"):
    """
    Load a database instance.

    Parameters:
    - db_type (str): either 'garmin' or 'activities'

    Returns:
    - Instance of GarminDb or ActivitiesDb
    """

    gc_config = GarminConnectConfigManager()
    db_params_dict = gc_config.get_db_params()
    garmin_act_db = ActivitiesDb(db_params_dict)

    return Activities.get_latest(garmin_act_db, 10)


if __name__ == "__main__":
    download_and_import_all_activity_data(debug=1, overwrite=True)
    activities = load_database(db_type="activities")
    for activity in activities:
        print(f"{activity.start_time.date()} - {np.round(activity.distance,2)}")
