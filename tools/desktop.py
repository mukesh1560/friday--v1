"""
tools/desktop.py — Mouse & Keyboard control for Friday
Uses pyautogui to control anything on screen.

Install:
    pip install pyautogui pillow

FAILSAFE: Move your mouse to the TOP-LEFT corner of the screen
          to immediately abort any running action.
"""

import time
import pyautogui

# Safety settings
pyautogui.FAILSAFE = True   # top-left corner = emergency stop
pyautogui.PAUSE    = 0.4    # pause between every pyautogui call


# ── Mouse ────────────────────────────────────────────────────

def move_mouse(x, y) -> str:
    pyautogui.moveTo(int(x), int(y), duration=0.4)
    return f"🖱️ Mouse moved to ({x}, {y})"


def click_mouse(x=None, y=None, button="left") -> str:
    if x is not None and y is not None:
        pyautogui.click(int(x), int(y), button=button)
        return f"🖱️ {button.capitalize()} clicked at ({x}, {y})"
    pyautogui.click(button=button)
    return f"🖱️ {button.capitalize()} clicked at current position"


def double_click(x=None, y=None) -> str:
    if x is not None and y is not None:
        pyautogui.doubleClick(int(x), int(y))
        return f"🖱️ Double-clicked at ({x}, {y})"
    pyautogui.doubleClick()
    return "🖱️ Double-clicked at current position"


def right_click(x=None, y=None) -> str:
    if x is not None and y is not None:
        pyautogui.rightClick(int(x), int(y))
        return f"🖱️ Right-clicked at ({x}, {y})"
    pyautogui.rightClick()
    return "🖱️ Right-clicked at current position"


def scroll_screen(direction="down", amount=3) -> str:
    clicks = -int(amount) if direction == "down" else int(amount)
    pyautogui.scroll(clicks)
    return f"🖱️ Scrolled {direction} by {amount}"


def get_mouse_position() -> str:
    x, y = pyautogui.position()
    return f"🖱️ Mouse is at ({x}, {y})"


# ── Keyboard ─────────────────────────────────────────────────

def type_text(text: str, delay: float = 0.05) -> str:
    """Type text character by character (supports all characters)."""
    pyautogui.write(str(text), interval=delay)
    return f"⌨️ Typed: '{text}'"


def type_text_clipboard(text: str) -> str:
    """
    Paste text via clipboard (faster, supports Unicode/emojis).
    Use this for non-English text or long messages.
    """
    import subprocess
    process = subprocess.Popen(["clip"], stdin=subprocess.PIPE, shell=True)
    process.communicate(text.encode("utf-16le"))
    time.sleep(0.2)
    pyautogui.hotkey("ctrl", "v")
    return f"⌨️ Pasted: '{text}'"


def press_key(key: str) -> str:
    pyautogui.press(key)
    return f"⌨️ Pressed: '{key}'"


def hotkey(keys: str) -> str:
    """
    Press a key combination.
    Pass keys as a '+' separated string: e.g. 'ctrl+c', 'alt+tab', 'ctrl+shift+t'
    """
    parts = [k.strip() for k in keys.split("+")]
    pyautogui.hotkey(*parts)
    return f"⌨️ Hotkey: {keys}"


def wait(seconds) -> str:
    time.sleep(float(seconds))
    return f"⏳ Waited {seconds} second(s)"


# ── Screen ───────────────────────────────────────────────────

def take_screenshot(save_path: str = "screenshot.png") -> str:
    img = pyautogui.screenshot()
    img.save(save_path)
    return f"📸 Screenshot saved → {save_path}"


def find_and_click(image_path: str, confidence: float = 0.8) -> str:
    """
    Find an image on screen and click it.
    Useful for clicking buttons by appearance.
    Requires: pip install opencv-python
    """
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if location:
            pyautogui.click(location)
            return f"🖱️ Found and clicked image: {image_path}"
        return f"❌ Image not found on screen: {image_path}"
    except Exception as e:
        return f"❌ find_and_click failed: {e}"
