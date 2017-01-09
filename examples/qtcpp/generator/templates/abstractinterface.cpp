{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'QmlAbstract{0}'.format(interface) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "{{class|lower}}.h"

#include <QtQml>

{{interface.comment}}
{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{% for property in interface.properties %}
    , m_{{property}}({{property|defaultValue}})
{% endfor %}
{
{% for property in interface.properties %}
{% if property.type.is_model %}
    m_{{property}} = new {{property.type.nested}}Model(this);
{% endif %}
{% endfor %}
}

{% for property in interface.properties %}
void {{class}}::set{{property|upperfirst}}({{ property|parameterType }})
{
    if(m_{{property}} == {{property}}) {
        return;
    }
    m_{{property}} = {{property}};
    emit {{property}}Changed();
}

{{property|returnType}} {{class}}::{{property}}() const
{
    return m_{{property}};
}
{% endfor %}

{%- for operation in interface.operations %}    
{{operation|returnType}} {{class}}::{{operation}}({{operation.parameters|map('parameterType')|join(', ')}})
{
    {% for parameter in operation.parameters %}
    Q_UNUSED({{parameter.name}});
    {% endfor %}
    qWarning() << "{{class}}::{{operation}}(...) not implemented";
    return {{operation|defaultValue}};
}
{% endfor %}

