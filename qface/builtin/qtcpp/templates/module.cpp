{# Copyright (c) Pelagicore AB 2016 #}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/
{% set class = 'Qml{0}Module'.format(module.module_name) %}


#include "{{class|lower}}.h"

#include <QtQml>

QObject* {{class|lower}}_singletontype_provider(QQmlEngine*, QJSEngine*)
{
    return new {{class}}();
}

{{class}}::{{class}}(QObject *parent)
    : QObject(parent)
{
}

{% for struct in module.structs %}
Qml{{struct}} {{class}}::create{{struct}}()
{
    return Qml{{struct}}();
}
{% endfor %}

void {{class}}::registerTypes()
{
    {% for struct in module.structs %}
    qRegisterMetaType<Qml{{struct}}>();
    {% endfor %}
    {% for enum in module.enums %}
    qRegisterMetaType<{{class}}::{{enum}}>();
    {% endfor %}
}

void {{class}}::registerQmlTypes(const QString& uri, int majorVersion, int minorVersion)
{
    {% for struct in module.structs %}
    qmlRegisterUncreatableType<Qml{{struct}}Model>(uri.toLatin1(), majorVersion, minorVersion, "{{struct}}Model", "Model can not be instantiated from QML");
    {% endfor %}
    qmlRegisterSingletonType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{module.module_name}}Module", {{class|lower}}_singletontype_provider);
}
