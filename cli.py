#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
from subprocess import call
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from path import Path
import time
import os
import yaml
import logging
import logging.config
from livereload import Server, shell


here = os.path.dirname(__file__)

logging.config.dictConfig(yaml.load(open(os.path.join(here, 'log.yaml'))))
logger = logging.getLogger(__name__)


os.environ['PYTHONPATH'] = os.getcwd()


def sh(cmd, all=False, **kwargs):
    click.echo('$ {0}'.format(cmd))
    return call(cmd, shell=True, **kwargs)


@click.group()
def cli():
    pass


@cli.command()
def antlr():
    """generate a new parser based on the grammar using antlr"""
    cwd = str(Path('qface/idl/parser').abspath())
    sh('antlr4 -Dlanguage=Python3 -Werror -package qface.idl.parser -o . -listener -visitor T.g4', cwd=cwd)


@cli.command()
@click.option('--debug/--nodebug')
def test(debug):
    """run the tests"""
    sh('python3 -m pytest -v -s -l {0}'.format('-pdb' if debug else ''))


@cli.command()
def test_ci():
    """run the tests for CI integration"""
    sh('python3 -m pytest --cov=qface -v -l tests/')


class RunTestChangeHandler(FileSystemEventHandler):
    def __init__(self, clickContext):
        super().__init__()
        self.clickContext = clickContext

    def on_any_event(self, event):
        if event.is_directory:
            return
        if Path(event.src_path).ext == '.py':
            sh('python3 -m pytest')


@cli.command()
@click.pass_context
def test_monitor(ctx):
    """run the tests and re-run on changes"""
    sh('python3 -m pytest')
    while True:
        event_handler = RunTestChangeHandler(ctx)
        observer = Observer()
        observer.schedule(event_handler, './tests', recursive=True)
        observer.schedule(event_handler, './qface', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class RunScriptChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        super().__init__()
        self.script = script
        self.is_running = False

    def on_modified(self, event):
        if event.src_path.endswith('.cache'):
            return
        self.run()

    def run(self):
        if self.is_running:
            return
        self.is_running = True
        sh(self.script, cwd=Path.getcwd())
        self.is_running = False


@cli.command()
@click.argument('script', nargs=1, type=click.Path(exists=True))
@click.argument('input', nargs=-1, type=click.Path(exists=True))
@click.argument('output', nargs=1, type=click.Path(exists=True))
def reload(script, input, output):
    """
    reloads the generator script when the script files
    or the input files changes
    """
    script = Path(script).expand().abspath()
    output = Path(output).expand().abspath()
    input = input if isinstance(input, (list, tuple)) else [input]
    output.makedirs_p()
    _script_reload(script, input, output)


def _script_reload(script, input, output):
    """run the named generator and monitor the input and generator folder"""
    input = [Path(entry).expand().abspath() for entry in input]
    output = Path(output).expand().abspath()
    cmd = 'python3 {0} {1} {2}'.format(script, ' '.join(input), output)
    event_handler = RunScriptChangeHandler(cmd)
    event_handler.run()  # run always once
    observer = Observer()
    path = script.dirname().expand().abspath()
    click.secho('watch: {0}'.format(path), fg='blue')
    observer.schedule(event_handler, path, recursive=True)
    for entry in input:
        entry = entry.dirname().expand().abspath()
        click.secho('watch: {0}'.format(entry), fg='blue')
        observer.schedule(event_handler, entry, recursive=True)
    path = Path(__file__).parent / 'qface'
    click.secho('watch: {0}'.format(path), fg='blue')
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@click.option('--editable/--no-editable', default=False, help='install editable package')
@cli.command()
def install(editable):
    """install the script onto the system using pip3"""
    script_dir = str(Path(__file__).parent.abspath())
    click.secho(script_dir, fg='blue')
    if editable:
        sh('pip3 install --editable {0} --upgrade'.format(script_dir))
    else:
        sh('pip3 install {0} --upgrade'.format(script_dir))


@cli.command()
def uninstall():
    """uninstall the script from the system using pip3"""
    sh('pip3 uninstall qface')


@cli.command()
def upload():
    Path('build').rmtree_p()
    dist = Path('dist')
    dist.rmtree_p()
    dist.makedirs_p()
    sh('python3 setup.py bdist_wheel')
    sh('twine upload dist/*')
    Path('build').rmtree_p()


@cli.command()
def docs_serve():
    server = Server()
    server.watch('docs/*.rst', shell('make html', cwd='docs'))
    server.serve(root='docs/_build/html', open_url=True)


if __name__ == '__main__':
    cli()
