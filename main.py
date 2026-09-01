"""
main.py — Friday AI Assistant (Ollama / phi3)

Run modes:
    python main.py              → text mode
    python main.py --voice      → voice mode (speak in, Friday speaks back)

Make sure Ollama is running first:
    ollama serve
"""

import sys

# ── Force UTF-8 output so emojis work on all Windows terminals ───────────────
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import requests
import model_router
from controller import handle_intent
from memory     import remember
from task_chain import is_multi_task, run_chain
import config

# ── Voice setup ──────────────────────────────────────────────
try:
    from voice import speak, listen
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


def _check_voice():
    if not VOICE_AVAILABLE:
        print("\n⚠️  Voice packages not installed. Run:")
        print("    pip install speechrecognition pyttsx3 pyaudio")
        print("    (if pyaudio fails: pip install pipwin && pipwin install pyaudio)\n")
    return VOICE_AVAILABLE


def _check_ollama():
    """Verify Ollama is running and phi3 model is available."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        r.raise_for_status()
        models = [m["name"] for m in r.json().get("models", [])]
        model = config.OLLAMA_MODEL

        # Check exact match or match without tag
        found = any(model in m for m in models)
        if not found:
            print(f"\n❌ Model '{model}' not found in Ollama.")
            print(f"   Available models: {models if models else '(none)'}")
            print(f"   Pull it with: ollama pull {model}\n")
            return False
        return True
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to Ollama!")
        print("   Start it with: ollama serve\n")
        return False
    except Exception as e:
        print(f"\n⚠️  Ollama check error: {e}")
        return False


# ── Core pipeline ────────────────────────────────────────────
def process(user_input: str) -> str:
    """Memory → chain detect → AI analyze → execute → return result."""
    remember("user", user_input)

    # Multi-task chain execution
    if is_multi_task(user_input):
        return run_chain(user_input, model_router.analyze_intent, handle_intent)

    # Single-task execution
    intent_data = model_router.analyze_intent(user_input)
    return handle_intent(intent_data)


# ── Input helpers ────────────────────────────────────────────
def get_text_input() -> str | None:
    try:
        return input("\n🗣️  You: ").strip() or None
    except EOFError:
        return None


def get_voice_input() -> str | None:
    return listen()


# ── Main loop ────────────────────────────────────────────────
def main():
    voice_mode = "--voice" in sys.argv

    print("=" * 52)
    print("   🤖  FRIDAY  —  AI Assistant  v3.0")
    print(f"   Brain : 🖥️  Ollama ({config.OLLAMA_MODEL})")
    print(f"   Input : {'🎤 VOICE' if voice_mode else '⌨️  TEXT'}")
    print(f"   Output: {'🔊 VOICE + TEXT' if voice_mode else '📄 TEXT'}")
    print("   ──────────────────────────────────────────────")
    print("   Commands: exit | voice on/off")
    print("=" * 52)
    print()

    # ── Pre-flight checks ──
    if not _check_ollama():
        print("   ⏳ Fix the above issue, then restart Friday.\n")
        return

    print("   ✅ Ollama connected! Friday is ready.\n")

    if voice_mode and not _check_voice():
        voice_mode = False

    if voice_mode:
        speak("Hello! I'm Friday, your AI assistant. I'm ready.")

    while True:
        try:
            # ── Get input ──────────────────────────────────
            if voice_mode:
                user_input = get_voice_input()
                if user_input is None:
                    continue
            else:
                user_input = get_text_input()
                if not user_input:
                    continue

            cmd = user_input.lower().strip()

            # ── Built-in control commands ───────────────────
            if cmd in ("exit", "quit", "bye", "goodbye", "stop"):
                msg = "Goodbye! Shutting down."
                print(f"\n👋 {msg}")
                if voice_mode and VOICE_AVAILABLE:
                    speak(msg)
                break

            if cmd in ("voice on", "enable voice", "voice mode on"):
                if _check_voice():
                    voice_mode = True
                    print("🎤 Voice mode ON")
                    speak("Voice mode enabled.")
                continue

            if cmd in ("voice off", "disable voice", "voice mode off", "text mode"):
                voice_mode = False
                print("⌨️  Text mode ON")
                continue

            # ── Main pipeline ───────────────────────────────
            response = process(user_input)
            print(f"\n🤖 Friday: {response}\n")

            if voice_mode and VOICE_AVAILABLE:
                speak(response)

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Shutting down.")
            if voice_mode and VOICE_AVAILABLE:
                speak("Shutting down.")
            break


if __name__ == "__main__":
    main()
