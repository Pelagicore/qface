#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import sys
import click
import logging
from path import Path
from qface.generator import FileSystem, RuleGenerator
from qface.watch import monitor

here = Path(__file__).dirname()
logging.basicConfig()


def run(spec, src, dst):
    spec = Path(spec)
    project = Path(dst).name
    system = FileSystem.parse(src)

    context = {
        'dst': dst,
        'system': system,
        'project': project,
    }

    generator = RuleGenerator(search_path=spec.dirname() / 'templates', destination=dst, context=context)
    generator.process_rules(spec, system)


@click.command()
@click.option('--spec', type=click.Path(exists=True, file_okay=True))
@click.option('--dst', type=click.Path(exists=False, file_okay=False))
@click.option('--reload/--no-reload', default=False, help="Auto reload script on changes")
@click.argument('src', nargs=-1, type=click.Path(exists=True))
def main(spec, dst, reload, src):
    spec = Path(spec)
    if reload:
        argv = sys.argv.copy()
        argv.remove('--reload')
        monitor(args=argv, watch=src + (spec.dirname(),))
    else:
        run(spec, src, dst)


if __name__ == '__main__':
    main()
