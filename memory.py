"""
memory.py — Persistent conversation memory for Friday
Stores all interactions in memory.json as timestamped entries.
Supports save, recall (search), recent history, and clear.
"""

import json
import os
import datetime

MEMORY_FILE = "memory.json"


def _load() -> list:
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def _save(data: list):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def remember(role: str, content: str):
    """Save a new memory entry (role = 'user' or 'friday')."""
    data = _load()
    data.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "role": role,
        "content": content,
    })
    _save(data)


def recall(query: str) -> str:
    """Search memory for entries matching the query."""
    data = _load()
    if not data:
        return "🧠 No memories stored yet."

    q = query.lower()
    matches = [m for m in data if q in m["content"].lower()]

    if not matches:
        return f"🧠 No memories found matching '{query}'."

    lines = []
    for m in matches[-5:]:   # last 5 matches
        ts = m["timestamp"][:16].replace("T", " ")
        lines.append(f"  [{ts}] {m['role'].upper()}: {m['content']}")

    return "🧠 Memory recall:\n" + "\n".join(lines)


def get_recent_context(n: int = 8) -> list:
    """Return the last N memory entries as a list (for feeding into AI context)."""
    return _load()[-n:]


def clear_memory() -> str:
    """Wipe all stored memories."""
    _save([])
    return "🧠 Memory cleared."


def summary() -> str:
    """Return a short summary of what's in memory."""
    data = _load()
    if not data:
        return "🧠 Memory is empty."
    return f"🧠 {len(data)} memories stored. Oldest: {data[0]['timestamp'][:10]}, Latest: {data[-1]['timestamp'][:10]}"
