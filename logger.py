import json
import datetime

LOG_FILE = "friday.log"

def log_event(event_data: dict):
    """Logs interactions to a local JSON-lines file."""
    try:
        timestamp = datetime.datetime.now().isoformat()
        entry = {"timestamp": timestamp, **event_data}
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[Logger Error]: {e}")
