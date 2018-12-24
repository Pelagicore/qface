import click
import subprocess

"""
API for interacting with the system shell
"""


def sh(args, **kwargs):
    """
    runs the given cmd as shell command
    """
    if isinstance(args, str):
        args = args.split()
    if not args:
        return
    click.echo('$ {0}'.format(' '.join(args)))
    try:
        return subprocess.check_call(args, **kwargs)
    except subprocess.CalledProcessError as exc:
        click.secho('run error {}'.format(exc))
    except OSError as exc:
        click.secho('not found error {}'.format(exc))
