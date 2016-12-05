#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from qface.generator import FileSystem, Generator
import os

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
        return 'const {0} &{1}'.format(symbol.type, symbol)


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
        return symbol.type


def generate(input, output):
    system = FileSystem.parse(input)
    generator = Generator(searchpath=os.path.join(here, 'templates'))
    generator.register_filter('returnType', returnType)
    generator.register_filter('parameterType', paramterType)
    ctx = {'output': output}
    for module in system.modules:
        ctx.update({'module': module})
        moduleOutput = generator.apply('{{output}}/{{module|lower}}', ctx)
        ctx.update({'path': moduleOutput})
        generator.write('{{path}}/qmldir', 'qmldir', ctx)
        generator.write('{{path}}/plugin.cpp', 'plugin.cpp', ctx)
        generator.write('{{path}}/plugin.h', 'plugin.h', ctx)
        generator.write('{{path}}/{{module|lower}}.pri', 'project.pri', ctx)
        generator.write('{{path}}/{{module|lower}}.pro', 'project.pro', ctx)
        generator.write('{{path}}/qml{{module.module_name|lower}}module.h', 'module.h', ctx)
        generator.write('{{path}}/qml{{module.module_name|lower}}module.cpp', 'module.cpp', ctx)
        for interface in module.interfaces:
            ctx.update({'interface': interface})
            generator.write('{{path}}/{{interface|lower}}.h', 'interface.h', ctx)
            generator.write('{{path}}/{{interface|lower}}.cpp', 'interface.cpp', ctx)
        for struct in module.structs:
            ctx.update({'struct': struct})
            generator.write('{{path}}/{{struct|lower}}.h', 'struct.h', ctx)
            generator.write('{{path}}/{{struct|lower}}.cpp', 'struct.cpp', ctx)
            generator.write('{{path}}/{{struct|lower}}model.h', 'structmodel.h', ctx)
            generator.write('{{path}}/{{struct|lower}}model.cpp', 'structmodel.cpp', ctx)


@click.command()
@click.argument('input', nargs=-1, type=click.Path(exists=True))
@click.argument('output', nargs=1, type=click.Path(exists=True))
def main(input, output):
    """Takes several files or directories as input and generates the code
    in the given output directory."""
    generate(input, output)


if __name__ == '__main__':
    main()
