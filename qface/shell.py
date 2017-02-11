import click
from subprocess import call


def sh(cmd, **kwargs):
    if not cmd:
        return
    click.echo('$ {0}'.format(cmd))
    return call(cmd, shell=True, **kwargs)
