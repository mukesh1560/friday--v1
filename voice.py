"""
voice.py — Speech Input (STT) + Speech Output (TTS) for Friday

Install:
    pip install speechrecognition pyttsx3 pyaudio

If pyaudio fails on Windows:
    pip install pipwin
    pipwin install pyaudio
"""

import config

# ─────────────────────────────────────────────────
#  TTS — Text to Speech (pyttsx3, fully OFFLINE)
# ─────────────────────────────────────────────────
_engine = None

def _get_tts():
    global _engine
    if _engine is None:
        import pyttsx3
        _engine = pyttsx3.init()
        _engine.setProperty("rate", 170)      # speed (default ~200)
        _engine.setProperty("volume", 1.0)    # 0.0 to 1.0

        # Pick a better voice if available
        voices = _engine.getProperty("voices")
        for v in voices:
            if "zira" in v.name.lower() or "david" in v.name.lower():
                _engine.setProperty("voice", v.id)
                break
    return _engine


def speak(text: str):
    """Friday speaks the given text aloud."""
    if not config.TTS_ENABLED:
        return
    try:
        engine = _get_tts()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"[TTS Error]: {e}")


# ─────────────────────────────────────────────────
#  STT — Speech to Text (Google via microphone)
# ─────────────────────────────────────────────────
def listen(timeout: int = 6, phrase_limit: int = 15) -> str | None:
    """
    Listen from the microphone and return transcribed text.
    Returns None if nothing was heard or recognized.
    """
    if not config.STT_ENABLED:
        return None

    try:
        import speech_recognition as sr
        r = sr.Recognizer()
        r.energy_threshold = 300        # sensitivity (lower = more sensitive)
        r.dynamic_energy_threshold = True

        with sr.Microphone() as source:
            print("🎤 Listening...")
            r.adjust_for_ambient_noise(source, duration=0.4)
            audio = r.listen(source, timeout=timeout, phrase_time_limit=phrase_limit)

        print("🔄 Processing speech...")
        text = r.recognize_google(audio)
        print(f"🎤 You said: \"{text}\"")
        return text

    except Exception as e:
        name = type(e).__name__
        if "WaitTimeoutError" in name:
            return None   # silence — not an error
        elif "UnknownValueError" in name:
            print("🎤 Couldn't understand. Please speak clearly.")
        elif "RequestError" in name:
            print("🎤 Google STT unavailable. Check internet connection.")
        else:
            print(f"[STT Error]: {e}")
        return None
