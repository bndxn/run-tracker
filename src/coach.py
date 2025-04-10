import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


from datetime import datetime

today = datetime.today().strftime('%Y-%m-%d')


def query_coach(recent_running_times: str):

    openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI()

    prompt = (
        "You are a running coach helping runners train for a half marathon. Here are a runner's recent runs:"
        f"{recent_running_times}\n. Today's date is {today}. "
        "Suggest a workout for them today, or tomorrow if they've already done a run today. Be concise."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "text"},
        max_completion_tokens=500,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    response = query_coach("5k in 25 minutes")
    print(response)
