{# Copyright (c) Pelagicore AB 2016 #}
{% set ampersand = joiner(" &&") %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include <{{struct|lower}}.h>


{{struct.comment}}

bool {{struct}}::operator==(const {{struct}} &other) const
{
    return (
        {%- for field in struct.fields %}{{ ampersand() }}
        m_{{field}} == other.m_{{field}}
        {%- endfor %} );
}

