import click
from subprocess import call

"""
API for interacting with the system shell
"""


def sh(cmd, **kwargs):
    """
    runs the given cmd as shell command
    """
    if not cmd:
        return
    click.echo('$ {0}'.format(cmd))
    return call(cmd, shell=True, **kwargs)
