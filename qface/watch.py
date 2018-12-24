from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import click
from path import Path
import time
from subprocess import call

"""
Provides an API to monitor the file system
"""


class RunScriptChangeHandler(FileSystemEventHandler):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.is_running = False

    def on_modified(self, event):
        if event.is_directory:
            return
        self.run()

    def run(self):
        if self.is_running:
            return
        self.is_running = True
        call(self.args, cwd=Path.getcwd())
        self.is_running = False


def monitor(args, watch):
    """
    reloads the script given by argv when src files changes
    """
    watch = watch if isinstance(watch, (list, tuple)) else [watch]
    watch = [Path(entry).expand().abspath() for entry in watch]
    event_handler = RunScriptChangeHandler(args)
    observer = Observer()
    for entry in watch:
        if entry.isfile():
            entry = entry.parent
        click.secho('watch recursive: {0}'.format(entry), fg='blue')
        observer.schedule(event_handler, entry, recursive=True)
    event_handler.run()  # run always once
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
