"""
prompt_memory.py
----------------
Saves every prompt version + score + output.
So we can track improvement across iterations and always return the best.
"""

import json
import os
from datetime import datetime

MEMORY_FILE = "prompt_history.json"


def _load() -> list:
    if not os.path.exists(MEMORY_FILE):
        return []
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def _save(history: list):
    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)


def save_iteration(task: str, prompt: str, output: str, evaluation: dict, iteration: int):
    history = _load()
    history.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "task": task[:100],
        "iteration": iteration,
        "prompt": prompt,
        "output": output,
        "score": evaluation.get("score", 0),
        "evaluation": evaluation,
    })
    _save(history)


def get_best_prompt(task: str) -> str | None:
    """Return the highest scoring prompt for a similar task."""
    history = _load()
    if not history:
        return None
    # Filter by task similarity (simple keyword match)
    relevant = [h for h in history if any(word in h["task"] for word in task.split()[:3])]
    if not relevant:
        return None
    best = max(relevant, key=lambda x: x.get("score", 0))
    return best["prompt"] if best["score"] >= 7 else None


def get_history() -> list:
    return _load()
