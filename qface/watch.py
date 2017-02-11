from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import click
from path import Path
import time
from .shell import sh


class RunScriptChangeHandler(FileSystemEventHandler):
    def __init__(self, argv):
        super().__init__()
        self.argv = argv
        self.is_running = False

    def on_modified(self, event):
        self.run()

    def run(self):
        if self.is_running:
            return
        self.is_running = True
        # cmd = '{0} {1}'.format(sys.executable, ' '.join(self.argv))
        sh(' '.join(self.argv), cwd=Path.getcwd())
        self.is_running = False


def monitor(src, argv):
    """
    reloads the script when src files changes
    """
    script = Path(argv[0]).expand().abspath()
    src = src if isinstance(src, (list, tuple)) else [src]
    src = [Path(entry).expand().abspath() for entry in src]
    event_handler = RunScriptChangeHandler(argv)
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
