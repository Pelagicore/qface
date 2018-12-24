#!/usr/bin/env python3
# Copyright (c) Pelagicore AB 2016

import sys
import click
import logging
from path import Path
from qface.generator import FileSystem, RuleGenerator
from qface.watch import monitor
from qface.utils import load_filters
from qface.shell import sh

here = Path(__file__).dirname()
logging.basicConfig()


def run_generator(spec, src, dst, features, force):
    spec = Path(spec)
    project = Path(dst).name
    system = FileSystem.parse(src)

    extra_filters_path = spec.dirname() / 'filters.py'
    extra_filters = load_filters(extra_filters_path)

    ctx = {
        'dst': dst,
        'system': system,
        'project': project,
    }

    generator = RuleGenerator(
        search_path=spec.dirname() / 'templates',
        destination=dst,
        context=ctx,
        features=features,
        force=force
    )
    generator.filters = extra_filters
    generator.process_rules(spec, system)


@click.command()
@click.option('--rules', type=click.Path(exists=True, file_okay=True))
@click.option('--target', type=click.Path(exists=False, file_okay=False))
@click.option('--reload/--no-reload', default=False, help="Auto reload script on changes")
@click.option('--scaffold/--no-scaffold', default=False, help="Add extrac scaffolding code")
@click.option('--watch', type=click.Path(exists=False, file_okay=False))
@click.option('--feature', multiple=True)
@click.option('--run', help="run script after generation")
@click.option('--force/--no-force', default=False, help="forces overwriting of files")
@click.argument('source', nargs=-1, type=click.Path(exists=True))
def main(rules, target, reload, source, watch, scaffold, feature, force, run):
    rules = Path(rules)
    if reload:
        argv = sys.argv.copy()
        argv.remove('--reload')
        watch_list = list(source)
        watch_list.append(rules.dirname())
        if watch:
            watch_list.append(watch)
        monitor(args=argv, watch=watch_list)
    else:
        features = set(feature)
        if scaffold:
            features.add('scaffold')
        run_generator(rules, source, target, features=features, force=force)
        if run:
            sh(run)


if __name__ == '__main__':
    main()
