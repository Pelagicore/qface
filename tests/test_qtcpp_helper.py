import logging
import logging.config
from pathlib import Path

from qface.idl.domain import *
from qface.helper import qtcpp

logging.basicConfig()

log = logging.getLogger(__name__)


src = Path('tests/in')

system = System()
module = Module('org.example', system)
interface = Interface('Test', module)
operation = Operation('echo', interface)
parameter = Parameter('message', operation)
parameter.type.name = 'string'
parameter.type.is_primitive = True


def test_return_type():
    interface = system.lookup('org.example.Test')
    assert interface
    operation = interface._operationMap['echo']
    assert operation
    parameter = operation._parameterMap['message']

    # bool
    parameter.type.name = 'bool'
    assert parameter.type.is_bool
    answer = qtcpp.Filters.returnType(parameter)
    assert answer == 'bool'

    # int
    parameter.type.name = 'int'
    assert parameter.type.is_int
    answer = qtcpp.Filters.returnType(parameter)
    assert answer == 'int'

    # real
    parameter.type.name = 'real'
    assert parameter.type.is_real
    answer = qtcpp.Filters.returnType(parameter)
    assert answer == 'qreal'

    # string
    parameter.type.name = 'string'
    assert parameter and parameter.type.is_string
    answer = qtcpp.Filters.returnType(parameter)
    assert answer == 'QString'

    # var
    parameter.type.name = 'var'
    assert parameter and parameter.type.is_variant
    answer = qtcpp.Filters.returnType(parameter)
    assert answer == 'QVariant'


def test_default_value():
    interface = system.lookup('org.example.Test')
    assert interface
    operation = interface._operationMap['echo']
    assert operation
    parameter = operation._parameterMap['message']

    # bool
    parameter.type.name = 'bool'
    assert parameter.type.is_bool
    answer = qtcpp.Filters.defaultValue(parameter)
    assert answer == 'false'

    # int
    parameter.type.name = 'int'
    assert parameter.type.is_int
    answer = qtcpp.Filters.defaultValue(parameter)
    assert answer == '0'

    # real
    parameter.type.name = 'real'
    assert parameter.type.is_real
    answer = qtcpp.Filters.defaultValue(parameter)
    assert answer == '0.0'

    # string
    parameter.type.name = 'string'
    assert parameter and parameter.type.is_string
    answer = qtcpp.Filters.defaultValue(parameter)
    assert answer == 'QString()'

    # var
    parameter.type.name = 'var'
    assert parameter and parameter.type.is_variant
    answer = qtcpp.Filters.defaultValue(parameter)
    assert answer == 'QVariant()'


def test_parameter_type():
    interface = system.lookup('org.example.Test')
    assert interface
    operation = interface._operationMap['echo']
    assert operation
    parameter = operation._parameterMap['message']
    name = parameter.name
    # bool
    parameter.type.name = 'bool'
    assert parameter.type.is_bool
    answer = qtcpp.Filters.parameterType(parameter)
    assert answer == 'bool {0}'.format(name)

    # int
    parameter.type.name = 'int'
    assert parameter.type.is_int
    answer = qtcpp.Filters.parameterType(parameter)
    assert answer == 'int {0}'.format(name)

    # real
    parameter.type.name = 'real'
    assert parameter.type.is_real
    answer = qtcpp.Filters.parameterType(parameter)
    assert answer == 'qreal {0}'.format(name)

    # string
    parameter.type.name = 'string'
    assert parameter and parameter.type.is_string
    answer = qtcpp.Filters.parameterType(parameter)
    assert answer == 'const QString &{0}'.format(name)

    # var
    parameter.type.name = 'var'
    assert parameter and parameter.type.is_variant
    answer = qtcpp.Filters.parameterType(parameter)
    assert answer == 'const QVariant &{0}'.format(name)
