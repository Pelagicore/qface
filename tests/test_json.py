from qface.generator import FileSystem
import logging
from path import Path
import json

# logging.config.fileConfig('logging.ini')
logging.basicConfig()

log = logging.getLogger(__name__)

inputPath = Path('tests/in')


def loadEcho():
    path = inputPath / 'org.example.echo.qface'
    return FileSystem.parse_document(path)


def load_tuner():
    path = inputPath / 'com.pelagicore.ivi.tuner.qface'
    return FileSystem.parse_document(path)


def test_echo_json():
    system = loadEcho()
    data = system.toJson()
    text = json.dumps(data)
    data = json.loads(text)
    assert len(data['modules']) == 1
    module = data['modules'][0]
    assert module['name'] == 'org.example.echo'
    assert module['version'] == '1.0'
    assert len(module['interfaces']) == 1
    interface = module['interfaces'][0]
    assert interface['name'] == 'Echo'
    assert len(interface['operations']) == 1
    # string echo(string msg);
    operation = interface['operations'][0]
    assert operation['parameters'][0]['name'] == 'msg'
    assert operation['parameters'][0]['type']['name'] == 'string'


def test_tuner_json():
    system = load_tuner()
    data = system.toJson()
    text = json.dumps(data)
    data = json.loads(text)
    module = data['modules'][0]
    interface = module['interfaces'][0]
    assert interface['name'] == 'Tuner'

