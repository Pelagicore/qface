from qface.generator import FileSystem
from qface.helper import doc
import logging
import logging.config
from path import Path


# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')


def qdoc_translate(name, value):
    if not value.startswith('http'):
        value = value.replace('.', '::')
    return r'\{0}{{{1}}}'.format(name, value)


# doc.DocObject.translate = translate

def loadEcho():
    path = inputPath / 'org.example.echo.qface'
    return FileSystem.parse_document(path)


def test_comment():
    system = loadEcho()
    doc.translate = None
    module = system.lookup('org.example.echo')
    assert module.comment == '/** module */'
    assert module
    interface = system.lookup('org.example.echo.Echo')
    assert interface
    o = doc.parse_doc(interface.comment)
    assert o.brief == ['the brief']
    assert o.description == ['the description', 'continues {@link http://qt.io}', 'continued description']
    assert o.deprecated is True
    assert o.see == ['org.example.echo.Echo', 'org.example', 'http://qt.io']


def test_qdoc_translate():
    system = loadEcho()
    module = system.lookup('org.example.echo')
    assert module.comment == '/** module */'
    assert module
    interface = system.lookup('org.example.echo.Echo')
    assert interface
    doc.translate = qdoc_translate
    o = doc.parse_doc(interface.comment)
    assert o.description == ['the description', 'continues \\link{http://qt.io}', 'continued description']
