import json
from pathlib import Path
CONFIG_FILE = Path.home() / ".devtime.json"
HISTORY_FILE = Path.home() / ".devtime_history.json"

DEFAULT_CONFIG = {"default_strategy": "Balanced",
                  "default_session": 60}

def load_config():
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)

    with open(CONFIG_FILE, "r") as file:
        return json.load(file)
def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent = 4)
def save_session(session):
    history = load_history()
    history.append(session)
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent = 4)
def load_history():
    if not HISTORY_FILE.exists():
        return []
    with open(HISTORY_FILE, "r") as file: 
        return json.load(file)