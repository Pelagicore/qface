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
    path = inputPath / 'tuner.qface'
    return FileSystem.parse_document(path)


def test_parse():
    log.debug('test parse')
    names = FileSystem.find_files(inputPath, '*.qface')
    # import pdb; pdb.set_trace()
    system = System()
    for name in names:
        log.debug('name: {0}'.format(name))
        FileSystem.parse_document(name, system)


def test_package():
    system = loadTuner()
    assert len(system.packages) == 1
    package = system.lookup_package('entertainment.tuner')
    assert package in system.packages


def test_service():
    system = loadTuner()
    package = system.lookup_package('entertainment.tuner')
    service = system.lookup_service('entertainment.tuner.Tuner')
    assert service in package.services
    assert service.comment == '/*! Service Tuner */'


def test_attribute():
    system = loadTuner()
    service = system.lookup_service('entertainment.tuner.Tuner')
    package = system.lookup_package('entertainment.tuner')
    attr = service.attributeMap['currentStation']
    assert attr.type.name == 'Station'
    assert attr.package == package
    assert attr.type.qualifiedName == 'entertainment.tuner.Station'
    assert attr.is_readonly
    assert attr.comment == '/*! attribute currentStation */'


def test_struct():
    system = loadTuner()
    package = system.lookup_package('entertainment.tuner')
    symbol = system.lookup_struct('entertainment.tuner.Station')
    assert symbol.name == 'Station'
    assert symbol.package == package
    assert symbol.qualifiedName == 'entertainment.tuner.Station'
    assert symbol.comment == '/*! struct Station */'


def test_enum():
    system = loadTuner()
    definition = system.lookup_definition('entertainment.tuner.Waveband')
    package = system.lookup_package('entertainment.tuner')
    symbol = system.lookup_enum('entertainment.tuner.Waveband')
    assert definition == symbol
    assert symbol.name == 'Waveband'
    assert symbol.package == package
    assert symbol.qualifiedName == 'entertainment.tuner.Waveband'
    assert symbol.comment == '/*! enum Waveband */'
    assert symbol.is_enum


def test_flag():
    system = loadTuner()
    symbol = system.lookup_enum('entertainment.tuner.Features')
    assert symbol.is_flag


def test_list():
    system = loadTuner()
    service = system.lookup_service('entertainment.tuner.Tuner')
    attr = service.attributeMap['primitiveList']
    assert attr.type.name == 'list'
    assert attr.type.is_list is True
    assert attr.type.nested.is_primitive
    assert attr.type.nested.name == 'int'

    attr = service.attributeMap['complexList']
    assert attr.type.name == 'list'
    assert attr.type.is_list is True
    assert attr.type.nested.is_complex
    assert attr.type.nested.name == 'Station'


def test_model():
    system = loadTuner()
    service = system.lookup_service('entertainment.tuner.Tuner')
    attr = service.attributeMap['primitiveModel']
    assert attr.type.name == 'model'
    assert attr.type.is_model is True
    assert attr.type.nested.is_primitive
    assert attr.type.nested.name == 'int'

    attr = service.attributeMap['complexModel']
    assert attr.type.name == 'model'
    assert attr.type.is_model is True
    assert attr.type.nested.is_complex
    assert attr.type.nested.name == 'Station'




