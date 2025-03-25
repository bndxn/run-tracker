import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime

load_dotenv()


def query_coach(recent_running_times: str):

    openai_api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=openai_api_key)

    prompt = (
        "You are a running coach helping a runner prepare for a half marathon. Here are a runner's recent runs:"
        f"{recent_running_times}\n. Today is {datetime.today()}. Suggest a workout for them today. Be concise."
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "text"},
        max_completion_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    response = query_coach("5k in 25 minutes")
    print(response)
