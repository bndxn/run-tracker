import json

import requests

# Define the event to send to the Lambda function
event = {"key1": "value1", "key2": "value2"}

# Lambda Runtime API URL (default for local container testing)
LAMBDA_URL = "http://localhost:9001/2015-03-31/functions/function/invocations"


def invoke_lambda(event_payload):
    response = requests.post(
        LAMBDA_URL,
        data=json.dumps(event_payload),
        headers={"Content-Type": "application/json"},
    )
    return response


if __name__ == "__main__":
    response = invoke_lambda(event)
    print("Status code:", response.status_code)
    print("Response body:", response.text)
