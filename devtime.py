import time
from datetime import datetime

BREAK_INTERVAL = 45 * 60


def remind():
    print("Get up and move.")
    print("Take a break from the screen")
    print("=" * 30)

def start():
    print("DevTime Started.")
    print("Next reminder in " + BREAK_INTERVAL // 60 + " minutes.")
    while True:
        time.sleep(BREAK_INTERVAL)
        remind()

if __name__ == "__main__":
    start()
    