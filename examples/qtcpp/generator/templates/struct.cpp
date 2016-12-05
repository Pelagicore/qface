{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}'.format(struct) %}
{% set ampersand = joiner(" &&") %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "{{class|lower}}.h"


{{struct.comment}}

bool {{class}}::operator==(const {{class}} &other) const
{
    return (
        {%- for field in struct.fields %}{{ ampersand() }}
        m_{{field}} == other.m_{{field}}
        {%- endfor %} );
}

