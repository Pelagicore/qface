# Copyright (c) Pelagicore AG 2016
import logging
from _operator import concat

from .parser.TListener import TListener
from .parser.TParser import TParser
from .domain import *


log = logging.getLogger(__name__)

# associates parser context to domain objects
contextMap = {}

class DomainListener(TListener):
    """The domain listener is called by the parser to fill the
       domain data struture. As a result a system is passed
       back"""
    def __init__(self, system):
        super(DomainListener, self).__init__()
        contextMap.clear()
        self.system = system or System()  # type:System
        self.module = None  # type:Module
        self.interface = None  # type:Interface
        self.struct = None  # type:Struct
        self.enum = None  # type:Enum
        self.enumCounter = 0 # int
        self.operation = None  # type:Operation
        self.parameter = None  # type:Parameter
        self.property = None  # type:Property
        self.member = None  # type:Member

    def parse_type(self, ctx, type: TypeSymbol):
        if not ctx.typeSymbol():
            # import pdb; pdb.set_trace()
            type.is_void = True
            type.name = 'void'
        else:
            if ctx.typeSymbol().primitiveTypeSymbol():
                ctxSymbol = ctx.typeSymbol().primitiveTypeSymbol()  # type:TParser.PrimitiveTypeSymbolContext
                type.is_primitive = True
                type.name = ctxSymbol.name.text
            elif ctx.typeSymbol().complexTypeSymbol():
                ctxSymbol = ctx.typeSymbol().complexTypeSymbol()  # type:TParser.ComplexTypeSymbolContext
                type.is_complex = True
                type.name = ctxSymbol.name.text
            elif ctx.typeSymbol().listTypeSymbol():
                ctxSymbol = ctx.typeSymbol().listTypeSymbol()  # type:TParser.ListTypeSymbolContext
                type.is_list = True
                type.name = 'list'
                type.nested = TypeSymbol("", type)
                self.parse_type(ctxSymbol, type.nested)
            elif ctx.typeSymbol().modelTypeSymbol():
                ctxSymbol = ctx.typeSymbol().modelTypeSymbol()  # type:TParser.ModelTypeSymbolContext
                type.is_model = True
                type.name = 'model'
                type.nested = TypeSymbol("", type)
                self.parse_type(ctxSymbol, type.nested)

    def parse_comment(self, ctx, symbol):
        if ctx.comment:
            comment = ctx.comment.text
            symbol.comment = comment


    def enterEveryRule(self, ctx):
        log.debug('enter ' + ctx.__class__.__name__)

    def exitEveryRule(self, ctx):
        log.debug('exit ' + ctx.__class__.__name__)

    def enterModuleSymbol(self, ctx: TParser.ModuleSymbolContext):
        assert self.system
        name = ctx.name.text
        self.module = Module(name, self.system)
        contextMap[ctx] = self.module

    def exitModuleSymbol(self, ctx: TParser.ModuleSymbolContext):
        pass

    def enterInterfaceSymbol(self, ctx: TParser.InterfaceSymbolContext):
        assert self.module
        name = ctx.name.text
        self.interface = Interface(name, self.module)
        self.parse_comment(ctx, self.interface)
        contextMap[ctx] = self.interface

    def exitInterfaceSymbol(self, ctx: TParser.InterfaceSymbolContext):
        self.interface = None

    def enterStructSymbol(self, ctx: TParser.StructSymbolContext):
        assert self.module
        name = ctx.name.text
        self.struct = Struct(name, self.module)
        self.parse_comment(ctx, self.struct)
        contextMap[ctx] = self.struct

    def exitStructSymbol(self, ctx: TParser.StructSymbolContext):
        self.struct = None

    def enterEnumSymbol(self, ctx: TParser.EnumSymbolContext):
        assert self.module
        name = ctx.name.text
        # import ipdb; ipdb.set_trace()
        self.enum = Enum(name, self.module)
        self.parse_comment(ctx, self.enum)
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
        is_event = bool(ctx.isEvent)
        self.operation = Operation(name, self.interface, is_event)
        self.parse_comment(ctx, self.operation)
        self.parse_type(ctx, self.operation.type)
        contextMap[ctx] = self.operation

    def exitOperationSymbol(self, ctx: TParser.OperationSymbolContext):
        self.operation = None

    def enterParameterSymbol(self, ctx: TParser.ParameterSymbolContext):
        name = ctx.name.text
        self.parameter = Parameter(name, self.operation)
        contextMap[ctx] = self.parameter

    def exitParameterSymbol(self, ctx: TParser.ParameterSymbolContext):
        self.parse_type(ctx, self.parameter.type)

    def enterPropertySymbol(self, ctx: TParser.PropertySymbolContext):
        assert self.interface
        name = ctx.name.text
        self.property = Property(name, self.interface)
        self.property.is_readonly = bool(ctx.isReadOnly)
        self.parse_comment(ctx, self.property)
        self.parse_type(ctx, self.property.type)
        contextMap[ctx] = self.property

    def exitPropertySymbol(self, ctx: TParser.PropertySymbolContext):
        self.property = None

    def enterStructMemberSymbol(self, ctx: TParser.StructMemberSymbolContext):
        assert self.struct
        name = ctx.name.text
        self.member = Member(name, self.struct)
        contextMap[ctx] = self.member

    def exitStructMemberSymbol(self, ctx: TParser.StructMemberSymbolContext):
        self.parse_type(ctx, self.member.type)
        self.member = None

    def enterEnumMemberSymbol(self, ctx: TParser.EnumMemberSymbolContext):
        assert self.enum
        name = ctx.name.text
        self.member = EnumMember(name, self.enum)
        value = self.enumCounter
        if ctx.intSymbol():
            value = int(ctx.intSymbol().value.text, 0)
        self.member.value = value
        contextMap[ctx] = self.member
        # import ipdb; ipdb.set_trace()
        if self.enum.is_flag:
            self.enumCounter <<= 1
        else:
            self.enumCounter += 1

    def exitEnumMemberSymbol(self, ctx: TParser.EnumMemberSymbolContext):
        self.member = None

    def enterImportSymbol(self, ctx: TParser.ImportSymbolContext):
        assert self.module
        name = ctx.name.text
        self.module._importMap[name] = None

    def exitImportSymbol(self, ctx: TParser.ImportSymbolContext):
        pass

