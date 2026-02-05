import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi3:mini"   # fast + accurate on low RAM


def ask_ollama(question, context, chat_history):
    history = ""
    for chat in chat_history[-3:]:
        history += f"User: {chat['question']}\nAssistant: {chat['answer']}\n"

    prompt = f"""
You are a financial assistant having an ongoing conversation.
You can refer to known facts discussed earlier.
Do NOT invent numbers.

RULES:
- Use ONLY the provided data
- Do NOT invent numbers
- If information is missing, say so clearly

DATA:
{context}

PREVIOUS CONVERSATION:
{history}

QUESTION:
{question}
"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 200
        }
    }

    response = requests.post(
        OLLAMA_URL,
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        timeout=120
    )

    response.raise_for_status()
    return response.json()["response"]