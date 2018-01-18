"""
Provides helper functionality specificially for Qt5 QML code generators
"""


def upper_first(s):
    s = str(s)
    return s[0].upper() + s[1:]


class Filters(object):
    """provides a set of filters to be used with the template engine"""
    classPrefix = ''

    @staticmethod
    def className(symbol):
        classPrefix = Filters.classPrefix
        return '{0}{1}'.format(classPrefix, symbol.name)

    @staticmethod
    def defaultValue(symbol):
        module = upper_first(symbol.module.module_name)
        t = symbol.type
        if t.is_primitive:
            if t.name == 'int':
                return '0'
            elif t.name == 'real':
                return "0.0"
            elif t.name == 'bool':
                return 'false'
            elif t.name == 'string':
                return "''"
            elif t.name == 'var':
                return "undefined"
        elif t.is_enum:
            value = next(iter(t.reference.members))
            return '{0}Module.{1}'.format(module, value)
        if t.is_struct:
            return '{0}Module.create{1}()'.format(module, t)
        if t.is_model:
            return 'ListModel {}'
        return 'XXX'

    @staticmethod
    def propertyType(symbol):
        t = symbol.type
        if t.is_enum:
            return 'int'
        if t.is_void or t.is_primitive:
            if t.name == 'int':
                return 'int'
            if t.name == 'bool':
                return 'bool'
            if t.name == 'string':
                return 'string'
        if t.is_struct:
            return 'var'
        if t.is_model:
            return 'ListModel'
        return t

    @staticmethod
    def path(s):
        return str(s).replace('.', '/')

    @staticmethod
    def identifier(s):
        return str(s).lower().replace('.', '_')

