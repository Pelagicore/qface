from qface.generator import FileSystem
from qface.helper import doc
import logging
import logging.config
from path import Path


# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')


def loadEcho():
    path = inputPath / 'org.example.echo.qface'
    return FileSystem.parse_document(path)


def test_comment():
    system = loadEcho()
    module = system.lookup('org.example.echo')
    assert module.comment == '/** module */'
    assert module
    interface = system.lookup('org.example.echo.Echo')
    assert interface
    o = doc.parse_doc(interface.comment)
    assert o.brief == 'the brief'
    assert o.description == 'the description continues'
    assert o.deprecated is None

