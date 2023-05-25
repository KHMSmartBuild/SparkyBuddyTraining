import sys
import time
import json
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('responses.json'):
            with open(event.src_path, 'r') as json_file:
                data = json.load(json_file)

            new_file_name = 'training_data.json'
            with open(new_file_name, 'w') as training_file:
                json.dump(data, training_file)
            print(f'New training data file {new_file_name} has been created.')

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'

    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
