"""Main controller function for the run-tracker application."""

import numpy as np
import os
import subprocess
import sys
from datetime import datetime, timedelta
from download_and_import_separately import download_and_import_all_activity_data, load_database_and_get_activities
from coach import query_coach
from get_activities import extract_activity_metrics
from setup_config import dump_config
from config import dummy_response

DUMMY_RESPONSE = True


def main():
    if DUMMY_RESPONSE:
        recent_runs = dummy_response["recent_runs"],
        suggested_next_run = dummy_response["suggested_next_run"]
    else:
        download_and_import_all_activity_data()
        activities = load_database_and_get_activities()
        recent_runs = extract_activity_metrics(activities)
        suggested_next_run = query_coach(recent_runs)
    return recent_runs, suggested_next_run


if __name__ == "__main__":
    DUMMY_RESPONSE = False
    recent_runs, suggested_next_run = main()
