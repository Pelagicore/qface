from setuptools import setup

setup(
    name='qface',
    version='1.0',
    py_modules=['qface'],
    install_requires=[
        'antlr4-python3-runtime',
        'jinja2',
        'click',
        'path.py',
        'watchdog',
        'pyyaml',
        'pytest',
        'ipdb'
    ],
    entry_points='''
        [console_scripts]
        qface=cli:cli
    ''',
)
