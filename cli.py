#!/usr/bin/env python3
# Copyright (c) Pelagicore AG 2016

import click
from subprocess import call
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from pathlib import Path
import time
import os
import yaml


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
    cwd = str(Path('qface/idl/parser').absolute())
    sh('antlr4 -Dlanguage=Python3 -Werror -package qface.idl.parser -o . -listener -visitor T.g4', cwd=cwd)


@cli.command()
@click.option('--debug/--nodebug')
def test(debug):
    """run the tests"""
    sh('python3 -m pytest -v -s -l {0}'.format('-pdb' if debug else ''))


@cli.command()
def test_ci():
    """run the tests for CI integration"""
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
    """run the tests and re-run on changes"""
    sh('python3 -m pytest -v -s -l')
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
    def __init__(self, script, cwd=None):
        super(RunTestChangeHandler).__init__()
        self.script = script
        self.cwd = cwd

    def on_modified(self, event):
        if event.src_path.endswith('.cache'):
            return
        if event.is_directory:
            return
        print(event)
        sh('python3 {0}'.format(self.script), cwd=self.cwd)


@cli.command()
@click.option('--runner', type=click.File('r'))
@click.option('--generator', type=click.Path(exists=True))
@click.option('--input', type=click.Path(exists=True))
@click.option('--output', type=click.Path(exists=True))
def generate_monitor(runner, generator, input, output):
    """run the named generator and monitor the input and generator folder"""
    if runner:
        config = yaml.load(runner)
        generator = config['generator']
        input = config['input']
        output = config['output']
    generator = Path(generator).absolute()
    input = Path(input).absolute()
    output = Path(output).absolute()
    script = generator / '{0}.py --input {1} --output {2}'.format(generator.name, input, output)
    event_handler = RunScriptChangeHandler(script, cwd=generator.as_posix())
    observer = Observer()
    observer.schedule(event_handler, generator.as_posix(), recursive=True)
    observer.schedule(event_handler, input.as_posix(), recursive=True)
    observer.schedule(event_handler, './qface', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@cli.command()
@click.option('--runner', type=click.File('r'))
@click.option('--reload/--no-reload', default=False)
@click.option('--generator', type=click.Path(exists=True))
@click.option('--input', type=click.Path(exists=True))
@click.option('--output', type=click.Path(exists=True))
def generate(runner, generator, input, output, reload):
    """run the named generator"""
    if runner:
        config = yaml.load(runner)
        generator = config['generator']
        input = config['input']
        output = config['output']
    generator = Path(generator).absolute()
    input = Path(input).absolute()
    output = Path(output).absolute()
    if not reload:
        _generate_once(generator, input, output)
    else:
        _generate_reload(generator, input, output)


def _generate_once(generator, input, output):
    script = '{0}.py'.format(generator.name)
    input = Path(input).absolute()
    output = Path(output).absolute()
    sh('python3 {0} --input {1} --output {2}'
        .format(script, input, output),
        cwd=generator.as_posix())


def _generate_reload(generator, input, output):
    """run the named generator and monitor the input and generator folder"""
    script = generator / '{0}.py --input {1} --output {2}'.format(generator.name, input, output)
    event_handler = RunScriptChangeHandler(script, cwd=generator.as_posix())
    observer = Observer()
    observer.schedule(event_handler, generator.as_posix(), recursive=True)
    observer.schedule(event_handler, input.as_posix(), recursive=True)
    observer.schedule(event_handler, './qface', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    cli()
