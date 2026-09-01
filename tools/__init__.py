"""
tools/__init__.py — Friday Tools Package
Re-exports all tool functions so the rest of the codebase can still do:
    from tools import open_app, run_command, ...
"""

from tools.core        import open_app, run_command, read_file, write_file
from tools.web         import search_web
from tools.email       import send_email
from tools.desktop     import (
    move_mouse, click_mouse, double_click, right_click,
    scroll_screen, type_text, type_text_clipboard,
    press_key, hotkey, wait, take_screenshot,
    get_mouse_position, find_and_click,
)

__all__ = [
    # core
    "open_app", "run_command", "read_file", "write_file",
    # web
    "search_web",
    # email
    "send_email",
    # desktop
    "move_mouse", "click_mouse", "double_click", "right_click",
    "scroll_screen", "type_text", "type_text_clipboard",
    "press_key", "hotkey", "wait", "take_screenshot",
    "get_mouse_position", "find_and_click",
]
