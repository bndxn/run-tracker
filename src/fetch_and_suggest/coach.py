"""Contains helpers to send training data to a coach and obtain suggested work."""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def query_coach(recent_running_times: str) -> str:
    """Generates a running workout suggestion based on recent running activity.

    Uses OpenAI's GPT model to act as a virtual running coach. It takes recent
    running times as input and returns a concise workout suggestion tailored
    to the runner's recent performance.

    Args:
        recent_running_times (str): A string summarizing recent running activity.

    Returns:
        str: A concise workout suggestion for the runner.

    Raises:
        openai.OpenAIError: If the API request fails.
        EnvironmentError: If the OpenAI API key is not set in environment variables.
    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI()

    prompt = (
        "You are a running coach helping runners train for a half marathon. "
        f"Here are a runner's recent runs: {recent_running_times}\n"
        "Suggest a workout for them today. Be concise."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "text"},
        max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content
