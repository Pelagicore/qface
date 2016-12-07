# Copyright (c) Pelagicore AB 2016

from jinja2 import Environment, FileSystemLoader, Template
from path import Path
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.error import DiagnosticErrorListener
import shelve
import logging
import hashlib

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
    """Manages the templates and applies your context data"""
    def __init__(self, searchpath: str):
        if searchpath:
            searchpath = Path(searchpath).expand()
            self.env = Environment(loader=FileSystemLoader(searchpath), trim_blocks=True, lstrip_blocks=True)
        self.env.filters['upperfirst'] = upper_first_filter

    def get_template(self, name: str):
        """Retrievs a single template file from the template loader"""
        return self.env.get_template(name)

    def render(self, name: str, context: dict):
        """Returns the rendered text from a single template file from the
        template loader using the given context data"""
        template = self.get_template(name)
        return template.render(context)

    def apply(self, template: Template, context: dict):
        """Return the rendered text of a template instance"""
        return self.env.from_string(template).render(context)

    def write(self, fileTemplate: str, template: str, context: dict, preserve=False):
        """Using a templated file name it renders a template
           into a file given a context"""
        path = Path(self.apply(fileTemplate, context))
        path.parent.makedirs_p()
        logger.info('write {0}'.format(path))
        data = self.render(template, context)
        if self.hasDifferentContent(data, path):
            if not preserve and path.exists():
                print('skip changed file: {0}'.format(path))
            else:
                print('write changed file: {0}'.format(path))
                path.open('w').write(data)

    def hasDifferentContent(self, data, path):
        if not path.exists():
            return True
        dataHash = hashlib.new('md5', data.encode('utf-8')).digest()
        pathHash = path.read_hash('md5')
        return dataHash != pathHash

    def register_filter(self, name, callback):
        """Register your custom template filter"""
        self.env.filters[name] = callback


class FileSystem(object):
    """QFace helper function to work with the file system"""

    @staticmethod
    def parse_document(path: str, system: System = None):
        """Parses a document and returns the resulting domain system

        :param path: document path to parse
        :param system: system to be used (optional)
        """
        logger.debug('parse document: {0}'.format(path))

        system = system or System()

        data = FileStream(str(path), encoding='utf-8')
        lexer = TLexer(data)
        stream = CommonTokenStream(lexer)
        parser = TParser(stream)
        parser.addErrorListener(DiagnosticErrorListener.DiagnosticErrorListener())
        tree = parser.documentSymbol()
        walker = ParseTreeWalker()
        walker.walk(DomainListener(system), tree)

        return system

    @staticmethod
    def parse(input, identifier: str = None, use_cache=False, clear_cache=True):
        """Input can be either a file or directory or a list of files or directory.
        A directory will be parsed recursively. The function returns the resulting system.
        Stores the result of the run in the domain cache named after the identifier.

        :param path: directory to parse
        :param identifier: identifies the parse run. Used to name the cache
        :param clear_cache: clears the domain cache (defaults to true)
        """
        inputs = input if isinstance(input, (list, tuple)) else [input]
        logging.debug('parse input={0}'.format(inputs))
        identifier = 'system' if not identifier else identifier
        system = System()
        cache = None
        if use_cache:
            cache = shelve.open('qface.cache')
            if identifier in cache and clear_cache:
                del cache[identifier]
            if identifier in cache:
                # use the cached domain model
                system = cache[identifier]
        # if domain model not cached generate it
        for input in inputs:
            path = Path.getcwd() / str(input)
            if path.isfile():
                FileSystem.parse_document(path, system)
            else:
                for document in path.walkfiles('*.qdl'):
                    FileSystem.parse_document(document, system)
        if use_cache:
            cache[identifier] = system
        return system
