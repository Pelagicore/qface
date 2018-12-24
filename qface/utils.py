from .generator import FileSystem
from .helper import doc
import click

def module_info(text):
    system = FileSystem.parse_text(text)
    module = list(system.modules)[0]
    return {
        'title': module.name,
        'brief': " ".join(doc.parse_doc(module.comment).brief)
    }


def load_filters(path):
    if not path.exists():
        return {}

    click.secho('loading extra filters from {}'.format(path), fg='green')
    ctx = {
        'filters': {}
    }
    exec(path.text(), ctx)
    return ctx['filters']

