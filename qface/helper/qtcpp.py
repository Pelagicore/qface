"""
Provides helper functionality specificially for Qt C++/QML code generators
"""


def upper_first(s):
    s = str(s)
    return s[0].upper() + s[1:]


class Filters(object):
    """provides a set of filters to be used with the template engine"""
    classPrefix = 'Qml'

    @staticmethod
    def className(symbol):
        classPrefix = Filters.classPrefix
        return '{0}{1}'.format(classPrefix, symbol.name)

    @staticmethod
    def defaultValue(symbol):
        prefix = Filters.classPrefix
        t = symbol.type  # type: qface.domain.TypeSymbol
        if t.is_primitive:
            if t.is_int:
                return '0'
            if t.is_bool:
                return 'false'
            if t.is_string:
                return 'QString()'
            if t.is_real:
                return '0.0'
            if t.is_variant:
                return 'QVariant()'
        elif t.is_void:
            return ''
        elif t.is_enum:
            module_name = t.reference.module.module_name
            value = next(iter(t.reference.members))
            return '{0}{1}Module::{2}'.format(prefix, module_name, value)
        elif symbol.type.is_list:
            nested = Filters.returnType(symbol.type.nested)
            return 'QVariantList()'.format(nested)
        elif symbol.type.is_struct:
            return '{0}{1}()'.format(prefix, symbol.type)
        elif symbol.type.is_model:
            nested = symbol.type.nested
            if nested.is_primitive:
                return 'new {0}VariantModel(this)'.format(prefix)
            elif nested.is_complex:
                return 'new {0}{1}Model(this)'.format(prefix, nested)
        return 'XXX'

    @staticmethod
    def parameterType(symbol):
        prefix = Filters.classPrefix
        module_name = symbol.module.module_name
        if symbol.type.is_enum:
            return '{0}{1}Module::{2} {3}'.format(prefix, module_name, symbol.type, symbol)
        if symbol.type.is_void or symbol.type.is_primitive:
            if symbol.type.name == 'string':
                return 'const QString &{0}'.format(symbol)
            if symbol.type.name == 'var':
                return 'const QVariant &{0}'.format(symbol)
            if symbol.type.name == 'real':
                return 'qreal {0}'.format(symbol)
            return '{0} {1}'.format(symbol.type, symbol)
        elif symbol.type.is_list:
            nested = Filters.returnType(symbol.type.nested)
            return 'const QVariantList &{1}'.format(nested, symbol)
        elif symbol.type.is_model:
            nested = symbol.type.nested
            if nested.is_primitive:
                return '{0}VariantModel *{1}'.format(prefix, symbol)
            elif nested.is_complex:
                return '{0}{1}Model *{2}'.format(prefix, nested, symbol)
        else:
            return 'const {0}{1} &{2}'.format(prefix, symbol.type, symbol)
        return 'XXX'

    @staticmethod
    def returnType(symbol):
        prefix = Filters.classPrefix
        module_name = symbol.module.module_name
        if symbol.type.is_enum:
            return '{0}{1}Module::{2}'.format(prefix, module_name, symbol.type)
        if symbol.type.is_void or symbol.type.is_primitive:
            if symbol.type.name == 'string':
                return 'QString'
            if symbol.type.name == 'var':
                return 'QVariant'
            if symbol.type.name == 'real':
                return 'qreal'
            return symbol.type.name
        elif symbol.type.is_list:
            nested = Filters.returnType(symbol.type.nested)
            return 'QVariantList'.format(nested)
        elif symbol.type.is_model:
            nested = symbol.type.nested
            if nested.is_primitive:
                return '{0}VariantModel *'.format(prefix)
            elif nested.is_complex:
                return '{0}{1}Model *'.format(prefix, nested)
        else:
            return '{0}{1}'.format(prefix, symbol.type)
        return 'XXX'

    @staticmethod
    def open_ns(symbol):
        # 'namespace x { y {'
        blocks = ['{0} {{'.format(x) for x in symbol.module.name_parts]
        return 'namespace {0}'.format(str.join(' ', blocks))

    @staticmethod
    def close_ns(symbol):
        # '} }'
        return ' '.join(['}' for x in symbol.module.name_parts])

