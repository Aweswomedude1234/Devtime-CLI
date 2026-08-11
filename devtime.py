from config import load_config
from notifier import remind
from timer import wait, get_time

def start():
    config = load_config()
    break_interval = config["break_interval"]
    start_time = get_time()
    print("DevTime Started.")
    print(f"Next reminder in {break_interval} minutes.")
    while True:
        current_time = get_time()
        elapsed = current_time - start_time
        minutes = int(elapsed // 60)
        print(f"\rCoding session: {minutes} minutes", end = "")
        wait(1)
        if minutes >= break_interval:
            remind(break_interval)
            start_time = get_time()

if __name__ == "__main__":
    start()