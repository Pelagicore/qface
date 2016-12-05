{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}'.format(interface) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#include "{{class|lower}}.h"

#include <QtQml>

{{interface.comment}}
{{class}}::{{class}}(QObject *parent)
    : QmlAbstract{{interface}}(parent)
{
}

void {{class}}::registerQmlTypes(const QString& uri, int majorVersion, int minorVersion)
{
    qmlRegisterType<{{class}}>(uri.toLatin1(), majorVersion, minorVersion, "{{interface}}");
}
