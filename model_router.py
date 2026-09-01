"""
model_router.py — Friday brain (Ollama / local only)
All intent analysis runs through the local Ollama model.
No internet or API key required.
"""

from ollama_client import analyze_intent as _analyze


def analyze_intent(user_input: str) -> dict:
    """Send user input to Ollama and return a structured intent dict."""
    return _analyze(user_input)
