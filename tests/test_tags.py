from qface.generator import FileSystem
import logging
import logging.config
from path import Path


# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.abspath()))


def loadTuner():
    path = inputPath / 'com.pelagicore.ivi.tuner.qface'
    return FileSystem.parse_document(path)


def test_tag():
    system = loadTuner()
    # lookup module
    module = system.lookup('com.pelagicore.ivi.tuner')
    assert module is module.lookup('com.pelagicore.ivi.tuner')
    # lookup service
    service = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert service is module.lookup('Tuner')
    assert 'service' in service.tags
    assert 'interface' in service.tags

    # lookup struct
    struct = system.lookup('com.pelagicore.ivi.tuner.Station')
    assert struct is module.lookup('Station')

    # lookup enum
    enum = system.lookup('com.pelagicore.ivi.tuner.Waveband')
    assert enum is module.lookup('Waveband')
    assert 'default' in enum.tags
    assert enum.attribute('default', 'value') == 'FM'


def test_meta_tags():
    system = loadTuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert interface
    assert 'port' in interface.tags


def test_flag():
    system = loadTuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert interface
    assert interface.attribute('config', 'private') is True
    assert interface.attribute('config', 'a') == 'a'  # use value from yaml
    assert interface.attribute('config', 'b') == 'b'  # use value from yaml
    assert interface.attribute('config', 'c') == 'C'  # use value from IDL
    assert interface.tags['data'] == [1, 2, 3]  # array annotatiom



