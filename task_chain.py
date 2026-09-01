"""
task_chain.py — Multi-step task execution for Friday

Detects chained commands like:
  "open chrome and then search for python tutorials"
  "get the time then open notepad"
  "read notes.txt, then send it to friend@email.com"

Splits them into individual tasks and runs each through the pipeline.
"""

import re

# Keywords that separate chained tasks
_SEPARATORS = [
    r"\band then\b",
    r"\bafter that\b",
    r"\bafterwards\b",
    r"\bthen\b",
    r"\band also\b",
    r"\balso\b",
    r"\bnext\b",
]

_PATTERN = re.compile("|".join(_SEPARATORS), flags=re.IGNORECASE)


def is_multi_task(user_input: str) -> bool:
    """Return True if input contains multiple chained tasks."""
    return len(split_tasks(user_input)) > 1


def split_tasks(user_input: str) -> list[str]:
    """Split a chained command into individual task strings."""
    parts = _PATTERN.split(user_input)
    return [p.strip() for p in parts if p.strip()]


def run_chain(user_input: str, analyze_fn, handle_fn) -> str:
    """
    Split the input into tasks, analyze + execute each one,
    and return a combined result string.

    Args:
        user_input  : the full chained user command
        analyze_fn  : model_router.analyze_intent
        handle_fn   : controller.handle_intent
    """
    tasks = split_tasks(user_input)
    results = []

    print(f"\n🔗 Multi-step task detected — {len(tasks)} steps")

    for i, task in enumerate(tasks, start=1):
        print(f"\n▶ Step {i}/{len(tasks)}: '{task}'")
        intent_data = analyze_fn(task)
        result = handle_fn(intent_data)
        results.append(f"Step {i} ({task[:30]}...):\n  {result}")
        print(f"  ↳ {result}")

    return "\n\n".join(results)
