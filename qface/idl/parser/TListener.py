# Generated from T.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .TParser import TParser
else:
    from TParser import TParser

# This class defines a complete listener for a parse tree produced by TParser.
class TListener(ParseTreeListener):

    # Enter a parse tree produced by TParser#documentSymbol.
    def enterDocumentSymbol(self, ctx:TParser.DocumentSymbolContext):
        pass

    # Exit a parse tree produced by TParser#documentSymbol.
    def exitDocumentSymbol(self, ctx:TParser.DocumentSymbolContext):
        pass


    # Enter a parse tree produced by TParser#headerSymbol.
    def enterHeaderSymbol(self, ctx:TParser.HeaderSymbolContext):
        pass

    # Exit a parse tree produced by TParser#headerSymbol.
    def exitHeaderSymbol(self, ctx:TParser.HeaderSymbolContext):
        pass


    # Enter a parse tree produced by TParser#importSymbol.
    def enterImportSymbol(self, ctx:TParser.ImportSymbolContext):
        pass

    # Exit a parse tree produced by TParser#importSymbol.
    def exitImportSymbol(self, ctx:TParser.ImportSymbolContext):
        pass


    # Enter a parse tree produced by TParser#moduleSymbol.
    def enterModuleSymbol(self, ctx:TParser.ModuleSymbolContext):
        pass

    # Exit a parse tree produced by TParser#moduleSymbol.
    def exitModuleSymbol(self, ctx:TParser.ModuleSymbolContext):
        pass


    # Enter a parse tree produced by TParser#definitionSymbol.
    def enterDefinitionSymbol(self, ctx:TParser.DefinitionSymbolContext):
        pass

    # Exit a parse tree produced by TParser#definitionSymbol.
    def exitDefinitionSymbol(self, ctx:TParser.DefinitionSymbolContext):
        pass


    # Enter a parse tree produced by TParser#interfaceSymbol.
    def enterInterfaceSymbol(self, ctx:TParser.InterfaceSymbolContext):
        pass

    # Exit a parse tree produced by TParser#interfaceSymbol.
    def exitInterfaceSymbol(self, ctx:TParser.InterfaceSymbolContext):
        pass


    # Enter a parse tree produced by TParser#interfaceMemberSymbol.
    def enterInterfaceMemberSymbol(self, ctx:TParser.InterfaceMemberSymbolContext):
        pass

    # Exit a parse tree produced by TParser#interfaceMemberSymbol.
    def exitInterfaceMemberSymbol(self, ctx:TParser.InterfaceMemberSymbolContext):
        pass


    # Enter a parse tree produced by TParser#operationSymbol.
    def enterOperationSymbol(self, ctx:TParser.OperationSymbolContext):
        pass

    # Exit a parse tree produced by TParser#operationSymbol.
    def exitOperationSymbol(self, ctx:TParser.OperationSymbolContext):
        pass


    # Enter a parse tree produced by TParser#operationModifierSymbol.
    def enterOperationModifierSymbol(self, ctx:TParser.OperationModifierSymbolContext):
        pass

    # Exit a parse tree produced by TParser#operationModifierSymbol.
    def exitOperationModifierSymbol(self, ctx:TParser.OperationModifierSymbolContext):
        pass


    # Enter a parse tree produced by TParser#signalSymbol.
    def enterSignalSymbol(self, ctx:TParser.SignalSymbolContext):
        pass

    # Exit a parse tree produced by TParser#signalSymbol.
    def exitSignalSymbol(self, ctx:TParser.SignalSymbolContext):
        pass


    # Enter a parse tree produced by TParser#propertySymbol.
    def enterPropertySymbol(self, ctx:TParser.PropertySymbolContext):
        pass

    # Exit a parse tree produced by TParser#propertySymbol.
    def exitPropertySymbol(self, ctx:TParser.PropertySymbolContext):
        pass


    # Enter a parse tree produced by TParser#propertyModifierSymbol.
    def enterPropertyModifierSymbol(self, ctx:TParser.PropertyModifierSymbolContext):
        pass

    # Exit a parse tree produced by TParser#propertyModifierSymbol.
    def exitPropertyModifierSymbol(self, ctx:TParser.PropertyModifierSymbolContext):
        pass


    # Enter a parse tree produced by TParser#operationParameterSymbol.
    def enterOperationParameterSymbol(self, ctx:TParser.OperationParameterSymbolContext):
        pass

    # Exit a parse tree produced by TParser#operationParameterSymbol.
    def exitOperationParameterSymbol(self, ctx:TParser.OperationParameterSymbolContext):
        pass


    # Enter a parse tree produced by TParser#tagSymbol.
    def enterTagSymbol(self, ctx:TParser.TagSymbolContext):
        pass

    # Exit a parse tree produced by TParser#tagSymbol.
    def exitTagSymbol(self, ctx:TParser.TagSymbolContext):
        pass


    # Enter a parse tree produced by TParser#tagAttributeSymbol.
    def enterTagAttributeSymbol(self, ctx:TParser.TagAttributeSymbolContext):
        pass

    # Exit a parse tree produced by TParser#tagAttributeSymbol.
    def exitTagAttributeSymbol(self, ctx:TParser.TagAttributeSymbolContext):
        pass


    # Enter a parse tree produced by TParser#typeSymbol.
    def enterTypeSymbol(self, ctx:TParser.TypeSymbolContext):
        pass

    # Exit a parse tree produced by TParser#typeSymbol.
    def exitTypeSymbol(self, ctx:TParser.TypeSymbolContext):
        pass


    # Enter a parse tree produced by TParser#complexTypeSymbol.
    def enterComplexTypeSymbol(self, ctx:TParser.ComplexTypeSymbolContext):
        pass

    # Exit a parse tree produced by TParser#complexTypeSymbol.
    def exitComplexTypeSymbol(self, ctx:TParser.ComplexTypeSymbolContext):
        pass


    # Enter a parse tree produced by TParser#primitiveTypeSymbol.
    def enterPrimitiveTypeSymbol(self, ctx:TParser.PrimitiveTypeSymbolContext):
        pass

    # Exit a parse tree produced by TParser#primitiveTypeSymbol.
    def exitPrimitiveTypeSymbol(self, ctx:TParser.PrimitiveTypeSymbolContext):
        pass


    # Enter a parse tree produced by TParser#listTypeSymbol.
    def enterListTypeSymbol(self, ctx:TParser.ListTypeSymbolContext):
        pass

    # Exit a parse tree produced by TParser#listTypeSymbol.
    def exitListTypeSymbol(self, ctx:TParser.ListTypeSymbolContext):
        pass


    # Enter a parse tree produced by TParser#mapTypeSymbol.
    def enterMapTypeSymbol(self, ctx:TParser.MapTypeSymbolContext):
        pass

    # Exit a parse tree produced by TParser#mapTypeSymbol.
    def exitMapTypeSymbol(self, ctx:TParser.MapTypeSymbolContext):
        pass


    # Enter a parse tree produced by TParser#modelTypeSymbol.
    def enterModelTypeSymbol(self, ctx:TParser.ModelTypeSymbolContext):
        pass

    # Exit a parse tree produced by TParser#modelTypeSymbol.
    def exitModelTypeSymbol(self, ctx:TParser.ModelTypeSymbolContext):
        pass


    # Enter a parse tree produced by TParser#structSymbol.
    def enterStructSymbol(self, ctx:TParser.StructSymbolContext):
        pass

    # Exit a parse tree produced by TParser#structSymbol.
    def exitStructSymbol(self, ctx:TParser.StructSymbolContext):
        pass


    # Enter a parse tree produced by TParser#structFieldSymbol.
    def enterStructFieldSymbol(self, ctx:TParser.StructFieldSymbolContext):
        pass

    # Exit a parse tree produced by TParser#structFieldSymbol.
    def exitStructFieldSymbol(self, ctx:TParser.StructFieldSymbolContext):
        pass


    # Enter a parse tree produced by TParser#enumSymbol.
    def enterEnumSymbol(self, ctx:TParser.EnumSymbolContext):
        pass

    # Exit a parse tree produced by TParser#enumSymbol.
    def exitEnumSymbol(self, ctx:TParser.EnumSymbolContext):
        pass


    # Enter a parse tree produced by TParser#enumTypeSymbol.
    def enterEnumTypeSymbol(self, ctx:TParser.EnumTypeSymbolContext):
        pass

    # Exit a parse tree produced by TParser#enumTypeSymbol.
    def exitEnumTypeSymbol(self, ctx:TParser.EnumTypeSymbolContext):
        pass


    # Enter a parse tree produced by TParser#enumMemberSymbol.
    def enterEnumMemberSymbol(self, ctx:TParser.EnumMemberSymbolContext):
        pass

    # Exit a parse tree produced by TParser#enumMemberSymbol.
    def exitEnumMemberSymbol(self, ctx:TParser.EnumMemberSymbolContext):
        pass


    # Enter a parse tree produced by TParser#intSymbol.
    def enterIntSymbol(self, ctx:TParser.IntSymbolContext):
        pass

    # Exit a parse tree produced by TParser#intSymbol.
    def exitIntSymbol(self, ctx:TParser.IntSymbolContext):
        pass


