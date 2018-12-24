import logging
import logging.config
import pytest
from path import Path

from qface.generator import FileSystem
import qface.idl.domain as domain

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
    assert property.readonly
    assert not property.const
    assert property.comment == '/** property currentStation */'

    property = interface._propertyMap['defaultStation']
    assert not property.readonly
    assert property.const


def test_operation():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    operation = interface._operationMap['nextStation']
    assert operation
    operation = interface._contentMap['previousStation']
    assert operation
    assert not operation.is_const
    operation = interface._contentMap['numStations']
    assert operation
    assert operation.is_const


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
    assert type(enum) is domain.Enum
    assert enum
    assert enum._memberMap['Null'].value is 0
    assert enum._memberMap['Failure'].value is 3


def test_flag_counter():
    system = load_test()
    flag = system.lookup('com.pelagicore.test.Phase')
    assert type(flag) is domain.Enum
    assert flag
    assert flag._memberMap['PhaseOne'].value is 1
    assert flag._memberMap['PhaseTwo'].value is 2
    assert flag._memberMap['PhaseThree'].value is 4


def test_flag():
    system = load_tuner()
    symbol = system.lookup('com.pelagicore.ivi.tuner.Feature')
    assert type(symbol) is domain.Enum
    assert symbol.is_flag
    assert not symbol.is_enum
    symbol = system.lookup('com.pelagicore.ivi.tuner.Tuner#feature')
    assert type(symbol) is domain.Property
    assert type(symbol.type.reference) is domain.Enum

    assert symbol.type.is_flag
    assert symbol.type.is_enumeration


def test_list():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    property = interface._propertyMap['primitiveList']
    assert type(property) is domain.Property
    assert property.type.name == 'list'
    assert property.type.is_list is True
    assert property.type.nested.is_primitive
    assert property.type.nested.name == 'int'

    property = interface._propertyMap['complexList']
    assert type(property) is domain.Property
    assert property.type.name == 'list'
    assert property.type.is_list is True
    assert property.type.nested.is_complex
    assert property.type.nested.name == 'Station'


def test_struct_list():
    system = load_tuner()
    struct = system.lookup('com.pelagicore.ivi.tuner.Station')
    field = struct._fieldMap['primitiveList']
    assert type(field) is domain.Field
    assert field.type.name == 'list'
    assert field.type.is_list is True
    assert field.type.nested.is_primitive
    assert field.type.nested.name == 'int'

    field = struct._fieldMap['complexList']
    assert type(field) is domain.Field
    assert field.type.name == 'list'
    assert field.type.is_list is True
    assert field.type.nested.is_complex
    assert field.type.nested.name == 'Station'


def test_map():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    property = interface._propertyMap['primitiveMap']
    assert type(property) is domain.Property
    assert property.type.name == 'map'
    assert property.type.is_map is True
    assert property.type.nested.is_primitive
    assert property.type.nested.name == 'int'

    property = interface._propertyMap['complexMap']
    assert type(property) is domain.Property
    assert property.type.name == 'map'
    assert property.type.is_map is True
    assert property.type.nested.is_complex
    assert property.type.nested.name == 'Station'


def test_struct_map():
    system = load_tuner()
    struct = system.lookup('com.pelagicore.ivi.tuner.Station')
    field = struct._fieldMap['primitiveMap']
    assert type(field) is domain.Field
    assert field.type.name == 'map'
    assert field.type.is_map is True
    assert field.type.nested.is_primitive
    assert field.type.nested.name == 'int'

    field = struct._fieldMap['complexMap']
    assert type(field) is domain.Field
    assert field.type.name == 'map'
    assert field.type.is_map is True
    assert field.type.nested.is_complex
    assert field.type.nested.name == 'Station'


def test_model():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    property = interface._propertyMap['primitiveModel']
    assert type(property) is domain.Property
    assert property.type.name == 'model'
    assert property.type.is_model is True
    assert property.type.nested.is_primitive
    assert property.type.nested.name == 'int'

    property = interface._propertyMap['complexModel']
    assert type(property) is domain.Property
    assert property.type.name == 'model'
    assert property.type.is_model is True
    assert property.type.nested.is_complex
    assert property.type.nested.name == 'Station'


def test_extension():
    system = load_tuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    extends = system.lookup('com.pelagicore.ivi.tuner.BaseTuner')
    # import pdb; pdb.set_trace()
    assert extends is interface.extends


def test_interface_property():
    system = load_tuner()
    tuner = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    extension = system.lookup('com.pelagicore.ivi.tuner.TunerExtension')
    prop = tuner._propertyMap['extension']
    assert prop.type.is_interface
    assert prop.type.reference is extension


def test_symbol_kind():
    system = load_tuner()
    tuner = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert tuner.kind == 'interface'
    property = system.lookup('com.pelagicore.ivi.tuner.Tuner#primitiveModel')
    assert property.kind == 'property'


def test_parser_exceptions():
    path = inputPath / 'org.example.failing.qface'
    system = FileSystem.parse_document(path)

    system = FileSystem.parse_document('not-exists')


def test_default_values():
    system = load_test()
    interface = system.lookup('com.pelagicore.test.ContactService')
    symbol = system.lookup('com.pelagicore.test.ContactService#intValue')
    assert symbol.value == "2"    
    symbol = system.lookup('com.pelagicore.test.ContactService#realValue')
    assert symbol.value == "0.1"    
    
