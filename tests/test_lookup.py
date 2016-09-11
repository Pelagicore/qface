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


def loadTuner():
    path = inputPath / 'tuner.qdl'
    return FileSystem.parse_document(path)


def test_lookup():
    system = loadTuner()
    # lookup module
    module = system.lookup('entertainment.tuner')
    assert module is module.lookup('entertainment.tuner')
    # lookup service
    service = system.lookup('entertainment.tuner.Tuner')
    assert service is module.lookup('Tuner')

    # lookup struct
    struct = system.lookup('entertainment.tuner.Station')
    assert struct is module.lookup('Station')

    # lookup enum
    enum = system.lookup('entertainment.tuner.Waveband')
    assert enum is module.lookup('Waveband')

