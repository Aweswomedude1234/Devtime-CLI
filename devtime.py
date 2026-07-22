import time
from datetime import datetime

from config import load_config


def remind():
    print("Get up and move.")
    print("Take a break from the screen")
    print("=" * 30)

def start():
    config = load_config()
    break_interval = config["break_interval"] * 60
    print("DevTime Started.")
    print("Next reminder in ", config["break_interval"], " minutes.")
    while True:
        time.sleep(break_interval)
        remind()

if __name__ == "__main__":
    start()
    