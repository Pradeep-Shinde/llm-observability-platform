import os
from openai import OpenAI

LITELLM_URL = os.getenv("LITELLM_URL", "http://localhost:4000/v1")

client = OpenAI(
    api_key="dummy",
    base_url=LITELLM_URL,
    timeout=90.0
)


def ask_llm(prompt):

    response = client.chat.completions.create(
        model="llama3",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content