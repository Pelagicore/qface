from qif.idl.domain import System
from qif.generator import FileSystem
import logging
import logging.config
from pathlib import Path

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

examples = Path('./examples')
log.debug('examples folder: {0}'.format(examples.absolute()))


def test_parse():
    log.debug('test parse')
    names = FileSystem.find_files(examples, '*.qif')
    # import pdb; pdb.set_trace()
    system = System()
    for name in names:
        log.debug('name: {0}'.format(name))
        FileSystem.parse_document(name, system)


def test_package():
    path = examples / 'tuner.qif'
    system = FileSystem.parse_document(path)
    assert len(system.packages) == 1
    package = system.lookup_package('entertainment.tuner')
    assert package in system.packages.values()


def test_service():
    path = examples / 'tuner.qif'
    system = FileSystem.parse_document(path)
    package = system.lookup_package('entertainment.tuner')
    service = system.lookup_service('entertainment.tuner.Tuner')
    assert service in package.services.values()
    assert service.comment == '/*! Service Tuner */'


def test_attribute():
    path = examples / 'tuner.qif'
    system = FileSystem.parse_document(path)
    service = system.lookup_service('entertainment.tuner.Tuner')
    package = system.lookup_package('entertainment.tuner')
    attr = service.attributes['currentStation']
    assert attr.type.name == 'Station'
    assert attr.package == package
    assert attr.type.qualifiedName == 'entertainment.tuner.Station'
    assert attr.is_readonly
    assert attr.comment == '/*! attribute currentStation */'



def test_struct():
    path = examples / 'tuner.qif'
    system = FileSystem.parse_document(path)
    package = system.lookup_package('entertainment.tuner')
    symbol = system.lookup_struct('entertainment.tuner.Station')
    assert symbol.name == 'Station'
    assert symbol.package == package
    assert symbol.qualifiedName == 'entertainment.tuner.Station'
    assert symbol.comment == '/*! struct Station */'


def test_enum():
    path = examples / 'tuner.qif'
    system = FileSystem.parse_document(path)
    definition = system.lookup_definition('entertainment.tuner.Waveband')
    package = system.lookup_package('entertainment.tuner')
    symbol = system.lookup_enum('entertainment.tuner.Waveband')
    assert definition == symbol
    assert symbol.name == 'Waveband'
    assert symbol.package == package
    assert symbol.qualifiedName == 'entertainment.tuner.Waveband'
    assert symbol.comment == '/*! enum Waveband */'



