#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from qface.generator import FileSystem, Generator
from qface.helper.qtcpp import Filters
import os
from path import Path

here = os.path.dirname(__file__)


def run_generation(input, output):
    system = FileSystem.parse(input)
    generator = Generator(searchpath=os.path.join(here, 'templates'))
    generator.register_filter('returnType', Filters.returnType)
    generator.register_filter('parameterType', Filters.parameterType)
    generator.register_filter('defaultValue', Filters.defaultValue)
    ctx = {'output': output}
    for module in system.modules:
        ctx.update({'module': module})
        dst = generator.apply('{{output}}/{{module|lower|replace(".", "-")}}', ctx)
        ctx.update({'dst': dst})
        generator.write('{{dst}}/qmldir', 'qmldir', ctx, preserve=True)
        generator.write('{{dst}}/plugin.cpp', 'plugin.cpp', ctx, preserve=True)
        generator.write('{{dst}}/plugin.h', 'plugin.h', ctx, preserve=True)
        generator.write('{{dst}}/{{module|lower|replace(".", "-")}}.pro', 'plugin.pro', ctx, preserve=True)
        generator.write('{{dst}}/generated/generated.pri', 'generated.pri', ctx)
        generator.write('{{dst}}/generated/qml{{module.module_name|lower}}module.h', 'module.h', ctx)
        generator.write('{{dst}}/generated/qml{{module.module_name|lower}}module.cpp', 'module.cpp', ctx)
        for interface in module.interfaces:
            ctx.update({'interface': interface})
            generator.write('{{dst}}/qml{{interface|lower}}.h', 'interface.h', ctx, preserve=True)
            generator.write('{{dst}}/qml{{interface|lower}}.cpp', 'interface.cpp', ctx, preserve=True)
            generator.write('{{dst}}/generated/qmlabstract{{interface|lower}}.h', 'abstractinterface.h', ctx)
            generator.write('{{dst}}/generated/qmlabstract{{interface|lower}}.cpp', 'abstractinterface.cpp', ctx)
        for struct in module.structs:
            ctx.update({'struct': struct})
            generator.write('{{dst}}/generated/qml{{struct|lower}}.h', 'struct.h', ctx)
            generator.write('{{dst}}/generated/qml{{struct|lower}}.cpp', 'struct.cpp', ctx)
            generator.write('{{dst}}/generated/qml{{struct|lower}}model.h', 'structmodel.h', ctx)
            generator.write('{{dst}}/generated/qml{{struct|lower}}model.cpp', 'structmodel.cpp', ctx)


@click.command()
@click.argument('input', nargs=-1, type=click.Path(exists=True))
@click.argument('output', nargs=1, type=click.Path(exists=True))
def generate(input, output):
    """Takes several files or directories as input and generates the code
    in the given output directory."""
    run_generation(input, output)


if __name__ == '__main__':
    generate()
