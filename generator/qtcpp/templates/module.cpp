{% from 'helper.tpl' import module %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/
{% set module = module(package) %}
{% set class = 'Qml{0}'.format(module) %}


#include "{{ module|lower }}.h"

#include <QtQml>

QObject* {{module|lower}}_singletontype_provider(QQmlEngine*, QJSEngine*)
{
      return new {{class}}();
}

{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{
}

{% for struct in package.structs %}
{{struct}} {{class}}::create{{struct}}()
{
    return {{struct}}();
}
{% endfor %}

void {{class}}::registerTypes()
{
    {% for struct in package.structs %}
    qRegisterMetaType<{{struct}}>();
    {% endfor %}
}

void {{class}}::registerQmlTypes(const QString& uri, int majorVersion, int minorVersion)
{
    {% for struct in package.structs %}
    qmlRegisterUncreatableType<{{struct}}Model>(uri.toLatin1(), majorVersion, minorVersion, "{{struct}}Model", "Model can not be instantiated from QML");
    {% endfor %}
    qmlRegisterSingletonType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{module}}", {{module|lower}}_singletontype_provider);
}
