"""
Provides helper functionality specificially for Qt C++/QML code generators
"""
import qface.idl.domain as domain
from jinja2 import environmentfilter
from ..filters import upper_first


class Filters(object):
    """provides a set of filters to be used with the template engine"""
    classPrefix = ''

    @staticmethod
    def className(symbol):
        classPrefix = Filters.classPrefix
        return '{0}{1}'.format(classPrefix, symbol.name)

    @staticmethod
    def defaultValue(symbol):
        prefix = Filters.classPrefix
        t = symbol.type
        if t.is_primitive:
            if t.is_int:
                return 'int(0)'
            if t.is_bool:
                return 'bool(false)'
            if t.is_string:
                return 'QString()'
            if t.is_real:
                return 'qreal(0.0)'
            if t.is_var:
                return 'QVariant()'
        elif t.is_void:
            return ''
        elif t.is_enum:
            value = next(iter(t.reference.members))
            return '{0}::{0}Enum::{1}'.format(symbol.type, value)
        elif symbol.kind == 'enum':
            value = next(iter(symbol.members))
            return '{0}::{1}'.format(symbol, value)
        elif t.is_flag:
            return '0'
        elif t.is_list:
            nested = Filters.returnType(t.nested)
            return 'QVariantList()'.format(nested)
        elif t.is_struct:
            return '{0}{1}()'.format(prefix, t)
        elif t.is_model:
            return 'new VariantModel(this)'
        elif t.is_interface:
            return 'nullptr'
        raise Exception("Unknown symbol type" + repr(symbol))

    @staticmethod
    def parameterType(symbol):
        prefix = Filters.classPrefix
        if symbol.type.is_enum:
            return '{0}::{0}Enum {1}'.format(symbol.type, symbol)
        if symbol.type.is_void or symbol.type.is_primitive:
            if symbol.type.is_string:
                return 'const QString &{0}'.format(symbol)
            if symbol.type.is_var:
                return 'const QVariant &{0}'.format(symbol)
            if symbol.type.is_real:
                return 'qreal {0}'.format(symbol)
            if symbol.type.is_bool:
                return 'bool {0}'.format(symbol)
            if symbol.type.is_int:
                return 'int {0}'.format(symbol)
            return '{0} {1}'.format(symbol.type, symbol)
        elif symbol.type.is_list:
            nested = Filters.returnType(symbol.type.nested)
            return 'const QVariantList &{1}'.format(nested, symbol)
        elif symbol.type.is_model:
            return 'VariantModel *{0}'.format(symbol)
        elif symbol.type.is_complex:
            if symbol.type.is_interface:
                return '{0}Base *{1}'.format(symbol.type, symbol)
            else:
                return 'const {0}{1} &{2}'.format(prefix, symbol.type, symbol)
        raise Exception("Unknown symbol type")

    @staticmethod
    def returnType(symbol):
        prefix = Filters.classPrefix
        t = symbol.type
        if t.is_enum:
            return '{0}::{0}Enum'.format(symbol.type)
        if symbol.type.is_void or symbol.type.is_primitive:
            if t.is_string:
                return 'QString'
            if t.is_var:
                return 'QVariant'
            if t.is_real:
                return 'qreal'
            if t.is_int:
                return 'int'
            if t.is_bool:
                return 'bool'
            if t.is_void:
                return 'void'
            print(t)
            assert False
        elif symbol.type.is_list:
            nested = Filters.returnType(symbol.type.nested)
            return 'QVariantList'.format(nested)
        elif symbol.type.is_model:
            return 'VariantModel *'
        elif symbol.type.is_complex:
            if symbol.type.is_interface:
                return '{0}Base *'.format(symbol.type)
            else:
                return '{0}{1}'.format(prefix, symbol.type)
        raise Exception("Unknown symbol type")

    @staticmethod
    def header_dependencies(symbol):
        types = symbol.dependencies
        lines = []
        for t in types:
            if t.is_primitive:
                continue
            if t.is_model:
                lines.append('class VariantModel;')
            if t.is_interface:
                lines.append('class {0};'.format(t))
            if t.is_struct:
                lines.append('#include "{0}.h"'.format(t))
        return "\n".join(lines)

    @staticmethod
    def source_dependencies(symbol):
        types = symbol.dependencies
        lines = []
        module_name = symbol.module.module_name
        if not symbol.kind == 'module':
            lines.append('#include "{0}module.h"'.format(module_name.lower()))
        for t in types:
            if t.is_primitive:
                continue
            if t.is_model:
                lines.append('#include "variantmodel.h"')
            if t.is_interface:
                lines.append('#include "{0}.h"'.format(t.name.lower()))
        return "\n".join(lines)

    @staticmethod
    def open_ns(symbol):
        ''' generates a open namespace from symbol namespace x { y { z {'''
        blocks = ['namespace {0} {{'.format(x) for x in symbol.module.name_parts]
        return ' '.join(blocks)

    @staticmethod
    def close_ns(symbol):
        '''generates a closing names statement from a symbol'''
        closing = ' '.join(['}' for x in symbol.module.name_parts])
        name = '::'.join(symbol.module.name_parts)
        return '{0} // namespace {1}'.format(closing, name)

    @staticmethod
    def using_ns(symbol):
        '''generates a using namespace x::y::z statement from a symbol'''
        id = '::'.join(symbol.module.name_parts)
        return 'using namespace {0};'.format(id)

    @staticmethod
    def ns(symbol):
        '''generates a namespace x::y::z statement from a symbol'''
        if symbol.type and symbol.type.is_primitive:
            return ''
        return '{0}::'.format('::'.join(symbol.module.name_parts))

    @staticmethod
    def fqn(symbol):
        '''generates a fully qualified name from symbol'''
        return '{0}::{1}'.format(Filters.ns(symbol), symbol.name)

    @staticmethod
    def signalName(s):
        if isinstance(s, domain.Property):
            return '{0}Changed'.format(s)
        return s

    @staticmethod
    @environmentfilter
    def parameters(env, s, filter=None, spaces=True):
        if not filter:
            filter = Filters.parameterType
        elif isinstance(filter, str):
            filter = env.filters[filter]
        args = []
        indent = ', '
        if not spaces:
            indent = ','
        if isinstance(s, domain.Operation):
            args = s.parameters
        elif isinstance(s, domain.Signal):
            args = s.parameters
        elif isinstance(s, domain.Struct):
            args = s.fields
        elif isinstance(s, domain.Property):
            args = [s]
        return indent.join([filter(a) for a in args])

    @staticmethod
    @environmentfilter
    def signature(env, s, expand=False, filter=None):
        if not filter:
            filter = Filters.returnType
        elif isinstance(filter, str):
            filter = env.filters[filter]
        if isinstance(s, domain.Operation):
            args = s.parameters
        elif isinstance(s, domain.Signal):
            args = s.parameters
        elif isinstance(s, domain.Property):
            args = [s]  # for <property>Changed(<type>)
        elif isinstance(s, domain.Struct):
            args = s.fields
        else:
            args = []
        if expand:
            return ', '.join(['{0} {1}'.format(filter(a), a.name) for a in args])
        return ','.join([filter(a) for a in args])

    @staticmethod
    def identifier(s):
        return str(s).lower().replace('.', '_')

    @staticmethod
    def path(s):
        return str(s).replace('.', '/')

    @staticmethod
    def get_filters():
        return {
            'defaultValue': Filters.defaultValue,
            'returnType': Filters.returnType,
            'parameterType': Filters.parameterType,
            'open_ns': Filters.open_ns,
            'close_ns': Filters.close_ns,
            'using_ns': Filters.using_ns,
            'ns': Filters.ns,
            'fqn': Filters.fqn,
            'signalName': Filters.signalName,
            'parameters': Filters.parameters,
            'signature': Filters.signature,
            'identifier': Filters.identifier,
            'path': Filters.path,
            'className': Filters.className,
            'source_dependencies': Filters.source_dependencies,
            'header_dependencies': Filters.header_dependencies,
        }
