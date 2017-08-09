
# Copyright (c) Pelagicore AB 2016

from jinja2 import Environment, Template
from jinja2 import FileSystemLoader, PackageLoader, ChoiceLoader
from jinja2 import TemplateSyntaxError, TemplateNotFound, TemplateError
from path import Path
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker
from antlr4.error import DiagnosticErrorListener, ErrorListener
import shelve
import logging
import hashlib
import yaml
import click
import sys

from .idl.parser.TLexer import TLexer
from .idl.parser.TParser import TParser
from .idl.parser.TListener import TListener
from .idl.domain import System
from .idl.listener import DomainListener
from .utils import merge
from .filters import filters


try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

logger = logging.getLogger(__name__)


"""
Provides an API for accessing the file system and controlling the generator
"""


class ReportingErrorListener(ErrorListener.ErrorListener):
    def __init__(self, document):
        self.document = document

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        msg = '{0}:{1}:{2} {2}'.format(self.document, line, column, msg)
        click.secho(msg, fg='red')
        raise ValueError(msg)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        click.secho('ambiguity', fg='red')

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        click.secho('reportAttemptingFullContext', fg='red')

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        click.secho('reportContextSensitivity', fg='red')


class Generator(object):
    """Manages the templates and applies your context data"""
    strict = False
    """ enables strict code generation """

    def __init__(self, search_path: str, context: dict={}):
        loader = ChoiceLoader([
            FileSystemLoader(search_path),
            PackageLoader('qface')
        ])
        self.env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.filters.update(filters)
        self._destination = Path()
        self._source = ''
        self.context = context

    @property
    def destination(self):
        """destination prefix for generator write"""
        return self._destination

    @destination.setter
    def destination(self, dst: str):
        if dst:
            self._destination = Path(self.apply(dst, self.context))

    @property
    def source(self):
        """source prefix for template lookup"""
        return self._source

    @source.setter
    def source(self, source: str):
        if source:
            self._source = source

    @property
    def filters(self):
        return self.env.filters

    @filters.setter
    def filters(self, filters):
        self.env.filters.update(filters)

    def get_template(self, name: str):
        """Retrieves a single template file from the template loader"""
        source = name
        if name and name[0] is '/':
            source = name[1:]
        elif self.source is not None:
            source = '/'.join((self.source, name))
            print('get_template: ', name, source)

        return self.env.get_template(source)

    def render(self, name: str, context: dict):
        """Returns the rendered text from a single template file from the
        template loader using the given context data"""
        template = self.get_template(name)
        return template.render(context)

    def apply(self, template: str, context: dict):
        """Return the rendered text of a template instance"""
        return self.env.from_string(template).render(context)

    def write(self, file_path: Path, template: str, context: dict={}, preserve: bool = False):
        """Using a template file name it renders a template
           into a file given a context
        """
        if not context:
            context = self.context
        error = False
        try:
            self._write(file_path, template, context, preserve)
        except TemplateSyntaxError as exc:
            message = '{0}:{1} error: {2}'.format(exc.filename, exc.lineno, exc.message)
            click.secho(message, fg='red')
            error = True
        except TemplateNotFound as exc:
            message = '{0} error: Template not found'.format(exc.name)
            click.secho(message, fg='red')
            error = True
        except TemplateError as exc:
            message = 'error: {0}'.format(exc.message)
            click.secho(message, fg='red')
            error = True
        if error and Generator.strict:
            sys.exit(-1)

    def _write(self, file_path: Path, template: str, context: dict, preserve: bool = False):
        path = self.destination / Path(self.apply(file_path, context))
        path.parent.makedirs_p()
        logger.info('write {0}'.format(path))
        data = self.render(template, context)
        if self._has_different_content(data, path):
            if path.exists() and preserve:
                click.secho('preserve: {0}'.format(path), fg='blue')
            else:
                click.secho('create: {0}'.format(path), fg='blue')
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


class RuleGenerator(Generator):
    """Generates documents based on a rule YAML document"""
    def __init__(self, search_path: str, destination:Path, context:dict={}, features:set=set()):
        super().__init__(search_path, context)
        self.context.update({
            'dst': destination,
            'project': Path(destination).name,
            'features': features,
        })
        self.destination = '{{dst}}'
        self.features = features

    def process_rules(self, path: Path, system: System):
        """writes the templates read from the rules document"""
        self.context.update({
            'system': system,
        })
        document = FileSystem.load_yaml(path, required=True)
        for module, rules in document.items():
            click.secho('process: {0}'.format(module), fg='green')
            self._process_rules(rules, system)

    def _process_rules(self, rules: dict, system: System):
        """ process a set of rules for a target """
        self._source = None # reset the template source
        if not self._shall_proceed(rules):
            return
        self.context.update(rules.get('context', {}))
        self.destination = rules.get('destination', '{{dst}}')
        self.source = rules.get('source', None)
        self._process_rule(rules.get('system', None), {'system': system})
        for module in system.modules:
            self._process_rule(rules.get('module', None), {'module': module})
            for interface in module.interfaces:
                self._process_rule(rules.get('interface', None), {'interface': interface})
            for struct in module.structs:
                self._process_rule(rules.get('struct', None), {'struct': struct})
            for enum in module.enums:
                self._process_rule(rules.get('enum', None), {'enum': enum})

    def _process_rule(self, rule: dict, context: dict):
        """ process a single rule """
        if not rule or not self._shall_proceed(rule):
            return
        self.context.update(context)
        self.context.update(rule.get('context', {}))
        self.destination = rule.get('destination', None)
        self.source = rule.get('source', None)
        preserved = rule.get('preserve', [])
        if not preserved:
            preserved = []
        for target, source in rule.get('documents', {}).items():
            preserve = target in preserved
            self.write(target, source, preserve=preserve)

    def _shall_proceed(self, obj):
        conditions = obj.get('when', [])
        if not conditions:
            return True
        if not isinstance(conditions, list):
            conditions = [conditions]
        result = self.features.intersection(set(conditions))
        return bool(len(result))


class FileSystem(object):
    """QFace helper functions to work with the file system"""
    strict = False
    """ enables strict parsing """

    @staticmethod
    def parse_document(document: Path, system: System = None):
        error = False
        try:
            return FileSystem._parse_document(document, system)
        except FileNotFoundError as e:
            click.secho('{0}: file not found'.format(document), fg='red')
            error = True
        except ValueError as e:
            click.secho('Error parsing document {0}'.format(document))
            error = True
        if error and FileSystem.strict:
            sys.exit(-1)

    @staticmethod
    def _parse_document(document: Path, system: System = None):
        """Parses a document and returns the resulting domain system

        :param path: document path to parse
        :param system: system to be used (optional)
        """
        logger.debug('parse document: {0}'.format(document))
        stream = FileStream(str(document), encoding='utf-8')
        system = FileSystem._parse_stream(stream, system, document)
        FileSystem.merge_annotations(system, document.stripext() + '.yaml')
        return system

    @staticmethod
    def _parse_stream(stream, system: System = None, document=None):
        logger.debug('parse stream')
        system = system or System()

        lexer = TLexer(stream)
        stream = CommonTokenStream(lexer)
        parser = TParser(stream)
        parser.addErrorListener(ReportingErrorListener(document))
        tree = parser.documentSymbol()
        walker = ParseTreeWalker()
        walker.walk(DomainListener(system), tree)
        return system

    @staticmethod
    def merge_annotations(system, document):
        """Read a YAML document and for each root symbol identifier
        updates the tag information of that symbol
        """
        if not Path(document).exists():
            return
        meta = FileSystem.load_yaml(document)
        click.secho('merge: {0}'.format(document.name), fg='blue')
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

    @staticmethod
    def load_yaml(document: Path, required=False):
        document = Path(document)
        if not document.exists():
            if required:
                click.secho('yaml document does not exists: {0}'.format(document), fg='red')
            return {}
        try:
            return yaml.load(document.text(), Loader=Loader)
        except yaml.YAMLError as exc:
            click.secho(str(exc), fg='red')
        return {}
