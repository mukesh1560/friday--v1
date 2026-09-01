"""
ollama_client.py — Ollama intent parser for Friday (phi3)
Sends user input to the local Ollama server and parses the JSON response.
"""

import requests
import json
import re
import config

MODEL_NAME = config.OLLAMA_MODEL
OPTIONS    = getattr(config, "OLLAMA_OPTIONS", {})
SYSTEM_PROMPT = config.INTENT_SYSTEM_PROMPT


def _extract_json(raw: str) -> dict:
    """
    Robustly extract a JSON object from model output.
    Handles markdown fences, extra text before/after JSON, etc.
    """
    # Strip markdown code fences
    raw = raw.strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)
    raw = raw.strip()

    # Try direct parse first
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object within the text using regex
    match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', raw)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    # Last resort: look for {"intent" pattern
    match = re.search(r'\{"intent".*?\}[\s]*\}', raw, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    return {"intent": "unknown", "args": {}}


def analyze_intent(user_input: str) -> dict:
    """Sends user input to Ollama and returns structured intent."""
    payload = {
        "model":   MODEL_NAME,
        "prompt":  f"{SYSTEM_PROMPT}\n\nUser: {user_input}\n\nJSON:",
        "stream":  False,
        "options": OPTIONS,
    }
    try:
        print(f"🖥️  Sending to Ollama ({MODEL_NAME})...")
        response = requests.post(config.OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        raw = response.json().get("response", "").strip()
        print(f"📝 Raw model output: {raw[:200]}")
        return _extract_json(raw)
    except requests.exceptions.ConnectionError:
        return {"intent": "error", "args": {"message": "Ollama is not running. Start it with: ollama serve"}}
    except Exception as e:
        return {"intent": "error", "args": {"message": str(e)}}
