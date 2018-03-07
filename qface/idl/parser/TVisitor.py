# Generated from T.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TParser import TParser
else:
    from TParser import TParser

# This class defines a complete generic visitor for a parse tree produced by TParser.

class TVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TParser#documentSymbol.
    def visitDocumentSymbol(self, ctx:TParser.DocumentSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#headerSymbol.
    def visitHeaderSymbol(self, ctx:TParser.HeaderSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#importSymbol.
    def visitImportSymbol(self, ctx:TParser.ImportSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#moduleSymbol.
    def visitModuleSymbol(self, ctx:TParser.ModuleSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#definitionSymbol.
    def visitDefinitionSymbol(self, ctx:TParser.DefinitionSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#interfaceSymbol.
    def visitInterfaceSymbol(self, ctx:TParser.InterfaceSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#interfaceMemberSymbol.
    def visitInterfaceMemberSymbol(self, ctx:TParser.InterfaceMemberSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#operationSymbol.
    def visitOperationSymbol(self, ctx:TParser.OperationSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#operationModifierSymbol.
    def visitOperationModifierSymbol(self, ctx:TParser.OperationModifierSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#signalSymbol.
    def visitSignalSymbol(self, ctx:TParser.SignalSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#propertySymbol.
    def visitPropertySymbol(self, ctx:TParser.PropertySymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#propertyModifierSymbol.
    def visitPropertyModifierSymbol(self, ctx:TParser.PropertyModifierSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#operationParameterSymbol.
    def visitOperationParameterSymbol(self, ctx:TParser.OperationParameterSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#tagSymbol.
    def visitTagSymbol(self, ctx:TParser.TagSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#tagAttributeSymbol.
    def visitTagAttributeSymbol(self, ctx:TParser.TagAttributeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#typeSymbol.
    def visitTypeSymbol(self, ctx:TParser.TypeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#complexTypeSymbol.
    def visitComplexTypeSymbol(self, ctx:TParser.ComplexTypeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#primitiveTypeSymbol.
    def visitPrimitiveTypeSymbol(self, ctx:TParser.PrimitiveTypeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#listTypeSymbol.
    def visitListTypeSymbol(self, ctx:TParser.ListTypeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#mapTypeSymbol.
    def visitMapTypeSymbol(self, ctx:TParser.MapTypeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#modelTypeSymbol.
    def visitModelTypeSymbol(self, ctx:TParser.ModelTypeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#structSymbol.
    def visitStructSymbol(self, ctx:TParser.StructSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#structFieldSymbol.
    def visitStructFieldSymbol(self, ctx:TParser.StructFieldSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#enumSymbol.
    def visitEnumSymbol(self, ctx:TParser.EnumSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#enumTypeSymbol.
    def visitEnumTypeSymbol(self, ctx:TParser.EnumTypeSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#enumMemberSymbol.
    def visitEnumMemberSymbol(self, ctx:TParser.EnumMemberSymbolContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TParser#intSymbol.
    def visitIntSymbol(self, ctx:TParser.IntSymbolContext):
        return self.visitChildren(ctx)



del TParser