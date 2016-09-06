from qface.generator import FileSystem
import logging
import logging.config
from pathlib import Path

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.absolute()))


def load_system():
    path = inputPath / 'climate.qface'
    return FileSystem.parse_document(path)


def test_interface():
    system = load_system()
    interface = system.lookup_interface('vehicle.climate.ClimateControl')
    assert interface.name == 'ClimateControl'





