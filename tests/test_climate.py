from qif.idl.domain import System
from qif.generator import FileSystem, Generator
import logging
import logging.config
from pathlib import Path

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

examples = Path('./examples')
log.debug('examples folder: {0}'.format(examples.absolute()))


def load_system():
    path = examples / 'climate.qif'
    return FileSystem.parse_document(path)


def test_service():
    system = load_system()
    service = system.lookup_service('vehicle.climate.ClimateControl')
    assert service.name == 'ClimateControl'





