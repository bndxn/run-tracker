"""Sets up the user config dictionary required by GarminConnect, and the OpenAI API key."""

import json
import os
from pathlib import Path

import boto3
from botocore.exceptions import ClientError

S3_BUCKET = os.environ.get("S3_BUCKET", "run-tracker-suggestions")
S3_PREFIX = os.environ.get("S3_PREFIX", "lambda-outputs")


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


def dump_config() -> None:
    """Dump the provided Garmin Connect configuration to a JSON file.

    This function writes the given `config` dictionary to a file named
    `GarminConnectConfig.json` in the user's home directory under the `.GarminDb` folder.
    If the directory does not exist, it is created.

    Raises
    ------
        TypeError: If `config` contains non-serializable values.
        OSError: If the file or directory cannot be created or written to.

    """
    config = {
        "db": {"type": "sqlite"},
        "garmin": {"domain": "garmin.com"},
        "credentials": {
            "user": os.environ.get("GARMIN_USERNAME"),
            "secure_password": False,
            "password": os.environ.get("GARMIN_PASSWORD"),
        },
        "data": {
            "weight_start_date": "01/01/2025",
            "sleep_start_date": "01/01/2025",
            "rhr_start_date": "01/01/2025",
            "monitoring_start_date": "01/01/2025",
            "download_latest_activities": 5,
            "download_all_activities": 10,
        },
        "directories": {
            "relative_to_home": True,
            "base_dir": "HealthData",
            "mount_dir": "/Volumes/GARMIN",
        },
        "enabled_stats": {
            "monitoring": False,
            "steps": False,
            "itime": False,
            "sleep": False,
            "rhr": False,
            "weight": False,
            "activities": False,
        },
        "course_views": {"steps": []},
        "modes": {},
        "activities": {"display": []},
        "settings": {
            "metric": False,
            "default_display_activities": ["running", "cycling"],
        },
        "checkup": {"look_back_days": 90},
    }

    home_dir = Path.home()
    config_path = home_dir / ".GarminDb" / "GarminConnectConfig.json"

    config_path.parent.mkdir(parents=True, exist_ok=True)

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
