from .helper import generic
from .helper import qtqml
from .helper import qtcpp
from .helper import doc
import importlib.util


def get_filters():
    filters = {}
    filters.update(generic.get_filters())
    filters.update(qtqml.Filters.get_filters())
    filters.update(qtcpp.Filters.get_filters())
    filters.update(doc.get_filters())
    return filters


def load_filters(path):
    if not path.exists():
        print('filter module does not exist')
        return {}

    extra_filters = {}
    spec = importlib.util.spec_from_file_location('filters', path.abspath())
    filters_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(filters_module)
    filters_module.get_filters(extra_filters)
    return extra_filters

