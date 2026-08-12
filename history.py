import json
from pathlib import Path

HISTORY_FILE = Path.home() / ".devtime_history.json"

def load_history():
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)

def save_session(data):
    history = load_history()
    history.append(data)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent = 4)
    