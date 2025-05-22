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
    """Execute the GarminDB CLI script with predefined arguments.

    This function runs `garmindb_cli.py` using subprocess with
    flags to download, import, and analyze activities. Any stderr
    output or non-zero exit codes are printed to stdout.
    """
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
    """Generate a running suggestion based on recent Garmin activity.

    This function loads external credentials and configuration,
    optionally returns a dummy response for testing, or invokes the
    GarminDB CLI to fetch recent runs, then queries a coach model
    for a suggested next workout.

    Returns
    -------
        tuple[list[str], str]: A tuple containing a list of recent runs and
        a suggestion string.

    """
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
    """Save a dictionary as a JSON object to an S3 bucket.

    Args:
    ----
        data (dict): The data to save.
        bucket (str): The S3 bucket name.
        prefix (str): The key prefix to use.

    Returns:
    -------
        str: The full S3 key of the stored object.

    """
    key = f"{prefix}/recent_runs_{datetime.now().isoformat()}.json"
    s3.put_object(
        Bucket=bucket, Key=key, Body=json.dumps(data), ContentType="application/json"
    )
    return key


def lambda_handler(event, context):
    """AWS Lambda handler for generating and storing run suggestions.

    This function is intended as an entrypoint for an AWS Lambda function.
    It generates a suggestion based on recent Garmin activity, stores the
    result in S3, and returns a JSON response containing the S3 key and
    the suggestion.

    Args:
    ----
        event: The Lambda event payload.
        context: The Lambda context runtime information.

    Returns:
    -------
        dict: A dictionary with HTTP status code and JSON body containing
        the result key and data.

    """
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
