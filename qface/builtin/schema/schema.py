#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from path import Path

from qface.generator import FileSystem, Generator
from qface.watch import monitor
from qface.filters import jsonify


here = Path(__file__).dirname()

logging.config.dictConfig(yaml.load(open(here / 'log.yaml')))

log = logging.getLogger(__file__)


def run(src, dst):
    log.debug('run {0} {1}'.format(src, dst))
    system = FileSystem.parse(src)
    search_path = [
        Path('_templates').abspath(),
        Path(here / 'templates').abspath()
    ]
    generator = Generator(search_path=search_path)
    generator.register_filter('jsonify', jsonify)
    ctx = {'dst': dst}
    for module in system.modules:
        ctx.update({
            'module': module,
        })
        generator.destination = generator.apply("{{dst}}", ctx)
        generator.write('{{module}}.json', 'module.json', ctx)


@click.command()
@click.option('--reload/--no-reload', default=False)
@click.argument('src', nargs=-1, type=click.Path(exists=True))
@click.argument('dst', nargs=1, type=click.Path(exists=True))
def app(src, dst, reload):
    """Takes several files or directories as src and generates the code
    in the given dst directory."""
    if reload:
        script = Path(__file__).abspath()
        monitor(script, src, dst)
    else:
        run(src, dst)


if __name__ == '__main__':
    app()
