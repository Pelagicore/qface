/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include <{{service|lower}}.h>

#include <QtQml>

{% set class = 'Qml{0}'.format(service) %}

QObject* {{service|lower}}_singletontype_provider(QQmlEngine*, QJSEngine*)
{
      return new {{class}}();
}


{{service.comment}}
{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{
{% for attribute in service.attributes %}
{% if attribute.type.is_model %}
    m_{{attribute}} = new {{attribute.type.nested}}Model(this);
{% endif %}
{% endfor %}
}

void {{class}}::registerQmlTypes(const QString& uri, int majorVersion, int minorVersion)
{
    qmlRegisterSingletonType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{service}}", {{service|lower}}_singletontype_provider);
}

{% for attribute in service.attributes %}
void {{class}}::set{{attribute|upperfirst}}({{ attribute|parameterType }})
{
    if(m_{{attribute}} == {{attribute}}) {
        return;
    }
    m_{{attribute}} = {{attribute}};
    emit {{attribute}}Changed({{attribute}});
}

{{attribute|returnType}} {{class}}::{{attribute}}() const
{
    return m_{{attribute}};
}

{% endfor %}

{% for operation in service.operations %}
{{operation.comment}}
{{operation.type}} {{class}}::{{operation}}()
{
}

{% endfor %}
