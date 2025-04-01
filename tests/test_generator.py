from qface.generator import FileSystem, Generator, RuleGenerator
from qface.utils import load_filters
from unittest.mock import patch
from io import StringIO
import logging
import logging.config
import tempfile
from pathlib import Path
import shutil

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.absolute()))


def loadSystem():
    path = inputPath / 'com.pelagicore.ivi.tuner.qface'
    return FileSystem.parse_document(path)


def test_gen_module():
    system = loadSystem()
    gen = Generator(search_path='tests/templates')
    template = "{{module}}"
    module = system.lookup('com.pelagicore.ivi.tuner')
    text = gen.apply(template, {"module": module})
    assert text == 'com.pelagicore.ivi.tuner'


def test_gen_interface():
    system = loadSystem()
    gen = Generator(search_path='tests/templates')
    template = """{{module.interfaces|join(',')}}"""
    module = system.lookup('com.pelagicore.ivi.tuner')
    text = gen.apply(template, {"module": module})
    assert text == 'BaseTuner,Tuner,TunerExtension'


def test_parse_document():
    system = FileSystem.parse(inputPath / 'com.pelagicore.ivi.tuner.qface')
    assert system.lookup('com.pelagicore.ivi.tuner')

def test_extra_filters():
    system = FileSystem.parse(inputPath / 'com.pelagicore.ivi.tuner.qface')
    load_filters(Path('tests/templates/filters.py'))
    assert system.lookup('com.pelagicore.ivi.tuner')

def test_parse_document_list():
    src = [inputPath / 'com.pelagicore.ivi.tuner.qface',
           inputPath / 'com.pelagicore.ivi.climate.qface']
    system = FileSystem.parse(src)
    assert system.lookup('com.pelagicore.ivi.tuner')
    assert system.lookup('com.pelagicore.ivi.climate')


def test_parse_document_mixed():
    src = [inputPath, inputPath / 'com.pelagicore.ivi.climate.qface']
    system = FileSystem.parse(src)
    assert system.lookup('com.pelagicore.ivi.tuner')
    assert system.lookup('com.pelagicore.ivi.climate')
    assert system.lookup('com.pelagicore.one')


def test_destination_prefix():
    system = FileSystem.parse(inputPath)
    out = Path('tests/out')
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)
    generator = Generator(search_path='tests/templates')
    for module in system.modules:
        dst_template = '{{out}}/{{module|lower}}.txt'
        ctx = {'out': out.absolute(), 'module': module}
        generator.write(dst_template, 'module.txt', ctx)
        path = generator.apply(dst_template, ctx)
        assert Path(path).exists() == True
    shutil.rmtree(out, ignore_errors=True)

def test_regeneration():
    system = FileSystem.parse(inputPath)
    out = Path('tests/out')
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)
    generator = Generator(search_path='tests/templates')
    for module in system.modules:
        dst_template = '{{out}}/{{module|lower}}.txt'
        ctx = {'out': out.absolute(), 'module': module}
        generator.write(dst_template, 'module.txt', ctx)
        generator.write(dst_template, 'module.txt', ctx)
        path = generator.apply(dst_template, ctx)
        assert Path(path).exists() == True
    shutil.rmtree(out, ignore_errors=True)

def test_rulegenerator():
    system = FileSystem.parse(inputPath)
    out = Path('tests/out')
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)
    generator = RuleGenerator(search_path='tests/templates', destination=out)
    generator.process_rules('tests/templates/rules.yaml', system)
    shutil.rmtree(out, ignore_errors=True)

@patch('sys.stderr', new_callable=StringIO)
def test_error_template_syntax_error(mock_stderr):
    tmpDir = tempfile.TemporaryDirectory()
    src = [inputPath, inputPath / 'com.pelagicore.ivi.climate.qface']
    system = FileSystem.parse(src)
    dst_template = '{{out}}/out.txt'
    ctx = {'out': tmpDir.name}
    generator = Generator(search_path='tests/templates')
    generator.write(dst_template, 'syntaxError.txt', ctx)
    path = generator.apply(dst_template, ctx)
    assert Path(path).exists() == False
    expected_error = "tests/templates/syntaxError.txt:1: error: Encountered unknown tag 'fooo'.\n"
    actual_output = mock_stderr.getvalue().replace("\\", "/")  # Normalize backslashes
    assert expected_error in actual_output, f"Expected error not found. Expected: {expected_error}, Actual: {actual_output}"

@patch('sys.stderr', new_callable=StringIO)
def test_error_template_undefined_variable(mock_stderr):
    tmpDir = tempfile.TemporaryDirectory()
    src = [inputPath, inputPath / 'com.pelagicore.ivi.climate.qface']
    system = FileSystem.parse(src)
    dst_template = '{{out}}/out.txt'
    ctx = {'out': tmpDir.name}
    generator = Generator(search_path='tests/templates')
    generator.write(dst_template, 'undefinedVariable.txt', ctx)
    path = generator.apply(dst_template, ctx)
    assert Path(path).exists() == False
    expected_error = "tests/templates/undefinedVariable.txt:1: error: 'this_is_not_defined' is undefined\n"
    actual_output = mock_stderr.getvalue().replace("\\", "/")  # Normalize backslashes
    assert expected_error in actual_output, f"Expected error not found. Expected: {expected_error}, Actual: {actual_output}"

@patch('sys.stderr', new_callable=StringIO)
def test_error_template_doesnt_exist(mock_stderr):
    tmpDir = tempfile.TemporaryDirectory()
    src = [inputPath, inputPath / 'com.pelagicore.ivi.climate.qface']
    system = FileSystem.parse(src)
    dst_template = '{{out}}/out.txt'
    ctx = {'out': tmpDir.name}
    generator = Generator(search_path='tests/templates')
    generator.write(dst_template, 'doesnt_exist.txt', ctx)
    path = generator.apply(dst_template, ctx)
    assert Path(path).exists() == False
    assert "/doesnt_exist.txt: error: Template not found\n" in mock_stderr.getvalue()

@patch('sys.stderr', new_callable=StringIO)
def test_error_yaml_doesnt_exist(mock_stderr):
    tmpDir = tempfile.TemporaryDirectory()
    system = FileSystem.parse(inputPath)
    out = Path('tests/out')
    shutil.rmtree(out, ignore_errors=True)
    out.mkdir(parents=True, exist_ok=True)
    generator = RuleGenerator(search_path='tests/templates', destination=out)
    generator.process_rules('doesnt_exist.txt', system)
    assert "yaml document does not exists: doesnt_exist.txt\n" in mock_stderr.getvalue()
