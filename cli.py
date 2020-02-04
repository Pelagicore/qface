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


here = Path(__file__).abspath().dirname()

logging.config.dictConfig(yaml.load((here / 'log.yaml').open()))
logger = logging.getLogger(__name__)


os.environ['PYTHONPATH'] = Path.getcwd()


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
def test-ci():
    """run the tests for CI integration"""
    sh('python3 -m pytest --cov=qface -v -l tests/')


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
    sh('twine upload dist/*')
    Path('build').rmtree_p()


@cli.command()
def pack():
    Path('build').rmtree_p()
    Path('dist').rmtree_p()
    sh('python3 setup.py bdist_wheel')
    sh('unzip -l dist/*.whl')


@cli.command()
def docs_serve():
    server = Server()
    server.watch('docs/*.rst', shell('make html', cwd='docs'))
    server.serve(root='docs/_build/html', open_url=True)


@cli.command()
def clean():
    Path('build').rmtree_p()
    Path('dist').rmtree_p()
    Path('qface.egg-info').rmtree_p()


if __name__ == '__main__':
    cli()
