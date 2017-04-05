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


def load_test():
    path = inputPath / 'com.pelagicore.test.qface'
    return FileSystem.parse_document(path)


def test_parse():
    log.debug('test parse')
    system = FileSystem.parse(inputPath)
    assert system


def test_module():
    system = load_tuner()
    assert len(system.modules) == 1
    module = system.lookup('com.pelagicore.ivi.tuner')
    assert module in system.modules


def test_interface():
    system = load_tuner()
    module = system.lookup('com.pelagicore.ivi.tuner')
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert interface in module.interfaces
    assert interface.comment == '/** Service Tuner */'


def test_property():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    module = system.lookup('com.pelagicore.ivi.tuner')
    property = interface._propertyMap['currentStation']
    assert property.type.name == 'Station'
    assert property.module == module
    assert property.type.qualified_name == 'com.pelagicore.ivi.tuner.Station'
    assert property.is_readonly
    assert not property.is_const
    assert property.comment == '/** property currentStation */'

    property = interface._propertyMap['defaultStation']
    assert not property.is_readonly
    assert property.is_const


def test_operation():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    operation = interface._operationMap['nextStation']
    assert operation
    operation = interface._contentMap['previousStation']
    assert operation


def test_signals():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    signal = interface._signalMap['scanFinished']
    assert signal


def test_struct():
    system = load_tuner()
    module = system.lookup('com.pelagicore.ivi.tuner')
    symbol = system.lookup('com.pelagicore.ivi.tuner.Station')
    assert symbol.name == 'Station'
    assert symbol.module == module
    assert symbol.qualified_name == 'com.pelagicore.ivi.tuner.Station'
    assert symbol.comment == '/** struct Station */'


def test_enum():
    system = load_tuner()
    definition = system.lookup('com.pelagicore.ivi.tuner.Waveband')
    module = system.lookup('com.pelagicore.ivi.tuner')
    symbol = system.lookup('com.pelagicore.ivi.tuner.Waveband')
    assert definition == symbol
    assert symbol.name == 'Waveband'
    assert symbol.module == module
    assert symbol.qualified_name == 'com.pelagicore.ivi.tuner.Waveband'
    assert symbol.comment == '/** enum Waveband */'
    assert symbol.is_enum


def test_enum_counter():
    system = load_test()
    enum = system.lookup('com.pelagicore.test.State')
    assert enum
    assert enum._memberMap['Null'].value is 0
    assert enum._memberMap['Failure'].value is 3


def test_flag_counter():
    system = load_test()
    flag = system.lookup('com.pelagicore.test.Phase')
    assert flag
    assert flag._memberMap['PhaseOne'].value is 1
    assert flag._memberMap['PhaseTwo'].value is 2
    assert flag._memberMap['PhaseThree'].value is 4


def test_flag():
    system = load_tuner()
    symbol = system.lookup('com.pelagicore.ivi.tuner.Features')
    assert symbol.is_flag


def test_list():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    property = interface._propertyMap['primitiveList']
    assert property.type.name == 'list'
    assert property.type.is_list is True
    assert property.type.nested.is_primitive
    assert property.type.nested.name == 'int'

    property = interface._propertyMap['complexList']
    assert property.type.name == 'list'
    assert property.type.is_list is True
    assert property.type.nested.is_complex
    assert property.type.nested.name == 'Station'


def test_model():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    property = interface._propertyMap['primitiveModel']
    assert property.type.name == 'model'
    assert property.type.is_model is True
    assert property.type.nested.is_primitive
    assert property.type.nested.name == 'int'

    property = interface._propertyMap['complexModel']
    assert property.type.name == 'model'
    assert property.type.is_model is True
    assert property.type.nested.is_complex
    assert property.type.nested.name == 'Station'
