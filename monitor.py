import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directory to watch
DIRECTORY_TO_WATCH = "C:/Users/moham/bsm/test"
LOG_FILE = r"C:\Users\moham\bsm\logs\changes.json"

class Watcher:
    def __init__(self):
        self.observer = Observer()

    def run(self):
        print(f"Watching directory: {DIRECTORY_TO_WATCH}")  # Debugging line
        event_handler = Handler()
        self.observer.schedule(event_handler, DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event("modified", event)

    def on_created(self, event):
        self.log_event("created", event)

    def on_deleted(self, event):
        self.log_event("deleted", event)

    def log_event(self, event_type, event):
        print(f"Event Detected: {event_type} on {event.src_path}")  # Debugging line
        data = {
            "event": event_type,
            "path": event.src_path,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            with open(LOG_FILE, "a") as log_file:
                log_file.write(json.dumps(data) + "\n")
        except Exception as e:
            print(f"Failed to write to log: {e}")

if __name__ == "__main__":
    watcher = Watcher()
    watcher.run()
