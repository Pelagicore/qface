#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from qface.generator import FileSystem, Generator
import os
from path import Path

here = os.path.dirname(__file__)

def paramterType(symbol):
    module_name = symbol.module.module_name
    if symbol.type.is_enum:
        return 'Qml{0}Module::{1} {2}'.format(module_name, symbol.type, symbol)
    if symbol.type.is_void or symbol.type.is_primitive:
        if symbol.type.name == 'string':
            return 'const QString &{0}'.format(symbol)
        if symbol.type.name == 'var':
            return 'const QVariant &{0}'.format(symbol)
        if symbol.type.name == 'real':
            return 'float {0}'.format(symbol)
        return '{0} {1}'.format(symbol.type, symbol)
    elif symbol.type.is_list:
        return 'const QList<{0}> &{1}'.format(symbol.type.nested, symbol)
    elif symbol.type.is_model:
        return '{0}Model *{1}'.format(symbol.type.nested, symbol)
    else:
        return 'const Qml{0} &{1}'.format(symbol.type, symbol)


def returnType(symbol):
    module_name = symbol.module.module_name
    if symbol.type.is_enum:
        return 'Qml{0}Module::{1}'.format(module_name, symbol.type)
    if symbol.type.is_void or symbol.type.is_primitive:
        if symbol.type.name == 'string':
            return 'QString'
        if symbol.type.name == 'var':
            return 'QVariant'
        if symbol.type.name == 'real':
            return 'float'
        return symbol.type
    elif symbol.type.is_list:
        return 'QList<{0}>'.format(symbol.type.nested)
    elif symbol.type.is_model:
        return '{0}Model*'.format(symbol.type.nested)
    else:
        return 'Qml{0}'.format(symbol.type)


def run_generation(input, output):
    system = FileSystem.parse(input)
    generator = Generator(searchpath=os.path.join(here, 'templates'))
    generator.register_filter('returnType', returnType)
    generator.register_filter('parameterType', paramterType)
    ctx = {'output': output}
    for module in system.modules:
        ctx.update({'module': module})
        dst = generator.apply('{{output}}/{{module|lower}}', ctx)
        ctx.update({'dst': dst})
        generator.write('{{dst}}/qmldir', 'qmldir', ctx, overwrite=False)
        generator.write('{{dst}}/plugin.cpp', 'plugin.cpp', ctx, overwrite=False)
        generator.write('{{dst}}/plugin.h', 'plugin.h', ctx, overwrite=False)
        generator.write('{{dst}}/{{module|lower}}.pro', 'plugin.pro', ctx, overwrite=False)
        generator.write('{{dst}}/_generated/{{module|lower}}.pri', 'plugin.pri', ctx)
        generator.write('{{dst}}/_generated/qml{{module.module_name|lower}}module.h', 'module.h', ctx)
        generator.write('{{dst}}/_generated/qml{{module.module_name|lower}}module.cpp', 'module.cpp', ctx)
        for interface in module.interfaces:
            ctx.update({'interface': interface})
            generator.write('{{dst}}/_generated/qmlabstract{{interface|lower}}.h', 'interface.h', ctx)
            generator.write('{{dst}}/_generated/qmlabstract{{interface|lower}}.cpp', 'interface.cpp', ctx)
        for struct in module.structs:
            ctx.update({'struct': struct})
            generator.write('{{dst}}/_generated/qml{{struct|lower}}.h', 'struct.h', ctx)
            generator.write('{{dst}}/_generated/qml{{struct|lower}}.cpp', 'struct.cpp', ctx)
            generator.write('{{dst}}/_generated/qml{{struct|lower}}model.h', 'structmodel.h', ctx)
            generator.write('{{dst}}/_generated/qml{{struct|lower}}model.cpp', 'structmodel.cpp', ctx)


@click.command()
@click.argument('input', nargs=-1, type=click.Path(exists=True))
@click.argument('output', nargs=1, type=click.Path(exists=True))
def generate(input, output):
    """Takes several files or directories as input and generates the code
    in the given output directory."""
    run_generation(input, output)


if __name__ == '__main__':
    generate()
