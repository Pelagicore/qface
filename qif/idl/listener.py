import logging
from .parser.TListener import TListener
from .parser.TParser import TParser
from .domain import *


log = logging.getLogger(__name__)


class DomainListener(TListener):
    def __init__(self, system):
        super(DomainListener, self).__init__()
        self.system = system or System()  # type:System
        self.package = None  # type:Package
        self.service = None  # type:Service
        self.struct = None  # type:Struct
        self.enum = None  # type:Enum
        self.operation = None  # type:Operation
        self.parameter = None  # type:Parameter
        self.attribute = None  # type:Attribute
        self.member = None  # type:Member

    def parse_type(self, ctx, symbol: TypedSymbol):
        if not ctx.typeSymbol():
            # import pdb; pdb.set_trace()
            symbol.type.is_void = True
            symbol.type.name = 'void'
        else:
            if ctx.typeSymbol().primitiveTypeSymbol():
                ctxSymbol = ctx.typeSymbol().primitiveTypeSymbol()  # type:TParser.PrimitiveTypeSymbolContext
                symbol.type.is_primitive = True
                symbol.type.name = ctxSymbol.name.text
            if ctx.typeSymbol().complexTypeSymbol():
                ctxSymbol = ctx.typeSymbol().complexTypeSymbol()  # type:TParser.ComplexTypeSymbolContext
                symbol.type.is_complex = True
                symbol.type.name = ctxSymbol.name.text

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

    def enterServiceSymbol(self, ctx: TParser.ServiceSymbolContext):
        assert self.package
        name = ctx.name.text
        self.service = Service(name, self.package)
        self.parse_comment(ctx, self.service)

    def exitServiceSymbol(self, ctx: TParser.ServiceSymbolContext):
        self.service = None

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
        self.enum = Enum(name, self.package)
        self.parse_comment(ctx, self.enum)

    def exitEnumSymbol(self, ctx: TParser.EnumSymbolContext):
        self.enum = None

    def enterOperationSymbol(self, ctx: TParser.OperationSymbolContext):
        assert self.service
        name = ctx.name.text
        is_event = bool(ctx.isEvent)
        self.operation = Operation(name, self.service, is_event)
        self.parse_comment(ctx, self.operation)
        self.parse_type(ctx, self.operation)

    def exitOperationSymbol(self, ctx: TParser.OperationSymbolContext):
        self.operation = None

    def enterParameterSymbol(self, ctx: TParser.ParameterSymbolContext):
        name = ctx.name.text
        self.parameter = Parameter(name, self.operation)

    def exitParameterSymbol(self, ctx: TParser.ParameterSymbolContext):
        self.parse_type(ctx, self.parameter)

    def enterAttributeSymbol(self, ctx: TParser.AttributeSymbolContext):
        assert self.service
        name = ctx.name.text
        self.attribute = Attribute(name, self.service)
        self.attribute.is_readonly = bool(ctx.isReadOnly)
        self.parse_comment(ctx, self.attribute)
        self.parse_type(ctx, self.attribute)

    def exitAttributeSymbol(self, ctx: TParser.AttributeSymbolContext):
        self.attribute = None

    def enterStructMemberSymbol(self, ctx: TParser.StructMemberSymbolContext):
        assert self.struct
        name = ctx.name.text
        self.member = Member(name, self.struct)

    def exitStructMemberSymbol(self, ctx: TParser.StructMemberSymbolContext):
        self.parse_type(ctx, self.member)
        self.member = None

    def enterEnumMemberSymbol(self, ctx: TParser.EnumMemberSymbolContext):
        assert self.enum
        name = ctx.name.text
        self.member = EnumMember(name, self.enum)
        self.member.value = int(ctx.intSymbol().value.text, 0)

    def exitEnumMemberSymbol(self, ctx: TParser.EnumMemberSymbolContext):
        self.member = None

    def enterImportSymbol(self, ctx:TParser.ImportSymbolContext):
        assert self.package
        name = ctx.name.text
        self.package.importMap[name] = None


    def exitImportSymbol(self, ctx:TParser.ImportSymbolContext):
        pass






