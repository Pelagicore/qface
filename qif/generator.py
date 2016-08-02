from jinja2 import Environment, FileSystemLoader, Template
from pathlib import Path
import shelve
import logging

from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.error import DiagnosticErrorListener

from .idl.parser.TLexer import TLexer
from .idl.parser.TParser import TParser
from .idl.parser.TListener import TListener
from .idl.domain import System
from .idl.listener import DomainListener


logger = logging.getLogger(__name__)


def upper_first_filter(s):
    s = str(s)
    return s[0].upper() + s[1:]


class Generator(object):
    def __init__(self, folder: str ='templates'):
        folder = Path(folder).resolve().as_posix()
        self.env = Environment(loader=FileSystemLoader(folder), trim_blocks=True, lstrip_blocks=True)
        self.register_filters()

    def get_template(self, name: str):
        return self.env.get_template(name)

    def render(self, name: str, context: dict):
        template = self.get_template(name)
        return template.render(context)

    def apply(self, template: Template, context: dict):
        return Template(template).render(context)

    def write(self, fileTemplate: str, template: str, context: dict):
        path = Path(self.apply(fileTemplate, context))
        self.mkdir(path.parent)
        logger.info('write {0}'.format(path))
        data = self.render(template, context)
        path.open('w').write(data)

    def mkdir(self, path: str):
        path = Path(path)
        try:
            path.mkdir(parents=True)
        except OSError:
            pass

    def register_filters(self):
        self.env.filters['upperfirst'] = upper_first_filter

    def register_filter(self, name, callback):
        self.env.filters[name] = callback



class FileSystem(object):
    @staticmethod
    def parse_document(path: str, system: System = None):
        system = system or System()
        listener = DomainListener(system)
        FileSystem._parse_document(path, listener)
        return system

    @staticmethod
    def _parse_document(path: str, listener: TListener):
        logger.debug('parse document: {0}'.format(path))
        data = FileStream(str(path), encoding='utf-8')
        lexer = TLexer(data)
        stream = CommonTokenStream(lexer)
        parser = TParser(stream)
        parser.addErrorListener(DiagnosticErrorListener.DiagnosticErrorListener())
        tree = parser.documentSymbol()
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

    @staticmethod
    def parse_dir(path, identifier: str = None, clear_cache=True):
        path = Path(path)
        logging.debug('parse_tree path={0}'.format(path))
        if not identifier:
            identifier = 'system'
        system = System()
        cache = shelve.open('qif.cache')
        if identifier in cache and clear_cache:
            del cache[identifier]
        if identifier in cache:
            # use the cached domain model
            system = cache[identifier]
        else:
            # if domain model not cached generate it
            documents = path.rglob('*.qif')
            for document in documents:
                listener = DomainListener(system)
                FileSystem._parse_document(document, listener)
            cache[identifier] = system
        return system

    @staticmethod
    def find_files(path, glob='*.qif'):
        path = Path(path)
        logging.debug('find_files path={0} glob={1}'.format(path, glob))
        return path.rglob(glob)
