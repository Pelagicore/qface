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
            name = t.reference.name
            value = next(iter(t.reference.members))
            return '{0}::{1}'.format(name, value)
        elif symbol.type.is_list:
            nested = Filters.returnType(symbol.type.nested)
            return 'QVariantList()'.format(nested)
        elif symbol.type.is_struct:
            return 'Qml{0}()'.format(symbol.type)
        elif symbol.type.is_model:
            nested = symbol.type.nested
            if nested.is_primitive:
                return 'new QmlVariantModel(this)'
            elif nested.is_complex:
                return 'new Qml{0}Model(this)'.format(nested)
        return 'XXX'

    @staticmethod
    def parameterType(symbol):
        classPrefix = Filters.classPrefix
        module_name = symbol.module.module_name
        if symbol.type.is_enum:
            return '{0}{1}Module::{2} {3}'.format(classPrefix, module_name, symbol.type, symbol)
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
                return 'QmlVariantModel *{0}'.format(symbol)
            elif nested.is_complex:
                return 'Qml{0}Model *{1}'.format(nested, symbol)
        else:
            return 'const {0}{1} &{2}'.format(classPrefix, symbol.type, symbol)
        return 'XXX'

    @staticmethod
    def returnType(symbol):
        classPrefix = Filters.classPrefix
        module_name = symbol.module.module_name
        if symbol.type.is_enum:
            return '{0}{1}Module::{2}'.format(classPrefix, module_name, symbol.type)
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
                return 'QmlVariantModel *'
            elif nested.is_complex:
                return 'Qml{0}Model *'.format(nested)
        else:
            return '{0}{1}'.format(classPrefix, symbol.type)
        return 'XXX'

