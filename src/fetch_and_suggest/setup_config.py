"""Sets up the user config dictionary required by GarminConnect, and the OpenAI API key."""

import json
import os

import boto3
from botocore.exceptions import ClientError

S3_BUCKET = os.environ.get("S3_BUCKET", "run-tracker-suggestions")
S3_PREFIX = os.environ.get("S3_PREFIX", "lambda-outputs-intervals")


def get_secret(secret_name: str, region_name: str = "eu-west-2"):
    """Retrieve a secret value from AWS Secrets Manager.

    Attempts to fetch and parse a secret stored in Secrets Manager.
    If the secret is a JSON string, it returns a dictionary. Otherwise, returns the raw string.

    Args:
    ----
        secret_name (str): The name of the secret to retrieve.
        region_name (str, optional): AWS region of the Secrets Manager. Defaults to "eu-west-2".

    Returns:
    -------
        dict | str: The parsed secret as a dictionary if JSON, else the raw string.

    Raises:
    ------
        RuntimeError: If the AWS client fails to retrieve the secret.

    """
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise RuntimeError(f"Failed to retrieve secret: {e}")

    secret_string = response["SecretString"]

    try:
        return json.loads(secret_string)
    except json.JSONDecodeError:
        return secret_string


def ensure_external_credentials_set():
    """Ensure all required external credentials are set as environment variables.

    Retrieves 'OPENAI_API_KEY', 'GARMIN_USERNAME' and 'GARMIN_PASSWORD' from AWS Secrets Manager
    and sets them as environment variables if not already set.
    """
    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = get_secret("OPENAI_API_KEY")
    if "GARMIN_USERNAME" not in os.environ:
        garmin_credentials = get_secret("garmin-credentials")
        os.environ["GARMIN_USERNAME"] = garmin_credentials["GARMIN_USERNAME"]
        os.environ["GARMIN_PASSWORD"] = garmin_credentials["GARMIN_PASSWORD"]
