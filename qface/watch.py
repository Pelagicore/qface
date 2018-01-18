from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import click
from path import Path
import time
from .shell import sh

"""
Provides an API to monitor the file system
"""

class RunScriptChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        super().__init__()
        self.script = script
        self.is_running = False

    def on_modified(self, event):
        if event.is_directory:
            return
        self.run()

    def run(self):
        if self.is_running:
            return
        self.is_running = True
        sh(str(self.script), cwd=Path.getcwd())
        self.is_running = False


def monitor(script, src, dst, args):
    """
    reloads the script given by argv when src files changes
    """
    src = src if isinstance(src, (list, tuple)) else [src]
    dst = Path(dst).expand().abspath()
    src = [Path(entry).expand().abspath() for entry in src]
    command = ' '.join(args)
    print('command: ', command)
    event_handler = RunScriptChangeHandler(command)
    observer = Observer()
    click.secho('watch recursive: {0}'.format(script.dirname()), fg='blue')
    observer.schedule(event_handler, script.dirname(), recursive=True)
    for entry in src:
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
