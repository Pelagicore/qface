import click
from subprocess import call

"""
API for interacting with the system shell
"""


def sh(args, **kwargs):
    """
    runs the given cmd as shell command
    """
    if not args:
        return
    click.echo('$ {0}'.format(' '.join(args)))
    return call(args, **kwargs)
