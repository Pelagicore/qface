#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from path import Path

from qface.generator import FileSystem, Generator
from qface.helper.qtqml import Filters


here = Path(__file__).dirname()

logging.config.dictConfig(yaml.load(open(here / 'log.yaml')))

log = logging.getLogger(__file__)


def run(src, dst):
    log.debug('run {0} {1}'.format(src, dst))
    system = FileSystem.parse(src)
    generator = Generator(searchpath=here / 'templates')
    generator.register_filter('defaultValue', Filters.defaultValue)
    generator.register_filter('propertyType', Filters.propertyType)
    ctx = {'dst': dst}
    for module in system.modules:
        module_name = module.module_name
        module_path = '/'.join(module.name_parts)
        plugin_name = "".join(module.name_parts[:2])
        ctx.update({
            'module': module,
            'module_name': module_name,
            'module_path': module_path,
            'plugin_name': plugin_name,
        })
        generator.destination = generator.apply("{{dst}}/{{module_path}}", ctx)
        generator.write('private/{{module_name}}Module.js', 'module.js', ctx)
        generator.write('qmldir', 'public_qmldir', ctx)
        generator.write('private/qmldir', 'private_qmldir', ctx)

        for interface in module.interfaces:
            ctx.update({
                'interface': interface,
            })
            generator.write('private/Abstract{{interface}}.qml', 'AbstractInterface.qml', ctx)
            generator.write('{{interface}}.qml', 'Interface.qml', ctx, preserve=True)
            generator.write('private/{{interface}}Provider.qml', 'InterfaceProvider.qml', ctx)


@click.command()
@click.argument('src', nargs=-1, type=click.Path(exists=True))
@click.argument('dst', nargs=1, type=click.Path(exists=True))
def app(src, dst):
    """Takes several files or directories as src and generates the code
    in the given dst directory."""
    run(src, dst)


if __name__ == '__main__':
    app()
