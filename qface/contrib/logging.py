import yaml
import logging
import logging.config
import coloredlogs
from path import Path
import os


def basic_log(level):
    logging.basicConfig(level=level)
    coloredlogs.install(level=level)
    print('Fall back to basic logging')


def setup_log(path='logging.yaml', level=logging.INFO, env_key='QFACE_LOG_CFG'):
    path = Path(os.getenv(env_key, path))
    if path.exists():
        try:
            config = yaml.safe_load(path.text())
            logging.config.dictConfig(config)
            coloredlogs.install()
        except Exception as e:
            print(e)
            print('Error in logging configuration. Fall back to defaults.')
            basic_log(level)
    else:
        basic_log(level)
        print('Failed to load logging config file.')
