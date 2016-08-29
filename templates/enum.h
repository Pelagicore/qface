/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#pragma once

#include <QtCore>

{% set comma = joiner(",") %}

class {{enum}} : public QObject
{
    Q_OBJECT
public:
    enum {{enum}}Enum { 
        {%- for member in enum.members -%}
        {{ comma() }}
        {{member.name}} = {{member.value}}
        {%- endfor %}        
    };
    Q_ENUM({{enum}}Enum)

    {{enum}}(QObject *parent=0);
};
