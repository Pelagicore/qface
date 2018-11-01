import sys
import click
from path import Path
from qface.generator import FileSystem, RuleGenerator
from qface.watch import monitor


def run(config, src, dst, force=False, features=None):
    project = Path(dst).name
    system = FileSystem.parse(src)
    template_dir = config.dirname() / 'templates'

    context = {
        'dst': dst,
        'system': system,
        'project': project,
        'features': features,
    }

    generator = RuleGenerator(template_dir, destination=dst, context=context, features=features, force=force)
    generator.process_rules(config, system)


@click.command()
@click.option('--config', '-c', type=click.Path(exists=True))
@click.option('--reload/--no-reload', default=False)
@click.option('--features', '-f', multiple=True)
@click.option('--force/--no-force', default=True, help="Force writing of target files, ignores preserve")
@click.argument('src', nargs=-1, type=click.Path(exists=True))
@click.argument('dst', nargs=1, type=click.Path(exists=False, file_okay=False))
def app(config, src, dst, features, reload, force):
    """Takes several files or directories as src and generates the code
    in the given dst directory."""
    config = Path(config)
    if reload:
        argv = sys.argv.copy()
        argv.remove('--reload')
        monitor(config.dirname(), src, dst, argv)
    else:
        run(config, src, dst, force)
