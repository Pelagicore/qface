import logging
import logging.config
from pathlib import Path

from qface.helper import qtcpp
from qface.generator import FileSystem


from antlr4 import InputStream

logging.basicConfig()

log = logging.getLogger(__name__)


src = Path('tests/in')

document = """
// org.example.qface
module org.example 1.0

interface Test {
    void echo(string message);
    Message message;
    Status status;
    list<int> list001;
    list<Message> list002;

}

struct Message {
    string body
}

enum Status {
    ON,
    OFF
}
"""


def parse_document():
    stream = InputStream(document)
    return FileSystem._parse_stream(stream)


def test_return_type():
    system = parse_document()
    interface = system.lookup('org.example.Test')
    assert interface
    operation = interface._operationMap['echo']
    assert operation
    parameter = operation._parameterMap['message']

    types = {
        'bool': 'bool',
        'int': 'int',
        'real': 'qreal',
        'string': 'QString',
        'var': 'QVariant'
    }

    for key, value in types.items():
        parameter.type.name = key
        answer = qtcpp.Filters.returnType(parameter)
        assert answer == value

    # check for struct
    prop = interface._propertyMap['message']
    answer = qtcpp.Filters.returnType(prop)
    assert answer == 'QmlMessage'
    # check for enum
    prop = interface._propertyMap['status']
    answer = qtcpp.Filters.returnType(prop)
    assert answer == 'QmlExampleModule::Status'

    # check for list of primitive
    prop = interface._propertyMap['list001']
    answer = qtcpp.Filters.returnType(prop)
    assert answer == 'QVariantList'

    # check for list of structs
    prop = interface._propertyMap['list002']
    answer = qtcpp.Filters.returnType(prop)
    assert answer == 'QVariantList'


def test_default_value():
    system = parse_document()
    interface = system.lookup('org.example.Test')
    assert interface
    operation = interface._operationMap['echo']
    assert operation
    parameter = operation._parameterMap['message']

    types = {
        'bool': 'false',
        'int': '0',
        'real': '0.0',
        'string': 'QString()',
        'var': 'QVariant()'
    }

    for key, value in types.items():
        parameter.type.name = key
        answer = qtcpp.Filters.defaultValue(parameter)
        assert answer == value

    # check for struct
    prop = interface._propertyMap['message']
    answer = qtcpp.Filters.defaultValue(prop)
    assert answer == 'QmlMessage()'
    # check for enum
    prop = interface._propertyMap['status']
    answer = qtcpp.Filters.defaultValue(prop)
    assert answer == 'Status::ON'

    # check for list of primitive
    prop = interface._propertyMap['list001']
    answer = qtcpp.Filters.defaultValue(prop)
    assert answer == 'QVariantList()'

    # check for list of structs
    prop = interface._propertyMap['list002']
    answer = qtcpp.Filters.defaultValue(prop)
    assert answer == 'QVariantList()'


def test_parameter_type():
    system = parse_document()
    interface = system.lookup('org.example.Test')
    assert interface
    operation = interface._operationMap['echo']
    assert operation
    parameter = operation._parameterMap['message']
    name = parameter.name

    types = {
        'bool': 'bool {0}'.format(name),
        'int': 'int {0}'.format(name),
        'real': 'qreal {0}'.format(name),
        'string': 'const QString &{0}'.format(name),
        'var': 'const QVariant &{0}'.format(name)
    }

    for key, value in types.items():
        parameter.type.name = key
        answer = qtcpp.Filters.parameterType(parameter)
        assert answer == value

    # check for struct
    prop = interface._propertyMap['message']
    answer = qtcpp.Filters.parameterType(prop)
    assert answer == 'const QmlMessage &{0}'.format(prop.name)
    # check for enum
    prop = interface._propertyMap['status']
    answer = qtcpp.Filters.parameterType(prop)
    assert answer == 'QmlExampleModule::Status {0}'.format(prop.name)

    # check for list of primitive
    prop = interface._propertyMap['list001']
    answer = qtcpp.Filters.parameterType(prop)
    assert answer == 'const QVariantList &{0}'.format(prop.name)

    # check for list of structs
    prop = interface._propertyMap['list002']
    answer = qtcpp.Filters.parameterType(prop)
    assert answer == 'const QVariantList &{0}'.format(prop.name)
