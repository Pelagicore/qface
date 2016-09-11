// Copyright (c) Pelagicore AG 2016
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
    : 'import' name=IDENTIFIER version=VERSION ';'
    ;

moduleSymbol
    : comment=DOCCOMMENT? 'module' name=IDENTIFIER ';'
    ;

definitionSymbol
    : interfaceSymbol
    | structSymbol
    | enumSymbol
    ;

interfaceSymbol
    : comment=DOCCOMMENT? 'interface' name=IDENTIFIER '{' memberSymbol* '}'
    ;

memberSymbol
    : operationSymbol
    | propertySymbol
    ;

operationSymbol
    : comment=DOCCOMMENT? isEvent='event'? (typeSymbol | 'void') name=IDENTIFIER '(' parameterSymbol* ')' ';'
    ;

propertySymbol
    : comment=DOCCOMMENT? isReadOnly='readonly'? typeSymbol name=IDENTIFIER ';'
    ;

parameterSymbol
    : typeSymbol name=IDENTIFIER ','?
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
    ;

listTypeSymbol
    : 'list' '<' valueType=typeSymbol '>'
    ;

modelTypeSymbol
    : 'model' '<' valueType=typeSymbol '>'
    ;

structSymbol
    : comment=DOCCOMMENT? 'struct' name=IDENTIFIER '{' structMemberSymbol* '}'
    ;

structMemberSymbol
    : comment=DOCCOMMENT? typeSymbol name=IDENTIFIER ';'?
    ;

enumSymbol
    : comment=DOCCOMMENT? enumTypeSymbol name=IDENTIFIER '{' enumMemberSymbol* '}'
    ;

enumTypeSymbol
    : isEnum = 'enum'
    | isFlag = 'flag'
    ;

enumMemberSymbol
    : comment=DOCCOMMENT? name=IDENTIFIER '=' intSymbol ','?
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
