from qface.generator import FileSystem
import logging
import logging.config
from path import Path


# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.abspath()))


def loadValues():
    path = inputPath / 'values.qface'
    return FileSystem.parse_document(path)


def test_values():
    system = loadValues()
    # lookup module
    interface = system.lookup('values.Namespace')
    assert interface

