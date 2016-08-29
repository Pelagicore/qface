#!/usr/bin/env python3
from qface.generator import FileSystem, Generator

system = FileSystem.parse_dir('./examples')


def paramterType(symbol):
    if symbol.type.is_void or symbol.type.is_primitive:
        return '{0} {1}'.format(symbol.type, symbol)
    else:
        return 'const {0} &{1}'.format(symbol.type, symbol)


def returnType(symbol):
    if symbol.type.is_void or symbol.type.is_primitive:
        return symbol.type
    else:
        return symbol.type

generator = Generator()
generator.register_filter('returnType', returnType)
generator.register_filter('parameterType', paramterType)

for package in system.packages:
    for service in package.services:
        ctx = {'service': service, 'package': package}
        generator.write('out/{{service|lower}}.h', 'service.tpl.h', ctx)
        generator.write('out/{{service|lower}}.cpp', 'service.tpl.cpp', ctx)
    ctx = {'package': package}
    generator.write('out/{{package}}.pro', 'services.pro', ctx)
