import logging
import logging.config
from path import Path

from qface.generator import FileSystem

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.abspath()))


def load_one():
    path = inputPath / 'com.pelagicore.one.qface'
    return FileSystem.parse_document(path)


def test_resolve():
    system = load_one()
    module = system.lookup('com.pelagicore.one')
    assert module
    service = module.lookup('OneService')
    assert service
    operation = service._operationMap['echo']
    assert operation
    struct = module.lookup('StringStruct')
    assert struct
    assert operation.type.reference is struct

    parameter = operation._parameterMap['message']
    assert parameter
    assert parameter.type.reference is struct

    property = service._propertyMap['message']
    assert property

    assert property.type.reference is struct


def test_resolve_nested():
    system = load_one()
    module = system.lookup('com.pelagicore.one')
    assert module
    struct = module.lookup('com.pelagicore.one.StringStruct')
    nested = module.lookup('com.pelagicore.one.NestedStruct')
    assert struct and nested
    member = struct._fieldMap['nested']
    assert member
    assert member.type.reference is nested

    service = module.lookup('com.pelagicore.one.OneService')
    assert service
    list_property = service._propertyMap['messageList']
    assert list_property
    assert list_property.type.nested.reference is struct

    model_property = service._propertyMap['messageModel']
    assert model_property
    assert model_property.type.nested.reference is struct
