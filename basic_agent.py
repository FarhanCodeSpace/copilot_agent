from dotenv import load_dotenv
import os
import requests

load_dotenv()


def get_genai_response(dev_prompt, user_prompt):
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "moonshotai/kimi-k3")

    messages = [
        {
            "role": "developer",
            "content": dev_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": model,
            "messages": messages,
            "max_tokens": 256
        }
    )

    data = response.json()

    if "error" in data:
        return "Error: " + data["error"]["message"]

    return data["choices"][0]["message"]["content"]
