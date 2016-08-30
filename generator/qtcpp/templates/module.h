{% from 'helper.tpl' import module %}
/****************************************************************************
** This is an auto-generated file.
** Do not edit! All changes made to it will be lost.
****************************************************************************/
{% set module = module(package) %}
{% set class = 'Qml{0}'.format(module) %}

#pragma once

{% for struct in package.structs %}
#include "{{struct|lower}}.h"
#include "{{struct|lower}}model.h"
{% endfor %}

class {{class}} : public QObject {
    Q_OBJECT
public:
    {{class}}(QObject *parent=0);

{% for enum in package.enums %}
    {% set comma = joiner(",") %}
    enum {{enum}} { 
        {%- for member in enum.members -%}
        {{ comma() }}
        {{member.name}} = {{member.value}}
        {%- endfor %}
    };
    Q_ENUM({{enum}})
{% endfor %}

{% for struct in package.structs %}
    Q_INVOKABLE {{struct}} create{{struct}}();
{% endfor %}

    static void registerTypes();
    static void registerQmlTypes(const QString& uri, int majorVersion = 1, int minorVersion = 0);
};
