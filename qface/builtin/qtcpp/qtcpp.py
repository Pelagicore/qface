#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from path import Path

from qface.generator import FileSystem, Generator
from qface.helper.qtcpp import Filters
from qface.helper.doc import parse_doc
from qface.watch import monitor


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
    generator.register_filter('parameters', Filters.parameters)
    generator.register_filter('parse_doc', parse_doc)
    ctx = {'dst': dst}
    for module in system.modules:
        log.debug('generate code for module %s', module)
        ctx.update({'module': module})
        dst = generator.apply('{{dst}}/{{module|lower|replace(".", "-")}}', ctx)
        generator.destination = dst
        generator.write('.qmake.conf', 'qmake.conf', ctx)
        generator.write('{{module|lower|replace(".", "-")}}.pro', 'plugin.pro', ctx, preserve=True)
        generator.write('CMakeLists.txt', 'CMakeLists.txt', ctx)
        generator.write('plugin.cpp', 'plugin.cpp', ctx, preserve=True)
        generator.write('plugin.h', 'plugin.h', ctx, preserve=True)
        generator.write('qmldir', 'qmldir', ctx, preserve=True)
        generator.write('generated/generated.pri', 'generated/generated.pri', ctx)
        generator.write('generated/qml{{module.module_name|lower}}module.h', 'generated/module.h', ctx)
        generator.write('generated/qml{{module.module_name|lower}}module.cpp', 'generated/module.cpp', ctx)
        generator.write('generated/qmlvariantmodel.h', 'generated/variantmodel.h', ctx)
        generator.write('generated/qmlvariantmodel.cpp', 'generated/variantmodel.cpp', ctx)
        generator.write('docs/plugin.qdocconf', 'docs/plugin.qdocconf', ctx)
        generator.write('docs/plugin-project.qdocconf', 'docs/plugin-project.qdocconf', ctx)
        generator.write('docs/docs.pri', 'docs/docs.pri', ctx)
        for interface in module.interfaces:
            log.debug('generate code for interface %s', interface)
            ctx.update({'interface': interface})
            generator.write('qml{{interface|lower}}.h', 'interface.h', ctx, preserve=True)
            generator.write('qml{{interface|lower}}.cpp', 'interface.cpp', ctx, preserve=True)
            generator.write('generated/qmlabstract{{interface|lower}}.h', 'generated/abstractinterface.h', ctx)
            generator.write('generated/qmlabstract{{interface|lower}}.cpp', 'generated/abstractinterface.cpp', ctx)
        for struct in module.structs:
            log.debug('generate code for struct %s', struct)
            ctx.update({'struct': struct})
            generator.write('generated/qml{{struct|lower}}.h', 'generated/struct.h', ctx)
            generator.write('generated/qml{{struct|lower}}.cpp', 'generated/struct.cpp', ctx)
            generator.write('generated/qml{{struct|lower}}model.h', 'generated/structmodel.h', ctx)
            generator.write('generated/qml{{struct|lower}}model.cpp', 'generated/structmodel.cpp', ctx)


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
