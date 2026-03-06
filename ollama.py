import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3:12b"


def ask_gemma(full_prompt):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": full_prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]