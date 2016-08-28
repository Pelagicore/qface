{%- macro parameterType(symbol) -%}
    {%- if symbol.type.is_void or symbol.type.is_primitive -%}
        {{ symbol.type }} {{symbol}}
    {%- else -%}
        const {{ symbol.type }} &{{symbol}}
    {%- endif -%}
{%- endmacro -%}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include <{{service|lower}}.h>

{{service.comment}}
{{service}}::{{service}}(QObject *parent)
    : QObject(parent)
{
}

{% for attribute in service.attributes %}
void {{service}}::set{{attribute|upperfirst}}({{ attribute|parameterType }})
{
    if(m_{{attribute}} == {{attribute}}) {
        return;
    }
    m_{{attribute}} = {{attribute}};
    emit {{attribute}}Changed({{attribute}});
}

{{attribute|returnType}} {{service}}::{{attribute}}() const
{
    return m_{{attribute}};
}

{% endfor %}

{% for operation in service.operations %}
{{operation.comment}}
{{operation.type}} {{service}}::{{operation}}()
{
}

{% endfor %}
