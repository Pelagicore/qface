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


def test_service():
    system = load_system()
    service = system.lookup_service('vehicle.climate.ClimateControl')
    assert service.name == 'ClimateControl'





