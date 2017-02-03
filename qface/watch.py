from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import click
from subprocess import call
from path import Path
import time


def sh(cmd, all=False, **kwargs):
    click.secho('$ {0}'.format(cmd), fg='green')
    return call(cmd, shell=True, **kwargs)


class RunScriptChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        super().__init__()
        self.script = script
        self.is_running = False

    def on_modified(self, event):
        self.run()

    def run(self):
        if self.is_running:
            return
        self.is_running = True
        sh(self.script, cwd=Path.getcwd())
        self.is_running = False


def monitor(src, script):
    """
    reloads the script when src files changes
    """
    script = Path(script).expand().abspath()
    src = src if isinstance(src, (list, tuple)) else [src]
    src = [Path(entry).expand().abspath() for entry in src]
    event_handler = RunScriptChangeHandler(script)
    observer = Observer()
    path = script.dirname().expand().abspath()
    click.secho('watch recursive: {0}'.format(path), fg='blue')
    observer.schedule(event_handler, path, recursive=True)
    for entry in src:
        entry = entry.dirname().expand().abspath()
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
