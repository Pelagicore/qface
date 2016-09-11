from qface.idl.domain import System
from qface.generator import FileSystem
import logging
import logging.config
from pathlib import Path

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.absolute()))


def loadOne():
    path = inputPath / 'one.qdl'
    return FileSystem.parse_document(path)


def test_resolve():
    system = loadOne()
    module = system.lookup('one')
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
    system = loadOne()
    module = system.lookup('one')
    assert module
    struct = module.lookup('one.StringStruct')
    nested = module.lookup('one.NestedStruct')
    assert struct and nested
    member = struct._memberMap['nested']
    assert member
    assert member.type.reference is nested

    service = module.lookup('one.OneService')
    assert service
    listProperty = service._propertyMap['messageList']
    assert listProperty
    assert listProperty.type.nested.reference is struct

    modelProperty = service._propertyMap['messageModel']
    assert modelProperty
    assert modelProperty.type.nested.reference is struct


