from qface.generator import FileSystem
from unittest.mock import patch
from io import StringIO
import logging
import logging.config
from pathlib import Path


# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.absolute()))


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

    # lookup system
    system = system.lookup('system')
    assert 'global_option' in system.tags

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
    nestedVal = interface.attribute('config', 'c')
    assert nestedVal == {'C': 'e'}
    assert nestedVal['C'] == 'e'
    assert interface.attribute('config', 'd') == 'qrc:/path'  # use value from IDL, Value containing :
    assert interface.tags['data'] == [1, 2, 3]  # array annotatiom

def test_merge_annotation():
    system = loadTuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert interface
    assert interface.attribute('config', 'private') is True
    assert interface.attribute('extra', 'extraA') is None
    FileSystem.merge_annotations(system, inputPath / 'tuner_annotations.yaml')
    assert interface.attribute('extra', 'extraA') is True

@patch('sys.stderr', new_callable=StringIO)
def test_merge_empty_annotation(mock_stderr):
    system = loadTuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert interface
    FileSystem.merge_annotations(system, inputPath / 'empty_tuner_annotations.yaml')

    assert interface.attribute('extra', 'extraA') is None
    assert not mock_stderr.getvalue().__contains__("Error parsing annotation")

@patch('sys.stderr', new_callable=StringIO)
def test_merge_unsafe_annotation(mock_stderr):
    # Regression test for #122: annotation YAML must be parsed with a safe loader,
    # so that tags such as !!python/object/apply cannot instantiate arbitrary
    # Python objects (which would allow code execution from a crafted file).
    import yaml
    from qface.generator import Loader

    # The loader used by load_yaml() must reject Python object instantiation.
    raised = False
    try:
        yaml.load("x: !!python/object/apply:os.getenv ['PATH']", Loader=Loader)
    except yaml.YAMLError:
        raised = True
    assert raised, "unsafe YAML tag accepted: the annotation loader is not safe"

    # The real annotation loading path rejects such a file and loads nothing.
    result = FileSystem.load_yaml(inputPath / 'unsafe_tuner_annotations.yaml')
    assert result == {}
    assert 'error' in mock_stderr.getvalue().lower()


@patch('sys.stderr', new_callable=StringIO)
def test_merge_broken_annotation(mock_stderr):
    system = loadTuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert interface
    FileSystem.merge_annotations(system, inputPath / 'broken_tuner_annotations.yaml')

    assert interface.attribute('extra', 'extraA') is None
    expected_error = "tests/in/broken_tuner_annotations.yaml:2: error: mapping values are not allowed"
    actual_output = mock_stderr.getvalue().replace("\\", "/")  # Normalize backslashes
    assert expected_error in actual_output, f"Expected error not found. Expected: {expected_error}, Actual: {actual_output}"

@patch('sys.stderr', new_callable=StringIO)
def test_merge_invalid_annotation(mock_stderr):
    system = loadTuner()
    interface = system.lookup('com.pelagicore.ivi.tuner.Tuner')
    assert interface
    FileSystem.merge_annotations(system, inputPath / 'invalid_tuner_annotations.yaml')

    assert interface.attribute('extra', 'extraA') is None
    expected_error = "Error parsing annotation tests/in/invalid_tuner_annotations.yaml: not able to lookup symbol: Tunerrrrrrrr\n"
    actual_output = mock_stderr.getvalue().replace("\\", "/")  # Normalize backslashes
    assert expected_error in actual_output, f"Expected error not found. Expected: {expected_error}, Actual: {actual_output}"

@patch('sys.stderr', new_callable=StringIO)
def test_broken_annotation(mock_stderr):
    path = inputPath / 'com.pelagicore.two.qface'
    system = FileSystem.parse_document(path)
    assert system is None
    expected_error = "Invalid YAML: Missing space after ':' in key 'config.qml_type:\"UiAddressBook\"'"
    actual_output = mock_stderr.getvalue().replace("\\", "/")  # Normalize backslashes
    assert expected_error in actual_output, f"Expected error not found. Expected: {expected_error}, Actual: {actual_output}"

@patch('sys.stderr', new_callable=StringIO)
def test_broken_annotation_1(mock_stderr):
    path = inputPath / 'com.pelagicore.three.qface'
    system = FileSystem.parse_document(path)
    assert system is None
    expected_error = "YAML Parsing Error: while parsing [\'config:{ qml_type: \"UiAddressBook\" }\']"
    actual_output = mock_stderr.getvalue().replace("\\", "/")  # Normalize backslashes
    assert expected_error in actual_output, f"Expected error not found. Expected: {expected_error}, Actual: {actual_output}"

@patch('sys.stderr', new_callable=StringIO)
def test_broken_annotation_2(mock_stderr):
    path = inputPath / 'com.pelagicore.four.qface'
    system = FileSystem.parse_document(path)
    assert system is None
    expected_error = "Invalid YAML: Missing space after ':' in key 'config.qml_type.key:value'"
    actual_output = mock_stderr.getvalue().replace("\\", "/")  # Normalize backslashes
    assert expected_error in actual_output, f"Expected error not found. Expected: {expected_error}, Actual: {actual_output}"
