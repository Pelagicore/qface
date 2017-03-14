import logging
import logging.config
from path import Path

from qface.generator import FileSystem

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.abspath()))


def load_tuner():
    path = inputPath / 'com.pelagicore.ivi.tuner.qface'
    return FileSystem.parse_document(path)


def test_lookup():
    system = load_tuner()
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

    property = system.lookup('com.pelagicore.ivi.tuner.Tuner#currentStation')
    assert property.name == 'currentStation'

    operation = system.lookup('com.pelagicore.ivi.tuner.Tuner#nextStation')
    assert operation.name == 'nextStation'
