#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from garmindb import (
    Download, GarminConnectConfigManager, GarminDb, GarminTcxData,
    GarminJsonSummaryData, GarminJsonDetailsData, GarminActivitiesFitData,
    ActivityFitFileProcessor, Analyze, Attributes, Statistics, FitFileProcessor, PluginManager
)
from garmindb.garmindb import ActivitiesDb

logging.basicConfig(filename="garmindb.log", filemode="w", level=logging.INFO)
logger = logging.getLogger(__file__)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))
root_logger = logging.getLogger()

gc_config = GarminConnectConfigManager()
db_params_dict = gc_config.get_db_params()
plugin_manager = PluginManager(gc_config.get_plugins_dir(), db_params_dict)


def __get_date_and_days(db, latest, table, col, stat_name):
    import datetime
    last_ts = table.latest_time(db, col)
    if latest and last_ts is not None:
        date = last_ts.date() - datetime.timedelta(days=1)
        days = (datetime.date.today() - date).days
    else:
        date, days = gc_config.stat_start_date(stat_name)
        days = min((datetime.date.today() - date).days, days)
    return date, days


def download_data(overwite, latest):
    logger.info("___Downloading Data___")
    download = Download()
    if not download.login():
        logger.error("Failed to login!")
        sys.exit()

    activity_count = gc_config.latest_activity_count() if latest else gc_config.all_activity_count()
    activities_dir = gc_config.get_activities_dir()
    root_logger.info("Fetching %d activities to %s", activity_count, activities_dir)
    download.get_activity_types(activities_dir, overwite)
    download.get_activities(activities_dir, activity_count, overwite)


def import_data(debug, latest):
    logger.info("___Importing Data___")
    activities_dir = gc_config.get_activities_dir()
    db = GarminDb(db_params_dict)
    measurement_system = Attributes.measurements_type(db)

    gtd = GarminTcxData(activities_dir, latest, measurement_system, debug)
    if gtd.file_count() > 0:
        gtd.process_files(db_params_dict)

    gjsd = GarminJsonSummaryData(db_params_dict, activities_dir, latest, measurement_system, debug)
    if gjsd.file_count() > 0:
        gjsd.process()

    gdjd = GarminJsonDetailsData(db_params_dict, activities_dir, latest, measurement_system, debug)
    if gdjd.file_count() > 0:
        gdjd.process()

    gfd = GarminActivitiesFitData(activities_dir, latest, measurement_system, debug)
    if gfd.file_count() > 0:
        gfd.process_files(ActivityFitFileProcessor(db_params_dict, plugin_manager, debug))


def analyze_data(debug):
    logger.info("___Analyzing Data___")
    analyze = Analyze(db_params_dict, debug - 1)
    analyze.summary()
    analyze.create_dynamic_views()


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--trace", type=int, default=0)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--import", dest="import_data", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--activities", action="store_true")
    parser.add_argument("-l", "--latest", action="store_true")
    parser.add_argument("-o", "--overwrite", action="store_true")
    args = parser.parse_args()

    if args.trace > 0:
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    if args.download and args.activities:
        download_data(args.overwrite, args.latest)
    if args.import_data and args.activities:
        import_data(args.trace, args.latest)
    if args.analyze:
        analyze_data(args.trace)


if __name__ == "__main__":
    main(sys.argv[1:])
