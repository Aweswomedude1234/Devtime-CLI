import time

def wait(minutes, stop_event):
    seconds = minutes * 60

    while seconds > 0:
        if stop_event.is_set():
            return False
        time.sleep(1)
        seconds -= 1
    return True

def wait_for_return(stop_event):
        while not stop_event.is_set():
             try:
                input("\nPress Enter when you are back . . .")
                return True
             except KeyboardInterrupt:
                  return False
        return False