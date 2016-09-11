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
    module = system.lookup_module('one')
    assert module
    service = module.lookup_definition('OneService')
    assert service
    operation = service.operationMap['echo']
    assert operation
    struct = module.lookup_definition('StringStruct')
    assert struct
    assert operation.type.reference is struct

    parameter = operation.parameterMap['message']
    assert parameter
    assert parameter.type.reference is struct

    property = service.propertyMap['message']
    assert property

    assert property.type.reference is struct


def test_resolve_nested():
    system = loadOne()
    module = system.lookup_module('one')
    assert module
    struct = module.lookup_definition('one.StringStruct')
    nested = module.lookup_definition('one.NestedStruct')
    assert struct and nested
    member = struct.memberMap['nested']
    assert member
    assert member.type.reference is nested

    service = module.lookup_definition('one.OneService')
    assert service
    listProperty = service.propertyMap['messageList']
    assert listProperty
    assert listProperty.type.nested.reference is struct

    modelProperty = service.propertyMap['messageModel']
    assert modelProperty
    assert modelProperty.type.nested.reference is struct


