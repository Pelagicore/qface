{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}'.format(interface) %}
/*
 * This is a preserved file and can be edited.
 * All changes will not be override.
 */

#include "{{class|lower}}.h"

#include <QtQml>

QObject* {{class|lower}}_singletontype_provider(QQmlEngine*, QJSEngine*)
{
      return new {{class}}();
}


{{interface.comment}}
{{class}}::{{class}}(QObject *parent)
    : QmlAbstract{{interface}}(parent)
{
}

{{class}}::~{{class}}()
{
}

void {{class}}::registerQmlTypes(const QString& uri, int majorVersion, int minorVersion)
{
    {% if 'singleton' in interface.tags %}
    qmlRegisterSingletonType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{interface}}", {{class|lower}}_singletontype_provider);
    {% else %}
    qmlRegisterType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{interface}}");
    {% endif %}
}
