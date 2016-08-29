grammar T;


documentSymbol
    : headerSymbol definitionSymbol*
    ;

/**
package name;
import name;
*/
headerSymbol
    : packageSymbol importSymbol*
    ;

importSymbol
    : 'import' name=IDENTIFIER ';'
    ;

packageSymbol
    : comment=DOCCOMMENT? 'package' name=IDENTIFIER ';'
    ;

definitionSymbol
    : serviceSymbol
    | structSymbol
    | enumSymbol
    ;

serviceSymbol
    : comment=DOCCOMMENT? 'service' name=IDENTIFIER '{' memberSymbol* '}'
    ;

memberSymbol
    : operationSymbol
    | attributeSymbol
    ;

operationSymbol
    : comment=DOCCOMMENT? isEvent='event'? (typeSymbol | 'void') name=IDENTIFIER '(' parameterSymbol* ')' ';'
    ;

attributeSymbol
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
IDENTIFIER      : [a-zA-Z0-9_][a-zA-Z0-9_\.]*;
DOCCOMMENT      : '/*!' .*? '*/';
WHITESPACE      : [ \t\r\n]+ -> skip;
COMMENT         : '//' ~[\r\n]* -> skip;
MULTICOMM       : '/*' .*? '*/' -> skip;
