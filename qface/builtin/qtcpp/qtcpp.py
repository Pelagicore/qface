#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from path import Path

from qface.generator import FileSystem, Generator
from qface.helper.qtcpp import Filters


here = Path(__file__).dirname()

logging.config.dictConfig(yaml.load(open(here / 'log.yaml')))

log = logging.getLogger(__file__)


def run(src, dst):
    log.debug('run {0} {1}'.format(src, dst))
    system = FileSystem.parse(src)
    generator = Generator(search_path=here / 'templates')
    generator.register_filter('returnType', Filters.returnType)
    generator.register_filter('parameterType', Filters.parameterType)
    generator.register_filter('defaultValue', Filters.defaultValue)
    ctx = {'dst': dst}
    for module in system.modules:
        log.debug('generate code for module %s', module)
        ctx.update({'module': module})
        dst = generator.apply('{{dst}}/{{module|lower|replace(".", "-")}}', ctx)
        generator.destination = dst
        generator.write('qmldir', 'qmldir', ctx, preserve=True)
        generator.write('plugin.cpp', 'plugin.cpp', ctx, preserve=True)
        generator.write('plugin.h', 'plugin.h', ctx, preserve=True)
        generator.write('{{module|lower|replace(".", "-")}}.pro', 'plugin.pro', ctx, preserve=True)
        generator.write('generated/generated.pri', 'generated.pri', ctx)
        generator.write('generated/qml{{module.module_name|lower}}module.h', 'module.h', ctx)
        generator.write('generated/qml{{module.module_name|lower}}module.cpp', 'module.cpp', ctx)
        for interface in module.interfaces:
            log.debug('generate code for interface %s', interface)
            ctx.update({'interface': interface})
            generator.write('qml{{interface|lower}}.h', 'interface.h', ctx, preserve=True)
            generator.write('qml{{interface|lower}}.cpp', 'interface.cpp', ctx, preserve=True)
            generator.write('generated/qmlabstract{{interface|lower}}.h', 'abstractinterface.h', ctx)
            generator.write('generated/qmlabstract{{interface|lower}}.cpp', 'abstractinterface.cpp', ctx)
        for struct in module.structs:
            log.debug('generate code for struct %s', struct)
            ctx.update({'struct': struct})
            generator.write('generated/qml{{struct|lower}}.h', 'struct.h', ctx)
            generator.write('generated/qml{{struct|lower}}.cpp', 'struct.cpp', ctx)
            generator.write('generated/qml{{struct|lower}}model.h', 'structmodel.h', ctx)
            generator.write('generated/qml{{struct|lower}}model.cpp', 'structmodel.cpp', ctx)
            generator.write('generated/qmlvariantmodel.h', 'variantmodel.h', ctx)
            generator.write('generated/qmlvariantmodel.cpp', 'variantmodel.cpp', ctx)


@click.command()
@click.argument('src', nargs=-1, type=click.Path(exists=True))
@click.argument('dst', nargs=1, type=click.Path(exists=True))
def app(src, dst):
    """Takes several files or directories as src and generates the code
    in the given dst directory."""
    run(src, dst)


if __name__ == '__main__':
    app()
