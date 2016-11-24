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


def loadTest():
    path = inputPath / 'com.pelagicore.test.qdl'
    return FileSystem.parse_document(path)


def test_parse():
    log.debug('test parse')
    names = FileSystem.find_files(inputPath, '*.qdl')
    # import pdb; pdb.set_trace()
    system = System()
    for name in names:
        log.debug('name: {0}'.format(name))
        FileSystem.parse_document(name, system)


def test_module():
    system = loadTuner()
    assert len(system.modules) == 1
    module = system.lookup('com.pelagicore.ivi.tuner')
    assert module in system.modules


def test_interface():
    system = loadTuner()
    module = system.lookup('com.pelagicore.ivi.tuner')
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert interface in module.interfaces
    assert interface.comment == '/*! Service Tuner */'


def test_property():
    system = loadTuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    module = system.lookup('com.pelagicore.ivi.tuner')
    property = interface._propertyMap['currentStation']
    assert property.type.name == 'Station'
    assert property.module == module
    assert property.type.qualified_name == 'com.pelagicore.ivi.tuner.Station'
    assert property.is_readonly
    assert property.comment == '/*! property currentStation */'


def test_struct():
    system = loadTuner()
    module = system.lookup('com.pelagicore.ivi.tuner')
    symbol = system.lookup('com.pelagicore.ivi.tuner.Station')
    assert symbol.name == 'Station'
    assert symbol.module == module
    assert symbol.qualified_name == 'com.pelagicore.ivi.tuner.Station'
    assert symbol.comment == '/*! struct Station */'


def test_enum():
    system = loadTuner()
    definition = system.lookup('com.pelagicore.ivi.tuner.Waveband')
    module = system.lookup('com.pelagicore.ivi.tuner')
    symbol = system.lookup('com.pelagicore.ivi.tuner.Waveband')
    assert definition == symbol
    assert symbol.name == 'Waveband'
    assert symbol.module == module
    assert symbol.qualified_name == 'com.pelagicore.ivi.tuner.Waveband'
    assert symbol.comment == '/*! enum Waveband */'
    assert symbol.is_enum


def test_enum_counter():
    system = loadTest()
    enum = system.lookup('com.pelagicore.test.State')
    assert enum
    # import ipdb; ipdb.set_trace()
    assert enum._memberMap['Null'].value is 0
    assert enum._memberMap['Failure'].value is 3

def test_flag_counter():
    system = loadTest()
    flag = system.lookup('com.pelagicore.test.Phase')
    assert flag
    # import ipdb; ipdb.set_trace()
    assert flag._memberMap['PhaseOne'].value is 1
    assert flag._memberMap['PhaseTwo'].value is 2
    assert flag._memberMap['PhaseThree'].value is 4

def test_flag():
    system = loadTuner()
    symbol = system.lookup('com.pelagicore.ivi.tuner.Features')
    assert symbol.is_flag


def test_list():
    system = loadTuner()
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
    system = loadTuner()
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




