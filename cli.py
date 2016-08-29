#!/usr/bin/env python3
import click
from subprocess import call
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pathlib import Path
import time
import os
import yaml


os.environ['PYTHONPATH'] = os.getcwd()


def sh(cmd, all=False):
    click.echo('$ {0}'.format(cmd))
    return call(cmd, shell=True)


@click.group()
def cli():
    pass


@cli.command()
def antlr():
    sh('antlr4 -Dlanguage=Python3 -Werror -package qface.idl.parser -o qface/idl/parser -listener -visitor T.g4')


@cli.command()
def test():
    sh('python3 -m pytest -v -s -l --pdb')


@cli.command()
def test_ci():
    sh('python3 -m pytest -v -s -l')


class RunTestChangeHandler(FileSystemEventHandler):
    def __init__(self, clickContext):
        super(RunTestChangeHandler).__init__()
        self.clickContext = clickContext

    def on_any_event(self, event):
        if event.is_directory:
            return
        if Path(event.src_path).suffix == '.py':
            sh('python3 -m pytest -v -s -l')


@cli.command()
@click.pass_context
def test_monitor(ctx):
    sh('python3 -m pytest -v -s -l')
    while True:
        event_handler = RunTestChangeHandler(ctx)
        observer = Observer()
        observer.schedule(event_handler, './tests', recursive=False)
        observer.schedule(event_handler, './examples', recursive=False)
        observer.schedule(event_handler, './qface/idl', recursive=False)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()


class RunScriptChangeHandler(FileSystemEventHandler):
    def __init__(self, script):
        super(RunTestChangeHandler).__init__()
        self.script = script

    def on_modified(self, event):
        if event.src_path.endswith('.cache'):
            return
        if event.is_directory:
            return
        print(event)
        sh('python3 {0}'.format(self.script))


@cli.command()
@click.option('--script')
def generator_monitor(script):
    print('run script: ' + script)
    event_handler = RunScriptChangeHandler(script)
    observer = Observer()
    observer.schedule(event_handler, './templates', recursive=True)
    observer.schedule(event_handler, './examples', recursive=True)
    observer.schedule(event_handler, str(Path(script).parent), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@cli.command()
@click.option('--runner', type=click.File('r'))
@click.option('--generator', type=click.Path(exists=True))
@click.option('--input', type=click.Path(exists=True))
@click.option('--output', type=click.Path(exists=True))
def generate(runner, generator, input, output):
    if runner:
        config = yaml.load(runner)
        generator = config['generator']
        input = config['input']
        output = config['output']
    input = Path(input).absolute()
    output = Path(output).absolute()
    sh('python3 ./generator/{0}/{0}.py --input {1} --output {2}'.format(generator, input, output))

if __name__ == '__main__':
    cli()
