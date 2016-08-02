from qif.idl.domain import System
from qif.generator import FileSystem, Generator
import logging
import logging.config
from pathlib import Path

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

examples = Path('./examples')
log.debug('examples folder: {0}'.format(examples.absolute()))


def loadSystem():
    path = examples / 'tuner.qif'
    return FileSystem.parse_document(path)


def test_gen_package():
    system = loadSystem()
    gen = Generator()
    template = "{{package}}"
    package = system.lookup_package('entertainment.tuner')
    text = gen.apply(template, {"package": package})
    assert text == 'entertainment.tuner'


def test_gen_service():
    system = loadSystem()
    gen = Generator()
    template = """
        {%- for service in package.services -%}
            {{service}}
        {%- endfor -%}
    """
    package = system.lookup_package('entertainment.tuner')
    text = gen.apply(template, {"package": package})
    assert text == 'Tuner'

