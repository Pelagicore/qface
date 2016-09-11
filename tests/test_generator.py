from qface.generator import FileSystem, Generator
import logging
import logging.config
from pathlib import Path

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')
log.debug('input path folder: {0}'.format(inputPath.absolute()))


def loadSystem():
    path = inputPath / 'tuner.qdl'
    return FileSystem.parse_document(path)


def test_gen_module():
    system = loadSystem()
    gen = Generator(searchpath='tests/templates')
    template = "{{module}}"
    module = system.lookup('entertainment.tuner')
    text = gen.apply(template, {"module": module})
    assert text == 'entertainment.tuner'


def test_gen_interface():
    system = loadSystem()
    gen = Generator(searchpath='tests/templates')
    template = """
        {%- for interface in module.interfaces -%}
            {{interface}}
        {%- endfor -%}
    """
    module = system.lookup('entertainment.tuner')
    text = gen.apply(template, {"module": module})
    assert text == 'Tuner'

