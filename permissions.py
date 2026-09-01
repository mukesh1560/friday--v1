# Intents that are always allowed (no confirmation needed)
ALLOWED_INTENTS = [
    "open_app",
    "read_file",
    "get_time",
    "get_date",
    "search_web",
    "recall_memory",
    "list_reminders",
    "get_mouse_pos",
    "move_mouse",
    "scroll_screen",
    "take_screenshot",
    "wait",
]

# Intents that require user confirmation before executing
CONFIRM_REQUIRED = [
    "run_command",
    "write_file",
    "delete_file",
    "send_email",
    "clear_memory",
    "set_reminder",
    "click_mouse",
    "double_click",
    "right_click",
    "type_text",
    "press_key",
    "hotkey",
    "find_and_click",
]

# Intents that are always blocked
DENIED_INTENTS = [
    "format_drive",
    "rm_rf",
    "shutdown",
    "delete_system",
]

# Dangerous substrings blocked in shell commands
DANGEROUS_PATTERNS = [
    "rm -rf",
    "del /f",
    "format c:",
    "shutdown",
    ":(){:|:&};:",
    "dd if=",
]


def is_allowed(intent: str) -> bool:
    return intent in ALLOWED_INTENTS

def needs_confirmation(intent: str) -> bool:
    return intent in CONFIRM_REQUIRED

def is_denied(intent: str) -> bool:
    return intent in DENIED_INTENTS

def is_command_safe(command: str) -> bool:
    cmd_lower = command.lower()
    for pattern in DANGEROUS_PATTERNS:
        if pattern in cmd_lower:
            return False
    return True
