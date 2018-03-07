# Copyright (c) Pelagicore AB 2016
import logging

from .parser.TListener import TListener
from .parser.TParser import TParser
from .domain import *
from antlr4 import ParserRuleContext
import yaml
import click
from .profile import get_features, EProfile, EFeature

try:
    from yaml import CSafeLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import SafeLoader as Loader, Dumper


log = logging.getLogger(__name__)

# associates parser context to domain objects
contextMap = {}


class QFaceListener(TListener):
    def __init__(self, system, profile=EProfile.FULL):
        super().__init__()
        click.secho('qface uses language profile: {}'.format(profile), fg='blue')
        self.lang_features = get_features(profile)
        self.system = system or System()  # type:System

    def check_support(self, feature, report=True):
        if feature not in self.lang_features and report:
            click.secho('Unsuported language feature: {}'.format(EFeature.IMPORT), fg='red')
            return False
        return True


class DomainListener(QFaceListener):
    """The domain listener is called by the parser to fill the
       domain data struture. As a result a system is passed
       back"""

    def __init__(self, system, profile=EProfile.FULL):
        super().__init__(system, profile)
        contextMap.clear()
        self.module = None  # type:Module
        self.interface = None  # type:Interface
        self.struct = None  # type:Struct
        self.enum = None  # type:Enum
        self.enumCounter = 0  # int
        self.operation = None  # type:Operation
        self.signal = None  # type:Signal
        self.parameter = None  # type:Parameter
        self.property = None  # type:Property
        self.field = None  # type:Field

    def parse_type(self, ctx: ParserRuleContext, type: TypeSymbol):
        assert type
        if not ctx.typeSymbol():
            type.is_void = True
            type.name = 'void'
        else:
            if ctx.typeSymbol().primitiveTypeSymbol():
                # type:TParser.PrimitiveTypeSymbolContext
                ctxSymbol = ctx.typeSymbol().primitiveTypeSymbol()
                type.is_primitive = True
                type.name = ctxSymbol.name.text
            elif ctx.typeSymbol().complexTypeSymbol():
                # type:TParser.ComplexTypeSymbolContext
                ctxSymbol = ctx.typeSymbol().complexTypeSymbol()
                type.is_complex = True
                type.name = ctxSymbol.name.text
            elif ctx.typeSymbol().listTypeSymbol():
                # type:TParser.ListTypeSymbolContext
                ctxSymbol = ctx.typeSymbol().listTypeSymbol()
                type.is_list = True
                type.name = 'list'
                type.nested = TypeSymbol("", type)
                self.parse_type(ctxSymbol, type.nested)
            elif ctx.typeSymbol().mapTypeSymbol():
                self.check_support(EFeature.MAPS)
                # type:TParser.ListTypeSymbolContext
                ctxSymbol = ctx.typeSymbol().mapTypeSymbol()
                type.is_map = True
                type.name = 'map'
                type.nested = TypeSymbol("", type)
                self.parse_type(ctxSymbol, type.nested)
            elif ctx.typeSymbol().modelTypeSymbol():
                # type:TParser.ModelTypeSymbolContext
                ctxSymbol = ctx.typeSymbol().modelTypeSymbol()
                type.is_model = True
                type.name = 'model'
                type.nested = TypeSymbol("", type)
                self.parse_type(ctxSymbol, type.nested)
        if not type.module.checkType(type):
            log.warn('Unknown type: {0}. Missing import?'.format(type.name))

    def parse_annotations(self, ctx, symbol):
        assert ctx and symbol
        if ctx.comment:
            comment = ctx.comment.text
            symbol.comment = comment
        if ctx.tagSymbol():
            lines = [tag.line.text[1:] for tag in ctx.tagSymbol()]
            try:
                data = yaml.load('\n'.join(lines), Loader=Loader)
                symbol._tags = data
            except yaml.YAMLError as exc:
                click.secho(str(exc), fg='red')

    def enterEveryRule(self, ctx):
        log.debug('enter ' + ctx.__class__.__name__)

    def exitEveryRule(self, ctx):
        log.debug('exit ' + ctx.__class__.__name__)

    def enterModuleSymbol(self, ctx: TParser.ModuleSymbolContext):
        assert self.system
        name = ctx.name.text
        version = ctx.version.text
        self.module = Module(name, self.system)
        self.module.version = version
        contextMap[ctx] = self.module
        self.parse_annotations(ctx, self.module)

    def exitModuleSymbol(self, ctx: TParser.ModuleSymbolContext):
        pass

    def enterInterfaceSymbol(self, ctx: TParser.InterfaceSymbolContext):
        assert self.module
        name = ctx.name.text
        self.interface = Interface(name, self.module)
        self.parse_annotations(ctx, self.interface)
        if ctx.extends:
            self.interface._extends = ctx.extends.text
        contextMap[ctx] = self.interface

    def exitInterfaceSymbol(self, ctx: TParser.InterfaceSymbolContext):
        self.interface = None

    def enterStructSymbol(self, ctx: TParser.StructSymbolContext):
        assert self.module
        name = ctx.name.text
        self.struct = Struct(name, self.module)
        self.parse_annotations(ctx, self.struct)
        contextMap[ctx] = self.struct

    def exitStructSymbol(self, ctx: TParser.StructSymbolContext):
        self.struct = None

    def enterEnumSymbol(self, ctx: TParser.EnumSymbolContext):
        assert self.module
        name = ctx.name.text
        self.enum = Enum(name, self.module)
        self.parse_annotations(ctx, self.enum)
        contextMap[ctx] = self.enum

    def exitEnumSymbol(self, ctx: TParser.EnumSymbolContext):
        self.enum = None
        self.enumCounter = 0

    def enterEnumTypeSymbol(self, ctx: TParser.EnumTypeSymbolContext):
        assert self.enum
        self.enumCounter = 0
        if ctx.isFlag:
            self.enum.is_enum = False
            self.enum.is_flag = True
            self.enumCounter = 1

    def exitEnumTypeSymbol(self, ctx: TParser.EnumTypeSymbolContext):
        pass

    def enterOperationSymbol(self, ctx: TParser.OperationSymbolContext):
        assert self.interface
        name = ctx.name.text
        self.operation = Operation(name, self.interface)
        modifier = ctx.operationModifierSymbol()
        if modifier:
            self.operation.is_const = bool(modifier.is_const)
        self.parse_annotations(ctx, self.operation)
        self.parse_type(ctx, self.operation.type)
        contextMap[ctx] = self.operation

    def exitOperationSymbol(self, ctx: TParser.OperationSymbolContext):
        self.operation = None

    def enterSignalSymbol(self, ctx: TParser.SignalSymbolContext):
        assert self.interface
        name = ctx.name.text
        self.signal = Signal(name, self.interface)
        self.parse_annotations(ctx, self.signal)
        contextMap[ctx] = self.signal

    def exitSignalSymbol(self, ctx: TParser.SignalSymbolContext):
        self.signal = None

    def enterOperationParameterSymbol(self, ctx: TParser.OperationParameterSymbolContext):
        name = ctx.name.text
        symbol = self.operation if self.operation else self.signal
        self.parameter = Parameter(name, symbol)
        contextMap[ctx] = self.parameter

    def exitOperationParameterSymbol(self, ctx: TParser.OperationParameterSymbolContext):
        self.parse_type(ctx, self.parameter.type)

    def enterPropertySymbol(self, ctx: TParser.PropertySymbolContext):
        assert self.interface
        name = ctx.name.text
        self.property = Property(name, self.interface)
        modifier = ctx.propertyModifierSymbol()

        if modifier:
            self.property.readonly = bool(modifier.is_readonly)
            self.property.const = bool(modifier.is_const)

        # if ctx.value:
        #     try:
        #         value = yaml.load(ctx.value.text, Loader=Loader)
        #         self.property._value = value
        #     except yaml.YAMLError as exc:
        #         click.secho(exc, fg='red')

        self.parse_annotations(ctx, self.property)
        self.parse_type(ctx, self.property.type)
        contextMap[ctx] = self.property

    def exitPropertySymbol(self, ctx: TParser.PropertySymbolContext):
        self.property = None

    def enterStructFieldSymbol(self, ctx: TParser.StructFieldSymbolContext):
        assert self.struct
        name = ctx.name.text
        self.field = Field(name, self.struct)
        self.parse_annotations(ctx, self.field)
        contextMap[ctx] = self.field

    def exitStructFieldSymbol(self, ctx: TParser.StructFieldSymbolContext):
        self.parse_type(ctx, self.field.type)
        self.field = None

    def enterEnumMemberSymbol(self, ctx: TParser.EnumMemberSymbolContext):
        assert self.enum
        name = ctx.name.text
        self.field = EnumMember(name, self.enum)
        value = self.enumCounter
        if ctx.intSymbol():
            value = int(ctx.intSymbol().value.text, 0)
        self.field.value = value
        self.parse_annotations(ctx, self.field)
        contextMap[ctx] = self.field
        if self.enum.is_flag:
            self.enumCounter <<= 1
        else:
            self.enumCounter += 1

    def exitEnumMemberSymbol(self, ctx: TParser.EnumMemberSymbolContext):
        self.field = None

    def enterImportSymbol(self, ctx: TParser.ImportSymbolContext):
        assert self.module
        self.check_support(EFeature.IMPORT)
        name = ctx.name.text
        version = ctx.version.text
        self.module._importMap[name] = '{0} {1}'.format(name, version)

    def exitImportSymbol(self, ctx: TParser.ImportSymbolContext):
        pass
