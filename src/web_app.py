"""Flask app for providing web interface."""

import json

import boto3
import markdown
from botocore.exceptions import ClientError
from flask import Flask, render_template

app = Flask(__name__, template_folder="templates")

s3 = boto3.client("s3")
BUCKET_NAME = "run-tracker-suggestions"


def get_most_recent_runs_and_suggestions_from_s3():
    """Retrieve the most recent run data and suggestion from S3.

    Lists all objects under the 'lambda-outputs/' prefix in the S3 bucket,
    identifies the latest file by `LastModified`, downloads and parses its
    JSON content, and extracts the recent runs and suggestion.

    Returns
    -------
        tuple[list[str], str]: A tuple containing a list of recent runs and
        a suggested next run description.

    Raises
    ------
        Exception: If S3 listing fails, no files are found, or the file content
        cannot be parsed as JSON.

    """
    try:
        response = s3.list_objects_v2(
            Bucket=BUCKET_NAME, Prefix="lambda-outputs-intervals/"
        )
        objects = response.get("Contents", [])
        if not objects:
            raise Exception("No files found in S3 bucket.")
    except ClientError as e:
        raise Exception(f"Failed to list objects in S3 bucket: {e}")

    latest_file = max(objects, key=lambda obj: obj["LastModified"])
    key = latest_file["Key"]

    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        raw_content = response["Body"].read().decode("utf-8")
        first_layer = json.loads(raw_content)
    except Exception as e:
        raise Exception(f"Failed to parse content from {key}: {e}")

    recent_runs = first_layer.get("recent_runs", [])
    suggested_next_run = first_layer.get("suggestion", "No suggestion found.")
    return recent_runs, suggested_next_run


@app.route("/health")
def health():
    """Health check endpoint.

    Returns
    -------
        tuple[str, int]: A tuple containing a simple "OK" message and HTTP 200 status code.

    """
    return "OK", 200


@app.route("/")
def homepage():
    """Homepage route for displaying recent runs and a suggested next run.

    Fetches the latest run data and suggestion from S3, renders them using
    the `index.html` template, and applies basic Markdown formatting to the
    suggestion.

    Returns
    -------
        Response: The rendered HTML template as a Flask response object.

    """
    recent_runs, suggested_next_run = get_most_recent_runs_and_suggestions_from_s3()
    return render_template(
        "index.html",
        recent_runs=recent_runs,
        suggested_next_run=markdown.markdown(suggested_next_run, extensions=["nl2br"]),
    )


if __name__ == "__main__":
    app.run(debug=False, port=80, host="0.0.0.0")
