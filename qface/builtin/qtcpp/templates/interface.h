{# Copyright (c) Pelagicore AB 2016 #}
{% import "qtcpp.j2" as cpp %}
{{ cpp.preserved() }}
{% set class = '{0}'.format(interface) %}

#pragma once

#include <QtCore>

#include "generated/{{module.module_name|lower}}module.h"
#include "generated/abstract{{interface|lower}}.h"

class {{class}} : public Abstract{{interface}}
{
    Q_OBJECT
public:
    {{class}}(QObject *parent = nullptr);
    virtual ~{{class}}();

    static void registerQmlTypes(const QString& uri, int majorVersion=1, int minorVersion=0);
};
