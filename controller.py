import datetime
from permissions import is_allowed, needs_confirmation, is_denied, is_command_safe
from tools import (
    # core
    open_app, run_command, read_file, write_file,
    # web
    search_web,
    # email
    send_email,
    # desktop
    move_mouse, click_mouse, double_click, right_click,
    scroll_screen, type_text, type_text_clipboard,
    press_key, hotkey, wait, take_screenshot,
    get_mouse_position, find_and_click,
)
from reminder import set_reminder, list_reminders
from memory   import recall, clear_memory, remember
from logger   import log_event

DRY_RUN = False


def handle_intent(intent_data: dict, dry_run: bool = DRY_RUN) -> str:
    intent = intent_data.get("intent", "unknown")
    args   = intent_data.get("args", {})

    if intent == "error":
        return f"⚠️  System Error: {args.get('message', 'Unknown error')}"

    if is_denied(intent):
        log_event({"action": "BLOCKED", "intent": intent, "args": args})
        return f"🚫 Blocked: '{intent}' is not permitted."

    if needs_confirmation(intent):
        confirm = input(
            f"⚠️  Friday wants to run '{intent}' with args {args}.\n   Allow? (y/n): "
        ).strip().lower()
        if confirm != "y":
            log_event({"action": "DENIED_BY_USER", "intent": intent, "args": args})
            return "❌ Action cancelled by user."

    if dry_run:
        log_event({"action": "DRY_RUN", "intent": intent, "args": args})
        return f"[DRY RUN] Would execute: {intent} with {args}"

    result = _execute(intent, args)
    log_event({"action": "EXECUTED", "intent": intent, "args": args, "result": result})
    remember("friday", result[:200])
    return result


def _execute(intent: str, args: dict) -> str:

    # ── App & Shell ──────────────────────────────────────────
    if intent == "open_app":
        app = args.get("app", "")
        return open_app(app) if app else "❌ No app specified."

    elif intent == "run_command":
        cmd = args.get("command", "")
        if not cmd:
            return "❌ No command provided."
        if not is_command_safe(cmd):
            log_event({"action": "BLOCKED_DANGEROUS_CMD", "command": cmd})
            return f"🚫 Dangerous command blocked: '{cmd}'"
        return run_command(cmd)

    # ── File Operations ──────────────────────────────────────
    elif intent == "read_file":
        path = args.get("path", "")
        return read_file(path) if path else "❌ No file path provided."

    elif intent == "write_file":
        path    = args.get("path", "")
        content = args.get("content", "")
        return write_file(path, content) if path else "❌ No file path provided."

    # ── Time & Date ──────────────────────────────────────────
    elif intent == "get_time":
        return f"🕐 Current time: {datetime.datetime.now().strftime('%H:%M:%S')}"

    elif intent == "get_date":
        return f"📅 Today's date: {datetime.datetime.now().strftime('%A, %d %B %Y')}"

    # ── Web Search ───────────────────────────────────────────
    elif intent == "search_web":
        query = args.get("query", "")
        return search_web(query) if query else "❌ No search query provided."

    # ── Email ────────────────────────────────────────────────
    elif intent == "send_email":
        return send_email(
            to      = args.get("to", ""),
            subject = args.get("subject", ""),
            body    = args.get("body", ""),
        )

    # ── Reminders ────────────────────────────────────────────
    elif intent == "set_reminder":
        return set_reminder(
            message = args.get("message", "Reminder!"),
            seconds = args.get("seconds", 60),
        )

    elif intent == "list_reminders":
        return list_reminders()

    # ── Memory ───────────────────────────────────────────────
    elif intent == "recall_memory":
        query = args.get("query", "")
        return recall(query) if query else "❌ No query provided."

    elif intent == "clear_memory":
        return clear_memory()

    # ── Mouse ────────────────────────────────────────────────
    elif intent == "move_mouse":
        return move_mouse(args.get("x", 0), args.get("y", 0))

    elif intent == "click_mouse":
        return click_mouse(
            x      = args.get("x"),
            y      = args.get("y"),
            button = args.get("button", "left"),
        )

    elif intent == "double_click":
        return double_click(args.get("x"), args.get("y"))

    elif intent == "right_click":
        return right_click(args.get("x"), args.get("y"))

    elif intent == "scroll_screen":
        return scroll_screen(
            direction = args.get("direction", "down"),
            amount    = args.get("amount", 3),
        )

    elif intent == "get_mouse_pos":
        return get_mouse_position()

    elif intent == "find_and_click":
        return find_and_click(
            image_path = args.get("image_path", ""),
            confidence = float(args.get("confidence", 0.8)),
        )

    # ── Keyboard ─────────────────────────────────────────────
    elif intent == "type_text":
        text = args.get("text", "")
        if not text:
            return "❌ No text to type."
        # Use clipboard paste for unicode/emoji support
        use_clipboard = args.get("clipboard", False)
        return type_text_clipboard(text) if use_clipboard else type_text(text)

    elif intent == "press_key":
        key = args.get("key", "")
        return press_key(key) if key else "❌ No key specified."

    elif intent == "hotkey":
        keys = args.get("keys", "")
        return hotkey(keys) if keys else "❌ No keys specified."

    # ── Utility ──────────────────────────────────────────────
    elif intent == "wait":
        return wait(args.get("seconds", 1))

    elif intent == "take_screenshot":
        return take_screenshot(args.get("path", "screenshot.png"))

    # ── Chat & Unknown ──────────────────────────────────────────────
    elif intent == "chat":
        return args.get("response", "Hello! How can I help you today?")

    elif intent == "unknown":
        return "🤔 I didn't understand that. Please try rephrasing."

    else:
        return f"❓ Unknown intent: '{intent}'"
