from qface.generator import FileSystem
import logging
import logging.config
from path import Path


# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')


def loadValues():
    path = inputPath / 'values.qface'
    return FileSystem.parse_document(path)


def test_values():
    system = loadValues()
    assert system
    # lookup module
    interface = system.lookup('values.Namespace')
    assert interface
    properties = interface._propertyMap
    assert properties['intValue'].value == "99"
    assert properties['realValue'].value == "0.99"
    assert properties['message'].value == "foo"
    assert properties['person'].value == '{ name: "Hello", age: 101 }'
    struct = system.lookup('values.Person')
    assert struct
    fields = struct._fieldMap
    assert fields["name"].value == "hello"
    assert fields["age"].value == "99"

