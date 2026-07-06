import os
from datetime import datetime

LOG_FOLDER = "logs"
EVENT_FILE = os.path.join(LOG_FOLDER, "events.log")

os.makedirs(LOG_FOLDER, exist_ok=True)

def log_event(event_type, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    line = f"{timestamp} | {event_type} | {message}\n"

    with open(EVENT_FILE, "a", encoding="utf-8") as file:
        file.write(line)