#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import click
from qface.generator import FileSystem, Generator


def run(src, dst):
    system = FileSystem.parse(src)
    generator = Generator(searchpath='templates')
    ctx = {'dst': dst, 'system': system}
    generator.write('{{dst}}/modules.csv', 'modules.csv', ctx)


@click.command()
@click.argument('src', nargs=-1, type=click.Path(exists=True))
@click.argument('dst', nargs=1, type=click.Path(exists=True))
def app(src, dst):
    """Generates a modules,csv file with statistics about all
    interfaces, structs and enums from the given interface
    sources"""
    run(src, dst)


if __name__ == '__main__':
    app()
