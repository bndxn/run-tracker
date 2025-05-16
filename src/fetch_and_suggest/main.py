"""Main controller function for the run-tracker application."""

from fetch_and_suggest.setup_config import config, dump_config

dump_config(config)

import json
import os
import subprocess
import sys
from datetime import datetime, timedelta

import boto3

from fetch_and_suggest.coach import query_coach
from fetch_and_suggest.get_activities import get_running_in_period
from fetch_and_suggest.setup_config import S3_BUCKET, S3_PREFIX

s3 = boto3.client("s3")

DUMMY_RESPONSE = False

def run_garmindb_cli():
    script_path = os.path.abspath("src/fetch_and_suggest/garmindb_cli.py")
    cmd = [
        sys.executable,
        script_path,
        "--activities",
        "--download",
        "--import",
        "--analyze"
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stderr:
        print("Errors:", result.stderr)

    if result.returncode != 0:
        print(f"Script exited with errors (code {result.returncode})")

def generate_suggestion():
    run_garmindb_cli()
    recent_runs = get_running_in_period()
    suggestion = query_coach(recent_runs)
    return recent_runs, suggestion

def main():
    if DUMMY_RESPONSE:
        recent_runs = [
            "2025-04-16 - 7.4 km - 0:41 - 5:14 mins per km",
            "2025-04-14 - 11.6 km - 1:16 - 5:08 mins per km",
            "2025-04-10 - 21.2 km - 1:44 - 4:48 mins per km"
            "Date - distance km - time - pace ",
        ]
        suggestion = (
            "Dummy next run"
            "Run 10K at a 5 mins per km pace! Why not?")
        return recent_runs, suggestion
    else:
        return generate_suggestion()


def save_to_s3(data: dict, bucket: str, prefix: str) -> str:
    key = f"{prefix}/recent_runs_{datetime.now().isoformat()}.json"
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data),
        ContentType="application/json"
    )
    return key

def lambda_handler(event, context):
    recent_runs, suggestion = generate_suggestion()

    output = {
        "timestamp": datetime.now().isoformat(),
        "recent_runs": recent_runs,
        "suggestion": suggestion
    }

    key = save_to_s3(output, S3_BUCKET, S3_PREFIX)

    return {
        'statusCode': 200,
        'body': json.dumps({"s3_key": key, "recent_runs": recent_runs, "suggestion": suggestion})
    }

if __name__ == "__main__":
    recent_runs, suggestion = generate_suggestion()
    print(recent_runs, suggestion)
