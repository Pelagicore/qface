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
    generator.write('out/{{package|lower}}/plugin.cpp', 'plugin.cpp', ctx)
    generator.write('out/{{package|lower}}/plugin.h', 'plugin.h', ctx)
    generator.write('out/{{package|lower}}/{{package|lower}}.pri', 'project.pri', ctx)
    generator.write('out/{{package|lower}}/{{package|lower}}.pro', 'project.pro', ctx)
    for service in package.services:
        ctx = {'service': service, 'package': package}
        generator.write('out/{{package|lower}}/{{service|lower}}.h', 'service.tpl.h', ctx)
        generator.write('out/{{package|lower}}/{{service|lower}}.cpp', 'service.tpl.cpp', ctx)
    ctx = {'package': package}
