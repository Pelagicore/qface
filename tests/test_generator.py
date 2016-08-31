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
    path = inputPath / 'tuner.qface'
    return FileSystem.parse_document(path)


def test_gen_package():
    system = loadSystem()
    gen = Generator(searchpath='tests/templates')
    template = "{{package}}"
    package = system.lookup_package('entertainment.tuner')
    text = gen.apply(template, {"package": package})
    assert text == 'entertainment.tuner'


def test_gen_service():
    system = loadSystem()
    gen = Generator(searchpath='tests/templates')
    template = """
        {%- for service in package.services -%}
            {{service}}
        {%- endfor -%}
    """
    package = system.lookup_package('entertainment.tuner')
    text = gen.apply(template, {"package": package})
    assert text == 'Tuner'

