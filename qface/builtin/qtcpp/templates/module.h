{# Copyright (c) Pelagicore AB 2016 #}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/
{% set class = 'Qml{0}Module'.format(module.module_name) %}

#pragma once

#include <QtCore>

#include "qmlvariantmodel.h"
{% for struct in module.structs %}
#include "qml{{struct|lower}}.h"
#include "qml{{struct|lower}}model.h"
{% endfor %}

class {{class}} : public QObject {
    Q_OBJECT
public:
    {{class}}(QObject *parent = nullptr);

{% for enum in module.enums %}
    {% set comma = joiner(",") %}
    enum {{enum}} {
        {%- for member in enum.members -%}
        {{ comma() }}
        {{member.name}} = {{member.value}}
        {%- endfor %}

    };
    Q_ENUM({{enum}})
{% endfor %}

{% for struct in module.structs %}
    Q_INVOKABLE Qml{{struct}} create{{struct}}();
{% endfor %}

    static void registerTypes();
    static void registerQmlTypes(const QString& uri, int majorVersion = 1, int minorVersion = 0);
};
