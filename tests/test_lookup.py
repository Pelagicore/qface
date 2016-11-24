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
    path = inputPath / 'com.pelagicore.ivi.tuner.qdl'
    return FileSystem.parse_document(path)


def test_lookup():
    system = loadTuner()
    # lookup module
    module = system.lookup('com.pelagicore.ivi.tuner')
    assert module is module.lookup('com.pelagicore.ivi.tuner')
    # lookup service
    service = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert service is module.lookup('Tuner')

    # lookup struct
    struct = system.lookup('com.pelagicore.ivi.tuner.Station')
    assert struct is module.lookup('Station')

    # lookup enum
    enum = system.lookup('com.pelagicore.ivi.tuner.Waveband')
    assert enum is module.lookup('Waveband')

