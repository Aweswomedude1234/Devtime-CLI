import time

def wait(minutes):
    seconds = minutes * 60
    time.sleep(seconds)

def get_time():
    return time.time()