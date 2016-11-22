#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
import logging
import logging.config
import yaml
from qface.generator import FileSystem, Generator


logging.config.dictConfig(yaml.load(open('log.yaml')))
logger = logging.getLogger(__name__)


def className(symbol):
    return 'QIvi{0}'.format(symbol.name)


def paramterType(symbol):
    module_name = symbol.module.name_parts[-1].capitalize()
    if symbol.type.is_enum:
        return 'Qml{0}Module::{1} {2}'.format(module_name, symbol.type, symbol)
    if symbol.type.is_void or symbol.type.is_primitive:
        if symbol.type.name == 'string':
            return 'const QString &{0}'.format(symbol)
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
    module_name = symbol.module.module_name()
    if symbol.type.is_enum:
        return 'QIvi{0}Module::{1}'.format(module_name, symbol.type)
    if symbol.type.is_void or symbol.type.is_primitive:
        if symbol.type.name == 'string':
            return 'QString'
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
    system = FileSystem.parse_dir(input)
    generator = Generator(searchpath='./templates')
    generator.register_filter('className', className)
    generator.register_filter('returnType', returnType)
    generator.register_filter('parameterType', paramterType)
    ctx = {'output': output}
    for module in system.modules:
        logger.debug('process %s' % module)
        module_name = module.module_name()
        ctx.update({'module': module, 'module_name': module_name})
        moduleOutput = generator.apply('{{output}}/ivi{{module_name|lower}}', ctx)
        ctx.update({'path': moduleOutput})
        generator.write('{{path}}/ivi{{module_name|lower}}.pro', 'project.pro', ctx)
        for interface in module.interfaces:
            ctx.update({'interface': interface})
            generator.write('{{path}}/{{interface|className|lower}}.h', 'interface.h', ctx)
            generator.write('{{path}}/{{interface|className|lower}}_p.h', 'interface_p.h', ctx)
            generator.write('{{path}}/{{interface|className|lower}}.cpp', 'interface.cpp', ctx)
            generator.write('{{path}}/{{interface|className|lower}}backendinterface.h', 'backendinterface.h', ctx)
            generator.write('{{path}}/{{interface|className|lower}}backendinterface.cpp', 'backendinterface.cpp', ctx)
        for struct in module.structs:
            ctx.update({'struct': struct})
            generator.write('{{path}}/{{struct|className|lower}}.h', 'struct.h', ctx)
            generator.write('{{path}}/{{struct|className|lower}}.cpp', 'struct.cpp', ctx)


@click.command()
@click.option('--input', type=click.Path(exists=True))
@click.option('--output', type=click.Path(exists=True))
def runner(input, output):
    generate(input, output)


if __name__ == '__main__':
    runner()
