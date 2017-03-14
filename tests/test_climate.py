from qface.generator import FileSystem
import logging
import logging.config
from path import Path

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.abspath()))


def load_system():
    path = inputPath / 'com.pelagicore.ivi.climate.qface'
    return FileSystem.parse_document(path)


def test_interface():
    system = load_system()
    interface = system.lookup('com.pelagicore.ivi.climate.ClimateControl')
    assert interface.name == 'ClimateControl'
