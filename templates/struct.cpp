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
        {%- for member in struct.members %}{{ ampersand() }}
        m_{{member}} == other.m_{{member}}
        {%- endfor %} );
}

