{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'QmlAbstract{0}'.format(interface) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "{{class|lower}}.h"

#include <QtQml>

/*!
   \qmltype {{interface}}
   \inqmlmodule {{module}}
{% with doc = interface.comment|parse_doc %}
   \brief {{doc.brief}}

   {{doc.description}}
{% endwith %}
*/
{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{% for property in interface.properties %}
    , m_{{property}}({{property|defaultValue}})
{% endfor %}
{
}


{{class}}::~{{class}}()
{
}

{% for property in interface.properties %}
/*!
   \qmlproperty {{property.type}} {{interface}}::{{property}}
{% with doc = property.comment|parse_doc %}
   \brief {{doc.brief}}

   {{doc.description}}
{% endwith %}
*/

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
/*!
   \qmlmethod {{operation.type}} {{interface}}::{{operation}}({{operation.parameters|map('parameterType')|join(', ')}})
{% with doc = operation.comment|parse_doc %}
   \brief {{doc.brief}}
   {{doc.description}}
{% endwith %}
*/
{{operation|returnType}} {{class}}::{{operation}}({{operation.parameters|map('parameterType')|join(', ')}})
{
    {% for parameter in operation.parameters %}
    Q_UNUSED({{parameter.name}});
    {% endfor %}
    qWarning() << "{{class}}::{{operation}}(...) not implemented";
    return {{operation|defaultValue}};
}
{% endfor %}


