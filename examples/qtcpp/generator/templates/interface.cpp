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
{
{% for property in interface.properties %}
{% if property.type.is_model %}
    m_{{property}} = new {{property.type.nested}}Model(this);
{% endif %}
{% endfor %}
}

void {{class}}::registerQmlTypes(const QString& uri, int majorVersion, int minorVersion)
{
    qmlRegisterType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{interface}}");
}

{% for property in interface.properties %}
void {{class}}::set{{property|upperfirst}}({{ property|parameterType }})
{
    if(m_{{property}} == {{property}}) {
        return;
    }
    m_{{property}} = {{property}};
    emit {{property}}Changed({{property}});
}

{{property|returnType}} {{class}}::{{property}}() const
{
    return m_{{property}};
}

{% endfor %}

{% for operation in interface.operations %}
{{operation.comment}}
{{operation|returnType}} {{class}}::{{operation}}({{operation.parameters|map('parameterType')|join(', ')}})
{
    qWarning() << "Not implemented: {{class}}::{{operation}}(...)";
}
{% endfor %}
