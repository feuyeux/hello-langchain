import os
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

completion = client.chat.completions.create(
    model="gpt-oss:20b",
    messages=[
        {
            "role": "user",
            "content": "你好"
        }
    ]
)

print(completion.choices[0].message)    