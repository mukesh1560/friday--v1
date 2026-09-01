"""
reminder.py — Timer-based reminders for Friday
Uses background threads so Friday keeps running while waiting.
Reminders fire a console alert + optional voice announcement.
"""

import threading
import datetime

# Track all active reminders so we can list them
_active_reminders: list[dict] = []


def set_reminder(message: str, seconds) -> str:
    """Set a reminder that fires after `seconds` seconds."""
    try:
        seconds = int(seconds)
        if seconds <= 0:
            return "❌ Seconds must be a positive number."

        fire_at = datetime.datetime.now() + datetime.timedelta(seconds=seconds)

        def _fire():
            alert = f"\n{'='*45}\n⏰  REMINDER: {message}\n{'='*45}"
            print(alert)
            # Optional TTS
            try:
                import config, voice
                if config.TTS_ENABLED:
                    voice.speak(f"Reminder: {message}")
            except Exception:
                pass
            # Remove from active list
            _active_reminders[:] = [r for r in _active_reminders if r["message"] != message]

        t = threading.Timer(seconds, _fire)
        t.daemon = True
        t.start()

        _active_reminders.append({
            "message": message,
            "fire_at": fire_at.strftime("%H:%M:%S"),
            "timer": t,
        })

        # Human-readable time
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        parts = []
        if hours: parts.append(f"{hours}h")
        if mins:  parts.append(f"{mins}m")
        if secs:  parts.append(f"{secs}s")
        time_str = " ".join(parts) if parts else "0s"

        return f"⏰ Reminder set for {time_str} from now ({fire_at.strftime('%H:%M:%S')}): '{message}'"

    except ValueError:
        return "❌ Invalid time. Please say something like 'remind me in 30 seconds'."
    except Exception as e:
        return f"❌ Could not set reminder: {e}"


def list_reminders() -> str:
    """List all active (pending) reminders."""
    if not _active_reminders:
        return "⏰ No active reminders."
    lines = [f"  • [{r['fire_at']}] {r['message']}" for r in _active_reminders]
    return "⏰ Active reminders:\n" + "\n".join(lines)


def cancel_all() -> str:
    """Cancel all pending reminders."""
    for r in _active_reminders:
        r["timer"].cancel()
    count = len(_active_reminders)
    _active_reminders.clear()
    return f"⏰ Cancelled {count} reminder(s)."
