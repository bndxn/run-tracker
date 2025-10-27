"""Contains helpers to send training data to a coach and obtain suggested work."""

import os

from dotenv import load_dotenv
from openai import OpenAI

from fetch_and_suggest.training import guidance, plan

load_dotenv()


def query_coach(recent_running_times: str) -> str:
    """Generate a running workout suggestion based on recent running activity.

    Uses OpenAI's GPT model to act as a virtual running coach. It takes recent
    running times as input and returns a concise workout suggestion tailored
    to the runner's recent performance.

    Args:
    ----
        recent_running_times (str): A string summarizing recent running activity.

    Returns:
    -------
        str: A concise workout suggestion for the runner.

    Raises:
    ------
        openai.OpenAIError: If the API request fails.
        EnvironmentError: If the OpenAI API key is not set in environment variables.

    """
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI()

    prompt = (
        "You are a running coach helping runners train for a half marathon with reference to a training plan."
        f"Here is their training plan: {plan}"
        f"Here are a runner's recent runs: {recent_running_times}\n"
        f"{guidance}"
    )

    response = client.chat.completions.create(
        model="gpt-5-mini-2025-08-07",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "text"},
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content


def pretty_format(runs: str) -> str:
    """Convert a string of activity dictionaries into a Markdown bullet list for the web.

    The input is a string containing a list of dictionaries that describe running activities. Interval runs may include
    phrases like “VO2-max / speed session”, “Progressive long”, or “easy tempo”. Regular runs are labeled “running” and
    may include a location.

    Returns
    -------
        str: A clean Markdown bullet list. Regular runs render as one bullet.

    """
    guidance = """
You are given structured output containing running activities. Each activity may be a regular run or an interval run.
Intervals will have words like " VO2-max / speed session", or "Progressive long" or "easy tempo". Regular runs will have "running" possibly with a location.
Convert this data into a clean HTML unordered list (<ul>) with the following rules:

For regular runs, output one bullet:
For regular runs, output one <li> inside a top-level <ul>:

HTML template:
<ul>
  <li>[Date] – [Name], [distance_km] km, [duration_min] min, pace [pace_min_per_km]/km, avg HR [avg_hr]</li>
</ul>

For interval runs, output a parent <li> summary with a nested <ul> of intervals:

HTML template:
<ul>
  <li>[Date] – [Name], total [sum distance_km] km, total [sum duration_min] min, avg pace [average pace], avg HR [average of avg_hr values]
    <ul>
      <li>Interval [index] – [distance_km] km, [duration_min] min, pace [pace_min_per_km]/km, avg HR [avg_hr]</li>
      <!-- repeat for each active interval -->
    </ul>
  </li>
</ul>

Additional instructions:

Output valid HTML only (no Markdown). Do not include <html>, <head>, or <body>—just the <ul>/<li> structure.

Dates should be taken from start_time_local (YYYY-MM-DD).

Keep numbers to one decimal place where appropriate.

There are rest intervals which should be removed. If an interval is very short, e.g. 0.0 - 0.1 km, or is a obviously at a significantly slower pace e.g. slower than 6:30 min/ km, remove it.

For interval summaries, compute statistics only of the active intervals, discarding the any intervals. Compute total distance and average heart rate (mean of intervals). Do not add any preamble - only include the bullet points as requested.
""".strip()

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY not found in environment variables.")

    client = OpenAI()

    prompt = guidance + "\n" + runs

    response = client.chat.completions.create(
        model="gpt-5-mini-2025-08-07",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "text"},
        # max_completion_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content
