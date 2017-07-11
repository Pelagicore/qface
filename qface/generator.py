# Copyright (c) Pelagicore AB 2016

from jinja2 import Environment, Template
from jinja2 import FileSystemLoader, PackageLoader, ChoiceLoader
from jinja2 import TemplateSyntaxError, TemplateNotFound, TemplateError
from path import Path
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.error import DiagnosticErrorListener
import shelve
import logging
import hashlib
import yaml
import click

from .idl.parser.TLexer import TLexer
from .idl.parser.TParser import TParser
from .idl.parser.TListener import TListener
from .idl.domain import System
from .idl.listener import DomainListener
from .utils import merge


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

logger = logging.getLogger(__name__)


"""
Provides an API for accessing the file system and controlling the generator
"""


def upper_first_filter(s):
    s = str(s)
    return s[0].upper() + s[1:]


def lower_first_filter(s):
    s = str(s)
    return s[0].lower() + s[1:]


class Generator(object):
    """Manages the templates and applies your context data"""
    def __init__(self, search_path: str):
        loader = ChoiceLoader([
            FileSystemLoader(search_path),
            PackageLoader('qface')
        ])
        self.env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters['upperfirst'] = upper_first_filter
        self.env.filters['lowerfirst'] = lower_first_filter
        self._destination = Path()

    @property
    def destination(self):
        """destination prefix for generator write"""
        return self._destination

    @destination.setter
    def destination(self, dst: str):
        self._destination = Path(dst)

    def get_template(self, name: str):
        """Retrieves a single template file from the template loader"""
        return self.env.get_template(name)

    def render(self, name: str, context: dict):
        """Returns the rendered text from a single template file from the
        template loader using the given context data"""
        template = self.get_template(name)
        return template.render(context)

    def apply(self, template: str, context: dict):
        """Return the rendered text of a template instance"""
        return self.env.from_string(template).render(context)

    def write(self, file_path: Path, template: str, context: dict, preserve: bool = False):
        """Using a template file name it renders a template
           into a file given a context
        """
        try:
            self._write(file_path, template, context, preserve)
        except TemplateSyntaxError as exc:
            # import pdb; pdb.set_trace()
            message = '{0}:{1} error: {2}'.format(exc.filename, exc.lineno, exc.message)
            click.secho(message, fg='red')
        except TemplateNotFound as exc:
            message = '{0} error: Template not found'.format(exc.name)
            click.secho(message, fg='red')
        except TemplateError as exc:
            message = 'error: {0}'.format(exc.message)
            click.secho(message, fg='red')

    def _write(self, file_path: Path, template: str, context: dict, preserve: bool = False):
        path = self.destination / Path(self.apply(file_path, context))
        path.parent.makedirs_p()
        logger.info('write {0}'.format(path))
        data = self.render(template, context)
        if self._has_different_content(data, path):
            if path.exists() and preserve:
                click.secho('preserve changed file: {0}'.format(path), fg='blue')
            else:
                click.secho('write changed file: {0}'.format(path), fg='blue')
                path.open('w', encoding='utf-8').write(data)

    def _has_different_content(self, data, path):
        if not path.exists():
            return True
        dataHash = hashlib.new('md5', data.encode('utf-8')).digest()
        pathHash = path.read_hash('md5')
        return dataHash != pathHash

    def register_filter(self, name, callback):
        """Register your custom template filter"""
        self.env.filters[name] = callback


class FileSystem(object):
    """QFace helper functions to work with the file system"""

    @staticmethod
    def parse_document(document: Path, system: System = None):
        """Parses a document and returns the resulting domain system

        :param path: document path to parse
        :param system: system to be used (optional)
        """
        logger.debug('parse document: {0}'.format(document))
        stream = FileStream(str(document), encoding='utf-8')
        system = FileSystem._parse_stream(stream, system)
        FileSystem.merge_annotations(system, document.stripext() + '.yaml')
        return system

    @staticmethod
    def _parse_stream(stream, system: System = None):
        logger.debug('parse stream')
        system = system or System()

        lexer = TLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = TParser(stream)
        parser.addErrorListener(DiagnosticErrorListener.DiagnosticErrorListener())
        tree = parser.documentSymbol()
        walker = ParseTreeWalker()
        walker.walk(DomainListener(system), tree)
        return system

    @staticmethod
    def merge_annotations(system, document):
        """Read a YAML document and for each root symbol identifier
        updates the tag information of that symbol
        """
        if not document.exists():
            return
        meta = {}
        try:
            meta = yaml.load(document.text(), Loader=Loader)
        except yaml.YAMLError as exc:
            click.secho(exc, fg='red')
        click.secho('merge tags from {0}'.format(document), fg='blue')
        for identifier, data in meta.items():
            symbol = system.lookup(identifier)
            if symbol:
                merge(symbol.tags, data)

    @staticmethod
    def parse(input, identifier: str = None, use_cache=False, clear_cache=True, pattern="*.qface"):
        """Input can be either a file or directory or a list of files or directory.
        A directory will be parsed recursively. The function returns the resulting system.
        Stores the result of the run in the domain cache named after the identifier.

        :param path: directory to parse
        :param identifier: identifies the parse run. Used to name the cache
        :param clear_cache: clears the domain cache (defaults to true)
        """
        inputs = input if isinstance(input, (list, tuple)) else [input]
        logger.debug('parse input={0}'.format(inputs))
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
                for document in path.walkfiles(pattern):
                    FileSystem.parse_document(document, system)

        if use_cache:
            cache[identifier] = system
        return system
