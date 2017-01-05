// Copyright (c) Pelagicore AB 2016
grammar T;


documentSymbol
    : headerSymbol definitionSymbol*
    ;

/**
module name;
import name;
*/
headerSymbol
    : moduleSymbol importSymbol*
    ;

importSymbol
    : 'import' name=IDENTIFIER version=VERSION ';'?
    ;

moduleSymbol
    : comment=DOCCOMMENT? tagSymbol? 'module' name=IDENTIFIER version=VERSION ';'?
    ;

definitionSymbol
    : interfaceSymbol
    | structSymbol
    | enumSymbol
    ;

interfaceSymbol
    : comment=DOCCOMMENT? tagSymbol? 'interface' name=IDENTIFIER '{' interfaceMemberSymbol* '}' ';'?
    ;

interfaceMemberSymbol
    : operationSymbol
    | propertySymbol
    ;

operationSymbol
    : comment=DOCCOMMENT?  tagSymbol? isEvent='event'? (typeSymbol | 'void') name=IDENTIFIER '(' operationParameterSymbol* ')' ';'?
    ;

propertySymbol
    : comment=DOCCOMMENT? tagSymbol? isReadOnly='readonly'? typeSymbol name=IDENTIFIER ';'?
    ;

operationParameterSymbol
    : typeSymbol name=IDENTIFIER ','?
    ;

tagSymbol
    : '@' name=IDENTIFIER '(' tagAttributeSymbol* ')'
    ;

tagAttributeSymbol
    : name=IDENTIFIER ('=' value=IDENTIFIER)?
    ;    

typeSymbol
    : primitiveTypeSymbol
    | complexTypeSymbol
    | listTypeSymbol
    | modelTypeSymbol
    ;

complexTypeSymbol
    : name=IDENTIFIER
    ;

primitiveTypeSymbol
    : name='bool'
    | name='int'
    | name='real'
    | name='string'
    | name='var'
    ;

listTypeSymbol
    : 'list' '<' valueType=typeSymbol '>'
    ;

modelTypeSymbol
    : 'model' '<' valueType=typeSymbol '>'
    ;

structSymbol
    : comment=DOCCOMMENT? tagSymbol? 'struct' name=IDENTIFIER '{' structFieldSymbol* '}' ';'?
    ;

structFieldSymbol
    : comment=DOCCOMMENT? tagSymbol? typeSymbol name=IDENTIFIER ';'?
    ;

enumSymbol
    : comment=DOCCOMMENT? tagSymbol? enumTypeSymbol name=IDENTIFIER '{' enumMemberSymbol* '}' ';'?
    ;

enumTypeSymbol
    : isEnum = 'enum'
    | isFlag = 'flag'
    ;

enumMemberSymbol
    : comment=DOCCOMMENT? tagSymbol? name=IDENTIFIER ('=' intSymbol)? ','?
    ;

intSymbol
    : value=INTCONSTANT
    | value=HEXCONSTANT
    ;

INTCONSTANT     : ('+' | '-')? '0'..'9'+;
HEXCONSTANT     : '0x' ('0'..'9' | 'a'..'f' | 'A'..'F')+;
IDENTIFIER      : [a-zA-Z_][a-zA-Z0-9_\.]*;
VERSION         : [0-9]'.'[0-9];
DOCCOMMENT      : '/*!' .*? '*/';
WHITESPACE      : [ \t\r\n]+ -> skip;
COMMENT         : '//' ~[\r\n]* -> skip;
MULTICOMM       : '/*' .*? '*/' -> skip;
