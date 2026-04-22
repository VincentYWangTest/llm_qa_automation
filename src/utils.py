import time
import datetime
import os

LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, f"test_log_{datetime.date.today()}.log")

def log(message, level="INFO"):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")

class Timer:
    def __init__(self, task_name):
        self.task_name = task_name
    def __enter__(self):
        self.start = time.time()
        log(f"Task started: {self.task_name}")
        return self
    def __exit__(self, *args):
        cost = time.time() - self.start
        log(f"Task finished: {self.task_name} | Time: {cost:.2f}s")