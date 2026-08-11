import time

def wait(minutes):
    seconds = minutes * 60

    while seconds > 0:
        minutes_left = seconds // 60
        seconds_left = seconds % 60
        print(f"\rTime remaining: {minutes_left:02d}:{seconds_left:02d}", end = "")
        time.sleep(1)
        seconds -= 1
    print("\rTime remaining: 00:00")

def wait_for_return():
    input("Press Enter once you return . . .")


