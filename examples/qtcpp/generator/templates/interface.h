{# Copyright (c) Pelagicore AB 2016 #}
{% set class = 'Qml{0}'.format(interface) %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/

#pragma once

#include <QtCore>

#include "generated/qml{{module.module_name|lower}}module.h"
#include "generated/qmlabstract{{interface|lower}}.h"

class {{class}} : public QmlAbstract{{interface}}
{
    Q_OBJECT
public:
    {{class}}(QObject *parent=0);

    static void registerQmlTypes(const QString& uri, int majorVersion=1, int minorVersion=0);
};
