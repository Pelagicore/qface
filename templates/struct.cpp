/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include <{{struct|lower}}.h>

{{struct.comment}}
{{struct}}::{{struct}}()
{    
}

{{struct}}::~{{struct}}()
{
}
{% for member in struct.members %}

void {{struct}}::set{{member|upperfirst}}({{ member|parameterType }})
{
    m_{{member}} = {{member}};
}
{{member.comment}}
{{member|returnType}} {{struct}}::{{member}}() const
{
    return m_{{member}};
}
{% endfor %}

