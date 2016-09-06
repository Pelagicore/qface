{# Copyright (c) Pelagicore AG 2016 #}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include <{{interface|lower}}.h>

#include <QtQml>

{% set class = 'Qml{0}'.format(interface) %}

QObject* {{interface|lower}}_singletontype_provider(QQmlEngine*, QJSEngine*)
{
      return new {{class}}();
}


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
    qmlRegisterSingletonType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{interface}}", {{interface|lower}}_singletontype_provider);
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
{{operation.type}} {{class}}::{{operation}}()
{
}

{% endfor %}
