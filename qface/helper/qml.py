"""
Provides helper functionality specificially for Qt5 QML code generators
"""


class Filters(object):
    """provides a set of filters to be used with the template engine"""
    classPrefix = ''

    @staticmethod
    def className(symbol):
        classPrefix = Filters.classPrefix
        return '{0}{1}'.format(classPrefix, symbol.name)

    @staticmethod
    def defaultValue(symbol):
        t = symbol.type
        if t.is_primitive:
            if t.name == 'int':
                return '0'
            if t.name == 'bool':
                return 'false'
            if t.name == 'string':
                return ''
        elif t.is_enum:
            name = t.reference.name
            value = next(iter(t.reference.members))
            return '{0}.{1}'.format(name, value)
        return 'XXX'

    @staticmethod
    def propertyType(symbol):
        return symbol
        classPrefix = Filters.classPrefix
        module_name = symbol.module.module_name
        if symbol.type.is_enum:
            return '{0}{1}Module.{2} {3}'.format(classPrefix, module_name, symbol.type, symbol)
        if symbol.type.is_void or symbol.type.is_primitive:
            if symbol.type.name == 'string':
                return 'string {0}'.format(symbol)
            if symbol.type.name == 'var':
                return 'var {0}'.format(symbol)
            if symbol.type.name == 'real':
                return 'real {0}'.format(symbol)
            return '{0} {1}'.format(symbol.type, symbol)
        elif symbol.type.is_list:
            return 'ListModel {1}'.format(symbol.type.nested, symbol)
        elif symbol.type.is_model:
            return '{0}Model {1}'.format(symbol.type.nested, symbol)
        else:
            return '{0}{1} {2}'.format(classPrefix, symbol.type, symbol)

