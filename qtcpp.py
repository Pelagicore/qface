#!/usr/bin/env python3
from qface.generator import FileSystem, Generator

system = FileSystem.parse_document('./examples/test.qface')


def cppType(symbol):
    if symbol.type.is_void:
        return 'void'
    if symbol.type.is_primitive:
        if symbol.type.name == 'string':
            return 'QString'
        if symbol.type.name == 'real':
            return 'float'


def paramterType(symbol):
    if symbol.type.is_void or symbol.type.is_primitive:
        if symbol.type.name == 'string':
            return 'const QString &{0}'.format(symbol)
        if symbol.type.name == 'real':
            return 'float {0}'.format(symbol)
        return '{0} {1}'.format(symbol.type, symbol)
    else:
        return 'const {0} &{1}'.format(symbol.type, symbol)


def returnType(symbol):
    if symbol.type.is_void or symbol.type.is_primitive:
        if symbol.type.name == 'string':
            return 'QString'
        if symbol.type.name == 'real':
            return 'float'
        return symbol.type
    else:
        return symbol.type

generator = Generator()
generator.register_filter('returnType', returnType)
generator.register_filter('parameterType', paramterType)

for package in system.packages:
    ctx = {'package': package}
    out = generator.apply('out/{{package|lower}}', ctx)
    ctx['out'] = out
    generator.write('{{out}}/qmldir', 'qmldir', ctx)
    generator.write('{{out}}/plugin.cpp', 'plugin.cpp', ctx)
    generator.write('{{out}}/plugin.h', 'plugin.h', ctx)
    generator.write('{{out}}/{{package|lower}}.pri', 'project.pri', ctx)
    generator.write('{{out}}/{{package|lower}}.pro', 'project.pro', ctx)
    for service in package.services:
        ctx = {'service': service, 'package': package, 'out': out}
        generator.write('{{out}}/{{service|lower}}.h', 'service.h', ctx)
        generator.write('{{out}}/{{service|lower}}.cpp', 'service.cpp', ctx)
    for enum in package.enums:
        ctx = {'enum': enum, 'package': package, 'out': out}
        generator.write('{{out}}/{{enum|lower}}.h', 'enum.h', ctx)
        generator.write('{{out}}/{{enum|lower}}.cpp', 'enum.cpp', ctx)

    for struct in package.structs:
        ctx = {'struct': struct, 'package': package, 'out': out}
        generator.write('{{out}}/{{struct|lower}}.h', 'struct.h', ctx)
        generator.write('{{out}}/{{struct|lower}}.cpp', 'struct.cpp', ctx)
        generator.write('{{out}}/{{struct|lower}}factory.h', 'structfactory.h', ctx)
        generator.write('{{out}}/{{struct|lower}}factory.cpp', 'structfactory.cpp', ctx)

    ctx = {'package': package}
