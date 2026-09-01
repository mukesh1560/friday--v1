"""
tools/core.py — App launching, shell commands, and file I/O for Friday
"""

import subprocess
import os
import sys

# ── Known website shortcuts ───────────────────────────────────────────────────
WEBSITE_MAP = {
    "youtube":       "https://www.youtube.com",
    "google":        "https://www.google.com",
    "gmail":         "https://mail.google.com",
    "github":        "https://www.github.com",
    "reddit":        "https://www.reddit.com",
    "twitter":       "https://www.twitter.com",
    "x":             "https://www.x.com",
    "facebook":      "https://www.facebook.com",
    "instagram":     "https://www.instagram.com",
    "whatsapp":      "https://web.whatsapp.com",
    "netflix":       "https://www.netflix.com",
    "spotify":       "https://open.spotify.com",
    "wikipedia":     "https://www.wikipedia.org",
    "stackoverflow": "https://www.stackoverflow.com",
    "chatgpt":       "https://chat.openai.com",
    "maps":          "https://maps.google.com",
}

# ── Known app name → Windows command mappings ─────────────────────────────────
APP_MAP = {
    "notepad":        "notepad",
    "calculator":     "calc",
    "calc":           "calc",
    "paint":          "mspaint",
    "file explorer":  "explorer",
    "explorer":       "explorer",
    "task manager":   "taskmgr",
    "control panel":  "control",
    "cmd":            "cmd",
    "command prompt": "cmd",
    "powershell":     "powershell",
    "word":           "winword",
    "excel":          "excel",
    "powerpoint":     "powerpnt",
    "chrome":         "chrome",
    "firefox":        "firefox",
    "edge":           "msedge",
    "brave":          "brave",
    "vlc":            "vlc",
    "vs code":        "code",
    "vscode":         "code",
    "discord":        "discord",
    "steam":          "steam",
    "spotify":        "spotify",
    "zoom":           "zoom",
    "slack":          "slack",
}


def open_app(app_name: str) -> str:
    """
    Opens an application or website by name.
    Understands natural language like 'youtube', 'notepad', 'chrome', etc.
    Also handles 'open <site> in <browser>' style inputs.
    """
    original  = app_name
    app_lower = app_name.lower().strip()

    # ── Parse "open X in chrome/firefox/edge" style ───────────────────────
    browser = None
    for b in ("chrome", "firefox", "edge", "brave", "msedge"):
        if f" in {b}" in app_lower:
            app_lower = app_lower.replace(f" in {b}", "").strip()
            browser = b
            break

    # Strip common prefixes like "open ", "launch ", "start "
    for prefix in ("open ", "launch ", "start "):
        if app_lower.startswith(prefix):
            app_lower = app_lower[len(prefix):]

    # ── Check if it's a website shortcut ─────────────────────────────────
    url = WEBSITE_MAP.get(app_lower)

    # Also check if it looks like a raw URL
    if not url and (
        app_lower.startswith("http://")
        or app_lower.startswith("https://")
        or app_lower.startswith("www.")
    ):
        url = app_lower if app_lower.startswith("http") else f"https://{app_lower}"

    if url:
        return _open_url(url, browser)

    # ── Check known app name aliases ──────────────────────────────────────
    cmd = APP_MAP.get(app_lower, app_lower)

    try:
        subprocess.Popen(cmd, shell=True)
        return f"✅ Opened '{original}' successfully."
    except Exception as e:
        return f"❌ Failed to open '{original}': {e}"


def _open_url(url: str, browser: str = None) -> str:
    """Opens a URL, optionally in a specific browser."""
    try:
        if browser:
            # Use 'start' command on Windows to find browser by name
            browser_cmd = APP_MAP.get(browser, browser)
            # Try 'start <browser> <url>' which works reliably on Windows
            subprocess.Popen(f'start {browser_cmd} "{url}"', shell=True)
            return f"✅ Opened {url} in {browser}."
        else:
            import webbrowser
            webbrowser.open(url)
            return f"✅ Opened {url} in your default browser."
    except Exception as e:
        return f"❌ Failed to open {url}: {e}"


def run_command(command: str) -> str:
    """Runs a shell command safely and returns output."""
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        output = result.stdout.strip() or result.stderr.strip()
        return f"✅ Command Output:\n{output}" if output else "✅ Command ran with no output."
    except subprocess.TimeoutExpired:
        return "❌ Command timed out after 15 seconds."
    except Exception as e:
        return f"❌ Command failed: {e}"


def read_file(path: str) -> str:
    """Reads and returns the content of a file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"❌ File not found: {path}"
    except Exception as e:
        return f"❌ Could not read file: {e}"


def write_file(path: str, content: str) -> str:
    """Writes content to a file."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"✅ File written: {path}"
    except Exception as e:
        return f"❌ Could not write file: {e}"
