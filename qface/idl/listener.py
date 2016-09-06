# Copyright (c) Pelagicore AG 2016
import logging
from .parser.TListener import TListener
from .parser.TParser import TParser
from .domain import *


log = logging.getLogger(__name__)


class DomainListener(TListener):
    """The domain listener is called by the parser to fill the
       domain data struture. As a result a system is passed
       back"""
    def __init__(self, system):
        super(DomainListener, self).__init__()
        self.system = system or System()  # type:System
        self.package = None  # type:Package
        self.interface = None  # type:Interface
        self.struct = None  # type:Struct
        self.enum = None  # type:Enum
        self.operation = None  # type:Operation
        self.parameter = None  # type:Parameter
        self.attribute = None  # type:Attribute
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

    def enterPackageSymbol(self, ctx: TParser.PackageSymbolContext):
        assert self.system
        name = ctx.name.text
        self.package = Package(name, self.system)

    def exitPackageSymbol(self, ctx: TParser.PackageSymbolContext):
        pass

    def enterInterfaceSymbol(self, ctx: TParser.InterfaceSymbolContext):
        assert self.package
        name = ctx.name.text
        self.interface = Interface(name, self.package)
        self.parse_comment(ctx, self.interface)

    def exitInterfaceSymbol(self, ctx: TParser.InterfaceSymbolContext):
        self.interface = None

    def enterStructSymbol(self, ctx: TParser.StructSymbolContext):
        assert self.package
        name = ctx.name.text
        self.struct = Struct(name, self.package)
        self.parse_comment(ctx, self.struct)

    def exitStructSymbol(self, ctx: TParser.StructSymbolContext):
        self.struct = None

    def enterEnumSymbol(self, ctx: TParser.EnumSymbolContext):
        assert self.package
        name = ctx.name.text
        # import ipdb; ipdb.set_trace()
        self.enum = Enum(name, self.package)
        self.parse_comment(ctx, self.enum)

    def exitEnumSymbol(self, ctx: TParser.EnumSymbolContext):
        self.enum = None

    def enterEnumTypeSymbol(self, ctx: TParser.EnumTypeSymbolContext):
        assert self.enum
        if ctx.isFlag:
            self.enum.is_enum = False
            self.enum.is_flag = True

    def exitEnumTypeSymbol(self, ctx: TParser.EnumTypeSymbolContext):
        pass

    def enterOperationSymbol(self, ctx: TParser.OperationSymbolContext):
        assert self.interface
        name = ctx.name.text
        is_event = bool(ctx.isEvent)
        self.operation = Operation(name, self.interface, is_event)
        self.parse_comment(ctx, self.operation)
        self.parse_type(ctx, self.operation.type)

    def exitOperationSymbol(self, ctx: TParser.OperationSymbolContext):
        self.operation = None

    def enterParameterSymbol(self, ctx: TParser.ParameterSymbolContext):
        name = ctx.name.text
        self.parameter = Parameter(name, self.operation)

    def exitParameterSymbol(self, ctx: TParser.ParameterSymbolContext):
        self.parse_type(ctx, self.parameter.type)

    def enterAttributeSymbol(self, ctx: TParser.AttributeSymbolContext):
        assert self.interface
        name = ctx.name.text
        self.attribute = Attribute(name, self.interface)
        self.attribute.is_readonly = bool(ctx.isReadOnly)
        self.parse_comment(ctx, self.attribute)
        self.parse_type(ctx, self.attribute.type)

    def exitAttributeSymbol(self, ctx: TParser.AttributeSymbolContext):
        self.attribute = None

    def enterStructMemberSymbol(self, ctx: TParser.StructMemberSymbolContext):
        assert self.struct
        name = ctx.name.text
        self.member = Member(name, self.struct)

    def exitStructMemberSymbol(self, ctx: TParser.StructMemberSymbolContext):
        self.parse_type(ctx, self.member.type)
        self.member = None

    def enterEnumMemberSymbol(self, ctx: TParser.EnumMemberSymbolContext):
        assert self.enum
        name = ctx.name.text
        self.member = EnumMember(name, self.enum)
        self.member.value = int(ctx.intSymbol().value.text, 0)
        # import ipdb; ipdb.set_trace()

    def exitEnumMemberSymbol(self, ctx: TParser.EnumMemberSymbolContext):
        self.member = None

    def enterImportSymbol(self, ctx:TParser.ImportSymbolContext):
        assert self.package
        name = ctx.name.text
        self.package.importMap[name] = None


    def exitImportSymbol(self, ctx:TParser.ImportSymbolContext):
        pass






