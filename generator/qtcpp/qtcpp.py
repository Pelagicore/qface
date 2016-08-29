#!/usr/bin/env python3
import click
from qface.generator import FileSystem, Generator

system = FileSystem.parse_dir('./in')


def paramterType(symbol):
    moduleName = symbol.package.nameParts[-1].capitalize()
    if symbol.type.is_enum:
        return 'Qml{0}Module::{1} {2}'.format(moduleName, symbol.type, symbol)
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
    moduleName = symbol.package.nameParts[-1].capitalize()
    if symbol.type.is_enum:
        return 'Qml{0}Module::{1}'.format(moduleName, symbol.type)
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
    generator.register_filter('returnType', returnType)
    generator.register_filter('parameterType', paramterType)
    ctx = {'output': output}
    for package in system.packages:
        moduleName = package.nameParts[-1].capitalize()
        ctx.update({'package': package, 'module': moduleName})
        packageOutput = generator.apply('{{output}}/{{package|lower}}', ctx)
        ctx.update({'path': packageOutput})
        generator.write('{{path}}/qmldir', 'qmldir', ctx)
        generator.write('{{path}}/plugin.cpp', 'plugin.cpp', ctx)
        generator.write('{{path}}/plugin.h', 'plugin.h', ctx)
        generator.write('{{path}}/{{package|lower}}.pri', 'project.pri', ctx)
        generator.write('{{path}}/{{package|lower}}.pro', 'project.pro', ctx)
        generator.write('{{path}}/{{module|lower}}module.h', 'module.h', ctx)
        generator.write('{{path}}/{{module|lower}}module.cpp', 'module.cpp', ctx)
        for service in package.services:
            ctx.update({'service': service})
            generator.write('{{path}}/{{service|lower}}.h', 'service.h', ctx)
            generator.write('{{path}}/{{service|lower}}.cpp', 'service.cpp', ctx)
        for enum in package.enums:
            ctx.update({'enum': enum})
            generator.write('{{path}}/{{enum|lower}}.h', 'enum.h', ctx)
            generator.write('{{path}}/{{enum|lower}}.cpp', 'enum.cpp', ctx)

        for struct in package.structs:
            ctx.update({'struct': struct})
            generator.write('{{path}}/{{struct|lower}}.h', 'struct.h', ctx)
            generator.write('{{path}}/{{struct|lower}}.cpp', 'struct.cpp', ctx)


@click.command()
@click.option('--input', type=click.Path(exists=True))
@click.option('--output', type=click.Path(exists=True))
def runner(input, output):
    generate(input, output)


if __name__ == '__main__':
    runner()
