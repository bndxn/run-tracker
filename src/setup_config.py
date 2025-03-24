import os
import json
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

config = {
    "db": {
        "type"                          : "sqlite"
    },
    "garmin": {
        "domain"                        : "garmin.com"
    },
    "credentials": {
        "user"                          : os.environ.get("GARMIN_USERNAME"),
        "secure_password"               : False,
        "password"                      : os.environ.get("GARMIN_PASSWORD")
    },
    "data": {
        "weight_start_date"             : "01/01/2025",
        "sleep_start_date"              : "01/01/2025",
        "rhr_start_date"                : "01/01/2025",
        "monitoring_start_date"         : "01/01/2025",
        "download_latest_activities"    : 5,
        "download_all_activities"       : 10
    },
    "directories": {
        "relative_to_home"              : True,
        "base_dir"                      : "HealthData",
        "mount_dir"                     : "/Volumes/GARMIN"
    },
    "enabled_stats": {
        "monitoring"                    : False,
        "steps"                         : False,
        "itime"                         : False,
        "sleep"                         : False,
        "rhr"                           : False,
        "weight"                        : False,
        "activities"                    : False
    },
    "course_views": {
        "steps"                         : []
    },
    "modes": {
    },
    "activities": {
        "display"                       : []
    },
    "settings": {
        "metric"                        : False,
        "default_display_activities"    : ["running", "cycling"]
    },
    "checkup": {
        "look_back_days"                : 90
    }
}


def dump_config():
    home_dir = Path.home()
    config_path = home_dir / ".GarminDb" / "GarminConnectConfig.json"

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

if __name__ == "__main__":
    dump_config()
