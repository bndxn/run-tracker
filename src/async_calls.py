import openai
import asyncio
import time
from openai import AsyncOpenAI

prompts = [
    "Tell me about the height of different mice.",
    "Tell me about the height of different famous men.",
]

client = AsyncOpenAI()


async def fetch_openai_response(prompt):
    response = await client.chat.completions.create(
        model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}]
    )
    return response


async def main():
    start_time = time.time()
    tasks = [fetch_openai_response(prompt) for prompt in prompts]
    responses = await asyncio.gather(*tasks)
    print("Total time:", time.time() - start_time)
    return responses


responses = asyncio.run(main())
