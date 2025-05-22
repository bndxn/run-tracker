"""Main controller function for the run-tracker application."""

import json
import os
import subprocess
import sys
from datetime import datetime

import boto3

from fetch_and_suggest.coach import query_coach
from fetch_and_suggest.get_activities import get_running_in_period
from fetch_and_suggest.setup_config import (
    S3_BUCKET,
    S3_PREFIX,
    dump_config,
    ensure_external_credentials_set,
)

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
        "--analyze",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.stderr:
        print("Errors:", result.stderr)

    if result.returncode != 0:
        print(f"Script exited with errors (code {result.returncode})")


def generate_suggestion():
    ensure_external_credentials_set()
    dump_config()
    if DUMMY_RESPONSE:
        return (["A recent run", "Another run"], "Run 10K at 5mins per km")
    else:
        run_garmindb_cli()
        recent_runs = get_running_in_period()
        suggestion = query_coach(recent_runs)
        return recent_runs, suggestion


def save_to_s3(data: dict, bucket: str, prefix: str) -> str:
    key = f"{prefix}/recent_runs_{datetime.now().isoformat()}.json"
    s3.put_object(
        Bucket=bucket, Key=key, Body=json.dumps(data), ContentType="application/json"
    )
    return key


def lambda_handler(event, context):
    recent_runs, suggestion = generate_suggestion()

    output = {
        "timestamp": datetime.now().isoformat(),
        "recent_runs": recent_runs,
        "suggestion": suggestion,
    }

    key = save_to_s3(output, S3_BUCKET, S3_PREFIX)

    return {
        "statusCode": 200,
        "body": json.dumps(
            {"s3_key": key, "recent_runs": recent_runs, "suggestion": suggestion}
        ),
    }
