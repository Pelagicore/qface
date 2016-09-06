# Copyright (c) Pelagicore AG 2016
# !/usr/bin/env python3
import click
import logging
from qface.generator import FileSystem, Generator

logging.basicConfig(filename='qfacegen.log', filemode='w', level=logging.DEBUG)


def generate(input, output):
    system = FileSystem.parse_dir(input)
    generator = Generator(searchpath='./templates')
    ctx = {'output': output}
    for counter in range(200):
        for module in system.modules:
            ctx.update({'module': module, 'counter': counter})
            generator.write('{{output}}/x{{module}}{{counter}}.qdl', 'document.qdl', ctx)


@click.command()
@click.option('--input', type=click.Path(exists=True))
@click.option('--output', type=click.Path(exists=True))
def runner(input, output):
    generate(input, output)


if __name__ == '__main__':
    runner()
