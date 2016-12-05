#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
from subprocess import call
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from path import Path
import time
import os
import sys
import yaml
import logging
import logging.config

# logging.config.dictConfig(yaml.load(open('log.yaml')))
logging.basicConfig()
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
        super(RunTestChangeHandler).__init__()
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
        super(RunTestChangeHandler).__init__()
        self.script = script

    def on_modified(self, event):
        if event.src_path.endswith('.cache'):
            return
        if event.is_directory:
            return
        self.run()

    def run(self):
        sh(self.script, cwd=Path.getcwd())


@cli.command()
@click.argument('input', nargs=-1, type=click.Path(exists=True))
@click.argument('output', nargs=1, type=click.Path(exists=True))
@click.option('--runner', type=click.File('r'), help="use the runner YAML file to configure the generation")
@click.option('--reload/--no-reload', default=False, help="if enabled auto-reload the generator on input changes")
@click.option('--generator', help="specifies the generator (either by name or path)", required=True)
@click.option('--clean/--no-clean', help="initially cleans the output directory")
def generate(input, output, runner, generator, reload, clean):
    """generate from the list of input files or directories the source code
    in the output folder using the given generator."""
    generator = Path(generator).expand().abspath()
    output = Path(output).expand().abspath()
    input = input if isinstance(input, (list, tuple)) else [input]
    """run the named generator"""
    if runner:
        config = yaml.load(runner)
        generator = config['generator']
        input = config['input']
        output = config['output']
    # look if generator points to an external generator
    if not generator.exists():
        click.echo('genertor does not exists: {0}'.format(generator))
        sys.exit(-1)
    if clean:
        output.rmtree_p()
    output.makedirs_p()
    if not reload:
        _generate_once(generator, input, output)
    else:
        _generate_reload(generator, input, output)


def _generate_once(generator, input, output):
    in_option = ' '.join(input)
    script = 'python3 {0} {1} {2}'.format(generator, in_option, output)
    sh(script, Path.getcwd())


def _generate_reload(generator, input, output):
    """run the named generator and monitor the input and generator folder"""
    in_option = ' '.join(input)
    script = 'python3 {0} {1} {2}'.format(generator, in_option, output)
    event_handler = RunScriptChangeHandler(script)
    event_handler.run()  # run always once
    observer = Observer()
    observer.schedule(event_handler, generator.dirname().abspath(), recursive=True)
    for entry in input:
        observer.schedule(event_handler, Path(entry).abspath(), recursive=True)
    observer.schedule(event_handler, './qface', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@click.option('--editable/--no-editable', default=False, help='install editable package')
@cli.command()
def install(editable):
    """install the script onto the system using pip3"""
    script_dir = str(Path(__file__).parent.abspath())
    print(script_dir)
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
    dist = Path('dist')
    dist.rmdir_p()
    sh('python3 setup.py bdist_wheel')
    sh('twine upload dist/*')


if __name__ == '__main__':
    cli()
