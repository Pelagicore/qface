from qface.generator import FileSystem, Generator
from unittest.mock import patch
from io import StringIO
import logging
import logging.config
import tempfile
from path import Path

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.abspath()))


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
    out.rmtree_p()
    out.makedirs_p()
    generator = Generator(search_path='tests/templates')
    for module in system.modules:
        dst_template = '{{out}}/{{module|lower}}.txt'
        ctx = {'out': out.abspath(), 'module': module}
        generator.write(dst_template, 'module.txt', ctx)
        path = generator.apply(dst_template, ctx)
        assert Path(path).exists() == True
    out.rmtree_p()

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
    assert mock_stderr.getvalue() == "tests/templates/syntaxError.txt:1: error: Encountered unknown tag 'fooo'.\n"

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
    assert mock_stderr.getvalue() == "tests/templates/undefinedVariable.txt:1: error: 'this_is_not_defined' is undefined\n"

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
    assert mock_stderr.getvalue() == "/doesnt_exist.txt: error: Template not found\n"
